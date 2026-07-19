"""
Main API endpoint for AI tool recommendations
"""
import os
import json
import logging
import time
import uuid
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.getLevelName(os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import our modules
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from recommendation_engine import get_recommendation_engine
from utils.validators import validate_task_input
from utils.formatters import format_error_response, format_success_response
from utils.logger import log_event

# Rate limiting (simple in-memory)
_rate_limit_store = {}
RATE_LIMIT = int(os.getenv('RATE_LIMIT', '100'))
RATE_WINDOW = 3600  # 1 hour

API_VERSION = '1.0.0'


def check_rate_limit(ip: str) -> bool:
    """Check if IP has exceeded rate limit"""
    now = time.time()

    if ip not in _rate_limit_store:
        _rate_limit_store[ip] = []

    # Remove old requests outside the window
    _rate_limit_store[ip] = [
        t for t in _rate_limit_store[ip]
        if now - t < RATE_WINDOW
    ]

    # Check limit
    if len(_rate_limit_store[ip]) >= RATE_LIMIT:
        return False

    # Add current request
    _rate_limit_store[ip].append(now)
    return True


class handler(BaseHTTPRequestHandler):
    """Vercel serverless function handler"""

    def _get_client_id(self) -> str:
        return self.headers.get('X-Client-Id') or str(uuid.uuid4())

    def _send_json(self, status_code: int, payload: dict, client_id: str = None):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self._send_cors_headers()
        if client_id:
            self.send_header('X-Client-Id', client_id)
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def _send_cors_headers(self):
        """Send CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Client-Id')

    def do_OPTIONS(self):
        """Handle OPTIONS preflight requests"""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        parsed = urlparse(self.path)
        client_id = self._get_client_id()

        if parsed.path == '/api/health':
            self._send_json(200, {
                'status': 'healthy',
                'version': API_VERSION,
                'clientId': client_id,
            }, client_id)
            return

        if parsed.path == '/api/models':
            from airtable_client import get_airtable_client
            from openrouter_client import get_openrouter_client
            from recommendation_engine import merge_models

            params = parse_qs(parsed.query)
            category = params.get('category', [''])[0]
            limit = int(params.get('limit', ['50'])[0])
            
            airtable_models = get_airtable_client().fetch_models()
            openrouter_models = get_openrouter_client().fetch_models()
            models = merge_models(airtable_models, openrouter_models)
            
            if category:
                models = [m for m in models if m.get('category', '').lower() == category.lower()]
            self._send_json(200, {'models': models[:limit], 'count': len(models), 'clientId': client_id}, client_id)
            log_event(logger, 'models_listed', clientId=client_id, category=category or 'all', limit=limit)
            return

        # Return 404 for other GET requests
        self._send_json(404, {'error': 'Not Found', 'message': 'Endpoint not found'}, client_id)

    def do_POST(self):
        """Handle POST requests"""
        parsed = urlparse(self.path)
        client_id = self._get_client_id()
        # Get client IP for rate limiting
        ip = self.headers.get('X-Forwarded-For', self.client_address[0])

        # Check rate limit
        if not check_rate_limit(ip):
            logger.warning(f"Rate limit exceeded for IP: {ip}")
            self._send_json(429, {
                'error': 'Rate limit exceeded',
                'message': f'Maximum {RATE_LIMIT} requests per hour',
                'clientId': client_id,
            }, client_id)
            return

        if parsed.path != '/api/recommend':
            self._send_json(404, {'error': 'Not Found', 'message': 'Endpoint not found', 'clientId': client_id}, client_id)
            return

        # Read request body
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self._send_json(400, {
                'error': 'Bad Request',
                'message': 'Request body is required',
                'clientId': client_id,
            }, client_id)
            return

        try:
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            self._send_json(400, {
                'error': 'Invalid JSON',
                'message': str(e),
                'clientId': client_id,
            }, client_id)
            return

        # Validate input
        try:
            task_description = data.get('taskDescription', '')
            category = data.get('category', '')
            validate_task_input(task_description)
        except ValueError as e:
            self._send_json(400, {
                'error': 'Validation Error',
                'message': str(e),
                'clientId': client_id,
            }, client_id)
            return

        # Get recommendation
        try:
            engine = get_recommendation_engine()
            recommendation = engine.get_recommendation(
                task_description=task_description,
                category=category if category else None
            )

            # Send success response
            payload = dict(recommendation)
            payload['clientId'] = client_id
            self._send_json(200, payload, client_id)
            log_event(logger, 'recommend_generated', clientId=client_id, category=category or 'all', taskLength=len(task_description))

        except ValueError as e:
            logger.error(f"Validation error: {e}")
            self._send_json(400, {
                'error': 'Bad Request',
                'message': str(e),
                'clientId': client_id,
            }, client_id)

        except Exception as e:
            logger.exception("Error generating recommendation")
            self._send_json(500, {
                'error': 'Internal Server Error',
                'message': 'Failed to generate recommendation. Please try again.',
                'clientId': client_id,
            }, client_id)


# For local testing
if __name__ == '__main__':
    from http.server import HTTPServer

    port = 3000
    server = HTTPServer(('localhost', port), handler)
    print(f"Server running on http://localhost:{port}")
    server.serve_forever()

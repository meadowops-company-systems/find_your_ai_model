"""
Airtable Client - Fetches AI model data from Airtable
"""
import os
import logging
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Cache for storing Airtable data
_cache = {}
_cache_ttl = 300  # 5 minutes
_cache_timestamp = None


MOCK_MODELS = [
    # Coding
    {
        'id': 'mock-claude35sonnet',
        'name': 'Claude 3.5 Sonnet',
        'description': 'Anthropic\'s state-of-the-art model setting industry benchmarks for coding and precise technical tasks.',
        'category': 'coding',
        'website': 'https://claude.ai',
        'pricing': 'Free tier / Pro $20/mo',
        'features': ['Coding', 'Artifacts', 'Document analysis', 'Precise reasoning'],
        'best_for': 'Advanced programming, debugging, and precise technical writing',
        'free_tier': True,
        'api': True
    },
    {
        'id': 'mock-gpt4o',
        'name': 'GPT-4o',
        'description': 'OpenAI\'s flagship multimodal model, excellent for complex reasoning, coding, writing, and analysis.',
        'category': 'coding',
        'website': 'https://openai.com/gpt-4',
        'pricing': 'Free tier / Pro $20/mo',
        'features': ['Coding', 'Reasoning', 'Vision', 'Multimodal'],
        'best_for': 'Complex coding tasks and deep analytical research',
        'free_tier': True,
        'api': True
    },
    {
        'id': 'mock-cursor',
        'name': 'Cursor',
        'description': 'An AI-first code editor built around VS Code, enabling seamless codebase-wide generation and edits.',
        'category': 'coding',
        'website': 'https://cursor.sh',
        'pricing': 'Free tier / Pro $20/mo',
        'features': ['Codebase indexing', 'Tab autocomplete', 'Composer multi-file edit'],
        'best_for': 'Speeding up software engineering workflow',
        'free_tier': True,
        'api': False
    },
    # Writing
    {
        'id': 'mock-claude35sonnet-writing',
        'name': 'Claude 3.5 Sonnet',
        'description': 'Anthropic\'s state-of-the-art model with a highly natural, sophisticated, and conversational writing tone.',
        'category': 'writing',
        'website': 'https://claude.ai',
        'pricing': 'Free tier / Pro $20/mo',
        'features': ['Natural writing', 'Creative storytelling', 'Analysis'],
        'best_for': 'Articles, essays, copywriting, and professional documentation',
        'free_tier': True,
        'api': True
    },
    {
        'id': 'mock-jasper',
        'name': 'Jasper AI',
        'description': 'Enterprise-grade copy generator optimized for marketing campaigns, SEO optimization, and brand voice consistency.',
        'category': 'writing',
        'website': 'https://jasper.ai',
        'pricing': 'From $39/mo',
        'features': ['Brand voice training', 'SEO templates', 'Campaign tools'],
        'best_for': 'Marketing copy, blog posts, and scaling content production',
        'free_tier': False,
        'api': False
    },
    {
        'id': 'mock-copyai',
        'name': 'Copy.ai',
        'description': 'An AI content generator designed to help marketing teams draft blog posts, social media, and ad copy.',
        'category': 'writing',
        'website': 'https://copy.ai',
        'pricing': 'Free tier / Pro $36/mo',
        'features': ['Social media templates', 'Workflow automation', 'Ad copy templates'],
        'best_for': 'Fast social media drafts and email marketing templates',
        'free_tier': True,
        'api': False
    },
    # Image Generation
    {
        'id': 'mock-midjourney',
        'name': 'Midjourney v6',
        'description': 'The gold standard for artistic, realistic, and highly detailed AI image generation via Discord.',
        'category': 'image',
        'website': 'https://midjourney.com',
        'pricing': 'From $10/mo',
        'features': ['Photorealism', 'Artistic styles', 'Text rendering'],
        'best_for': 'Stunning illustrations, concept art, and photorealistic assets',
        'free_tier': False,
        'api': False
    },
    {
        'id': 'mock-dalle3',
        'name': 'DALL-E 3',
        'description': 'OpenAI\'s native image generator, built directly into ChatGPT, known for exceptional prompt adherence.',
        'category': 'image',
        'website': 'https://openai.com/dall-e-3',
        'pricing': 'Included in ChatGPT Plus ($20/mo)',
        'features': ['Prompt adherence', 'Text generation in images', 'Vibrant styles'],
        'best_for': 'Quick, precise illustrations and cartoon or graphic assets',
        'free_tier': False,
        'api': True
    },
    {
        'id': 'mock-stablediffusion3',
        'name': 'Stable Diffusion 3',
        'description': 'State-of-the-art open weights image model, offering excellent text rendering and highly customizable settings.',
        'category': 'image',
        'website': 'https://stability.ai',
        'pricing': 'Free local run / API pricing varies',
        'features': ['Open source', 'High customization', 'Excellent text generation'],
        'best_for': 'Local deployments, developer APIs, and deep control over image structure',
        'free_tier': True,
        'api': True
    },
    # Audio & Music
    {
        'id': 'mock-suno',
        'name': 'Suno AI v3.5',
        'description': 'Generate full-length songs, vocals, lyrics, and instrumentals from descriptive text prompts in minutes.',
        'category': 'audio',
        'website': 'https://suno.com',
        'pricing': '50 free credits daily / Paid from $8/mo',
        'features': ['Vocal generation', 'Full song structures', 'Multi-genre support'],
        'best_for': 'Creating complete songs, background tracks, and catchy jingles',
        'free_tier': True,
        'api': False
    },
    {
        'id': 'mock-udio',
        'name': 'Udio',
        'description': 'Highly expressive AI music generation, capturing high-fidelity instrumentals and professional vocals.',
        'category': 'audio',
        'website': 'https://udio.com',
        'pricing': 'Free tier / Pro $10/mo',
        'features': ['High-fidelity audio', 'Extending tracks', 'Lyrics upload'],
        'best_for': 'Professional quality music, vocals, and sound design',
        'free_tier': True,
        'api': False
    },
    {
        'id': 'mock-whisper',
        'name': 'Whisper v3',
        'description': 'OpenAI\'s open-source speech-to-text model, offering near-human accuracy across multiple languages.',
        'category': 'audio',
        'website': 'https://openai.com/research/whisper',
        'pricing': 'Free open source / API $0.006/min',
        'features': ['Transcription', 'Translation', 'Multi-language support'],
        'best_for': 'Subtitling, dictation, transcribing interviews, and meeting notes',
        'free_tier': True,
        'api': True
    },
    # Video & Animation
    {
        'id': 'mock-runway',
        'name': 'Runway Gen-3 Alpha',
        'description': 'A major leap forward in high-fidelity video generation, providing cinematic control and fidelity.',
        'category': 'video',
        'website': 'https://runwayml.com',
        'pricing': 'Free tier / Pro from $12/mo',
        'features': ['High fidelity', 'Camera motion control', 'Text to video'],
        'best_for': 'Cinematic video clips, visual effects, and advanced motion graphics',
        'free_tier': True,
        'api': True
    },
    {
        'id': 'mock-sora',
        'name': 'Sora',
        'description': 'OpenAI\'s text-to-video model capable of generating videos up to a minute long with high visual quality.',
        'category': 'video',
        'website': 'https://openai.com/sora',
        'pricing': 'Access restricted / API pricing varies',
        'features': ['Photorealism', 'Extended length', 'Complex physics simulation'],
        'best_for': 'Creating long photorealistic scenes and premium video content',
        'free_tier': False,
        'api': True
    },
    # Data & Analytics
    {
        'id': 'mock-julius',
        'name': 'Julius AI',
        'description': 'An advanced AI data scientist that can write code, analyze data, and build interactive charts from CSVs.',
        'category': 'data',
        'website': 'https://julius.ai',
        'pricing': 'Free tier / Pro $20/mo',
        'features': ['Data analysis', 'Chart plotting', 'Mathematical reasoning'],
        'best_for': 'Analyzing complex spreadsheets, datasets, and plotting statistics',
        'free_tier': True,
        'api': False
    },
    {
        'id': 'mock-chatgpt-data',
        'name': 'ChatGPT Advanced Data Analysis',
        'description': 'Built-in sandboxed Python environment inside ChatGPT Plus for executing scripts and manipulating files.',
        'category': 'data',
        'website': 'https://openai.com/chatgpt',
        'pricing': 'Included in ChatGPT Plus ($20/mo)',
        'features': ['Python execution', 'File upload/download', 'Visualization'],
        'best_for': 'On-the-fly Python scripting, data wrangling, and file conversion',
        'free_tier': False,
        'api': False
    },
    # Research & Learning
    {
        'id': 'mock-perplexity',
        'name': 'Perplexity Pro',
        'description': 'An answer engine that searches the live web and provides synthesized answers with precise inline citations.',
        'category': 'research',
        'website': 'https://perplexity.ai',
        'pricing': 'Free tier / Pro $20/mo',
        'features': ['Live web search', 'Source citations', 'Copilot mode'],
        'best_for': 'Academic research, market analysis, and quick fact checking with sources',
        'free_tier': True,
        'api': True
    },
    {
        'id': 'mock-consensus',
        'name': 'Consensus',
        'description': 'A research assistant that searches over 200 million academic papers to provide consensus-based answers.',
        'category': 'research',
        'website': 'https://consensus.app',
        'pricing': 'Free tier / Pro $9.99/mo',
        'features': ['Scientific search', 'Synthesized paper summaries', 'Citations'],
        'best_for': 'Finding peer-reviewed research papers and scientific consensus',
        'free_tier': True,
        'api': False
    },
    # Productivity
    {
        'id': 'mock-notion',
        'name': 'Notion AI',
        'description': 'Integrated directly into your Notion workspace to help you summarize, write, autofill databases, and brainstorm.',
        'category': 'productivity',
        'website': 'https://notion.so',
        'pricing': 'Add-on $10/month',
        'features': ['Workspace integration', 'Document summarization', 'Database automation'],
        'best_for': 'Organizing notes, summarizing wikis, and drafting docs inline',
        'free_tier': False,
        'api': False
    },
    {
        'id': 'mock-grammarly',
        'name': 'Grammarly Premium',
        'description': 'Real-time writing assistant providing grammar corrections, tone adjustments, and vocabulary suggestions.',
        'category': 'productivity',
        'website': 'https://grammarly.com',
        'pricing': 'Free tier / Premium $12/mo',
        'features': ['Grammar check', 'Tone adjustment', 'Plagiarism detection'],
        'best_for': 'Polishing emails, business documents, and professional writing',
        'free_tier': True,
        'api': False
    }
]


class AirtableClient:
    """Client for interacting with Airtable API"""

    def __init__(self):
        self.api_key = os.getenv('AIRTABLE_API_KEY')
        self.base_id = os.getenv('AIRTABLE_BASE_ID')
        self.table_name = os.getenv('AIRTABLE_TABLE_NAME', 'AI Models')
        self.base_url = f"https://api.airtable.com/v0/{self.base_id}/{self.table_name}"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def fetch_models(self, force_refresh: bool = False) -> List[Dict]:
        """
        Fetch all AI models from Airtable with caching.

        Args:
            force_refresh: If True, bypass cache and fetch fresh data

        Returns:
            List of AI model dictionaries
        """
        global _cache, _cache_timestamp

        # Check cache validity
        if not force_refresh and _cache.get('models'):
            import time
            if _cache_timestamp and (time.time() - _cache_timestamp) < _cache_ttl:
                logger.info("Returning cached models")
                return _cache['models']

        # Fetch from Airtable
        try:
            logger.info("Fetching models from Airtable")
            all_models = []
            offset = None

            while True:
                params = {'pageSize': 100}
                if offset:
                    params['offset'] = offset

                response = requests.get(
                    self.base_url,
                    headers=self.headers,
                    params=params,
                    timeout=30
                )
                response.raise_for_status()

                data = response.json()
                records = data.get('records', [])

                for record in records:
                    model = self._parse_record(record)
                    if model:
                        all_models.append(model)

                offset = data.get('offset')
                if not offset:
                    break

            if not all_models:
                logger.warning("Fetched 0 valid models from Airtable, falling back to local mock models")
                all_models = MOCK_MODELS

            # Update cache
            _cache['models'] = all_models
            import time
            _cache_timestamp = time.time()

            logger.info(f"Fetched {len(all_models)} models")
            return all_models

        except requests.RequestException as e:
            logger.error(f"Airtable request failed: {e}. Falling back to local mock models.")
            # Return cached data if available, even if expired
            if _cache.get('models'):
                logger.info("Returning stale cache due to error")
                return _cache['models']
            
            logger.info("Returning local mock models")
            return MOCK_MODELS

    def _parse_record(self, record: Dict) -> Optional[Dict]:
        """Parse Airtable record into simplified model dict"""
        fields = record.get('fields', {})

        # Support both 'Model Name' (custom schema) and 'Name' (standard schema)
        name = fields.get('Model Name') or fields.get('Name')
        if not name:
            return None

        # Determine description/notes
        description = fields.get('Notes') or fields.get('Description', '')

        # Map and normalize category
        category_raw = fields.get('Primary Category') or fields.get('Category', 'General')
        category_raw = str(category_raw).lower()
        if category_raw == 'text':
            # Classify 'Text' models based on name/ID
            if 'perplexity' in name.lower() or 'sonar' in name.lower() or 'search' in name.lower():
                category = 'research'
            else:
                category = 'writing'
        elif category_raw in ['audio', 'image', 'video', 'coding', 'data', 'research', 'productivity']:
            category = category_raw
        else:
            category = category_raw

        # Website
        website = fields.get('Official URL') or fields.get('Website', '')

        # Build clean pricing string
        monthly_price = fields.get('Monthly Price(USD)')
        if monthly_price is None:
            monthly_price = fields.get('Monthly Price', 0)
        
        pricing_type_list = fields.get('Pricing Type', [])
        pricing_type_str = "".join(pricing_type_list) if isinstance(pricing_type_list, list) else str(pricing_type_list)
        free_tier_details = fields.get('Free Tier Details', '')
        
        is_free_tier = 'free_tier' in pricing_type_str or 'free' in free_tier_details.lower() or fields.get('Free Tier', False)
        
        pricing_parts = []
        if is_free_tier:
            pricing_parts.append("Free tier")
        if isinstance(monthly_price, (int, float)) and monthly_price > 0:
            pricing_parts.append(f"Pro ${monthly_price}/mo")
        
        if not pricing_parts:
            pricing_str = fields.get('Pricing', 'Free')
        else:
            pricing_str = " / ".join(pricing_parts)

        # Parse strengths into features list
        strengths_raw = fields.get('Strenghts') or fields.get('Strengths')
        if strengths_raw:
            features = [s.strip() for s in strengths_raw.split('|') if s.strip()]
        else:
            features_raw = fields.get('Features', [])
            if isinstance(features_raw, list):
                features = features_raw
            else:
                features = [features_raw] if features_raw else []

        # Parse best_for
        best_for_raw = fields.get('Best For', '')
        if isinstance(best_for_raw, list):
            best_for_str = ", ".join(best_for_raw)
        else:
            best_for_str = str(best_for_raw)
        best_for_str = best_for_str.replace(';', ', ').replace('_', ' ')

        # API capabilities
        api_docs_url = fields.get('API Docs URL')
        is_api = 'api' in pricing_type_str or bool(api_docs_url) or fields.get('API', False)

        return {
            'id': fields.get('Model ID') or record.get('id'),
            'name': name,
            'description': description,
            'category': category,
            'website': website,
            'pricing': pricing_str,
            'features': features,
            'best_for': best_for_str,
            'free_tier': is_free_tier,
            'api': is_api,
        }

    def get_models_by_category(self, category: str) -> List[Dict]:
        """Get models filtered by category"""
        all_models = self.fetch_models()
        if not category:
            return all_models
        return [m for m in all_models if m.get('category', '').lower() == category.lower()]


# Singleton instance
_client = None


def get_airtable_client() -> AirtableClient:
    """Get or create Airtable client singleton"""
    global _client
    if _client is None:
        _client = AirtableClient()
    return _client

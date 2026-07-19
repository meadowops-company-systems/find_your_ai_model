"""
OpenRouter Client - Interfaces with OpenRouter API for AI recommendations
"""
import os
import json
import logging
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


_models_cache = {}
_models_cache_ttl = 300
_models_cache_timestamp = None


class OpenRouterClient:
    """Client for interacting with OpenRouter API"""

    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = os.getenv('OPENROUTER_MODEL', 'openai/gpt-oss-20b:free')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': os.getenv('REFERER', 'https://findyouraimodel.com'),
            'X-Title': 'Find Your AI Model'
        }

    def get_recommendation(
        self,
        task_description: str,
        models: List[Dict],
        category: Optional[str] = None
    ) -> Dict:
        """
        Get AI recommendation for the best tool based on task description.

        Args:
            task_description: User's task description
            models: List of available AI models/tools
            category: Optional category filter

        Returns:
            Dictionary with recommendation data
        """
        # Prepare models list for the prompt
        models_info = self._format_models_for_prompt(models, category)

        # Build the prompt
        prompt = self._build_prompt(task_description, models_info)

        try:
            logger.info("Calling OpenRouter API for recommendation")
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    'model': self.model,
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'You are an AI tool expert helping users find the perfect AI tool for their specific tasks. You must respond with ONLY valid JSON, no other text.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    'temperature': 0.3,
                    'max_tokens': 2000
                },
                timeout=15
            )
            response.raise_for_status()

            data = response.json()
            content = data['choices'][0]['message']['content']

            # Parse JSON response
            recommendation = json.loads(content)
            return self._validate_recommendation(recommendation, models)

        except Exception as e:
            logger.error(f"OpenRouter request/parsing failed: {e}. Falling back to local match engine.")
            return self.get_local_recommendation(task_description, models, category)

    def get_local_recommendation(
        self,
        task_description: str,
        models: List[Dict],
        category: Optional[str] = None
    ) -> Dict:
        """Fallback recommendation generator that runs locally without API calls"""
        logger.info(f"Generating local recommendation for category: {category}")
        
        # 1. Filter models by category if provided, otherwise search all
        filtered_models = models
        if category:
            filtered_models = [m for m in models if m.get('category', '').lower() == category.lower()]
            
        if not filtered_models:
            filtered_models = models
            
        # 2. Match keywords to find the best tool
        task_lower = task_description.lower()
        
        # Determine likely category from keywords if not provided
        inferred_category = category
        if not inferred_category:
            keywords = {
                'coding': ['code', 'python', 'script', 'programming', 'js', 'html', 'css', 'develop', 'react', 'bug', 'debug'],
                'writing': ['write', 'blog', 'post', 'article', 'essay', 'copy', 'content', 'marketing', 'ad'],
                'image': ['image', 'art', 'draw', 'paint', 'photograph', 'logo', 'design', 'picture'],
                'audio': ['audio', 'music', 'song', 'voice', 'whisper', 'speech', 'transcript', 'sing'],
                'video': ['video', 'movie', 'film', 'animation', 'clip'],
                'data': ['data', 'excel', 'csv', 'analysis', 'chart', 'plot', 'statistic', 'math'],
                'research': ['research', 'paper', 'search', 'find', 'learn', 'study', 'academic'],
                'productivity': ['note', 'organize', 'summarize', 'meeting', 'grammar', 'calendar']
            }
            for cat, words in keywords.items():
                if any(w in task_lower for w in words):
                    inferred_category = cat
                    break
        
        # If we still don't have a category, default to coding or writing
        if not inferred_category:
            inferred_category = 'coding'
            
        # Group models by category
        cat_models = [m for m in filtered_models if m.get('category', '').lower() == inferred_category.lower()]
        if not cat_models:
            cat_models = filtered_models
            
        # Sort or select primary and alternatives
        if len(cat_models) >= 1:
            best_model = cat_models[0]
            # alternatives are remaining models
            alt_candidates = cat_models[1:4]
            # if we don't have enough, pull from other categories
            if len(alt_candidates) < 2:
                other_models = [m for m in filtered_models if m.get('id') != best_model.get('id')]
                alt_candidates.extend(other_models[:3-len(alt_candidates)])
        else:
            # Absolute fallback
            best_model = models[0] if models else {
                'name': 'Claude 3.5 Sonnet',
                'category': 'coding',
                'description': 'Advanced AI assistant',
                'pricing': 'Free tier / Pro $20/mo',
                'website': 'https://claude.ai',
                'features': ['Coding', 'Writing']
            }
            alt_candidates = models[1:3] if len(models) > 1 else []

        # Construct payload with scores
        primary_score = 95 if inferred_category in ['coding', 'writing', 'research'] else 91
        
        recommendation = {
            "primary": {
                "name": best_model.get('name'),
                "matchScore": primary_score,
                "reason": f"Perfect match for your needs because it is highly optimized for {inferred_category} tasks and offers top-tier output quality.",
                "description": best_model.get('description', ''),
                "website": best_model.get('website', ''),
                "features": best_model.get('features', []),
                "pricing": best_model.get('pricing', ''),
                "category": best_model.get('category', '')
            },
            "alternatives": [],
            "reasoning": f"Based on your task description, we recommend {best_model.get('name')} as the primary option due to its strong performance in {inferred_category} use cases. If you need alternative capabilities or a different pricing structure, consider the other options."
        }
        
        # Add alternatives with scores
        base_score = primary_score - 4
        for idx, alt in enumerate(alt_candidates):
            recommendation["alternatives"].append({
                "name": alt.get('name'),
                "matchScore": base_score - (idx * 3),
                "reason": f"Excellent alternative offering specialized features for {inferred_category} workflows.",
                "description": alt.get('description', ''),
                "website": alt.get('website', ''),
                "features": alt.get('features', []),
                "pricing": alt.get('pricing', '')
            })
            
        return recommendation

    def _format_models_for_prompt(self, models: List[Dict], category: Optional[str]) -> str:
        """Format models list for inclusion in prompt"""
        filtered = models
        if category:
            filtered = [m for m in models if m.get('category', '').lower() == category.lower()]

        # Limit to top 50 for prompt length
        models_to_show = filtered[:50]

        lines = []
        for i, model in enumerate(models_to_show, 1):
            lines.append(f"""
{i}. {model.get('name', 'Unknown')}
   Category: {model.get('category', 'General')}
   Best for: {model.get('best_for', 'General use')}
   Pricing: {model.get('pricing', 'Unknown')}
   Features: {', '.join(model.get('features', [])[:5])}
""")

        return '\n'.join(lines)

    def _build_prompt(self, task_description: str, models_info: str) -> str:
        """Build the prompt for the AI"""
        return f"""Analyze the following task and recommend the best AI tool from the list below.

Task: {task_description}

Available AI Tools:
{models_info}

Respond with ONLY a JSON object in this exact format (no other text):
{{
    "primary": {{
        "name": "Tool Name",
        "matchScore": 85,
        "reason": "Short explanation why this tool is best for the task"
    }},
    "alternatives": [
        {{
            "name": "Alternative Tool Name",
            "matchScore": 70,
            "reason": "Why this is a good alternative"
        }}
    ],
    "reasoning": "Brief explanation of the recommendation"
}}

Important:
- matchScore should be 0-100
- Include 2-3 alternatives maximum
- Consider pricing, features, and best use case when recommending
- If a category was specified, prioritize tools in that category"""

    def _validate_recommendation(self, recommendation: Dict, models: List[Dict]) -> Dict:
        """Validate and enrich recommendation with full model data"""
        if not recommendation:
            raise ValueError("Empty recommendation")

        primary = recommendation.get('primary')
        if not isinstance(primary, dict):
            primary = {}
            recommendation['primary'] = primary

        primary_name = primary.get('name')
        
        alt_list = recommendation.get('alternatives')
        if not isinstance(alt_list, list):
            alt_list = []
            recommendation['alternatives'] = alt_list

        model_map = {}
        for m in models:
            m_name = m.get('name')
            if m_name:
                model_map[str(m_name).lower()] = m

        # Enrich primary
        if primary_name:
            primary_lower = str(primary_name).lower()
            if primary_lower in model_map:
                full_model = model_map[primary_lower]
                primary.update({
                    'description': full_model.get('description', ''),
                    'website': full_model.get('website', ''),
                    'features': full_model.get('features', []),
                    'pricing': full_model.get('pricing', ''),
                    'category': full_model.get('category', '')
                })

        # Enrich alternatives
        for alt in alt_list:
            if isinstance(alt, dict):
                alt_name = alt.get('name')
                if alt_name:
                    alt_lower = str(alt_name).lower()
                    if alt_lower in model_map:
                        full_model = model_map[alt_lower]
                        alt.update({
                            'description': full_model.get('description', ''),
                            'website': full_model.get('website', ''),
                            'features': full_model.get('features', []),
                            'pricing': full_model.get('pricing', '')
                        })

        return recommendation

    def fetch_models(self, force_refresh: bool = False) -> List[Dict]:
        """
        Fetch all models from OpenRouter and map them to our internal model format.
        """
        global _models_cache, _models_cache_timestamp
        import time
        
        if not force_refresh and _models_cache.get('models'):
            if _models_cache_timestamp and (time.time() - _models_cache_timestamp) < _models_cache_ttl:
                logger.info("Returning cached OpenRouter models")
                return _models_cache['models']
                
        try:
            logger.info("Fetching models from OpenRouter API")
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers,
                timeout=15
            )
            response.raise_for_status()
            data = response.json()
            raw_models = data.get('data', [])
            
            parsed_models = []
            for rm in raw_models:
                model_id = rm.get('id')
                name = rm.get('name')
                if not model_id or not name:
                    continue
                    
                # Categorize based on keywords in name or id
                category = self._classify_category(model_id, name)
                
                # Pricing
                pricing_data = rm.get('pricing', {})
                prompt_price = float(pricing_data.get('prompt', 0))
                completion_price = float(pricing_data.get('completion', 0))
                
                if prompt_price == 0.0 and completion_price == 0.0:
                    pricing_str = "Free"
                    free_tier = True
                elif prompt_price < 0.0 or completion_price < 0.0:
                    pricing_str = "Varies"
                    free_tier = False
                else:
                    prompt_1m = prompt_price * 1000000
                    completion_1m = completion_price * 1000000
                    pricing_str = f"${prompt_1m:.2f}/M prompt, ${completion_1m:.2f}/M completion"
                    free_tier = False
                    
                # Features
                features = ["Text Generation", "API Access", "OpenRouter"]
                if category == "coding":
                    features.insert(0, "Coding")
                    features.insert(1, "Autocompletion")
                elif category == "image":
                    features = ["Image Generation", "API Access", "Visuals"]
                elif category == "audio":
                    features = ["Audio Processing", "API Access"]
                elif category == "video":
                    features = ["Video Generation", "API Access"]
                
                # Description
                desc = rm.get('description', '')
                if not desc:
                    desc = f"High-performance AI model hosted on OpenRouter for {category} workflows."
                    
                parsed_models.append({
                    'id': model_id,
                    'name': name,
                    'description': desc,
                    'category': category,
                    'website': f"https://openrouter.ai/models/{model_id}",
                    'pricing': pricing_str,
                    'features': features,
                    'best_for': f"Advanced language processing and {category} tasks.",
                    'free_tier': free_tier,
                    'api': True
                })
                
            _models_cache['models'] = parsed_models
            _models_cache_timestamp = time.time()
            logger.info(f"Fetched {len(parsed_models)} models from OpenRouter")
            return parsed_models
            
        except Exception as e:
            logger.error(f"Failed to fetch models from OpenRouter: {e}")
            if _models_cache.get('models'):
                logger.info("Returning stale cached OpenRouter models due to request failure")
                return _models_cache['models']
            return []

    def _classify_category(self, model_id: str, name: str) -> str:
        """Helper to classify model based on name or ID keywords"""
        text = f"{model_id} {name}".lower()
        
        if any(w in text for w in ["code", "coder", "starcoder", "deepseek-coder", "wizardcoder", "codellama", "qwen-coder", "stable-code", "phind", "sql"]):
            return "coding"
        if any(w in text for w in ["image", "stable-diffusion", "dall-e", "flux", "midjourney", "diffusion", "paint", "draw", "art", "sdxl", "pixel"]):
            return "image"
        if any(w in text for w in ["audio", "whisper", "tts", "speech", "voice", "music", "suno", "udio"]):
            return "audio"
        if any(w in text for w in ["video", "sora", "gen-3", "runway", "motion", "clip", "film"]):
            return "video"
        if any(w in text for w in ["data", "math", "julius", "excel", "csv", "statistic", "calculator", "analysis"]):
            return "data"
        if any(w in text for w in ["search", "perplexity", "consensus", "find", "academic", "research", "paper"]):
            return "research"
        if any(w in text for w in ["notion", "grammarly", "calendar", "note", "productivity", "schedule"]):
            return "productivity"
            
        return "writing"


# Singleton instance
_client = None


def get_openrouter_client() -> OpenRouterClient:
    """Get or create OpenRouter client singleton"""
    global _client
    if _client is None:
        _client = OpenRouterClient()
    return _client

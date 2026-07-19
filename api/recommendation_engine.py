"""
Recommendation Engine - Coordinates between Airtable and OpenRouter
"""
import logging
import time
from typing import Dict, List, Optional

from airtable_client import get_airtable_client
from openrouter_client import get_openrouter_client

logger = logging.getLogger(__name__)


def normalize_model_name(name: str) -> str:
    """Normalize model name to facilitate comparison and deduplication"""
    name = str(name or '').lower().strip()
    # Remove common provider prefixes
    prefixes = ['openai:', 'anthropic:', 'google:', 'meta:', 'mistral:', 'cohere:', 'deepseek:', 'qwen:', 'microsoft:', 'replicate:']
    for p in prefixes:
        if name.startswith(p):
            name = name[len(p):].strip()
    return name


def merge_models(airtable_models: List[Dict], openrouter_models: List[Dict]) -> List[Dict]:
    """Merge and deduplicate models from Airtable and OpenRouter"""
    merged = {}
    
    # Process Airtable models first
    for m in airtable_models:
        name = m.get('name', '')
        normalized = normalize_model_name(name)
        if normalized:
            merged[normalized] = dict(m)  # Copy to avoid mutating cache
            
    # Process OpenRouter models
    for m in openrouter_models:
        name = m.get('name', '')
        normalized = normalize_model_name(name)
        if not normalized:
            continue
            
        if normalized in merged:
            # Model exists, enrich it
            existing = merged[normalized]
            existing['api'] = True
            if not existing.get('website') and m.get('website'):
                existing['website'] = m.get('website')
            # Store openrouter_id for routing if needed
            existing['openrouter_id'] = m.get('id')
        else:
            # New model from OpenRouter
            new_model = dict(m)
            new_model['openrouter_id'] = m.get('id')
            merged[normalized] = new_model
            
    # Return sorted list of models by name
    return sorted(merged.values(), key=lambda x: str(x.get('name') or '').lower())


class RecommendationEngine:
    """Engine for generating AI tool recommendations"""

    def __init__(self):
        self.airtable = get_airtable_client()
        self.openrouter = get_openrouter_client()

    def get_recommendation(
        self,
        task_description: str,
        category: Optional[str] = None
    ) -> Dict:
        """
        Generate a recommendation for the given task.

        Args:
            task_description: Detailed description of the user's task
            category: Optional category to filter tools

        Returns:
            Dictionary containing primary recommendation and alternatives
        """
        start_time = time.time()

        # Step 1: Fetch available models from Airtable and OpenRouter
        logger.info("Fetching models from Airtable and OpenRouter")
        airtable_models = self.airtable.fetch_models()
        openrouter_models = self.openrouter.fetch_models()
        models = merge_models(airtable_models, openrouter_models)

        if not models:
            raise ValueError("No AI models available")

        # Filter by category if specified
        if category:
            models = [m for m in models if m.get('category', '').lower() == category.lower()]
            logger.info(f"Filtered to {len(models)} models in category: {category}")

        # Step 2: Get recommendation from OpenRouter
        logger.info("Getting recommendation from OpenRouter")
        recommendation = self.openrouter.get_recommendation(
            task_description=task_description,
            models=models,
            category=category
        )

        # Step 3: Enhance response with additional data
        processing_time = int((time.time() - start_time) * 1000)

        # Add workflow steps for primary recommendation
        if recommendation.get('primary'):
            recommendation['primary']['workflow'] = self._generate_workflow(
                recommendation['primary']
            )

        # Add cost breakdown
        if recommendation.get('primary'):
            recommendation['primary']['cost'] = self._estimate_cost(
                recommendation['primary'].get('pricing', '')
            )

        # Add processing time
        recommendation['processingTime'] = processing_time

        logger.info(f"Recommendation generated in {processing_time}ms")
        return recommendation

    def _generate_workflow(self, tool: Dict) -> list:
        """Generate workflow steps for using the recommended tool"""
        name = str(tool.get('name') or '').lower()

        # Generic workflows based on tool category
        workflows = {
            'default': [
                'Visit the tool website and create an account',
                'Navigate to the main interface',
                'Enter or paste your task description',
                'Adjust settings if needed (tone, length, format)',
                'Generate and review the output',
                'Edit and refine as needed'
            ],
            'chatgpt': [
                'Go to chat.openai.com and log in',
                'Select GPT-4 or GPT-3.5',
                'Enter your task in the chat',
                'Refine with follow-up prompts',
                'Copy or export the output'
            ],
            'claude': [
                'Visit claude.ai and start a new chat',
                'Enter your detailed task',
                'Use the textarea for long inputs',
                'Iterate with follow-up questions',
                'Export or copy the final response'
            ],
            'midjourney': [
                'Join Discord server for Midjourney',
                'Use /imagine command with your prompt',
                'Upscale or vary the generated images',
                'Download the final image'
            ],
            'copy.ai': [
                'Sign up at copy.ai',
                'Choose a template or start fresh',
                'Enter your product/service details',
                'Generate and edit content',
                'Export in your preferred format'
            ]
        }

        # Check for specific tool matches
        for key, workflow in workflows.items():
            if key in name:
                return workflow

        return workflows['default']

    def _estimate_cost(self, pricing: str) -> Dict:
        """Estimate monthly cost based on pricing model"""
        pricing = str(pricing or '').lower()

        if 'free' in pricing:
            return {
                'monthly': 0,
                'yearly': 0,
                'tier': 'Free',
                'notes': 'Free tier available'
            }

        if 'freemium' in pricing:
            return {
                'monthly': 0,
                'yearly': 0,
                'tier': 'Freemium',
                'notes': 'Free tier with optional paid upgrades'
            }

        if 'monthly' in pricing or '/month' in pricing:
            # Try to extract price
            import re
            match = re.search(r'\$?(\d+)', pricing)
            if match:
                price = int(match.group(1))
                return {
                    'monthly': price,
                    'yearly': price * 12,
                    'tier': 'Paid',
                    'notes': f'Estimated ${price}/month'
                }

        # Default
        return {
            'monthly': None,
            'yearly': None,
            'tier': 'Varies',
            'notes': 'Check website for current pricing'
        }


# Singleton instance
_engine = None


def get_recommendation_engine() -> RecommendationEngine:
    """Get or create recommendation engine singleton"""
    global _engine
    if _engine is None:
        _engine = RecommendationEngine()
    return _engine

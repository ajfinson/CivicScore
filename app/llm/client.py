"""Generic OpenAI-style client wrapper"""
from openai import OpenAI
from app.config import settings


class LLMClient:
    """Wrapper for OpenAI-compatible API"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )
    
    def complete(self, prompt: str, model: str = "gpt-4", temperature: float = 0.0) -> str:
        """Send a completion request"""
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content
    
    def complete_json(self, prompt: str, model: str = "gpt-4") -> dict:
        """Send a completion request expecting JSON response"""
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        import json
        return json.loads(response.choices[0].message.content)


# Global client instance
llm_client = LLMClient()

import requests
from typing import Dict, Any


class LLMGateway:
    def __init__(self, api_key: str, base_url: str = "https://openrouter.ai/api/v1/chat/completions"):
        self.api_key = api_key
        self.base_url = base_url

    def generate_completion(self, prompt: str, model: str = "openai/gpt-3.5-turbo", **kwargs) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            **kwargs
        }
        response = requests.post(self.base_url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

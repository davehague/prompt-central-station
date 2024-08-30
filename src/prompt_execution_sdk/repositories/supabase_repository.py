# supabase_repository.py
import os
from supabase import create_client, Client
from typing import List, Optional
from .base import PromptRepository
from ..models.prompt import Prompt, PromptParameter, PromptConfig


def _convert_to_prompt(data: dict) -> Prompt:
    return Prompt(
        id=data['id'],
        name=data.get('name', ''),
        description=data.get('description', ''),
        tags=data.get('tags', []),
        parameters=[PromptParameter(**param) for param in data.get('parameters', [])],
        content=data['content'],
        config=PromptConfig(**data.get('config', {}))
    )


class SupabasePromptRepository(PromptRepository):
    def __init__(self):
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)

    def get_prompts_by_tag(self, tag: str) -> List[Prompt]:
        response = self.supabase.table("prompts").select("*").eq("tag", tag).execute()
        return [_convert_to_prompt(item) for item in response.data]

    def get_prompt_by_id(self, prompt_id: str) -> Optional[Prompt]:
        response = self.supabase.table("prompts").select("*").eq("id", prompt_id).limit(1).execute()
        if response.data:
            return _convert_to_prompt(response.data[0])
        return None

# base.py
from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.prompt import Prompt


class PromptRepository(ABC):
    @abstractmethod
    def get_prompts_by_tag(self, tag: str) -> List[Prompt]:
        pass

    @abstractmethod
    def get_prompt_by_id(self, prompt_id: str) -> Optional[Prompt]:
        pass

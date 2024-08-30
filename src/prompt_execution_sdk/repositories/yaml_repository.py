import os
import yaml
from typing import List, Optional
from .base import PromptRepository
from ..models.prompt import Prompt, PromptConfig, ModelInfo, ModelConfiguration, PromptParameter


def _convert_to_prompt(data: dict, file_path: str) -> Prompt:
    config = PromptConfig(
        name=data['name'],
        description=data['description'],
        version=data.get('version'),
        authors=data.get('authors', []),
        tags=data.get('tags', []),
        model=ModelInfo(
            api=data['model']['api'],
            configuration=ModelConfiguration(**data['model']['configuration']),
            parameters=data['model'].get('parameters', {}),
            response=data['model'].get('response', 'first')
        ),
        inputs={
            key: PromptParameter(**value)
            for key, value in data.get('inputs', {}).items()
        },
        outputs=data.get('outputs'),
        sample=data.get('sample')
    )

    return Prompt(
        config=config,
        template=data['template']
    )


class YAMLPromptRepository(PromptRepository):
    def __init__(self, base_path: str):
        self.base_path = base_path

    def get_prompts_by_tag(self, tag: str) -> List[Prompt]:
        prompts = []
        for root, _, files in os.walk(self.base_path):
            for file in files:
                if file.endswith('.yaml'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = yaml.safe_load(f)
                        if tag in data.get('tags', []):
                            prompts.append(_convert_to_prompt(data, file_path))
        return prompts

    def get_prompt_by_id(self, prompt_id: str) -> Optional[Prompt]:
        normalized_prompt_id = prompt_id.replace('\\', '/')
        file_path = os.path.join(self.base_path, normalized_prompt_id + '.yaml')

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
                return _convert_to_prompt(data, file_path)
        return None

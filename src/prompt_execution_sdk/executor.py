import time
from jinja2 import Template
from .repositories.base import PromptRepository
from .gateways.llm_gateway import LLMGateway
from .logging.logger import Logger


class PromptExecutor:
    def __init__(self, repository: PromptRepository, llm_gateway: LLMGateway, logger: Logger):
        self.repository = repository
        self.llm_gateway = llm_gateway
        self.logger = logger

    def execute_prompt(self, prompt_id: str, variables: dict = None):
        prompt = self.repository.get_prompt_by_id(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt with id {prompt_id} not found")

        # Use Jinja2 to format the prompt
        template = Template(prompt.template)
        formatted_prompt = template.render(**variables) if variables else prompt.template

        start_time = time.time()
        result = self.llm_gateway.generate_completion(
            formatted_prompt,
            model=f"{prompt.config.model.configuration.type}/{prompt.config.model.configuration.name}",
            **prompt.config.model.parameters
        )
        end_time = time.time()

        self.logger.log({
            "prompt_id": prompt_id,
            "variables": variables,
            "model": f"{prompt.config.model.configuration.type}/{prompt.config.model.configuration.name}",
            "execution_time": end_time - start_time,
            "result": result
        })

        return result

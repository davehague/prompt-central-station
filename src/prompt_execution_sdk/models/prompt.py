from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class ModelConfiguration(BaseModel):
    type: str
    name: str
    connection: Optional[str] = None
    azure_deployment: Optional[str] = None


class ModelInfo(BaseModel):
    api: str
    configuration: ModelConfiguration
    parameters: Dict[str, Any] = {}
    response: str = "first"


class PromptParameter(BaseModel):
    type: str
    description: str
    default: Optional[Any] = None


class PromptConfig(BaseModel):
    name: str
    description: str
    version: Optional[str] = None
    authors: List[str] = []
    tags: List[str] = []
    model: ModelInfo
    inputs: Dict[str, PromptParameter]
    outputs: Optional[Dict[str, Any]] = None
    sample: Optional[Dict[str, Any]] = None


class Prompt(BaseModel):
    config: PromptConfig
    template: str

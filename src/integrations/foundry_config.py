from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class FoundryConfig:
    project_endpoint: str | None
    model_deployment: str | None

    @property
    def is_configured(self) -> bool:
        return bool(self.project_endpoint and self.model_deployment)


def get_foundry_config() -> FoundryConfig:
    return FoundryConfig(
        project_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
        model_deployment=os.getenv("AZURE_AI_MODEL_DEPLOYMENT", "gpt-4o"),
    )

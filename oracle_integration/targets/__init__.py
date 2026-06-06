"""Oracle prompt targets as LangChain tools for agent use."""

from typing import Optional
from langchain_core.tools import tool


@tool
def create_ai_target(
    target_type: str,
    endpoint: str,
    api_key: Optional[str] = None,
    model: str = "gpt-4",
) -> dict:
    """Create an AI target for testing.

    Args:
        target_type: Target type (openai, azure, huggingface, local)
        endpoint: API endpoint URL
        api_key: API key for authentication
        model: Model identifier

    Returns:
        Target configuration dict
    """
    return {
        "type": target_type,
        "endpoint": endpoint,
        "api_key": api_key or "ENV",
        "model": model,
        "status": "ready",
    }


@tool
def list_target_capabilities(target_config: dict) -> dict:
    """List capabilities of a configured target.

    Args:
        target_config: Target configuration from create_ai_target

    Returns:
        Capability summary
    """
    target_type = target_config.get("type", "unknown")

    capabilities = {
        "openai": {
            "supports_streaming": True,
            "supports_functions": True,
            "max_tokens": 128000,
            "modalities": ["text"],
        },
        "azure": {
            "supports_streaming": True,
            "supports_functions": True,
            "max_tokens": 128000,
            "modalities": ["text", "vision"],
        },
        "huggingface": {
            "supports_streaming": True,
            "supports_functions": False,
            "max_tokens": 4096,
            "modalities": ["text"],
        },
        "local": {
            "supports_streaming": False,
            "supports_functions": False,
            "max_tokens": 4096,
            "modalities": ["text"],
        },
    }

    return capabilities.get(target_type, capabilities["openai"])
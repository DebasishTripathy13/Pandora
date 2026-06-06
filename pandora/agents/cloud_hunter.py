"""Cloud Hunter Agent — AWS/Azure/GCP/k8s exploitation lane."""

from __future__ import annotations

from deepagents.middleware.patch_tool_calls import PatchToolCallsMiddleware
from deepagents.middleware.summarization import create_summarization_middleware
from langchain.agents import create_agent
from langchain.agents.middleware import ModelFallbackMiddleware
from langchain_anthropic.middleware import AnthropicPromptCachingMiddleware

from pandora.agents._benchmark_mode import benchmark_skill_sources
from pandora.agents.prompts import load_prompt
from pandora.backends import DockerSandbox
from pandora.core.config import load_config
from pandora.llm import LLMFactory
from pandora.middleware import (
    EngagementContextMiddleware,
    FilesystemMiddleware,
    SandboxNotificationMiddleware,
)
from pandora.middleware.skills import SkillsMiddleware
from pandora.tools.bash import BASH_TOOLS
from pandora.tools.bash.bash import set_sandbox
from pandora.tools.cloud.tools import CLOUD_TOOLS
from pandora.tools.research.tools import (
    cve_lookup,
    kg_add_edge,
    kg_add_node,
    kg_neighbors,
    kg_query,
    kg_stats,
)


def create_cloud_hunter_agent():
    config = load_config()
    factory = LLMFactory()
    llm = factory.get_model("cloud_hunter")
    fallback_models = factory.get_fallback_models("cloud_hunter")

    sandbox = DockerSandbox(container_name=config.docker.sandbox_container_name)
    set_sandbox(sandbox)

    system_prompt = load_prompt("cloud_hunter", shared=["bash"])
    backend = sandbox

    middleware = [
        EngagementContextMiddleware(),
        SkillsMiddleware(
            backend=backend,
            sources=["/skills/cloud/", "/skills/shared/", *benchmark_skill_sources()],
        ),
        FilesystemMiddleware(backend=backend),
        SandboxNotificationMiddleware(sandbox=sandbox),
    ]
    if fallback_models:
        middleware.append(ModelFallbackMiddleware(*fallback_models))
    middleware.extend(
        [
            create_summarization_middleware(llm, backend),
            AnthropicPromptCachingMiddleware(unsupported_model_behavior="ignore"),
            PatchToolCallsMiddleware(),
        ]
    )

    tools = [
        # Cloud tools
        *CLOUD_TOOLS,
        # KG core
        kg_add_node,
        kg_add_edge,
        kg_query,
        kg_neighbors,
        kg_stats,
        # CVE intelligence
        cve_lookup,
        # Execution
        *BASH_TOOLS,
    ]
    agent = create_agent(
        llm,
        system_prompt=system_prompt,
        tools=tools,
        middleware=middleware,
        name="cloud_hunter",
    ).with_config({"recursion_limit": 250})
    return agent


graph = create_cloud_hunter_agent()

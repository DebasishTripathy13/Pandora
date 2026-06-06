"""Patcher Agent — Stage 4 of the vulnresearch pipeline.

The Patcher generates minimal diffs for validated findings and proves
the fix holds by re-running the Verifier's PoC through
:func:`pandora.research.patch.patch_verify`. It runs on Opus with a
high recursion budget because the iteration loop (write → apply → test
→ verify → revise) can take many turns on non-trivial bugs.

Tool surface:
  - ``patch_propose`` / ``patch_verify`` — proposal + ZFP verification
  - ``kg_query`` / ``kg_neighbors`` — read verified findings
  - Filesystem Edit / Read via ``FilesystemMiddleware`` — apply diffs
  - ``bash`` — run the repo's test suite and stage test commands
"""

from __future__ import annotations

from deepagents.middleware.patch_tool_calls import PatchToolCallsMiddleware
from deepagents.middleware.summarization import create_summarization_middleware
from langchain.agents import create_agent
from langchain.agents.middleware import ModelFallbackMiddleware
from langchain_anthropic.middleware import AnthropicPromptCachingMiddleware

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
from pandora.tools.research.patch import patch_propose, patch_verify
from pandora.tools.research.tools import (
    kg_neighbors,
    kg_query,
    kg_stats,
)


def create_patcher_agent():
    """Initialize the Patcher Agent — opus, iterative fix-verify loops."""
    config = load_config()

    factory = LLMFactory()
    llm = factory.get_model("patcher")
    fallback_models = factory.get_fallback_models("patcher")

    sandbox = DockerSandbox(
        container_name=config.docker.sandbox_container_name,
    )
    set_sandbox(sandbox)

    system_prompt = load_prompt("patcher", shared=["bash"])

    backend = sandbox

    middleware = [
        EngagementContextMiddleware(),
        SkillsMiddleware(
            backend=backend,
            sources=["/skills/patcher/", "/skills/shared/"],
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
        patch_propose,
        patch_verify,
        kg_query,
        kg_neighbors,
        kg_stats,
        *BASH_TOOLS,
    ]

    agent = create_agent(
        llm,
        system_prompt=system_prompt,
        tools=tools,
        middleware=middleware,
        name="patcher",
    ).with_config({"recursion_limit": 200})

    return agent


graph = create_patcher_agent()

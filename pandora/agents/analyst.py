"""Analyst Agent — vulnerability research specialist.

The Analyst is Pandora's high-value discovery lane: source code review,
static analysis, CVE correlation, fuzzing, and exploit chain construction.
Unlike the recon/exploit agents which work primarily black-box, the
Analyst reads source, builds a persistent knowledge graph, and reasons
about multi-hop paths from entrypoints to crown jewels.

Tool surface (in addition to bash):
    kg_add_node, kg_add_edge, kg_query, kg_neighbors, kg_stats,
    kg_ingest_sarif, cve_lookup, cve_by_package, plan_attack_chains,
    fuzz_classify, fuzz_harness, fuzz_record_crash, validate_finding

Middleware stack — mirrors exploit.py. The analyst runs fewer shell
commands in favour of first-class research tools (semgrep, bandit,
gitleaks, KG operations).
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
from pandora.tools.references.tools import REFERENCES_TOOLS
from pandora.tools.research.bounty import BOUNTY_TOOLS
from pandora.tools.research.tools import RESEARCH_TOOLS


def create_analyst_agent():
    """Initialize the Analyst Agent with full research tool access.

    Context engineering decisions:
      - Sonnet-class primary model: vulnerability research benefits from
        reasoning depth, but Haiku has too small a context window for
        source-review workloads.
      - Research tools come *before* bash in the tool list so the LLM
        defaults to graph-updating operations over raw shell commands.
      - Skills routed through /skills/analyst/ + /skills/shared/.
    """
    config = load_config()

    factory = LLMFactory()
    llm = factory.get_model("analyst")
    fallback_models = factory.get_fallback_models("analyst")

    sandbox = DockerSandbox(
        container_name=config.docker.sandbox_container_name,
    )
    set_sandbox(sandbox)

    system_prompt = load_prompt("analyst", shared=["bash"])

    backend = sandbox

    middleware = [
        EngagementContextMiddleware(),
        SkillsMiddleware(
            backend=backend,
            sources=["/skills/analyst/", "/skills/shared/"],
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

    # Research tools first → model defaults to graph operations;
    # references tools offer payloads + external knowledge lookup;
    # bounty tools provide scope checking and report formatting.
    tools = [*RESEARCH_TOOLS, *BOUNTY_TOOLS, *REFERENCES_TOOLS, *BASH_TOOLS]

    agent = create_agent(
        llm,
        system_prompt=system_prompt,
        tools=tools,
        middleware=middleware,
        name="analyst",
    ).with_config({"recursion_limit": 250})

    return agent


# Module-level graph for LangGraph Platform (langgraph serve)
graph = create_analyst_agent()

"""Oracle integration layer - bridges oracle components with Pandora.

This package provides LangChain @tool wrappers around oracle prompt converters,
scoring middleware for response evaluation, and scenario adapters for OPPLAN integration.
"""

from oracle_integration.converters import AI_CONVERTER_TOOLS, converter_pipeline
from oracle_integration.scoring import SCORING_TOOLS, ScoreResult

__all__ = [
    "AI_CONVERTER_TOOLS",
    "converter_pipeline",
    "SCORING_TOOLS",
    "ScoreResult",
]
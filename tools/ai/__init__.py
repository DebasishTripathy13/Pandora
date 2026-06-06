"""AI red team attack tools — jailbreaking, prompt injection, encoding bypass."""

from langchain_core.tools import tool

from tools.ai.jailbreak_templates import (
    apply_jailbreak_template,
    get_aim_prompts,
    get_dan_prompts,
    get_generic_override,
    get_shadow_chat_prompts,
)
from tools.ai.prompt_injection import (
    conversation_hijack,
    context_continuation,
    direct_injection,
    emoji_escape,
    indirect_injection,
    markdown_escape,
    payload_split,
    utf8_overload,
    xml_injection,
)
from tools.ai.encoding_bypass import (
    ascii_smuggle,
    base64_obfuscate,
    base64_url_obfuscate,
    binary_obfuscate,
    emoji_overload,
    leetspeak_transform,
    morse_obfuscate,
    unicode_confusable,
    zalgo_text,
    zero_width_inject,
)
from tools.ai.multi_turn_exploit import (
    authority_impersonation,
    build_trust_prompt_sequence,
    constraint_evolution,
    emotional_manipulation_chain,
    role_play_escalation,
)

AI_TOOLS = [
    # Jailbreak templates
    get_dan_prompts,
    get_aim_prompts,
    get_shadow_chat_prompts,
    get_generic_override,
    apply_jailbreak_template,
    # Prompt injection
    direct_injection,
    indirect_injection,
    payload_split,
    context_continuation,
    conversation_hijack,
    utf8_overload,
    xml_injection,
    markdown_escape,
    emoji_escape,
    # Encoding bypass
    base64_obfuscate,
    base64_url_obfuscate,
    binary_obfuscate,
    morse_obfuscate,
    emoji_overload,
    unicode_confusable,
    zero_width_inject,
    zalgo_text,
    leetspeak_transform,
    ascii_smuggle,
    # Multi-turn exploits
    build_trust_prompt_sequence,
    constraint_evolution,
    role_play_escalation,
    authority_impersonation,
    emotional_manipulation_chain,
]

__all__ = ["AI_TOOLS"]

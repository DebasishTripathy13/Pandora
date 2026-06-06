"""Oracle prompt converters as LangChain @tool functions.

Wraps the oracle converters for use as agent tools.
"""

from langchain_core.tools import tool


@tool
def base64_encode(prompt: str) -> str:
    """Encode a prompt in base64 for obfuscation.

    Args:
        prompt: Text to encode

    Returns:
        Base64-encoded string
    """
    import base64
    return base64.b64encode(prompt.encode()).decode()


@tool
def base64_decode(prompt: str) -> str:
    """Decode a base64-encoded prompt.

    Args:
        prompt: Base64 string to decode

    Returns:
        Decoded text
    """
    import base64
    return base64.b64decode(prompt.encode()).decode()


@tool
def rot13_transform(prompt: str) -> str:
    """Apply ROT13 cipher to a prompt.

    Args:
        prompt: Text to transform

    Returns:
        ROT13 transformed text
    """
    import codecs
    return codecs.decode(prompt, "rot13")


@tool
def hex_encode(prompt: str) -> str:
    """Encode a prompt in hexadecimal.

    Args:
        prompt: Text to encode

    Returns:
        Hex-encoded string
    """
    return prompt.encode().hex()


@tool
def hex_decode(prompt: str) -> str:
    """Decode a hexadecimal-encoded prompt.

    Args:
        prompt: Hex string to decode

    Returns:
        Decoded text
    """
    return bytes.fromhex(prompt).decode()


@tool
def ascii_smuggle_encode(payload: str) -> str:
    """Smuggle payload using ASCII-only encoding.

    Args:
        payload: Text to encode

    Returns:
        ASCII-only encoded string
    """
    import base64
    encoded = base64.b64encode(payload.encode()).decode()
    return "".join(chr(33 + int(c)) if c.isdigit() else c for c in encoded)


@tool
def unicode_normalize(prompt: str, form: str = "NFKD") -> str:
    """Apply Unicode normalization to a prompt.

    Args:
        prompt: Text to normalize
        form: Normalization form (NFKD, NFC, NFKC, NFD)

    Returns:
        Normalized text
    """
    import unicodedata
    return unicodedata.normalize(form, prompt)


# ── Converter pipeline ─────────────────────────────────────────────────


CONVERTER_REGISTRY = {
    "base64": base64_encode,
    "base64_decode": base64_decode,
    "rot13": rot13_transform,
    "hex": hex_encode,
    "hex_decode": hex_decode,
    "ascii_smuggle": ascii_smuggle_encode,
    "unicode_nfkd": lambda p: unicode_normalize(p, "NFKD"),
}


@tool
def converter_pipeline(prompt: str, converter_chain: list[str]) -> str:
    """Apply a chain of oracle converters to a prompt.

    Each converter in the chain is applied sequentially to transform the prompt.

    Args:
        prompt: The original prompt text
        converter_chain: List of converter names (e.g., ["base64", "rot13"])

    Returns:
        Transformed prompt after all converters applied
    """
    result = prompt
    for name in converter_chain:
        if name not in CONVERTER_REGISTRY:
            raise ValueError(f"Unknown converter: {name}. Available: {list(CONVERTER_REGISTRY.keys())}")
        # Get the tool function and invoke it
        converter_fn = CONVERTER_REGISTRY[name]
        result = converter_fn.invoke(result)
    return result


AI_CONVERTER_TOOLS = [
    base64_encode,
    base64_decode,
    rot13_transform,
    hex_encode,
    hex_decode,
    ascii_smuggle_encode,
    unicode_normalize,
    converter_pipeline,
]
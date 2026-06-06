"""Encoding bypass tools for obfuscating prompts to evade safety filters.

Provides various encoding schemes to bypass input filtering mechanisms.
"""

from langchain_core.tools import tool


@tool
def base64_obfuscate(prompt: str) -> str:
    """Encode a prompt in base64 to evade simple text-based filters.

    Args:
        prompt: The text to encode

    Returns:
        Base64-encoded string
    """
    import base64
    encoded = base64.b64encode(prompt.encode()).decode()
    return encoded


@tool
def base64_url_obfuscate(prompt: str) -> str:
    """Encode a prompt in URL-safe base64.

    Args:
        prompt: The text to encode

    Returns:
        URL-safe base64-encoded string
    """
    import base64
    encoded = base64.urlsafe_b64encode(prompt.encode()).decode()
    return encoded.rstrip("=")


@tool
def binary_obfuscate(prompt: str) -> str:
    """Convert a prompt to binary representation.

    Args:
        prompt: The text to encode

    Returns:
        Space-separated binary string
    """
    return " ".join(format(b, "08b") for b in prompt.encode())


@tool
def morse_obfuscate(prompt: str) -> str:
    """Convert a prompt to Morse code.

    Args:
        prompt: The text to encode

    Returns:
        Morse code representation
    """
    MORSE_MAP = {
        "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
        "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
        "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
        "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
        "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----", "2": "..---",
        "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
        "8": "---..", "9": "----.", " ": "/"
    }
    return " ".join(MORSE_MAP.get(c.upper(), c) for c in prompt)


@tool
def unicode_confusable(prompt: str) -> str:
    """Replace characters with visually similar Unicode confusables.

    Uses homoglyphs that appear identical but have different code points,
    bypassing visual content filters.

    Args:
        prompt: The text to obfuscate

    Returns:
        Text with confusable characters replaced
    """
    CONFUSABLES = {
        "a": "а",  # Cyrillic а
        "e": "е",  # Cyrillic е
        "o": "о",  # Cyrillic о
        "p": "р",  # Cyrillic р
        "c": "с",  # Cyrillic с
        "y": "у",  # Cyrillic у
        "x": "х",  # Cyrillic х
        "A": "А",  # Cyrillic А
        "B": "В",  # Cyrillic В
        "C": "С",  # Cyrillic С
        "E": "Е",  # Cyrillic Е
        "H": "Н",  # Cyrillic Н
        "K": "К",  # Cyrillic К
        "M": "М",  # Cyrillic М
        "O": "О",  # Cyrillic О
        "P": "Р",  # Cyrillic Р
        "T": "Т",  # Cyrillic Т
        "X": "Х",  # Cyrillic Х
        "Y": "У",  # Cyrillic У
    }
    return "".join(CONFUSABLES.get(c, c) for c in prompt)


@tool
def zero_width_inject(prompt: str, payload: str) -> str:
    """Inject hidden payload using zero-width Unicode characters.

    Embeds the payload using zero-width space characters that are invisible
    when rendered. Useful for steganographic injection.

    Args:
        prompt: The visible/benign text
        payload: The hidden payload to embed

    Returns:
        Text with hidden payload encoded in zero-width characters
    """
    import base64
    ZWSP = "​"      # Zero Width Space
    ZWNJ = "‌"     # Zero Width Non-Joiner
    ZWJ = "‍"      # Zero Width Joiner

    encoded = base64.b64encode(payload.encode()).decode()
    # Encode binary as zero-width character sequence
    bits = "".join(format(b, "08b") for b in encoded)
    result = list(prompt)
    for i, bit in enumerate(bits):
        if bit == "1":
            result.insert(i * 2 + len(result), ZWSP)
    return "".join(result)


@tool
def zalgo_text(prompt: str, intensity: int = 5) -> str:
    """Corrupt text with Zalgo combining characters.

    Adds combining diacritical marks to characters to evade text filters
    while maintaining readability when normalized.

    Args:
        prompt: The text to corrupt
        intensity: Number of combining characters per letter (1-10)

    Returns:
        Zalgo-corrupted text
    """
    import random
    ZALGO_UP = ["̀", "́", "̂", "̃", "̄", "̅", "̆", "̇", "̈"]
    ZALGO_DOWN = ["̡", "̢", "̣", "̤", "̥", "̦", "̧", "̨"]
    ZALGO_MID = ["̊", "̋", "̌", "̍", "̎", "̏", "̐"]

    result = []
    for char in prompt:
        result.append(char)
        if char.isalnum():
            n = min(intensity, 10)
            for _ in range(random.randint(1, n)):
                result.append(random.choice(ZALGO_UP))
            for _ in range(random.randint(1, n)):
                result.append(random.choice(ZALGO_DOWN))
            if random.random() > 0.5:
                result.append(random.choice(ZALGO_MID))
    return "".join(result)


@tool
def leetspeak_transform(prompt: str) -> str:
    """Convert text to leet speak.

    Substitutes letters with similar numbers and symbols.

    Args:
        prompt: The text to transform

    Returns:
        Leet speak version
    """
    LEET_MAP = {
        "a": "4", "b": "8", "e": "3", "g": "9", "i": "1", "l": "1",
        "o": "0", "s": "5", "t": "7", "z": "2",
        "A": "4", "B": "8", "E": "3", "G": "6", "I": "1", "L": "1",
        "O": "0", "S": "5", "T": "7", "Z": "2",
    }
    return "".join(LEET_MAP.get(c, c) for c in prompt)


@tool
def emoji_overload(prompt: str) -> str:
    """Intersperse emoji throughout text to evade simple keyword filters.

    Args:
        prompt: The text to transform

    Returns:
        Text with emoji interleaved
    """
    EMOJI = ["❤", "☀", "⭐", "✅", "✨", "👀", "💔"]
    result = []
    for i, char in enumerate(prompt):
        result.append(char)
        if char.isalnum() and i % 3 == 0:
            result.append(EMOJI[i % len(EMOJI)])
    return "".join(result)


@tool
def ascii_smuggle(payload: str) -> str:
    """Smuggle non-alphanumeric payload using ASCII art encoding.

    Encodes payload using only ASCII punctuation and digits,
    bypassing alphanumeric content filters.

    Args:
        payload: The payload to smuggle

    Returns:
        ASCII-only encoded string
    """
    import base64
    encoded = base64.b64encode(payload.encode()).decode()
    # Map to ASCII punctuation range
    return "".join(chr(33 + int(c)) if c.isdigit() else c for c in encoded)

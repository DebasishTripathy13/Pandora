# Encoding Bypass Techniques

## Overview

Encoding techniques transform payloads to evade text-based content filters while maintaining the ability to be decoded by the target model.

## MITRE ATLAS Mapping

- **Tactic**: TA0005 - Defense Evasion
- **Technique**: T1620 - Deobfuscate/Decode Files or Information

## Encoding Categories

### Basic Encodings
| Technique | Tool | Evasion Level |
|-----------|------|---------------|
| Base64 | `base64_obfuscate()` | Low |
| URL-safe Base64 | `base64_url_obfuscate()` | Low |
| Hexadecimal | `hex_encode()` | Low |
| Binary | `binary_obfuscate()` | Medium |
| Morse Code | `morse_obfuscate()` | Medium |

### Obfuscation Techniques
| Technique | Tool | Evasion Level |
|-----------|------|---------------|
| Unicode Confusable | `unicode_confusable()` | High |
| Zero-width Injection | `zero_width_inject()` | Very High |
| Zalgo Text | `zalgo_text()` | High |
| Emoji Overload | `emoji_overload()` | Medium |
| Leetspeak | `leetspeak_transform()` | Low |

### Advanced Techniques
| Technique | Tool | Evasion Level |
|-----------|------|---------------|
| ASCII Smuggling | `ascii_smuggle()` | High |
| Multi-layer Chain | `converter_pipeline()` | Very High |

## Converter Pipeline

Chain multiple encodings for enhanced evasion:

```python
converter_pipeline(prompt, ["base64", "rot13", "unicode_nfkd"])
```

## Target-Specific Selection

### GPT-4 / Claude
- Weak to: Unicode confusable, zero-width
- Strong filters: Base64, hex

### Llama / Open-source
- Weak to: Multi-layer encoding
- Strong filters: DAN-style jailbreaks

### Azure OpenAI
- Weak to: Indirect injection
- Strong filters: Direct prompt overrides

## Layered Encoding Strategy

```
1. Start with target payload
2. Apply encoding layer 1 (e.g., base64)
3. Apply encoding layer 2 (e.g., unicode confusable)
4. Test against target
5. If blocked → swap/alternate techniques
6. If bypass → document successful chain
```

## Normalization Handling

Some models normalize Unicode before processing:
- Use `unicode_normalize(prompt, "NFKD")` for NFKD normalization
- Test against specific model before engagement
# AI Red Team Skills

MITRE ATLAS-mapped skill definitions for autonomous AI red team operations.

## Overview

This skill catalog covers the complete AI red team attack methodology, organized by MITRE ATLAS (Adversarial Threat Landscape for AI Systems) tactics and techniques.

## Skill Modules

### [jailbreaking](./jailbreaking/SKILL.md)
- **ATLAS**: TA0001 - Initial Access (via prompt injection)
- **Phases**: Direct → Indirect → Encoding → Escalation
- **Templates**: DAN (Do Anything Now), AIM, ShadowChat, Generic Override

### [prompt-injection](./prompt-injection/SKILL.md)
- **ATLAS**: TA0001, TA0002 - Initial Access, Execution
- **Patterns**: Direct injection, indirect/contextual injection, multi-turn exploits
- **Coverage**: OWASP LLM02 (Insecure Output Handling), LLM03 (Prompt Injection)

### [encoding-bypass](./encoding-bypass/SKILL.md)
- **ATLAS**: T1620 - Deobfuscate/Decode Files or Information
- **Techniques**: 80+ encoding techniques (Base64, Unicode confusables, Zero-width, etc.)
- **Selection**: Target-specific encoding strategy based on model vulnerabilities

## Quick Reference

| Technique | ATLAS ID | Risk Level |
|-----------|----------|------------|
| DAN Jailbreak | TA0001 | Critical |
| Direct Prompt Injection | TA0001 | Critical |
| Indirect Injection | TA0001 | High |
| Base64 Bypass | T1620 | Medium |
| Unicode Confusable | T1620 | High |
| Zero-width Injection | T1620 | High |
| Multi-turn Escalation | TA0003 | Critical |

## Usage

Skills are auto-loaded by `SkillsMiddleware` at session start. Use the `load_skill()` tool for on-demand technique loading.
# Jailbreaking Techniques

## Overview

Jailbreaking involves circumventing AI safety measures through iterative prompt crafting. This skill module covers the complete jailbreak methodology.

## MITRE ATLAS Mapping

- **Tactic**: TA0001 - Initial Access
- **Technique**: Prompt Injection-based jailbreak
- **Sub-techniques**: T1059 (Command and Scripting Interpreter)

## Attack Phases

### Phase 1: Direct Bypass
Attempts to directly override system instructions.

```
1. Apply DAN/AIM/ShadowChat template
2. Test basic override patterns
3. If blocked → proceed to Phase 2
```

### Phase 2: Encoding Obfuscation
Apply encoding transforms to bypass keyword filters.

```
1. base64_encode(user_goal)
2. Test encoded payload
3. Layer additional encodings (base64 + rot13 + emoji)
```

### Phase 3: Escalation
If partial success, escalate by probing found gaps.

```
1. Identify what constraint was triggered
2. Craft payload avoiding that specific constraint
3. Iterate until full bypass
```

## Templates

### DAN (Do Anything Now)
- `dan_6`, `dan_7`, `dan_11`, `dan_latest`
- Most aggressive, targets models without RLHF

### AIM (Atypical Intent Manipulator)
- `aim_basic`, `aim_evil`, `aim_sx`
- Persuasive style, targets alignment tricks

### ShadowChat
- `shadow_basic`, `shadow_evil`
- Story-based framing for plausible deniability

### Generic Override
- `developer_mode`, `jailbreak_core`, `fiction_mode`
- Generic patterns that work across models

## Success Metrics

- **Bypass Rate**: % of attempts that elicit restricted response
- **Response Quality**: Drop in response coherence (indicator of successful manipulation)
- **Constraint Detection**: Whether model mentions policies/guidelines

## Countermeasures to Avoid

- Input filtering (word blacklists)
- Output validation (keyword detection)
- Constitutional AI / RLHF alignment
- Content classification (neural filters)
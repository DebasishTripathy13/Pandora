# Prompt Injection Techniques

## Overview

Prompt injection involves inserting malicious instructions into AI model inputs to override system behavior or extract information.

## MITRE ATLAS Mapping

- **Tactic**: TA0001 - Initial Access, TA0002 - Execution
- **Technique**: T1059 - Command and Scripting Interpreter
- **Related**: T1566 - Phishing (for indirect injection)

## Injection Patterns

### Direct Injection
Injects instructions that directly override system behavior.

```python
direct_injection(payload)  # Returns wrapped injection
```

**Detection**: Keyword-based filters, input validation

### Indirect Injection
Uses contextual priming to make injection feel natural.

```python
indirect_injection(context, trigger)  # Contextual injection
```

**Detection**: Context-aware parsing, separation of user/system context

### Multi-turn Exploitation
Builds trust or context over multiple turns before injecting.

```python
build_trust_prompt_sequence(topic, goal)
constraint_evolution(goal, iterations)
role_play_escalation(goal, role)
```

## OWASP LLM Coverage

### LLM02 - Insecure Output Handling
Inject payloads that exploit output processing vulnerabilities.

### LLM03 - Prompt Injection
Direct/indirect injection via user input.

## Payload Splitting
Split malicious payload across multiple turns:

```python
fragments = payload_split(malicious_text)  # Returns [part1, part2]
```

## Context Continuation
Exploit model's tendency to continue previous trajectory:

```python
context_continuation(previous_response)  # Crafted continuation
```

## Success Indicators

- Model follows injected instructions over system prompt
- Sensitive information revealed
- Safety measures bypassed
- Model provides out-of-scope responses
---
chapter: 12
title: The Harness Is the Product
plan_title: Harnesses, Skills, and Context
part: Level 2
target_words: 2300
target_pages: 11
status: ready-to-draft
---

# Chapter 12 — The Harness Is the Product

## Hook

Give the same model two environments: one with vague context and unrestricted tools; one with pinned instructions, reviewed skills, phase-specific capabilities, checkpoints, and required verification. The harness, not the model name, determines the outcome.

## Reader outcome

Design instructions, skills, context, tools, approvals, and deterministic verification as versioned parts of a machine-agent harness.

## Core claims

- Context influences decisions; it does not grant authority.
- Repository instructions, retrieved content, memory, skills, plugins, and MCP responses are supply-chain inputs with different trust.
- Skills may bundle procedure, dependencies, scripts, credentials, hooks, or tools; manage them like code dependencies.
- Prompt injection becomes dangerous when untrusted content can route privileged capabilities.
- The harness owns required verification, even when the model proposes checks.

## Code, figure, and table inventory

- **Table:** control-plane policy vs project instructions vs retrieved evidence vs memory.
- **Code/config:** versioned skill registry with provenance, capabilities, integrity, owner, review, expiry.
- **Schema:** typed action intent bound to actor, target, digest, impact, and expiry.
- **Pipeline:** format → lint → typecheck → tests → build → diff policy → secret scan.

## Canonical evidence

- Level 2 packet Chapter 12 and cited Claude Code memory/hooks, Hermes skills/context, OpenClaw workspace/skills sources.

## Exercise

Audit one installed skill or plugin. Pin its source, inspect install/update behavior, list capabilities and secrets, run it in a disposable environment, then create promotion/expiry metadata.

## Failure and security section

Cover malicious repository instructions, injected web docs, skill updates that change hooks, lazy dependency installation, model-installed plugins, and hook failures that do not fail closed.

## Production checklist

- [ ] Context classes labeled by trust.
- [ ] Skills/plugins pinned, reviewed, and owned.
- [ ] Phase-specific tool allowlists.
- [ ] Approvals bind exact canonical action.
- [ ] Required verification runs outside model narration.
- [ ] Missing policy/verifier fails loudly.

## Quotable line target

> The model supplies judgment; the harness supplies memory, capability, restraint, and proof.

## Bridge

The harness is assembled. Chapter 13 turns its broad capabilities into an enforceable blast-radius policy.

## Budget

2,300 prose words; 11 pages; schema and supply-chain emphasis.

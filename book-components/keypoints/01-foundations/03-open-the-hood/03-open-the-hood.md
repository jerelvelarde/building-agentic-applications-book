---
chapter: 3
title: Open the Hood
plan_title: The Production-Grade Agent Stack
part: Foundations
target_words: 2200
target_pages: 10
status: ready-to-draft
---

# Chapter 3 — Open the Hood

## Hook

Begin with a polished demo that fails after refresh, repeats a write, leaks another tenant's record, and leaves no trace of why. The model worked; the application did not.

## Reader outcome

Identify every major subsystem behind a production agent and assign each responsibility to an explicit owner and enforcement boundary.

## Core claims

- The production stack includes model, runtime/harness, tools/skills, task state, memory, policy/planning, identity/authority, interface, protocols, evaluation, observability, and operations.
- State, policy, identity, and operations cut across the whole stack; they are not optional backend boxes.
- CopilotKit is the interaction layer; AG-UI is an observable event contract; LangChain/LangGraph are runtime/orchestration choices; none substitutes for application authorization.
- “Production-grade” describes the whole system's demonstrated behavior, not a framework selection.

## Code, figure, and table inventory

- **Hero figure:** exploded “open the hood” architecture with trust boundaries.
- **Timeline:** run, step, tool call, thread, checkpoint, and trace mappings.
- **Table:** subsystem → builder question → failure if omitted.
- **Worksheet:** eleven engineering knobs reused in every level.

## Canonical evidence

- Level 1 packet, “Anatomy of an agentic application,” terminology mapping, and reference architecture.
- Level 2 packet, machine harness anatomy.
- Level 3 packet, current Channels runtime path.
- `authoring/terminology.md` and `authoring/source-and-evidence-policy.md`.

## Exercise

Annotate an existing agent architecture. For every box, name its owner, trusted inputs, outputs, persistence, identity, failure mode, and operational signal. Highlight any responsibility that currently lives only in prompt text.

## Failure and security section

Use the demo failure to show missing thread identity, idempotency, tenant scope, and audit. Explain why schemas are not authorization and traces are not state.

## Production checklist

- [ ] Every subsystem and owner named.
- [ ] Trust boundaries drawn.
- [ ] Identity and tenant scope reach every tool.
- [ ] State, memory, and telemetry separated.
- [ ] Recovery and evaluation attached to actual side effects.

## Quotable line target

> The model may choose the next action; the application decides whether that action deserves to exist in the real world.

## Bridge

Chapter 4 turns the architecture toward the user: if the system is uncertain and stateful, the interface must become a control plane.

## Budget

2,200 prose words; 10 designed pages; architecture-first layout.

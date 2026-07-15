---
chapter: 2
title: When Software Starts Choosing
plan_title: What Makes Software Agentic?
part: Foundations
target_words: 1900
target_pages: 8
status: ready-to-draft
---

# Chapter 2 — When Software Starts Choosing

## Hook

Show four interfaces that look identical in chat but hide different execution: one model call, a fixed workflow, a tool-using assistant, and an adaptive agent loop. Ask which one is “agentic” without looking at the UI.

## Reader outcome

Distinguish model-powered features, workflows, tool-using assistants, and agents, and decide where adaptive judgment is justified.

## Core claims

- Chat is an interaction form, not an execution architecture.
- A workflow has developer-authored routing; an agent dynamically selects actions inside a constrained loop.
- Tool calling alone does not prove autonomy—the application may still own the loop.
- Deterministic nodes belong inside agentic systems when the transformation is predictable.
- Agency should be added only when its adaptability is worth uncertainty, cost, and control burden.

## Code, figure, and table inventory

- **Code:** tested contrast among one model call, fixed LangGraph workflow, and dynamic agent loop (`FND-01`).
- **Figure:** goal → decide → act → observe → adapt/pause/finish.
- **Table:** model feature vs workflow vs assistant vs agent across routing, state, tools, termination, evaluation.
- **Decision tree:** “workflow or agent?”

## Canonical evidence

- Level 1 packet, “A precise taxonomy for builders” and claim map.
- Official LangChain model/agent and LangGraph workflow/agent sources cited in that packet.
- `authoring/terminology.md` for canonical run/step/tool definitions.

## Exercise

Take a five-step AI workflow. Mark every step as deterministic or adaptive. Replace each unnecessary model decision with code and define the stop conditions for the remaining agent loop.

## Failure and security section

Cover infinite loops, fake completion at step limits, agents selecting write tools too early, and deterministic business rules hidden in prompts. Make model choice subordinate to runtime limits and policy.

## Production checklist

- [ ] Goal and terminal conditions explicit.
- [ ] Adaptive decisions justified.
- [ ] Tool set and step/time/cost limits bounded.
- [ ] Deterministic invariants enforced in code.
- [ ] Evaluation covers trajectory, not only final prose.

## Quotable line target

> An agent begins where the execution path stops being fully known in advance—and where controls must become explicit.

## Bridge

Once the reader can identify the loop, Chapter 3 opens the rest of the system that makes that loop usable and operable.

## Budget

1,900 prose words; 8 designed pages; one short runnable comparison.

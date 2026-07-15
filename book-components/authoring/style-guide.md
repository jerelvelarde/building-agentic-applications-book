---
title: Editorial Style Guide
status: active-drafting
updated: 2026-07-14
---

# Editorial style guide

## Editorial posture

Write as an experienced builder opening the hood with another builder. The voice is direct, specific, curious, and evidence-led. Teach the durable pattern first, then show how CopilotKit, LangChain, LangGraph, LangSmith, AG-UI, and the Channels SDK implement it in the pinned edition.

This is a field guide, not a framework manual and not a trend report. Every chapter must convert architecture into a decision, implementation, verification step, or operating control.

## The chapter rhythm

Use this sequence unless the chapter has a documented reason to vary it:

1. **Hook:** a concrete failure, tension, or engineering choice.
2. **Context:** why the decision becomes important at this authority level.
3. **Mental model:** the durable concept before the API.
4. **Build:** code, configuration, or architecture from a pinned source.
5. **Proof:** screenshot, trace, test result, or artifact.
6. **Knobs:** parameters and tradeoffs the builder must choose.
7. **Failure and security:** how the design breaks or can be abused.
8. **Production gate:** conditions that must be true before shipping.
9. **Exercise:** one small, inspectable build milestone.
10. **Bridge:** the unresolved pressure that motivates the next chapter.

Aim for one memorable line per chapter, but never sacrifice precision for a slogan.

## Voice and sentence craft

- Prefer active voice and concrete subjects: “The runtime checkpoints state,” not “State is checkpointed.”
- Use “you” for builder decisions and “we” only for the book's shared model or verified reference run.
- Keep most paragraphs to three to five lines in the designed layout.
- Lead sections with the decision or consequence, not historical throat-clearing.
- Define a term once, use it consistently, and link to `terminology.md` when ambiguity is likely.
- Use an analogy only when it makes a system boundary easier to reason about. Return quickly to the actual mechanism.
- Prefer exact verbs: propose, authorize, execute, persist, resume, compensate, revoke.
- Avoid hype words such as revolutionary, magical, seamless, autonomous by default, or production-ready without evidence.
- Avoid anthropomorphism when the mechanism matters. An agent may “select a tool” in product prose; it should not “understand the organization” without a scoped technical meaning.

## Explanatory standard

Each important control needs four parts:

```text
intent → enforcement point → evidence → failure behavior
```

“Require approval” is incomplete. Name where the run pauses, which principal may decide, what exact proposal is bound to the decision, and what happens on timeout, edit, replay, or revocation.

Distinguish:

- observed behavior from proposed architecture;
- model guidance from enforced policy;
- visibility from authorization;
- cancellation from rollback or business compensation;
- state from memory and telemetry;
- platform scopes from application authorization.

## Code and API prose

- Print most snippets at 8–30 lines.
- Introduce the file and decision before the code block; explain the non-obvious consequence after it.
- Do not narrate every line.
- Use exact package and hook names from the pinned implementation.
- Mark migration or legacy examples explicitly.
- Never style pseudocode as verified code. Use a `Conceptual` or `Target architecture` label.
- Do not claim parity between web and React Native APIs without a runtime-verified compatibility note.
- Put complete implementations, fixtures, and tests in the companion repository.

Detailed rules live in `code-and-screenshot-policy.md`.

## Figures, tables, and callouts

Use a figure when the reader needs to see sequence, hierarchy, state change, or a trust boundary. Use a table for three or more comparable terms, tools, roles, or choices.

Every figure brief must answer a reader question. Every screenshot caption must say what to notice and why it matters.

Allowed callouts:

- **Builder decision** — a parameter or architecture choice.
- **Boundary check** — where trust, identity, or authority changes.
- **Failure mode** — a concrete way the design breaks.
- **Version note** — a time-sensitive or migration-specific caveat.
- **Production gate** — a non-negotiable condition before shipping.
- **In the wild** — a source-present repository example, with evidence status.

## Product and vendor treatment

- CopilotKit is the canonical interaction layer because this book demonstrates it in depth.
- LangChain/LangGraph are the canonical orchestration teaching stack.
- Explain the underlying pattern in vendor-neutral language before naming the implementation.
- Compare Claude Code, Hermes, OpenClaw, Claude Tag, OpenTag, managed services, and self-hosted options on explicit dimensions and a dated evidence set.
- Do not crown a universal winner. End comparisons with “choose this when” guidance.
- Product availability, API names, versions, pricing, and supported channels require publication-time verification.

## Reasoning and transparency

Never promise hidden chain-of-thought. Show operational evidence: plan, stage, tool, safe arguments, state change, source, assumption, approval, result, and recovery option.

## Technical typography

- Product names: CopilotKit, LangChain, LangGraph, LangSmith, OpenTag, Claude Tag, OpenClaw, Hermes.
- Protocols and standards: AG-UI, MCP, OAuth 2.0, RBAC, ABAC.
- Code identifiers use backticks.
- UI labels use quotation marks only when quoting the interface.
- Use an en dash for a label and explanation; use an arrow only for actual flow.
- Prefer sentence-case headings.

## Drafting residue prohibited in review prose

No `TODO`, “fill this in,” agent instructions, evidence-status shorthand without explanation, reviewer priority labels, or unsupported placeholder claims may remain in a review manuscript. Unresolved facts stay in keypoints/evidence packets or appear as clearly formatted publication notes outside reader-facing prose.

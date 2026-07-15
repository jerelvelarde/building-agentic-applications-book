---
title: Reader Personas
status: active-drafting
owner: Jerel Velarde
updated: 2026-07-14
ssot: true
---

# Reader personas

This file is the single source of truth for audience decisions. When a chapter cannot serve every reader, optimize for the primary persona below.

## Primary persona — the application engineer opening the hood

The primary reader is a software builder or engineer entering agentic development. They have used ChatGPT, Claude Code, or a channel agent and may have shipped a model-powered feature. They understand APIs, JSON, Git, package managers, and React concepts. They do not yet have a complete mental model for the product system around an agent: runtime, tools, state, memory, permissions, interface, evaluation, and operations.

They pick up the book because demos have stopped answering their real questions:

- Where should a tool execute?
- What state belongs to the UI, agent, thread, or long-term memory?
- What does an approval actually secure?
- When does a workspace agent need a sandbox or dedicated machine?
- How does a Slack agent preserve requester identity and organizational policy?
- How do I know the system worked, recovered correctly, and stayed inside its authority?

### Their starting point

- Comfortable reading TypeScript and short Python examples.
- Familiar with React components and HTTP APIs.
- Able to run a repository locally and inspect a diff.
- Has seen tool calling, but may equate it with agency.
- Has not necessarily used LangGraph, AG-UI, MCP, CopilotKit, or the Channels SDK.
- Has limited experience threat-modeling autonomous side effects.

### Their desired transformation

The reader begins as someone who can interact with agents. They finish as someone who can design the system around one.

By the final page, they can:

1. Classify a problem by operating surface, authority, and blast radius.
2. Select the smallest sufficient level: application, machine, or organization.
3. Trace a CopilotKit interaction through AG-UI to a runtime and tool boundary.
4. Place frontend, backend, external, and human tools deliberately.
5. Design typed shared state, persistence, recovery, and human intervention.
6. Evaluate a machine-agent harness across skills, context, access, isolation, and verification.
7. Connect an agent to a channel while preserving requester, agent, and approver identity.
8. Define measurable production gates for security, evaluation, reliability, cost, and operations.
9. Run or adapt the companion examples rather than copying untested snippets.

### What earns this reader's trust

- Code that points to a real file, version, and verification command.
- Screenshots that prove a specific running state and explain what to notice.
- Honest separation between source-present, runtime-verified, and target architecture.
- Failure paths beside happy paths.
- Knobs tables that explain tradeoffs, not just API options.
- A production checklist that names the owner and enforcement boundary.
- Comparisons that help choose rather than manufacture a winner.

### What loses this reader

- Framework marketing presented as architecture.
- Pseudocode styled as a tested snippet.
- Generic advice such as “add guardrails” without an enforcement point.
- A wall of prose where a diagram, diff, or decision table is needed.
- Hidden assumptions about identity, persistence, or data access.
- Multi-agent complexity without a real capability, context, security, or ownership boundary.
- Claims that an attractive UI or successful tool call proves production readiness.

## Secondary personas

### Product-minded founder or engineering leader

They use the three-level model to choose an authority surface, estimate operating cost, identify controls their team must own, and decide whether to build, buy, or self-host. They should be able to skim the diagrams, decision tables, hardening ladders, and production checklists without reading every code block.

### AI or platform engineer

They already understand agent loops but need a stronger interaction and governance model. Their high-value sections are AG-UI, shared state, durable interrupts, machine isolation, channel identity, delegated credentials, evaluation, and operating controls.

### Product designer for agentic interfaces

They need the control-plane model: streaming, partial artifacts, explicit status, consequence-aware approvals, editability, cancellation semantics, provenance, accessibility, and recovery. Code is supporting evidence; figure sequences and UI state inventories are their main path.

## Deliberate non-audiences

- Readers seeking a general introduction to programming, React, TypeScript, Python, or cloud deployment.
- Readers seeking prompt templates without application architecture.
- Teams seeking a compliance certification or financial-services security standard from a demo ledger.
- Buyers seeking a static vendor ranking detached from use case and authority.

## Persona review lens

Before a chapter is accepted, the reviewer must answer:

1. What can the primary reader do after this chapter that they could not do before?
2. Is the core decision visible in the first two pages?
3. Does the chapter show the enforcement boundary, not merely describe an intention?
4. Can the reader connect each important snippet and screenshot to a reproducible artifact?
5. Are unverified or time-sensitive claims clearly labeled?
6. Does the exercise produce an inspectable outcome?
7. Does the closing bridge explain how authority or controls change next?

---
title: The Builder's Guide to Agentic Applications 2026 — Master Outline
status: integration-draft
updated: 2026-07-15
chapters: 26
drafted_chapters: 26
target_pages: 297
target_words: 64400
persona_ssot: ../authoring/reader-personas.md
---

# Master outline

## Book promise

> By the end of this book, you will be able to design, build, and operate production-grade agentic applications across application, machine, and organizational environments using the patterns, controls, and engineering practices that matter in 2026.

Short form:

> Build production-grade agents for applications, machines, and organizations.

## The argument in one page

The model is not the product. Builders ship a system around it: interface, runtime, tools, state, memory, policy, identity, evaluation, observability, and operations.

The book organizes that system across three independent operating surfaces:

```text
Level 1 — Application Agents
Purpose-built web and mobile experiences
Application-scoped state and tools

Level 2 — Machine Agents
Filesystems, shells, processes, browsers, CLIs, and MCP
Machine and environment authority

Level 3 — Organizational Agents
Channels, shared systems, institutional context, and delegation
Organizational identity and policy
```

The levels are not a maturity ladder. The right design uses the smallest authority surface that can solve the problem. When levels compose, authority and provenance must survive every handoff.

The recurring teaching pattern is:

```text
working demo → boundary audit → hardening ladder → production gate
```

The recurring engineering lens is:

```text
surface → runtime → models → tools/skills → state/memory
→ identity/authority → permissions/isolation → human control
→ evaluation → observability → operations
```

## Reader journey

| Stage | Reader starts believing | Reader leaves understanding |
|---|---|---|
| Foundations | The model and chat interface are the agent. | The agent is one component inside an authority-bearing product system. |
| Level 1 | Tool calling and a polished chat are enough. | Tool placement, shared state, generative UI, durable control, identity, and operations determine product quality. |
| Level 2 | A smarter model or more shell access creates a better machine agent. | The harness, skill/context system, access boundary, isolation, and verification loop are the product. |
| Level 3 | Putting the agent in Slack makes it organizational. | Requester, agent, and approver identity; policy; memory governance; delegation; and audit create an organizational actor. |
| Production | A strong final answer proves success. | Result, trajectory, policy compliance, recovery, reliability, cost, and authority must all be evaluated. |

## Canonical examples and evidence boundaries

| Level | Canonical source | What it demonstrates | Hardening delta |
|---|---|---|---|
| 1 | `personal-finance-copilot@d8760064…` | Bare React Native shell, frontend reads, approval-gated writes, native result UI, receipt flow, `BuiltInAgent` route | Server-authorized writes, typed durable state, LangGraph extension, auth, tenant isolation, reconnect, evals |
| 1 web/bridge | `GTM Operations Workspace` | Next.js/PWA shell, selectable agent backends, render-only machine tool visibility | Current v2 renderer, backend authorization, stable adapter, production identity and persistence |
| 2 | `hermes-cpk@fc434913…` plus GTM bridge | CopilotKit/AG-UI seam to a machine harness and visible machine activity | Reproducible external Hermes runtime, identity, scope, approval, sandbox, rollback, audit |
| 3 | CopilotKit `examples/slack@855446e1…` | Current Channels packages, semantic channel UI, sender context, MCP tools, blocking confirmation | Durable store, approver binding, authorization, audit, organizational memory, machine delegation |
| 3 case study | `OpenTag@df93bc0d…` and managed snapshot `d6a80778…` | Multi-channel product architecture and rich interactions | Package modernization, availability verification, governed organizational actor controls |

Evidence labels are defined in `authoring/source-and-evidence-policy.md`. No source-present claim becomes runtime-verified without a recorded run.

## Part I — Foundations

**Part promise:** Give the reader a complete mental model before APIs and product comparisons.

### Chapter 1 — Three Surfaces of Agency

Classify agentic systems by surface, authority, and blast radius. Establish that levels are independent and composable. Introduce the three canonical examples and the book's authority gradient.

**Central decision:** Where should this agent operate?

### Chapter 2 — When Software Starts Choosing

Separate a model-powered feature, deterministic workflow, tool-using assistant, and agent. Show the run/step/tool/observation loop, stop conditions, and when not to add agency.

**Central decision:** Which decisions genuinely require adaptive model judgment?

### Chapter 3 — Open the Hood

Explode the production stack into model, runtime/harness, tools/skills, state/memory, policy, identity, interface, protocols, evaluation, observability, and operations.

**Central decision:** Which subsystem owns each responsibility?

### Chapter 4 — The Interface Is the Control Plane

Show why streaming, uncertain, interruptible work breaks request-response UI assumptions. Define truthful progress, partial artifacts, editability, stop/cancel/rollback semantics, provenance, and recovery.

**Central decision:** What must the user see and control while work is still happening?

**Part bridge:** Once the whole system is visible, build the smallest authority surface: an agent inside an application.

## Part II — Level 1: Application Agents

**Part promise:** Build a purpose-made agent experience on web and mobile with CopilotKit, then harden it into an operable application.

### Chapter 5 — Inside the Application Agent

Trace the finance mobile shell and GTM web shell through CopilotKit and AG-UI to `BuiltInAgent` or service adapters. Introduce LangGraph only as a separately tested durability extension.

**Build milestone:** Run one application agent and trace a complete event lifecycle.

### Chapter 6 — Put the Tool in the Right Place

Choose among frontend, backend, external worker, rendered tool, and human tool. Cover schemas, secrets, side effects, idempotency, retries, and tool-risk metadata.

**Build milestone:** Move one privileged mutation behind an authenticated server boundary.

### Chapter 7 — When the Result Is an Interface

Build display, interactive, and approval components from semantic objects. Teach `useComponent`, `useRenderTool`, `useFrontendTool`, `useHumanInTheLoop`, lifecycle states, accessibility, and web/mobile differences.

**Build milestone:** Render an accessible financial artifact and a structured correction path.

### Chapter 8 — One State, Two Editors

Define task, thread, view, and memory state. Assign field ownership, version changes, handle conflicts, persist checkpoints, and rejoin a run. Contrast `BuiltInAgent` state with a LangGraph durable extension.

**Build milestone:** Reject or rebase one stale user/agent state update.

### Chapter 9 — The Right Moment to Ask

Distinguish client-blocking HITL from a durable runtime interrupt. Bind decisions to exact proposals, show approve/edit/reject, handle disconnect/resume, and separate cancel, rollback, and compensation.

**Build milestone:** Approve an edited synthetic transaction exactly once after reconnect.

### Chapter 10 — Ship the Whole System

Add authentication, tenant isolation, secrets, deployment topology, checkpoints, budgets, traces, evals, release/version discipline, and mobile lifecycle tests.

**Build milestone:** Complete the Level 1 production-readiness worksheet and clean-run scenario.

**Part bridge:** Application tools are deliberate and bounded. Machine agents expose a far broader, dynamically composable capability surface.

## Part III — Level 2: Machine Agents

**Part promise:** Evaluate and harden a machine-agent harness instead of confusing broad access with capability.

### Chapter 11 — The Machine Is the Environment

Map filesystem, shell, process, browser, CLI, MCP, network, credentials, and workspace context. Compare local, remote, container, VM, and dedicated-machine shapes.

**Central decision:** What environment can this agent change?

### Chapter 12 — The Harness Is the Product

Explain instructions, skills, tool discovery, context selection/compaction, durable task state, planning, subagents, hooks, verification loops, and fail-loud operation.

**Central decision:** Which harness controls make behavior repeatable and inspectable?

### Chapter 13 — Draw the Blast Radius

Specify paths, commands, network, credentials, approvals, sandboxes, symlink/path rules, untrusted instructions, poisoned dependencies/skills, dedicated machines, and recovery.

**Build milestone:** Write and adversarially test a machine policy.

### Chapter 14 — Choose the Harness, Not the Logo

Compare Claude Code, Hermes, and OpenClaw using a dated matrix: surface, model, tools/skills, permissions, sandbox, MCP, memory, delegation, observability, hosting, and operations.

**Build milestone:** Produce a use-case-specific decision record, not a universal ranking.

### Chapter 15 — From Visibility to Supervision

Use Hermes + CopilotKit as an unsafe baseline. Connect the control plane, display plans/commands/diffs/tests, then add identity, scope, approval, isolation, recovery, and verification.

**Build milestone:** Complete a repository task inside an enforced boundary and render its evidence.

### Chapter 16 — Operate the Worker

Cover queues, workspaces/worktrees, environment caching, concurrency, budgets, traces, benchmark tasks, failure classification, cleanup, incident response, and reproducible bootstrap.

**Build milestone:** Run a failure and recovery game day.

**Part bridge:** A machine agent usually has one operator and one environment. In an organization, multiple people can invoke shared authority through persistent social context.

## Part IV — Level 3: Organizational Agents

**Part promise:** Move from a working channel agent to an identity-bound, policy-governed organizational actor.

### Chapter 17 — When the Agent Joins the Team

Separate channel bot, channel agent, and governed organizational actor. Preserve who asked, which agent acted, which system accepted the action, and who owns the outcome.

**Central decision:** Has the system crossed the organizational-agent threshold?

### Chapter 18 — One Agent, Many Channels

Explain current Channels core/UI/adapters, semantic IR, direct versus managed paths, platform capabilities, state stores, locks, dedup, transcripts, actions, and OpenTag version truth.

**Build milestone:** Connect one self-hosted agent to one channel with minimum scopes.

### Chapter 19 — Who Asked, Who Acts, Who Approves

Map platform sender, application principal, agent service identity, approver, RBAC/ABAC, delegated credentials, channel policy, and trusted tool authorization. Upgrade confirmation UI into bound approval.

**Build milestone:** Prove wrong-user, replay, expiry, and reauthorization behavior.

### Chapter 20 — Delegation Without Ambient Authority

Design approval records, institutional-memory promotion, audit events, and a signed Level 3-to-Level 2 delegation envelope. Return diffs, commands, tests, hashes, and provenance.

**Build milestone:** Delegate a read-only repository analysis to a sandboxed worker.

### Chapter 21 — Managed, Open, and In Between

Compare direct Channels, OpenTag, managed CopilotKit direction, and Claude Tag on identity, hosting, state, tools, approvals, memory, audit, data, operations, and availability.

**Build milestone:** Write a build-versus-buy responsibility matrix.

### Chapter 22 — Operate the Organizational Actor

Stage rollout from synthetic/read-only to reversible writes, machine delegation, curated memory, and ambient/scheduled work. Define SLOs, spend, kill switches, incident response, retention, revocation, and decommissioning.

**Build milestone:** Run duplicate-event, wrong-approver, revoked-credential, and restart scenarios.

**Part bridge:** The three surfaces differ, but their production questions converge: did the system take the right path, stay within authority, recover, and earn its cost?

## Part V — Production Engineering Across All Levels

**Part promise:** Turn the three-level model into one reusable production discipline.

### Chapter 23 — Evaluate the Trajectory

Evaluate tools, arguments, state transitions, policy, latency, cost, intervention, and recovery—not only the final text. Build unit, node, trajectory, simulation, and online evaluation layers with LangSmith as the canonical example.

### Chapter 24 — Secure the Authority Surface

Threat-model prompt/behavior hijacking, tool misuse, identity/privilege abuse, memory poisoning, data leakage, skills/supply chain, delegation, and cross-level confused deputies. Match controls to authority.

### Chapter 25 — Reliability Has a Budget

Specify latency, retries, timeouts, idempotency, queues, concurrency, model routing, context, caching, fallbacks, SLOs, alerts, and cost/step budgets.

### Chapter 26 — Choose the Smallest Sufficient Level

Use a decision tree and matrix to select application tools, machine harness, organizational channel, or hybrid composition. End with architecture records and a next-build plan.

**Final action:** Choose one real use case, bound its authority, and write the first production gate before adding autonomy.

## Cross-chapter continuity rules

1. Introduce a concept once at full depth; later chapters show how it changes by level.
2. Each level revisits the same eleven engineering knobs in the same order.
3. Every expansion of authority adds stronger identity, isolation, supervision, provenance, and recovery.
4. Keep source-present examples and target hardening visibly separate.
5. End every level with an operability chapter and a production-readiness artifact.
6. Never describe a frontend confirmation card, visible command, sender context, platform scope, or prompt rule as an enforced security boundary.
7. Return to the canonical line: **the interface is the control plane; the enforcement point lives at the trusted boundary.**

## Completion definition for the integrated manuscript draft

**Draft status — 2026-07-15:** All 26 numbered chapter files, five part openers, front matter, and the field guide now exist. The manuscript is in whole-book integration and visual QA; remaining work is technical verification, current-fact review, copyediting, evidence-gated capture, and final layout rather than missing-chapter drafting.

The integrated manuscript is structurally complete when every chapter contains:

- a compelling opening problem;
- one explicit reader outcome;
- the core mental model and decision;
- code/figure/table placements;
- evidence-aware claims;
- an exercise with an inspectable result;
- a failure/security section;
- a production checklist;
- one quotable line target;
- a bridge to the next chapter;
- a word/page budget.

Runtime-gated screenshots or code may remain explicitly marked for production. They may not be silently fabricated.

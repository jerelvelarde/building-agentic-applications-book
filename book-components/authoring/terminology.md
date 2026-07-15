---
title: Canonical Terminology
status: active-drafting
updated: 2026-07-14
---

# Canonical terminology

Use these terms consistently across keypoints, manuscript, figures, code annotations, and captions. When a product uses a conflicting noun, state the product-specific mapping.

## The three levels

| Canonical term | Definition | Do not imply |
|---|---|---|
| **Level 1 — Application Agents** | Agents embedded in a purpose-built web or mobile application, operating through application-scoped state and tools. | That a chat layout alone is agentic or that Level 1 is inferior. |
| **Level 2 — Machine Agents** | Agents operating inside a workstation, server, container, VM, or dedicated machine through filesystem, shell, process, browser, CLI, and configured tool access. | That shell access alone provides a safe harness. |
| **Level 3 — Organizational Agents** | Shared agents acting in collaboration and work systems under explicit organizational identity, authority, policy, memory, and accountability. | That appearing in Slack or Teams automatically crosses this threshold. |
| **Agentic application** | The whole product system: interface, runtime, model, tools, state, memory, policy, identity, observability, evaluation, and operations. | That the model or agent loop is the entire product. |

The levels are independent operating surfaces with expanding authority and blast radius, not a maturity ladder every product must climb.

## Execution terms

| Term | Book definition | Caveat |
|---|---|---|
| **Model-powered feature** | A bounded model call controlled by application code. | May have no adaptive loop. |
| **Workflow** | A developer-authored, predetermined execution path or graph; nodes may call models. | Conditional branches do not automatically make it an agent. |
| **Agent** | A runtime in which a model selects actions and tool use from current state and observations until it finishes, pauses, fails, or reaches a limit. | Always exists inside a harness and policy envelope. |
| **Run** | One user-visible attempt to pursue a goal under a start and terminal lifecycle. | In LangSmith, a “run” can also mean a traced span; qualify where needed. |
| **Step** | A named unit inside a run. | Not guaranteed to equal a graph node, model thought, or tool call. |
| **Tool call** | A structured request to invoke a named capability with arguments, plus an optional result. | A request event is not proof of a completed side effect. |
| **Thread** | A stable task or conversation container joining related runs and durable state. | A platform thread, agent thread, and business case ID may map without being identical. |
| **Checkpoint** | Persisted runtime state at a recoverable execution boundary. | Does not reverse external side effects. |
| **Trace** | An observability record composed of spans/runs. | Not product state or durable memory. |

## System components

| Term | Definition |
|---|---|
| **Runtime** | Executes the agent or graph, emits events, applies limits, retries, pauses, and resumes. |
| **Harness** | The machinery that turns a model into a repeatable agent: instructions, tools, skills, context selection, permissions, execution loop, verification, and lifecycle. |
| **Tool** | A typed capability an agent may invoke to read, compute, or change something. |
| **Skill** | Reusable procedural knowledge or workflow instructions loaded by a harness; it may refer to tools but is not itself permission. |
| **Policy** | Rules evaluated at a trusted enforcement point to allow, deny, constrain, or require approval for an action. Prompt text is guidance, not policy enforcement. |
| **Sandbox** | An enforced isolation boundary for filesystem, processes, network, and resources. A working directory convention is not a sandbox. |
| **Dedicated machine** | A separately governed physical or virtual machine whose credentials, filesystem, network, and lifecycle are scoped to agent work. |

## State and memory

| Term | Definition | Default question |
|---|---|---|
| **View state** | Current component/session presentation such as an open panel. | Does the agent need this at all? |
| **Task state** | Typed facts describing current progress, artifacts, decisions, and errors. | Who owns each field? |
| **Thread state** | Durable state shared across related runs. | Who may rejoin or delete it? |
| **Long-term memory** | Information intentionally available across threads for a user or account. | What are provenance, TTL, correction, and consent? |
| **Institutional memory** | Organization-approved knowledge with provenance, scope, review, effective dates, access, and deletion controls. | Who owns and reviews it? |
| **Transcript** | Retained conversational history. | Never use as a synonym for institutional memory. |

## Interaction and control

| Term | Definition |
|---|---|
| **Generative UI** | The agent selects a semantic object or registered component; the application owns rendering, interaction, accessibility, and action boundaries. |
| **Frontend tool** | A tool whose handler executes in the browser or native client. It cannot safely hold service secrets or become the sole authority for privileged writes. |
| **Rendered tool** | A UI projection of a tool executed by a backend or external runtime. Rendering does not move authority to the client. |
| **Human-in-the-loop (HITL)** | A run pauses at a meaningful decision boundary, presents exact context, receives an identified decision, and resumes. |
| **Approval** | A policy-relevant decision bound to an exact proposal, eligible principal, scope, version, and expiry. A generic confirmation button is not sufficient. |
| **Interrupt** | A runtime or tool pause awaiting external input. Name whether it is client-local or durably checkpointed. |
| **Cancel/stop** | Prevents some future work according to documented semantics. |
| **Rollback** | Restores runtime/application state to a prior point. |
| **Compensation/undo** | A domain-specific action that reverses or mitigates an already completed side effect. |

## Protocols and channel terms

| Term | Definition |
|---|---|
| **AG-UI** | Event protocol between an agent runtime and a user-facing application: run, message, tool, state, activity, and interrupt events. |
| **MCP** | Protocol for connecting agents to tools, resources, and data. It does not replace AG-UI. |
| **Channels SDK** | CopilotKit's channel-neutral runtime, semantic UI, and platform-adapter package family. Use current `@copilotkit/channels*` package names in new code. |
| **Channel adapter** | Translates platform ingress and semantic output for Slack, Discord, Teams, or another surface. |
| **Channel bot** | Receives and sends platform events. |
| **Channel agent** | Uses a model/runtime and tools to pursue goals through a channel. |
| **Governed organizational actor** | A channel agent with explicit service identity, enforceable authority, policy, approvals, memory governance, audit, and operational ownership. |
| **Requester principal** | The trusted application identity of the person or system asking for work. |
| **Agent principal** | The service identity under which the organizational agent acts. |
| **Approver principal** | An authenticated identity eligible under policy to decide a specific proposal. |

## Product naming and time-sensitive terms

- **CopilotKit**, never “Copilot Kit” in prose.
- **OpenTag** is the CopilotKit open-source channel-agent project.
- **Claude Tag** is Anthropic's managed organizational-agent product. Reverify availability and supported channels at publication freeze.
- **Hermes** refers to the machine-agent harness/runtime used by the audited bridge examples; pin the exact external runtime before implementation claims.
- **OpenClaw** and **Claude Code** require dated, primary-source comparison evidence before feature claims.
- **CopilotKit Intelligence** must be labeled early access, waitlisted, internal, or generally available according to current official evidence at publication freeze.

---
chapter: 11
title: The Machine Is the Environment
plan_title: The Machine as an Agent Environment
part: Level 2
target_words: 2100
target_pages: 10
status: ready-to-draft
---

# Chapter 11 — The Machine Is the Environment

## Hook

A repository-scoped task reads a malicious file, invokes an allowed shell, inherits a cloud token, and reaches outside the working directory. The model never “escaped”; the process was never confined.

## Reader outcome

Map a machine-agent harness and distinguish workspace routing, tool policy, approval, OS sandbox, and host isolation.

## Core claims

- A machine agent is a harness, not an LLM with shell access.
- Working directory and repository instructions select context; they do not create an OS boundary.
- Tool policy controls dispatched capabilities; sandbox/container/VM controls what the process can actually touch.
- Files, processes, browser, CLIs, MCP, network, credentials, and persistence are separate capability surfaces.
- Threat model actors, inputs, assets, effects, persistence, and recovery before selecting a product.

## Code, figure, and table inventory

- **Figure:** ten-part machine harness from run intake through verifier/audit.
- **State machine:** context → action intent → policy → execution → observation → verification.
- **Table:** five boundaries and what each does/does not control.
- **Map:** capability surface and blast radius.

## Canonical evidence

- `materials/evidence-packets/level-2-machines.md`, executive findings and Chapter 11.
- First-party Claude Code, Hermes, and OpenClaw sources pinned in its registry.

## Exercise

Threat-model one machine-agent use case. List requesters, untrusted inputs, assets, side effects, persistence, and recovery objective; draw every enforcement boundary.

## Failure and security section

Demonstrate the working-directory fallacy, terminal bypass of file guards, inherited secrets, broad network egress, exposed sockets, and mutually untrusted users sharing one gateway.

## Production checklist

- [ ] Workspace is server-selected and identified.
- [ ] Tool and process boundaries separate.
- [ ] Execution identity and isolation profile explicit.
- [ ] Credentials and network reach inventoried.
- [ ] Recovery objective defined before writes.

## Quotable line target

> A working directory tells the agent where to begin; only an enforced boundary tells the process where it must stop.

## Bridge

Chapter 12 fills the harness with the instructions, skills, context, tools, and verification loops that make behavior repeatable.

## Budget

2,100 prose words; 10 pages; architecture-first.

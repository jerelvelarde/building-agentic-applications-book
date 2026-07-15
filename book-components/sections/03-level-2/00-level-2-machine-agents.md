---
title: "Part III — Level 2: Machine Agents"
part: "Level 2 — Machine Agents"
status: review-draft
updated: 2026-07-15
---

# Part III — Level 2: Machine Agents

In Level 1, the ledger agent acted through product-shaped capabilities. It could search transactions, render a spending artifact, and propose a versioned write. The application decided which tools existed. A trusted service protected the source of truth.

Now the task changes:

> Add a category-budget feature to the ledger application. Inspect the repository, update the web and mobile clients, install any required dependency, run the checks, and return a reviewable diff.

The agent no longer needs one ledger tool. It needs an environment.

Files, directories, processes, package managers, source control, browsers, CLIs, network destinations, MCP servers, credentials, caches, and persistent memory all become potential capability surfaces. A repository file can shape the agent's instructions. A shell can bypass a guard implemented only in a file tool. A worktree can isolate changes without isolating the process. A dedicated machine can reduce personal-device risk while still accumulating secrets and reachable services.

Level 2 is therefore not “Level 1 with a terminal.” It is a different authority envelope.

This part follows one builder question through six chapters:

> What authority is this run using, which boundary enforces it, what evidence will the user see, and how will we recover if the action is wrong?

Chapter 11 treats the machine as an environment and opens the ten-part harness. Chapter 12 makes instructions, skills, plugins, MCP, tools, approvals, and verification explicit supply-chain and control surfaces. Chapter 13 writes the path, command, network, credential, isolation, and recovery policy. Chapter 14 compares Claude Code, Hermes, and OpenClaw by operating model rather than logo. Chapter 15 uses the Hermes–CopilotKit seam as an intentionally unsafe baseline and climbs toward real supervision. Chapter 16 turns one hardened run into a durable worker operating model.

The examples use synthetic repositories and credentials. The pinned Hermes–CopilotKit applications prove an inspectable UI seam and recent HTTP availability, not an end-to-end machine run. Where that live run could not be verified, this part uses source-faithful schematics derived from the pinned application state and inspected code paths. The external `/hermes/` runtime and adapter were unavailable during the evidence pass, so those schematics are not presented as proof of live execution. **Verified July 2026.**

The goal is not to make the machine agent feel fearless. It is to make every consequential action bounded, legible, interruptible, verifiable, and recoverable.

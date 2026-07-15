---
chapter: 5
title: Inside the Application Agent
plan_title: The Anatomy of an In-App Agent
part: Level 1
target_words: 2100
target_pages: 10
status: ready-to-draft
---

# Chapter 5 — Inside the Application Agent

## Hook

Follow one question—“Where did I overspend?”—from the finance mobile screen through CopilotKit and AG-UI to the runtime, tool set, and visible result. Show every handoff the user never sees.

## Reader outcome

Trace a complete application-agent run and explain when `BuiltInAgent`, a service adapter, or a LangGraph extension is appropriate.

## Core claims

- CopilotKit owns the interaction layer, not the data-security perimeter.
- AG-UI carries observable lifecycle, message, tool, and state events.
- The audited finance example uses `BuiltInAgent`; GTM Operations Workspace uses selectable adapters; neither proves LangGraph durability.
- Start with the smallest runtime that satisfies execution and recovery needs; add LangGraph when explicit topology, checkpointing, or durable interrupts matter.

## Code, figure, and table inventory

- **Code:** finance `App.tsx`, custom `ChatScreen.tsx`, runtime agent, catch-all route (`L1-01`, `L1-02`).
- **Figure:** native/web client → authenticated AG-UI boundary → runtime → product services.
- **Table:** `BuiltInAgent` vs LangGraph decision dimensions.
- **Screenshots:** mobile dashboard/assistant and GTM shell; current captures remain reference-only.

## Canonical evidence

- Level 1 packet executive findings 3, 7–9; sections 4, 7, 11, 15–18.
- Finance and anonymized operations-workspace entries in `reference-projects/README.md` and `materials/evidence-packets/level-1-foundations.md`.

## Exercise

Run or inspect one pinned shell and annotate a single run with run ID, agent ID, tool registration, runtime route, event families, and source-of-truth data boundary.

## Failure and security section

Show missing model key, unreachable runtime, client-selected backend not server-allowlisted, and unauthenticated thread access. Explain that a provider key or health route does not verify an agent call.

## Production checklist

- [ ] Runtime and package versions pinned.
- [ ] Agent/thread identity authenticated.
- [ ] Missing config fails loudly.
- [ ] Event and error lifecycle visible.
- [ ] LangGraph claims match a tested extension only.

## Quotable line target

> The fastest way to misunderstand an agentic app is to start at the chat box and stop before the runtime boundary.

## Bridge

The run is connected; Chapter 6 decides where each capability should execute.

## Budget

2,100 prose words; 10 pages; one end-to-end trace.

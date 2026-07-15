---
chapter: 4
title: The Interface Is the Control Plane
plan_title: The Agentic UI Problem
part: Foundations
target_words: 1900
target_pages: 10
status: ready-to-draft
---

# Chapter 4 — The Interface Is the Control Plane

## Hook

Open on a user closing a spinner after thirty seconds, retrying, and accidentally creating two external actions. Nothing in the interface explained whether work was running, blocked, complete, or safe to repeat.

## Reader outcome

Design a task surface for streamed, partial, fallible, interruptible work with truthful status and explicit control semantics.

## Core claims

- Agentic work breaks immediate, deterministic request-response assumptions.
- Useful intermediate artifacts often matter more than streamed prose.
- `running: boolean` is too weak; the UI needs planning, waiting, retrying, partial, cancel-requested, failed, and complete states.
- Stop, disconnect, interrupt, cancel, rollback, and compensation are different operations.
- Trust comes from operational evidence, not hidden chain-of-thought.

## Code, figure, and table inventory

- **Figure:** conventional request-response vs agentic task sequence.
- **State machine:** idle → planning/running/waiting/retrying/partial/cancelled/failed/complete.
- **Table:** user intent vs actual cancellation/recovery mechanism.
- **Screenshot grid:** progress, approval, failure, and rejoin states; use reference frames only as composition until recaptured.

## Canonical evidence

- Level 1 packet sections 5–6, 14, and trust stack.
- AG-UI event families cited in Level 1 packet.
- `images/repository-captures/*/CAPTURE NOTES.md` for current proof limits.

## Exercise

Replace a spinner in an existing AI feature with stage, current action, first useful artifact, stop semantics, and recovery copy. Test a disconnect and a tool failure.

## Failure and security section

Cover fake percentages, duplicate retries, premature success, raw tool arguments leaking secrets, and “Undo” labels without compensation. Accessibility: no color-only status, focus-safe streaming, accessible chart summaries.

## Production checklist

- [ ] Task phases and invalid transitions defined.
- [ ] Progress is evidence-based.
- [ ] Stop/cancel/disconnect semantics stated.
- [ ] Completed side effects remain visible.
- [ ] Failure and recovery are first-class states.
- [ ] Tool UI passes accessibility checks.

## Quotable line target

> In an agentic application, the interface is not the prompt box; it is the place where autonomy becomes legible and controllable.

## Bridge

With the control-plane requirements established, Part II builds the first concrete Level 1 system in CopilotKit.

## Budget

1,900 prose words; 10 designed pages; high visual density.

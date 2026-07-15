---
chapter: 23
title: Evaluate the Trajectory
plan_title: Evaluation That Measures the Whole System
part: Production
target_words: 2200
target_pages: 11
status: ready-to-draft
---

# Chapter 23 — Evaluate the Trajectory

## Hook

An agent returns the correct ledger total after reading the wrong tenant, retrying a write, and ignoring an approval. A final-answer judge gives it full credit.

## Reader outcome

Build an evaluation pyramid that measures deterministic boundaries, adaptive trajectory, policy, recovery, user experience, latency, and cost.

## Core claims

- Evaluate the complete run, not only the final prose.
- Put most volume in deterministic tool/reducer contracts; use node, trajectory, simulation, and sampled online evals for adaptive behavior.
- Define required events, forbidden events, repetition limits, budgets, and terminal invariants.
- LangSmith and OpenTelemetry are complementary; neither is product state or the immutable action ledger.
- Confirmed production failures should become minimized, redacted regression cases.

## Code, figure, and table inventory

- **Figure:** evaluation pyramid and production-to-regression loop.
- **Code:** subset trajectory evaluator with required safe-write path; pinned/tested before print.
- **Dataset:** golden, boundary, policy, adversarial, reliability, and production-regression suites.
- **Trace figure:** correlated agent trace, service trace, action-ledger row.

## Canonical evidence

- `materials/evidence-packets/production-engineering.md`, Chapter 23.
- Official LangSmith/AgentEvals/OpenTelemetry sources cited there.

## Exercise

Create one case per suite for a canonical example. Make a plausible final answer fail because of a forbidden tool, duplicate effect, missing approval, or budget breach; route the trace into a regression dataset.

## Failure and security section

Cover uncalibrated LLM judges, averages hiding critical failures, production payload leakage, experimental telemetry fields, high-cardinality IDs in metrics, and baggage used as trusted identity.

## Production checklist

- [ ] Critical deterministic/policy suites zero-failure.
- [ ] Consequential tools test denial, duplicate, timeout, ambiguity, cancellation.
- [ ] Judges calibrated/versioned.
- [ ] Crash/resume runtime-observed.
- [ ] Risk-based online sampling and redaction.
- [ ] Action ledger retained separately from sampled traces.

## Quotable line target

> A convincing answer can still be the final sentence of an unsafe trajectory.

## Bridge

Evaluation tells us whether controls work. Chapter 24 designs those controls around the authority each level carries.

## Budget

2,200 prose words; 11 pages; metrics and trace visuals.

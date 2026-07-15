---
chapter: 25
title: Reliability Has a Budget
plan_title: Reliability, Cost, and Scaling
part: Production
target_words: 2100
target_pages: 10
status: ready-to-draft
---

# Chapter 25 — Reliability Has a Budget

## Hook

A provider slows down, the gateway retries, the queue redelivers, and the agent fans out to more tools. Each layer is “resilient”; together they exceed the user's deadline and budget and duplicate an effect.

## Reader outcome

Operate agentic systems within explicit latency, reliability, concurrency, and cost budgets with safe retry and degraded-mode behavior.

## Core claims

- Durable execution does not create exactly-once side effects; idempotency and outcome lookup belong at the tool boundary.
- Retry only classified transient errors, at one chosen layer, inside remaining time/cost budgets, with backoff and jitter.
- Enforce model calls, tool calls, depth, parallelism, output, egress, elapsed time, and cost before every step.
- Agent SLOs describe a journey: acknowledgement, first useful artifact, correct terminal state, queue delay, resume success, intervention latency.
- Unauthorized action, cross-tenant access, and secret leakage are zero-tolerance invariants, not error-budget events.
- Pool/silo/bridge tenant models trade cost, isolation, and blast radius.

## Code, figure, and table inventory

- **Code/config:** run budget checked before each step; retry classifier and idempotency/outcome ledger.
- **Figure:** deadline/budget propagation across UI, gateway, queue, worker, model, tool.
- **Table:** error class → retry/deny/review/recover.
- **Scorecard:** SLOs, budget burn, queue/concurrency, resume, duplicate effects, cost per verified outcome.

## Canonical evidence

- Production evidence packet executive findings 8–13 and telemetry dictionary.
- Level 1 retry/idempotency cases; Level 2 durable-run model; Level 3 retry/dedup guidance.

## Exercise

Inject 429, 5xx, timeout-before-commit, timeout-after-commit, queue redelivery, provider degradation, and budget exhaustion. Prove one retry owner, one side effect, truthful terminal state, and bounded cost.

## Failure and security section

Cover retry storms, cascading delegation, ambiguous outcomes, model fallback changing tool behavior, shared-tenant noisy neighbor, unbounded observability cardinality, and cost dashboard without runtime enforcement.

## Production checklist

- [ ] Journey SLOs and safety invariants defined.
- [ ] Deadline/budget propagated.
- [ ] Retry owner and classifier explicit.
- [ ] Consequential writes idempotent/outcome-ledgered.
- [ ] Queue/concurrency/circuit breakers tested.
- [ ] Degraded mode and incident alerts owned.

## Quotable line target

> Reliability is not how often the agent keeps trying; it is how predictably the system reaches a truthful outcome inside its authority and budget.

## Bridge

The book now has every production knob. Chapter 26 uses them to choose the smallest architecture that can create the outcome.

## Budget

2,100 prose words; 10 pages; SLO and failure-injection heavy.

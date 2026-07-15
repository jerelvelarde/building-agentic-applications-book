---
chapter: 26
title: Choose the Smallest Sufficient Level
plan_title: Choosing the Right Level
part: Production
target_words: 1700
target_pages: 9
status: ready-to-draft
---

# Chapter 26 — Choose the Smallest Sufficient Level

## Hook

Return to the opening goal. It can be solved by an app-scoped analysis tool, a machine worker, or an organizational agent. Each version adds capability—and a different operating burden.

## Reader outcome

Select Level 1, 2, 3, or a narrow hybrid using outcome, authority, interaction, environment, identity, and operational constraints.

## Core claims

- Choose the smallest authority surface that can create the desired outcome.
- Application tools are enough when capabilities can be typed and scoped to product state.
- A machine harness is justified when environment discovery and dynamic composition matter more than a fixed tool surface.
- An organizational agent is justified when shared invocation, asynchronous team work, service identity, and governed institutional context create real value.
- Hybrid systems should compose levels through typed, authenticated, expiring task contracts—not ambient context or credentials.
- More autonomy is not the default migration path; deterministic nodes and narrower tools remain valid endpoints.

## Code, figure, and table inventory

- **Decision tree:** outcome → required surface/context → side effects → identity → duration → human control → smallest level.
- **Matrix:** levels across eleven engineering knobs, blast radius, and operating owner.
- **Patterns:** pure Level 1, app + machine worker, channel + app tools, channel + bounded machine delegation.
- **Artifact:** one-page architecture decision record.

## Canonical evidence

- Master outline and the authority gradient across all evidence packets.
- Production evidence packet executive finding 14.
- Level readiness checklists from Chapters 10, 16, and 22.

## Exercise

Choose a real use case. Write the user outcome, current surface, required context, minimum tools, acting identity, worst side effect, human gates, recovery, evaluation, owner, and why the next-higher level is unnecessary today.

## Failure and security section

Cover convenience-driven shell access, putting a private task in a shared channel, premature institutional memory, multi-agent inflation, and a hybrid handoff that loses requester/policy provenance.

## Production checklist

- [ ] Outcome and non-goals explicit.
- [ ] Smallest authority surface justified.
- [ ] Deterministic alternatives considered.
- [ ] Owners and gates assigned.
- [ ] Hybrid contracts typed/authenticated/expiring.
- [ ] Reassessment trigger defined.

## Quotable line target

> The best agent architecture is not the one with the most autonomy; it is the one that creates the outcome with the least authority you must continuously defend.

## Bridge

Close by sending the reader back to the companion examples: choose one level, implement one vertical slice, prove one failure path, and expand only when evidence earns it.

## Budget

1,700 prose words; 9 pages; synthesis and decision matrix.

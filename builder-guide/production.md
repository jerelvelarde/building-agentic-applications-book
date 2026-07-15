# Production engineering across all three levels

Production readiness is not a fourth level. It is the evaluation, security, reliability, and architecture discipline applied to every operating surface.

## Read

1. [Evaluate the trajectory](../book-components/sections/05-production/23-evaluate-the-trajectory.md)
2. [Secure the authority surface](../book-components/sections/05-production/24-secure-the-authority-surface.md)
3. [Reliability has a budget](../book-components/sections/05-production/25-reliability-has-a-budget.md)
4. [Choose the smallest sufficient level](../book-components/sections/05-production/26-choose-the-smallest-sufficient-level.md)

## Inspect and run

- [`trajectory.ts`](../companion/src/production/trajectory.ts) — outcome and execution-trajectory evaluation.
- [`run-budget.ts`](../companion/src/production/run-budget.ts) — bounded runtime budgets.
- [`production.test.ts`](../companion/tests/production.test.ts) — executable production-control cases.

## Ship gate

- Evaluate both task outcome and the path taken to reach it.
- Enforce policy outside model context and fail closed when the control plane is unavailable.
- Maintain one operation identifier and one retry owner across services.
- Define time, step, token, cost, network, and side-effect budgets.
- Test degraded modes, cancellation, duplicate delivery, stale work, and recovery.
- Choose the smallest operating surface that can safely achieve the goal.

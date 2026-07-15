# Level 2 — Machine agents

Level 2 agents operate on a workspace or host. The model is only one part of the product; the harness owns identity, context assembly, capabilities, policy, execution, persistence, evidence, verification, and recovery.

## Read

1. [The machine is the environment](../book-components/sections/03-level-2/11-the-machine-is-the-environment.md)
2. [The harness is the product](../book-components/sections/03-level-2/12-the-harness-is-the-product.md)
3. [Draw the blast radius](../book-components/sections/03-level-2/13-draw-the-blast-radius.md)
4. [Choose the harness, not the logo](../book-components/sections/03-level-2/14-choose-the-harness-not-the-logo.md)
5. [From visibility to supervision](../book-components/sections/03-level-2/15-from-visibility-to-supervision.md)
6. [Operate the worker](../book-components/sections/03-level-2/16-operate-the-worker.md)

## Inspect and run

- [`machine-policy.ts`](../companion/src/level-2/machine-policy.ts) — allow, deny, and approval decisions.
- [`workspace.ts`](../companion/src/level-2/workspace.ts) — realpath-aware workspace containment.
- [`ag-ui-bridge.ts`](../companion/src/level-2/ag-ui-bridge.ts) — machine events surfaced through an application control plane.
- [`machine-policy.test.ts`](../companion/tests/machine-policy.test.ts) and [`workspace.test.ts`](../companion/tests/workspace.test.ts) — executable boundary cases.

## Builder checklist

- Inventory every capability: files, shell, processes, network, credentials, browser, CLIs, MCP, and persistence.
- Promote reusable skills through review instead of treating downloaded instructions as trusted code.
- Separate the planning identity from the execution identity.
- Use path containment, network policy, sandboxing, budgets, and approval gates together.
- Make side effects idempotent and independently verify completion.
- Plan for a dedicated worker or machine when isolation, credential scope, or lifecycle warrants it.

## Reference implementation

Use the pinned [Hermes CPK](../reference-projects/README.md#hermes-cpk) demo to study the Level 1-to-Level 2 seam. The book treats it as a visible machine-agent baseline and then adds the supervision and containment controls needed for production.

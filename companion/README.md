# Agentic Applications 2026 companion snippets

Original, book-oriented examples for _The Builder's Guide to Agentic Applications 2026_. They teach boundaries and controls; they are not copies of the audited demo repositories.

## Verification status

- **Executable and tested:** state ownership, server write boundary, machine policy, realpath/symlink containment, governed approvals, replay suppression, trajectory evaluation, run budgets, and the LangGraph interrupt/resume graph.
- **Compile-verified integration:** CopilotKit v2 hooks, rendered tools, immediate HITL UI, AG-UI custom events, Channels SDK Slack wiring, and the server-side ledger reference slice under `apps/ledger-web/`.
- **Not included as a runnable app in this draft:** the browser client, model-backed AG-UI runtime, Slack deployment, and external financial write. Those need a complete host application, credentials, a running agent endpoint, synthetic data, and a capture ledger.

`skipLibCheck` is enabled because the exact published CopilotKit/Channels dependency graph has third-party declaration conflicts under `exactOptionalPropertyTypes`. Strict checking remains enabled for all companion source and tests.

## Snippet map

| ID              |   Chapter | File                                    | Status                                             |
| --------------- | --------: | --------------------------------------- | -------------------------------------------------- |
| L1-TOOLS        |       6–7 | `src/level-1/ledger-tools.tsx`          | Compile-verified                                   |
| L1-STATE        |         8 | `src/level-1/shared-state.ts`           | Tested                                             |
| L1-BOUNDARY     |      6, 9 | `src/level-1/runtime-boundary.ts`       | Tested by type/build gates; adapter is injectable  |
| L1-GRAPH        |       8–9 | `python/src/book_agent/ledger_graph.py` | Tested                                             |
| L2-POLICY       |        13 | `src/level-2/machine-policy.ts`         | Tested                                             |
| L2-WORKSPACE    |        13 | `src/level-2/workspace.ts`              | Tested, including symlink escape                   |
| L2-AGUI         |        16 | `src/level-2/ag-ui-bridge.ts`           | Compile-verified                                   |
| L3-CHANNELS     |        18 | `src/level-3/channels-bot.ts`           | Compile-verified; credentials required to run      |
| L3-GOVERN       | 19–20, 22 | `src/level-3/governed-action.ts`        | Tested, including unauthorized approver and replay |
| PROD-TRAJECTORY |        23 | `src/production/trajectory.ts`          | Tested                                             |
| PROD-BUDGET     |        25 | `src/production/run-budget.ts`          | Tested                                             |

## Exact versions

- Node `>=22.11.0`; verified with Node `25.8.2`
- TypeScript `5.9.3`, Vitest `4.1.3`
- React/React DOM `19.2.3`
- CopilotKit React Core `1.62.3`
- AG-UI client/core `0.0.57`
- Channels `0.1.1`, Channels UI `0.1.1`, Channels Slack `0.1.2`
- Python `>=3.11`; verified with Python `3.11.15`
- LangGraph `1.2.9`, pytest `9.1.1`, Ruff `0.15.21`

The CopilotKit and Channels API selection is grounded in CopilotKit commit [`855446e1abc8f29756dc5e539e5e50a90321ac2d`](https://github.com/CopilotKit/CopilotKit/tree/855446e1abc8f29756dc5e539e5e50a90321ac2d). Re-run every gate before publishing a new book edition.

## Verify

```bash
npm ci
npm run format:check
npm run lint
npm run typecheck
npm test
npm run build
```

```bash
cd python
uv sync --group dev --python 3.11
uv run ruff format --check .
uv run ruff check .
uv run pytest -q
```

The July 15, 2026 verification produced 13 passing TypeScript tests across five files, two passing Python tests, clean format/lint/typecheck/build gates, and zero npm audit vulnerabilities. The First Draft repository intentionally compiles the ledger server boundary without claiming that it ships a complete browser application.

## Runtime boundaries to preserve

1. A frontend schema makes arguments typed; it does not authorize a privileged write.
2. An AG-UI event makes machine intent visible; it does not grant a filesystem, command, or network capability.
3. A channel button captures a choice; the server must bind it to an eligible approver, exact request/action digest, expiry, and idempotency key.
4. LangGraph resumes the interrupted node from its start. Keep non-idempotent effects after the interrupt.

All companion source is original and MIT-licensed. Framework names and API shapes are used for interoperability; see the excerpt catalog for per-snippet provenance.

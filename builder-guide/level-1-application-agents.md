# Level 1 — Application agents

Level 1 agents operate inside a web or mobile product. The application owns the user experience, typed state, authenticated server boundary, and the tools the agent may propose or execute.

## Read

1. [Inside the application agent](../book-components/sections/02-level-1/05-inside-the-application-agent.md)
2. [Tools are trust boundaries](../book-components/sections/02-level-1/06-tools-are-trust-boundaries.md)
3. [Generative UI as a contract](../book-components/sections/02-level-1/07-generative-ui-as-a-contract.md)
4. [Shared state without lost work](../book-components/sections/02-level-1/08-shared-state-without-lost-work.md)
5. [Pause, resume, and approve](../book-components/sections/02-level-1/09-pause-resume-and-approve.md)
6. [Ship the whole system](../book-components/sections/02-level-1/10-ship-the-whole-system.md)

## Inspect and run

- [`ledger-tools.tsx`](../companion/src/level-1/ledger-tools.tsx) — frontend tools, render contracts, and explicit action boundaries.
- [`runtime-boundary.ts`](../companion/src/level-1/runtime-boundary.ts) — server-side authorization boundary.
- [`shared-state.ts`](../companion/src/level-1/shared-state.ts) — revision-aware state updates.
- [`risk.ts`](../companion/src/level-1/risk.ts) — action risk classification.
- [`ledger_graph.py`](../companion/python/src/book_agent/ledger_graph.py) — LangGraph interrupt and resume.
- [`ledger-service.ts`](../companion/apps/ledger-web/server/ledger-service.ts) — compile-checked ledger service boundary.

```bash
cd companion
npm ci
npm run verify
```

```bash
cd companion/python
uv sync --group dev --python 3.11
uv run pytest -q
```

## Builder checklist

- Decide which tools render in the client and which effects execute on the server.
- Treat tool schemas as validation, not authorization.
- Store semantic state with explicit ownership and revisions.
- Bind approvals to the exact proposal, principal, resource version, and expiry.
- Design streaming, interruption, recovery, and terminal evidence before polishing the chat surface.

## Reference implementation

The canonical external example is the pinned [Personal Finance Copilot](../reference-projects/README.md#personal-finance-copilot), a React Native application with frontend read tools, inline components, approval-gated writes, and receipt parsing.

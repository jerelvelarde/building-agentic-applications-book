---
title: Level 1 Repository Capture Notes
type: evidence
status: partial
created: 2026-07-14
updated: 2026-07-14
---

# Level 1 Repository Capture Notes

## Scope and evidence status

This folder records the attempted live capture of the two pinned Level 1 repositories. No model output was fabricated and no private or live financial data was used.

- `personal-finance-copilot`: `d8760064c626712a8fa15c192a8c4bc69bb24055`
- `GTM Operations Workspace`: `private revision omitted`
- Capture date: 2026-07-14
- Host model credentials: `OPENAI_API_KEY` absent; `ANTHROPIC_API_KEY` absent

The five PNGs in this folder are byte-identical copies of repository-committed iPhone simulator screenshots from `personal-finance-copilot/docs/screenshots/`. They are prior run evidence from the pinned repository, not screenshots produced during this capture session. They use the repository's synthetic finance fixtures.

No GTM Operations Workspace screenshot was captured. The web application ran and returned HTTP 200, but the required in-app browser-control runtime reported no available browser backend. The capture was not replaced with an unrelated browser-control mechanism.

## Personal Finance Copilot

### Run attempt and environment

Clone inspected at `/tmp/personal-finance-copilot`.

Dependencies had already been installed for the application and `runtime/`. Verification in this session established:

- React Native unit test: 1 of 1 passed.
- Runtime `npm run typecheck`: passed.
- Runtime `npm run build`: passed.
- Application lint: failed with two errors and 149 warnings.
- Full native launch: blocked before build because the active developer directory is `/Library/Developer/CommandLineTools`; full Xcode, `xcodebuild`, and `simctl` are unavailable.
- Computer-use app discovery found no installed Xcode or Simulator application.
- Live CopilotKit/model flows could not be rerun because no supported model key was present.

Expected reproduction on a correctly provisioned Mac:

```sh
cd personal-finance-copilot
npm install
cd ios
bundle install
bundle exec pod install
cd ../runtime
npm install
cp .env.example .env
# Add OPENAI_API_KEY.
npm run dev

# In two additional terminals from the repository root:
npm start
npm run ios
maestro test .maestro/readme-demo.yaml
```

The committed reproducible interaction script is `.maestro/readme-demo.yaml`. It captures the empty chat, spend-by-category tool result, account result, transaction preparation, and actionable approval card.

### Finance image inventory

All images are 1206 by 2622 pixels.

| File | Caption | Alt text | Source | Status |
|---|---|---|---|---|
| `finance-dashboard-reference.png` | The mobile ledger dashboard presents synthetic balances, budgets, and recent activity before the agent is opened. | iPhone simulator showing the Personal Finance Copilot overview with three synthetic accounts, budget progress, and recent activity. | `docs/screenshots/dashboard.png` | Reference-only. Not publication-ready: a developer warning banner is visible at the bottom and should be recaptured cleanly. |
| `finance-chat-empty-reference.png` | The empty assistant state offers task-oriented starter prompts instead of an unstructured blank chat. | Empty Personal Finance Copilot assistant screen with starter prompt chips and bottom navigation. | `docs/screenshots/chat-empty.png` | Reference-only; strong recapture target. |
| `finance-read-tool-donut-reference.png` | A read-only frontend tool renders spending data as a controlled native donut chart instead of repeating figures as chat text. | iPhone simulator showing a spend-by-category donut chart with grocery, transport, and food totals inside the assistant conversation. | `docs/screenshots/chat-donut.png` | Reference-only; visually strong, but includes an active loading indicator and should be recaptured at a deliberate stable state if used in print. |
| `finance-approval-preparing-reference.png` | While tool arguments are still resolving, the inline transaction surface displays a distinct preparing state. | Finance assistant conversation showing a synthetic coffee expense and an inline transaction card in its preparing state. | `docs/screenshots/chat-hitl-card.png` | Reference-only; useful for a run-state sequence, not as a final standalone hero image. |
| `finance-approval-actionable-reference.png` | The write tool exposes the full proposed transaction with Add expense, Edit, and Cancel controls before data changes. | Finance assistant showing a synthetic Blue Bottle expense approval card with amount, category, account, date, and Add expense, Edit, and Cancel buttons. | `docs/screenshots/chat-hitl-resolved.png` | Reference-only; strongest current human-in-the-loop capture. The filename in the source repository says resolved, but the visible state is actionable and has not yet been approved. |

### Finance checksums

```text
a3dc778f3a79537669ab2db19609bc876bc1f6371ae94cadde8217383d2f1404  finance-approval-actionable-reference.png
5684d69b87d7e51bdfa4ad056489987b6a1462e7a5015e8a6b4a9ff44f288dcf  finance-approval-preparing-reference.png
9fb1c30bd830d86582809f53ba8ce6a5c952e5695b8d5eb8745835eee4e4ffed  finance-chat-empty-reference.png
3289df19a2de16fa4851518c2f4e097dedf41236dfdd790651ea862af8f0b139  finance-dashboard-reference.png
dc7a04800f021f8dcbb06be2cea1c2857c13ab0abee987539af0c3e52acc4eed  finance-read-tool-donut-reference.png
```

### Missing finance captures

- A clean dashboard without the developer warning banner.
- Read-tool result after all loading indicators settle.
- Approval card before interaction and a true post-approval confirmation with the updated account balance.
- Edit and Cancel branches.
- Receipt attachment, parsing, preview, and approval.
- Tool failure, retry, disconnect, and reconnect states.

## GTM Operations Workspace

### What actually ran

Clone inspected at `/tmp/GTM Operations Workspace`; Next.js app under `/tmp/GTM Operations Workspace/app`.

Installed with:

```sh
pnpm install --frozen-lockfile --ignore-scripts
```

Started with:

```sh
NEXT_PUBLIC_ENABLE_COPILOTKIT=1 pnpm exec next dev --turbopack -p 3400
```

Verified routes:

```text
GET http://localhost:3400/            -> 200
GET http://localhost:3400/api/health -> 200
{"status":"ok"}
```

Next.js reported ready in 424 ms. The first root request compiled successfully and returned 200. No source files were changed.

An initial command, `pnpm dev -- --port 3400`, failed because the extra `--` reached Next.js and was interpreted as a project directory. The corrected direct Next command above fixed the invocation without a code change. A sandboxed start then failed with `listen EPERM`; starting the same local server with the approved localhost permission succeeded.

### GTM visual-capture blocker

The in-app Browser workflow was initialized for `http://localhost:3400/`, but browser discovery returned an empty list and `getForUrl` reported `No browser is available`. Following the browser-control constraints, no alternate browser automation surface was substituted.

The app was therefore verified at the process and HTTP layers only. There are no GTM Operations Workspace PNGs in this folder, and the following desired states remain uncaptured:

- Main application UI at `/`.
- Open Copilot sidebar.
- Backend selector with Hermes, Claude, and OpenAI readiness.
- Hermes reachable/unreachable status.
- Default tool renderer showing a machine tool call and result.

### GTM environment requirements for a complete live capture

The deterministic application shell needs no live model key, but a real conversation requires one of:

- `ANTHROPIC_API_KEY` for the Claude service adapter.
- `OPENAI_API_KEY` for the OpenAI service adapter.
- The external Hermes AG-UI fork and adapter plus `AGENT_URL` for the Hermes path.

The repository's Hermes runbook states that upstream Hermes does not include the required `agui_adapter` module. A book-quality Hermes capture should use a pinned, distributable adapter revision rather than the runbook's machine-specific worktree path.

## Publication decision

Current folder status: **reference packet, not final publication art**.

The finance images are useful for chapter planning and layout prototypes, but should be recaptured from a fully provisioned simulator with a pinned model/runtime, stable completed states, no developer overlays, and metadata recorded at capture time. GTM Operations Workspace still requires a browser-capable capture environment.

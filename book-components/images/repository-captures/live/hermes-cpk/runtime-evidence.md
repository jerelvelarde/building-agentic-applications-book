---
title: Hermes CopilotKit Fresh Runtime Evidence
type: evidence
status: http-verified-no-screenshot
captured: 2026-07-14T22:17:57-07:00
---

# Hermes CopilotKit fresh runtime evidence

## Evidence identity

- Repository: `jerelvelarde/hermes-cpk`
- Pinned commit: `fc43491368f19248ca58e1409501cd28722d0f61`
- Checkout: `/tmp/hermes-cpk-audit`
- Data/actions: repository-provided synthetic Ledger data and read-only health probes only
- Screenshots created: **0**

The checkout contained one pre-existing untracked `expense-tracker-live/pnpm-workspace.yaml` (filesystem timestamp `2026-07-14T20:20:47-0700`, before this `22:17` capture). No tracked source was modified in this pass, and the untracked file was preserved.

## Browser boundary

The required in-app Browser backend was unavailable:

```text
Browser is not available: iab
agent.browsers.list() => []
```

No unrelated capture mechanism was substituted. The evidence below proves process and HTTP behavior, not rendered UI.

### Second GUI/Chrome attempt — still no screenshot

- Timestamp: `2026-07-14T22:28:10-07:00`
- Pinned commit reverified: `fc43491368f19248ca58e1409501cd28722d0f61`
- Planned commands and ports: `pnpm exec next dev --turbopack -p 3500` (live Ledger), `-p 3501` (reference Ledger), and `-p 3100` (Command Center); expected adapter `8000`
- Intended viewport: high-resolution desktop; no viewport was established because no controllable browser tab opened
- Listener boundary: the immediately preceding pinned GTM restart returned `listen EPERM`, and the required localhost escalation was rejected because the session had reached its usage limit; the three Hermes shells were therefore not restarted in this pass
- Chrome result: Google Chrome `150.0.7871.115` was installed and running; the native-host manifest was correct; the ChatGPT Chrome Extension was installed but disabled in the selected `Default` profile
- Visible limitations: no Ledger, offline reference state, Command Center, replay, flow, protocol, tool, or permission state was observed in a controllable GUI during this pass

Chrome troubleshooting explicitly forbids fallback scripting or another GUI-control surface after this failure. No adapter, model, financial write, or machine tool call was attempted, and all earlier evidence was preserved.

## Run commands and ports

Each pinned source-present shell was started with approved localhost permission after the managed sandbox rejected listener creation:

```sh
cd /tmp/hermes-cpk-audit/expense-tracker-live
pnpm exec next dev --turbopack -p 3500

cd /tmp/hermes-cpk-audit/expense-tracker
pnpm exec next dev --turbopack -p 3501

cd /tmp/hermes-cpk-audit/command-center
pnpm exec next dev --turbopack -p 3100
```

```text
expense-tracker-live: Next.js 15.5.4, ready in 784ms, localhost:3500
expense-tracker:      Next.js 15.5.4, ready in 791ms, localhost:3501
command-center:       Next.js 15.5.4, ready in 804ms, localhost:3100
expected adapter:     connection refused, localhost:8000
```

## Fresh route evidence

### Live Ledger shell

```text
GET http://127.0.0.1:3500/                     -> 200, title "Financial Ledger"
GET http://127.0.0.1:3500/api/health            -> 200
GET http://127.0.0.1:3500/api/copilotkit/info   -> 200
```

```json
{ "ok": true, "app": "expense-tracker-live" }
```

CopilotKit registration information included:

```json
{
  "version": "1.62.3",
  "agents": { "default": { "name": "default" } },
  "mode": "sse",
  "telemetryDisabled": false
}
```

This proves a registered runtime surface, not a reachable Hermes agent. The development log also emitted `shiki`/`shiki/wasm` external-package warnings and CopilotKit's anonymous-telemetry notice; both should be resolved or explicitly configured before publication capture.

### Reference Ledger explicit failure state

```text
GET http://127.0.0.1:3501/               -> 200, title "Ledger — expense tracker"
GET http://127.0.0.1:3501/api/copilotkit  -> 200
```

```json
{
  "status": "ok",
  "agent_url": "http://localhost:8000",
  "agent": "unreachable (fetch failed)"
}
```

### Command Center shell

```text
GET http://127.0.0.1:3100/            -> 200
title                                 -> "Hermes ⇄ CopilotKit · Command Center"
GET http://127.0.0.1:8000/health      -> connection refused
GET http://127.0.0.1:8000/runs        -> connection refused
```

The Command Center page existed and rendered server-side, but Replay, Flow, Protocol, and liveness data could not populate without the trace backend.

## Adapter start boundary

The repository launcher was invoked without adding credentials or changing source:

```sh
cd /tmp/hermes-cpk-audit
./run-adapter.sh expense-tracker-live
```

```text
!! No LLM key set. Copy adapter.env.example -> adapter.env and fill it in.
```

The external `hermes/` checkout and its `.venv` were absent. No model credential, adapter substitute, or permissive machine execution was introduced.

## Runtime and safety limits

- No Hermes model run, filesystem write, terminal command, diff, Undo, PDF event, replay, flow, or protocol trace was produced.
- No financial mutation occurred.
- The capture did not enable `HERMES_YOLO=1` or weaken any control.
- All three UI servers were stopped after the probes; port `8000` remained unavailable throughout.

## Evidence classification

**R for the three source UI shells, their named HTTP routes, and the adapter-unreachable failure; not R for visual state or Hermes execution.** The explicit offline response is a strong future figure target once the in-app browser is available.

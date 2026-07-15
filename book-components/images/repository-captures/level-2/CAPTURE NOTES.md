# Hermes + CopilotKit Level 2 Capture Notes

## Evidence identity

- Repository: `https://github.com/jerelvelarde/hermes-cpk`
- Commit: `fc43491368f19248ca58e1409501cd28722d0f61`
- Branch at capture time: `main`
- Capture attempt date: 2026-07-14 (America/Los_Angeles)
- Source checkout used: authenticated clone at `/tmp/hermes-cpk-audit`
- Data policy: only the repository's synthetic Ledger seed data was served. No personal financial data, live credentials, or secrets were introduced.

## Outcome

The three source-present Next.js UIs were run and queried successfully. The external Hermes runtime was not available and was not simulated. No browser screenshots were produced because the required in-app Browser runtime reported zero available browser backends.

This folder therefore contains runtime notes only. It must not be represented as a completed screenshot set.

## Runtime proof classification

| Surface | Classification | Verified result |
|---|---|---|
| `expense-tracker-live` page | Source-present, HTTP-verified | Dev server reached ready state on port 3000; `GET /` returned HTTP 200 and title `Financial Ledger`. |
| `expense-tracker-live` health | Source-present, HTTP-verified | `GET /api/health` returned HTTP 200 with `{ "ok": true, "app": "expense-tracker-live" }`. |
| CopilotKit runtime information | Source-present, HTTP-verified | `GET /api/copilotkit/info` returned HTTP 200, CopilotKit runtime `1.62.3`, and a registered `default` agent. This proves registration only, not Hermes reachability. |
| `expense-tracker` reference page | Source-present, HTTP-verified | Dev server reached ready state on port 3000; `GET /` returned HTTP 200 and title `Ledger — expense tracker`. |
| `expense-tracker` adapter status | Source-present, offline state verified | `GET /api/copilotkit` returned HTTP 200 with `agent: "unreachable (fetch failed)"` for `http://localhost:8000`. |
| Command Center shell | Source-present, HTTP-verified | Dev server reached ready state on port 3100; `GET /` returned HTTP 200 and title `Hermes ⇄ CopilotKit · Command Center`. |
| Hermes adapter | Unavailable, failure verified | Documented launcher stopped because no LLM key was configured. The external `hermes/` checkout and `hermes/.venv/bin/python` were also absent. Port 8000 refused connections. |
| Live Hermes tool calls | Not verified | No external adapter or model credentials were available. |
| Diff and Undo interaction | Source-only | Components compile and production-build, but no live Hermes `write_file` or `patch` event was produced. |
| PDF tool rendering | Source-only | The PDF component and route compile and production-build, but no live Hermes PDF tool event was produced. |
| Command Center replay, flow, and protocol data | UI source-only | The shell ran, but the external adapter endpoints `/runs`, `/trace/stream`, and deep `/health` were unavailable. |

## Commands and ports

### Documented adapter attempt

```sh
cd /tmp/hermes-cpk-audit
./run-adapter.sh expense-tracker-live
```

Observed output:

```text
!! No LLM key set. Copy adapter.env.example -> adapter.env and fill it in.
```

Follow-up evidence:

```text
adapter.env: absent
hermes/: absent
hermes/.venv/bin/python: absent
http://127.0.0.1:8000/health: connection refused
```

No credential was created and no alternative runtime was substituted.

### Live Ledger UI

```sh
cd /tmp/hermes-cpk-audit/expense-tracker-live
pnpm dev
```

- Port: `3000`
- Routes verified: `/`, `/api/health`, `/api/copilotkit/info`
- `/api/copilotkit/info` reported `telemetryDisabled: false`; this should be reviewed before publication/runtime distribution.

### Reference Ledger UI

The live Ledger process was stopped before starting the reference app because both scripts bind port 3000.

```sh
cd /tmp/hermes-cpk-audit/expense-tracker
pnpm dev
```

- Port: `3000`
- Routes verified: `/`, `/api/copilotkit`
- The API returned the clear adapter-offline state `agent: "unreachable (fetch failed)"`.

### Command Center

```sh
cd /tmp/hermes-cpk-audit/command-center
pnpm dev
```

- Port: `3100`
- Route verified: `/`
- The UI shell ran concurrently with each Ledger app.
- Replay, Flow, and Protocol views were not classified as runtime-proven because their event backend was absent.

## Screenshot manifest

The following filenames are reserved capture targets. **None of these PNG files was created during this run.** Their captions and alt text are recorded so a later browser-enabled capture can reproduce the intended set without changing the evidence standard.

| Intended filename | Status | Caption | Alt text | Readiness |
|---|---|---|---|---|
| `ledger-live-overview.png` | Blocked: no browser backend | Financial Ledger running from the pinned `hermes-cpk` source with synthetic July 2026 transactions. | Financial Ledger dashboard with spending summary, budget progress, category chart, and synthetic recent expenses. | Capture again; not publication-ready. |
| `ledger-live-copilot-pane-offline.png` | Blocked: no browser backend | The CopilotKit pane is source-present, while the external Hermes adapter remains unavailable. | Financial Ledger beside its docked CopilotKit chat pane in an adapter-offline run. | Capture again; reference-only until the offline state is visibly confirmed. |
| `ledger-live-tool-renderer.png` | Unreachable without verified Hermes run | Hermes machine-side tool events rendered inside the CopilotKit pane. | CopilotKit chat showing a Hermes filesystem or terminal tool call with its path, status, and result. | Requires pinned adapter and synthetic live run. |
| `ledger-live-diff-card.png` | Unreachable without verified Hermes write event | A Hermes file edit shown as an application-owned diff with best-effort Undo. | Red and green file diff card for a Hermes patch, including file location and Undo control. | Requires pinned adapter and synthetic live run. |
| `ledger-live-pdf-viewer.png` | Unreachable without verified Hermes PDF event | A PDF produced by the machine agent rendered inline in the application UI. | CopilotKit tool result containing an inline PDF preview with open-in-tab and modal controls. | Requires pinned adapter and synthetic live run. |
| `ledger-reference-agent-unreachable.png` | Blocked: no browser backend | The reference Ledger API reports the Hermes adapter at port 8000 as unreachable. | Ledger application with a clear indication that its configured Hermes adapter cannot be reached. | Capture again; suitable as an explicit failure-state figure. |
| `command-center-overview-offline.png` | Blocked: no browser backend | The Command Center shell running without its external Hermes trace backend. | Hermes and CopilotKit Command Center overview with unavailable service state. | Capture again; suitable only if the offline pills are visibly verified. |
| `command-center-replay.png` | Unreachable without trace backend | A verified Hermes conversation reconstructed from persisted AG-UI events. | Command Center Replay view showing user input, assistant text, and machine tool calls. | Requires external trace backend and a synthetic run. |
| `command-center-flow.png` | Unreachable without trace backend | A verified run animated across App, CopilotKit Runtime, AG-UI, and Hermes. | Command Center Flow view showing events moving across the four system boundaries. | Requires external trace backend and a synthetic run. |
| `command-center-protocol.png` | Unreachable without trace backend | Raw AG-UI lifecycle, message, and tool events from a verified Hermes run. | Command Center Protocol view with an AG-UI event waterfall and selected JSON payload. | Requires external trace backend and a synthetic run. |

## Browser capture blocker

The required in-app Browser skill was loaded before browser interaction. Browser setup completed, but discovery returned:

```text
agent.browsers.list() => []
```

The Browser troubleshooting instructions require reporting an unavailable backend rather than substituting a different browser-control surface. No Playwright, Chrome, Computer Use, static HTML renderer, or generated mock was used as a workaround.

## Failures and root causes

### Local socket bind failed inside the default sandbox

Observed error for both ports:

```text
Error: listen EPERM: operation not permitted 0.0.0.0:3000
Error: listen EPERM: operation not permitted 0.0.0.0:3100
```

Root cause: the managed sandbox denied listening sockets. Verification: the unchanged commands reached Next.js `Ready` when run with approved local-network escalation. This was an environment restriction, not an application defect.

### Default-sandbox curl could not reach escalated services

Root cause: the sandboxed probe could not reach services bound outside that sandbox. The same localhost requests returned HTTP 200 when queried with approved escalation.

### Hermes adapter did not start

Immediate root cause: `run-adapter.sh` intentionally exits when no LLM key is present.

Additional blocking dependency: the script expects `hermes/.venv/bin/python`, but the external `hermes/` checkout is gitignored and absent from commit `fc434913`.

No source change was made because the task prohibited inventing or bypassing the missing runtime and credentials.

### Live Ledger development warnings

The first `GET /` compiled and returned HTTP 200, but Next.js emitted warnings that `shiki` and `shiki/wasm` could not be resolved as external packages from the project directory. The previously run production build completed successfully. Treat this as a reproducibility warning to resolve before publication capture, not as proof of a page failure.

## Publication assessment

### Publication-ready

- No screenshot from this attempt.
- The HTTP and command evidence in this note is suitable for internal verification, not as a book figure.

### Reference-only

- Ledger and Command Center UI source and successful HTTP responses.
- CopilotKit runtime registration metadata.
- The explicit adapter-unreachable API response.
- Source-present Diff, Undo, PDF, Replay, Flow, and Protocol components.

### Required before publication capture

1. Make an in-app browser backend available.
2. Pin and restore the exact external Hermes checkout and adapter commit.
3. Use a synthetic-only credential and task.
4. Capture an explicit permission-denied or approval state; do not run the book capture with `HERMES_YOLO=1`.
5. Verify trace storage redaction before capturing Replay or Protocol views.
6. Resolve the development-time `shiki` warnings.
7. Disable or explicitly document CopilotKit telemetry for the capture environment.
8. Record each PNG's viewport, timestamp, route, prompt, and exact runtime commit.

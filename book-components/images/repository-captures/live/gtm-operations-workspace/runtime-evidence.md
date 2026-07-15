---
title: GTM Operations Workspace Fresh Runtime Evidence
type: evidence
status: http-verified-no-screenshot
captured: 2026-07-14T22:17:57-07:00
---

# GTM Operations Workspace fresh runtime evidence

## Evidence identity

- Repository: `GTM Operations Workspace`
- Pinned commit: `private revision omitted`
- Checkout: `/tmp/GTM Operations Workspace`
- Checkout state before capture: clean (`git status --short` returned no entries)
- Data/actions: read-only shell and health probes; no drafts, integrations, posts, or external writes
- Screenshots created: **0**

## Browser boundary

The required in-app Browser runtime initialized, but the requested backend was absent:

```text
Browser is not available: iab
agent.browsers.list() => []
```

Per the Browser skill, no Chrome, standalone Playwright, Computer Use, generated mock, or static-page renderer was substituted. This file is fresh HTTP/process evidence, not visual evidence.

### Second GUI/Chrome attempt — still no screenshot

- Timestamp: `2026-07-14T22:28:10-07:00`
- Pinned commit reverified: `private revision omitted`
- Requested command: `NEXT_PUBLIC_ENABLE_COPILOTKIT=1 pnpm exec next dev --turbopack -p 3400`
- Requested port: `3400`
- Intended viewport: high-resolution desktop; no viewport was established because no controllable browser tab opened
- Listener result: managed sandbox returned `listen EPERM`; the required localhost escalation was rejected because the session had reached its usage limit
- Chrome result: Google Chrome `150.0.7871.115` was installed and running; the native-host manifest was correct; the ChatGPT Chrome Extension was installed but disabled in the selected `Default` profile
- Visible limitations: none of the GTM shell, sidebar, backend selector, or explicit Hermes-offline page state was observed in a controllable GUI during this pass

Chrome troubleshooting explicitly forbids falling back to scripting or another GUI-control mechanism after this extension failure. No substitute rendering was created, and all earlier evidence was preserved.

## Run command and port

The default sandbox correctly rejected the local listener with `listen EPERM`. The unchanged pinned app was then started with approved localhost permission:

```sh
cd /tmp/GTM Operations Workspace/app
NEXT_PUBLIC_ENABLE_COPILOTKIT=1 pnpm exec next dev --turbopack -p 3400
```

```text
Next.js 16.1.7 (Turbopack)
Local: http://localhost:3400
Ready in 1110ms
Warning: the middleware file convention is deprecated; Next.js recommends proxy.
```

## Fresh route evidence

```text
GET http://127.0.0.1:3400/                         -> 200 text/html
GET http://127.0.0.1:3400/api/health               -> 200 {"status":"ok"}
GET http://127.0.0.1:3400/api/ai/backends           -> 200
GET http://127.0.0.1:3400/api/settings/env          -> 200
GET http://127.0.0.1:3400/api/copilotkit?health=1   -> 200
```

Backend registry result:

```json
{
  "backends": [
    { "id": "hermes", "label": "Hermes Agent", "readiness": "ready" },
    { "id": "claude", "label": "Claude", "readiness": "not-configured" },
    { "id": "openai", "label": "OpenAI", "readiness": "not-configured" }
  ],
  "defaultBackend": "hermes"
}
```

The UI's environment-derived `ready` label did **not** prove runtime reachability. The bounded health probe returned:

```json
{
  "status": "ok",
  "backend": "hermes",
  "agent": "unreachable (fetch failed)",
  "agent_url": "http://localhost:8000"
}
```

Server request log:

```text
GET / 200
GET /api/health 200
GET /api/ai/backends 200
GET /api/settings/env 200
GET /api/copilotkit?health=1 200
```

## Runtime and credential limits

- `NEXT_PUBLIC_ENABLE_COPILOTKIT=1` mounted the UI and made Hermes configuration-ready.
- `AGENT_URL` was absent, so the code used its default `http://localhost:8000`.
- `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` were absent.
- The external Hermes AG-UI adapter/runtime was not available and was not simulated.
- No model conversation or machine tool call was attempted.
- The server was stopped after the probes.

## Evidence classification

**R for shell and HTTP health only; not R for visual state, model behavior, Hermes execution, or tool rendering.** A new browser-enabled pass should capture the app shell, AI pane, backend selector, and explicit adapter-unreachable state from this same pinned revision.

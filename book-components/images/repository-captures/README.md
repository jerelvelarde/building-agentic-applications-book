---
title: Agentic Applications 2026 — Repository Capture Ledger
type: evidence
status: partial
created: 2026-07-15
updated: 2026-07-15
---

# Repository Capture Ledger

> **Zero new live screenshots were produced.** On 2026-07-15, the pinned Hermes reference Ledger and Command Center shells both returned HTTP 200, but the browser runtime reported no available browser (`agent.browsers.list() => []`). The external adapter was absent, so no model, tool, file, diff, PDF, or approval flow ran. Ten source-faithful schematics now replace unresolved manuscript screenshot notes; each is visibly labeled as a schematic and is not runtime proof. The five finance images and six OpenTag images remain repository/demo-derived **reference-only** assets.

Detailed notes: [Level 1](level-1/CAPTURE%20NOTES.md) · [Level 2](level-2/CAPTURE%20NOTES.md) · [Level 3](level-3/CAPTURE%20NOTES.md) · [Final Book Lane B evidence](FINAL%20BOOK%20LANE%20B%20EVIDENCE.md) · Fresh evidence: [GTM Operations Workspace](live/gtm-operations-workspace/runtime-evidence.md) · [Hermes CPK](live/hermes-cpk/runtime-evidence.md) · [Channels decision](live/copilotkit-channels/runtime-evidence.md)

## Second GUI/Chrome capture attempt

Attempt timestamp: `2026-07-14T22:28:10-07:00`.

| Repository | Commit | Requested command / port | Intended viewport | Result and visible limitations |
|---|---|---|---|---|
| `GTM Operations Workspace` | `private revision omitted` | `NEXT_PUBLIC_ENABLE_COPILOTKIT=1 pnpm exec next dev --turbopack -p 3400` / `3400` | High-resolution desktop; not established because no controllable tab opened | Managed sandbox returned `listen EPERM`; the required localhost escalation was then rejected because the session had reached its usage limit. Chrome 150 was running, but the ChatGPT Chrome Extension was installed and disabled in the selected `Default` profile. No new page state was observed or captured. |
| `jerelvelarde/hermes-cpk` | `fc43491368f19248ca58e1409501cd28722d0f61` | `pnpm exec next dev --turbopack -p 3500`, `3501`, and `3100`; expected adapter `8000` | High-resolution desktop; not established because no controllable tab opened | The GTM listener denial established that the same required localhost permission path was unavailable for this pass, so the Hermes shells were not restarted. Chrome control had the same disabled-extension blocker. No adapter, model, tool, or financial action was attempted. |

Chrome diagnostics were read-only: Chrome was installed and running; the native-host manifest existed and allowed the expected extension origin; the selected profile reported the extension as installed but `enabled: false` with disable reason `1`. Chrome troubleshooting forbids substituting automation scripts or another GUI-control surface after this failure. All prior evidence and reference assets were left intact.

## Master status

| Repository | Pinned SHA | Actual run result | HTTP/build/install proof | Screenshots | Proof class | Primary blocker | Next recapture action |
|---|---|---|---|---:|---|---|---|
| `jerelvelarde/personal-finance-copilot` | `d8760064c626712a8fa15c192a8c4bc69bb24055` | React Native test passed; runtime typecheck and build passed. Native launch and live model flows did not run. | 1/1 Jest test passed; runtime `typecheck` and `build` passed; app lint failed with 2 errors and 149 warnings. | 5 | Repo reference-only | Full Xcode/Simulator and model credentials unavailable; browser backend unavailable. | Provision Xcode/Simulator and a pinned synthetic runtime, fix lint, run Maestro, and recapture stable mobile states without developer overlays. |
| `GTM Operations Workspace` | `private revision omitted` | Next.js/PWA shell reran on `:3400`; no visual capture or live model/Hermes conversation. | Fresh `GET /`, `/api/health`, `/api/ai/backends`, and `/api/settings/env` returned 200. Hermes was configuration-`ready` but its health probe explicitly returned `agent: unreachable (fetch failed)`. | 0 | HTTP/process runtime-verified | In-app browser absent; second-pass Chrome extension disabled; second-pass localhost approval rejected by session usage limit; model credentials and distributable Hermes adapter absent. | Enable the ChatGPT Chrome Extension, restore localhost approval capacity, re-run with a controllable browser, then capture shell, sidebar, backend readiness, explicit Hermes-offline state, and—only with a pinned runtime—tool rendering. |
| `jerelvelarde/hermes-cpk` | `fc43491368f19248ca58e1409501cd28722d0f61` | All three source UIs reran: live Ledger on `:3500`, reference Ledger on `:3501`, and Command Center on `:3100`. External Hermes runtime and live tool events did not run. | Fresh page, title, health/runtime-info, and offline-status probes returned 200. Port `8000` refused connections; the reference Ledger returned `agent: unreachable (fetch failed)`. | 0 | HTTP/process runtime-verified | In-app browser absent; second-pass Chrome extension disabled; second-pass localhost approval unavailable; external `/hermes/` checkout, adapter venv, and model key unavailable. | Enable the ChatGPT Chrome Extension, restore localhost approval capacity, pin the external runtime, keep permissive execution disabled, use synthetic credentials, then capture offline/online, permission, tool, diff/undo, PDF, replay, flow, and protocol states. |
| `CopilotKit/CopilotKit` Channels | `855446e1abc8f29756dc5e539e5e50a90321ac2d` | Filtered Channels workspace had installed earlier; the Slack example was correctly not started because it has no credential-free conversation preview. | Fresh credential-boundary check: `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, `AGENT_URL`, and `OPENAI_API_KEY` were absent. | 0 | No new runtime proof | Browser backend, model key, agent URL, and platform credentials unavailable. | Use a dedicated synthetic Slack or Teams workspace, then capture health, streaming, rich UI, approval, and result. |
| `CopilotKit/OpenTag` | `df93bc0dccd0afc8eb7bb02206ffbe2ef7922322` | Source inspected; no local OpenTag platform session ran. | No runtime proof; execution requires `AGENT_URL`, platform tokens, and a model-backed runtime. Main also uses the earlier `@copilotkit/bot*` topology. | 6 | Repo demo reference-only | Browser backend and required credentials/runtime unavailable; reference frames include real UI/person/workspace details. | Recreate the six beats in a synthetic workspace on current Channels packages, then recapture and complete privacy/trademark review. |

## Reference image inventory

### Source-faithful schematics — ten SVGs

The `schematics/` directory contains the Chapter 4, 7, 9, 10, 15, and 18 visual specifications listed in the figure manifest. They are editorial explanations with explicit evidence limits, not screenshots.

### Finance — five repository-derived references

- [Dashboard](level-1/finance-dashboard-reference.png)
- [Empty assistant](level-1/finance-chat-empty-reference.png)
- [Read-tool donut](level-1/finance-read-tool-donut-reference.png)
- [Approval preparing](level-1/finance-approval-preparing-reference.png)
- [Approval actionable](level-1/finance-approval-actionable-reference.png)

### OpenTag — six demo-derived references

- [GitHub issue triage](level-3/opentag-reference-01-github-issue-triage.png)
- [Issues table](level-3/opentag-reference-02-issues-table.png)
- [Chart response](level-3/opentag-reference-03-chart-response.png)
- [Inline chart preview](level-3/opentag-reference-04-inline-chart-preview.png)
- [Linear draft progress](level-3/opentag-reference-05-linear-draft-progress.png)
- [Human-in-the-loop approved](level-3/opentag-reference-06-hitl-approved.png)

## Publication gate

No image in this ledger is publication-ready proof. A final figure must be a new live capture tied to the pinned source and runtime revision, with synthetic data, reproducible commands, viewport and timestamp metadata, stable UI state, redaction review, and an explicit evidence classification.

# Level 3 repository capture notes

Captured on 2026-07-14 for *Builder's Guide to Agentic Applications 2026*.

## Scope and pinned revisions

- CopilotKit Channels: `CopilotKit/CopilotKit@855446e1abc8f29756dc5e539e5e50a90321ac2d`
  - Inspected and installed from `/tmp/cpk-channels-audit`.
  - Priority examples: `examples/slack` and `examples/teams`.
- OpenTag: `CopilotKit/OpenTag@df93bc0dccd0afc8eb7bb02206ffbe2ef7922322`
  - Inspected from `/tmp/opentag-audit`.
  - The six images in this folder are frames from the demo video linked in the OpenTag README, not a newly executed local session.

## Run status

| Target | Furthest honest state | Proof classification | Publication status |
| --- | --- | --- | --- |
| CopilotKit filtered workspace install | Successful: 8 of 42 projects, 1,243 packages, pinned lockfile | Newly run terminal verification; no screenshot | Suitable to cite in working notes, not a book figure |
| Teams example | Source and dependencies installed. No agent session executed because current example exits without `OPENAI_API_KEY`; real Teams additionally needs Microsoft bot credentials. | Credential-blocked; source inspection only | No publication image captured |
| Teams M365 Agents Playground | The package is installed and the repository documents a credential-free Microsoft platform playground at `http://localhost:56150`, but the bot still requires a model key. The Playground was not presented as end-to-end proof. | Not captured | Do not claim as run |
| Slack example | Source and dependencies installed. No platform session executed because at least one adapter token set is required; the agent runtime also needs a model key to answer. | Credential-blocked; source inspection only | No publication image captured |
| OpenTag main | Current source inspected. No local platform session executed: it requires `AGENT_URL`, platform tokens, and a model-backed agent runtime. Main still imports the earlier `@copilotkit/bot*` package names. | Credential/package-topology blocked | Use only README-sourced reference frames below |

No secrets were read, created, logged, or embedded in these captures.

## Commands and observed results

```sh
cd /tmp/cpk-channels-audit
git rev-parse HEAD
# 855446e1abc8f29756dc5e539e5e50a90321ac2d

pnpm install --filter teams-example... --filter slack-example... --frozen-lockfile --reporter=append-only
# Success: Scope 8 of 42 workspace projects; 1,243 packages; pnpm 10.33.4
```

The host's direct pnpm executable reports 11.1.2 outside the repository, but pnpm honored the repository's `packageManager` declaration and ran the install with 10.33.4.

A first sandboxed install produced no progress because registry access was restricted. Re-running with explicitly approved network access completed in about 11 seconds. This was an environment restriction, not a repository failure.

Direct `tsc` checks were inconclusive because the filtered install did not build the workspace packages first. Imports such as `@copilotkit/channels-ui`, `@copilotkit/channels-teams`, and `@copilotkit/runtime/v2` resolve through package build outputs, which were absent. Do not describe this as a source typecheck regression; the documented example build runs Nx over those packages first.

Attempting the TypeScript entrypoints inside the restricted sandbox hit `tsx` IPC socket denial (`listen EPERM` on a `tsx-501/*.pipe`) before application startup. That is a sandbox process-IPC restriction. An unsandboxed probe did not yield a stable, attributable UI capture and was terminated rather than misrepresented.

Relevant documented routes:

- Teams bot webhook: `http://localhost:3978/api/messages`
- Teams liveness: `http://localhost:3978/healthz`
- Teams in-process agent runtime: `127.0.0.1:8200`
- Microsoft 365 Agents Playground: `http://localhost:56150`
- Slack/OpenTag default AG-UI target: `http://localhost:8200/api/copilotkit/agent/triage/run`

## Credential boundaries

### Teams example

- Local M365 Agents Playground itself needs no Microsoft credentials.
- The current in-process `BuiltInAgent` exits without `OPENAI_API_KEY`.
- A real Teams deployment also needs a Microsoft/Entra client ID, client secret, tenant ID, Azure Bot resource, public messaging endpoint, and uploaded app package.
- Channel/group file access may require Microsoft Graph permissions and consent; a personal 1:1 upload follows a different path.

### Slack example

- Native Slack: `SLACK_BOT_TOKEN` plus `SLACK_APP_TOKEN`.
- Alternative adapters have their own required token/app-ID sets.
- Agent bridge: `AGENT_URL`.
- Built-in runtime: `OPENAI_API_KEY` (or the configured model provider credential).
- Linear and Notion demonstrations require their corresponding MCP credentials; writes use a confirm-before-write gate.

### OpenTag

- `AGENT_URL` plus at least one platform credential set.
- A model provider credential for the agent runtime.
- Optional Linear/Notion credentials for the demo's external tools.

## Reference-only OpenTag frames

Source video: OpenTag README user-attachment `a74fa1cb-add0-463e-a23c-aa09b95d5135`.

Extraction command:

```sh
ffmpeg -y -i /tmp/opentag-demo.mp4 -vf 'fps=1/8' -frames:v 7 /tmp/opentag-shot-%02d.png
```

Every file below is **reference-only**. It proves what the repository's published demo depicts, not what was newly run in this capture session.

1. `opentag-reference-01-github-issue-triage.png`
   - Caption: “OpenTag returns a structured GitHub issue-triage status card after being mentioned in Slack.”
   - Alt text: “Slack thread with an OpenTag agent response summarizing GitHub issue triage in a structured status card.”
2. `opentag-reference-02-issues-table.png`
   - Caption: “A channel-native issue table appears while OpenTag continues evaluating the request.”
   - Alt text: “Slack conversation showing a rich table of GitHub issues and an agent progress message.”
3. `opentag-reference-03-chart-response.png`
   - Caption: “OpenTag follows up with a table and chart rather than flattening structured results into prose.”
   - Alt text: “Slack agent response containing an issue table and an embedded chart preview.”
4. `opentag-reference-04-inline-chart-preview.png`
   - Caption: “The generated chart can be opened as a larger artifact from the channel conversation.”
   - Alt text: “Expanded chart artifact opened from an OpenTag Slack response.”
5. `opentag-reference-05-linear-draft-progress.png`
   - Caption: “The agent gathers context before drafting a Linear ticket.”
   - Alt text: “Slack thread where a user asks OpenTag to draft a Linear ticket and the agent reports that it is gathering information.”
6. `opentag-reference-06-hitl-approved.png`
   - Caption: “A human-in-the-loop card records approval before the agent performs the write.”
   - Alt text: “Slack approval card showing that a proposed Linear write was approved and is being executed.”

## Publication, privacy, and trademark review

- These frames contain Slack UI, CopilotKit/OpenTag branding, a real person's display name/avatar, and issue/workspace data. They are not publication-ready as-is.
- Before book publication, obtain permission or recapture in a controlled demo workspace; otherwise redact the person's name/avatar and any organization-, repository-, issue-, or workspace-specific identifiers.
- Preserve a source credit to the OpenTag repository/demo. Do not imply Slack, Microsoft Teams, Discord, GitHub, Linear, Notion, Claude, or Anthropic endorsement.
- Product and company names/logos remain their respective owners' trademarks. Use them editorially and follow the publisher's trademark guidance.
- Preferred final-book path: recreate the same six beats in a synthetic CopilotKit demo workspace with seeded fake issues and users, then label those images as newly captured walkthrough evidence.

## Recommended recapture checklist

1. Use a dedicated test Slack or Teams workspace and synthetic identities/data.
2. Pin the exact repository SHA and record the model/provider version.
3. Capture startup health, first useful streamed output, a channel-native rich component, a tool/progress state, the approval boundary, and the post-approval result.
4. Record whether the agent is CopilotKit Intelligence-managed or self-hosted, plus the identity and policy boundary under which it acts.
5. Crop or redact tokens, tenant IDs, channel IDs, private URLs, names, avatars, and customer data before export.

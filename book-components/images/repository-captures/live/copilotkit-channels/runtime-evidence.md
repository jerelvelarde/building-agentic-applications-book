---
title: CopilotKit Channels Fresh Capture Decision
type: evidence
status: credential-blocked-no-preview
captured: 2026-07-14T22:17:57-07:00
---

# CopilotKit Channels fresh capture decision

## Evidence identity

- Repository: `CopilotKit/CopilotKit`
- Pinned commit: `855446e1abc8f29756dc5e539e5e50a90321ac2d`
- Checkout: `/tmp/cpk-channels-audit`
- Priority target: `examples/slack`
- Screenshots created: **0**

## Why no local preview was started

The pinned Slack example is a channel adapter process, not a credential-free browser preview. Its current run path needs a platform connection and an AG-UI/model runtime. This capture environment reported only presence/absence, never secret values:

```text
SLACK_BOT_TOKEN=absent
SLACK_APP_TOKEN=absent
AGENT_URL=absent
OPENAI_API_KEY=absent
```

The README's chart/diagram renderer is a tool implementation, not a substitute Slack conversation surface. Running it alone would not prove a channel-agent session. No Slack, Teams, Discord, Telegram, or WhatsApp post was attempted.

The in-app Browser backend was also unavailable (`Browser is not available: iab`; `agent.browsers.list() => []`). Even with a browser, the example would still require a synthetic platform workspace and credentials for an end-to-end capture.

## Evidence classification

**No new runtime or visual proof.** Retain the earlier filtered-install evidence only. The next honest capture needs a dedicated synthetic workspace, non-production credentials, a pinned runtime/model, and an explicit approval/result flow.

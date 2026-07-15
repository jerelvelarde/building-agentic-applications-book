# Reference projects used in the book

These are pointers, not Git submodules. A normal clone of this book remains small, while every implementation claim can still resolve to an immutable source revision.

The pins below were rechecked on July 15, 2026. A pinned source shows what was present at that revision; it does not by itself prove the project was runtime-verified or production-ready.

## Personal Finance Copilot

- **Level:** 1 — application agent
- **Use in the book:** canonical mobile example for frontend tools, inline native renderers, human-in-the-loop writes, and receipt parsing.
- **Pinned source:** [`jerelvelarde/personal-finance-copilot@d876006`](https://github.com/jerelvelarde/personal-finance-copilot/tree/d8760064c626712a8fa15c192a8c4bc69bb24055)
- **Companion concepts:** [`companion/src/level-1/`](../companion/src/level-1/) and [`ledger_graph.py`](../companion/python/src/book_agent/ledger_graph.py)

## Hermes CPK

- **Level:** 2, with a Level 1 supervision UI
- **Use in the book:** CopilotKit-to-AG-UI-to-Hermes seam and visible machine-agent baseline.
- **Pinned source:** [`jerelvelarde/hermes-cpk@fc43491`](https://github.com/jerelvelarde/hermes-cpk/tree/fc43491368f19248ca58e1409501cd28722d0f61)
- **Companion concepts:** [`companion/src/level-2/`](../companion/src/level-2/)
- **Important boundary:** the book does not treat the demo as proof of production sandboxing, authorization, approvals, or rollback.

## CopilotKit Channels

- **Level:** 3 — organizational agent infrastructure
- **Use in the book:** channel-neutral core plus Slack, Discord, and Teams adapter architecture.
- **Pinned source:** [`CopilotKit/CopilotKit@855446e/packages/channels`](https://github.com/CopilotKit/CopilotKit/tree/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels)
- **Companion concepts:** [`companion/src/level-3/`](../companion/src/level-3/)

## OpenTag

- **Level:** 3 — organizational agent case study
- **Use in the book:** self-hosted Slack agent, rich channel-native results, tool integrations, and a human approval interaction.
- **Pinned source:** [`CopilotKit/OpenTag@df93bc0`](https://github.com/CopilotKit/OpenTag/tree/df93bc0dccd0afc8eb7bb02206ffbe2ef7922322)
- **Important boundary:** package names and managed-service availability in this historical pin may differ from current CopilotKit releases. The book separates the channel adapter from the additional governance required for an organizational actor.

## Anonymized operations workspace

- **Levels:** 1 and 2
- **Use in the book:** a private web/PWA case study that selects hosted models or Hermes behind one CopilotKit interface and renders machine activity in a frontend pane.
- **Link:** intentionally omitted because the repository is private.
- **Publication treatment:** screenshots may appear under an anonymized product name; private repository names, locators, and credentials are not published.

## Evidence and excerpt provenance

The book's detailed claim status, source locators, and excerpt permissions live in [`book-components/materials/`](../book-components/materials/). Repository screenshots are references unless their capture notes explicitly establish runtime evidence.

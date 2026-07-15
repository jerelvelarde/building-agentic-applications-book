---
title: "Level 3 evidence packet — organizational agents"
book: "The Builder's Guide to Agentic Applications 2026"
status: "research complete; chapter drafting not started"
owner: "Level 3 research"
accessed: "2026-07-14"
source_policy: "official documentation and official repositories only"
chapters:
  - 17
  - 18
  - 19
  - 20
  - 21
  - 22
---

# Level 3: Organizational Agents — Evidence Packet

This packet is the factual and architectural source layer for Part IV of *The Builder's Guide to Agentic Applications 2026*. It is not manuscript prose. It records what the current products and repositories actually support, where the evidence is only source-present, what the reference builds still need to implement, and which claims the book must avoid.

## Research frame

**Reader outcome.** After Chapters 17–22, a builder should be able to distinguish a channel bot from an organizational agent, connect an agent to collaboration channels, design an identity and authorization model, implement approval and memory boundaries, delegate safely to a machine agent, and plan a production rollout.

**Official source cutoff.** 2026-07-14.

**Pinned repository snapshots.** All repository findings in this packet refer to these immutable commits:

- CopilotKit monorepo: [`855446e1abc8f29756dc5e539e5e50a90321ac2d`](https://github.com/CopilotKit/CopilotKit/tree/855446e1abc8f29756dc5e539e5e50a90321ac2d)
- OpenTag `main`: [`df93bc0dccd0afc8eb7bb02206ffbe2ef7922322`](https://github.com/CopilotKit/OpenTag/tree/df93bc0dccd0afc8eb7bb02206ffbe2ef7922322)
- OpenTag managed-development snapshot: [`d6a807783136a9e0b6a610f16648df8f1980cdbc`](https://github.com/CopilotKit/OpenTag/tree/d6a807783136a9e0b6a610f16648df8f1980cdbc)

### Evidence labels

| Label | Meaning | Permitted wording in the manuscript |
|---|---|---|
| **D — documented** | Current official product or platform documentation states the capability. | “The documentation supports…” |
| **S — source-present** | The pinned official repository contains the API or implementation. It was inspected, not necessarily exercised live. | “At the pinned commit, the source includes…” |
| **R — runtime-observed** | The behavior was exercised and captured in the controlled reference environment. | “In our pinned reference run…” |
| **EA — early access / beta** | Officially labeled beta, waitlist, preview, internal, or otherwise not generally available. | Name the exact availability label and date. |
| **A — aspirational** | Proposed target architecture or future product statement. | “The reference implementation should…” or “The vendor says it plans…” |

Never collapse these labels. Source-present is not runtime-proven, and a product page's future intention is not a current capability.

## Executive findings

1. **A channel integration is not yet an organizational agent.** A bot transports messages. A channel agent also plans, calls tools, streams progress, and renders interactions. A governed organizational actor adds an explicit identity, authority, policy, accountability, retention, and operating model. The book should treat these as three distinct maturity states.

2. **CopilotKit Channels is a useful channel/runtime boundary, not a complete organizational-governance system.** At the pinned commit, `@copilotkit/channels` normalizes channel ingress, drives an agent run, renders agent events back to the channel, and exposes state, identity-correlation, transcripts, action rehydration, locking, deduplication, and queue primitives. Those are application primitives. They do not decide whether a Slack user may approve a wire transfer, whether a Teams channel may access customer records, or whether an action satisfies separation of duties.

3. **The current source is ahead of some public documentation.** The pinned packages contain a broader `StateStore` contract, typed state, identity and transcript support, and adapter behaviors not consistently reflected in current guides. The book must pin every code sample and label documentation/source drift. It should not silently combine APIs from different dates.

4. **Identity resolution is not authorization.** Channels can resolve a platform user to a stable application key and can inject sender context into a run. Neither proves that the user is entitled to the requested resource or action. Authorization must be enforced at the tool boundary using trusted platform/application attributes, not model-visible prompt text.

5. **A rendered confirmation is not yet a secure approval.** The current Slack/OpenTag example can pause for a button choice, but the inspected example does not bind the click to a permitted approver, bind the decision to a canonical action digest, enforce an expiry or quorum, or reauthorize immediately before execution. It is a teaching-quality interaction pattern, not evidence of production-grade governance.

6. **The same semantic UI can cross channels, but behavior cannot be assumed identical.** `@copilotkit/channels-ui` builds a serializable semantic intermediate representation. Slack, Discord, and Teams adapters translate that representation into native surfaces. Platform limits differ in acknowledgements, modals, ephemeral responses, reactions, files, identity lookup, and streaming semantics. Design to declared capabilities and fallbacks rather than lowest-common-denominator prose.

7. **OpenTag is the best Level 3 reference project, but it must be described precisely.** The pinned `main` snapshot is a self-hosted, multi-channel agent example using the earlier `@copilotkit/bot*` package names. Its directly configured adapters cover Slack, Discord, Telegram, and WhatsApp, not Teams. A later managed-development snapshot uses current `@copilotkit/channels*` package names and a managed adapter, but this is source-present, not proof of generally available CopilotKit Intelligence.

8. **CopilotKit Intelligence is not safe to present as generally available.** Official Channels and LangGraph channel documentation currently describes managed Slack/Teams access as a waitlist. The pinned monorepo also contains an Intelligence package and managed examples, but one source entry explicitly describes itself as internal and not publicly documented. Classify it as early access/source-present until publication verification says otherwise.

9. **Claude Tag is the clearest current example of a managed organizational actor, with important boundaries.** Anthropic introduced Claude Tag on June 23, 2026 as a public beta for Claude Team and Enterprise. Current official documentation names Slack as the supported collaboration surface and does not name or commit to Microsoft Teams. Claude Tag uses an agent service identity for channel work, isolated ephemeral execution environments, selected channel scopes, profile policies, logs, spend controls, and shared memory. It does not mean every action runs on the requesting user's own permissions.

10. **An agent service identity creates a deliberate confused-deputy risk to manage.** A channel member can potentially ask an agent to use resources granted to the agent profile even if that member lacks direct access. The risk can be acceptable when explicit and tightly scoped. The policy should combine agent authority, requester rights, channel policy, resource sensitivity, and action risk, especially for writes.

11. **Institutional memory is a governed knowledge product, not a transcript dump.** Raw channel messages and agent transcripts have participants, retention duties, and deletion requirements. A reusable organizational memory should carry provenance, scope, review status, sensitivity, retention, and correction controls. Transcript persistence alone does not provide those properties.

12. **Delegating into Level 2 expands blast radius.** An organizational agent that assigns work to a machine agent needs a constrained task specification, sandbox, short-lived capability, network/filesystem policy, independent write approvals, and returned artifacts with provenance. It must not forward ambient organization credentials or treat a channel mention as permission to change a machine.

## Taxonomy: bot, channel agent, organizational actor

Use this taxonomy at the start of Chapter 17. It prevents the book from treating “it works in Slack” as the end state.

| Dimension | Channel bot | Channel agent | Governed organizational actor |
|---|---|---|---|
| Primary job | Receive and send platform events | Pursue goals through models and tools | Act under organization-defined authority |
| Context | Current event or thread | Thread, agent state, tools, perhaps memory | Tenant, workspace, channel, requester, policies, resources, history |
| Identity | Bot/application installation | Agent runtime plus platform sender | Explicit agent service identity plus actor/subject chain |
| Authorization | Platform installation and scopes | Often tool-level application checks | Central policy enforcement at every consequential boundary |
| Interaction | Messages, commands, buttons | Streaming, tool UI, approvals, interrupts | Identity-bound, policy-bound, auditable interventions |
| Memory | Platform history | Thread/checkpoint/transcript | Provenanced, scoped, reviewed institutional memory |
| Delegation | None or webhooks | Calls another agent/tool | Capability-constrained delegation with accountability |
| Audit | Platform log | Runtime traces | Cross-system decision and action ledger |
| Failure model | Retry event delivery | Retry/resume run | Contain, revoke, compensate, investigate, and notify |
| Owner | App developer | Agent product team | Product, security, platform, data, legal, and business owner |

### Chapter 17 thesis candidates

- The organizational-agent threshold is crossed when an agent's authority becomes shared, durable, and accountable, not when its interface moves into Slack.
- A collaboration channel supplies social context. It does not supply business authorization.
- The three identities to preserve are **who asked**, **which agent acted**, and **which system accepted the action**.

### Maturity test

An implementation should not be called a governed organizational agent until the team can answer all of these questions with executable policy or an owned operational procedure:

1. Who is the agent, independently of the person who invoked it?
2. Which users, roles, channels, workspaces, and tenants may invoke it?
3. Which resources may it read under its own identity?
4. When does it act on behalf of the requester instead?
5. What decision combines requester, channel, agent, action, resource, and risk?
6. Which actions need approval, by whom, with what evidence and expiry?
7. What is stored as thread state, transcript, or institutional memory?
8. How are derived memories corrected and deleted?
9. How are tool use and delegated machine work audited across systems?
10. What happens when the platform retries an event or a user clicks twice?
11. Who can stop the agent, revoke its credentials, or disable a single tool?
12. How is the agent decommissioned, including tokens, memory, logs, schedules, and downstream artifacts?

## Current CopilotKit Channels architecture

### Package map at the pinned commit

| Package | Role | Evidence | Boundary to explain |
|---|---|---|---|
| `@copilotkit/channels` | Channel-neutral bot/agent runtime, thread abstraction, tools, state, identity, transcript, action dispatch | **S**: [package source](https://github.com/CopilotKit/CopilotKit/tree/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels) | Does not itself define enterprise authorization policy |
| `@copilotkit/channels-ui` | JSX runtime and semantic UI intermediate representation | **S**: [package source](https://github.com/CopilotKit/CopilotKit/tree/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels-ui) | JSX here is not React DOM and does not imply pixel parity |
| `@copilotkit/channels-slack` | Slack ingress, capabilities, and Block Kit rendering | **S**: [package source](https://github.com/CopilotKit/CopilotKit/tree/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels-slack) | Slack scopes and installation do not replace app authorization |
| `@copilotkit/channels-discord` | Discord Gateway/interaction ingress and Components rendering | **S**: [package source](https://github.com/CopilotKit/CopilotKit/tree/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels-discord) | Intents determine event/data access, not business entitlement |
| `@copilotkit/channels-teams` | Teams bot ingress and Adaptive Card rendering | **S**: [package source](https://github.com/CopilotKit/CopilotKit/tree/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels-teams) | Entra, Azure Bot, Graph, and Teams app permissions remain separate layers |
| `@copilotkit/channels-intelligence` | Managed-listener/Intelligence-facing source integration | **S/EA**: [package source](https://github.com/CopilotKit/CopilotKit/tree/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels-intelligence) | Source describes an internal, not publicly documented API; public docs still say waitlist |

Official Channels documentation presents the direct package stack and labels managed Slack and Teams as waitlist experiences: [Channels reference](https://docs.copilotkit.ai/reference/channels), [LangGraph channels guide](https://docs.copilotkit.ai/langgraph-python/channels), [Slack guide](https://docs.copilotkit.ai/slack), and [Teams guide](https://docs.copilotkit.ai/teams). These pages are live documentation and may drift after the cutoff; the book should capture their publication date or commit before final layout.

### Runtime path

The chapter diagram should show this sequence:

```text
Platform event
  -> platform adapter verifies/normalizes ingress
  -> createBot selects conversation/thread
  -> acquire per-conversation lock
  -> deduplicate platform event ID
  -> resolve stable user identity, if configured
  -> construct trusted context plus agent-visible context
  -> run AG-UI-compatible agent
  -> receive lifecycle, message, tool, state, and interrupt events
  -> convert semantic BotNode UI into platform-native representation
  -> post/update/stream through adapter
  -> persist state, action snapshot, transcript, and audit events as configured
```

This is an explanatory synthesis from the pinned [`create-bot.ts`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels/src/create-bot.ts), [`thread.ts`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels/src/thread.ts), and state sources. Do not redraw the sequence as if every stage were a security control. For example, event deduplication protects ingestion behavior; it does not make the downstream side effect exactly once.

### `createBot` knobs builders need to understand

The pinned `createBot` surface includes adapters, an agent, tools, context builders, components, commands, and store configuration. The store configuration is especially relevant for Chapters 18–20:

- `adapter`: a `StateStore` implementation.
- `state`: an optional Standard Schema for typed bot/thread state.
- `identity`: a resolver from platform identity to a stable application user key.
- `transcripts`: retention and maximum-per-user configuration, paired with identity.
- `onLockConflict`: drop, force, or callback behavior when a conversation is already running.
- lock TTL and dedup TTL, with defaults visible in source.

Source candidate: [`packages/channels/src/create-bot.ts`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels/src/create-bot.ts).

Editorial warning: name these options as source-present at the pinned commit. Do not copy a sample from a newer docs page without retesting it against the pinned package versions.

### StateStore is an application primitive

At the pinned commit, [`StateStore`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels/src/state/state-store.ts) covers more than a single JSON blob. The source exposes categories for key-value state, ordered lists, locks, deduplication, and queues. The default memory implementation is useful for development but loses state on process restart.

The chapter should turn this into a production decision table:

| Store capability | Why Channels needs it | Production design question |
|---|---|---|
| Key/value | Thread state, action snapshots, configuration | Tenant partition key, encryption, schema migration, TTL |
| List | Transcripts and ordered records | Maximum size, stable ordering, pagination, deletion |
| Lock | Serialize overlapping work per conversation | Distributed fencing, TTL expiry, crash recovery, stale holder behavior |
| Dedup | Suppress repeated platform events | Idempotency horizon, atomicity with work acceptance, retry semantics |
| Queue | Deferred or ordered work primitives | Visibility timeout, dead-letter policy, poison message handling |

The default behavior around overlapping runs also deserves a worked example. “Drop” protects a single conversation from concurrent work but may surprise a user. “Force” allows the new work to proceed and does not necessarily cancel work already in flight. A callback can implement a business-specific decision. None of these modes is a substitute for a durable workflow scheduler when jobs run for minutes or hours.

### Locking, deduplication, and exactly-once myths

From the pinned ingress flow:

- The runtime attempts a conversation lock before deduplication.
- A platform event identifier is used when available for deduplication.
- Dedup-store failures warn and continue.
- Lock conflicts follow configured behavior.

Book implication: the reader must distinguish **duplicate delivery**, **duplicate agent run**, and **duplicate external side effect**. A correct design gives a write tool its own idempotency key and stores a result keyed by the canonical requested action. Event dedup alone cannot prove the CRM update, payment, ticket creation, or deployment ran only once.

### Identity resolver and transcripts

The source identity resolver can correlate Slack, Discord, or Teams identities to a stable application user key. Transcript support then lists or deletes records by that user key, applies configured retention and maximum counts, injects prior history when explicitly requested, and appends the new user/assistant exchange. See [`transcripts.ts`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels/src/transcripts.ts).

Important boundaries:

- Resolution failure can continue without a user key. That may be acceptable for public read-only help, but a high-risk tool should fail closed when trusted identity is required.
- A stable correlation key says “these platform identities belong to this application principal.” It does not say “this principal may perform this action.”
- Transcript retention is not a complete privacy or records-management program. Platform copies, tool logs, traces, derived memories, backups, and exports may have separate lifecycles.
- A transcript is conversation history. Institutional memory needs curation, provenance, scope, sensitivity, review, and correction.

### Thread capabilities

The pinned [`Thread`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels/src/thread.ts) abstraction can post, update, delete, and stream content; run or resume an agent; wait for a user choice; and expose capability-gated methods such as message lookup, user lookup, files, suggested prompts, title updates, reactions, and ephemeral messages. Builders should interrogate capabilities before promising a channel-specific experience.

The book should use “thread” carefully. A channel platform's thread, a CopilotKit conversation key, an agent thread/checkpoint, and a business case ID can be related without being identical. Store their mapping explicitly so an audit can cross the boundary.

### Semantic JSX and intermediate representation

[`@copilotkit/channels-ui`](https://github.com/CopilotKit/CopilotKit/tree/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels-ui) is a small JSX runtime that produces a semantic `BotNode[]` intermediate representation rather than a browser DOM. Registered components include message/header/section/markdown/field/context/actions/image/divider/button/select/input/table and chart concepts at the pinned source. Adapters render those concepts using Slack Block Kit, Discord components, or Teams Adaptive Cards.

This is the correct mental model:

```text
Agent chooses a semantic artifact or tool interaction
  -> application renders a named, registered channel component
  -> JSX runtime creates serializable semantic nodes
  -> adapter maps supported nodes to native UI
  -> adapter supplies an explicit fallback for unsupported behavior
```

The interaction layer supports behaviors such as click, selection, form submission, and reaction. Action identifiers are opaque `ck:` values derived from stable content, and action snapshots can support later rehydration. Registered named components plus durable storage are required if a click must survive a process restart. Inline closures only exist in the current process.

Do not describe the opaque ID as an authorization token. It is an action-routing mechanism. A handler must still authenticate the platform actor, verify eligibility, reauthorize the action, reject replay, and audit the result.

## Platform adapter realities

### Cross-platform capability matrix at the pinned source

This table is source inspection, not live end-to-end proof.

| Capability | Slack | Discord | Teams | Manuscript implication |
|---|---|---|---|---|
| Declared acknowledgement deadline | ~3 seconds | ~3 seconds | ~15 seconds | Acknowledge quickly and move long work off the ingress path |
| Modals | Declared supported | Declared supported at the pin | Not declared | Provide a message/card fallback |
| Typing indicator | Not declared | Declared | Declared | Do not use typing as the only progress signal |
| Reactions | Declared | Declared | Not declared | Reaction-driven actions need fallbacks |
| Streaming | Declared | Declared | Declared through updates | “Streaming” may mean tokens or repeated message edits |
| Ephemeral output | Declared | Limited by Discord context | Not declared | Sensitive previews need channel-specific handling |
| Render limits | Slack block limit represented | Discord component limit represented | Adaptive Card constraints apply | Test the same semantic tree in every target adapter |
| User lookup | Adapter capability exists | Adapter-dependent | Not wired at the pinned source | Never assume a cross-channel directory API |
| File handling | Platform adapter support | Platform adapter support | Personal inline; channel files require Graph configuration; group-chat gaps | Files change permissions and data-location risk |

Because public guides can lag the pinned source, the final book should generate this table from a versioned capability test rather than copying it uncritically. Where docs and source disagree, note the exact version and test the published sample.

### Slack deployment and security considerations

Official Slack sources establish these platform facts:

- [Socket Mode](https://api.slack.com/apis/connections/socket) carries events over a pre-authenticated WebSocket, but the app must still acknowledge each event.
- The [Events API](https://api.slack.com/apis/connections/events-api) retries failed deliveries and uses a short acknowledgement window. Retry metadata must be expected.
- HTTP endpoints should follow Slack's [request-signature verification](https://docs.slack.dev/authentication/verifying-requests-from-slack/) using the signing secret, request timestamp, and replay window.
- OAuth scopes control which Slack events and APIs the app can access. Conversation history access depends on scopes and membership. Sending as the app differs from impersonating a user.

Builder knobs for Chapter 18:

1. Socket Mode versus public HTTP event receiver.
2. Workspace installation model and tenant mapping.
3. Mention-only, direct message, assistant pane, or ambient event behavior.
4. Minimum OAuth scopes and whether the app must join a channel.
5. Signature verification and raw-body handling for HTTP ingress.
6. Retry/dedup keys and acknowledgement path.
7. Token storage, rotation, uninstall, and revocation.
8. Enterprise Grid and multi-workspace isolation.
9. Private-channel handling and whether memory crosses channel boundaries.
10. Whether a post is visibly from the app, from an agent identity, or an explicitly authorized user impersonation.

Platform scopes answer what the Slack application can technically receive or do. They do not answer whether Jerel in `#finance-ops` may approve a particular payment. That decision belongs to the application policy layer.

### Discord deployment and security considerations

Official Discord documentation defines [Gateway intents](https://docs.discord.com/developers/events/gateway) as the event categories and data a bot receives. Message Content and Guild Members are privileged intents; verified applications above Discord's threshold require approval. Without Message Content, most message fields are unavailable except in defined cases such as direct messages, mentions, and the application's own messages.

Discord [interactions](https://docs.discord.com/developers/interactions/receiving-and-responding) require a fast initial response, while interaction tokens remain useful only for a bounded period. This affects modal and deferred-response design.

Builder knobs:

1. Which Gateway intents are truly necessary.
2. Slash commands and mentions versus ambient message ingestion.
3. Bot role and channel permissions, separate from intents.
4. Interaction acknowledgement and deferred response.
5. Guild-to-tenant mapping and direct-message policy.
6. Thread/channel identity and data segregation.
7. Privileged intent approval as the app scales.
8. Component and modal fallbacks when an interaction context cannot support them.

Intents are data-delivery controls, not business authorization. A bot seeing a message is not proof the sender may use an attached business tool.

### Teams deployment and security considerations

Microsoft's official Teams setup requires an [Entra app registration, Azure Bot resource, messaging endpoint, and Teams channel configuration](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/authentication/add-authentication). The exact guide routes evolve, so the final manuscript should verify the current Microsoft 365 Agents Toolkit flow at publication.

Teams permissions span multiple layers:

- Entra/Graph delegated or application permissions.
- Teams app manifest permissions and [resource-specific consent](https://learn.microsoft.com/en-us/microsoftteams/platform/graph-api/rsc/resource-specific-consent).
- Bot installation scope and conversation context.
- Application-level policy for the requested action.

Microsoft documents [channel and chat message access for bots and agents](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/conversations/channel-messages-with-rsc), including RSC permissions that can allow message receipt without an explicit mention after appropriate consent. Treat ambient channel access as a higher-risk mode than mention-only invocation.

At the pinned CopilotKit source, Teams channel-file access can require Microsoft Graph application credentials because channel files live in SharePoint-backed storage. Personal-context files and channel files do not have the same path; group-chat support has gaps. This should become a screenshot and test matrix, not a blanket “file support” checkmark.

Builder knobs:

1. Entra tenant and app-registration ownership.
2. Single-tenant versus multi-tenant installation.
3. Azure Bot messaging endpoint, validation, and production hosting.
4. Delegated versus application Graph permissions.
5. Resource-specific consent versus tenant-wide access.
6. Mention-only versus ambient channel messages.
7. Personal, channel, and group-chat file paths.
8. SharePoint/OneDrive data residency and retention inheritance.
9. Adaptive Card version and host capability.
10. Credential rotation, admin consent removal, and app uninstall.

Do not use a successful run in the local Microsoft 365 Agents Playground as proof that a production tenant's Entra, Azure Bot, consent, SharePoint, or retention configuration works.

## Actions, interrupts, and production-grade approvals

### What the current example demonstrates

The pinned Slack example registers a frontend-style `confirm_write` tool and calls `thread.awaitChoice` to display approval choices before a write. Sources:

- [`confirm-write-tool.tsx`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/examples/slack/app/human-in-the-loop/confirm-write-tool.tsx)
- [`sender-context.ts`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/examples/slack/app/sender-context.ts)
- [`app/index.ts`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/examples/slack/app/index.ts)

This is a good demonstration of pausing an agent and using native UI. It is not evidence of the following controls:

- The clicking user is the requester or an eligible approver.
- The approved arguments are exactly the arguments later executed.
- The decision expires.
- The action can be approved only once.
- A high-risk action requires two different people.
- The underlying permission has not changed since the card was rendered.
- The execution is idempotent.
- Approval and execution share a tamper-evident audit chain.

The sender-context helper can add a name, email, or ID to model context. The chapter should explicitly annotate this code: **context helps the model communicate; it must not make the authorization decision**.

### Approval record the reference build should implement

The implementation chapter should define a persisted, server-created approval proposal with at least:

| Field | Purpose |
|---|---|
| `proposal_id` | Stable identifier, never model-generated authority |
| `tenant_id`, `workspace_id`, `channel_id` | Scope and isolation |
| `requester_principal` | Human or system that requested the action |
| `agent_principal` | Service identity proposing/executing |
| `tool_name`, `tool_version` | Exact operation contract |
| `canonical_arguments_hash` | Binds approval to normalized arguments |
| `target_resource` | Human-readable and machine-checkable target |
| `risk_class`, `reversibility` | Chooses approval policy |
| `eligible_approver_policy_version` | Freezes which policy was evaluated |
| `approvals[]` | Approver principal, decision, timestamp, evidence |
| `threshold` | One-person, M-of-N, or role-separated quorum |
| `expires_at` | Rejects stale decisions |
| `idempotency_key` | Deduplicates execution at the side-effect boundary |
| `run_id`, `thread_id`, `platform_event_id`, `trace_id` | Cross-system correlation |
| `status` | Proposed, approved, rejected, revoked, expired, executing, executed, failed, compensated |

Execution sequence to teach:

1. The model proposes a typed tool call.
2. A trusted policy layer validates schema, target, requester, channel, agent, and current resource policy.
3. If approval is required, the server canonicalizes arguments and persists the proposal before rendering UI.
4. The channel action ID contains or resolves only an opaque proposal reference.
5. On click, the server authenticates the platform actor and maps it to an application principal.
6. The server verifies eligibility, separation of duties, decision expiry, proposal status, and argument hash.
7. When quorum is met, execution reauthorizes against current policy and current resource state.
8. The tool uses an idempotency key at the downstream system.
9. Result, failure, or compensation is appended to the audit record.
10. The channel message is updated from authoritative state, not from the button payload.

### Wrong-user, replay, and race tests

These tests should be mandatory for the Level 3 reference repo and screenshot set:

- A user outside the eligible approver set clicks Approve: rejected with no state change.
- The requester attempts to approve an action requiring separation of duties: rejected.
- An approved card is clicked twice: one execution result, one replay rejection.
- Two eligible approvers click simultaneously for a one-of-N policy: one transition wins safely.
- Arguments or target change after approval rendering: original approval invalidated.
- Approval expires before execution: rejected and re-proposed if still needed.
- Process restarts after rendering and before click: registered action rehydrates from durable state.
- Process restarts after downstream success and before local status update: idempotent recovery reads the existing result.
- Approver loses the necessary role between render and click: current reauthorization rejects.
- Agent service credential is revoked: action fails closed and produces an operational alert.

### Blocking and non-blocking channel interaction

Some channel/runtime combinations can hold a logical run while awaiting a choice; managed or asynchronous surfaces may end the turn and start a follow-up run. The OpenTag managed-development snapshot contains a dual-mode pattern in which a button can start a new run when blocking choice is unavailable. This is **S/EA**, not a generic availability promise: [`app/managed.ts`](https://github.com/CopilotKit/OpenTag/blob/d6a807783136a9e0b6a610f16648df8f1980cdbc/app/managed.ts).

The reference implementation should not resume from a natural-language “approved” prompt. It should resume from a trusted approval record and exact proposal ID. The model may explain the transition, but the policy engine owns it.

## Identity, authority, and policy model

### Principal model

Every consequential tool invocation should preserve this tuple:

```text
requester principal
+ agent service principal
+ tenant/workspace/channel context
+ selected policy profile
+ action and canonical arguments
+ target resource and sensitivity
+ credential mode (agent or delegated user)
+ execution environment and risk
```

The model may help select an intended tool. It must not manufacture any of these trusted attributes.

### RBAC and ABAC

Use role-based access control for understandable coarse permissions:

- Who may install or configure the agent.
- Who may invoke it in a channel.
- Who may administer memory and policies.
- Who may approve a risk class.
- Who may inspect audit records.

Use attribute-based access control for contextual decisions. [NIST SP 800-162](https://csrc.nist.gov/pubs/sp/800/162/upd2/final) defines ABAC around attributes of the subject, object, requested operation, and environment. Relevant attributes include tenant, workspace, channel classification, requester department, resource owner, record sensitivity, tool risk, amount, time, location, incident state, and data residency.

[NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) supports per-request, least-privilege decisions and treats non-person entities as identities worth governing. Apply that principle to the agent, machine worker, adapter, and tool service.

Recommended policy shape:

```text
allow = agent_profile_allows(action, resource)
    AND channel_policy_allows(action, resource)
    AND requester_policy_allows(requester, action, resource)
    AND environment_policy_allows(risk, location, time)
    AND required_approval_policy_is_satisfied
```

Some organizations may intentionally allow an agent service identity to perform tasks beyond a requester's own direct access. If so, document that as the product's authority model, scope the channel to the least-privileged member, restrict who may invoke it, and require stronger approvals for high-impact actions. Do not hide the choice inside a prompt.

### Agent identity versus on-behalf-of access

Two credential modes must be distinct in code, UI, and audit:

1. **Agent identity.** The target system records that the organizational agent acted. Its service account has its own least-privilege scope. This supports durable team workflows but creates a shared-authority surface.
2. **On behalf of the requester.** The target system evaluates a delegated user token and records the user plus the acting agent. This preserves individual entitlement but may be harder for asynchronous or scheduled work.

[RFC 8693 OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693) distinguishes delegation from impersonation and defines subject/actor token concepts. For delegated execution, the reference architecture should mint a short-lived, audience-bound, resource-bound token carrying the actor/subject chain. Raw long-lived tokens should not be placed in prompts, transcripts, channel state, or an agent sandbox.

### Confused deputy threat

The organizational agent is a classic potential deputy: it possesses authority and receives instructions from users with varying rights. Attack paths include:

- A channel member asks the agent to retrieve a document they cannot access directly.
- Malicious text in a shared document asks the agent to exfiltrate data through another tool.
- A low-trust channel delegates work to a machine worker with broader filesystem or cloud credentials.
- A forged or replayed button action appears to authorize a write.
- An agent uses its own high-privilege identity when the operation should have used the requester's delegated rights.
- One agent delegates to another without propagating the requester, policy, and resource constraints.

The primary mitigation is a policy enforcement point outside the model for every privileged tool call. Prompt rules and sender context are useful signals only after trusted identity mapping and only as model context.

The [OWASP Top 10 for Agentic Applications 2026](https://owasp.org/www-project-top-10-for-agentic-applications/) is a useful security-review crosswalk for identity and privilege abuse, tool misuse, memory poisoning, and insecure inter-agent communication. Use OWASP as a taxonomy, not as evidence that a specific product has or lacks a vulnerability.

## Memory, transcripts, retention, and audit

### Memory taxonomy for an organizational agent

| Layer | Example | Default owner | Required controls |
|---|---|---|---|
| Platform event history | Slack thread or Teams conversation | Platform/organization | Platform retention, legal hold, participant access |
| Agent run state | Current plan, pending tool, checkpoint | Agent runtime team | Tenant key, TTL, resume policy, encryption |
| Transcript | User/assistant exchanges retained for continuity | Product team | Identity mapping, retention, export/delete, redaction |
| Working artifact | Report, table, code diff, ticket draft | Business workflow owner | Versioning, source links, approval status |
| Candidate memory | Model-proposed durable fact | Memory service | Provenance, sensitivity scan, reviewer status |
| Institutional memory | Approved policy, decision, or reusable fact | Organization knowledge owner | Scope, effective dates, citations, review, expiry, deletion |
| Audit record | Decision, policy evaluation, tool action, result | Security/compliance owner | Append-only controls, access separation, retention, redaction |

The manuscript should show a promotion pipeline:

```text
channel evidence
  -> candidate memory with source pointers
  -> sensitivity and policy check
  -> human or rules-based review
  -> scoped institutional store
  -> retrieval with provenance and effective date
  -> correction, expiry, or deletion workflow
```

Raw transcripts should not be promoted automatically. A hostile instruction, obsolete decision, private-channel fact, or unverified claim can poison future behavior if copied into shared memory.

### Audit event model

Channels does not claim to supply an immutable enterprise audit log. The reference system should append events outside ordinary conversational state. Each event should include:

- Tenant, workspace, channel, platform event, business case, agent run, and trace correlation IDs.
- Requester and agent principals, credential mode, and delegated actor/subject chain.
- Policy version, input attributes, decision, reason code, and approval requirement.
- Tool name/version, canonical argument digest, target resource, and risk class.
- Approver identities, decisions, timestamps, quorum result, and expiry.
- Execution environment, downstream request/idempotency ID, result, and compensation.
- Memory reads/writes with source provenance and scope.
- Redaction metadata rather than raw secrets or unnecessary message bodies.

“Tamper evident” or “immutable” should only be used if the implementation actually provides append-only storage, restricted writers, integrity checks, retention locks, and tested export. A normal application log file is not enough.

### Deletion and residency questions

Builders need a data inventory before rollout:

1. Where does the platform store messages, files, reactions, and app metadata?
2. Where does the channel adapter store state and action snapshots?
3. Where does the agent runtime store checkpoints and traces?
4. Which model provider receives message content and tool results?
5. Where do tools store created artifacts?
6. Which derived memories retain facts after a transcript is deleted?
7. Which backups, exports, and audit stores are subject to different retention?
8. Which region processes and stores each class of data?
9. Can a tenant export, correct, delete, or place a legal hold on each class?
10. What happens to scheduled jobs and delegated machine artifacts when a user or workspace is removed?

Transcript `delete` support is helpful, but it cannot delete copies in Slack, Microsoft 365, Discord, LangSmith or another tracer, model-provider logs, tool systems, backups, or derived institutional memory. The book should never imply otherwise.

## OpenTag: what it is and what it proves

### `main` snapshot

The pinned [`OpenTag` main snapshot](https://github.com/CopilotKit/OpenTag/tree/df93bc0dccd0afc8eb7bb02206ffbe2ef7922322) is an official open-source, self-hostable reference project. At that commit:

- Package metadata and examples still use the earlier `@copilotkit/bot*` naming rather than the current `@copilotkit/channels*` names.
- Direct adapters cover Slack, Discord, Telegram, and WhatsApp.
- The runtime uses a CopilotKit built-in AG-UI agent plus MCP-connected tools.
- The inspected snapshot does not establish a LangGraph supervisor, a policy engine, a durable organizational memory service, or machine-agent delegation.
- The human-in-the-loop example and sender context illustrate interaction but have the approval boundaries described above.

Relevant immutable sources:

- [README](https://github.com/CopilotKit/OpenTag/blob/df93bc0dccd0afc8eb7bb02206ffbe2ef7922322/README.md)
- [`package.json`](https://github.com/CopilotKit/OpenTag/blob/df93bc0dccd0afc8eb7bb02206ffbe2ef7922322/package.json)
- [`app/index.ts`](https://github.com/CopilotKit/OpenTag/blob/df93bc0dccd0afc8eb7bb02206ffbe2ef7922322/app/index.ts)
- [`runtime.ts`](https://github.com/CopilotKit/OpenTag/blob/df93bc0dccd0afc8eb7bb02206ffbe2ef7922322/runtime.ts)
- [`confirm-write-tool.tsx`](https://github.com/CopilotKit/OpenTag/blob/df93bc0dccd0afc8eb7bb02206ffbe2ef7922322/app/human-in-the-loop/confirm-write-tool.tsx)
- [`sender-context.ts`](https://github.com/CopilotKit/OpenTag/blob/df93bc0dccd0afc8eb7bb02206ffbe2ef7922322/app/sender-context.ts)

Correct positioning: **OpenTag demonstrates how one agent application can enter multiple conversation surfaces using CopilotKit's channel stack. The book's reference build then adds the missing organizational governance layers.**

### Managed-development snapshot

The later [`d6a8077` snapshot](https://github.com/CopilotKit/OpenTag/tree/d6a807783136a9e0b6a610f16648df8f1980cdbc) contains current `@copilotkit/channels*` dependencies, a `MANAGED.md`, and [`app/managed.ts`](https://github.com/CopilotKit/OpenTag/blob/d6a807783136a9e0b6a610f16648df8f1980cdbc/app/managed.ts). This is useful evidence of direction and API design. It is not proof that every reader can provision the managed service.

The final book must check three independent facts at publication:

1. Is CopilotKit Intelligence generally available, private preview, or waitlisted?
2. Which channels are provisionable and in which regions?
3. Which identity, state, approval, observability, and retention functions are service responsibilities versus application responsibilities?

Until that verification, label the managed path **early access/source-present** and keep the self-hosted path as the reproducible build.

## Claude Tag: managed organizational-agent reference

Anthropic's [June 23, 2026 announcement](https://www.anthropic.com/news/introducing-claude-tag) describes Claude Tag as a team-oriented agent that joins selected Slack channels, connects to chosen tools, data, and code, works asynchronously, and supports schedules, memory, spending controls, and logs. Current official pages label it a public beta for Claude Team and Enterprise:

- [Claude Tag overview](https://claude.com/docs/claude-tag/overview)
- [How it works](https://claude.com/docs/claude-tag/concepts/how-it-works)
- [Agent identity](https://claude.com/docs/claude-tag/concepts/agent-identity)
- [Security and data](https://claude.com/docs/claude-tag/concepts/security-and-data)
- [Settings map](https://claude.com/docs/claude-tag/concepts/settings-map)
- [Memory](https://claude.com/docs/claude-tag/users/memory)
- [Product page](https://claude.com/product/tag)
- [Agent identity and access model](https://claude.com/blog/agent-identity-access-model)

### Confirmed current positioning

- **EA/D:** Public beta, available to Team and Enterprise customers in Slack.
- **D:** Current official documentation names Slack and does not name or commit to Microsoft Teams.
- **D:** A Slack thread maps to an isolated execution session with an ephemeral sandbox; durable thread/session records and the sandbox have different lifetimes.
- **D:** Channel work uses an agent/service identity configured with profiles and scoped connections; direct-message behavior can differ.
- **D:** Credentials are mediated outside the sandbox through an agent proxy rather than exposed directly in the execution environment.
- **D:** Organization and channel configuration can control invocation, profiles, instructions, spend, and related settings.
- **D:** Public-channel memory can be shared at workspace scope, while private-channel handling is scoped differently. Channel participants can influence shared memory, making channel membership a governance decision.
- **D:** Retained memory/session transcripts make the product unavailable to organizations requiring zero-data-retention according to current security documentation.

### Important non-claims

- Do not say Claude Tag runs channel actions with each requester's delegated credentials by default. Its distinguishing model is an agent identity.
- Do not state a Microsoft Teams roadmap; current official pages name Slack and only express a general intent to expand availability.
- Do not say its sandbox is durable; current documentation separates ephemeral execution from retained session/memory records.
- Do not present future just-in-time credential grants or identity-aware overlays from the identity-model article as current product behavior.
- Do not imply that administrator configuration eliminates confused-deputy risk. Profile scope and invocation rights still need least-privilege design.

### Comparison lesson for builders

Claude Tag demonstrates that Level 3 cannot be reduced to an adapter. The managed product explicitly owns an execution environment, agent identities, credential mediation, channel scopes, administration, logs, spend limits, and memory behavior. A self-hosted Channels/OpenTag build must choose owners for the same concerns even if its implementation differs.

## Direct, managed, and product comparison matrix

This is an editorial comparison, not a buyer's ranking.

| Dimension | Direct CopilotKit Channels | OpenTag `main` | CopilotKit managed direction | Claude Tag public beta |
|---|---|---|---|---|
| Availability at cutoff | Source/packages and direct docs | Open-source reference | Waitlist/source-present; verify | Public beta for Team/Enterprise |
| Current surfaces | Slack, Discord, Teams source packages; current public API reference documents Slack and Discord directly | Slack, Discord, Telegram, WhatsApp in pinned app | Managed Slack/Teams waitlist described in docs; exact access verify | Slack; no named Teams commitment in current public pages |
| Hosting | Builder owns runtime and adapters | Builder self-hosts | CopilotKit-managed edge/runtime responsibilities need verification | Anthropic managed |
| Platform credentials | Builder provisions and protects | Builder provisions | Managed service may own more of channel edge; contract verify | Admin configures connections/profiles; credentials proxied |
| Agent runtime | Builder supplies compatible agent | Built-in AG-UI agent plus MCP in pin | Application/agent integration shown in source | Claude in isolated Anthropic execution environment |
| State | Memory default plus custom StateStore primitives | Project implementation | Managed claims/responsibilities need verification | Managed session/profile behavior |
| Identity | Resolver primitive; authorization app-owned | Sender context example, no complete policy engine | Identity responsibility claimed in waitlist messaging; verify API | Agent service identities and profile/channel controls |
| UI | Semantic JSX to native adapters | Example components/actions | Same conceptual channel UI | Product-owned Slack experience |
| Approvals | `awaitChoice`/actions primitives; secure approval app-owned | Demonstration confirmation | Managed workflow semantics need verification | Product controls exist; exact per-tool approval semantics verify per connection |
| Institutional memory | App-owned | Not established by pin | Managed responsibility unclear | Product memory with public/private scope rules |
| Audit/observability | App-owned plus chosen tracing/logging | Basic app/runtime evidence | Docs claim managed observability direction; exact SLA/export verify | Admin logs and usage/spend controls documented |
| Residency/retention | Builder selects every store/provider | Builder responsibility | Verify regions, subprocessors, and deletion | Product documentation and contract govern; ZDR restriction noted |
| Machine delegation | Builder-defined | Not established by pin | Not established by inspected evidence | Code/data/tool work supported; exact external machine authority depends on configured connections |

## Delegating from Level 3 to Level 2

The book's three-level model becomes concrete when a Slack request causes machine work. The safe reference flow should be:

```text
channel request
  -> trusted requester and channel resolution
  -> organization policy evaluation
  -> constrained task proposal
  -> approval when machine access or writes require it
  -> issue short-lived task capability and signed policy bundle
  -> machine worker starts in isolated workspace/sandbox
  -> worker reads only authorized files and uses allowlisted network/tools
  -> worker returns plan, commands, diffs, tests, and provenance
  -> organization agent renders artifacts for review
  -> separate approval for merge, deploy, publish, or external communication
  -> audit links channel, org run, machine run, repository commit, and result
```

### Delegation envelope

The organization agent should send a machine worker a structured envelope rather than an unconstrained transcript:

- Immutable task ID and originating tenant/workspace/channel/thread.
- Requester and agent principals, with signed actor/subject chain.
- Plain-language objective plus typed acceptance criteria.
- Repository/workspace locator pinned to a revision.
- Read/write path allowlists and explicit denies.
- Allowed commands and network destinations.
- Secret handles, not secret values.
- Step, time, token, and cost budgets.
- Side effects allowed without approval and those requiring another gate.
- Data classification and retention requirements.
- Callback/trace destination and artifact-signing requirements.
- Expiry, nonce, and revocation handle.

### Returned evidence

The machine worker should return:

- Files inspected and changed.
- Commands run with exit status.
- Test/lint/build results.
- Diff or artifact hash.
- External network/tool calls.
- Policy exceptions and approval IDs.
- Unresolved risks.
- Worker environment/version and source revision.

The channel UI should render this evidence as inspectable artifacts, not a model summary alone. A green “done” message is insufficient for merge or deployment authority.

### Prohibited shortcuts

- Do not forward the organization agent's broad service credentials into the worker.
- Do not let repository text override the signed task policy.
- Do not interpret a channel mention as approval to modify files.
- Do not let a machine worker publish, merge, deploy, or message customers merely because it completed local tests.
- Do not lose requester and agent identity when handing work to another agent.
- Do not return only a prose result; preserve exact diffs, commands, logs, and trace correlation.

## Rollout and operating model

### Recommended staged rollout

| Stage | Capability | Exit evidence |
|---|---|---|
| 0. Synthetic workspace | Fake users, channels, tools, and data | Retry, wrong-user, injection, restart, and deletion tests pass |
| 1. Private read-only pilot | One team, selected channels, no writes | Accuracy, source coverage, latency, cost, and privacy review |
| 2. Narrow real tools | Least-privilege read tools, explicit invocations | Tool authorization and tenant isolation tests pass |
| 3. Draft actions | Agent creates drafts but cannot commit | Users find artifacts useful; rejection/correction data reviewed |
| 4. Reversible writes | Low-risk, idempotent writes with one approval | Approval binding, recovery, audit, and compensation tested |
| 5. High-impact writes | Quorum/separation of duties | Security, compliance, business owner sign-off and game day |
| 6. Machine delegation | Sandboxed narrow worker | Capability revocation, artifact evidence, and escalation tested |
| 7. Memory | Curated, scoped institutional memory | Provenance, poisoning, correction, expiry, and deletion tested |
| 8. Ambient/scheduled work | Broader asynchronous autonomy | Spend limits, kill switches, on-call, and missed/duplicate job recovery |

Ambient listening, schedules, institutional memory, and machine delegation should arrive late because they expand authority and persistence simultaneously.

### Service-level objectives and metrics

Track product and safety outcomes together:

- Event acknowledgement success and platform retry rate.
- Accepted event to first useful artifact.
- Run completion, cancellation, recovery, and duplicate suppression.
- Tool authorization allow/deny/error distribution.
- Approval requested, approved, rejected, expired, replayed, and wrong-user rates.
- Side-effect idempotency conflicts and compensation rate.
- Cost per successful organizational task and per workspace.
- Memory write/retrieval/correction/deletion volume.
- Cross-tenant isolation test results.
- Policy engine latency and availability.
- Machine-worker sandbox or policy violations.
- User-reported unwanted action and mean time to containment.

Avoid optimizing completion rate alone. A low refusal rate can indicate over-broad authority.

### Operational controls

Every production deployment needs:

- Global agent kill switch.
- Per-tenant, workspace, channel, tool, and credential disable controls.
- Model/tool step, time, and spend budgets.
- Token and signing-key rotation.
- Adapter health, queue depth, store health, policy-engine health, and downstream tool dashboards.
- Dead-letter and manual-replay procedure that preserves idempotency.
- Incident playbooks for data exposure, malicious memory, compromised service identity, duplicate writes, and runaway scheduled work.
- Break-glass access with review and expiry.
- Export, deletion, legal-hold, and tenant-offboarding procedures.
- Decommission checklist covering platform uninstall, OAuth/Entra revocation, agent identities, webhooks, schedules, queues, memory, traces, backups, and delegated machine artifacts.

### Failure modes to teach

- Adapter start failure: the pinned `createBot.start()` path can isolate adapter failures and keep other adapters running. Operationally, partial startup must surface as degraded health, not a silent success.
- Store failure: identity/dedup behavior may warn and continue in some source paths. High-risk deployments should define which dependencies are fail-open and fail-closed.
- Platform retry: acknowledge quickly, persist acceptance, deduplicate, and let a worker process asynchronously.
- Agent timeout: show durable status and recovery options rather than losing the thread.
- Tool partial success: inspect downstream idempotency state before retrying.
- Card/action expiry: render authoritative status and refuse stale callbacks.
- Credential revocation: stop queued work, mark dependent schedules blocked, and notify owners.
- Memory corruption or poisoning: quarantine suspect entries, show provenance, roll back derived indexes, and retest affected tasks.

## Code excerpt candidates for Chapters 18–20

These are candidates for short, annotated excerpts. Copy only the minimum lines needed, preserve license attribution, pin the commit, and test against the book's reference repo before publication.

| Candidate | Source | Teaching point | Annotation required |
|---|---|---|---|
| `createBot` store configuration | [`create-bot.ts`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels/src/create-bot.ts) | State, identity, transcript, locking, and dedup knobs | “Primitives, not org authorization” |
| `StateStore` interface | [`state-store.ts`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels/src/state/state-store.ts) | Durable backend contract categories | Explain memory-store restart loss and tenant partitioning |
| Transcript API | [`transcripts.ts`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels/src/transcripts.ts) | Identity-keyed history and deletion | Separate transcript from institutional memory |
| Semantic channel UI component | [`components.tsx`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels-ui/src/components.tsx) | Named semantic IR across adapters | Show adapter-specific screenshots and fallback |
| Current adapter factory | [`examples/slack/app/index.ts`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/examples/slack/app/index.ts) | Direct, self-hosted multi-channel setup | Do not infer Teams from this example's adapter list |
| Sender context | [`sender-context.ts`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/examples/slack/app/sender-context.ts) | Useful personalized context | Put a red callout: not authorization |
| Confirmation tool | [`confirm-write-tool.tsx`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/examples/slack/app/human-in-the-loop/confirm-write-tool.tsx) | Native interaction and pause | Follow immediately with production approval delta |
| OpenTag self-hosted entry | [`app/index.ts`](https://github.com/CopilotKit/OpenTag/blob/df93bc0dccd0afc8eb7bb02206ffbe2ef7922322/app/index.ts) | Existing Level 3 reference architecture | Pin older package naming and supported adapters |
| OpenTag managed entry | [`app/managed.ts`](https://github.com/CopilotKit/OpenTag/blob/d6a807783136a9e0b6a610f16648df8f1980cdbc/app/managed.ts) | Blocking versus follow-up-run HITL | Label source-present/early access, not GA |

### Original code the book's repo should provide

The book should write and test original, production-shaped examples for these gaps rather than implying the upstream demos already solve them:

1. Trusted platform-identity mapping to an application principal.
2. Tool-bound authorization middleware using requester, agent, channel, action, resource, and risk attributes.
3. Short-lived delegated token exchange with actor/subject audit.
4. Persisted, argument-bound, expiring approval proposals.
5. Wrong-user rejection and M-of-N quorum.
6. Idempotent side-effect execution and crash recovery.
7. Tenant-partitioned durable `StateStore` implementation.
8. Institutional-memory promotion and deletion workflow.
9. Organization-to-machine delegation envelope and verifier.
10. Unified audit event schema and cross-system trace viewer.

These examples belong in the companion repo once its final URL and application layout are supplied. Leave repository links as publication blanks until the user confirms them.

## Screenshot and figure plan

### Existing OpenTag frames

The project currently has six OpenTag demonstration frames covering issue triage, a table, a chart, an inline chart, draft progress, and a human-in-the-loop approved state. They are reference material only. They do not prove a fresh runtime at the pinned commit and must not be captioned as runtime verification.

### Fresh capture set

| ID | Capture | What it proves | Required setup/caption metadata |
|---|---|---|---|
| L3-01 | Slack mention starts a scoped agent run | Invocation and thread identity | Synthetic workspace/user, package versions, pin, run ID |
| L3-02 | Progress plus structured table/card | State/event UI beyond text | Semantic component name and adapter |
| L3-03 | Same semantic artifact in Slack, Discord, Teams | IR reuse and native rendering differences | Side-by-side, capability/fallback annotations |
| L3-04 | Approval card before a reversible write | Human intervention surface | Proposal ID, exact target, risk, reversibility |
| L3-05 | Wrong user clicks Approve | Authorization is server-side | Rejection reason with synthetic identities |
| L3-06 | Two-person quorum reaches approved | Separation of duties | Distinct approver roles and authoritative status |
| L3-07 | Process restart before click | Durable action rehydration | Store backend, restart marker, same proposal ID |
| L3-08 | Duplicate platform delivery | Event dedup versus tool idempotency | Event ID and one downstream result |
| L3-09 | Agent delegates repository analysis to machine worker | Level 3 to Level 2 boundary | Policy envelope, sandbox, pinned revision |
| L3-10 | Machine diff/tests return to channel | Evidence-rich review | Commands, hashes, test result, trace links |
| L3-11 | Institutional-memory candidate review | Transcript versus approved memory | Source, scope, reviewer, expiry |
| L3-12 | Operations dashboard | Cost, failures, approvals, policy denies | Synthetic metrics, time window, no secrets |
| L3-13 | Direct versus managed architecture | Ownership boundary | Exact availability labels at publication |
| L3-14 | Claude Tag channel profile/admin view | Managed identity and policy surface | Only if authorized product access; label public beta |

### Capture quality rules

- Use a synthetic organization, users, channels, records, repositories, and credentials.
- Include exact commit/package versions and capture date in the caption or adjacent source note.
- Record the platform event ID, agent run/trace ID, and approval proposal ID when relevant.
- Blur or replace workspace IDs, tokens, emails, tenant IDs, and customer data.
- Show the browser/channel chrome needed to understand the platform, but crop irrelevant personal UI.
- Never use a marketing screenshot as runtime proof.
- Never use the M365 playground alone as evidence of a production tenant integration.
- Provide alt text that states the interaction and the builder lesson, not decorative appearance.
- Capture failure and rejection states, not only the happy path.

## Claims ledger

### Safe claims with qualification

| Claim | Evidence label | Required qualification |
|---|---|---|
| Channels provides channel-neutral runtime and semantic UI packages | S/D | Pin version; do not imply governance completeness |
| The pinned StateStore includes key/value, list, lock, dedup, and queue primitives | S | State that source was inspected; default memory store is not durable |
| Identity resolution can correlate platform users to an application key | S | Explicitly say it is not authorization |
| Registered actions can be rehydrated with durable state | S | Inline handlers do not survive restart; secure approval still app-owned |
| Slack, Discord, and Teams adapters differ in capabilities | S/D | Pin matrix and test current release |
| OpenTag is an open-source self-hostable multi-channel reference | S | Name supported adapters at the pinned main commit |
| CopilotKit has managed channel work in source and public waitlist docs | S/EA/D | Do not say GA |
| Claude Tag is a managed Slack organizational-agent public beta | D/EA | Team/Enterprise; current public pages do not name or commit to Teams |
| Claude Tag uses an agent identity for channel work | D | Distinguish DM/user behavior and future plans |

### Claims to avoid

1. “OpenTag is a production-governed organizational actor out of the box.”
2. “Adding sender context authenticates or authorizes the requester.”
3. “A confirmation button is a durable, secure approval.”
4. “All Channels adapters have feature parity.”
5. “OpenTag `main` currently uses all latest package names.”
6. “OpenTag `main` includes Teams in the configured adapters.”
7. “CopilotKit Intelligence is generally available.”
8. “Claude Tag currently supports Microsoft Teams.”
9. “Claude Tag uses each channel requester's delegated permissions by default.”
10. “A StateStore automatically provides tenant isolation, governance, or immutable audit.”
11. “A transcript is institutional memory.”
12. “An opaque channel action ID is an authorization token.”
13. “Event deduplication makes external writes exactly once.”
14. “Platform scopes, Gateway intents, or Entra consent replace business authorization.”
15. “AG-UI, MCP, and channel adapters solve the same protocol boundary.”
16. “Source-present code has been runtime-verified.”
17. “The current Slack/OpenTag example uses LangGraph orchestration.”
18. “A local Teams playground run proves production Azure/Entra configuration.”
19. “Persistent action rehydration guarantees exactly-once execution.”
20. “Deleting a Channels transcript deletes all downstream and derived data.”

## Chapter mapping

### Chapter 17 — From assistant to organizational actor

**Core teaching:** bot versus channel agent versus governed actor; authority expands with shared identity, persistent context, and organization tools.

**Evidence to use:** taxonomy, maturity test, Claude Tag as managed example, confused-deputy frame.

**Builder artifact:** authority map listing requester, agent identity, channels, resources, actions, owners, and blast radius.

**Chapter action:** classify an existing bot and identify the missing properties before calling it an organizational agent.

### Chapter 18 — Channels SDK and OpenTag

**Core teaching:** adapter/runtime/semantic UI architecture, direct versus managed deployment, platform constraints.

**Evidence to use:** package map, runtime path, `createBot` knobs, cross-platform matrix, OpenTag branch truth.

**Code candidates:** current direct `createBot`, semantic JSX component, `StateStore` interface.

**Screenshots:** L3-01 through L3-03 and L3-13.

**Chapter action:** connect one self-hosted agent to one channel with minimum scopes and a durable store.

### Chapter 19 — Identity, policy, and channel context

**Core teaching:** platform sender, application principal, agent service identity, actor/subject chain, RBAC/ABAC, agent versus delegated credentials.

**Evidence to use:** NIST, RFC 8693, platform scope sections, sender-context non-claim, Claude Tag identity model.

**Builder artifact:** authorization decision table and credential-mode matrix.

**Screenshots:** L3-04 through L3-06.

**Chapter action:** implement a policy enforcement point outside the model and prove a wrong-user rejection.

### Chapter 20 — Delegation, memory, and governance

**Core teaching:** institutional memory promotion, approval binding, quorum, audit, Level 3-to-Level 2 delegation.

**Evidence to use:** transcript boundaries, approval record, memory taxonomy, delegation envelope, OWASP crosswalk.

**Builder artifact:** signed task envelope, memory record schema, and audit event schema.

**Screenshots:** L3-07 through L3-11.

**Chapter action:** delegate a read-only repository analysis to a sandboxed worker and return provenance-rich artifacts.

### Chapter 21 — Claude Tag, OpenTag, and the emerging landscape

**Core teaching:** compare product/hosting/authority choices without flattening maturity or availability.

**Evidence to use:** direct/managed/product matrix, Claude Tag confirmed facts and non-claims, OpenTag main versus managed snapshot.

**Builder artifact:** build-versus-buy decision record with data, security, integration, and operations ownership.

**Screenshot:** L3-13 and authorized L3-14 only.

**Chapter action:** choose a deployment model and list every control still owned by the application team.

### Chapter 22 — Operating organizational agents

**Core teaching:** staged rollout, SLOs, spend, incident response, revocation, deletion, and decommission.

**Evidence to use:** rollout ladder, metrics, operational controls, failure modes.

**Builder artifact:** production readiness scorecard and game-day script.

**Screenshot:** L3-12 plus one failure/recovery timeline.

**Chapter action:** run a duplicate-event, wrong-approver, revoked-credential, and process-restart game day before enabling writes.

## Unresolved publication decisions

These require the author or an updated runtime capture; do not fill them by inference.

1. **Canonical companion repository URL and folder layout.** The user intends a repository tied to the book, but the exact name and `apps/` organization are still blank.
2. **Canonical Level 1 project.** The personal financial ledger is a candidate; the final project determines which organizational workflow delegates into it.
3. **Level 3 end-to-end use case.** Recommended: a product/finance operations request that begins in Slack, reads approved records, proposes a reversible change, obtains a bound approval, and delegates a repository analysis to a machine worker.
4. **CopilotKit Intelligence availability at layout freeze.** Recheck official docs, product access, regions, adapters, API names, and service ownership.
5. **OpenTag release line.** Decide whether the book pins the older `main`, a tagged release, or a newer commit with current package names. Never splice them invisibly.
6. **Claude Tag availability and collaboration surfaces.** Recheck immediately before publication because it is a public beta and product surface is moving quickly; do not infer a named roadmap.
7. **Teams reference capture credentials.** A real tenant, Entra app, Azure Bot, consent, and safe synthetic SharePoint files are required for trustworthy screenshots.
8. **Durable StateStore backend.** Select Postgres/Redis or another production backend and document atomicity expectations for locks, dedup, queues, and approval records.
9. **Policy engine.** Decide whether the sample uses application code, Cedar, OPA, or another engine. Keep the conceptual policy independent of the implementation.
10. **Audit backend.** Choose an implementation that can honestly support the book's integrity and retention claims.
11. **Approval risk taxonomy.** Define thresholds for read, reversible write, external communication, financial action, code merge, and deployment.
12. **Institutional-memory reviewer.** Define whether memory promotion is owner-only, role-based, or policy-automated for low-risk facts.
13. **Machine worker.** Confirm the Hermes/CopilotKit project revision and which sandbox, filesystem, command, network, and credential controls are actually demonstrable.
14. **Screenshot license and product access.** Confirm that every third-party admin/product image is captured under permitted access and can be published.

## Official source registry

Accessed 2026-07-14. Repository links are immutable; documentation links are live and must be rechecked at publication freeze.

### CopilotKit and OpenTag

- [CopilotKit pinned monorepo](https://github.com/CopilotKit/CopilotKit/tree/855446e1abc8f29756dc5e539e5e50a90321ac2d)
- [Channels core package](https://github.com/CopilotKit/CopilotKit/tree/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels)
- [Channels UI package](https://github.com/CopilotKit/CopilotKit/tree/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels-ui)
- [Slack adapter](https://github.com/CopilotKit/CopilotKit/tree/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels-slack)
- [Discord adapter](https://github.com/CopilotKit/CopilotKit/tree/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels-discord)
- [Teams adapter](https://github.com/CopilotKit/CopilotKit/tree/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels-teams)
- [Channels reference](https://docs.copilotkit.ai/reference/channels)
- [LangGraph channels guide](https://docs.copilotkit.ai/langgraph-python/channels)
- [Slack guide](https://docs.copilotkit.ai/slack)
- [Teams guide](https://docs.copilotkit.ai/teams)
- [OpenTag pinned main](https://github.com/CopilotKit/OpenTag/tree/df93bc0dccd0afc8eb7bb02206ffbe2ef7922322)
- [OpenTag managed-development snapshot](https://github.com/CopilotKit/OpenTag/tree/d6a807783136a9e0b6a610f16648df8f1980cdbc)

### Claude Tag

- [Introducing Claude Tag, June 23, 2026](https://www.anthropic.com/news/introducing-claude-tag)
- [Claude Tag overview](https://claude.com/docs/claude-tag/overview)
- [How Claude Tag works](https://claude.com/docs/claude-tag/concepts/how-it-works)
- [Claude Tag agent identity](https://claude.com/docs/claude-tag/concepts/agent-identity)
- [Claude Tag security and data](https://claude.com/docs/claude-tag/concepts/security-and-data)
- [Claude Tag settings map](https://claude.com/docs/claude-tag/concepts/settings-map)
- [Claude Tag memory](https://claude.com/docs/claude-tag/users/memory)
- [Claude Tag product page](https://claude.com/product/tag)
- [Agent identity and access model](https://claude.com/blog/agent-identity-access-model)

### Channel platforms

- [Slack Socket Mode](https://api.slack.com/apis/connections/socket)
- [Slack Events API](https://api.slack.com/apis/connections/events-api)
- [Slack request verification](https://docs.slack.dev/authentication/verifying-requests-from-slack/)
- [Discord Gateway and intents](https://docs.discord.com/developers/events/gateway)
- [Discord interactions](https://docs.discord.com/developers/interactions/receiving-and-responding)
- [Microsoft Teams bot authentication and setup](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/authentication/add-authentication)
- [Teams resource-specific consent](https://learn.microsoft.com/en-us/microsoftteams/platform/graph-api/rsc/resource-specific-consent)
- [Teams channel messages with RSC](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/conversations/channel-messages-with-rsc)

### Standards and security

- [NIST SP 800-162 — ABAC](https://csrc.nist.gov/pubs/sp/800/162/upd2/final)
- [NIST SP 800-207 — Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
- [RFC 8693 — OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693)
- [OWASP Top 10 for Agentic Applications](https://owasp.org/www-project-top-10-for-agentic-applications/)

## Drafting handoff checklist

- [ ] Preserve D/S/R/EA/A labels in chapter notes.
- [ ] Treat the pinned repositories as the code truth for excerpts.
- [ ] Recheck live documentation at publication freeze.
- [ ] Lead each chapter with a concrete organizational failure or decision, then teach the control.
- [ ] Include one build artifact and one verification exercise per chapter.
- [ ] Pair every happy-path screenshot with a failure, rejection, or recovery state.
- [ ] Explain platform scopes and application authorization as separate layers.
- [ ] Annotate sender context and identity correlation as non-authorization.
- [ ] Follow every upstream confirmation example with the production approval delta.
- [ ] Keep OpenTag main, OpenTag managed-development, direct Channels, CopilotKit Intelligence, and Claude Tag availability distinct.
- [ ] Do not claim runtime verification for the six existing OpenTag frames.
- [ ] Do not claim generally available managed service without current official proof.
- [ ] Do not use “institutional memory” for raw transcripts.
- [ ] Require exact provenance for Level 3-to-Level 2 delegated artifacts.
- [ ] Resolve every publication blank in the unresolved decisions section before final manuscript lock.

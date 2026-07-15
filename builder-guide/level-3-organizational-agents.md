# Level 3 — Organizational agents

Level 3 agents join shared organizational systems such as Slack, Teams, and Discord. A channel message is only the entry point; the surrounding system must establish who asked, who acts, what data may be used, who may approve, what persists, and how work is audited.

## Read

1. [When the agent joins the team](../book-components/sections/04-level-3/17-when-the-agent-joins-the-team.md)
2. [One agent, many channels](../book-components/sections/04-level-3/18-one-agent-many-channels.md)
3. [Who asked, who acts, who approves](../book-components/sections/04-level-3/19-who-asked-who-acts-who-approves.md)
4. [Delegation without ambient authority](../book-components/sections/04-level-3/20-delegation-without-ambient-authority.md)
5. [Managed, open, and in between](../book-components/sections/04-level-3/21-managed-open-and-in-between.md)
6. [Operate the organizational actor](../book-components/sections/04-level-3/22-operate-the-organizational-actor.md)

## Inspect and run

- [`channels-bot.ts`](../companion/src/level-3/channels-bot.ts) — channel-neutral message and action boundary.
- [`governed-action.ts`](../companion/src/level-3/governed-action.ts) — requester, actor, approver, proposal digest, and replay controls.
- [`governed-action.test.ts`](../companion/tests/governed-action.test.ts) — executable governance cases.

## Builder checklist

- Preserve stable requester, channel, thread, tenant, and agent-service identifiers.
- Intersect organization, workspace, agent, channel, task, and requester policy; lower scopes may narrow authority, never expand it.
- Keep requester identity, service identity, and approver identity distinct.
- Delegate to Level 2 through a bounded task envelope, not ambient machine access.
- Promote memory deliberately with provenance, retention, and deletion rules.
- Treat channel UI as a projection of durable action and audit records.

## Reference implementations

Study the pinned [CopilotKit Channels packages](../reference-projects/README.md#copilotkit-channels) for adapters and the pinned [OpenTag](../reference-projects/README.md#opentag) application for a self-hosted channel-agent case study.

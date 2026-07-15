---
chapter: 17
title: When the Agent Joins the Team
plan_title: From Assistant to Organizational Actor
part: Level 3
target_words: 1900
target_pages: 9
status: ready-to-draft
---

# Chapter 17 — When the Agent Joins the Team

## Hook

A teammate asks a Slack agent to open a record they cannot access directly. The bot can see the message and the agent service account can see the record. Who is the system acting for?

## Reader outcome

Distinguish a channel bot, channel agent, and governed organizational actor, then map the identities and authority required for shared work.

## Core claims

- Moving an interface into Slack or Teams does not automatically create an organizational agent.
- A governed actor adds explicit agent identity, requester context, policy, approvals, memory governance, audit, and operational ownership.
- Preserve three identities: who asked, which agent acted, and which system accepted the action.
- Collaboration channels add social context, not business authorization.
- Shared service identity creates a confused-deputy risk that must be designed deliberately.

## Code, figure, and table inventory

- **Table:** channel bot vs channel agent vs governed actor.
- **Figure:** organization policy → workspace → channel → thread → user request.
- **Sequence:** requester, agent principal, policy enforcement point, target system.
- **Artifact:** organizational authority map and maturity test.

## Canonical evidence

- Level 3 packet taxonomy, maturity test, executive findings, Claude Tag identity model.
- `authoring/terminology.md` channel and principal definitions.

## Exercise

Classify an existing channel integration. Name agent identity, invokers, resources, credential mode, approval rules, memory, audit owner, kill switch, and decommission path. List what prevents calling it governed today.

## Failure and security section

Cover confused deputy, low-trust channel invoking high-trust service identity, ambient context leakage, bot identity confused with requester identity, and unowned retained memory.

## Production checklist

- [ ] Requester/agent/target identities preserved.
- [ ] Invocation and resource policy external to model.
- [ ] Channel and tenant scope explicit.
- [ ] Approvals and memory have owners.
- [ ] Stop/revoke/decommission paths documented.

## Quotable line target

> The organizational threshold is crossed when authority becomes shared, durable, and accountable—not when the agent gets a Slack avatar.

## Bridge

Chapter 18 builds the channel/runtime boundary and shows what Channels and OpenTag provide—and what they intentionally leave to the application.

## Budget

1,900 prose words; 9 pages; taxonomy and identity visual heavy.

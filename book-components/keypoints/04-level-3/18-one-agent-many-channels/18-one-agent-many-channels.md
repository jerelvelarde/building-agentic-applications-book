---
chapter: 18
title: One Agent, Many Channels
plan_title: Channels SDK and OpenTag
part: Level 3
target_words: 2200
target_pages: 10
status: implementation-gated
---

# Chapter 18 — One Agent, Many Channels

## Hook

Render one semantic approval in Slack, Discord, and Teams. The intent is shared; acknowledgement deadlines, modals, files, identity lookup, ephemeral output, and native components differ.

## Reader outcome

Connect a self-hosted agent to one channel using current Channels packages, then reason about state, platform capabilities, and direct-versus-managed responsibilities.

## Core claims

- Channels normalizes ingress, agent runs, semantic UI, actions, state, identity correlation, transcripts, locks, dedup, and queues; it does not supply organizational authorization.
- `@copilotkit/channels-ui` creates semantic IR, not React DOM or pixel parity.
- Platform adapter capabilities and deployment/security models differ; test declared fallbacks.
- Event dedup, duplicate runs, and duplicate external side effects are distinct problems.
- Use CopilotKit `examples/slack` for current code; OpenTag main is a case study with older package names; managed direction remains availability-gated.

## Code, figure, and table inventory

- **Code:** `createBot`, durable store config, semantic component, direct adapter wiring.
- **Figure:** platform event → adapter → lock/dedup/identity → agent → semantic UI → platform.
- **Table:** Slack/Discord/Teams capabilities and deployment knobs.
- **Screenshots:** mention, structured response, same artifact across verified adapters, direct-vs-managed topology.

## Canonical evidence

- Level 3 packet package map, runtime path, store/thread/UI sections, adapter realities, OpenTag truth.
- Pinned CopilotKit `examples/slack` and OpenTag revisions.

## Exercise

Connect one self-hosted agent to Slack with minimum scopes, a persistent store, mention-only invocation, dedup key, and one semantic component. Record the exact package versions and run ID.

## Failure and security section

Cover unsigned HTTP ingress, delayed acknowledgement/retries, non-durable in-memory store, lock conflict behavior, inline action handlers lost after restart, and platform scopes confused with app authorization.

## Production checklist

- [ ] Exact adapter ran and was captured.
- [ ] Ingress verified and acknowledged quickly.
- [ ] Durable tenant-partitioned store.
- [ ] Locks/dedup/failure policy documented.
- [ ] Platform scopes minimized.
- [ ] Unsupported UI has tested fallback.
- [ ] Managed availability claims refreshed.

## Quotable line target

> Channel-neutral semantics let one agent travel; platform capabilities and organizational policy determine how safely it arrives.

## Bridge

The agent can receive and render work. Chapter 19 decides whose authority it may use and who may approve consequence.

## Budget

2,200 prose words; 10 pages; code and cross-platform screenshots.

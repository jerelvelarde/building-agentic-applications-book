---
title: "Part IV — Level 3: Organizational Agents"
part: "Level 3 — Organizational Agents"
status: review-draft
updated: 2026-07-15
---

# Part IV — Level 3: Organizational Agents

Level 2 ended with a bounded machine worker: a narrow task arrives, the worker operates inside an enforced authority envelope, and it returns evidence. That design becomes more important when the request begins in a shared channel.

Imagine a product manager writing:

> @OperationsAgent investigate the onboarding regression, ask the repository worker to inspect last week's releases, and prepare a ticket if you find a likely cause.

The message looks simple. The authority chain is not.

The channel identifies a sender, but that person may not be allowed to see raw customer events. The agent has its own service identity, but it should not spend that identity as ambient authority. The repository worker runs somewhere else under another policy. A ticket is an organizational record, not just rendered text. A teammate clicking **Approve** may or may not be an eligible approver. The conversation may be retained longer than the source data it summarizes.

Level 3 begins where agency becomes shared, durable, and accountable across an organization. The agent is no longer only inside one application or under one machine operator. It participates in team conversations, uses organizational systems, delegates work, remembers selected context, and can continue when the original requester is offline.

![A shared-channel request surrounded by callouts for requester access, agent identity, delegated machine work, target authority, approver eligibility, and independent retention.](../../images/diagrams/fig-level3-01-message-authority-anatomy.svg)

*Figure IV.1 — A short channel message is only the entry point to a longer identity, delegation, approval, and retention chain.*

This part builds that actor from the outside in.

Chapter 17 separates a channel bot, a channel agent, and a governed organizational actor. Chapter 18 connects one semantic agent application to Slack, Discord, and Microsoft Teams through the current CopilotKit Channels packages, while keeping platform capability differences visible. Chapter 19 preserves who asked, which principal acts, who may approve, and what exact action they approved. Chapter 20 hands work to the Level 2 worker through a signed, expiring task envelope instead of forwarding a transcript and broad credentials. Chapter 21 compares direct, open, managed, and hybrid operating models without confusing hosting with governance. Chapter 22 turns the architecture into a staged rollout, operating model, incident path, and decommission plan. **Verified July 2026.**

The examples use synthetic users, tenants, records, and credentials. CopilotKit Channels and OpenTag implementation claims are tied to pinned source revisions. Claude Tag and CopilotKit managed-service claims are dated because availability and platform coverage can change. Reference-only OpenTag demo frames are not presented as fresh runtime evidence. **Verified July 2026.**

The goal is not to make a bot sound like a teammate. It is to build a shared actor whose authority can be explained before an action, enforced during it, and reconstructed afterward.

---
chapter: 1
title: Three Surfaces of Agency
plan_title: The Three Levels of Agentic Applications
part: Foundations
target_words: 1800
target_pages: 8
status: ready-to-draft
---

# Chapter 1 — Three Surfaces of Agency

## Hook

Open on one goal—“investigate the onboarding drop”—expressed three ways: inside a product dashboard, inside a repository workspace, and in a shared Slack channel. The words barely change; the context, authority, users, and blast radius change completely.

## Reader outcome

Classify a system as Level 1, 2, or 3 by operating surface, authority, and control requirements, then identify when levels compose.

## Core claims

- The levels are independent surfaces, not a maturity ladder.
- The useful distinction is what the system can reach and change: application objects, machine environment, or shared organizational systems.
- Each authority expansion requires stronger identity, isolation, supervision, provenance, and recovery.
- One workflow may cross levels, but requester and policy context must survive every handoff.

## Code, figure, and table inventory

- **Figure:** three surfaces with increasing authority and blast radius; reader question: “Where does the agent operate?”
- **Sequence:** Slack request → governed organizational run → bounded machine task → application status UI.
- **Table:** surface, context, tools, user model, risk, controls, CopilotKit role, runtime role.
- **Screenshots:** one evidence-labeled reference frame per canonical level; do not present reference-only images as runtime proof.

## Canonical evidence

- `reference-projects/README.md`; `materials/evidence-packets/level-1-foundations.md`.
- `materials/evidence-packets/level-1-foundations.md`, sections 1–4.
- Level 2 packet executive findings and Chapter 11 boundaries.
- Level 3 packet taxonomy and maturity test.

## Exercise

Choose one agent product. Fill an authority map: surface, default context, reachable resources, acting identity, side effects, human controls, and recovery. Name the smallest sufficient level.

## Failure and security section

Show two classification errors: calling a chat UI agentic without an adaptive loop, and calling a Slack bot organizational without enforceable identity/policy. Explain that higher level does not mean better architecture.

## Production checklist

- [ ] Operating surface and authority stated.
- [ ] Acting/requesting identities named.
- [ ] Side effects and blast radius mapped.
- [ ] Cross-level handoffs preserve policy and provenance.
- [ ] Smallest sufficient level justified.

## Quotable line target

> The level is defined less by how smart the agent sounds than by what the surrounding system allows it to change.

## Bridge

With the surfaces clear, Chapter 2 defines when software is actually acting as an agent rather than wearing an agent-shaped interface.

## Budget

1,800 prose words; 8 designed pages; approximately 35% figures/tables.

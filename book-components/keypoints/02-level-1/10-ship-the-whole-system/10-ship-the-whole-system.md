---
chapter: 10
title: Ship the Whole System
plan_title: Shipping the Application Agent
part: Level 1
target_words: 2000
target_pages: 10
status: ready-to-draft
---

# Chapter 10 — Ship the Whole System

## Hook

The demo passes on localhost, but production adds multiple users, stale mobile clients, reconnects, rate limits, model drift, retained traces, and real incidents. Shipping changes the problem.

## Reader outcome

Deploy and operate the Level 1 application with explicit identity, persistence, evaluation, reliability, version, and release controls.

## Core claims

- Production readiness is the demonstrated behavior of the whole system.
- Authentication and tenant scope must reach tools, threads, state, traces, and artifacts.
- Web/mobile clients need documented lifecycle, reconnect, offline, and version behavior.
- Model, package, prompt, schema, and companion versions belong in one compatibility register.
- Evals and monitoring must cover the path, not just final response quality.

## Code, figure, and table inventory

- **Architecture:** web/mobile → authenticated AG-UI gateway → runtime/workers → product services → persistence/audit/LangSmith.
- **Code/config:** auth-scoped thread, rate/step/cost budgets, trace redaction, clean-install scripts.
- **Table:** knobs and production failure signals.
- **Deliverable:** Level 1 production-readiness worksheet.

## Canonical evidence

- Level 1 packet sections 15–16, acceptance suite, status matrix, and release protocol.
- Capture notes for actual run limitations.
- `authoring/code-and-screenshot-policy.md`.

## Exercise

Run the Level 1 scenario suite from a clean environment: read, propose, edit/approve, reject, timeout/retry, reconnect, cancel, tenant isolation, malicious render, and mobile background/resume.

## Failure and security section

Cover cross-tenant thread access, duplicate writes after timeout, provider fallback drift, PII in traces, expired mobile auth, and a successful shell with unreachable runtime.

## Production checklist

- [ ] Clean install/build/test/run documented.
- [ ] Auth and tenant isolation adversarially tested.
- [ ] Durable state and retention owned.
- [ ] Budget, SLO, alerts, and redaction configured.
- [ ] Snippets/screenshots tied to release tag.
- [ ] License and synthetic-data review complete.

## Quotable line target

> You do not ship an agent when the chat works; you ship it when identity, state, side effects, and recovery work together under failure.

## Bridge

Level 1 deliberately exposes app-scoped tools. Part III asks what changes when the tool surface becomes the machine itself.

## Budget

2,000 prose words; 10 pages; checklist and topology heavy.

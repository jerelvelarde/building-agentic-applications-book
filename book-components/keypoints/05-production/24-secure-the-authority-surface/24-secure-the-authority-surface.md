---
chapter: 24
title: Secure the Authority Surface
plan_title: Security by Authority Level
part: Production
target_words: 2400
target_pages: 12
status: ready-to-draft
---

# Chapter 24 — Secure the Authority Surface

## Hook

Use one hostile instruction across the levels: in Level 1 it targets a record, in Level 2 a machine and credentials, in Level 3 a shared identity and delegated workers. The text is the same; authority determines impact.

## Reader outcome

Threat-model an agent by inputs, identities, tools, trust zones, memory, delegation, and side effects, then convert risk labels into enforcement points and adversarial tests.

## Core claims

- Security is authority design: tools, identities, runtimes, and policy determine what can happen.
- Least agency—fewer autonomous decisions, tools, context, duration, and handoffs—is stronger than privilege reduction alone.
- OWASP ASI01–ASI10 is a threat taxonomy, not a deployable control set.
- Instructions, data, and authority must remain separate.
- Tool manifests, approval records, short-lived credentials, memory governance, sandboxing, supply-chain provenance, and action ledgers require real enforcement.
- Security controls expand from tenant/app boundaries to machine isolation to organizational actor chains.

## Code, figure, and table inventory

- **Table:** ASI risks → concrete failure → controls → evaluation.
- **Figure:** authority gradient and level-specific trust zones.
- **Code/schema:** enforced tool risk manifest; four-principal Level 3 identity chain.
- **Figure:** instruction/data/authority separation and sandbox layers.

## Canonical evidence

- Production evidence packet Chapter 24.
- OWASP Agentic Top 10/Skills Top 10 and NIST sources cited there.
- Level-specific threat registers in all three evidence packets.

## Exercise

Choose one tool per level. Identify untrusted inputs, actor chain, resource, credential, enforcement point, detection, response, recovery, owner, and a failing adversarial test. Remove one unnecessary agency surface.

## Failure and security section

The whole chapter is the section: cross-tenant reads, shell/code execution, skill supply chain, memory poisoning, insecure delegation, cascading retries, misleading approval, rogue persistence, and kill/revoke failure.

## Production checklist

- [ ] Threat model and trust zones explicit.
- [ ] Deny-by-default policy outside prompts.
- [ ] Target-bound authorization tested.
- [ ] Secrets scoped/revocable and absent from model context.
- [ ] Memory governed and deletable.
- [ ] Worker containment and action ledger verified.
- [ ] Kill/revoke drills runtime-observed.

## Quotable line target

> Secure agents by minimizing what may decide, what may act, and how long that authority survives.

## Bridge

Even a secure design can fail under load, delay, retries, or cost pressure. Chapter 25 makes those resource policies explicit.

## Budget

2,400 prose words; 12 pages; threat-model matrix heavy.

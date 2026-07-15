---
chapter: 19
title: Who Asked, Who Acts, Who Approves
plan_title: Identity, Policy, and Organizational Context
part: Level 3
target_words: 2400
target_pages: 11
status: implementation-gated
---

# Chapter 19 — Who Asked, Who Acts, Who Approves

## Hook

A confirmation card says “Approved,” but the click came from the wrong user, arguments changed after rendering, and the bot's service account still had permission. Interaction succeeded; governance failed.

## Reader outcome

Implement a policy enforcement point that separates platform sender, application principal, agent identity, delegated credentials, and eligible approver.

## Core claims

- Identity resolution and sender context are not authorization.
- Preserve requester, agent service principal, tenant/workspace/channel, policy profile, action, target, credential mode, and risk.
- Combine RBAC for understandable roles with ABAC for contextual resource/action decisions.
- Agent identity and on-behalf-of requester access are distinct credential modes.
- Approval must be a persisted proposal bound to canonical arguments, eligible principal, policy version, expiry, quorum, and idempotency key.
- Reauthorize immediately before execution.

## Code, figure, and table inventory

- **Schema:** approval proposal record and status machine.
- **Policy:** agent ∧ channel ∧ requester ∧ environment ∧ approval.
- **Sequence:** propose → canonicalize/persist → render opaque reference → authenticate click → authorize/quorum → reauthorize → execute idempotently → audit.
- **Screenshots:** exact proposal, wrong-user rejection, two-person quorum.

## Canonical evidence

- Level 3 packet approval record, identity/policy model, NIST ABAC/Zero Trust, RFC 8693, current confirmation-tool gap.

## Exercise

Upgrade a confirmation tool. Test wrong user, requester forbidden by separation-of-duties, double click, simultaneous approvers, changed arguments, expiry, role revocation, process restart, and downstream success before local status update.

## Failure and security section

The tests are the section: prompt-based authorization, opaque action ID treated as token, stale approval, replay/race, broad service identity, and lost actor chain.

## Production checklist

- [ ] Trusted identity mapping.
- [ ] Policy outside model and UI.
- [ ] Proposal canonicalized/persisted before display.
- [ ] Eligibility, expiry, quorum, replay enforced.
- [ ] Credential mode visible/audited.
- [ ] Reauthorization and idempotency at execution.

## Quotable line target

> Context tells the model who is speaking; authorization tells the system what that person may cause to happen.

## Bridge

Chapter 20 carries the identity and policy envelope into memory and delegated machine work without ambient authority.

## Budget

2,400 prose words; 11 pages; policy and sequence dense.

---
chapter: 13
title: Draw the Blast Radius
plan_title: Access, Restrictions, and Dedicated Machines
part: Level 2
target_words: 2700
target_pages: 12
status: ready-to-draft
---

# Chapter 13 — Draw the Blast Radius

## Hook

An agent with an “allowed path” reads an out-of-root secret through an in-root symlink, then sends it to an allowed domain. Every individual control appears configured; the combined path remains open.

## Reader outcome

Write and test an explicit machine policy for paths, commands, network, credentials, approvals, isolation, and recovery.

## Core claims

- Scope permissions across read, local write, external write, and destructive effects—not one global access switch.
- Canonical paths and symlink handling matter, but application checks do not replace OS isolation.
- Broker short-lived credentials per tool; never blanket-inherit personal or admin secrets.
- Network policy is part of the data boundary; broad domains and privileged sockets can collapse containment.
- Worktrees, OS sandboxes, containers, VMs, and dedicated hosts solve different problems.
- Recovery design—discard, restore, revert, compensate—must precede increased autonomy.

## Code, figure, and table inventory

- **Policy file:** roots, tools, argv constraints, network/methods, credential leases, approval class, isolation profile.
- **Code:** canonical existing-path resolution with limitations annotated.
- **Table:** worktree vs sandbox vs container vs VM vs dedicated host.
- **Threat model:** symlink, traversal, package scripts, skill poisoning, socket access, exfiltration.

## Canonical evidence

- Level 2 packet Chapter 13 and pinned Hermes path helpers/demonstration routes.
- First-party Claude Code sandbox, Hermes security/backends, OpenClaw sandbox/policy docs cited there.

## Exercise

Create adversarial fixtures for symlink escape, `..`, package lifecycle script, poisoned skill, allowed interpreter misuse, metadata endpoint, container socket, and data exfiltration. Capture one real denial per class.

## Failure and security section

This chapter is the security section: explicitly show check-then-open race, terminal bypass, broad egress, credential inheritance, privileged container mode, persistent agent state, and dedicated-machine misconceptions.

## Production checklist

- [ ] Realpath/no-follow behavior tested.
- [ ] Command identity and arguments constrained.
- [ ] Default-deny egress and socket policy.
- [ ] Short-lived scoped credential broker.
- [ ] Non-admin/disposable execution profile.
- [ ] Restore/revert/compensation tested.
- [ ] Kill/revoke/rebuild path owned.

## Quotable line target

> Least privilege is not one permission setting; it is the intersection of identity, tool policy, process isolation, network reach, and time.

## Bridge

With the evaluation dimensions clear, Chapter 14 compares real harnesses without flattening their different operating models.

## Budget

2,700 prose words; 12 pages; policy and adversarial evidence heavy.

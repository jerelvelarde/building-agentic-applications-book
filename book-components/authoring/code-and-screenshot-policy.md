---
title: Code and Screenshot Policy
status: active-drafting
updated: 2026-07-14
---

# Code and screenshot policy

Code teaches how. Screenshots prove a visible state. Neither is decoration.

## Printed code contract

Every printed snippet must:

- answer one engineering question;
- come from a real source file in a pinned repository or clearly say `Conceptual`;
- compile, run, or be imported by a test in the companion release before final review;
- stay between 8 and 30 lines unless the reader needs the full boundary;
- include only the lines needed for the decision;
- show expected output, UI state, or verification where consequential;
- omit secrets, real financial data, private workspace data, and unnecessary boilerplate;
- preserve license notices and attribution requirements.

Required metadata:

```yaml
snippet_id: L1-06
chapter: 6
source_file: apps/ledger/src/tools/read-spending.ts
source_ref: <immutable SHA or book release tag>
package_versions:
  "@copilotkit/react-core": <exact>
verified_on: 2026-XX-XX
verification_command: <exact command>
test_file: <exact path>
evidence: R
```

## Code selection rules

- Prefer one meaningful diff over a complete file.
- Use TypeScript/React/Next.js for canonical frontend code, bare React Native for the audited mobile path, and Python/LangGraph where durable orchestration is the lesson.
- Label platform imports and version differences explicitly.
- Use current `@copilotkit/channels*` names for new Level 3 code; show older `@copilotkit/bot*` only in a migration sidebar.
- Keep policy and security invariants outside prompts.
- Put privileged writes, secrets, identity derivation, and tenant checks behind a trusted server boundary.
- Show failure behavior for tool calls, persistence, approvals, and external writes.
- Do not use a type declaration as proof that policy is enforced.

## Screenshot contract

Every screenshot needs:

- figure ID in the form `FIG-CHNN-NN`;
- filename `fig-chNN-NN-short-slug.png`;
- source repository and immutable commit;
- exact capture command or runbook;
- synthetic fixture name;
- platform, device/viewport, theme, and scale;
- capture timestamp;
- scenario test or trace reference;
- redaction record;
- alt text;
- caption stating what to notice and why it matters;
- evidence status `R` before it is called proof.

Example record:

```yaml
figure_id: FIG-CH09-03
source_ref: <immutable SHA>
seed_fixture: synthetic-ledger-v1
platform: ios
device: iPhone 16 simulator
command: <exact command>
scenario_test: <path or test ID>
captured_at: <ISO timestamp>
redactions: none
alt_text: An approval card shows the exact account, amount, source, and edit/reject/approve actions.
lesson: Approval must bind a human decision to an exact proposal.
evidence: R
```

## Required screenshot families

Across the book, capture:

1. Empty or goal-entry state.
2. Streaming/in-progress state with truthful progress.
3. Tool arguments and structured result.
4. Shared-state edit or conflict.
5. Approval before consequence.
6. Rejection, wrong-user, or policy-denied state.
7. Failure and recovery.
8. Machine plan, command, diff, and test evidence.
9. Channel-native structured response and follow-up.
10. Trace/evaluation view aligned to the visible product state.

Pair happy-path screenshots with a failure, rejection, or recovery state. A polished success screen alone cannot teach supervision.

## Capture safety

- Use only synthetic users, organizations, channels, ledgers, receipts, repositories, records, and credentials.
- Never show real balances, emails, customer data, tenant IDs, API keys, tokens, hostnames, local network addresses, or private traces.
- Verify that browser and channel chrome do not reveal personal accounts.
- Do not use marketing images as runtime proof.
- Do not imply a shell, adapter, simulator, or external tool ran when only the application shell was available.
- Confirm third-party product screenshot rights and required attribution.
- Refer to the private web/PWA case study only as **GTM Operations Workspace**. Do not expose its repository name, owner, URL, checkout path, or private revision.
- Anonymize visible repository URLs/names, usernames, organizations/workspaces, branch names that reveal private context, hostnames, tenant IDs, local paths, emails, and private records before publication.
- Prefer anonymization in the synthetic fixture or capture environment. Record any post-capture redaction precisely in the screenshot sidecar.

## Accessibility and print quality

- Text must remain legible at the final 7 × 10 inch trim size.
- Use callout crops when full-window screenshots make code or UI unreadable.
- Status cannot rely on color alone.
- Charts need textual summaries and accessible source data.
- Alt text explains the interaction and builder lesson, not decorative colors.
- Use a consistent light/dark treatment and viewport family within a chapter.
- Do not annotate screenshots so heavily that the original UI becomes ambiguous.

## Current asset status

The finance simulator images and extracted OpenTag demo frames under `images/repository-captures/` are **reference-only**. They may guide composition and chapter planning. They must not be captioned as fresh runtime proof unless recaptured under the rules above.

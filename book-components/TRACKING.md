# Book improvement tracker

This is the only public work tracker for the book. It records durable next improvements without exposing internal prompts, schedules, or agent-production residue.

## Current artifact

| Area | State | Next proof |
| --- | --- | --- |
| Manuscript | First Draft; 26 chapters | Editorial pass for clarity, repetition, and citation placement |
| Companion code | TypeScript and Python boundaries implemented and tested | Add a complete browser/mobile reference app when the canonical use case is locked |
| Diagrams | Editable source, registry, validator, and 97 embedded assets | Continue page-by-page print QA as reader feedback arrives |
| Screenshots | Selected reference captures included | Replace reference-only frames with reproducible runtime captures and metadata |
| Sources | Pinned source registry and evidence packets | Reverify rolling APIs and product availability before the next edition |
| PDF | 317-page First Draft with zero recorded blocking validation findings | Rebuild after every manuscript or visual change and re-run full render QA |

## Near-term improvement queue

- [ ] Lock the canonical personal-ledger web and mobile reference experience.
- [ ] Add reproducible Level 1 screenshots for read tools, inline renderers, approval, edit, cancellation, and recovery.
- [ ] Add a governed Hermes supervision walkthrough that clearly distinguishes visibility from execution control.
- [ ] Add Channels SDK examples for Slack, Teams, and Discord with platform-specific degradation notes.
- [ ] Run citation and API-drift review against the pinned source registry.
- [ ] Add evaluation datasets for task outcome, trajectory, policy compliance, and recovery behavior.
- [ ] Perform accessibility, print contrast, overflow, and arrow-path QA for every updated figure.

## Definition of ready for the next draft

- Every new factual claim maps to a source and evidence status.
- Every printed code sample compiles or is explicitly labeled illustrative.
- Every screenshot has a reproducible flow, synthetic data, redaction review, and capture metadata.
- Every diagram passes the source validator and rendered-page inspection.
- Companion checks, manuscript lint, diagram validation, PDF build, and PDF validation are green.

Local prompts belong in `book-components/prompts/`, which is git-ignored.

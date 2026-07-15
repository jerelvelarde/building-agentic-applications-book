---
title: Page and Word Allocation
status: active-drafting
updated: 2026-07-15
design_target_pages: 297
manuscript_target_words: 64400
---

# Page and word allocation

The target is a highly actionable **250–300-page** field guide. The current design target is **297 pages** and approximately **64,400 words**, including front and back matter. Page budgets include code, figures, tables, and callouts; word targets count prose only unless noted.

## Allocation by chapter

| Chapter | Working title | Part | Target prose words | Target pages | Visual/code density |
|---:|---|---|---:|---:|---|
| 1 | Three Surfaces of Agency | Foundations | 1,800 | 8 | High diagram/table |
| 2 | When Software Starts Choosing | Foundations | 1,900 | 8 | Medium code/diagram |
| 3 | Open the Hood | Foundations | 2,200 | 10 | High architecture |
| 4 | The Interface Is the Control Plane | Foundations | 1,900 | 10 | High UI sequence |
| 5 | Inside the Application Agent | Level 1 | 2,100 | 10 | High code/screenshot |
| 6 | Put the Tool in the Right Place | Level 1 | 2,400 | 10 | High code/table |
| 7 | When the Result Is an Interface | Level 1 | 2,200 | 10 | Very high screenshot |
| 8 | One State, Two Editors | Level 1 | 2,500 | 11 | High code/diagram |
| 9 | The Right Moment to Ask | Level 1 | 2,400 | 11 | High sequence/UI |
| 10 | Ship the Whole System | Level 1 | 2,000 | 10 | High checklist/architecture |
| 11 | The Machine Is the Environment | Level 2 | 2,100 | 10 | High architecture |
| 12 | The Harness Is the Product | Level 2 | 2,300 | 11 | High table/code |
| 13 | Draw the Blast Radius | Level 2 | 2,700 | 12 | High policy/threat model |
| 14 | Choose the Harness, Not the Logo | Level 2 | 2,400 | 11 | Very high comparison |
| 15 | From Visibility to Supervision | Level 2 | 2,700 | 12 | Very high code/screenshot |
| 16 | Operate the Worker | Level 2 | 2,000 | 10 | High operations/checklist |
| 17 | When the Agent Joins the Team | Level 3 | 1,900 | 9 | High taxonomy/diagram |
| 18 | One Agent, Many Channels | Level 3 | 2,200 | 10 | Very high code/screenshot |
| 19 | Who Asked, Who Acts, Who Approves | Level 3 | 2,400 | 11 | High policy/sequence |
| 20 | Delegation Without Ambient Authority | Level 3 | 2,500 | 11 | High schemas/diagram |
| 21 | Managed, Open, and In Between | Level 3 | 2,500 | 11 | Very high comparison |
| 22 | Operate the Organizational Actor | Level 3 | 2,500 | 11 | High rollout/checklist |
| 23 | Evaluate the Trajectory | Production | 2,200 | 11 | High code/metrics |
| 24 | Secure the Authority Surface | Production | 2,400 | 12 | High threat-model tables |
| 25 | Reliability Has a Budget | Production | 2,100 | 10 | High operations/tables |
| 26 | Choose the Smallest Sufficient Level | Production | 1,700 | 9 | High decision matrix |
|  | **Chapter subtotal** |  | **57,700** | **280** |  |

## Front and back matter

| Section | Target words | Target pages |
|---|---:|---:|
| Title, copyright, contents, foreword placeholder | 300 | 5 |
| Introduction and how to use the book | 2,400 | 7 |
| Part openers and transitions | 1,000 | Included in chapter/part rhythm |
| Field guide: checklists, knobs, glossary, resources | 3,500 | 15 |
| Closing | 800 | 2 |
| **Total manuscript target** | **approximately 64,400** | **approximately 297** |

## Variance rules

- Chapter prose may vary by ±12% without editorial approval.
- A chapter over target must earn the space with a runnable build, necessary failure path, or visual explanation—not background survey material.
- Code blocks count separately in the word-count report and do not justify exceeding the prose target.
- If a screenshot replaces 250–400 words of explanation, reduce prose rather than treating the figure as free space.
- Preserve the 250–300-page ceiling by cutting repetition before cutting exercises, security boundaries, or verification.
- The first review draft may be shorter. A chapter is structurally complete when every contract item exists, even if runtime screenshots remain evidence-gated.

## Validation

Run:

```bash
python3 book-components/scripts/count_words.py
```

The script reports Markdown prose and fenced-code words by section and compares numbered chapters with this table. It exits nonzero only when `--strict` is supplied and a chapter falls outside the configured tolerance.

# First Draft diagram print QA

This log tracks defects found in the embedded PDF at book scale. PDF page numbers refer to `book/agentic-applications-2026-first-draft.pdf` and may differ from the printed footer by one page.

## Corrected in source

| PDF page | Asset | Source owner | Correction |
|---:|---|---|---|
| 8 | `fig-ch01-01-three-operating-surfaces.svg` | hand-authored | Widened and centered all level chips. |
| 19 | `fig-level3-01-message-authority-anatomy.svg` | Wave 1 generator | Replaced the central arrow knot with six separate dashed leader ports. |
| 59 | `fig-ch05-00-level1-build-path.svg` | final deterministic generator | Rebuilt as a two-row serpentine path with dedicated arrow gutters. |
| 75 | `fig-ch06-03-validation-layers.svg` | hand-authored | Replaced overlapping staircase rows with seven separated narrowing gates. |
| 78 | `fig-ch06-05-capabilities-by-phase.svg` | final deterministic generator | Aligned spans to an exact five-column grid and moved approval text inside its window. |
| 100 | `fig-ch08-04-three-store-boundary.svg` | final deterministic generator | Moved connector labels and arrows into separate inter-card gutter rails. |
| 103 | `fig-ch08-03-lost-edit-race.svg` | hand-authored | Terminated the stale-work curve at a dedicated bottom-edge port. |
| 132 | `fig-ch11-03-ten-part-harness.svg` | Wave 1 generator | Wrapped the long heading and moved loop labels into gutter badges. |
| 155 | `fig-ch13-02-combined-control-exfiltration.svg` | Wave 1 generator | Routed attack connectors to edge ports and moved status copy inside bounded cards. |
| 169 | `fig-ch14-01-machine-harness-operating-models.svg` | Wave 1 generator | Wrapped long ownership lines inside their cards. |
| 181 | `fig-ch15-02-readiness-staircase.svg` | Wave 1 generator | Increased card geometry and bounded staircase copy to three lines. |
| 187 | `fig-ch15-03-supervision-broker.svg` | Wave 1 generator | Separated lane headers and placed path labels on opaque plates away from connectors. |
| 197 | `fig-ch16-02-durable-run-state-machine.svg` | Wave 1 generator | Split the terminal label from its connector into a dedicated plate. |
| 206 | `fig-level3-01-message-authority-anatomy.svg` | Wave 1 generator | Reused the corrected page 19 asset; verified the six-port leader layout in the Level 3 opener. |
| 211 | `fig-ch17-03-policy-hierarchy.svg` | final deterministic generator | Moved the narrowing arrow into the right-side gutter. |
| 213 | `fig-ch17-02-memory-promotion.svg` | Wave 1 generator | Wrapped institutional and audit copy within their cards. |
| 234 | `fig-ch19-01-identity-authority-approval.svg` | hand-authored | Routed the policy return below the Approver card through a dedicated elbow lane and edge ports. |
| 271 | `fig-ch23-00-production-control-loop.svg` | final deterministic generator | Moved the control-chain label into a dedicated footer-safe band. |
| 279 | `fig-ch23-04-severity-and-safe-task-success.svg` | final deterministic generator | Rebuilt severity tiers with wrapped examples and release actions. |
| 288 | `fig-ch24-04-agentic-supply-chain-inventory.svg` | final deterministic generator | Replaced loose checklist columns with a true 3 × 2 grid. |
| 290 | `fig-ch24-05-agent-security-incident-runbook.svg` | final deterministic generator | Wrapped phase copy and confined connectors to card gutters. |
| 293 | `fig-ch25-01-four-record-ambiguity.svg` | hand-authored | Moved all timeline event labels into a separate annotation row above the record lanes. |
| 304 | `fig-ch26-01-smallest-sufficient-level.svg` | hand-authored | Wrapped the Level 2 heading and separated the hybrid chip from the connector branch lane. |
| 316 | `fig-ch27-03-consolidated-knobs-reference.svg` | final deterministic generator | Increased card height and row spacing so descriptions remain contained. |

## Active correction batch

None.

## Queued hand-authored corrections

None.

## Release gate

Do not call the PDF final. Before handing off the current First Draft:

- [x] Regenerate code-owned SVGs.
- [x] Validate all 85 SVGs.
- [x] Rebuild the First Draft PDF after the complete correction batch.
- [x] Render every tracked page at 180 DPI.
- [x] Run the full 317-page validator and contact-sheet sweep.
- [x] Record the PDF hash and blocker count.

Last completed run: 2026-07-15. PDF SHA-256 `302fd4126d168e937f23523be6dc31ce088b8f4f007cdcd57415044ed13e1f20`; 317 pages; 0 blocking findings.

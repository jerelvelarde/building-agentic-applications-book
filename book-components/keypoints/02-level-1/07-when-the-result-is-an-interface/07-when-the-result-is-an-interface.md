---
chapter: 7
title: When the Result Is an Interface
plan_title: Generative UI and Inline Components
part: Level 1
target_words: 2200
target_pages: 10
status: ready-to-draft
---

# Chapter 7 — When the Result Is an Interface

## Hook

Put the same spending result on the page twice: first as a paragraph of numbers, then as an accessible chart, time range, source label, table, and correction action. Ask which one is the real product.

## Reader outcome

Render agent-selected semantic objects as application-owned components with complete lifecycle, accessibility, and action boundaries.

## Core claims

- Let the agent choose the semantic artifact; let the application own rendering and interaction.
- Display components, rendered backend tools, frontend tools, and approval tools have distinct execution semantics.
- Important components need partial, executing, waiting, success, rejected, failed, cancelled, and historical states.
- Mobile is not a narrow web viewport; imports, lifecycle, attachments, keyboard, and safe areas differ.

## Code, figure, and table inventory

- **Code:** `useComponent` spending chart, `useRenderTool` transaction search, safe `useDefaultRenderTool`, finance native renderer (`L1-05`–`L1-07`, `L1-11`).
- **Figure:** semantic object → registered component → platform render.
- **Screenshot grid:** streaming args, structured result, approval, historical state.
- **Table:** primitive, execution location, best fit, risk.

## Canonical evidence

- Level 1 packet sections 7 and 9, lifecycle/accessibility checklists, React Native constraints.
- Current CopilotKit v2 hook source cited in packet.
- Finance reference screenshots and capture notes for composition only.

## Exercise

Turn one text result into a registered component. Test partial arguments, empty data, malicious labels, small mobile width, keyboard focus, and a screen-reader summary.

## Failure and security section

Cover raw HTML/tool output injection, active buttons on historical cards, premature submission from partial JSON, hidden consequences on narrow screens, and color-only status.

## Production checklist

- [ ] Semantic schema versioned.
- [ ] All lifecycle states rendered.
- [ ] Execution and display boundaries distinct.
- [ ] Sensitive arguments redacted.
- [ ] Keyboard, screen reader, narrow viewport tested.
- [ ] Historical state cannot re-execute accidentally.

## Quotable line target

> Generative UI is safest when the model chooses the meaning and the application keeps control of the pixels and consequences.

## Bridge

The interface is now rich enough for both user and agent to edit the task, which creates the state-sync problem in Chapter 8.

## Budget

2,200 prose words; 10 pages; very high visual density.

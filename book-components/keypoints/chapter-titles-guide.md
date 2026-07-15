---
title: Chapter Titles Guide
status: active-drafting
updated: 2026-07-14
---

# The Builder's Guide to Agentic Applications 2026 — Chapter titles

These working editorial titles add momentum while preserving the descriptive production-plan mapping. Use the working title in reader-facing prose and the plan label in metadata until the author locks final titles.

## Part I — Foundations

| # | Working title | Production-plan label | Meaning | Teaching connection |
|---:|---|---|---|---|
| 1 | *Three Surfaces of Agency* | The Three Levels of Agentic Applications | Agency is shaped by where it operates and what it can reach. “Surfaces” avoids implying a maturity ladder. | Introduces application, machine, and organizational authority and shows how the same goal changes across them. |
| 2 | *When Software Starts Choosing* | What Makes Software Agentic? | The threshold is dynamic action selection inside a bounded loop, not a chat box or tool-call badge. | Separates model calls, workflows, assistants, and agents, then asks where adaptive judgment is justified. |
| 3 | *Open the Hood* | The Production-Grade Agent Stack | Fulfills the reader promise to expose the components hidden beneath an agent interaction. | Explodes the stack into runtime, tools, state, memory, identity, policy, interface, and operations. |
| 4 | *The Interface Is the Control Plane* | The Agentic UI Problem | The UI is where people supervise uncertainty and consequence, not merely enter prompts. | Turns streaming, editability, intervention, evidence, and recovery into product requirements. |

## Part II — Level 1: Application Agents

| # | Working title | Production-plan label | Meaning | Teaching connection |
|---:|---|---|---|---|
| 5 | *Inside the Application Agent* | The Anatomy of an In-App Agent | Opens the first real implementation and traces the full path rather than admiring the surface. | Connects mobile/web UI, CopilotKit, AG-UI, `BuiltInAgent`, services, and the optional LangGraph extension. |
| 6 | *Put the Tool in the Right Place* | Tools, Frontend Tools, and Tool Calls | Tool placement determines secrets, latency, authority, and recoverability. | Compares frontend, backend, external, rendered, and human tools through the finance example. |
| 7 | *When the Result Is an Interface* | Generative UI and Inline Components | For agentic work, the useful result may be a card, chart, editor, or approval rather than prose. | Builds semantic, registered components and complete lifecycle states across web and mobile. |
| 8 | *One State, Two Editors* | Shared State, Persistence, and the LangGraph Extension | The user and runtime can both change the same task; ownership and versions become product design. | Covers typed state, conflict handling, checkpoints, thread recovery, and memory boundaries. |
| 9 | *The Right Moment to Ask* | Human Control on Web and Mobile | Human involvement creates value only at a meaningful decision boundary with enough context. | Contrasts immediate frontend HITL with durable runtime interrupts and exact proposal approval. |
| 10 | *Ship the Whole System* | Shipping the Application Agent | Shipping the UI and model is not shipping identity, persistence, evaluation, or recovery. | Closes Level 1 with deployment, tenant safety, budgets, traces, mobile lifecycle, and a readiness gate. |

## Part III — Level 2: Machine Agents

| # | Working title | Production-plan label | Meaning | Teaching connection |
|---:|---|---|---|---|
| 11 | *The Machine Is the Environment* | The Machine as an Agent Environment | At Level 2, files, processes, network, credentials, and installed software become the tool surface. | Maps capability and blast radius across local, remote, container, VM, and dedicated-machine environments. |
| 12 | *The Harness Is the Product* | Harnesses, Skills, and Context | The differentiator is the system that prepares, constrains, and verifies the model, not the model alone. | Explains skills, context, instructions, tools, checkpoints, subagents, hooks, and verification loops. |
| 13 | *Draw the Blast Radius* | Access, Restrictions, and Dedicated Machines | Safe autonomy begins by making every reachable resource and consequence explicit. | Builds paths, command/network policy, secret isolation, sandboxing, approval tiers, and recovery. |
| 14 | *Choose the Harness, Not the Logo* | Claude Code, Hermes, and OpenClaw | Product choice should follow engineering needs and authority, not brand allegiance. | Compares dated, verified capabilities and ends with use-case-specific guidance. |
| 15 | *From Visibility to Supervision* | Supervising Hermes with CopilotKit | Showing a command after it ran is visibility; controlling whether it may run is supervision. | Uses Hermes + CopilotKit as an unsafe baseline and climbs through identity, scope, approval, isolation, and recovery. |
| 16 | *Operate the Worker* | Operating Machine Agents | Long-running machine work is a worker-fleet problem with queues, environments, budgets, and incident response. | Turns a successful demo into a repeatable operating model and game day. |

## Part IV — Level 3: Organizational Agents

| # | Working title | Production-plan label | Meaning | Teaching connection |
|---:|---|---|---|---|
| 17 | *When the Agent Joins the Team* | From Assistant to Organizational Actor | Moving into shared work systems changes identity, expectations, and accountability. | Separates bot, channel agent, and governed actor and preserves the actor chain. |
| 18 | *One Agent, Many Channels* | Channels SDK and OpenTag | A semantic agent application can cross platforms, but each platform changes capabilities and operational ownership. | Explains Channels architecture, adapters, stores, semantic UI, and OpenTag version truth. |
| 19 | *Who Asked, Who Acts, Who Approves* | Identity, Policy, and Organizational Context | These identities can differ and must remain distinct from prompt to side effect. | Builds trusted identity mapping, policy enforcement, delegated credentials, and bound approvals. |
| 20 | *Delegation Without Ambient Authority* | Delegation, Memory, and Human Governance | A handoff should transfer a narrow capability and provenance, not the entire environment's credentials and context. | Designs approval records, institutional memory, audit, and Level 3-to-Level 2 task envelopes. |
| 21 | *Managed, Open, and In Between* | Claude Tag, OpenTag, and the Organizational Landscape | Hosting is a responsibility allocation, not a binary measure of quality. | Compares direct Channels, OpenTag, managed direction, and Claude Tag without flattening availability or control ownership. |
| 22 | *Operate the Organizational Actor* | Operating Organizational Agents | A shared agent needs rollout, ownership, revocation, retention, incident response, and decommissioning. | Stages authority from synthetic/read-only through writes, delegation, memory, and scheduled work. |

## Part V — Production Engineering

| # | Working title | Production-plan label | Meaning | Teaching connection |
|---:|---|---|---|---|
| 23 | *Evaluate the Trajectory* | Evaluation That Measures the Whole System | A plausible answer can hide a wasteful, unsafe, or policy-breaking path. | Evaluates result, tools, arguments, state, intervention, latency, cost, and recovery. |
| 24 | *Secure the Authority Surface* | Security by Authority Level | Threats should be prioritized by what the agent can reach, change, remember, and delegate. | Applies a consistent threat model across application, machine, and organization levels. |
| 25 | *Reliability Has a Budget* | Reliability, Cost, and Scaling | Every run consumes time, tokens, retries, concurrency, and operational attention. | Makes SLOs, idempotency, queues, routing, caching, fallbacks, and budget limits explicit. |
| 26 | *Choose the Smallest Sufficient Level* | Choosing the Right Level | Good architecture solves the problem with the least authority and operating burden. | Synthesizes the book into a decision tree, hybrid patterns, and the reader's next build plan. |

## Title pattern

The titles move from perception to control. Foundations expose the hidden system. Level 1 titles focus on product placement and shared interaction. Level 2 titles sharpen around environment and blast radius. Level 3 titles foreground identity and delegated authority. Production titles turn those lessons into measurable discipline. Most titles are imperative or tension-driven, helping a field guide feel actionable without becoming vague or promotional.

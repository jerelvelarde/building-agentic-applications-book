---
title: "Production engineering evidence packet — evaluation, security, reliability, and architecture selection"
book: "The Builder's Guide to Agentic Applications 2026"
status: "research complete; chapter drafting not started"
owner: "Production engineering research"
accessed: "2026-07-14"
source_policy: "official documentation, standards bodies, and official repositories only"
chapters:
  - 23
  - 24
  - 25
  - 26
---

# Production Engineering — Evidence Packet

This packet is the factual and architectural source layer for Chapters 23–26 of *The Builder's Guide to Agentic Applications 2026*. It is not chapter prose. It records the current primary-source evidence, converts that evidence into buildable engineering guidance, and marks the limits of what the book's audited applications prove.

The production thesis is simple: an agent is not production-ready because it can finish a happy-path demo. It is production-ready only when the team can measure its whole trajectory, constrain every authority boundary, recover its durable state without duplicating side effects, and operate it against explicit reliability and safety objectives.

## Research frame

**Reader outcome.** After Chapters 23–26, a builder should be able to design an evaluation program, instrument agent runs without leaking sensitive context, threat-model each authority level, implement durable and idempotent execution, set cost and step budgets, define service objectives, isolate tenants, and choose the smallest agent level that can deliver the product outcome.

**Official source cutoff.** 2026-07-14. All live documentation must be rechecked when manuscript code freezes.

### Evidence labels

| Label | Meaning | Permitted manuscript wording |
|---|---|---|
| **D — documented** | Current official documentation or a standards body states the behavior or recommendation. | “The documentation supports…” |
| **S — source-present** | The implementation is visible at the pinned official or audited repository revision. It was inspected, not necessarily run. | “At the pinned commit, the source includes…” |
| **R — runtime-observed** | The behavior was reproduced in the controlled book environment and captured with run metadata. | “In our pinned reference run…” |
| **EA — early access / development** | Officially preview, alpha, waitlist, development status, concept paper, or otherwise not stable normative guidance. | Name the exact status and date. |
| **E — editorial synthesis** | Engineering guidance derived from multiple primary sources and the authority model of this book. | “We recommend…” |
| **A — aspirational** | A target capability not proven by the current reference applications. | “The hardened reference build should…” |

Do not collapse these labels. A trace is not an audit log. A checkpoint is not exactly-once execution. An approval component is not authorization. A source-present test or screenshot is not runtime proof.

## Executive findings

1. **Evaluate the trajectory, not only the final answer.** A convincing answer can hide a forbidden tool, invalid arguments, excess cost, unsafe retries, or an incorrect state transition. The production scorecard must cover final output, tool selection, arguments, state transitions, policy compliance, intervention, recovery, latency, and cost.

2. **Build an evaluation pyramid, then feed production failures back into it.** Deterministic unit and contract tests should carry most of the volume. Node and trajectory evaluations cover adaptive behavior. Simulations cover multi-turn and failure behavior. Sampled online evaluators detect drift. A confirmed production failure becomes a versioned regression case.

3. **LangSmith and OpenTelemetry solve complementary observability problems.** LangSmith models traces, runs, threads, datasets, feedback, and agent evaluators. OpenTelemetry provides vendor-neutral traces, metrics, logs, context propagation, sampling, and collectors. Correlate them; do not force either to become product state or the immutable action ledger.

4. **The OpenTelemetry GenAI semantic conventions are still marked Development.** Use a stable internal telemetry dictionary and map it to the pinned convention version at export time. Do not make a production schema depend directly on names that can still break.

5. **OWASP's 2026 Agentic Top 10 is an organizing threat model, not a deployable control set.** Each risk must be converted into a trust boundary, enforcement point, test, owner, alert, and recovery procedure. The book should use the official ASI01–ASI10 names precisely.

6. **Authority determines the security model.** Level 1 concentrates risk in application data and APIs. Level 2 adds filesystem, shell, process, credential, and network authority. Level 3 adds organizational identity, shared context, delegated authority, institutional memory, and cross-system accountability. Controls must expand with authority rather than merely with model capability.

7. **Least privilege is necessary; least agency is the stronger design default.** Remove unnecessary autonomous decisions, tools, context, duration, and delegation paths. A deterministic node or narrow read tool is safer than a general-purpose agent with a policy prompt.

8. **Durable execution does not create exactly-once side effects.** LangGraph checkpoints make state resumable. Queues may redeliver work. Processes may fail after the target system commits but before the runtime records success. Consequential tools need stable idempotency keys, an outcome ledger, and an explicit compensation or manual-recovery path.

9. **Cancellation and rollback are different operations.** Stopping a run prevents or interrupts future work. Rewinding agent state does not reverse an email, payment, database mutation, deployment, or shell command already accepted elsewhere. Every write tool needs declared cancellation and compensation semantics.

10. **Retries are a resource policy, not a reflex.** Retry only errors classified as transient, at one chosen layer, within a remaining deadline and budget, with exponential backoff and jitter. Authentication failures, invalid arguments, policy denials, and ambiguous outcomes require different flows.

11. **Cost control belongs inside the execution loop.** Model-call, tool-call, elapsed-time, depth, parallelism, output-size, egress, and monetary budgets should be enforced before every step. A dashboard after the fact is observability, not control.

12. **Agent SLOs must describe a user journey.** Time to first token is useful but insufficient. Measure acknowledgement, first useful artifact, correct terminal outcome, queue delay, resume success, and intervention latency. Treat unauthorized writes, cross-tenant reads, and secret leakage as safety invariants with zero tolerance, not ordinary error-budget events.

13. **Tenant isolation is a product architecture choice.** Pool, silo, and bridge models trade cost, operational complexity, noisy-neighbor exposure, and blast radius. Identity metadata in prompts is not isolation; enforcement must exist at storage, queue, runtime, tool, secret, and observability boundaries.

14. **Choose the smallest authority surface that can create the outcome.** A Level 1 application should not gain machine access merely because a shell is convenient. A Level 2 worker should not become a shared organizational identity merely because Slack is convenient. Compose levels with narrow task contracts when a hybrid is justified.

## Pinned reference-application truth

The production chapters must reuse the repository audit rather than imply that any current demo is already hardened.

| Reference | Pinned revision | What it proves | What remains aspirational |
|---|---|---|---|
| [`personal-finance-copilot`](https://github.com/jerelvelarde/personal-finance-copilot/tree/d8760064c626712a8fa15c192a8c4bc69bb24055) | `d8760064c626712a8fa15c192a8c4bc69bb24055` | **S:** React Native application, frontend read tools, human-in-the-loop write gates, inline results, receipt flow | Robust authentication, tenant isolation, durable LangGraph state, idempotent finance writes, production audit and recovery |
| GTM Operations Workspace | `private revision omitted` | **S:** web/PWA case study and selectable Hermes, Anthropic, and OpenAI paths | Reproducible external Hermes runtime, complete authorization, policy enforcement, production model-routing evaluation |
| [`hermes-cpk`](https://github.com/jerelvelarde/hermes-cpk/tree/fc43491368f19248ca58e1409501cd28722d0f61) | `fc43491368f19248ca58e1409501cd28722d0f61` | **S:** CopilotKit-to-Hermes seam, tracked demos/scripts/docs/skill, visible machine activity | A bundled Hermes runtime, sandbox, enforceable approvals, scoped credentials, network policy, rollback, tenant auth |
| [CopilotKit Channels](https://github.com/CopilotKit/CopilotKit/tree/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/channels) | `855446e1abc8f29756dc5e539e5e50a90321ac2d` | **S:** channel runtime, state/identity/transcript primitives, Slack/Discord/Teams adapters | Organizational authorization policy, approver binding, institutional-memory governance, immutable cross-system audit |
| [`OpenTag`](https://github.com/CopilotKit/OpenTag/tree/df93bc0dccd0afc8eb7bb02206ffbe2ef7922322) | `df93bc0dccd0afc8eb7bb02206ffbe2ef7922322` | **S:** channel agent, MCP tools, rich channel UI, blocking confirmation | Current package migration, governed actor identity, RBAC/ABAC, approval binding, machine delegation, durable audit |

The teaching pattern for every production chapter should be:

```text
working demo
  -> boundary audit
  -> explicit failure injection
  -> hardening change
  -> measured verification
  -> production gate
```

# Chapter 23 — Evaluation That Measures the Whole System

## Chapter thesis

An agent is a policy-driven state machine with probabilistic decisions and deterministic side effects. Its evaluation target is therefore the complete run: inputs, selected actions, state changes, evidence, user interventions, side effects, recovery behavior, and terminal result.

LangSmith's current evaluation model separates **offline evaluation** over datasets from **online evaluation** over production traces. Its workflow supports datasets, code evaluators, human review, LLM-as-judge evaluators, pairwise comparison, repeated experiments, sampling, and rules that can route failures into datasets or annotation queues: [evaluation overview](https://docs.langchain.com/langsmith/evaluation), [evaluation types](https://docs.langchain.com/langsmith/evaluation-types), [evaluators](https://docs.langchain.com/langsmith/evaluators), and [automation rules](https://docs.langchain.com/langsmith/rules). **D.**

## The evaluation pyramid

| Layer | Primary question | Typical method | Volume | Failure caught earliest |
|---|---|---|---:|---|
| Tool and reducer contracts | Is the deterministic boundary correct? | Unit, property, schema, permission, idempotency tests | Highest | Invalid args, authorization omissions, state merge bugs, duplicate writes |
| Node tests | Does one graph step transform state correctly? | Frozen state fixture plus stubbed model/tool | High | Routing, normalization, interrupt, retry classification, ownership errors |
| Trajectory tests | Did the agent take an acceptable path? | Exact/ordered/subset match or judged trajectory | Medium | Wrong tool, wrong order, missing approval, excess steps, forbidden delegation |
| Scenario simulations | Does the system survive a user and environment sequence? | Multi-turn personas, fault injection, clock/network/tool simulators | Lower | Recovery, cancellation, stale approval, prompt injection, concurrent edit conflict |
| Online evaluation | Is production behavior drifting or failing? | Trace sampling, rules, LLM/code evaluators, human queues | Sampled | Novel failures, provider drift, live data/tool changes, abuse patterns |

This is **E**, synthesized from LangSmith's offline/online model, AgentEvals, LangGraph testable state, and conventional software-testing economics. The pyramid is not a claim that probabilistic behavior can be made deterministic. It is a strategy for making deterministic properties cheap and reserving expensive judges for genuinely semantic questions.

## Evaluation surfaces

Every reference build needs a scorecard that evaluates more than prose quality.

| Surface | Example assertion | Best evaluator |
|---|---|---|
| Final result | Ledger total matches fixtures; cited claims are supported | Code for exact facts; calibrated LLM judge for semantics |
| Tool selection | `create_transaction` is never used for a read-only question | Code or trajectory matcher |
| Tool arguments | Amount, currency, account, tenant, and idempotency key are valid | Schema plus deterministic business rules |
| State transition | User-owned edit is preserved; status moves only through legal states | Reducer/state-machine test |
| Policy compliance | External write cannot occur without a valid approval record | Code plus audit query |
| Intervention | Interrupt shows canonical arguments and accepts only an authorized reviewer | Integration test with multiple identities |
| Recovery | Crash after target commit does not create a second transaction | Fault injection plus outcome lookup |
| Efficiency | Successful run remains inside step, time, and cost budgets | Trace-derived metrics |
| Evidence | Claim points to a source and retrieval record | Code coverage check plus sampled review |
| User experience | First useful artifact arrives within objective; stop semantics are clear | Product telemetry plus usability test |

### Level-specific evaluation emphasis

| Level | Must-pass properties before semantic quality |
|---|---|
| Level 1 — application | Tenant/user authorization, reducer correctness, tool schemas, UI/state convergence, write approval, idempotent domain mutations |
| Level 2 — machine | Filesystem/network/command policy, sandbox escape resistance, secret denial, diff scope, test evidence, cancellation and rollback/compensation behavior |
| Level 3 — organization | Requester/agent/approver identity binding, workspace/channel/tenant policy, confused-deputy tests, memory provenance, cross-system audit, delegation constraints |

## Dataset design

LangSmith datasets can be created manually, from historical traces, or synthetically; examples can be split, exported, and used in experiments. Filtered traces can be added back to datasets. Public dataset sharing exposes dataset examples and related experiment material, so production data must be redacted and reviewed before sharing: [dataset management](https://docs.langchain.com/langsmith/manage-datasets). **D.**

A useful agent-evaluation record should contain:

```yaml
case_id: finance-write-duplicate-001
level: 1
goal: "Record the attached receipt"
initial_state_ref: fixtures/user-a-ledger-v3.json
trusted_context:
  tenant_id: tenant-a
  actor_id: user-17
untrusted_inputs:
  - receipt-injection.png
allowed_tools: [parse_receipt, list_accounts, propose_transaction]
forbidden_tools: [delete_account, shell]
expected_interrupt:
  type: transaction_approval
expected_side_effects:
  max_count: 1
  ledger_delta: 42.17
expected_terminal_state: complete
budgets:
  model_calls: 6
  tool_calls: 8
  elapsed_seconds: 45
tags: [prompt-injection, duplicate-delivery, approval]
```

This schema is **E**. Keep large artifacts and secrets out of the dataset body; reference versioned, access-controlled fixtures. Store both the expected outcome and forbidden outcomes. A dataset made only of “ideal answers” cannot test authority.

### Dataset portfolio

Maintain at least six named suites:

1. **Golden tasks** — representative successful user journeys.
2. **Boundary cases** — empty, large, malformed, multilingual, stale, and conflicting inputs.
3. **Policy cases** — allowed, denied, approval-required, and separation-of-duties decisions.
4. **Adversarial cases** — injection, data exfiltration, confused deputy, malicious tool output, poisoned memory, and hostile skills.
5. **Reliability cases** — timeout, 429/5xx, partial commit, duplicate delivery, crash, reconnect, cancellation, and compensation.
6. **Production regressions** — confirmed user-visible or security failures, minimized and redacted.

Every case needs an owner, source, creation date, sensitivity, expected behavior, evaluator version, and retirement rule. Version the model, prompt, tools, policy, fixture, evaluator, and dataset together in experiment metadata.

## Choosing evaluators

LangSmith documents LLM-as-judge, code, composite, human, pairwise, and offline summary evaluators. The recommended division of labor is:

- Use **code evaluators** for schemas, exact facts, permissions, budgets, citations, idempotency, state invariants, and forbidden actions.
- Use **LLM judges** for usefulness, relevance, completeness, or trajectory reasonableness when deterministic rules cannot capture the quality.
- Use **pairwise judges** when relative preference is more stable than an absolute score.
- Use **human review** for ambiguous high-impact failures, judge calibration, policy disputes, and sampled production quality.
- Use **composite gates** when shipping requires several independent conditions. Never let a high prose score average away a policy violation.

LLM judges are themselves model systems. Calibrate them against an adjudicated human set, test position/order effects, pin judge prompt and model, inspect disagreement slices, and retain the raw judge rationale only when policy and privacy allow it. Treat judge upgrades as production changes.

## Trajectory evaluation and AgentEvals

LangSmith describes three useful evaluation scopes: final response, individual step, and trajectory. The official AgentEvals repository provides Python and TypeScript helpers for agent trajectories: [trajectory concepts](https://docs.langchain.com/langsmith/evaluation-approaches), [trajectory evaluators](https://docs.langchain.com/langsmith/trajectory-evals), and [official `agentevals` repository](https://github.com/langchain-ai/agentevals). **D/S.**

The documented trajectory match modes are exact/strict, unordered, subset, and superset. Exact matching is useful for narrow deterministic flows but brittle when several safe paths are valid. Subset matching is often a better production gate for mandatory events such as `approval -> write -> verify`. An LLM trajectory judge can evaluate a flexible path, with or without a reference trajectory, but needs the same calibration discipline as any other judge.

Publication code candidate; pin and execute against the chosen `agentevals` release before print:

```python
from agentevals.trajectory.match import create_trajectory_match_evaluator

requires_safe_write_path = create_trajectory_match_evaluator(
    trajectory_match_mode="subset",
    tool_args_match_mode="exact",
)
```

Do not teach an exact tool sequence as the universal definition of success. Define **required events**, **forbidden events**, **maximum repetition**, and **terminal invariants**. For example:

```text
required:  propose_change -> authorized_approval -> execute_change -> verify
forbidden: shell, read_secret, execute_before_approval
limits:    execute_change <= 1; total_tool_calls <= 12
terminal:  verified=true; pending_approval=false
```

## Production-to-regression loop

LangSmith automation rules can filter or sample production traces and then add them to datasets, annotation queues, webhooks, or online evaluators. This supports a disciplined loop: [rules](https://docs.langchain.com/langsmith/rules) and [trace sampling](https://docs.langchain.com/langsmith/sample-traces). **D.**

```text
alert, rejection, correction, or support case
  -> locate correlated trace and action-ledger events
  -> classify root cause and impact
  -> redact and minimize the input
  -> reproduce in an isolated fixture
  -> add a failing regression case
  -> implement control or product fix
  -> prove the case and neighboring suite pass
  -> deploy gradually
  -> monitor the original slice
```

Do not automatically copy arbitrary production payloads into a broadly accessible dataset. Apply tenant scope, data minimization, retention, legal basis, and redaction first.

## Evaluation knobs the builder must expose

| Knob | Why it exists | Failure if omitted |
|---|---|---|
| Dataset version and split | Reproducible comparisons and held-out testing | Overfitting to visible cases |
| Repetitions | Measure nondeterministic variance | One lucky run becomes “proof” |
| Max concurrency | Protect providers/tools and avoid artificial throttling | Evaluation noise or rate-limit storms |
| Cache policy | Reduce repeat cost without hiding changes | Stale results or misleading speed |
| Model/prompt/tool/policy versions | Attribute regressions | Unexplainable experiment deltas |
| Step/time/cost limits | Bound pathological runs | Runaway evaluation spend |
| Judge model/prompt/rubric | Reproduce semantic scores | Silent grading drift |
| Failure severity | Prevent averages masking critical failures | Unsafe build passes on mean score |
| Slice tags | Inspect tenant, language, tool, risk, model, and channel | Aggregate metric hides vulnerable cohort |
| Human adjudication rule | Resolve judge disagreement | Arbitrary acceptance |

LangSmith supports experiment repetitions, concurrency, and test caching; these are product features whose exact APIs should be pinned when samples are finalized: [experiment configuration](https://docs.langchain.com/langsmith/experiment-configuration). **D.**

## Observability: domain trace plus service trace

LangSmith defines a **run** as one operation/span, a **trace** as the related runs for one operation, and a **thread** as a link across related traces. It also supports feedback, tags, metadata, automatic and manual instrumentation: [observability concepts](https://docs.langchain.com/langsmith/observability-concepts). **D.**

OpenTelemetry defines vendor-neutral signals—traces, metrics, logs, and baggage/context propagation—and supports collectors that can fan telemetry out to multiple backends: [concepts](https://opentelemetry.io/docs/concepts/), [traces](https://opentelemetry.io/docs/concepts/signals/traces/), [metrics](https://opentelemetry.io/docs/concepts/signals/metrics/), and LangSmith's [OTel export guide](https://docs.langchain.com/langsmith/trace-with-opentelemetry). **D.**

Use both planes:

```text
Product task ID / correlation ID
  ├─ agent-domain trace: model, tool, state, interrupt, evaluator, feedback
  ├─ service trace: gateway, queue, worker, database, MCP, provider, channel
  └─ action ledger: authorization, approval, canonical action, outcome, compensation
```

The correlation ID connects them; it does not grant authority. Never use OpenTelemetry baggage for trusted identity or authorization. OTel warns that baggage may propagate to unintended downstream services and has no built-in integrity guarantee: [baggage](https://opentelemetry.io/docs/concepts/signals/baggage/). **D.**

### Canonical book telemetry dictionary

Keep an internal schema stable even when vendors change:

| Field | Purpose | Cardinality/sensitivity note |
|---|---|---|
| `task_id`, `thread_id`, `run_id`, `attempt_id` | Correlate logical task and attempts | IDs belong in traces/logs, not metric labels |
| `tenant_id_hash`, `deployment`, `region` | Isolation and operations | Never raw tenant name in public telemetry |
| `agent_id`, `agent_version`, `graph_version` | Attribute behavior | Bounded cardinality |
| `model_provider`, `model_name`, `route_reason` | Routing and cost | Pin normalized names |
| `tool_name`, `tool_risk`, `tool_outcome` | Tool reliability and policy | Do not record raw args by default |
| `actor_id_hash`, `agent_principal`, `delegation_id` | Identity chain | Restricted audit plane; minimize elsewhere |
| `approval_id`, `policy_decision_id` | Correlate intervention | Never approval token/secret |
| `input_tokens`, `output_tokens`, `cached_tokens`, `cost` | Resource control | Verify provider accounting |
| `queue_delay_ms`, `ttfa_ms`, `total_ms`, `attempt_count` | Reliability/latency | Histograms, not unbounded labels |
| `error_class`, `retryable`, `terminal_status` | Recovery and alerting | Normalized error taxonomy |

LangSmith can track token and cost usage for major providers and accept custom token/cost data for other models and non-LLM operations. Its provider price map and historical behavior can change, so finance-grade chargeback should reconcile against provider invoices: [cost tracking](https://docs.langchain.com/langsmith/cost-tracking). **D plus E.**

### GenAI semantic-convention warning

The OpenTelemetry GenAI semantic conventions and their model/agent metrics are currently marked **Development** in the official semantic-conventions repository. Current definitions include model operation duration, token usage, time to first output chunk, and time per output chunk, with agent and tool spans also represented. Input/output and tool-definition capture is opt-in because it may contain sensitive information: [GenAI metrics](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-metrics.md) and [GenAI span model](https://github.com/open-telemetry/semantic-conventions/blob/main/model/gen-ai/spans.yaml). **EA.**

Publication rule: pin the semantic-conventions release, label it Development, and isolate provider/convention mapping in the exporter. Do not make application logic query experimental field names directly.

### Sensitive telemetry and sampling

OpenTelemetry places responsibility for sensitive-data handling on the implementer and recommends data minimization plus Collector processors for filtering, redaction, transformation, or attribute removal. Hashing alone may not anonymize low-entropy identifiers: [handling sensitive data](https://opentelemetry.io/docs/security/handling-sensitive-data/). **D.**

Recommended defaults:

- Do not collect hidden chain-of-thought.
- Do not log secrets, authorization headers, raw credentials, full tool arguments, receipt images, financial records, private channel content, or repository files by default.
- Store a redacted summary, schema-validity result, content hash, byte count, and restricted artifact reference when detailed evidence is required.
- Apply retention and access controls by data class, not one global trace setting.
- Use head sampling for predictable low-cost coverage and tail sampling when keeping errors/slow traces is worth collector state and operational complexity. OTel explains that sampling can miss critical data and that tail sampling decides after more of the trace is visible: [sampling](https://opentelemetry.io/docs/concepts/sampling/). **D.**
- Preserve all security-policy denials and consequential-action audit events in the dedicated ledger even when ordinary traces are sampled.

## Figures and screenshot candidates for Chapter 23

1. Evaluation pyramid with deterministic volume at the base and sampled online evaluation at the top.
2. One finance task shown as final-output score versus full-trajectory score; the output looks correct but a duplicate write fails the trajectory.
3. LangSmith experiment comparison over a small synthetic dataset, captured only after version pinning and redaction.
4. Correlated agent trace, OTel service waterfall, and action-ledger row for one approval-gated write.
5. Production failure becoming a minimized regression case.

### Chapter 23 production gate

- Critical deterministic and policy suites pass with zero critical failures.
- Every consequential tool has success, denial, duplicate-delivery, timeout, ambiguous-outcome, and cancellation cases.
- Semantic evaluators are calibrated against human adjudication and versioned.
- At least one crash-and-resume scenario is runtime-observed.
- Online sampling is configured by risk, not only randomly.
- Production failures have a redacted dataset intake process.
- Trace access, retention, and redaction are reviewed.
- No shipping metric averages away a forbidden action.

# Chapter 24 — Security by Authority Level

## Chapter thesis

Agent security is an authority-design problem. The model consumes instructions and untrusted data, but tools, identities, runtimes, and policy engines determine what can actually happen. The secure default is to minimize both privilege and agency, enforce decisions outside the prompt, and make every consequential action attributable and recoverable.

## Current primary-source frame

OWASP published the *Top 10 for Agentic Applications for 2026* in December 2025. The official list is: ASI01 Agent Goal Hijack; ASI02 Tool Misuse & Exploitation; ASI03 Identity & Privilege Abuse; ASI04 Agentic Supply Chain Vulnerabilities; ASI05 Unexpected Code Execution; ASI06 Memory & Context Poisoning; ASI07 Insecure Inter-Agent Communication; ASI08 Cascading Failures; ASI09 Human-Agent Trust Exploitation; ASI10 Rogue Agents: [official project page](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), [official PDF](https://genai.owasp.org/download/52117/?tmstv=1765059207), and [launch note](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/). **D.**

NIST's May 2026 `NIST AI 800-5` summarizes responses to an RFI on AI-agent security. It reports broad agreement among respondents that agents introduce novel risks while established cybersecurity practices remain relevant and need adaptation. This is a summary of comments, not a binding control standard: [NIST publication](https://www.nist.gov/publications/summary-analysis-responses-request-information-regarding-security-considerations-ai). **D/EA.**

NCCoE's February 2026 software and AI agent identity/authorization concept paper asks about agent identity metadata, authentication, credential lifecycle, zero-trust authorization, least privilege, delegation/on-behalf-of behavior, human-agent binding, and tamper-evident audit. It is a concept paper, not a final NIST profile: [concept paper](https://www.nccoe.nist.gov/sites/default/files/2026-02/accelerating-the-adoption-of-software-and-ai-agent-identity-and-authorization-concept-paper.pdf) and [NIST announcement](https://www.nist.gov/news-events/news/2026/02/new-concept-paper-identity-and-authority-software-agents). **EA.**

NIST SP 800-207 remains the stable zero-trust baseline: no implicit trust based on network location, and authentication/authorization before access to a resource. SP 800-207A extends the discussion to application and service identities with granular policy: [SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) and [SP 800-207A](https://csrc.nist.gov/pubs/sp/800/207/a/final). **D.**

## ASI risks converted into engineering work

| OWASP risk | Concrete agent failure | Primary controls | Required evaluation |
|---|---|---|---|
| ASI01 Goal Hijack | Receipt, webpage, issue, or channel message changes the agent's goal | Mark untrusted data, keep policy outside prompt, constrain tools, require approval for changed scope | Injection corpus across every ingestion path; forbidden-goal assertions |
| ASI02 Tool Misuse | Valid tool used with harmful target/arguments/frequency | Per-tool scopes, schema/business validation, rate/step limits, egress allowlist, risk policy | Invalid target, excess volume, parameter smuggling, sequence abuse |
| ASI03 Identity & Privilege Abuse | Agent uses ambient or service credentials for an unauthorized requester | Separate actor/agent/delegated identities, short-lived scoped tokens, resource authorization | Cross-user/tenant/channel tests; revoked/expired/delegated token tests |
| ASI04 Supply Chain | Malicious skill, MCP server, package, model, or prompt asset gains authority | Pin/sign/scan, provenance, review, capability manifest, controlled updates | Dependency/skill substitution; unsigned or drifted artifact rejection |
| ASI05 Unexpected Code Execution | Model-generated shell/code escapes intended boundary | No general shell by default, sandbox, syscall/process/fs/network limits, output validation | Escape, symlink, traversal, command injection, resource-exhaustion tests |
| ASI06 Memory & Context Poisoning | Untrusted claim becomes durable preference or institution fact | Provenance, scope, quarantine, review, TTL, correction/deletion | Poisoned memory retrieval; cross-user memory isolation; revocation |
| ASI07 Insecure Inter-Agent Communication | Delegation message is spoofed, replayed, overbroad, or loses accountability | Authenticated agent identity, signed/narrow task contract, nonce/expiry, authorization per hop | Spoof/replay/tamper tests; privilege non-amplification |
| ASI08 Cascading Failures | Retry/delegation loop amplifies load, cost, or bad changes | Budgets, circuit breakers, bounded fan-out, health gates, containment domains | Provider outage, queue surge, repeated failure, downstream corruption drills |
| ASI09 Human-Agent Trust Exploitation | User approves misleading summary or treats generated claim as fact | Canonical diff/arguments, provenance, risk label, reversible controls, trained approver UX | Approval comprehension, social engineering, stale/changed-action tests |
| ASI10 Rogue Agents | Agent exceeds goal, evades stop, or persists unauthorized behavior | Runtime-enforced policy, kill switch, credential revocation, anomaly detection, immutable audit | Stop/revoke drills; budget breach; policy-evasion and persistence tests |

The mapping is **E**; the risk names are **D**.

## Security architecture by level

| Boundary | Level 1 — application | Level 2 — machine | Level 3 — organization |
|---|---|---|---|
| Untrusted inputs | User text, files, retrieved content, frontend state | All Level 1 inputs plus repository files, command output, packages, skills | All prior inputs plus channel history, links, shared docs, messages from many actors |
| Crown jewels | Tenant records, user data, domain writes | Source, local files, secrets, processes, network, cloud credentials | Organization data, shared systems, service identities, institutional memory, delegated machines |
| Identity chain | End user -> application agent -> app API | Operator -> machine agent -> OS/tool credential | Requester -> organizational agent principal -> approver/delegate -> target system |
| Isolation minimum | Per-user/tenant data and thread authorization | Dedicated workspace/container/VM, scoped FS/network/process/credentials | Workspace/tenant/channel policy plus isolated workers and stores |
| Human control | Approve consequential app mutation | Approve scope, privileged command, external write, merge/deploy | Bind authorized approver/quorum to canonical action and policy |
| Audit minimum | Actor, tool, args digest, state delta, outcome | Plus command, file diff, environment, network, artifact/test provenance | Plus agent principal, requester, channel, policy, approvals, delegation chain |
| Dominant abuse | Cross-user action or prompt-induced tool misuse | Exfiltration, code execution, poisoned skill/repo, persistence | Confused deputy, impersonation, cross-team leakage, poisoned shared memory |

### Level 1 hardening target

For `personal-finance-copilot`, the current frontend approval surfaces are valuable interaction evidence, not a security boundary. The hardened write path should authenticate the user at the server, derive the tenant and account scope from trusted context, validate transaction arguments, persist an action proposal, bind approval to that proposal digest, execute with an idempotency key, and verify the ledger outcome. Never trust a tenant, user, balance, or authorization claim returned by the model or frontend.

Minimum failure cases:

- user A asks to read or mutate user B's account;
- attachment text says to ignore policy or change the amount;
- approval UI displays one amount while the canonical action contains another;
- approval expires or user privileges change before execution;
- target commits but the response is lost;
- mobile client submits the approval twice;
- trace exporter attempts to record raw receipt or account data.

### Level 2 hardening target

For `hermes-cpk`, the central lesson is “visibility is not supervision.” A CopilotKit pane can show commands without constraining them. The hardened machine boundary needs:

- a dedicated disposable worker or tightly isolated workspace;
- filesystem allow/deny rules resolved against canonical paths, including symlinks;
- network deny-by-default with explicit destinations and protocols;
- process, CPU, memory, wall-time, disk, and child-process limits;
- secrets brokered just in time rather than inherited ambiently;
- a command/tool allowlist or policy engine, not string-prefix matching alone;
- separate read, propose, write, execute, publish, and deploy authorities;
- artifact/diff review before irreversible external action;
- an append-only action record and explicit compensation procedure;
- hostile-repository and hostile-skill evaluations.

The OWASP Agentic Skills Top 10 is a separate official project useful here. It names malicious skills, supply-chain compromise, over-privileged skills, insecure metadata, untrusted external instructions, weak isolation, update drift, poor scanning, lack of governance, and unsafe cross-platform reuse: [official list](https://owasp.org/www-project-agentic-skills-top-10/top10.html). **D.** Do not merge its `AST` labels with the main `ASI` list.

### Level 3 hardening target

For Channels/OpenTag, sender context in the model prompt is not authorization and a clicked confirmation is not a governed approval. The hardened path must preserve at least four principals:

1. authenticated requester;
2. organizational agent service identity;
3. delegated/on-behalf-of subject, if any;
4. approving human or quorum.

Policy should evaluate tenant, workspace, channel, requester, agent profile, resource, action, sensitivity, time, and delegation. Reauthorize at execution time. Bind approval to a canonical digest, expiry, permitted approver set, and one-time use. The target tool must independently enforce the decision.

## Control patterns

### Separate instructions, data, and authority

Prompt injection cannot be solved by another prompt sentence. Treat all retrieved pages, documents, receipts, repository files, command output, MCP results, messages, and memories as data with provenance and trust metadata. Let the model propose an action; let deterministic code decide whether the action exists, whether arguments are valid, whether the actor is authorized, and whether approval is required.

```text
untrusted content -> parse/classify -> bounded model context -> proposed typed action
                                                     |
trusted actor/context -> policy engine -> permit / deny / require approval
                                                     |
                                      constrained tool executor
```

### Tool risk manifest

Every tool should declare properties that runtime policy can enforce:

```ts
type ToolPolicy = {
  impact: "read" | "local-write" | "external-write" | "execute";
  reversible: boolean;
  dataClasses: string[];
  credentialScope: string;
  networkDestinations: string[];
  approval: "never" | "conditional" | "always";
  maxCallsPerRun: number;
  timeoutMs: number;
};
```

This is **E**, not a current CopilotKit or LangChain API. The runtime must validate the manifest against actual enforcement. A declaration without a sandbox, authorization check, or egress control is documentation, not protection.

### Identity and delegated authority

Do not place credentials in graph state or model context. LangSmith's custom-auth documentation explicitly recommends resolving user credentials from a secure secret store rather than storing secrets in graph state. Its auth model separates authentication from per-resource authorization and can attach owner metadata/filters to threads and related resources: [authentication and access control](https://docs.langchain.com/langsmith/auth) and [custom authentication](https://docs.langchain.com/langsmith/custom-auth). **D.** Self-hosted deployments do not gain a secure policy merely by enabling the runtime; the implementer owns it.

Use short-lived, audience-bound credentials; record who delegated what scope to which agent; never let an agent upgrade its own grant; and validate the requester at the target resource. NIST's concept paper makes human-agent identity binding, delegated/on-behalf-of access, key lifecycle, and verifiable audit explicit open design areas. Treat its proposed direction as **EA**, not a finished standard.

### Memory and context governance

Memory writes are data writes. Attach source, author, tenant, scope, timestamp, sensitivity, confidence, reviewer, expiry, and supersession links. Quarantine model-derived or untrusted memories until policy permits reuse. Support correction and deletion propagation. Never convert a channel transcript, webpage assertion, or repository instruction into organization-wide memory solely because the model summarized it confidently.

Test retrieval with poisoned, stale, revoked, cross-tenant, and conflicting memories. Keep task state, personal preference, thread history, and institutional knowledge in separate stores and authorization domains.

### Supply chain and skills

Inventory and pin models, prompts, packages, containers, MCP servers, skills, system tools, and datasets. Verify provenance and signatures where available; scan code and declared permissions; review updates; block undeclared capability expansion; and retain a rollback version. NIST SP 800-218A supplies an AI-focused secure-development profile to use with the SSDF: [SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final). **D.**

For a skill, review both the manifest/instructions and every script/resource it can invoke. Run it in an isolated fixture with fake credentials. Test whether hostile external content can cause it to exceed declared scope. Cross-platform reuse requires a new authority review because “filesystem access” means something different in a browser sandbox, developer laptop, CI runner, and organization worker.

### Sandbox as a containment layer

A sandbox should restrict filesystem, process, network, credentials, devices, persistence, and resources. It is one layer, not the entire security model. A sandboxed agent can still misuse authorized APIs, leak allowed data to an allowed destination, corrupt its workspace, or persuade a human to approve harm. Combine it with least agency, policy, scoped identity, validation, monitoring, and disposable recovery.

### Action ledger versus trace

The action ledger is the durable accountability record for consequential operations. Minimum fields:

```text
event_id, timestamp, tenant, task/run/attempt
requester principal, agent principal, delegated subject
canonical action type and arguments digest
resource/target, risk classification, policy decision
approval identity/quorum, digest, expiry, decision
idempotency key, execution outcome, target receipt
verification outcome, compensation/recovery reference
```

Restrict sensitive fields, sign or otherwise make tampering detectable, define retention, and reconcile against target-system receipts. A trace optimized for debugging can be sampled, redacted, or deleted; the ledger for a payment, deployment, or organizational write may have different integrity and retention duties.

## Adversarial suite by reference build

| Reference | Required attacks before publication says “hardened” |
|---|---|
| Finance app | Receipt injection; tenant swap; stale/forged approval; duplicate submission; hidden amount/currency change; trace leakage |
| GTM Operations Workspace | Provider routing downgrade; tool-set mismatch across providers; prompt injection in CRM/email content; cross-workspace data; fallback after policy refusal |
| Hermes | Malicious `README`/issue/skill; symlink/path traversal; shell metacharacters; secret read; network exfiltration; fork bomb/resource exhaustion; stop/revoke failure |
| Channels/OpenTag | User spoofing; cross-workspace event; unauthorized approver; replayed click; changed action after approval; confused-deputy request; poisoned institutional memory |

## Chapter 24 figures and code candidates

1. Authority gradient: app record -> machine -> organization, with expanding blast radius.
2. Instruction/data/authority separation diagram.
3. Four-principal Level 3 identity chain.
4. One approval showing canonical digest, permitted approver, expiry, policy decision, and execution receipt.
5. Sandbox layers around a disposable machine worker.
6. Security control matrix mapping ASI01–ASI10 to prevention, detection, response, and test.

### Chapter 24 production gate

- Threat model inventories inputs, assets, identities, tools, trust zones, and side effects.
- Tool and skill capabilities are explicit, deny-by-default, and enforced outside prompts.
- Tenant/user/resource authorization is tested at the target boundary.
- Consequential approvals bind identity, canonical action, expiry, and one-time execution.
- Secrets are brokered, scoped, revocable, and absent from model context/state/traces.
- Memory has provenance, authorization, retention, correction, and deletion.
- Level 2 workers have effective filesystem/network/process/resource containment.
- Action ledger and incident procedure exist.
- OWASP attack cases are in the regression suite.
- Kill switch and credential-revocation drills are runtime-observed.

# Chapter 25 — Reliability, Cost, and Scaling

## Chapter thesis

Reliable agent execution is not one long HTTP request and not one uninterrupted model loop. It is a durable task with bounded attempts, explicit state, controlled side effects, observable progress, and a recovery contract. The product should remain correct when a worker dies, a queue redelivers, a provider throttles, a user disconnects, or the target system commits without returning a response.

## Four records that must not be confused

| Record | Purpose | Typical owner | What it does not prove |
|---|---|---|---|
| Agent checkpoint | Resume graph/task state | LangGraph checkpointer/store | That external side effects happened once |
| Queue/lease record | Deliver an attempt and track ownership/time | Queue/runtime | That the task is correct or complete |
| Action/outcome record | Deduplicate and reconcile consequential tools | Domain/tool boundary | That the whole run finished |
| UI projection | Show current user-facing status/artifacts | CopilotKit/application | That backend state or target outcome is authoritative |

The production design must give each record an ID and reconciliation rule. Conflating them creates the classic failure where the UI says “failed,” the target committed, and a retry performs the action again.

## Durable execution evidence

LangGraph persistence checkpoints graph state at supersteps and associates state with threads. Checkpoints enable human interrupts, recovery, inspection, and resumable execution. Pending writes support recovery from failures within a superstep: [persistence](https://docs.langchain.com/oss/python/langgraph/persistence). **D.**

LangGraph's Functional API documentation states that nondeterministic operations and side effects should be placed in tasks so their results can be checkpointed. It explicitly recommends idempotency keys or checking for an existing result before side effects, because a task can run more than once: [Functional API](https://docs.langchain.com/oss/python/langgraph/functional-api). **D.**

This yields a core book rule:

> Checkpoint before waiting; checkpoint after learning. At the side-effect boundary, assume the attempt can repeat.

### Checkpoint placement

Checkpoint or create a durable boundary:

- after a meaningful, serializable state transition;
- before an indefinite human interrupt;
- after an expensive model/tool result that is safe to reuse;
- before and after delegation;
- around a consequential side effect using an independent action/outcome record;
- after a recoverable unit whose repetition would be costly.

Do not checkpoint secrets, open sockets, process handles, mutable provider clients, or arbitrary UI objects. Store typed semantic state and references to restricted artifacts.

## Idempotency and ambiguous outcomes

At-least-once queues can deliver a message again, so AWS's SQS guidance recommends idempotent consumers. Visibility timeouts hide an in-flight message temporarily, can be extended while work is active, and allow redelivery if processing does not complete: [queue types](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-queue-types.html) and [visibility timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html). **D.** These are SQS-specific mechanics but illustrate a general distributed-systems constraint.

An idempotency key must represent the semantic action, not the process attempt:

```text
task_id:       user-visible objective
run_id:        one runtime execution
attempt_id:    one delivery/worker attempt
action_id:     one proposed domain mutation
idempotency:   stable key reused across retries of that action
target_receipt: evidence from the external system
```

Implementation candidate; editorial pseudocode, not a framework API:

```python
def execute_once(action, actor, approval):
    canonical = canonicalize(action)
    action_id = sha256(canonical)
    authorize(actor, canonical)
    verify_approval(approval, action_id)

    if prior := outcome_store.find(action_id):
        return reconcile(prior)

    outcome_store.mark_started(action_id)
    try:
        receipt = target.execute(canonical, idempotency_key=action_id)
    except AmbiguousOutcome:
        receipt = target.lookup_by_idempotency_key(action_id)
        if receipt is None:
            outcome_store.mark_manual_reconciliation(action_id)
            raise

    outcome_store.mark_committed(action_id, receipt)
    return receipt
```

Do not claim exactly-once unless the complete path—including target system—actually offers and verifies the required semantics. “Effectively once for this domain action under these assumptions” is usually more accurate.

## Failure taxonomy and retry policy

LangGraph's reliability guidance distinguishes transient failures suitable for retry, LLM-recoverable errors that can be returned into the agent loop, user-fixable errors that should interrupt, and unexpected errors that should surface for debugging. Node granularity affects how much successful work is repeated after failure: [thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph). **D.**

The current fault-tolerance documentation also includes per-node timeout and error-handler APIs labeled alpha/version-sensitive. Pin the exact LangGraph version if the book uses them: [fault tolerance](https://docs.langchain.com/oss/python/langgraph/fault-tolerance). **EA.**

| Failure class | Example | Default response | Never do |
|---|---|---|---|
| Invalid/deterministic | Schema error, impossible amount, missing required state | Reject or return structured correction | Blind retry |
| Policy/authorization | Forbidden resource, expired token, denied command | Fail closed; require new authorization/context | Fall back to a more permissive tool/model |
| Transient dependency | 429, temporary 5xx, short network failure | Bounded retry with backoff/jitter inside deadline | Retry at every stack layer |
| LLM-recoverable tool error | Search syntax or correctable parameter | Return a concise typed error to the loop, with attempt limit | Leak internals or permit infinite self-correction |
| User-fixable | Ambiguous account, missing approval | Persist and interrupt | Keep spending while waiting |
| Ambiguous outcome | Timeout after payment/deploy/write may have committed | Query outcome/idempotency receipt; reconcile or escalate | Repeat the side effect immediately |
| Poison task | Deterministically crashes or violates invariants | Quarantine/DLQ with evidence | Infinite redelivery |
| Capacity/overload | Queue surge, dependency saturation | Admission control, shed/degrade, circuit break | Fan out more retries |

AWS's Builders' Library recommends timeouts, limited retries, exponential backoff, and jitter; it also warns that retries can amplify overload and should be controlled at a selected layer: [timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) and [correlated failures](https://aws.amazon.com/builders-library/minimizing-correlated-failures-in-distributed-systems/). **D.**

### Retry decision inputs

Before retrying, evaluate:

- error classification and provider retry hint;
- whether the operation is read-only, idempotent, or ambiguous;
- attempts already consumed across all layers;
- remaining task deadline and cost budget;
- target/service health and circuit state;
- queue visibility/lease time;
- whether retry would violate policy, approval expiry, or user cancellation;
- whether a fallback changes quality, data residency, tools, or safety behavior.

## Queues, leases, heartbeats, and dead letters

For long-running work, use a durable queue or runtime that records accepted work independently of a client connection. The worker claims a lease, emits heartbeats/progress, and renews before expiry. If it dies, the attempt becomes eligible for controlled redelivery. Set the lease from observed attempt duration and heartbeat behavior; do not hardcode one global timeout for all tools.

Dead-letter queues isolate repeatedly failed tasks after a maximum receive/attempt policy. AWS documents DLQ configuration and redrive; redriven messages receive new delivery metadata and can interleave with new work, so replay must be deliberate: [DLQ configuration](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-dead-letter-queue.html) and [DLQ redrive](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-dead-letter-queue-redrive.html). **D.**

A DLQ is not a trash can. Store task/attempt IDs, normalized error, last safe checkpoint, action outcomes, policy/approval state, and an artifact reference. Redrive is a privileged operation with dry-run, batch limit, current-policy revalidation, and an audit record. Never replay a consequential action merely because code changed.

## Timeouts and deadline propagation

Define separate limits for:

- queue wait;
- whole task deadline;
- one run/attempt;
- model call;
- tool call;
- human approval expiry;
- stream inactivity;
- cancellation grace period;
- compensation/manual-recovery objective.

Propagate the remaining deadline downstream. A tool should not begin a five-minute action when the task has ten seconds left. Timeouts should terminate or detach work safely; otherwise the caller may retry while the original continues in the background.

## Cancellation, interrupt, and compensation

LangSmith Deployment's run API distinguishes cancellation behaviors including interrupt and rollback-like runtime options. Its documentation also covers disconnect-driven cancellation and strategies for concurrent runs such as enqueue, reject, interrupt, and rollback: [cancel runs](https://docs.langchain.com/langsmith/cancel-run). **D, product-specific.**

The book must make the semantic distinction explicit:

| User intent | Runtime behavior | Domain requirement |
|---|---|---|
| Stop generating | Cancel current model stream | No side effect assumption |
| Stop after current safe step | Set cancellation flag; do not start new step | Tools poll/return at safe boundaries |
| Cancel queued task | Remove/reject before claim | Record terminal cancellation |
| Interrupt run | Persist state and wait | Resume contract and expiry |
| Rewind runtime state | Restore prior checkpoint if supported | Does not reverse external changes |
| Undo action | Execute compensation/reversal | Domain-specific authorization and receipt |

Every consequential tool should declare: cancellable before start, cancellable while active, reversible, compensation method, compensation deadline, and manual recovery owner. Use a saga/compensation pattern when a multi-step operation spans systems, but recognize that compensation can itself fail and is not always equivalent to erasure.

## Recovery drills

A production claim requires runtime-observed drills, not just unit tests:

1. Kill a worker before any side effect and verify another attempt resumes.
2. Kill it after target commit but before outcome persistence; verify lookup prevents duplication.
3. Expire an approval while a task is queued; verify execution reauthorizes and denies.
4. Disconnect the client; verify configured background/cancel semantics.
5. Throttle the model and one tool; verify bounded retries and useful UI state.
6. Poison one task; verify it reaches quarantine without starving the queue.
7. Cancel during a long tool; verify safe boundary and outcome reconciliation.
8. Revoke the agent credential; verify active and future work fail closed.
9. Restore the checkpoint store from backup; verify consistency with action outcomes.
10. Redrive a DLQ batch in staging; verify current policy and idempotency checks.

## Latency and streaming as an operating model

Agents produce useful intermediate work and can run far longer than a request/response UI assumes. Measure at least:

| Metric | Definition | User value |
|---|---|---|
| Time to acknowledgement | Request accepted and durable task ID returned | Confidence work was received |
| Queue delay | Accepted until worker begins | Capacity signal |
| Time to first state update | First real stage/tool/state event | Proof of activity |
| Time to first token/chunk | First model output chunk | Conversational responsiveness |
| Time to first useful artifact | First source, plan, preview, diff, or card the user can act on | Strongest perceived-progress metric |
| Stage dwell time | Time in planning/search/tool/review/waiting | Diagnoses bottleneck |
| Intervention latency | Approval requested until surfaced and decided | Human workflow efficiency |
| Total time to terminal outcome | Accepted until verified completion/failure/cancel | Journey reliability |

LangSmith can record time to first token automatically for supported wrappers; manual instrumentation must identify token events: [TTFT tracing](https://docs.langchain.com/langsmith/log-llm-trace). **D.** OTel's current GenAI convention includes time-to-first-output-chunk and inter-chunk metrics, but remains Development as noted above.

### Streaming contract

Use structured lifecycle/state/artifact events, not only token deltas:

```text
task.accepted -> run.started -> stage.changed -> tool.proposed
-> approval.requested/decided -> tool.started/progress/completed
-> artifact.updated -> run.completed/failed/cancelled
```

Each event should carry run/attempt ID, monotonically ordered sequence within its stream, timestamp, semantic type, redacted payload, and replay/snapshot behavior. On reconnect, fetch an authoritative state snapshot and resume after a cursor; do not assume the client received every event. Coalesce high-frequency token/progress events and apply backpressure.

Use stage-based progress unless the work units are measurable. Never display a fake percentage for an adaptive loop. Distinguish “waiting for approval,” “retrying,” “degraded,” “cancel requested,” and “manual recovery required.” Define whether Stop means stop generation, stop current tool, stop after step, cancel task, or compensate.

## Model routing and fallback

LangChain's agent middleware supports dynamic model selection at runtime, model fallback, model-call limits, tool-call limits, retries, context editing, summarization, and PII detection. These features are current documented capabilities whose APIs require version pinning: [agents and dynamic models](https://docs.langchain.com/oss/python/langchain/agents), [middleware overview](https://docs.langchain.com/oss/python/langchain/middleware/overview), and [built-in middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in). **D.**

Route on explicit requirements rather than vague “complexity” alone:

- required tool/function/structured-output capability;
- reasoning/evaluation quality proven on the task slice;
- latency and cost budget;
- data residency, privacy, contractual, and retention constraints;
- modality and context size;
- provider health and rate limits;
- action risk and whether the model is proposing or only summarizing;
- tenant/product tier, where policy permits;
- fallback compatibility with tools, schemas, and safety behavior.

Record the route reason and evaluate every route independently. A fallback must not silently weaken data policy, tool constraints, structured-output guarantees, or approval behavior. Do not treat a model refusal or policy denial as provider failure deserving a more permissive fallback.

For GTM Operations Workspace, the source-present ability to choose Hermes, Anthropic, or OpenAI is a routing seam, not evidence that routes are behaviorally equivalent. Build a cross-provider suite for tool selection, argument schemas, streaming, cancellation, safety, cost, and final quality before enabling automatic fallback.

## Context engineering and memory pressure

Long context is a budget, not a substitute for state design. Separate:

```text
system policy and tool contracts
trusted invocation context
current semantic task state
recent interaction window
retrieved evidence with provenance
summarized older context
references to large artifacts
```

LangChain documents summarization and context-editing middleware that can compress older conversation history or clear older tool results. Model profiles can expose context/capability data used by middleware, with version requirements noted in the docs: [models](https://docs.langchain.com/oss/python/langchain/models) and [built-in middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in). **D.**

Store raw semantic data in state and format it for each consumer. Summaries can omit obligations, approvals, denials, or precise values; protect such invariants in typed fields outside the summary. Evaluate context compaction with long-running regression cases and compare required fact retention, tool behavior, latency, and cost.

## Caching layers

LangChain documents provider prompt caching as implicit for some providers and explicit for others, with cache usage reflected in model usage metadata. Minimum token thresholds and APIs vary by provider: [prompt caching](https://docs.langchain.com/oss/python/langchain/models#prompt-caching). **D.**

| Cache | Safe use | Key must include | Dangerous use |
|---|---|---|---|
| Provider prompt-prefix | Stable policy/tool definitions and repeated large context | Provider/model/version and exact prefix | Assuming a hit or savings; placing secrets in reusable prefix |
| Exact model-result | Pure, deterministic-ish transformation with accepted staleness | Model/prompt/schema/input/policy/tenant data class | Reusing action decisions or safety judgments across users |
| Read-tool result | Expensive read with explicit TTL | Tenant/resource/query/auth scope/version | Mutable entitlement, balance, deployment, or approval state |
| Artifact/retrieval | Immutable content addressed by hash/version | Source/version/tenant/access class | Returning an artifact after access is revoked |
| Semantic cache | Low-risk informational responses only | Tenant, policy, locale, model, embedding/version | Tool selection, writes, policy, finance, machine/organizational actions |

Never cache an authorization result beyond its policy/credential lifetime, an approval beyond its canonical action and expiry, or an ambiguous side-effect outcome. Cache lookup must itself enforce tenant and resource access. Observe hit rate, age, saved tokens/time, stale-error rate, and cross-scope denial.

## Budgets and runaway containment

Enforce budgets before the next unit of work:

| Budget | Examples of enforcement |
|---|---|
| Model calls/tokens | Hard per-run cap; reserve tokens for final/error response |
| Tool calls | Per-tool and aggregate caps; stricter for writes/network/shell |
| Steps/depth | Graph recursion/handoff/subagent limits |
| Parallelism | Per-run, per-tenant, per-tool, and global semaphores |
| Wall time/deadline | Propagated remaining deadline |
| Monetary cost | Preflight estimate plus cumulative hard ceiling |
| Output/artifact size | Byte/page/file limits and streaming backpressure |
| Network/egress | Destination, byte, and request budgets |
| Human wait | Approval expiry and stale-task policy |

LangChain's model/tool call limit middleware supplies framework-level primitives, but domain cost, external-tool spend, and tenant quotas remain application responsibilities. LangSmith cost tracking is an observation source; the execution runtime must enforce hard limits.

On budget exhaustion, stop at a safe boundary and return a structured terminal or resumable state: what completed, what remains, artifacts, side effects, why the budget stopped, and whether a human can extend it. Never conceal partial external effects behind “budget exceeded.”

## Scaling and admission control

Scale stateless gateways separately from durable queues, workers, checkpointers, artifact stores, and tool executors. Apply concurrency limits by tenant, tool, provider, and risk class so one expensive task cannot starve everyone. Use fair scheduling or reserved capacity for interactive/approval work. Bound subagent fan-out. Protect slow dependencies with bulkheads and circuit breakers.

Track queue age, claimed versus running work, heartbeat loss, retry amplification, per-tenant concurrency, provider saturation, tool saturation, stuck interrupts, and outcome-reconciliation backlog. Autoscaling on CPU alone misses queue delay and provider constraints.

## SLOs and safety invariants

Google's SRE guidance defines an SLI as a measured behavior, an SLO as a target value/range, and an error budget as the permitted unreliability implied by the SLO. It recommends measuring close to the user and using tail percentiles rather than averages for latency: [SLO chapter](https://sre.google/sre-book/service-level-objectives/) and [implementing SLOs](https://sre.google/workbook/implementing-slos/). Burn-rate alerts detect rapid error-budget consumption: [burn-rate alerting](https://docs.cloud.google.com/stackdriver/docs/solutions/slo-monitoring/alerting-on-budget-burn-rate). **D.**

Candidate agent SLIs:

| Journey | SLI numerator/denominator or distribution |
|---|---|
| Accept a task | Durably accepted eligible tasks / valid submitted tasks |
| First useful artifact | Distribution from durable acceptance to first usable plan/source/diff/card |
| Complete task | Verified correct terminal outcomes within deadline / eligible tasks |
| Resume | Injected/real recoverable failures resumed without loss or duplicate effects / recoverable failures |
| Consequential write | Verified authorized correct writes / attempted eligible writes |
| Intervention | Approval requests delivered before expiry / created approval requests |
| Cost efficiency | Cost and steps per verified successful task, by slice |
| Queue health | Distribution of queue age and oldest eligible task |

Set objectives by user journey and risk class, not one average across all tasks. Pair them with an approved error-budget policy that says what changes when the budget is spent.

**Safety invariants are not error-budget items:** no unauthorized write, no cross-tenant access, no secret leakage, no execution after invalid approval, no unbounded machine escape. Alert immediately, contain, investigate, and follow the incident process. A 99.9% objective would still authorize unacceptable harm at scale.

## Deployment and tenant isolation

AWS's official SaaS isolation guidance distinguishes **silo**, **pool**, and **bridge** models. Silo dedicates resources, pool shares resources with policy-based isolation, and bridge mixes approaches per layer. Tenant isolation is fundamental even when infrastructure is shared: [tenant isolation strategies](https://docs.aws.amazon.com/whitepapers/latest/saas-tenant-isolation-strategies/saas-tenant-isolation-strategies.html), [bridge model](https://docs.aws.amazon.com/whitepapers/latest/saas-tenant-isolation-strategies/the-bridge-model.html), and [architecture fundamentals](https://docs.aws.amazon.com/whitepapers/latest/saas-architecture-fundamentals/tenant-isolation.html). **D.**

| Model | Agent use | Benefit | Cost/risk |
|---|---|---|---|
| Pool | Shared gateways/workers/store partitions for low-to-medium-risk Level 1 | Efficiency and simpler operations | Strong policy enforcement, noisy-neighbor and larger blast radius |
| Silo | Dedicated machine worker, regulated/high-risk tenant, isolated secrets/data | Clear boundary and contained failure | Provisioning, utilization, upgrades, fleet complexity |
| Bridge | Shared control plane plus tenant/duty-specific workers, stores, or tool executors | Isolation where authority is highest | More architecture and reconciliation complexity |

Tenant isolation must cover authentication/authorization, threads/checkpoints, memory, datasets/traces, artifacts, cache keys, queues, workers, secrets, tool credentials, network policy, rate/cost budgets, and deletion. A `tenant_id` column or prompt field alone is insufficient.

LangSmith's authentication model separates authentication from authorization and supports owner/resource filters; without custom authentication the runtime may see only the API-key owner, not individual users. Its self-hosted model has different defaults and responsibilities: [auth](https://docs.langchain.com/langsmith/auth), [custom auth](https://docs.langchain.com/langsmith/custom-auth), and [shared responsibility](https://docs.langchain.com/langsmith/shared-responsibility-model). **D.** Apply the same resource-server principles even if using a different deployment platform.

## Chapter 25 figures and screenshots

1. Four-record diagram: checkpoint, queue lease, action outcome, UI projection.
2. Failure between target commit and response, then idempotent reconciliation.
3. Task timeline with queue delay, first useful artifact, intervention, retry, and completion.
4. Budget dashboard by successful task, with step/cost caps visible.
5. Pool/silo/bridge deployment diagram across the three levels.
6. Runtime-observed crash-and-resume trace with synthetic data and target receipt.

### Chapter 25 production gate

- Accepted tasks receive durable IDs and explicit terminal states.
- Checkpoints and side-effect outcomes are separate and reconciled.
- Consequential tools have stable idempotency keys or a documented non-repeatable/manual path.
- Errors are classified; retry layer, limit, backoff, jitter, deadline, and budget are explicit.
- Queue lease/heartbeat and DLQ/redrive procedures are tested.
- Cancellation and compensation semantics are user-visible and runtime-observed.
- First useful artifact, tail latency, queue age, success, recovery, and cost are measured.
- Model routes/fallbacks pass equivalent policy/tool/schema suites.
- Context compaction and caches preserve authorization and state invariants.
- Tenant boundaries cover all state, execution, secrets, caches, and telemetry.
- SLOs and safety invariants have owners, alerts, and incident actions.

# Chapter 26 — Choosing the Right Level

## Chapter thesis

Choose the smallest authority surface that can produce the user outcome. Levels are not maturity badges and do not require a one-way migration. A product can remain Level 1 permanently, invoke an isolated Level 2 worker for one bounded task, or expose a Level 3 organizational front door that delegates narrowly and returns governed artifacts.

## Decision sequence

Ask these questions in order:

1. **Can a deterministic workflow solve it?** If yes, use one. Add a model only where interpretation or adaptive judgment creates measurable value.
2. **Can application-scoped tools solve it?** If yes, keep it Level 1. Typed APIs are easier to authorize, evaluate, and recover than ambient machine access.
3. **Does the outcome inherently require workspace/machine operations?** If it must inspect/change arbitrary files, execute commands, run tests, or operate installed CLIs, use a bounded Level 2 worker.
4. **Does the agent need to be a shared organizational actor?** If multiple people invoke it in channels, it carries a service identity, shared authority, institutional memory, or multi-party accountability, Level 3 governance is required.
5. **Can the higher authority be delegated as one narrow subtask?** Prefer a constrained worker/tool contract over giving the primary agent ambient access.
6. **What is the maximum credible harm?** If controls and recovery cannot bound it, reduce authority or keep the step human-operated.

## Selection matrix

| Dimension | Level 1 — application | Level 2 — machine | Level 3 — organization |
|---|---|---|---|
| Primary surface | Web/mobile/product UI | CLI, IDE, desktop, server, container | Slack/Teams/Discord/shared work systems |
| Best for | Domain objects and typed application actions | Files, commands, tests, local/cloud tooling | Team requests, shared workflows, asynchronous coordination |
| Authority | App APIs and user/tenant state | Filesystem, process, network, credentials | Organizational systems, agent identity, delegation, shared memory |
| Default identity | End user plus app agent | Operator plus machine worker | Requester plus organizational agent principal and approver |
| Isolation unit | User/tenant/thread | Workspace/container/VM/credential scope | Tenant/workspace/channel plus isolated delegated workers |
| Human control | Domain write approval/edit | Scope, command, diff, publish/deploy approval | Policy-bound identity/quorum approvals |
| Dominant failure | Wrong app mutation/state conflict | System compromise/exfiltration/unsafe code | Confused deputy/cross-team leakage/organizational misuse |
| Operations burden | Lowest | High fleet/sandbox/recovery burden | Highest governance, identity, memory, audit, and change-management burden |
| Canonical book reference | Personal finance app | Hermes-CopilotKit supervision case | Channels/OpenTag governance case |

## Knobs to compare before choosing

Score each candidate architecture explicitly:

- **Surface:** where users initiate, inspect, interrupt, and recover work.
- **Runtime:** request loop, durable graph, worker queue, or managed agent service.
- **Models:** capability, route, fallback, privacy, residency, latency, cost.
- **Tools:** typed app API, MCP, filesystem, shell, browser, organizational service.
- **State:** task, thread, memory, artifacts, side-effect outcomes.
- **Identity:** user, agent service identity, delegated subject, target principal.
- **Isolation:** tenant, workspace, container/VM, network, secrets, channel.
- **Human control:** interrupt location, approver identity, expiry, quorum, undo.
- **Evaluation:** tool/state/policy/trajectory/recovery suites.
- **Observability:** domain trace, service telemetry, action ledger, SLOs.
- **Operations:** deployment, on-call, cost, capacity, upgrades, incidents, retirement.

The winning architecture is not the one with the most green boxes. It is the least complex system that satisfies the product outcome and risk constraints.

## When no agent is the right answer

Use a deterministic workflow or ordinary UI when:

- the path and inputs are known;
- correctness must be exact and rules can express it;
- the model would only choose among a tiny stable set of steps;
- the user needs a form, filter, or query rather than delegation;
- an error's harm cannot be bounded or reversed;
- the organization cannot operate the identity, audit, and incident obligations;
- evaluation cannot define acceptable behavior;
- the cost/latency variance adds no user value.

An LLM can still assist at a narrow boundary—classifying text, extracting a draft, or suggesting a plan—without owning execution.

## Upgrade triggers

### Level 1 to Level 2

Justified when the required work cannot be represented safely as application APIs and genuinely needs arbitrary workspace inspection, file modification, commands, installed tools, or environment feedback. Before upgrading, define:

- dedicated worker and workspace lifecycle;
- filesystem/network/process/credential policy;
- task scope and allowed artifacts;
- diff/test/verification contract;
- approval and external-write boundary;
- cancellation, compensation, and cleanup;
- security and recovery evaluation suites.

The `GTM Operations Workspace` to Hermes seam is a useful reference for the interface transition, but `hermes-cpk` remains an unsafe baseline until the external runtime is pinned and these controls are implemented and observed.

### Level 1 or 2 to Level 3

Justified when the agent must act as a shared organizational participant rather than merely expose the same personal app in chat. Triggers include multiple requesters, shared channels, service identity, organization tools, channel policy, multi-party approval, durable shared memory, schedules, or asynchronous responsibility.

Before upgrading, define requester/agent/delegate/approver identities; tenant/workspace/channel scope; authorization policy; retention and institutional-memory governance; action ledger; support/incident ownership; and agent decommissioning.

## Hybrid architectures

### Pattern A — Level 1 control plane, Level 2 worker

```text
CopilotKit application
  -> user defines goal and approves bounded scope
  -> durable orchestrator creates signed task specification
  -> disposable machine worker receives narrow capability
  -> worker returns diff, logs, tests, and artifact manifest
  -> application shows evidence and requests publish/merge approval
```

Use for repository migrations, data preparation, or long-running local work. The Level 1 app owns user control and durable task state; the Level 2 worker owns isolated machine execution. It does not receive all of the user's ambient credentials.

### Pattern B — Level 3 front door, Level 1 domain service

```text
Slack/Teams request
  -> organizational agent authenticates requester and channel policy
  -> invokes typed application tool under constrained delegated identity
  -> Level 1 service enforces tenant/resource authorization
  -> result and receipt return to channel
```

Use when the action already belongs to a domain API. Do not add a machine worker just because the request begins in a channel.

### Pattern C — Level 3 supervisor, Level 2 delegated worker

```text
organization request + policy
  -> organizational agent creates bounded task
  -> authorized approval for machine scope
  -> isolated Level 2 worker executes
  -> artifacts and provenance return
  -> separate approval for external organizational write
```

This has the largest blast radius. Use separate credentials, policy decisions, budgets, logs, and approval steps for delegation and publication. A channel mention is not permission to change a machine or merge code.

### Pattern D — Downshift after discovery

Start with an agent to discover the variable workflow, instrument trajectories, then replace stable branches with deterministic nodes and narrow tools. Keep the model at the genuinely adaptive boundary. This is often the best production migration because it reduces cost, latency, variance, and authority.

## Architecture decision record template

```markdown
# Agent authority decision

Outcome required:
Why a deterministic workflow is insufficient:
Selected level(s):
Maximum credible harm:

User surface:
Runtime and durability:
Model route/fallback policy:
Tools and side effects:
State and memory:
Identity/delegation chain:
Isolation boundary:
Human intervention/approval:
Evaluation gates:
Observability/action ledger:
SLOs and budgets:
Incident/kill/compensation owner:

Rejected lower-authority design and why:
Conditions that force redesign or downshift:
Publication/runtime evidence status:
```

## Chapter 26 figures and exercise

1. Decision tree that begins with deterministic workflow, not Level 1.
2. Three-level comparison using the eleven recurring knobs.
3. Hybrid diagram: Level 3 request -> Level 2 worker -> Level 1 dashboard, with identity and approval boundaries marked.
4. “Downshift” diagram showing adaptive agent branches becoming deterministic nodes.
5. Reader exercise: choose an architecture for five cases and defend the smallest authority surface.

Suggested cases:

- categorize transactions and propose a monthly budget;
- migrate a TypeScript repository and run tests;
- answer a shared channel question from approved documentation;
- create a production ticket after team approval;
- deploy a change across customer environments.

### Chapter 26 production gate

- The team documents why a deterministic workflow or lower level is insufficient.
- Every higher-authority capability maps to a required user outcome.
- Hybrid boundaries use narrow typed task contracts and separate identities.
- Runtime, state, tools, identity, isolation, HITL, evaluation, observability, and operations are owned.
- Maximum credible harm, kill path, and recovery owner are explicit.
- The architecture can downshift or disable autonomy without losing core product access.
- The selected design passes the gates from Chapters 23–25.

# Cross-chapter production scorecard

Score each item 0–3: 0 absent, 1 demo-only, 2 implemented/source-present, 3 runtime-observed under failure/adversarial conditions. Any zero in identity, authorization, isolation, side-effect correctness, recovery, or observability blocks a production claim.

| Area | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Evaluation | Ad hoc prompts | Happy-path examples | Versioned multi-layer suites | Production loop and calibrated online evals |
| Trajectory safety | Final answer only | Manual trace review | Required/forbidden trajectory gates | Adversarial and online drift coverage |
| Identity/auth | Ambient/shared | Login only | Per-resource actor/agent policy | Delegation, revocation, cross-tenant tests |
| Tools | Arbitrary/unvalidated | Schemas | Risk manifests and enforcement | Abuse-tested, idempotent, auditable |
| Isolation | None | Logical convention | Enforced tenant/workspace boundary | Escape and cross-scope tests observed |
| Persistence | In memory | Conversation history | Checkpoints/durable queue | Crash/restore/reconcile drills |
| Side effects | At-most hope | UI confirmation | Idempotency/outcome ledger | Ambiguous-outcome and compensation drills |
| Cancellation | Close UI | Stop tokens | Cooperative task cancellation | Domain compensation/manual recovery tested |
| Streaming | Spinner | Tokens | Structured lifecycle/state/artifacts | Reconnect, replay, backpressure tested |
| Cost | Unknown | Dashboard | Step/time/cost budgets | Per-success optimization and admission control |
| Observability | Logs | Agent traces | OTel + agent trace + metrics | Correlated alerts and incident runbooks |
| Audit | Debug trace | Tool log | Consequential action ledger | Tamper evidence and reconciliation |
| SLOs | None | Uptime | Journey SLIs/objectives | Error-budget policy and burn alerts |
| Tenant isolation | Shared implicit | Tenant field | Resource-enforced pool/silo/bridge | Continuous cross-tenant and recovery tests |

# Drafting map for Chapters 23–26

| Chapter | Opening failure | Core build | Repository anchor | Closing production gate |
|---|---|---|---|---|
| 23 | Correct-looking finance answer duplicated a write | Build dataset/eval pyramid and correlated telemetry | All references; finance trajectory first | Whole-system eval and production-regression loop |
| 24 | Repository or channel content hijacks an overpowered agent | Threat model and enforce authority outside prompt | Finance -> Hermes -> OpenTag gradient | Attack suite, identity, sandbox, ledger, kill drills |
| 25 | Worker dies after external commit; retry duplicates action | Checkpoint + queue + idempotency + streaming + SLOs | Harden finance write, then Hermes worker | Recovery, budgets, isolation, and SLO gates |
| 26 | Team chose machine/organization authority for an app-level job | Apply decision tree and compose a narrow hybrid | Compare all audited references honestly | Smallest sufficient authority ADR |

Recommended manuscript ratio for each chapter:

1. one concrete failure story;
2. one mental model;
3. one architecture figure;
4. one buildable code/config sequence;
5. one adversarial/failure test;
6. one repository boundary note;
7. one production checklist.

# Publication drift and verification ledger

Recheck immediately before code freeze:

- LangChain/LangGraph middleware, fault-tolerance, dynamic-model, auth, and cancellation API versions;
- `agentevals` package/repository release and trajectory matcher signatures;
- LangSmith plan-specific online evaluation, retention, auth, deployment, and cost behavior;
- OpenTelemetry GenAI semantic-convention stability status and exact release;
- OWASP Agentic Top 10 and Agentic Skills project revisions;
- NIST AI RMF revision status and any final agent identity/authorization publication replacing the concept paper;
- CopilotKit Channels package names and managed availability;
- OpenTag migration and managed branch availability;
- all model/provider pricing, token, caching, tool, and fallback behavior;
- every audited repository commit, license, install, test, runtime, and screenshot record.

Do not print volatile numeric defaults—retry counts, retention periods, pricing, context windows, cache thresholds, queue limits, or plan entitlements—without a dated footnote and pinned source. Prefer showing the knob and how to choose it.

# Primary-source registry

All links accessed 2026-07-14 unless the page itself gives another publication date.

## Evaluation and observability

- LangSmith: [Evaluation](https://docs.langchain.com/langsmith/evaluation); [evaluation types](https://docs.langchain.com/langsmith/evaluation-types); [evaluation concepts](https://docs.langchain.com/langsmith/evaluation-concepts); [evaluators](https://docs.langchain.com/langsmith/evaluators); [evaluation approaches](https://docs.langchain.com/langsmith/evaluation-approaches); [trajectory evaluation](https://docs.langchain.com/langsmith/trajectory-evals); [datasets](https://docs.langchain.com/langsmith/manage-datasets); [rules](https://docs.langchain.com/langsmith/rules); [trace sampling](https://docs.langchain.com/langsmith/sample-traces); [experiment configuration](https://docs.langchain.com/langsmith/experiment-configuration); [cost tracking](https://docs.langchain.com/langsmith/cost-tracking); [observability concepts](https://docs.langchain.com/langsmith/observability-concepts); [OTel tracing](https://docs.langchain.com/langsmith/trace-with-opentelemetry); [OTel evaluation](https://docs.langchain.com/langsmith/evaluate-with-opentelemetry); [TTFT](https://docs.langchain.com/langsmith/log-llm-trace).
- LangChain: official [`agentevals`](https://github.com/langchain-ai/agentevals) repository.
- OpenTelemetry: [concepts](https://opentelemetry.io/docs/concepts/); [traces](https://opentelemetry.io/docs/concepts/signals/traces/); [metrics](https://opentelemetry.io/docs/concepts/signals/metrics/); [sampling](https://opentelemetry.io/docs/concepts/sampling/); [sensitive data](https://opentelemetry.io/docs/security/handling-sensitive-data/); [baggage](https://opentelemetry.io/docs/concepts/signals/baggage/); [semantic conventions](https://opentelemetry.io/docs/specs/semconv/); [GenAI metrics source](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-metrics.md); [GenAI spans source](https://github.com/open-telemetry/semantic-conventions/blob/main/model/gen-ai/spans.yaml).

## Security and identity

- OWASP GenAI Security Project: [Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/); [official PDF](https://genai.owasp.org/download/52117/?tmstv=1765059207); [Agentic AI threats and mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/); [Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/top10.html).
- NIST/NCCoE: [`NIST AI 800-5`](https://www.nist.gov/publications/summary-analysis-responses-request-information-regarding-security-considerations-ai); [agent identity/authorization concept paper](https://www.nccoe.nist.gov/sites/default/files/2026-02/accelerating-the-adoption-of-software-and-ai-agent-identity-and-authorization-concept-paper.pdf); [SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final); [SP 800-207A](https://csrc.nist.gov/pubs/sp/800/207/a/final); [SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final); [AI RMF](https://www.nist.gov/itl/ai-risk-management-framework).
- LangSmith: [authentication and access control](https://docs.langchain.com/langsmith/auth); [custom authentication](https://docs.langchain.com/langsmith/custom-auth); [shared responsibility](https://docs.langchain.com/langsmith/shared-responsibility-model); [workload isolation](https://docs.langchain.com/langsmith/workload-isolation).

## Reliability, cost, and deployment

- LangGraph: [persistence](https://docs.langchain.com/oss/python/langgraph/persistence); [Functional API](https://docs.langchain.com/oss/python/langgraph/functional-api); [thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph); [fault tolerance](https://docs.langchain.com/oss/python/langgraph/fault-tolerance).
- LangSmith Deployment: [cancel runs](https://docs.langchain.com/langsmith/cancel-run); [scalability and resilience](https://docs.langchain.com/langsmith/scalability-and-resilience).
- LangChain: [agents/dynamic models](https://docs.langchain.com/oss/python/langchain/agents); [models and prompt caching](https://docs.langchain.com/oss/python/langchain/models); [middleware overview](https://docs.langchain.com/oss/python/langchain/middleware/overview); [built-in middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in); [tools](https://docs.langchain.com/oss/python/langchain/tools); [MCP interceptors](https://docs.langchain.com/oss/python/langchain/mcp).
- AWS: [SQS queue types](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-queue-types.html); [visibility timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html); [DLQ configuration](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-dead-letter-queue.html); [DLQ redrive](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-dead-letter-queue-redrive.html); [timeouts/retries/backoff/jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/); [correlated failures](https://aws.amazon.com/builders-library/minimizing-correlated-failures-in-distributed-systems/); [tenant isolation strategies](https://docs.aws.amazon.com/whitepapers/latest/saas-tenant-isolation-strategies/saas-tenant-isolation-strategies.html); [bridge model](https://docs.aws.amazon.com/whitepapers/latest/saas-tenant-isolation-strategies/the-bridge-model.html); [SaaS tenant isolation fundamentals](https://docs.aws.amazon.com/whitepapers/latest/saas-architecture-fundamentals/tenant-isolation.html).
- Google SRE: [Service Level Objectives](https://sre.google/sre-book/service-level-objectives/); [Implementing SLOs](https://sre.google/workbook/implementing-slos/); [error-budget policy](https://sre.google/workbook/error-budget-policy/); [burn-rate alerting](https://docs.cloud.google.com/stackdriver/docs/solutions/slo-monitoring/alerting-on-budget-burn-rate).

# Final handoff notes

- Treat code in this packet as publication candidates or editorial pseudocode until pinned, compiled, tested, and captured in the companion repository.
- Use synthetic finance, repository, and channel data in every screenshot. Record commit, dependency lock, model, prompt, policy, dataset, seed where applicable, environment, timestamp, and redaction review.
- Show one failing run before each hardening change and the corresponding passing run after it. A screenshot of a green UI without a trace, target receipt, and evidence label is illustration, not proof.
- Preserve the current repository audit language: the finance app, GTM Operations Workspace, Hermes integration, Channels, and OpenTag demonstrate valuable seams and interaction patterns. Production authentication, isolation, recovery, governance, and immutable audit remain work to implement and runtime-verify.
- End Chapter 26 by returning to the book promise: a production engineer in 2026 is not the person who knows the most agent frameworks. It is the person who can choose the right authority, expose the right controls, measure the real trajectory, and operate failure safely.

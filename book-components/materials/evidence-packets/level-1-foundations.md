---
title: "Evidence Packet — Foundations and Level 1 Application Agents"
book: "Builder's Guide to Agentic Applications 2026"
scope: "Chapters 1–10"
status: "research packet; not chapter prose"
access_date: "2026-07-14"
copilotkit_source_sha: "855446e1abc8f29756dc5e539e5e50a90321ac2d"
personal_finance_source_sha: "d8760064c626712a8fa15c192a8c4bc69bb24055"
gtm_os_source_sha: "private revision omitted"
---

# Foundations and Level 1 evidence packet

This packet is the fact base, implementation inventory, figure brief, and editorial guardrail set for Chapters 1–10. It is deliberately not continuous book prose. Every implementation claim should be converted into reader-facing language only after the companion code has been pinned, run, and captured. Unless a source row says otherwise, links were accessed on **2026-07-14**.

## Evidence labels used in this packet

| Label | Meaning | Publication treatment |
| --- | --- | --- |
| **D — documented** | A current official documentation page states the behavior. | May be taught, but version-sensitive API details still require a publication pin. |
| **S — source-present** | The behavior or API is visible in source at an immutable commit. | May be described as source evidence, not as a successful local run. |
| **R — runtime-verified** | A maintainer ran the exact companion example and recorded environment, command, result, and capture. | May be presented as demonstrated behavior. None of the findings in this research-only packet are promoted to R. |
| **A — aspirational** | Proposed architecture, missing production control, or future companion implementation. | Must be labeled as a target or exercise, never as already implemented. |
| **E — editorial synthesis** | A book-specific definition or recommendation inferred from multiple primary sources. | Phrase as the authors' model, with the evidence immediately adjacent. |

The strongest discipline for this book is simple: **source presence is not runtime proof**. Repository screenshots and code paths are usable evidence, but until the release companion is run and captured under a recorded environment they remain S, not R.

## Executive findings

1. **“Chatbot,” “workflow,” “agent,” and “agentic application” belong to different conceptual layers.** Chat is an interaction form; a workflow is a predetermined execution path; an agent dynamically chooses actions and tool use; an agentic application is the complete product system surrounding one or more agents. This editorial taxonomy is grounded in LangGraph's current workflow/agent distinction and LangChain's model-versus-agent execution model. [LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) and [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents) (**D/E**, accessed 2026-07-14).

2. **Tool calling alone does not prove useful autonomy.** A standalone model can emit a tool call while application code still has to execute it and decide whether to loop. LangChain's model documentation makes that boundary explicit; its agent abstraction supplies the model–tool loop. [LangChain models](https://docs.langchain.com/oss/python/langchain/models) and [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents) (**D**, accessed 2026-07-14).

3. **The canonical CopilotKit surface for new 2026 examples is the v2 hook set.** The current reference enumerates `useAgent`, `useCopilotKit`, `useFrontendTool`, `useHumanInTheLoop`, `useInterrupt`, `useRenderTool`, `useComponent`, and `useDefaultRenderTool`. The pinned package source exposes v2 and headless entry points while retaining v1 compatibility. [CopilotKit reference](https://docs.copilotkit.ai/reference) (**D**) and [`@copilotkit/react-core` exports at `855446e`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/package.json) (**S**, accessed 2026-07-14).

4. **`useDefaultTool` is legacy, not the API to teach as current.** GTM Operations Workspace uses the classic `useDefaultTool` wildcard catch-all. In the pinned current source, that hook is implemented through the legacy action system, while the v2 wildcard renderer is `useDefaultRenderTool` or `useRenderTool({ name: "*", ... })`. GTM Operations Workspace (**S**), [legacy `useDefaultTool`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/src/hooks/use-default-tool.ts) (**S**), and [v2 `useDefaultRenderTool`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/src/v2/hooks/use-default-render-tool.tsx) (**S**, accessed 2026-07-14).

5. **Frontend tools, rendered backend tools, and human-in-the-loop tools solve different jobs.** A frontend tool executes in the browser or client; `useRenderTool` adds UI for a tool executed elsewhere; `useHumanInTheLoop` intentionally blocks until `respond` is called. Conflating them creates security and UX errors. [`useFrontendTool` source](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/src/v2/hooks/use-frontend-tool.tsx), [`useRenderTool` source](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/src/v2/hooks/use-render-tool.tsx), and [`useHumanInTheLoop` source](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/src/v2/hooks/use-human-in-the-loop.tsx) (**S**, accessed 2026-07-14).

6. **AG-UI is the observable event contract, not the agent's hidden reasoning.** It defines run, step, message, tool-call, state, activity, and optional reasoning event families. The book should expose operational evidence—plans, calls, state changes, sources, and approvals—without promising chain-of-thought. [AG-UI events concept](https://docs.ag-ui.com/concepts/events) and [AG-UI JavaScript event types](https://docs.ag-ui.com/sdk/js/core/events) (**D**, accessed 2026-07-14).

7. **`BuiltInAgent` and LangGraph are not interchangeable runtime choices.** `BuiltInAgent` is a convenient in-process model/tool loop with AG-UI events and configurable step limits. LangGraph adds explicit graphs, durable checkpoints, thread-scoped state, interrupts, recovery, and stores. Use the former for constrained application agents and the latter when execution topology or durability is a first-class requirement. [`BuiltInAgent` pinned source](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/runtime/src/agent/index.ts) (**S**), [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence), and [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) (**D**, accessed 2026-07-14).

8. **The personal-finance example is valuable as a product pattern, not yet a production-finance claim.** It demonstrates a custom React Native chat shell, frontend read tools, four write approval gates, a server-side `BuiltInAgent`, and a runtime route. It does not demonstrate authentication, tenant isolation, durable threads, or a LangGraph backend. Exact evidence appears later in this packet.

9. **Mobile is not merely a narrower web viewport.** Device addressing, backgrounding, interrupted streams, native render registration, attachment permissions, and app lifecycle must be designed explicitly. The current React Native source and the current quickstart disagree on manual polyfills and availability of prebuilt components; version-pinned source must control the book's code, and the prose must be rechecked at publication. [`@copilotkit/react-native` package source](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-native/src/index.ts) (**S**) and [CopilotKit React Native quickstart](https://docs.copilotkit.ai/react-native) (**D**, accessed 2026-07-14).

10. **“Stop,” “cancel,” “interrupt,” “disconnect,” “rollback,” and “undo” are not synonyms.** CopilotKit can abort a client run and signal frontend handlers; a dropped stream need not cancel backend work; LangGraph/LangSmith distinguish interrupt/cancel behavior from rollback; none of these automatically compensates an already completed external side effect. [`stopAgent` source](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/core/src/core/core.ts), [LangSmith cancel or rollback](https://docs.langchain.com/langsmith/cancel-run), and [LangGraph join/rejoin](https://docs.langchain.com/oss/python/langchain/frontend/join-rejoin) (**S/D**, accessed 2026-07-14).

## Claim-to-chapter map

| Chapter | Claims the chapter may safely make | Required evidence or companion artifact | Claims to defer |
| --- | --- | --- | --- |
| **1. The three levels** | Levels describe operating surfaces and expanding authority: application, machine, organization. Level 1 is scoped to a product UI and its APIs/state. | Three-level comparison figure; one cross-level delegation sequence; authors' E label. | That the levels are an industry standard or strict maturity ladder. |
| **2. What makes an app agentic** | Workflow paths are predetermined; agent paths/tool selection are dynamic; chat is an interface, not proof of agency. | Taxonomy table and small executable contrast: model call, workflow, agent loop. | That every tool-calling chat UI is an autonomous agent. |
| **3. The Level 1 stack** | CopilotKit handles the application interaction layer; AG-UI carries observable events; a runtime such as BuiltInAgent or LangGraph performs execution; tools reach product systems. | One architecture figure with trust boundaries; current package/version register. | That CopilotKit itself provides every persistence, identity, or policy control. |
| **4. The agentic UI problem** | Agent work is streamed, partial, fallible, interruptible, and may outlive a request. UI must represent progress, state, evidence, and recovery. | State-machine figure; latency/cancel semantic table; screenshots of in-progress, approval, recovery. | Fake percent-complete or hidden, automatic undo claims. |
| **5. Anatomy and execution** | Separate model, tools, state, memory, policy/planning, runtime, identity/authority, and interface. Define run/step/tool call/thread carefully. | Terminology matrix with AG-UI, LangGraph, and LangSmith caveats. | A universal “step” definition across protocols/vendors. |
| **6. Tools and boundaries** | Frontend, backend, and external-service tools have different trust, latency, and credential properties. Schema validation is not authorization. | Tool placement decision table; frontend read and server write snippets. | Putting secrets or privileged writes in browser handlers. |
| **7. Tool-based Generative UI** | Registered application components render semantic tool/state objects; `useComponent`, `useRenderTool`, and `useDefaultRenderTool` have distinct roles. | One display, one interactive tool, one approval component, plus lifecycle states. | Arbitrary model-generated production frontend code as the default pattern. |
| **8. Shared state, threads, persistence** | State snapshots/deltas synchronize visible task state; LangGraph checkpoints are thread-scoped; stores support cross-thread memory. | State ownership table; conflict example; reconnect/resume test. | Treating a React state object, a checkpoint, and long-term memory as the same thing. |
| **9. Human intervention** | `useHumanInTheLoop` provides a client blocking tool pattern; LangGraph `interrupt` is runtime-enforced and resumes from a checkpoint. | Contextual approval UI; idempotency test across resume; rejection/edit branches. | Calling a client approval card a security boundary by itself. |
| **10. Ship a Level 1 app** | A finance copilot can demonstrate web/mobile interaction, read tools, proposed writes, approvals, and server execution. | Pinned runnable companion, synthetic data, recorded commands, fresh screenshots, smoke/e2e tests. | Production-grade finance, durable execution, or tenant security until implemented and tested. |

# I. Foundations

## 1. A precise taxonomy for builders

The book should declare the following as its own operating definitions, not quote them as universal consensus.

| Term | Book definition | Decision authority | Typical loop | Evidence status |
| --- | --- | --- | --- | --- |
| **Chatbot** | A conversational user interface that exchanges messages. It may front a simple model call, a fixed workflow, or an agent. | Undefined by the UI alone. | `message → response` is the minimal form. | **E** |
| **Model-powered feature** | Application code invokes a model for generation, extraction, classification, or structured output. | Application code determines when and why the call happens. | Usually one bounded call, possibly retried. | **E/D**, supported by [LangChain model interfaces](https://docs.langchain.com/oss/python/langchain/models). |
| **Tool-using assistant** | A model can request typed tools, but the surrounding application may still control a fixed execution policy. | Shared between model selection and application loop. | `model → requested tool → application executes → model/final`. | **E/D**, supported by [LangChain tool calling](https://docs.langchain.com/oss/python/langchain/tools). |
| **Workflow** | A program with a predetermined path or graph; individual nodes may contain model calls. | Developer-authored routing dominates. | Known nodes/edges with conditional branches. | **D**, [LangGraph workflow definition](https://docs.langchain.com/oss/python/langgraph/workflows-agents). |
| **Agent** | A runtime in which a model dynamically chooses actions and tool usage, observes results, and continues until a stop condition, limit, interruption, or completion. | Model within runtime, tool, budget, and policy constraints. | `goal → decide → act → observe → update → repeat/pause/finish`. | **D/E**, [LangChain agent loop](https://docs.langchain.com/oss/python/langchain/agents). |
| **Agentic application** | The product system users actually experience: agent runtime, interface, tools, typed state, memory, identity, policy, observability, evaluation, and human control. | Distributed across user, application, runtime, model, and organization policy. | One or more runs across a durable product surface. | **E** |

### Editorial tests for the phrase “agentic”

A Level 1 application earns the adjective only when the manuscript can answer most of these questions with concrete implementation evidence:

1. What user goal persists beyond a single response?
2. Which actions may the runtime choose dynamically?
3. What observations can change the next action?
4. Where is task state represented apart from prose messages?
5. What ends, pauses, or limits the loop?
6. Which actions are visible to the user while they occur?
7. Which state can the user edit or correct?
8. What requires human approval, and is the gate enforced at the right boundary?
9. Can the run be cancelled, resumed, retried, or recovered?
10. Who or what identity authorizes each side effect?

If a feature only turns one prompt into one answer, call it a model-powered feature. If code owns the route, call it a workflow. If the model selects among actions inside a controlled loop, call it an agent. This vocabulary protects the reader from architecture inflation.

### The three levels are surfaces, not a scoreboard

| Dimension | Level 1: application agents | Level 2: machine agents | Level 3: organizational agents |
| --- | --- | --- | --- |
| Primary surface | Web, mobile, or product UI | CLI, IDE, workstation, container | Slack, Teams, Discord, shared operational systems |
| Default context | Current user, document, page, account, app state | Filesystem, processes, shell, installed tools | Channel/thread, team systems, organizational policy |
| Typical authority | Product APIs and user-visible shared state | Files, commands, network, credentials | Delegated organizational identity and cross-system workflows |
| Main control problem | State synchronization and legible interaction | Sandboxing, permissions, command/file boundaries | Identity, delegation, provenance, multi-stakeholder approval |
| Level 1 book emphasis | CopilotKit interaction primitives and LangChain/LangGraph runtime choices | Preview only in Chapter 1 | Preview only in Chapter 1 |

These levels can compose. A request in a shared channel can initiate an organizational run, delegate bounded repository work to a machine agent, and stream status to an application dashboard. The expansion is authority and blast radius, not an assertion that Level 3 is always “more advanced.” **E**

## 2. Anatomy of an agentic application

The earlier six-part anatomy—model, tools, state, memory, planning/policy, runtime—is necessary but insufficient for production teaching. Level 1 should use nine parts:

| Part | Builder question | Common failure if omitted |
| --- | --- | --- |
| **Model** | Which model, structured-output mode, tool-call behavior, context budget, and fallback? | Product behavior changes silently across model upgrades. |
| **Tools** | What can be read, computed, or changed; where does each tool execute? | Secrets leak client-side or writes bypass validation. |
| **Task state** | What typed facts describe current progress, artifacts, and decisions? | UI and agent maintain incompatible stories. |
| **Memory** | What persists across steps, runs, threads, users, or the organization? | Sensitive or stale facts become permanent context. |
| **Policy and planning** | What may the runtime choose, when must it stop, ask, or escalate? | Unbounded or unauditable autonomy. |
| **Runtime** | How are loops, events, retries, timeouts, checkpoints, and interrupts executed? | A dropped request destroys work or repeats side effects. |
| **Identity and authority** | Which principal is acting, for which tenant, with which scopes? | A pleasant approval UI masks an unauthorized action path. |
| **Interface** | What progress, evidence, state, approval, cancellation, and recovery does the user see? | Long-running work becomes an opaque spinner. |
| **Operations** | How are traces, evaluations, cost, incidents, retention, and version drift managed? | A convincing demo cannot be debugged or safely shipped. |

The chapter should render these as a cutaway rather than a linear stack. State, policy, identity, and operations cross every layer.

## 3. Run, step, tool call, message, thread, checkpoint, and trace

The manuscript must avoid presenting one vendor's nouns as universal. Use the following book lexicon and show mappings.

| Book term | Working definition | Protocol/runtime mapping | Important caveat |
| --- | --- | --- | --- |
| **Run** | One user-visible attempt to pursue a goal under a start/terminal lifecycle. | AG-UI emits `RUN_STARTED`, then `RUN_FINISHED` or `RUN_ERROR`. [AG-UI events](https://docs.ag-ui.com/sdk/js/core/events) (**D**). | LangSmith also calls each traced span a “run”; a trace contains multiple runs. [LangSmith observability concepts](https://docs.langchain.com/langsmith/observability-concepts) (**D**). State which meaning is intended. |
| **Step** | A named unit of execution within the user-visible run. | AG-UI supplies `STEP_STARTED`/`STEP_FINISHED`; the emitter chooses the step name. | A step is not guaranteed to equal one model thought, one graph node, or one tool call. Never market it as exposed reasoning. |
| **Tool call** | A structured request to invoke a named capability with arguments, followed optionally by a result. | AG-UI start/args/end/result events. | An event saying a call was requested is not proof its external side effect completed. |
| **Message** | A conversational artifact with role, content, and lifecycle. | AG-UI text-message start/content/end or messages snapshot. | Messages are one projection of state, not the whole state model. |
| **Thread** | A stable conversation/task container joining related runs and state. | LangGraph checkpointers index checkpoints by `thread_id`; deployment threads can hold many runs. [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) and [LangSmith threads](https://docs.langchain.com/langsmith/use-threads) (**D**). | A browser chat array is not automatically a durable thread. |
| **Checkpoint** | Persisted runtime state at a recoverable execution boundary. | LangGraph writes checkpoints at graph super-steps. | Checkpoint restoration does not reverse a payment, email, or other side effect already accepted elsewhere. |
| **Store/memory** | Data intentionally available beyond one thread. | LangGraph store is cross-thread; checkpointer is thread-scoped. [LangGraph JS persistence](https://docs.langchain.com/oss/javascript/langgraph/persistence) (**D**). | Retention, provenance, access, correction, and deletion must be designed. |
| **Trace** | An observability record for an operation composed of spans/runs. | LangSmith trace model. | A trace is not application state and should not be used as the product database. |

### Minimal execution sequence for the book

```text
User goal
  → create or select thread
  → RUN_STARTED
  → read typed state and policy
  → STEP_STARTED("plan" or runtime-defined name)
  → model chooses response or tool call
  → tool call events / tool execution
  → state snapshot or delta
  → checkpoint where supported
  → continue, interrupt, fail, cancel, or finish
  → RUN_FINISHED | RUN_ERROR
```

AG-UI uses start/content/end patterns for streamed messages and calls, snapshot/delta patterns for synchronized state, and lifecycle patterns for runs. [AG-UI event architecture](https://docs.ag-ui.com/concepts/events) (**D**, accessed 2026-07-14). This sequence is an explanatory projection, not a guarantee that every runtime emits every optional event.

# II. Level 1 architecture and UI

## 4. Reference architecture and trust boundaries

```text
┌──────────────── Web or native application ────────────────┐
│ Product UI                                                 │
│  ├─ task surface / chat                                    │
│  ├─ shared-state views                                     │
│  ├─ rendered tool calls                                    │
│  └─ human guidance / approval                              │
│               CopilotKit hooks + AG-UI client              │
└───────────────────────┬────────────────────────────────────┘
                        │ authenticated AG-UI/HTTP boundary
┌───────────────────────▼────────────────────────────────────┐
│ Agent runtime                                               │
│  Option A: BuiltInAgent — constrained in-process loop       │
│  Option B: LangGraph — explicit stateful/durable graph      │
│  ├─ model and tool policy                                   │
│  ├─ server-side tools and credentials                       │
│  ├─ checkpoints / memory where configured                   │
│  └─ trace and evaluation hooks                              │
└───────────────────────┬────────────────────────────────────┘
                        │ least-privilege service identities
┌───────────────────────▼────────────────────────────────────┐
│ Product APIs, databases, queues, external services          │
└────────────────────────────────────────────────────────────┘
```

**E:** CopilotKit should be described as the interaction layer rather than the security perimeter. AG-UI carries observable interaction events. Authentication, authorization, tenant isolation, durable persistence, and business invariants must still be enforced by the application and runtime.

## 5. Why conventional UI assumptions fail

| Conventional assumption | Agentic reality | Required product response |
| --- | --- | --- |
| A click produces a fast deterministic result. | A goal may initiate multiple model/tool steps with uncertain latency. | Show stages, current action, first useful artifact, and a truthful wait state. |
| Final text is the result. | Sources, records, plans, diffs, charts, and approvals may be the real work product. | Render typed artifacts in product-native components. |
| The frontend is the sole state owner. | Runtime and user may both update task state. | Define field ownership, versioning/reducers, merge rules, and conflicts. |
| Failure ends the request. | The runtime may retry, branch, ask, resume, or partially complete. | Distinguish retriable, blocked, partial, cancelled, and terminal states. |
| A spinner is adequate progress. | The number of remaining steps may not be knowable. | Prefer stage/event progress over fabricated percentages. |
| Cancel means undo. | Abort may stop only future work; completed side effects remain. | Name cancellation semantics and expose compensation separately. |
| Approval is one generic “Allow” button. | Consequential actions differ by target, scope, reversibility, and authority. | Show proposed action, exact arguments, target, evidence, impact, and acting principal. |
| Reconnecting restarts the same request. | A stream disconnect may leave backend work running. | Use stable threads/run IDs and a join/rejoin strategy. [LangGraph join/rejoin](https://docs.langchain.com/oss/python/langchain/frontend/join-rejoin) (**D**). |

### UI state model to teach

Do not reduce the UI to `running: boolean`. A production-shaped task surface needs at least:

```ts
type TaskPhase =
  | "idle"
  | "planning"
  | "running"
  | "waiting_for_user"
  | "retrying"
  | "partially_complete"
  | "cancel_requested"
  | "cancelled"
  | "failed"
  | "complete";
```

This is a proposed book type (**A/E**), not a claim about a CopilotKit export. The companion should derive it from observable run, tool, interrupt, and application events and must test invalid transitions.

## 6. AG-UI event families the reader should recognize

| Event family | Representative events | Product use | Misuse to avoid |
| --- | --- | --- | --- |
| Run lifecycle | `RUN_STARTED`, `RUN_FINISHED`, `RUN_ERROR` | Task status, run IDs, terminal outcome, error recovery. | Marking success before the terminal event or external verification. |
| Step lifecycle | `STEP_STARTED`, `STEP_FINISHED` | Stage timeline and activity labels. | Calling steps chain-of-thought or assuming a universal granularity. |
| Text message | start, content chunks, end | Token streaming and partial conversational response. | Rebuilding semantic state by parsing prose. |
| Tool call | start, streamed args, end, result | Active tool UI, argument preview, result card, audit timeline. | Treating unvalidated partial JSON as executable arguments. |
| State | `STATE_SNAPSHOT`, `STATE_DELTA` | Shared semantic task state and reconnect synchronization. | Blind last-writer-wins on jointly edited fields. |
| Message snapshot | `MESSAGES_SNAPSHOT` | Full conversational synchronization. | Treating message snapshot as all task memory. |
| Activity | activity snapshot/delta | Long-running progress and custom runtime activity. | Fake precision or permanent noisy logs in primary UI. |
| Reasoning-related | optional reasoning events | Only provider/runtime-supported, user-appropriate summaries. | Promising hidden chain-of-thought. Prefer plans, actions, evidence, and assumptions. |

Primary definitions: [AG-UI concepts](https://docs.ag-ui.com/concepts/events) and [AG-UI SDK event types](https://docs.ag-ui.com/sdk/js/core/events) (**D**, accessed 2026-07-14).

## 7. Current CopilotKit v2 API inventory

The book should pin examples to a tested release; the source snapshot researched here reports `@copilotkit/react-core` **1.62.3** at commit `855446e1abc8f29756dc5e539e5e50a90321ac2d`. [`package.json`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/package.json) (**S**, accessed 2026-07-14).

| Primitive | Use it for | Key mechanics evidenced in pinned source | Book guidance |
| --- | --- | --- | --- |
| `useAgent` | Resolve and subscribe to an AG-UI `AbstractAgent`. | Exposes agent state/messages/run status through subscriptions; `agentId` selects an agent; `throttleMs` applies to message/state updates while run lifecycle updates remain immediate. [`useAgent` source](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/src/v2/hooks/use-agent.tsx) (**S**). | Use as the normal Level 1 entry point for stateful task surfaces. Teach agent object behavior from the exact pinned type, not a guessed `{ state, running, start }` shape. |
| `useCopilotKit` | Access low-level CopilotKit context and imperative orchestration. | Current context includes agent execution methods such as run/stop/tool invocation. [Official reference](https://docs.copilotkit.ai/reference/hooks/useCopilotKit) (**D**) and [`stopAgent` core source](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/core/src/core/core.ts) (**S**). | Reserve for custom shells and orchestration. Do not make it the default when a specialized hook exists. |
| `useFrontendTool` | Register a typed capability whose handler runs on the client, optionally with a renderer. | Registration is scoped by tool name and `agentId`; duplicate registration warns/overrides; unmount removes the tool while renderer retention supports historical tool-call UI. [`useFrontendTool` source](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/src/v2/hooks/use-frontend-tool.tsx) (**S**). | Use for client-local, user-contextual, low-risk work. Never place secrets in the handler. |
| `useRenderTool` | Render a named backend/external tool call without moving execution into the browser. | Renderer registration accepts a name or wildcard and Standard Schema-compatible schemas. [`useRenderTool` source](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/src/v2/hooks/use-render-tool.tsx) (**S**). | Preferred for showing results of privileged server tools. Separate execution evidence from display. |
| `useDefaultRenderTool` | Supply a catch-all renderer for otherwise unhandled tool calls. | Registers a wildcard renderer through `useRenderTool`; can use built-in or custom fallback. [`useDefaultRenderTool` source](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/src/v2/hooks/use-default-render-tool.tsx) (**S**). | Use as diagnostic/fallback UI, not as the primary experience for important tools. |
| `useComponent` | Let an agent choose a registered, application-owned component as a tool. | Wraps `useFrontendTool`; the component is the renderer and there is no ordinary work handler; optional follow-up behavior is supported. [`useComponent` source](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/src/v2/hooks/use-component.tsx) (**S**). | Good for display-only semantic components. The application owns implementation and styling. |
| `useHumanInTheLoop` | Pause a frontend tool call until a person responds. | Builds on `useFrontendTool`; the handler returns a Promise resolved by `respond`; abort rejects; render states distinguish in-progress/executing/complete. [`useHumanInTheLoop` source](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/src/v2/hooks/use-human-in-the-loop.tsx) (**S**). | Use for UI-mediated approval/guidance. Still enforce authorization and invariants server-side. |
| `useInterrupt` | Render and resolve runtime-originated interrupt payloads. | Listed in the current v2 reference and intended as the frontend half of an interrupt. [Official reference](https://docs.copilotkit.ai/reference/hooks/useInterrupt) (**D**). | Use when the backend/runtime owns the pause boundary. Require companion verification because current framework-specific documentation is contradictory. |
| `useThreads` | Work with conversation/task threads where the configured runtime supports them. | Listed in current reference; CopilotKit's thread docs describe persistent server-side threads with many runs. [Threads explained](https://docs.copilotkit.ai/langgraph-python/threads-explained) (**D**). | Do not imply local message history is durable. Name the persistence provider and retention behavior. |

### Migration note: `useDefaultTool`

The GTM Operations Workspace example imports `useDefaultTool` from the root and uses it to render arbitrary tool calls. GTM Operations Workspace (**S**). For a new v2 chapter:

- replace a display-only wildcard with `useDefaultRenderTool`;
- replace a named display-only renderer with `useRenderTool`;
- use `useFrontendTool` only when the client genuinely executes a capability;
- preserve a short “legacy code in the wild” sidebar so readers can recognize older examples.

Do not write “`useDefaultTool` was renamed to `useFrontendTool`.” They are not behaviorally identical in the source researched here.

## 8. Tool placement is an architecture decision

| Tool placement | Best fit | Credentials and authority | Latency/lifecycle | Examples | Required controls |
| --- | --- | --- | --- | --- | --- |
| **Frontend tool** | Current selection, viewport, clipboard, local draft, native navigation, low-risk client state. | User/client context only; no embedded service secret. | Tied to app/browser lifecycle; handler should honor abort signal where possible. | Read currently loaded accounts; highlight chart range; open editor. | Typed args; capability allowlist; user/tenant context passed to trusted server for privileged work; error and abort UI. |
| **Backend tool** | Database query/write, secret-bearing API, business invariant, large computation. | Server identity or delegated user identity. | Can be queued, retried, observed, and made idempotent. | Create transaction; fetch protected ledger; generate export. | AuthN/AuthZ; tenant scope; schema and domain validation; idempotency key; audit; timeout/retry. |
| **External worker/service** | Long-running, isolated, privileged, or independently scalable operation. | Narrow service identity; ideally per-job credentials. | Async status, callback/event, reconnect required. | Document ingestion; payment processor; machine worker. | Signed requests; network policy; job state; dedupe; compensation; result provenance. |
| **Human tool/interrupt** | Consequential choice, missing context, subjective judgment, privilege escalation. | Identified reviewer with relevant scope. | Potentially indefinite pause; persisted resume needed for durable runs. | Approve transfer draft; choose account match; correct categorization. | Exact proposal, impact, expiry, reviewer identity, argument editing, rejection branch, resume idempotency. |

### Frontend tool security statement

`useFrontendTool` schemas constrain the shape of arguments; they do not grant authority, authenticate the user, enforce tenant boundaries, or validate business rules. A frontend write that directly mutates important data should be treated as an application vulnerability unless a trusted server independently checks the principal, scope, invariants, and replay behavior. This is an **E** recommendation grounded in the handler's client execution model. [Official `useFrontendTool` reference](https://docs.copilotkit.ai/reference/hooks/useFrontendTool) and [pinned implementation](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/src/v2/hooks/use-frontend-tool.tsx) (**D/S**, accessed 2026-07-14).

### Tool contract fields worth teaching

```ts
type BookToolPolicy = {
  placement: "frontend" | "backend" | "external";
  impact: "read" | "local_write" | "system_write" | "external_action";
  reversible: boolean;
  approval: "never" | "conditional" | "always";
  idempotency: "not_applicable" | "required";
  timeoutMs: number;
  retry: "never" | "safe_only" | "bounded";
  dataClasses: string[];
};
```

This is a proposed teaching type (**A/E**). The companion should attach equivalent metadata to actual server tools or a policy registry and test enforcement; merely declaring the type is not a control.

## 9. Tool-based Generative UI patterns

The durable rule for this chapter is: **let the agent select a semantic object or registered capability; let the application own the component, accessibility, validation, and action boundary.**

| Pattern | CopilotKit primitive | Execution | Example in finance companion | Risk |
| --- | --- | --- | --- | --- |
| Display-only component selected by agent | `useComponent` | No ordinary work handler; registered UI component renders typed arguments. | Spending breakdown, account summary, budget comparison. | Treating display as verified truth without source/provenance. |
| Render an existing backend tool | `useRenderTool` | Backend or external runtime executes; frontend renders lifecycle/result. | Server fetch of protected transaction history rendered as a table. | Renderer assumes success before result. |
| Interactive client tool | `useFrontendTool` with handler and render | Browser/native handler executes and UI shows progress/result. | Change local date range or navigate to a ledger item. | Privileged side effect moved into untrusted client. |
| Blocking human response | `useHumanInTheLoop` | Promise remains unresolved until `respond`; abort can reject. | Approve/edit/reject a proposed transaction. | UI approval mistaken for backend authorization. |
| Runtime-enforced pause | backend interrupt + `useInterrupt` | Durable runtime suspends/checkpoints, UI resolves payload, runtime resumes. | Approval before server writes a ledger entry. | Repeated pre-interrupt side effects on resume. |
| Fallback/catch-all renderer | `useDefaultRenderTool` | Wildcard display for otherwise unregistered tools. | Developer diagnostics or safe generic card. | Shipping raw argument dumps containing sensitive data. |

### Lifecycle rendering checklist

Every tool component used in screenshots should have states for:

- arguments still streaming or incomplete;
- ready to execute;
- executing;
- waiting for human;
- succeeded with source/time/result;
- rejected or edited;
- failed with recovery action;
- aborted/cancelled;
- historical/completed after remount.

The pinned `useFrontendTool` intentionally retains renderer registration for historical tool calls even when the tool handler unregisters, and the pinned HITL implementation models in-progress/executing/complete. [`useFrontendTool`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/src/v2/hooks/use-frontend-tool.tsx) and [`useHumanInTheLoop`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/src/v2/hooks/use-human-in-the-loop.tsx) (**S**, accessed 2026-07-14).

### Accessibility and layout requirements for figures

- A tool's status cannot be color-only; include text/icon and live-region behavior.
- Approval controls need keyboard focus order, unambiguous labels, and a non-destructive default.
- Streaming regions should not steal focus on every token.
- Charts need textual summaries and accessible data tables.
- Inline components must survive narrow mobile widths without hiding the action, amount, target, or source.
- A completed historical tool card must not retain active buttons.

These are book product requirements (**A/E**); the companion acceptance suite must verify them.

# III. State, durability, and intervention

## 10. Shared state is a contract, not a chat transcript

AG-UI defines full snapshots and JSON Patch-style deltas for state synchronization. [AG-UI state events](https://docs.ag-ui.com/sdk/js/core/events) (**D**). CopilotKit documents using `useAgent` to access and update shared agent state and emitting state snapshots/deltas from an agent. [CopilotKit shared state](https://docs.copilotkit.ai/shared-state) (**D**, accessed 2026-07-14).

### State taxonomy

| State kind | Lifetime | Example | Storage/transport | Do not confuse with |
| --- | --- | --- | --- | --- |
| **View state** | Current component/session | Open panel, selected range | React/native UI state | Agent task state |
| **Task/run state** | Current run | Current phase, active tool, draft proposal | AG-UI state/events; runtime state | Long-term memory |
| **Thread state** | Related runs | Messages, accepted plan, accumulated artifacts | Durable checkpointer keyed by thread | Observability trace |
| **User/account memory** | Across threads | Currency preference, saved categorization rule | Authenticated application DB or scoped store | Model context copied forever |
| **Organizational memory** | Across users/workflows | Approved policy or glossary | Governed knowledge system with provenance | Arbitrary channel history |
| **Trace/telemetry** | Operational retention period | Model/tool spans, latency, errors | LangSmith/observability system | Source-of-truth product state |

### Ownership table for the finance teaching schema

| Field | Owner | Update rule | Conflict strategy | Persistence target |
| --- | --- | --- | --- | --- |
| `objective` | User | User edits; agent may propose clarification. | User edit wins; rerun plan against new version. | Thread state. |
| `phase` | Runtime | Event-derived only. | Reject arbitrary client overwrite. | Run/thread checkpoint. |
| `filters` | Joint | User edits directly; agent may propose. | Versioned patch; surface conflict instead of silent overwrite. | View plus optional thread state. |
| `accounts` | Backend | Read from server source of truth. | Refresh by server version/ETag. | Product database; cached projection in task state. |
| `draftTransaction` | Agent/user joint | Agent proposes, user edits. | Record both proposed and approved versions. | Thread state until accepted. |
| `approvedTransactionId` | Backend | Set only after authorized idempotent write. | Server response is authoritative. | Product database and audit reference. |
| `sources` | Runtime/tools | Append with provenance and retrieval time. | Deduplicate by stable identifier/version. | Thread state and trace. |
| `approval` | Identified reviewer/backend | Signed/authorized decision tied to exact proposal hash/version. | Stale decision invalid after proposal edit. | Audit log and thread state. |

### State-sync failure modes

1. Agent overwrites a newer user edit because both send a whole snapshot.
2. UI renders prose and attempts to reconstruct a typed artifact from it.
3. A stale reconnect snapshot regresses completed state.
4. State delta applies to a different schema version.
5. A jointly edited object has no revision or ownership metadata.
6. Sensitive server state is copied into the client unnecessarily.
7. A completed tool's result exists only in transient UI memory.
8. Long-term memory stores unverified model claims as fact.

The companion should include one deliberate version conflict and show rejection/rebase behavior; otherwise “shared state” remains a happy-path demo.

## 11. BuiltInAgent versus LangGraph

| Decision dimension | CopilotKit `BuiltInAgent` | LangGraph-backed agent |
| --- | --- | --- |
| Best starting point | Constrained application agent with a direct model/tool loop and CopilotKit runtime integration. | Multi-stage state machine, durable execution, explicit branching, long-running work, subgraphs, or runtime-enforced interrupts. |
| Execution topology | In-process agent loop built on CopilotKit runtime/AI SDK integration. [`BuiltInAgent` source](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/runtime/src/agent/index.ts) (**S**). | Developer-defined graph or LangChain agent built on LangGraph. [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents) and [LangGraph graphs](https://docs.langchain.com/oss/python/langgraph/workflows-agents) (**D**). |
| Step budget | Configurable loop limit; official advanced configuration documents `maxSteps` and other model settings. [Advanced configuration](https://docs.copilotkit.ai/advanced-configuration) (**D**). | Recursion/step limits plus explicit graph routing and stop conditions. |
| State | Can exchange AG-UI state and pass client context. | Typed graph state with reducers; persisted when a checkpointer is configured. |
| Durability | Do not claim durable, resumable execution merely from using the class. CopilotKit distinguishes the in-process loop from managed persistence features. [OSS vs managed concepts](https://docs.copilotkit.ai/strands/concepts/oss-vs-enterprise) (**D**). | Checkpoints at super-steps enable resume, HITL, time travel, and fault-tolerant recovery when a durable checkpointer is configured. [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) (**D**). |
| Interrupts | Frontend HITL can block a tool handler; durability depends on the surrounding runtime. | `interrupt()` persists pause state and resumes with `Command(resume=...)` using the same thread ID. [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) (**D**). |
| Operational complexity | Lower; good for first complete Level 1 build. | Higher; storage, serialization, thread IDs, idempotency, deployment, migrations, and reconnect must be designed. |
| Book use | Ship the first narrow finance slice, then show the boundary where LangGraph becomes justified. | Add a durable transaction-review workflow or research/report flow as an extension, not as decorative extra agents. |

### BuiltInAgent knobs to inventory in Chapter 10

Current official advanced configuration exposes or discusses controls including `maxSteps`, tool choice, output token limits, temperature, top-p/top-k, penalties, stop sequences, seed, retry count, instructions/prompt, tools, and MCP-related/agent overrides. [CopilotKit advanced configuration](https://docs.copilotkit.ai/advanced-configuration) (**D**, accessed 2026-07-14).

| Knob | Builder question | Safe teaching default |
| --- | --- | --- |
| `maxSteps` | How much autonomous tool chaining is appropriate for this task? | Small bounded number; treat reaching limit as an explicit outcome. |
| Tool choice/allowlist | Which tools may the model select in this phase? | Phase-specific least privilege; separate read and write sets. |
| Output tokens | What is the maximum response/artifact size? | Bound by UI and cost; stream structured artifacts separately. |
| Temperature/top-p | Is variability useful or harmful? | Low for extraction/action arguments; evaluate before changing. |
| Retries | Which failures are transient and safe to repeat? | Only bounded, idempotent operations; never blind retry an external write. |
| Prompt/instructions | What policy is prose versus enforced code? | Keep business/security constraints in code; prompt is guidance, not authority. |
| State passed from client | Which context is needed and trusted? | Minimal typed projection; revalidate anything consequential server-side. |
| Model/provider | What quality, latency, tool-call, region, and data policies apply? | Pin tested model identifier/config; have an evaluated fallback. |

The personal-finance runtime configures `maxSteps: 10` and forwards frontend tools to its `BuiltInAgent`; that is source evidence for the demo's architecture, not a recommended universal setting. [`lib/finance-agent.ts` at `d876006`](https://github.com/jerelvelarde/personal-finance-copilot/blob/d8760064c626712a8fa15c192a8c4bc69bb24055/apps/runtime/lib/finance-agent.ts) (**S**, accessed 2026-07-14).

## 12. LangGraph persistence, streaming, and interrupt facts

### Persistence

- With a checkpointer, LangGraph saves a checkpoint at each graph super-step and associates it with a thread identifier. This enables human intervention, memory, time travel, and fault-tolerant recovery. [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) (**D**).
- A checkpointer provides thread-scoped persistence; a store supports information shared across threads. [LangGraph JavaScript persistence](https://docs.langchain.com/oss/javascript/langgraph/persistence) (**D**).
- A durable application still needs a production persistence implementation, schema migration, retention, encryption, access control, and recovery tests. “Compiled with a checkpointer” is not a complete operations story. **E**

### Streaming

LangGraph documents stream modes for state updates, full values, messages/tokens, custom events, checkpoints, tasks, and debugging. [LangGraph streaming](https://docs.langchain.com/oss/python/langgraph/streaming) (**D**, accessed 2026-07-14). Map modes to UI intentionally:

| Stream content | Best UI | Noise/privacy concern |
| --- | --- | --- |
| Tokens/messages | Conversational response | Token flood; partial content may be revised. |
| State updates | Stage views and artifacts | Sensitive internal state should not all reach client. |
| Custom events | Domain progress, e.g. “3 of 8 files parsed” | Must be truthful and generated by measurable work. |
| Tasks/checkpoints/debug | Developer observability | Usually too detailed or sensitive for end users. |

Preview documentation for newer typed event-stream projections should not be made the book's canonical API until the companion pins and tests the release.

### Interrupts

- `interrupt()` pauses graph execution and returns a payload to the caller; resumption uses `Command(resume=...)` with the same thread. [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) (**D**).
- On resume, the interrupted node begins again from its start. Side effects executed before the interrupt can repeat; make them idempotent or move them after the interrupt. [LangGraph interrupt rules](https://docs.langchain.com/oss/python/langgraph/interrupts) (**D**).
- Production interrupts require a durable checkpointer and stable thread identity. **D/E**
- CopilotKit's generic `useInterrupt` reference describes the frontend primitive, but the current LangGraph-specific documentation simultaneously contains a “not supported” notice and LangGraph usage instructions. Treat the support matrix as unresolved until a pinned companion proves it. [CopilotKit `useInterrupt`](https://docs.copilotkit.ai/reference/hooks/useInterrupt) and [LangGraph-specific HITL page](https://docs.copilotkit.ai/langgraph-python/human-in-the-loop/useInterrupt) (**D, contradictory**, accessed 2026-07-14).

## 13. Human-in-the-loop: two distinct enforcement patterns

| Pattern | Where pause is enforced | Persistence | Best use | Publication wording |
| --- | --- | --- | --- | --- |
| `useHumanInTheLoop` frontend tool | Client tool handler returns a pending Promise until `respond`; abort can reject. | Depends on browser/app and surrounding runtime; do not assume durable indefinite pause. | Immediate, user-present approval or guidance in a Level 1 UI. | “The frontend blocks this tool call pending a response.” |
| LangGraph `interrupt` + `useInterrupt` UI | Graph runtime calls `interrupt`, checkpoints, and waits for resume. | Durable when configured with a production checkpointer and stable thread. | Long-running tasks, disconnect/reconnect, server-enforced decision boundary. | “The runtime suspends at a checkpoint and resumes with a human decision.” |

### Approval card information hierarchy

Every high-impact approval screenshot must show:

1. requested action and category (`create transaction`, not “use tool”);
2. target system/account/environment;
3. exact proposed arguments and source of each important value;
4. expected impact and whether it is reversible;
5. identity of requesting agent and approving principal;
6. evidence/assumptions and unresolved ambiguity;
7. expiry/staleness rule;
8. buttons for approve, edit, reject, and where appropriate “use safer alternative”;
9. post-decision receipt with immutable result ID or failure;
10. cancellation/undo semantics that are actually implemented.

The personal-finance repo supplies four client-side write-gate examples, useful for component design. They should be upgraded into a server-authorized, idempotent write path before the book calls them production approval. Exact paths appear below.

## 14. Cancellation and recovery semantic matrix

| User intent | Actual mechanism | What stops | What remains | UI label |
| --- | --- | --- | --- | --- |
| Stop visible generation | Abort client/agent run, e.g. CopilotKit `stopAgent`. | Further agent generation and cooperative tool work. | Completed calls/side effects; non-cooperative work may continue. | “Stop run” plus consequence copy. |
| Abort frontend handler | Handler receives/observes `AbortSignal`. | Work that passes/checks signal. | Already completed local/external operations. | “Cancel current action.” |
| Disconnect UI | Network or app stream closes. | Display stream only unless runtime couples disconnect to cancellation. | Backend run may continue. [Join/rejoin guide](https://docs.langchain.com/oss/python/langchain/frontend/join-rejoin) (**D**). | “Disconnected—work may still be running.” |
| Pause for user | HITL pending Promise or LangGraph interrupt. | Progress past decision boundary. | Run/thread and completed prior effects. | “Waiting for your review.” |
| Cancel runtime run | Runtime-specific cancel/interrupt behavior. | Future runtime work. | Checkpoints may remain; external effects remain. | “Cancel run.” |
| Roll back runtime state | LangSmith deployment rollback semantics delete/revert run/checkpoint state. [Cancel or rollback](https://docs.langchain.com/langsmith/cancel-run) (**D**). | Runtime history/state for that run. | External system side effects are not inherently compensated. | “Roll back task state.” |
| Undo business action | Domain-specific inverse or compensation. | Nothing automatically; executes a new business operation. | Audit history should remain. | “Reverse transaction” or exact domain term. |

Pinned CopilotKit core calls its run handler's abort mechanism and the agent's `abortRun`; frontend handlers receive abort-aware context in the core types. [`stopAgent`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/core/src/core/core.ts), [run handler](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/core/src/core/run-handler.ts), and [core types](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/core/src/types.ts) (**S**, accessed 2026-07-14). The book must say cancellation is cooperative, then prove behavior for each companion tool.

# IV. Web and mobile implementation constraints

## 15. Web application baseline

For the canonical web slice, use a pinned React/Next.js companion and record:

- Node and package-manager versions;
- exact CopilotKit, AG-UI, LangChain/LangGraph, React, and Next versions;
- runtime route location and supported methods;
- authentication/tenant derivation before agent selection;
- whether the route streams through a Node or Edge runtime;
- server tool boundary and secrets source;
- thread/run ID generation and persistence;
- reconnect behavior after refresh;
- content-security, error redaction, and trace retention decisions.

Next.js Route Handlers live in the `app` directory and use Web Request/Response APIs; the companion should follow the pinned Next documentation and avoid assuming old Pages Router behavior. [Next.js Route Handlers](https://nextjs.org/docs/app/getting-started/route-handlers-and-middleware) (**D**, accessed 2026-07-14).

The finance runtime currently exposes a catch-all CopilotKit route with `GET`, `POST`, `DELETE`, and `OPTIONS`, and constructs the v2 multi-route handler with a base path. [`apps/runtime/app/api/copilotkit/[[...all]]/route.ts`](https://github.com/jerelvelarde/personal-finance-copilot/blob/d8760064c626712a8fa15c192a8c4bc69bb24055/apps/runtime/app/api/copilotkit/%5B%5B...all%5D%5D/route.ts) (**S**, accessed 2026-07-14). Verify the encoded GitHub link during editorial QA.

## 16. Bare React Native and Expo/mobile constraints

The researched finance app is a bare React Native app, not an Expo Router application. Its pinned manifest uses React Native `0.85.3`, React `19.2.3`, `@copilotkit/react-native ^1.59.2`, Node `>=22.11.0`, Zod `^4.4.3`, and Zustand `^5.0.14`. [`apps/finance-mobile/package.json`](https://github.com/jerelvelarde/personal-finance-copilot/blob/d8760064c626712a8fa15c192a8c4bc69bb24055/apps/finance-mobile/package.json) (**S**, accessed 2026-07-14).

### Constraints to teach explicitly

| Constraint | Builder decision | Companion test/capture |
| --- | --- | --- |
| Device-to-runtime address | Simulator/emulator and physical device cannot always use the same `localhost` URL. Current quickstart discusses emulator host aliases and LAN URLs. [React Native quickstart](https://docs.copilotkit.ai/react-native) (**D**). | iOS simulator, Android emulator, and one physical device if supported; show environment configuration, not a hard-coded developer IP. |
| Streaming APIs/polyfills | React Native's web-stream support and package behavior vary by CopilotKit version. | Pin package; prove token/tool/state streaming. Do not copy current docs into a 1.59.2 example without testing. |
| App lifecycle/backgrounding | App may background, lose network, or be killed while backend work continues. | Background mid-run; foreground/rejoin same thread; distinguish disconnected vs cancelled. |
| Native render registry | Native tool rendering uses React Native-specific hooks/provider behavior. | Render all lifecycle states in a native screen and after navigation/remount. |
| Attachments/files | Native pickers and filesystem modules require platform permissions and optional peer packages. Current package manifest lists optional Expo modules. [`react-native/package.json`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-native/package.json) (**S**). | Denied permission, cancelled picker, large file, unsupported type, and redaction flow. |
| Keyboard/safe areas | Inline tool and approval cards share constrained vertical space with chat input. | Smallest supported phone, large text, keyboard open, landscape. |
| Secure storage/auth | Mobile tokens must use platform-appropriate secure storage and short-lived server credentials. | Logout/revocation; expired token mid-run; never embed provider keys in bundle. |
| Offline/retry | A reconnect can replay requests unless identity and idempotency are stable. | Drop network before/after server accepts a write; confirm exactly-once domain behavior or safe dedupe. |

### Current documentation/source contradiction

At commit `855446e`, the React Native entry point auto-imports polyfills and exports a headless `CopilotChat` plus prebuilt modal/sidebar/popup components, attachments, and hooks. [`packages/react-native/src/index.ts`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-native/src/index.ts) (**S**). The current quickstart still describes manual polyfill setup and says there are no prebuilt components. [CopilotKit React Native quickstart](https://docs.copilotkit.ai/react-native) (**D, inconsistent**, accessed 2026-07-14).

Publication rule:

1. select an exact `@copilotkit/react-native` version;
2. inspect that version's exports and migration notes;
3. run the companion on target platforms;
4. write code/prose to the tested version;
5. place a version-drift note rather than blending 1.59.2 demo behavior with 1.62.3 source behavior.

The current React Native-specific `useRenderTool` also differs from the web v2 export: it registers a native renderer and may include a handler. [`packages/react-native/src/hooks/use-render-tool.tsx`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-native/src/hooks/use-render-tool.tsx) (**S**, accessed 2026-07-14). Teach platform imports explicitly.

# V. Audited project evidence

## 17. Personal Finance Copilot: exact evidence inventory

**Repository:** [jerelvelarde/personal-finance-copilot](https://github.com/jerelvelarde/personal-finance-copilot/tree/d8760064c626712a8fa15c192a8c4bc69bb24055)

**Pinned SHA:** `d8760064c626712a8fa15c192a8c4bc69bb24055`

**Research status:** source inspected locally at the pinned SHA; not run in this packet (**S, not R**).

### What is actually present

| Capability | Exact source path | Evidence and book use |
| --- | --- | --- |
| Mobile CopilotKit provider | [`apps/finance-mobile/App.tsx`](https://github.com/jerelvelarde/personal-finance-copilot/blob/d8760064c626712a8fa15c192a8c4bc69bb24055/apps/finance-mobile/App.tsx) | Provider appears in the application shell around the lower half of the file. Use to discuss application-level runtime URL/configuration after re-running. |
| Custom headless chat screen | [`apps/finance-mobile/src/ChatScreen.tsx`](https://github.com/jerelvelarde/personal-finance-copilot/blob/d8760064c626712a8fa15c192a8c4bc69bb24055/apps/finance-mobile/src/ChatScreen.tsx) | Uses `useAgent` and `useCopilotKit`, adds a message to the agent, starts the run imperatively, and traverses registered rendered tool calls. Good “open the hood” example; it also creates upgrade risk by depending on low-level behavior. |
| Account read tools | [`apps/finance-mobile/src/copilot/reads.tsx`](https://github.com/jerelvelarde/personal-finance-copilot/blob/d8760064c626712a8fa15c192a8c4bc69bb24055/apps/finance-mobile/src/copilot/reads.tsx) | Five `useFrontendTool` registrations distributed through the file. Use one canonical read tool, not five near-duplicate snippets. |
| Account write approval | [`apps/finance-mobile/src/copilot/accounts.tsx`](https://github.com/jerelvelarde/personal-finance-copilot/blob/d8760064c626712a8fa15c192a8c4bc69bb24055/apps/finance-mobile/src/copilot/accounts.tsx) | `useHumanInTheLoop` write gate. Use as UI source, then move authoritative write to a server tool. |
| Budget write approvals | [`apps/finance-mobile/src/copilot/budgets.tsx`](https://github.com/jerelvelarde/personal-finance-copilot/blob/d8760064c626712a8fa15c192a8c4bc69bb24055/apps/finance-mobile/src/copilot/budgets.tsx) | Two HITL registrations. Useful for comparing approval cards and avoiding generic “Allow.” |
| Transaction write approval | [`apps/finance-mobile/src/copilot/transactions.tsx`](https://github.com/jerelvelarde/personal-finance-copilot/blob/d8760064c626712a8fa15c192a8c4bc69bb24055/apps/finance-mobile/src/copilot/transactions.tsx) | One HITL gate for transaction mutation. Make this the canonical high-impact example with synthetic data. |
| Receipt tool | [`apps/finance-mobile/src/copilot/receipt.tsx`](https://github.com/jerelvelarde/personal-finance-copilot/blob/d8760064c626712a8fa15c192a8c4bc69bb24055/apps/finance-mobile/src/copilot/receipt.tsx) | Client tool for receipt flow. Use to discuss native file/device affordances only after permission and error cases are verified. |
| BuiltInAgent | [`apps/runtime/lib/finance-agent.ts`](https://github.com/jerelvelarde/personal-finance-copilot/blob/d8760064c626712a8fa15c192a8c4bc69bb24055/apps/runtime/lib/finance-agent.ts) | Server constructs `BuiltInAgent`, sets `maxSteps: 10`, and includes frontend tools. System instructions separate read and write intent. |
| Runtime route | [`apps/runtime/app/api/copilotkit/[[...all]]/route.ts`](https://github.com/jerelvelarde/personal-finance-copilot/blob/d8760064c626712a8fa15c192a8c4bc69bb24055/apps/runtime/app/api/copilotkit/%5B%5B...all%5D%5D/route.ts) | Multi-method v2 runtime route and base path. Capture network/run behavior after execution. |
| Existing reference images | [`docs/screenshots`](https://github.com/jerelvelarde/personal-finance-copilot/tree/d8760064c626712a8fa15c192a8c4bc69bb24055/docs/screenshots) | Includes chat account, donut, empty, HITL, resolved, and dashboard images. Treat as composition references only until recaptured from the release companion. |

### What is not established by this pin

- No LangGraph implementation was found in the audited source.
- No demonstrated durable checkpointer/thread-resume path was found.
- No production authentication and tenant-isolation proof was found.
- Client HITL components do not alone establish server authorization.
- Existing images do not record current command, environment, seed data, or build SHA.
- Package ranges (`^1.59.2`) do not identify the actually installed resolution without a verified lock/install context.
- The example should not be called a financial adviser, banking platform, or production ledger security reference.

### Best editorial use

Use the repo as the Level 1 product skeleton: a personal finance workspace that can read visible ledger data, render charts/cards, propose a mutation, and ask for correction/approval. The book's companion should harden the architecture by moving sensitive data and writes server-side, adding authenticated thread identity, idempotency, error/reconnect cases, and a tested web sibling. Preserve the original as “source in the wild”; build the production-shaped teaching path separately.

## 18. GTM Operations Workspace: current and legacy patterns to compare

**Repository:** GTM Operations Workspace

**Pinned SHA:** `private revision omitted`

**Research status:** source inspected locally at the pinned SHA; not run in this packet (**S, not R**).

| Capability | Exact source | Evidence and chapter use |
| --- | --- | --- |
| Backend registry | GTM Operations Workspace | Declares Hermes, Anthropic, and OpenAI backend options/readiness notes. Use to teach provider/backend switching as an application concern, not to benchmark quality. |
| Runtime route | [`app/app/api/copilotkit/[[...slug]]/route.ts`](private-source-omitted) | Registers Hermes as an AG-UI agent and classic adapters for other providers; reads `x-gtmos-backend`. Use for runtime-selection/trust-boundary discussion. |
| Provider and fallback tool UI | GTM Operations Workspace | Sends backend choice in a header and uses legacy `useDefaultTool` as a catch-all renderer. Use as a migration exercise to v2 `useDefaultRenderTool`. |
| Basic middleware gate | GTM Operations Workspace | Demonstrates an application gate exists. Do not elevate it to comprehensive tenant security without tests and policy inspection. |
| Dependency snapshot | GTM Operations Workspace | CopilotKit ranges `^1.62.3`, Next `16.1.7`, React `^19.2.4`, AG-UI `0.0.57`; Hermes adapter is a preview URL. Use to show why version registers and supply-chain review matter. |

### Do not claim from this repo

- It is not a LangGraph example.
- A selectable header is not a complete server-side authorization mechanism.
- A preview adapter URL is not a stable production dependency.
- The backend options are not evidence of equivalent behavior, cost, quality, or safety.
- The wildcard default renderer is not the preferred current v2 teaching API.

### Useful bridge into Level 2

GTM Operations Workspace and the separate Hermes/CPK project can later show that a Level 1 UI may supervise a machine-capable agent without rebuilding every machine tool in the frontend. In Chapters 1–10, keep this to an architecture preview. Do not import Level 2 filesystem/shell authority into the finance example's threat model before that section defines its harness and restrictions.

# VI. Companion snippets and verification specifications

## 19. Snippet inventory: source-shaped, not yet publication-tested

Every printed snippet should live in the companion repository, be imported or executed by a test, and be extracted into the manuscript automatically or checked for drift. The following are snippet briefs, not code to copy blindly.

| ID | Chapter | Snippet | Source seed | Required test before publication |
| --- | --- | --- | --- | --- |
| `FND-01` | 2 | One model call vs predetermined workflow vs dynamic agent loop. | [LangChain models](https://docs.langchain.com/oss/python/langchain/models), [agents](https://docs.langchain.com/oss/python/langchain/agents), and [LangGraph workflow docs](https://docs.langchain.com/oss/python/langgraph/workflows-agents). | Deterministic fake model/tool tests prove which layer owns routing. |
| `L1-01` | 3 | Minimal Next route registering a named BuiltInAgent. | [Finance runtime route](https://github.com/jerelvelarde/personal-finance-copilot/blob/d8760064c626712a8fa15c192a8c4bc69bb24055/apps/runtime/app/api/copilotkit/%5B%5B...all%5D%5D/route.ts) and [BuiltInAgent source](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/runtime/src/agent/index.ts). | Route health, authenticated request, streaming response, missing model key fail-loud behavior. |
| `L1-02` | 4 | Custom task shell with `useAgent` and low-level `useCopilotKit` stop/run actions. | [Finance `ChatScreen.tsx`](https://github.com/jerelvelarde/personal-finance-copilot/blob/d8760064c626712a8fa15c192a8c4bc69bb24055/apps/finance-mobile/src/ChatScreen.tsx). | Start, duplicate-submit prevention, stop, error, refresh/rejoin, accessibility. |
| `L1-03` | 6 | Read-only client tool for current visible filters/selection. | [Finance reads](https://github.com/jerelvelarde/personal-finance-copilot/blob/d8760064c626712a8fa15c192a8c4bc69bb24055/apps/finance-mobile/src/copilot/reads.tsx) plus pinned [`useFrontendTool`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/src/v2/hooks/use-frontend-tool.tsx). | Valid/invalid schema; unmount/remount; abort; no access to secret/server-only fields. |
| `L1-04` | 6 | Protected backend tool that creates a synthetic ledger transaction with idempotency. | New companion implementation (**A**). | Unauthorized/other tenant; invalid amount; duplicate idempotency key; timeout after accept; audit receipt. |
| `L1-05` | 7 | Display-only spending chart registered with `useComponent`. | Pinned [`useComponent`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/src/v2/hooks/use-component.tsx). | Partial args, empty state, accessible text/table, mobile width, malicious labels escaped. |
| `L1-06` | 7 | Named renderer for server transaction-search tool using `useRenderTool`. | Pinned [`useRenderTool`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/src/v2/hooks/use-render-tool.tsx). | Streaming args, execution, result, failure, historical render after remount. |
| `L1-07` | 7 | Generic safe fallback using `useDefaultRenderTool`. | Pinned [`useDefaultRenderTool`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-core/src/v2/hooks/use-default-render-tool.tsx). | Redacts sensitive arguments/results and never exposes active destructive buttons. |
| `L1-08` | 8 | Typed shared ledger task state and versioned patch/update. | [AG-UI state events](https://docs.ag-ui.com/sdk/js/core/events), [CopilotKit shared state](https://docs.copilotkit.ai/shared-state). | Concurrent agent/user edits, stale revision rejection, reconnect snapshot, schema version mismatch. |
| `L1-09` | 9 | Immediate client approval with `useHumanInTheLoop`. | [Finance transaction gate](https://github.com/jerelvelarde/personal-finance-copilot/blob/d8760064c626712a8fa15c192a8c4bc69bb24055/apps/finance-mobile/src/copilot/transactions.tsx) and pinned hook source. | Approve/edit/reject/abort; stale proposal invalidation; server reauthorization. |
| `L1-10` | 9 | Durable LangGraph interrupt around server write. | [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts). | Disconnect before decision; resume same thread; node restart; exactly-once write; second reviewer/stale payload. |
| `L1-11` | 10 | Native tool renderer and task shell. | Finance mobile paths and pinned RN-specific hook. | iOS/Android target matrix; background/foreground; device URL; keyboard/safe area; denied permission. |
| `L1-12` | 10 | Backend selector migration from GTM Operations Workspace with server allowlist. | GTM Operations Workspace and route. | Unknown header rejected; user policy constrains providers; legacy wildcard migrated; preview dependency excluded from release path unless pinned. |

### Snippet publication template

Attach this metadata beside every code sample in the manuscript source:

```yaml
snippet_id: L1-06
source_file: apps/web/src/copilot/render-transaction-search.tsx
source_ref: <release tag or immutable SHA>
package_versions:
  "@copilotkit/react-core": <exact>
  "@ag-ui/client": <exact>
verified_on: 2026-XX-XX
verification_command: <exact command>
test_file: <exact path>
```

This is a production-process recommendation (**A/E**). It prevents a 2026 book from printing API-shaped pseudocode that never compiled.

## 20. Minimum acceptance suite for the Level 1 companion

### Unit and component

- tool schemas accept valid arguments and reject malformed/extra unsafe values;
- renderers cover streaming, executing, completed, failed, rejected, and cancelled states;
- state reducers reject stale revisions and preserve newer user edits;
- approval response is bound to the exact proposal version;
- cancellation propagates to cooperative frontend tools;
- no secret-bearing environment value is bundled into client code;
- charts and approval components have accessible names and nonvisual summaries.

### Integration

- authenticated web and mobile clients reach the same scoped synthetic ledger;
- backend tools derive tenant/user from trusted authentication rather than model arguments;
- one submitted transaction remains one transaction across retry, timeout, and reconnect;
- AG-UI lifecycle and tool events arrive in an acceptable order and produce stable UI;
- a failed server tool surfaces recoverable error state without fabricated success;
- refresh/rejoin restores the same thread and historical tool renderers;
- changing backend/model selection is server-allowlisted and observable.

### End to end

1. User asks for spending summary; agent selects a read path; product renders chart and textual summary with data timestamp.
2. User asks to record a synthetic transaction; agent proposes typed fields; user edits category; server revalidates and returns a receipt ID.
3. User rejects a proposal; no write occurs and the run continues or ends legibly.
4. Network drops after write acceptance but before UI response; retry does not duplicate the transaction.
5. User backgrounds mobile app during a longer read; backend behavior and rejoin state match documented semantics.
6. User cancels during a cooperative read; UI distinguishes cancelled from failed and does not imply rollback.
7. A malicious tool result/string is rendered as data, not executable markup or instructions.
8. User from tenant A cannot access or mutate tenant B data through tool arguments, state patches, thread IDs, or backend headers.

# VII. Figures and screenshot capture plan

## 21. Figures for Chapters 1–10

| Figure ID | Chapter | Composition | Evidence/content source | Capture/build status |
| --- | --- | --- | --- | --- |
| `FIG-01` | 1 | Three nested/adjacent surfaces: app, machine, organization; authority and blast radius increase. | Editorial three-level taxonomy. | **A** custom vector. |
| `FIG-02` | 2 | Three small paths: model call, fixed workflow, adaptive agent loop. | LangChain/LangGraph definitions. | **A** custom vector; avoid vendor UI. |
| `FIG-03` | 3 | Level 1 reference architecture with client, AG-UI boundary, runtime options, product services, trust zones. | Section 4 of this packet. | **A** custom vector. |
| `FIG-04` | 4 | Agentic task UI state machine including waiting/retry/partial/cancel. | Proposed state model. | **A** custom vector plus tested mapping. |
| `FIG-05` | 5 | Agent cutaway with nine parts and cross-cutting state/policy/identity/ops. | Section 2. | **A** custom vector. |
| `FIG-06` | 5 | Run/step/tool/thread/checkpoint/trace timeline. | AG-UI and LangGraph facts. | **A** custom vector with terminology caveat. |
| `FIG-07` | 6 | Tool placement decision tree: client context, credentials, duration, side effect, human review. | Section 8. | **A** custom vector. |
| `FIG-08` | 7 | Same semantic transaction shown as streaming tool card, approval, receipt, historical state. | Companion components. | **A/R required** screenshot grid. |
| `FIG-09` | 8 | Shared-state ownership and version conflict/rebase. | Section 10. | **A/R required** diagram + capture. |
| `FIG-10` | 8 | BuiltInAgent vs LangGraph decision map. | Section 11. | **A** custom vector. |
| `FIG-11` | 9 | Immediate frontend HITL versus durable runtime interrupt. | Sections 12–13. | **A** two-lane sequence diagram. |
| `FIG-12` | 10 | Web/mobile companion deployment and authentication/thread boundary. | Hardened finance implementation. | **A/R required** architecture + actual UI. |

## 22. Screenshot shot list

Existing finance images (`chat-accounts.png`, `chat-donut.png`, `chat-empty.png`, `chat-hitl-card.png`, `chat-hitl-resolved.png`, `dashboard.png`) are reference-only. [Pinned screenshot directory](https://github.com/jerelvelarde/personal-finance-copilot/tree/d8760064c626712a8fa15c192a8c4bc69bb24055/docs/screenshots) (**S**). Recapture the following with synthetic data and release SHA visible in accompanying metadata:

| Shot | Required state | Annotation focus |
| --- | --- | --- |
| `SHOT-L1-01` | Empty/new thread on web | Goal entry, scope/context, example prompt, data mode labeled synthetic. |
| `SHOT-L1-02` | Run in progress | Stage label, current tool, stop control, first useful artifact; no fake percentage. |
| `SHOT-L1-03` | Read tool complete | Typed account/spend card, timestamp/source, accessible summary. |
| `SHOT-L1-04` | Tool args streaming | Skeleton/partial state that cannot be submitted prematurely. |
| `SHOT-L1-05` | Proposed transaction approval | Action, account, amount, category, evidence, reversibility, edit/reject/approve. |
| `SHOT-L1-06` | Edited then approved | Diff from proposal to approved args plus reviewer identity. |
| `SHOT-L1-07` | Server receipt | Stable transaction ID, completed status, “undo” only if compensation exists. |
| `SHOT-L1-08` | Tool failure | Error class, what changed/did not change, retry or safer alternative. |
| `SHOT-L1-09` | Disconnected/rejoining | Thread/run IDs in debug metadata; user copy says work may continue. |
| `SHOT-L1-10` | Mobile narrow viewport | Inline component, keyboard, safe area, full action/amount visible. |
| `SHOT-L1-11` | Mobile background/resume | Rejoined run with preserved task state. |
| `SHOT-L1-12` | Developer trace | Redacted AG-UI event timeline aligned to visible UI, clearly marked developer view. |

Capture record per screenshot:

```yaml
shot_id: SHOT-L1-05
repo_sha: <immutable SHA>
seed_fixture: synthetic-ledger-v1
platform: web | ios | android
viewport_or_device: <exact>
command: <exact run command>
captured_at: <ISO timestamp>
scenario_test: <test name/path>
redactions: <none or exact list>
```

Do not use real account names, balances, transaction IDs, API keys, localhost IPs, email addresses, or trace payload secrets.

# VIII. Builder knobs, risks, and editorial constraints

## 23. Level 1 knobs inventory

The book promises “all the knobs” but should not imply every vendor setting deserves equal attention. Organize knobs by decision rather than API alphabet.

| Area | Knobs/parameters | What the reader must decide | Failure signal |
| --- | --- | --- | --- |
| Scope/autonomy | allowed goals, max steps, recursion, time budget, cost budget, stop condition | Smallest useful autonomy envelope | Loops, unnecessary calls, silent truncation at limit |
| Model | provider/model, region, temperature, token cap, structured output, fallback | Quality/latency/cost/data policy per task | Schema failure, drift, unacceptable tail latency |
| Tools | placement, schemas, descriptions, allowlist by phase, timeout, retry, idempotency | Capability and blast radius | Wrong tool, invalid args, duplicate side effect |
| State | schema, ownership, reducers, version, snapshots/deltas, client projection | Who may update what | Lost edits, stale state, privacy leak |
| Threads | ID origin, persistence provider, retention, access, delete/export | What survives and who can rejoin | Cross-user thread access, lost work |
| Memory | namespace, provenance, confidence, TTL, correction, retrieval | What is safe and useful across threads | Poisoned/stale context, data retention breach |
| Streaming | token/state/event mode, throttle, buffering, first-artifact target | Which partial result helps rather than distracts | UI thrash, out-of-order state, expensive noise |
| Human control | gate placement, reviewer scope, edit/reject branches, expiry | Which action needs which human | Rubber-stamp approval, stale decision |
| Cancellation | abort granularity, disconnect behavior, cleanup, compensation | What user-visible “stop” promises | Work continues unexpectedly; duplicate retry |
| Reliability | retries, backoff, fallback, queue, dead-letter, recovery | Which failures are safe to repeat | Retry storm or hidden partial completion |
| Security | authN, authZ, tenant binding, secret boundary, output encoding, network policy | Who can do what to which resource | Confused deputy, cross-tenant access, injection |
| Observability | traces, redaction, metrics, sampling, retention, correlation IDs | What is needed to diagnose without oversharing | No root cause or sensitive trace leak |
| Evaluation | dataset, trajectory checks, tool args, policy checks, online sampling | What “working” means beyond good prose | Unsafe/wasteful path with plausible answer |
| UX | progress stages, component registry, source visibility, accessibility, history | How users supervise and correct | Opaque spinner, inaccessible action, mistrust |
| Release/versioning | lockfile, source SHA, model config, migration window, snippet extraction | How book/code stay reproducible | Printed code no longer compiles |

## 24. Failure and security register

| Risk | Concrete Level 1 scenario | Control to teach | Verification |
| --- | --- | --- | --- |
| Prompt/tool injection | Transaction memo or retrieved document tells the agent to ignore policy. | Treat tool content as untrusted data; separate instructions from data; allowlist tools by phase; require server checks. | Malicious fixture cannot trigger unauthorized tool/write. |
| Client secret exposure | Frontend tool calls provider/service with embedded API key. | Keep secrets and privileged APIs server-side; scan built assets. | Secret scanner and bundle inspection. |
| Cross-tenant access | Model supplies another account/user ID to backend tool. | Derive tenant/user from authenticated context; ignore or validate model-provided ownership IDs. | Tenant isolation integration tests. |
| Confused deputy | Agent has broader server credentials than requesting user. | Delegated/scoped identity and per-tool authorization. | User without permission gets denial even with valid tool args. |
| Schema-only security | Zod-valid amount/account still violates policy. | Domain validation, authorization, limits, ledger invariants. | Valid-shape but unauthorized cases fail. |
| Duplicate side effect | Network drops after transaction accepted; tool retries. | Idempotency key bound to proposal/version; server dedupe and receipt lookup. | Fault-injection produces one record. |
| Approval race/staleness | User approves old proposal after agent/user changes amount. | Hash/version approval payload; invalidate on edit/expiry. | Stale approval rejected. |
| Resume replay | LangGraph node performed write before interrupt and repeats on resume. | Put side effect after interrupt or make it idempotent. | Resume test proves single write. |
| State overwrite | Agent snapshot replaces newer UI filters/draft. | Ownership/reducers/revision checks. | Concurrent update test. |
| Unsafe render | Tool result includes HTML/script-like content. | Escape by default; no raw HTML; sanitize allowed rich content. | Malicious string renders inert. |
| PII in traces | Ledger values/messages copied to observability. | Field-level redaction, sampling, retention, access controls. | Trace fixture inspection and automated redaction test. |
| Fake completion | UI marks transaction complete on tool-call start. | Terminal tool result plus product-system receipt. | Delayed/failing tool never shows success. |
| Cancel/undo confusion | User stops generation after write, assumes it was reversed. | Exact status and separate compensating action. | E2E stop after accept shows receipt and available next action. |
| Mobile replay | App background/reconnect resubmits message or tool. | Stable run/request/idempotency IDs and rejoin. | Lifecycle fault test. |
| Memory poisoning | Unverified categorization becomes permanent user preference. | Provenance, confidence, explicit save, edit/delete/TTL. | Untrusted suggestion never auto-promotes to durable memory. |
| Dependency drift | Caret range installs a changed hook/API after book release. | Exact lockfile, release tag, immutable links, scheduled drift check. | Clean install CI and snippet compile. |

## 25. Trust and transparency: show operational evidence

The manuscript should explicitly reject the promise of exposing hidden chain-of-thought. Instead, design a trust stack:

1. **Status:** what is happening now?
2. **Plan/stage:** what bounded sequence is the runtime attempting?
3. **Action:** which tool/system is being used with which safe-to-display arguments?
4. **Evidence:** which source, record version, timestamp, or calculation supports the output?
5. **Change:** what has changed versus what is merely proposed?
6. **Control:** can the user edit, reject, stop, retry, or compensate?
7. **Provenance:** which agent/runtime/model/tool and principal produced or approved it?

AG-UI reasoning-related events should not be used to make a blanket claim that the application exposes the model's private reasoning. [AG-UI events](https://docs.ag-ui.com/concepts/events) (**D**). Plans, summaries, assumptions, citations, tool calls, and state changes are both more defensible and more useful.

# IX. Verified, source-present, and aspirational matrix

## 26. Status matrix for Chapter 10 claims

| Capability | Finance pin | GTM Operations Workspace pin | Current upstream docs/source | Status allowed now | Upgrade needed for top-notch companion |
| --- | --- | --- | --- | --- | --- |
| Custom application agent UI | Present in RN `ChatScreen.tsx` | Product shell present | v2 hooks documented/source-present | **S** | Run/capture web + mobile; test lifecycle/accessibility. |
| Frontend read tools | Five in finance reads | Not central | v2 `useFrontendTool` present | **S** | Select one, migrate/pin, test schema/abort/unmount. |
| Human approval UI | Four finance HITL gates | Not central | v2 HITL present | **S** | Server-authorized/idempotent write; approve/edit/reject tests. |
| Rendered backend tool | Not established as canonical pattern | Legacy catch-all renderer | v2 `useRenderTool` present | **D/S upstream; A companion** | Implement named server tool renderer and result evidence. |
| Default tool renderer | Not central | Legacy `useDefaultTool` | v2 `useDefaultRenderTool` present | **S** | Migration example and safe redaction. |
| BuiltInAgent | Present, `maxSteps: 10` | Other runtime adapters | current source/docs | **S** | Run with exact version, fail-loud config, evaluated step budget. |
| LangGraph agent | Absent | Absent | official docs current | **D upstream; A companion** | Add only for durable/branching extension; test checkpointer/resume. |
| Durable thread persistence | Not established | Not established | LangGraph/platform docs | **D upstream; A companion** | Production checkpointer, auth-scoped threads, reconnect test. |
| Shared typed state | Some client/product state; not a documented durable contract | Product state exists | AG-UI/CopilotKit docs | **D upstream; A companion** | Typed ownership/revision conflict implementation. |
| Web and mobile parity | Mobile example is primary | Web app exists but different use case | RN/web packages present | **S separate projects; A parity** | One synthetic ledger API and scenarios on both clients. |
| Authentication/tenant isolation | Not proven | Basic gate only | application responsibility | **A** | Implement and adversarially test. |
| Cancellation/rejoin/rollback | Low-level stop path present | Not established | upstream behaviors documented/source-present | **D/S** | Scenario-specific semantics and fault tests. |
| Production finance security | Not established | Not applicable | no source can substitute | **A** | Keep example synthetic; add controls without regulatory claim. |

## 27. Claims the manuscript should avoid

1. “CopilotKit automatically makes an application agentic.”
2. “Any ChatGPT-like interface is a Level 1 agentic application.”
3. “Tool calling means the model autonomously completed the task.”
4. “`useFrontendTool` is safe for secrets or privileged database writes because it has a schema.”
5. “`useHumanInTheLoop` is an authorization system.”
6. “Stopping a run undoes completed tool calls.”
7. “Disconnecting the stream cancels backend work.”
8. “A LangGraph checkpoint reverses external side effects.”
9. “AG-UI step or reasoning events reveal chain-of-thought.”
10. “BuiltInAgent provides durable persistence by default.”
11. “LangGraph is required for every agentic application.”
12. “Multi-agent is the natural next step for every multi-step workflow.”
13. “The finance repo is production-ready, secure banking software, or financial advice.”
14. “The existing screenshots prove the current pinned application runs.”
15. “The web and React Native CopilotKit APIs are identical.”
16. “The current online docs and installed package behavior always match.”
17. “`useDefaultTool` is the preferred v2 generic renderer.”
18. “A provider/backend selector proves interchangeable behavior or safety.”
19. “A prompt restriction is an enforced permission boundary.”
20. “Shared state, thread state, memory, and observability traces are the same storage problem.”

# X. Version-drift and publication protocol

## 28. Source register

| Component | Research snapshot | Evidence |
| --- | --- | --- |
| CopilotKit monorepo | `855446e1abc8f29756dc5e539e5e50a90321ac2d`; package source reports `react-core`, `runtime`, and React Native `1.62.3` | [CopilotKit at SHA](https://github.com/CopilotKit/CopilotKit/tree/855446e1abc8f29756dc5e539e5e50a90321ac2d) (**S**, accessed 2026-07-14). |
| AG-UI used by pinned CopilotKit packages | package manifests include AG-UI `0.0.57` in relevant packages; runtime includes LangGraph adapter `0.0.42` | [`runtime/package.json`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/runtime/package.json) and [`react-native/package.json`](https://github.com/CopilotKit/CopilotKit/blob/855446e1abc8f29756dc5e539e5e50a90321ac2d/packages/react-native/package.json) (**S**, accessed 2026-07-14). |
| Personal Finance Copilot | `d8760064c626712a8fa15c192a8c4bc69bb24055`; manifests request CopilotKit `^1.59.2` | [Repo at SHA](https://github.com/jerelvelarde/personal-finance-copilot/tree/d8760064c626712a8fa15c192a8c4bc69bb24055) (**S**, accessed 2026-07-14). |
| GTM Operations Workspace | `private revision omitted`; manifest requests CopilotKit `^1.62.3`, AG-UI `0.0.57` | GTM Operations Workspace (**S**, accessed 2026-07-14). |
| LangGraph | Current official docs researched; release must be pinned in companion | [LangGraph releases](https://github.com/langchain-ai/langgraph/releases) (**D**, accessed 2026-07-14). |
| LangChain/LangSmith | Current official docs researched; exact packages/model IDs not yet selected | [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents) and [LangSmith evaluation](https://docs.langchain.com/langsmith/evaluation) (**D**, accessed 2026-07-14). |

### Release workflow

1. Freeze a book release tag and lockfile.
2. Record exact package versions, model identifiers/config, OS, Node/Python, package manager, browser, simulator/device, and runtime mode.
3. Compile/test every printed snippet from its source file.
4. Run the full synthetic scenario suite and store machine-readable results.
5. Capture screenshots from that same tag and seed fixture.
6. Check all official doc links for redirects/removals, while keeping immutable source links for implementation facts.
7. Compare current public hook docs against pinned exports; add migration callouts instead of silently updating code.
8. Re-run dependency/security/license review. The researched CopilotKit docs and repository surfaces should not be used to make a license claim until the apparent documentation/repository inconsistency is resolved.
9. Publish an online errata/version matrix mapping book edition to companion tag.
10. Schedule a drift job that clean-installs, compiles snippets, runs high-value e2e cases, and reports upstream API/doc changes without automatically rewriting the manuscript.

### Drift watchlist

- root versus `/v2` CopilotKit imports;
- `useAgent` return type and agent methods;
- `useCopilotKit` imperative API;
- `useFrontendTool`, `useRenderTool`, `useComponent`, and HITL schemas/status types;
- `useDefaultTool` legacy compatibility and v2 fallback renderer;
- React Native automatic polyfills, prebuilt UI exports, and native `useRenderTool` behavior;
- `BuiltInAgent` configuration, default step budget, and runtime handler surface;
- AG-UI event names/payloads and interrupt outcomes;
- CopilotKit–LangGraph interrupt support matrix;
- LangGraph event streaming APIs labeled preview versus stable;
- Next.js route/runtime defaults;
- model IDs and tool-calling/structured-output compatibility.

# XI. Unresolved research and execution queue

The following are the only `[NEED RESEARCH]` items intentionally left open; each requires a publication-time or runtime decision rather than more paraphrasing.

1. **[NEED RESEARCH] Select the exact companion release versions.** Decide whether to upgrade finance from its `^1.59.2` range to the current tested CopilotKit release or maintain a version-specific branch. Do not mix APIs across them.
2. **[NEED RESEARCH] Prove the CopilotKit/LangGraph interrupt path end to end.** Resolve the contradictory LangGraph-specific documentation by running one pinned Python or JavaScript LangGraph agent with `interrupt`, `useInterrupt`, durable checkpointer, disconnect, and resume.
3. **[NEED RESEARCH] Resolve React Native docs versus source.** Confirm which pinned release auto-installs/imports polyfills, which prebuilt native UI components are supported, and whether the finance custom shell should use current native `useRenderTool` or the existing low-level registry traversal.
4. **[NEED RESEARCH] Choose the canonical Level 1 repository layout and public URL.** The user proposed a book repo with `/apps`; define web, mobile, runtime, shared schemas, fixtures, snippets, and tests before chapter drafting locks paths.
5. **[NEED RESEARCH] Define authentication and tenant model.** Select provider/strategy, derive trusted principal and ledger scope server-side, and define thread ownership. No chapter should call the companion production-grade before adversarial tests pass.
6. **[NEED RESEARCH] Choose persistence.** Select a production LangGraph checkpointer or application persistence path, define migrations/retention/encryption, and record local versus hosted behavior.
7. **[NEED RESEARCH] Decide whether durable LangGraph is core Chapter 10 or an extension.** Recommended: ship the first narrow flow on BuiltInAgent, then add a transaction-review graph only if it materially demonstrates reconnect/resume and idempotency.
8. **[NEED RESEARCH] Run both audited repos at their pinned SHAs.** Record clean-install commands, resolved dependency versions, required environment variables, failures, platform support, and fresh captures. Promote only successful cases from S to R.
9. **[NEED RESEARCH] Verify GitHub links containing catch-all route brackets.** The encoded immutable URLs should be checked in final editorial QA.
10. **[NEED RESEARCH] Resolve CopilotKit license wording at the selected release.** Do not print a license claim until official docs/repository metadata agree or the maintainers clarify it.
11. **[NEED RESEARCH] Establish the synthetic finance data policy.** Define fixture names, amounts, accounts, receipt artifacts, and screenshot redaction rules; explicitly state the example is educational and not financial advice.
12. **[NEED RESEARCH] Pin evaluation targets.** For Chapter 10, define success/trajectory datasets, tool-call/argument checks, latency and cost budgets, and online trace sampling using current official [LangSmith evaluation guidance](https://docs.langchain.com/langsmith/evaluation) and [trajectory evaluation](https://docs.langchain.com/langsmith/trajectory-evals) (accessed 2026-07-14).

## Handoff recommendation

Before drafting Chapters 6–10, implement and runtime-verify one thin vertical slice:

```text
authenticated synthetic ledger read
  → agent selects server read tool
  → AG-UI streams lifecycle and typed result
  → application renders accessible spending component
  → agent proposes one transaction write
  → user edits/approves exact proposal
  → server authorizes and idempotently commits
  → UI renders product-system receipt
  → refresh/mobile reconnect rejoins the same thread
```

That slice exercises the central Level 1 thesis—agent, UI, tools, shared state, control, and operations—without pretending that more agents or more tools automatically create more builder value.

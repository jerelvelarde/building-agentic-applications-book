#!/usr/bin/env python3
"""Build the book's deduplicated source registry from its evidence backbone."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
INPUTS = [
    ROOT / "authoring/source-and-evidence-policy.md",
    ROOT / "authoring/terminology.md",
    *sorted((ROOT / "materials/evidence-packets").glob("*.md")),
    ROOT / "materials/code-excerpts/CODE EXCERPT CATALOG.md",
]
OUTPUT = ROOT / "materials/SOURCE REGISTRY.md"
LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
SHA_RE = re.compile(r"/(?:blob|tree)/([0-9a-f]{40})(?:/|$)")


def clean(text: str) -> str:
    text = re.sub(r"[`*_]", "", text).replace("|", "\\|")
    return re.sub(r"\s+", " ", text).strip()


def publisher(url: str) -> str:
    host = urlparse(url).netloc.lower()
    path = urlparse(url).path
    if host == "github.com":
        parts = path.strip("/").split("/")
        owner = parts[0] if parts else "GitHub"
        repo = parts[1] if len(parts) > 1 else ""
        known = {
            ("CopilotKit", "CopilotKit"): "CopilotKit",
            ("CopilotKit", "OpenTag"): "CopilotKit / OpenTag",
            ("jerelvelarde", "personal-finance-copilot"): "Jerel Velarde / Personal Finance Copilot",
            ("jerelvelarde", "GTM Operations Workspace"): "Jerel Velarde / GTM Operations Workspace",
            ("jerelvelarde", "hermes-cpk"): "Jerel Velarde / Hermes–CopilotKit demo",
            ("anthropics", "claude-code"): "Anthropic / Claude Code",
            ("NousResearch", "hermes-agent"): "Nous Research / Hermes Agent",
            ("openclaw", "openclaw"): "OpenClaw",
            ("langchain-ai", "langgraph"): "LangChain / LangGraph",
            ("langchain-ai", "agentevals"): "LangChain / AgentEvals",
            ("ag-ui-protocol", "ag-ui"): "AG-UI",
            ("open-telemetry", "semantic-conventions"): "OpenTelemetry",
        }
        return known.get((owner, repo), f"GitHub / {owner}/{repo}".rstrip("/"))
    mapping = {
        "docs.copilotkit.ai": "CopilotKit",
        "docs.ag-ui.com": "AG-UI",
        "docs.langchain.com": "LangChain",
        "code.claude.com": "Anthropic / Claude Code",
        "claude.com": "Anthropic / Claude Tag",
        "www.anthropic.com": "Anthropic",
        "nextjs.org": "Vercel / Next.js",
        "api.slack.com": "Slack",
        "docs.slack.dev": "Slack",
        "docs.discord.com": "Discord",
        "learn.microsoft.com": "Microsoft",
        "csrc.nist.gov": "NIST",
        "www.nist.gov": "NIST",
        "www.nccoe.nist.gov": "NIST NCCoE",
        "www.rfc-editor.org": "RFC Editor / IETF",
        "owasp.org": "OWASP",
        "genai.owasp.org": "OWASP GenAI Security Project",
        "opentelemetry.io": "OpenTelemetry",
        "aws.amazon.com": "AWS",
        "docs.aws.amazon.com": "AWS",
        "sre.google": "Google SRE",
        "docs.cloud.google.com": "Google Cloud",
    }
    return mapping.get(host, host)


def chapters(path: Path, line: int, heading: str, url: str) -> str:
    name = path.name
    if name == "level-1-foundations.md":
        if line < 160:
            return "1–5"
        if line < 336:
            return "3–7"
        if line < 475:
            return "8–9"
        if line < 593:
            return "10"
        return "1–10"
    for packet, lo, hi in (
        ("level-2-machines.md", 11, 16),
        ("level-3-organizations.md", 17, 22),
        ("production-engineering.md", 23, 26),
    ):
        if name == packet:
            match = re.search(r"Chapter\s+(\d+)", heading, re.I)
            return match.group(1) if match else f"{lo}–{hi}"
    if name == "CODE EXCERPT CATALOG.md":
        if "channels" in url.lower():
            return "18"
        if "langgraph" in url.lower():
            return "8–9"
        if "ag-ui" in url.lower():
            return "16"
        return "6–9"
    return "All"


def evidence(url: str) -> tuple[str, str, str]:
    host = urlparse(url).netloc.lower()
    pinned = SHA_RE.search(url)
    demo = any(x in url for x in ("jerelvelarde/", "CopilotKit/OpenTag"))
    standards = any(
        host.endswith(x)
        for x in (
            "nist.gov",
            "rfc-editor.org",
            "owasp.org",
            "opentelemetry.io",
            "amazon.com",
            "google.com",
        )
    ) or "open-telemetry/semantic-conventions" in url
    if pinned:
        kind = "S — pinned source; demo/reference-only" if demo else "S — pinned source"
        note = f"Immutable source at `{pinned.group(1)}`; source-present is not runtime proof."
        if "jerelvelarde/" in url:
            note += " Publication-permission/license gate applies."
        return "Pinned repository evidence", kind, "Low"
    if standards:
        return "Research and standards", "D — standard or authoritative guidance", "Medium"
    if host == "github.com":
        return "Official web documentation", "D/S — unpinned official repository", "High"
    early = any(x in url.lower() for x in ("claude-tag", "/tag", "channels", "agentic"))
    return "Official web documentation", "D/EA — live official documentation" if early else "D — live official documentation", "High"


def title_for(url: str, labels: list[str]) -> str:
    generic = {"source", "repository", "docs", "documentation", "here", "package.json"}
    choices = [clean(label) for label in labels]
    choices.sort(key=lambda x: ((x.lower() not in generic), len(x)), reverse=True)
    if choices and choices[0].lower() not in generic:
        return choices[0]
    parsed = urlparse(url)
    return f"{parsed.netloc}{parsed.path}".rstrip("/").replace("|", "\\|")


records: dict[str, dict[str, object]] = {}
raw_count = 0
for path in INPUTS:
    heading = ""
    in_fence = False
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and line.startswith("#"):
            heading = clean(line.lstrip("# "))
        if in_fence:
            continue
        for label, url in LINK_RE.findall(line):
            raw_count += 1
            rec = records.setdefault(url, {"labels": [], "chapters": set(), "dates": set(), "refs": []})
            rec["labels"].append(label)
            rec["chapters"].add(chapters(path, line_no, heading, url))
            rec["dates"].add("2026-07-15" if path.name == "CODE EXCERPT CATALOG.md" else "2026-07-14")
            rec["refs"].append(f"{path.relative_to(ROOT)}:{line_no}")

rows_by_category: dict[str, list[dict[str, str]]] = defaultdict(list)
for url, rec in records.items():
    category, kind, drift = evidence(url)
    dates = sorted(rec["dates"])
    title = title_for(url, rec["labels"])
    chapters_text = ", ".join(sorted(rec["chapters"], key=lambda x: int(re.match(r"\d+", x).group()) if re.match(r"\d+", x) else 99))
    note = "Immutable locator; source-present is not runtime proof." if category == "Pinned repository evidence" else "Recheck live content, status, and API wording at publication freeze."
    if kind.startswith("D — standard"):
        note = "Authoritative guidance; confirm revision/status at publication freeze."
    if "jerelvelarde/" in url:
        note = "Pinned demo evidence only; no runtime claim. Confirm publication permission/license."
    if "CopilotKit/OpenTag" in url:
        note = "Pinned case-study evidence only; distinguish main from managed-development snapshot."
    if "claude-tag" in url or "/product/tag" in url or "introducing-claude-tag" in url:
        note = "Time-sensitive beta/product surface; reverify availability and supported channels."
    if "channels-intelligence" in url:
        note = "Source-present early-access/internal surface; do not claim general availability."
    rows_by_category[category].append(
        {
            "title": title,
            "publisher": publisher(url),
            "url": url,
            "type": kind,
            "chapters": chapters_text,
            "date": "/".join(dates),
            "drift": drift,
            "note": note,
        }
    )

for values in rows_by_category.values():
    values.sort(key=lambda row: (row["publisher"].lower(), row["title"].lower(), row["url"]))


def esc(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def compact_chapters(values: list[str]) -> str:
    numbers: set[int] = set()
    keep_all = False
    for value in values:
        if "All" in value:
            keep_all = True
        for start, end in re.findall(r"(\d+)(?:–(\d+))?", value):
            lo, hi = int(start), int(end or start)
            numbers.update(range(lo, hi + 1))
    if keep_all:
        return "All"
    runs: list[str] = []
    ordered = sorted(numbers)
    if not ordered:
        return "—"
    start = previous = ordered[0]
    for number in ordered[1:] + [ordered[-1] + 2]:
        if number == previous + 1:
            previous = number
            continue
        runs.append(str(start) if start == previous else f"{start}–{previous}")
        start = previous = number
    return ", ".join(runs)


lines: list[str] = [
    "---",
    'title: "Agentic Applications 2026 — Source Registry"',
    "status: review-draft",
    "updated: 2026-07-15",
    "source_cutoff: 2026-07-14",
    "---",
    "",
    "# Source Registry",
    "",
    "This is the manuscript's source-management backbone. It follows `book-components/authoring/source-and-evidence-policy.md`: primary sources first, immutable repository locators for implementation claims, and explicit separation between documented, source-present, runtime-observed, early-access, editorial, and aspirational evidence. It does **not** promote any source-present demo to runtime-verified status.",
    "",
    "## Registry completeness",
    "",
    f"- Inputs: **{len(INPUTS)}** evidence-policy, terminology, packet, and code-catalog files.",
    f"- Markdown citations scanned outside code fences: **{raw_count}**.",
    f"- Unique exact source URLs after deduplication: **{len(records)}**.",
    f"- Duplicate citation occurrences collapsed: **{raw_count - len(records)}**.",
    "- Repository verification dates are 2026-07-14 for research packets and 2026-07-15 where the compiled code catalog added evidence.",
    "- Deduplication key: exact URL, including a line/section fragment when it is the evidence locator. A pinned root and a pinned file are separate source records because they support different claims.",
    "",
    "## Evidence and citation rules for authors",
    "",
    "1. Cite factual or time-sensitive claims at the sentence or paragraph they support; do not leave a link pile at chapter end.",
    "2. Use official documentation for documented behavior and immutable repository links for API/source assertions. If they disagree, teach the tested pin and disclose the drift.",
    "3. In prose, translate internal labels: **D** as “official documentation states,” **S** as “at the pinned commit, the source includes,” **R** as “in our recorded run,” **EA** with the exact availability label/date, **E** as “we define/recommend,” and **A** as “the target build should.”",
    "4. Never use S as R. A committed screenshot, test, UI shell, or health endpoint is not an end-to-end run.",
    "5. For code excerpts, cite the immutable file/symbol, name the upstream license, and print only the verified region from `book-components/materials/code-excerpts/CODE EXCERPT CATALOG.md`.",
    "6. Prefer paraphrase. Quote sparingly, accurately, and within source-license/copyright limits.",
    "7. Give product comparisons an evidence date. Avoid undated “supports,” “best,” “secure,” “production-ready,” price, model-default, channel, or package-version claims.",
    "8. Captions must say **illustrative**, **source-present**, **HTTP/runtime-layer verified**, or **end-to-end runtime-verified** and include the capture record when proof is claimed.",
    "9. Use the book's canonical product names: CopilotKit, AG-UI, MCP, LangChain, LangGraph, LangSmith, Channels SDK, OpenTag, Claude Tag, Claude Code, Hermes, and OpenClaw.",
    "10. Before publication, run the revalidation matrix below and replace every unresolved source flag with a dated result or an explicit limitation.",
    "",
    "## Named-claim publication revalidation matrix",
    "",
    "| Product/protocol/framework | Claims that must be reverified | Current evidence boundary | Chapters | Publication action |",
    "|---|---|---|---:|---|",
    "| CopilotKit React/web primitives | v2 exports, hook signatures/imports, `useAgent`, `useCopilotKit`, `useFrontendTool`, `useRenderTool`, `useComponent`, `useHumanInTheLoop`, `useInterrupt`, legacy `useDefaultTool` migration | Pinned source `855446e…`; live docs may drift | 3–10 | Clean-install exact lockfile; compile/test every printed excerpt; compare public docs with exports. |",
    "| CopilotKit React Native | Supported components/hooks, polyfills, bare RN versus Expo guidance, lifecycle behavior | Pinned source and live quickstart currently require reconciliation | 10 | Run web/iOS/Android target selected for the book; document exact device/runtime. |",
    "| CopilotKit BuiltInAgent | Constructor/configuration, event behavior, step limits, persistence implications | Source-present, not a durable-runtime guarantee | 3, 8–10 | Pin package and run boundary/failure tests. |",
    "| AG-UI | Event names/payloads, optional reasoning events, custom events, interrupt semantics, package version | Official live docs plus pinned CopilotKit dependency | 3–9, 15–18 | Pin protocol/packages and verify emitted traces; never equate events with hidden reasoning. |",
    "| LangChain | Agent/model/tool APIs, middleware, MCP interceptors, dynamic model routing | Rolling official docs | 1–10, 23–26 | Pin Python/JS versions and model/provider configuration. |",
    "| LangGraph | Persistence/checkpointer, interrupts, streaming, fault tolerance, join/rejoin, store APIs | Rolling docs; companion graph is compile/test verified only | 8–10, 23–25 | Run durable interrupt, disconnect, resume, idempotency, and recovery scenarios. |",
    "| LangSmith / AgentEvals | Evaluation APIs, trajectory matcher signatures, online evaluation, auth, retention, costs, OTel integration | Rolling docs and unpinned AgentEvals repository | 23–25 | Pin package/plan behavior and execute the evaluation dataset. |",
    "| Claude Code | Version, permissions, sandboxing, hooks, subagents, MCP, worktrees, devcontainer behavior | Repo pin plus rolling docs; only CLI version was runtime-observed | 11–16 | Recheck current version and run the exact comparison cases. |",
    "| Hermes Agent | Upstream package/version, security/path/checkpoint behavior, external AG-UI adapter compatibility | Upstream pin differs from absent demo fork | 11–16 | Identify/license/pin adapter and fork; do not transfer upstream capabilities to demo. |",
    "| OpenClaw | Package/version, trust model, sandbox/tool/elevated policy, exec approvals, skills, managed worktrees | Pinned official source | 11–16 | Re-run comparison and retain warning against hostile multi-tenant use in one trust boundary. |",
    "| Channels SDK | Package names/versions, Slack/Discord/Teams adapter capabilities, StateStore/locking/dedup semantics | Pinned source ahead of parts of public docs | 17–22 | Run each claimed adapter; document declared capabilities and fallbacks. |",
    "| OpenTag | Current release line, package migration, wired adapters, managed branch status | Main and managed-development pins differ | 17–22 | Select one release; never splice APIs; fresh runtime captures required. |",
    "| CopilotKit Intelligence | Name, access status, regions, adapters, pricing, responsibility boundary | Source-present/early-access; public waitlist language | 18, 21–22 | Obtain current official public evidence or keep EA/internal qualification. |",
    "| Claude Tag | Public-beta/GA status, plan eligibility, Slack/Teams support, identity, memory, logs, security/data behavior | Dated 2026 product/docs evidence | 17, 21–22 | Reverify immediately before layout lock; separate service identity from requester permissions. |",
    "| Slack, Discord, Microsoft Teams | Events/socket/gateway/interaction limits, signing/auth, scopes/consent/RSC, acknowledgement and UI capabilities | Rolling platform docs | 18–22 | Run capture tenant(s), verify scopes and request authentication, document platform-specific fallbacks. |",
    "| MCP | Protocol/API version and tool/resource semantics; distinction from AG-UI | Official LangChain/tool docs used in packets | 3, 12, 18, 25 | Pin implementation and keep agent↔tool separate from agent↔UI. |",
    "| OpenTelemetry GenAI conventions | Stability status, exact semantic-convention release, sensitive-data handling | GenAI conventions marked development in evidence packet | 23 | Keep a stable internal schema; pin export mapping. |",
    "| OWASP Agentic guidance | 2026 ASI01–ASI10 names and Agentic Skills revision | Official 2026 resources | 12–13, 19–25 | Recheck revision; map each cited risk to an enforcement/test, not a slogan. |",
    "| NIST agent identity/AI guidance | Whether concept papers were superseded; SP/AI RMF revisions | Standards plus 2026 concept paper | 19–25 | Cite normative status exactly; do not present a concept paper as a final standard. |",
    "| Next.js and deployment/runtime details | Route-handler/middleware/runtime defaults used by examples | Live Next.js docs and pinned demo source | 3, 10, 15 | Pin framework and deployment target; clean-build/run. |",
    "",
    "## Demo and reference-only material",
    "",
    "| Material | Immutable reference | Permitted use | Prohibited inference |",
    "|---|---|---|---|",
    "| Personal Finance Copilot | `d8760064c626712a8fa15c192a8c4bc69bb24055` | Canonical Level 1 mobile source pattern | Production finance, auth, tenant isolation, durable LangGraph, or current runtime proof |",
    "| GTM Operations Workspace | `private revision omitted` | Web/PWA case study and Level 1→2 seam | Interchangeable/safe backends or reproducible Hermes runtime |",
    "| Hermes–CopilotKit demo | `fc43491368f19248ca58e1409501cd28722d0f61` | Visible unsafe baseline and hardening ladder | Bundled adapter, sandbox, authorization, rollback, or end-to-end run |",
    "| OpenTag main | `df93bc0dccd0afc8eb7bb02206ffbe2ef7922322` | Channel-agent product pattern and governance-gap analysis | Current Channels packages, Teams wiring, RBAC/ABAC, bound approvals, institutional memory, immutable audit |",
    "| OpenTag managed-development | `d6a807783136a9e0b6a610f16648df8f1980cdbc` | Source-present managed direction | Generally available CopilotKit Intelligence |",
    "| Existing repository screenshots/frames | `images/repository-captures/` ledger | Clearly labeled reference illustration | Runtime proof; all publication proof images require fresh capture metadata |",
    "",
]

prefixes = {"Pinned repository evidence": "SRC", "Official web documentation": "DOC", "Research and standards": "STD"}
for category in ("Pinned repository evidence", "Official web documentation", "Research and standards"):
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows_by_category[category]:
        sha = SHA_RE.search(row["url"])
        key = f"{row['publisher']}@{sha.group(1)}" if sha else row["publisher"]
        grouped[key].append(row)
    lines += [f"## {category}", "", "Each row is one deduplicated source family. Every distinct cited page or immutable file locator remains linked in the title/locator cell.", "", "| ID | Publisher/project and pin | Titled pages / exact locators | Evidence type | Chapters | Verified | Drift | Notes |", "|---|---|---|---|---:|---|---|---|"]
    for index, (group_key, group_rows) in enumerate(sorted(grouped.items()), 1):
        source_id = f"{prefixes[category]}-{index:03d}"
        links = "<br>".join(f"[{esc(row['title'])}]({row['url']})" for row in group_rows)
        types = ", ".join(sorted({row["type"] for row in group_rows}))
        supported = compact_chapters([row["chapters"] for row in group_rows])
        dates = "/".join(sorted({date for row in group_rows for date in row["date"].split("/")}))
        drift = "High" if any(row["drift"] == "High" for row in group_rows) else "Medium" if any(row["drift"] == "Medium" for row in group_rows) else "Low"
        notes = " ".join(dict.fromkeys(row["note"] for row in group_rows))
        lines.append(
            f"| {source_id} | {esc(group_key)} | {links} | {esc(types)} | {esc(supported)} | {dates} | {drift} | {esc(notes)} |"
        )
    lines.append("")

lines += [
    "## Publication bibliography by part",
    "",
    "The three registry tables above are the canonical bibliography. Filter their **Chapters** column for the exact chapter. This compact part index records the required source families without duplicating 231 URLs.",
    "",
    "| Part / chapters | Required primary-source families | Repository pins / case studies | Publication emphasis |",
    "|---|---|---|---|",
    "| Foundations and Level 1, Chapters 1–10 | CopilotKit web/native hooks and runtime; AG-UI events; LangChain agents/models/tools; LangGraph persistence, streaming, interrupts; LangSmith thread/evaluation concepts; Next.js | CopilotKit `855446e…`; Personal Finance `d876006…`; GTM Operations Workspace `private revision omitted…` | Taxonomy, trust boundaries, UI lifecycle, tools/rendering, state, HITL, web/mobile build. |",
    "| Machine Agents, Chapters 11–16 | Claude Code permissions/security/sandbox/hooks/MCP/worktrees; Hermes architecture/security/checkpoints; OpenClaw policy/sandbox/skills/worktrees | Claude Code `b7784f2…`; Hermes `5d41035…`; OpenClaw `2372c71…`; Hermes–CopilotKit `fc43491…`; GTM Operations Workspace `private revision omitted…` | Harness, skills, capabilities, containment, comparison, visible demo seam, hardening and operations. |",
    "| Organizational Agents, Chapters 17–22 | Channels/Adapters; Slack/Discord/Teams platform docs; Claude Tag docs; NIST ABAC/Zero Trust; RFC 8693; OWASP | CopilotKit `855446e…`; OpenTag main `df93bc0…`; managed-development `d6a8077…` | Channel vs governed actor, identity/authority, bound approvals, delegation, memory, rollout. |",
    "| Production Engineering, Chapters 23–26 | LangSmith/AgentEvals; OpenTelemetry; OWASP/NIST; LangGraph durability; AWS queues/isolation; Google SRE | All audited application pins | Trajectory evaluation, security enforcement, idempotency/recovery, budgets/SLOs/isolation, smallest-authority choice. |",
    "",
]

lines += [
    "## Unresolved-source queue",
    "",
    "1. Select the canonical companion repository URL, release tag, folder layout, license, and maintenance window.",
    "2. Obtain explicit publication permission for code/screenshots from user-owned repositories without a confirmed license file.",
    "3. Identify and pin the Hermes AG-UI adapter/external fork used by the demos; verify license and end-to-end compatibility.",
    "4. Resolve CopilotKit React Native documentation versus pinned source behavior, including polyfills and supported render APIs.",
    "5. Runtime-verify one durable LangGraph interrupt → disconnect → resume → single idempotent write path.",
    "6. Select the OpenTag release line and decide whether Level 3 covers direct Channels only or a public managed path as well.",
    "7. Reverify Claude Tag status and Teams availability at layout freeze.",
    "8. Choose and verify the Level 3 StateStore, policy engine, approval binding, audit backend, and institutional-memory controls before production claims.",
    "9. Run fresh Slack/Discord/Teams captures only for adapters actually exercised with synthetic fixtures and recorded metadata.",
    "10. Resolve CopilotKit repository/license wording for the selected release and record third-party notices for every printed excerpt.",
    "11. Pin OTel semantic conventions, OWASP revisions, NIST normative status, LangSmith/AgentEvals packages, and all model/provider identifiers at code freeze.",
    "12. Replace every remaining S/EA/A manuscript claim that reads like R/GA with either runtime evidence or explicit qualification.",
    "",
    "## Maintenance protocol",
    "",
    "At code freeze: rerun this generator, inspect additions/removals, check every live URL, clean-install the companion lockfiles, run excerpt tests, and store a dated diff. Do not automatically rewrite manuscript claims from doc drift; route each change through technical review.",
    "",
]

OUTPUT.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {OUTPUT} with {raw_count} citations and {len(records)} unique URLs")

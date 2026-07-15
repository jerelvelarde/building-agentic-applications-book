import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const out = dirname(fileURLToPath(import.meta.url));
const C = {
  bg: "#FAFAFC", ink: "#11143D", text: "#010507", secondary: "#57575B",
  border: "#DBDBE5", lilac: "#BEC2FF", lilacSoft: "#EEE6FE",
  mint: "#85ECCE", mintSoft: "#E7FBF5", red: "#FA5F67", redSoft: "#FFF0F1",
  orange: "#FFAC4D", orangeSoft: "#FFF5E8", white: "#FFFFFF", pale: "#EDEDF5",
  purple: "#6857D9",
};

const esc = (s) => String(s).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
const rect = (x, y, w, h, fill = C.white, stroke = C.border, rx = 24, sw = 2) =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>`;
const text = (x, y, value, cls = "body", anchor = "start", fill = "") =>
  `<text x="${x}" y="${y}" class="${cls}" text-anchor="${anchor}"${fill ? ` style="fill:${fill}"` : ""}>${esc(value)}</text>`;
const lines = (x, y, values, cls = "body", gap = 38, anchor = "start", fill = "") =>
  `<text x="${x}" y="${y}" class="${cls}" text-anchor="${anchor}"${fill ? ` style="fill:${fill}"` : ""}>${values.map((v, i) => `<tspan x="${x}" dy="${i ? gap : 0}">${esc(v)}</tspan>`).join("")}</text>`;
const pill = (x, y, w, label, fill = C.pale, color = C.secondary) =>
  `${rect(x, y, w, 46, fill, fill, 23, 1)}${text(x + w / 2, y + 31, label, "label", "middle", color)}`;
const arrow = (x1, y1, x2, y2, color = C.purple, dashed = false, label = "") =>
  `<path d="M${x1} ${y1} L${x2} ${y2}" fill="none" stroke="${color}" stroke-width="5"${dashed ? ' stroke-dasharray="12 10"' : ""} marker-end="url(#arrow)"/>${label ? text((x1 + x2) / 2, (y1 + y2) / 2 - 14, label, "small", "middle") : ""}`;
const card = ({ x, y, w, h, label, heading, body = [], accent = C.lilac, fill = C.white, dark = false }) => {
  const fg = dark ? C.white : C.ink;
  const secondary = dark ? C.white : C.secondary;
  const labelW = Math.min(w - 44, Math.max(130, label.length * 14 + 36));
  return `${rect(x, y, w, h, fill, accent, 28, 3)}${pill(x + 22, y + 20, labelW, label, accent, dark ? C.ink : C.secondary)}${text(x + 26, y + 104, heading, "heading", "start", fg)}${lines(x + 26, y + 154, body, "small", 38, "start", secondary)}`;
};
const base = (title, subtitle, desc) => `<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">
<title id="title">${esc(title)}</title><desc id="desc">${esc(desc)}</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M0 0L10 5L0 10Z" fill="${C.purple}"/></marker>
<style>.title{font:700 52px 'Plus Jakarta Sans',Arial,sans-serif;fill:${C.ink}}.subtitle{font:400 30px 'Plus Jakarta Sans',Arial,sans-serif;fill:${C.secondary}}.heading{font:700 32px 'Plus Jakarta Sans',Arial,sans-serif;fill:${C.ink}}.body{font:600 30px 'Plus Jakarta Sans',Arial,sans-serif;fill:${C.ink}}.small{font:400 27px 'Plus Jakarta Sans',Arial,sans-serif;fill:${C.secondary}}.foot{font:600 25px 'Plus Jakarta Sans',Arial,sans-serif;fill:${C.white}}.label{font:700 20px 'Spline Sans Mono',monospace;letter-spacing:1px;fill:${C.secondary}}</style></defs>
<rect width="1600" height="900" fill="${C.bg}"/>${text(78, 80, title, "title")}${text(78, 126, subtitle, "subtitle")}`;
const footer = (value) => `${rect(100, 804, 1400, 66, C.ink, C.ink, 22, 0)}${text(800, 846, value, "foot", "middle", C.white)}</svg>`;
const save = (name, svg) => writeFileSync(join(out, name), svg);

function flow(name, title, subtitle, desc, nodes, foot) {
  let s = base(title, subtitle, desc);
  const gap = 24, x0 = 58, y = 245, h = 350;
  const w = (1484 - gap * (nodes.length - 1)) / nodes.length;
  nodes.forEach((n, i) => {
    const x = x0 + i * (w + gap);
    s += card({ x, y, w, h, label: n.label, heading: n.heading, body: n.body, accent: n.accent ?? (i % 2 ? C.mint : C.lilac), fill: n.fill ?? C.white });
    if (i < nodes.length - 1) s += arrow(x + w, y + h / 2, x + w + gap - 4, y + h / 2);
  });
  save(name, s + footer(foot));
}

// Figure 2.2 — explicit editorial gap.
{
  let s = base("Choose the least adaptive architecture that works", "Start with rules. Add model choice only where observation changes the path.", "Decision tree routing a task from deterministic rules to a model feature, workflow, bounded assistant, or adaptive agent.");
  const nodes = [
    [80, 225, 320, "Rules are enough?", "YES → no model", C.mint],
    [470, 225, 320, "One model step?", "YES → model feature", C.lilac],
    [860, 225, 320, "Steps are known?", "YES → workflow", C.lilac],
    [275, 525, 420, "User stays in control?", "YES → tool assistant", C.orange],
    [905, 525, 420, "Environment changes path?", "YES → bounded agent", C.red],
  ];
  nodes.forEach(([x, y, w, q, a, accent]) => { s += card({ x, y, w, h: 190, label: "DECISION", heading: q, body: [a], accent }); });
  s += arrow(400, 320, 470, 320); s += arrow(790, 320, 860, 320); s += arrow(1020, 415, 1115, 525); s += arrow(630, 415, 485, 525);
  s += text(800, 755, "If acceptable trajectories cannot be defined and measured, reduce agency.", "body", "middle");
  save("fig-ch02-02-workflow-or-agent-decision-tree.svg", s + footer("The first valid stop is the architecture—not a lower rung on a maturity ladder."));
}

// Figure II.1 — two-row serpentine build path with dedicated arrow gutters.
{
  let s = base("The Level 1 build path", "Six chapters turn a chat surface into a production application control plane.", "Six-step roadmap from tracing a run through tool placement, semantic rendering, shared state, durable approval, and production release.");
  const steps = [
    { x: 70, y: 190, label: "CHAPTER 5", heading: "Trace the run", body: ["identity + events", "terminal evidence"], accent: C.lilac },
    { x: 585, y: 190, label: "CHAPTER 6", heading: "Place tools", body: ["client vs server", "effects + receipts"], accent: C.mint },
    { x: 1100, y: 190, label: "CHAPTER 7", heading: "Render artifacts", body: ["semantic object", "platform-native UI"], accent: C.lilac },
    { x: 1100, y: 500, label: "CHAPTER 8", heading: "Share state", body: ["ownership + revision", "durable stores"], accent: C.mint },
    { x: 585, y: 500, label: "CHAPTER 9", heading: "Pause safely", body: ["bound approval", "resume + reconcile"], accent: C.lilac },
    { x: 70, y: 500, label: "CHAPTER 10", heading: "Ship the system", body: ["compatibility + evals", "operations + rollout"], accent: C.mint },
  ];
  steps.forEach((step) => s += card({ ...step, w: 430, h: 240 }));
  s += arrow(500, 310, 580, 310);
  s += arrow(1015, 310, 1095, 310);
  s += arrow(1315, 430, 1315, 495);
  s += arrow(1100, 620, 1020, 620);
  s += arrow(585, 620, 505, 620);
  save("fig-ch05-00-level1-build-path.svg", s + footer("Every chapter adds an enforcement point, evidence, and failure behavior—not another chat feature."));
}

// Chapter 6 — temporal least privilege.
{
  let s = base("Capabilities should exist only when the phase needs them", "A version-bound approval opens one narrow mutation window; completion closes it.", "Timing chart across understand, propose, wait, commit, and complete phases showing read, render, approval, write, and verification capabilities appearing only when needed.");
  const phases = ["UNDERSTAND", "PROPOSE", "WAIT", "COMMIT", "COMPLETE"];
  const laneX = 150, laneW = 1290, columnW = laneW / phases.length;
  phases.forEach((p, i) => { const x = laneX + i * columnW + 24; s += pill(x, 190, 210, p, i === 3 ? C.mint : C.pale); });
  const lanes = [["READ", 270, 0, 1], ["RENDER", 360, 0, 4], ["APPROVE", 450, 2, 2], ["WRITE", 540, 3, 3], ["VERIFY", 630, 3, 4]];
  lanes.forEach(([name, y, start, end]) => {
    s += text(45, y + 36, name, "label");
    s += rect(laneX, y, laneW, 58, C.white, C.border, 18, 2);
    const x = laneX + start * columnW + 12;
    const w = (end - start + 1) * columnW - 24;
    s += rect(x, y + 9, w, 40, start === 3 ? C.mintSoft : C.lilacSoft, start === 3 ? C.mint : C.lilac, 15, 2);
  });
  s += `<text x="${laneX + 2.5 * columnW}" y="488" class="small" text-anchor="middle" style="font-size:18px;fill:${C.ink}">digest-bound approval</text>`;
  save("fig-ch06-05-capabilities-by-phase.svg", s + footer("Retrieved content may request a capability; only trusted phase state can make it available."));
}

// Chapter 8 — three durable stores.
{
  let s = base("Checkpoint, memory, and product truth are different stores", "Duplicate the reference, not the authoritative business record.", "Three-store boundary diagram separating thread checkpoint state, cross-thread memory, and the authoritative ledger database.");
  const stores = [
    { x: 55, label: "THREAD CHECKPOINT", heading: "Resume this run", body: ["messages + graph state", "interrupt + cursor", "retention by thread"], accent: C.lilac },
    { x: 610, label: "MEMORY STORE", heading: "Reuse scoped context", body: ["preference + provenance", "scope + expiry", "not task truth"], accent: C.orange },
    { x: 1165, label: "PRODUCT DATABASE", heading: "Own the ledger", body: ["accounts + transactions", "versions + receipts", "authoritative effect"], accent: C.mint },
  ];
  stores.forEach((v) => s += card({ ...v, y: 230, w: 380, h: 430 }));

  // Connector copy belongs to the 175 px gutters, never on top of card content.
  // Split labels keep their measured text width inside the gutter while the arrow
  // runs on its own lower rail, leaving a clear 24 px gap between copy and line.
  const gutterConnector = (x1, x2, labelLines) => {
    const center = (x1 + x2) / 2;
    return `${rect(x1, 374, x2 - x1, 72, C.bg, C.border, 18, 1)}${lines(center, 401, labelLines, "label", 24, "middle", C.secondary)}${arrow(x1, 480, x2, 480, C.purple, true)}`;
  };
  s += gutterConnector(447, 598, ["SCOPED", "REFERENCE"]);
  s += gutterConnector(1002, 1153, ["STABLE ID", "+ VERSION"]);
  s += text(800, 740, "A trace observes all three. It replaces none of them.", "body", "middle");
  save("fig-ch08-04-three-store-boundary.svg", s + footer("Recover runtime state without silently recreating or overwriting product state."));
}

// Chapter 12 — independent verification.
flow("fig-ch12-04-independent-verifier-pipeline.svg", "Verification belongs to an independent producer", "The model may propose success. A fixed verifier emits the terminal evidence.", "Verification pipeline grouping format and static checks, tests and build, artifact and diff policy, and containment assertions with recorded provenance.", [
  { label: "GATE 1", heading: "Static quality", body: ["format · lint", "typecheck"] },
  { label: "GATE 2", heading: "Behavior", body: ["tests · build", "negative assertions"] },
  { label: "GATE 3", heading: "Artifact policy", body: ["diff · secret scan", "digest · inventory"], accent: C.orange },
  { label: "GATE 4", heading: "Containment", body: ["denied path + egress", "canary + leftovers"], accent: C.red },
  { label: "VERIFIER", heading: "Evidence bundle", body: ["argv · env · exit", "digest + terminal state"], accent: C.mint },
], "A passing assistant message is narration. A verifier result is evidence with a producer and artifact digest.");

// Chapter 13 — filesystem boundary.
{
  let s = base("Filesystem scope must survive path tricks", "Resolve the real object, constrain the parent, and rely on an OS boundary for stronger assurance.", "Three filesystem panels show an in-root read allowed, an outward symlink denied, and a symlinked write parent denied, plus a check-then-open race warning.");
  const panels = [
    { x: 70, label: "SAFE READ", heading: "realpath stays in root", body: ["/work/report.csv", "open by broker", "receipt: allowed"], accent: C.mint },
    { x: 555, label: "DENIED READ", heading: "symlink leaves root", body: ["/work/vendor → /etc", "resolved target outside", "receipt: denied"], accent: C.red },
    { x: 1040, label: "DENIED WRITE", heading: "parent leaves root", body: ["/work/out → /tmp", "resolve existing parent", "receipt: denied"], accent: C.red },
  ];
  panels.forEach((v) => s += card({ ...v, y: 220, w: 420, h: 390 }));
  s += rect(260, 660, 1080, 92, C.orangeSoft, C.orange, 24, 2); s += text(800, 700, "Check → attacker swaps path → open", "heading", "middle"); s += text(800, 735, "Use brokered file descriptors, mount boundaries, and no ambient terminal escape.", "small", "middle");
  save("fig-ch13-03-filesystem-path-boundaries.svg", s + footer("A lexical prefix check is input validation—not filesystem containment."));
}

// Chapter 17 — policy hierarchy.
{
  let s = base("Organizational policy can narrow authority, never expand it", "Each lower scope inherits the ceiling above it and may only remove capability.", "Descending policy hierarchy from organization through workspace, agent, channel, task, and requester action, with a denied payroll-access example.");
  const levels = [
    [130, 185, 1340, "ORGANIZATION", "global prohibited data + actions", C.ink, true],
    [210, 275, 1180, "WORKSPACE", "installed tools + tenant boundaries", C.lilac, false],
    [290, 365, 1020, "AGENT PROFILE", "owned capabilities + credential modes", C.mint, false],
    [370, 455, 860, "CHANNEL", "destination disclosure + guest limits", C.orange, false],
    [450, 545, 700, "THREAD / TASK", "purpose + expiry + budget", C.lilac, false],
    [450, 635, 700, "REQUESTER ACTION", "principal + exact resource", C.mint, false],
  ];
  levels.forEach(([x, y, w, label, value, accent, dark]) => { s += rect(x, y, w, 72, dark ? C.ink : C.white, accent, 22, 3); s += text(x + 24, y + 45, label, "label", "start", dark ? C.white : C.secondary); s += text(x + w - 24, y + 46, value, "small", "end", dark ? C.white : C.secondary); });
  s += arrow(1510, 250, 1510, 690);
  s += `<text x="1544" y="470" class="label" text-anchor="middle" style="fill:${C.purple}" transform="rotate(90 1544 470)">ONLY NARROWS</text>`;
  s += text(800, 760, "DENY: public channel cannot add payroll scope", "small", "middle", C.red);
  save("fig-ch17-03-policy-hierarchy.svg", s + footer("Context may suggest a request. Only the effective policy intersection grants an action."));
}

// Chapter 18 — graceful degradation.
{
  let s = base("Channel UI degrades by presentation, not by meaning", "Required semantics survive even when a platform cannot render the preferred component.", "Three-tier graceful-degradation ladder from required action semantics through structured channel UI to safe text and web fallback.");
  const tiers = [
    [150, 215, 1300, 150, "REQUIRED SEMANTICS", "action · target · consequence · actor · expiry · decision", C.ink, true],
    [260, 410, 1080, 150, "PREFERRED CHANNEL UI", "fields · buttons · selects · progress · accessible summary", C.lilac, false],
    [370, 605, 860, 130, "SAFE FALLBACK", "plain text + authenticated URL + explicit acknowledgement", C.mint, false],
  ];
  tiers.forEach(([x, y, w, h, label, value, accent, dark]) => { s += rect(x, y, w, h, dark ? C.ink : C.white, accent, 28, 3); s += text(x + 28, y + 54, label, "label", "start", dark ? C.white : C.secondary); s += text(x + w / 2, y + 105, value, "body", "middle", dark ? C.white : C.ink); });
  s += arrow(800, 365, 800, 408); s += arrow(800, 560, 800, 603);
  save("fig-ch18-04-graceful-degradation-ladder.svg", s + footer("A missing button may change interaction. It must not erase identity, consequence, or approval semantics."));
}

// Production part opener.
{
  let s = base("One production discipline across three authority surfaces", "Observe the run, enforce the boundary, operate failure, and reduce authority when evidence allows.", "Production control loop centered on a run with trajectory evaluation, authority defense, reliability budgets, and minimum-authority selection, grounded by the control chain.");
  s += card({ x: 600, y: 300, w: 400, h: 230, label: "THE RUN", heading: "Goal → action → effect", body: ["state + identity", "evidence + outcome"], accent: C.ink, fill: C.ink, dark: true });
  const outer = [
    [80, 205, "EVALUATE", "Trajectory", ["required + forbidden", "regression gate"], C.lilac],
    [1120, 205, "DEFEND", "Authority", ["identity + policy", "narrow credential"], C.mint],
    [80, 490, "OPERATE", "Reliability", ["deadline + budget", "reconcile failure"], C.orange],
    [1120, 490, "SELECT", "Minimum level", ["outcome + harm", "upgrade or downshift"], C.lilac],
  ];
  outer.forEach(([x, y, label, heading, body, accent]) => { s += card({ x, y, w: 390, h: 210, label, heading, body, accent }); s += arrow(x < 800 ? x + 390 : x, y + 105, x < 800 ? 595 : 1005, 415, C.purple, false); });
  s += rect(260, 718, 1080, 58, C.pale, C.lilac, 20, 2);
  s += text(800, 756, "intent → enforcement point → evidence → failure behavior", "small", "middle");
  save("fig-ch23-00-production-control-loop.svg", s + footer("Observed failure feeds design change; production readiness is part of the architecture."));
}

// Chapter 23 — dataset portfolio.
{
  let s = base("Maintain a portfolio of six evaluation suites", "Every capability change adds cases; every case carries a reproducible envelope.", "Six evaluation suite cards above a reusable case envelope containing ownership, sensitivity, fixture and component versions, expected and forbidden outcomes, evaluator, repetitions, and retirement.");
  const suites = [["GOLDEN", "safe success"], ["BOUNDARY", "edge inputs"], ["POLICY", "allow · deny"], ["ADVERSARIAL", "injection"], ["RELIABILITY", "timeout · replay"], ["REGRESSION", "known failures"]];
  suites.forEach(([a, b], i) => { const x = 52 + i * 255; s += card({ x, y: 190, w: 225, h: 210, label: `SUITE ${i + 1}`, heading: a, body: [b], accent: i % 2 ? C.mint : C.lilac }); });
  s += rect(100, 470, 1400, 250, C.white, C.border, 28, 2); s += pill(130, 495, 250, "CASE ENVELOPE", C.ink, C.white);
  const fields = ["owner + sensitivity", "fixture + dataset version", "model · prompt · tool · policy", "expected + forbidden outcomes", "evaluator + repetitions", "retirement reason"];
  fields.forEach((v, i) => { const x = 140 + (i % 3) * 460, y = 585 + Math.floor(i / 3) * 70; s += text(x, y, `□ ${v}`, "small"); });
  save("fig-ch23-03-dataset-suites-and-case-envelope.svg", s + footer("A score without the case envelope cannot explain why it changed."));
}

// Chapter 23 — severity and safe success.
{
  let s = base("Severity controls release behavior before scoring begins", "Safe task success is a conjunction; critical failure cannot be averaged away.", "Four severity tiers with release actions above a safe-task-success formula requiring result, path, policy, verified effect, and budget adherence.");
  const tiers = [
    [55, "CRITICAL", ["unauthorized", "effect"], ["zero tolerance", "stop release"], C.red],
    [430, "HIGH", ["duplicate effect"], ["disable capability", "owned exception"], C.orange],
    [805, "MEDIUM", ["contained", "failure"], ["threshold by", "task slice"], C.lilac],
    [1180, "LOW", ["presentation", "defect"], ["product-quality", "threshold"], C.mint],
  ];
  tiers.forEach(([x, label, example, action, accent]) => {
    s += rect(x, 200, 335, 260, C.white, accent, 28, 3);
    s += pill(x + 22, 220, 150, label, accent, accent === C.red || accent === C.orange ? C.white : C.secondary);
    s += lines(x + 26, 304, example, "heading", 36);
    s += lines(x + 26, example.length === 1 ? 370 : 400, action, "small", 34);
  });
  s += rect(120, 535, 1360, 180, C.ink, C.ink, 30, 0); s += text(800, 590, "SAFE TASK SUCCESS", "label", "middle", C.white); s += text(800, 645, "correct result  AND  acceptable path  AND  policy compliance", "body", "middle", C.white); s += text(800, 690, "AND  verified effect  AND  budget adherence", "body", "middle", C.white);
  save("fig-ch23-04-severity-and-safe-task-success.svg", s + footer("Report rescue, rejection, recovery, duplicates, cost, and time—not completion alone."));
}

// Chapter 24 — unavailable controls fail closed.
{
  let s = base("A missing control-plane dependency must reduce authority", "Consequential execution is available only when every required control is current and reachable.", "Hub-and-spoke failure map connecting execution to identity, policy, approval, credential, sandbox, and audit services, each routing loss to stop, read-only mode, or manual review.");
  const deps = [[60, 205, 390, "IDENTITY", "offline → stop"], [60, 520, 390, "POLICY", "stale → stop"], [540, 160, 520, "AUDIT", "backpressure → stop"], [540, 610, 520, "APPROVAL", "store down → queue"], [1150, 205, 390, "CREDENTIAL", "down → no write"], [1150, 520, 390, "SANDBOX", "degraded → inspect"]];
  const hub = [580, 350, 440, 220];
  deps.forEach(([x, y, w]) => { const cx = x + w / 2, cy = y + 85; s += `<path d="M${cx} ${cy} L800 460" fill="none" stroke="${C.purple}" stroke-width="4" stroke-dasharray="12 10"/>`; });
  s += card({ x: hub[0], y: hub[1], w: hub[2], h: hub[3], label: "CONSEQUENTIAL EXECUTION", heading: "All controls current", body: ["exact action + target", "narrow grant + receipt"], accent: C.ink, fill: C.ink, dark: true });
  deps.forEach(([x, y, w, label, rule], i) => { s += card({ x, y, w, h: 170, label, heading: rule, body: ["monitor + alert"], accent: i % 2 ? C.red : C.orange }); });
  save("fig-ch24-03-control-plane-fail-closed.svg", s + footer("Lost enforcement never routes around the control; it routes to less authority or no action."));
}

// Chapter 24 — supply-chain inventory.
{
  let s = base("Inventory the whole agentic supply chain", "Packages are one row; prompts, models, tools, skills, servers, indexes, policies, and evaluators also execute trust.", "Supply-chain inventory grouping eight asset families and the metadata required before promotion or change.");
  const groups = [["MODEL INPUTS", ["prompts", "models"]], ["CAPABILITY", ["tools", "skills"]], ["INTEGRATION", ["MCP servers", "indexes"]], ["CONTROL", ["policies", "evaluators"]]];
  groups.forEach(([label, body], i) => { const x = 70 + i * 380; s += card({ x, y: 205, w: 340, h: 240, label, heading: body[0], body: [body[1], "owner + provenance"], accent: i % 2 ? C.mint : C.lilac }); });
  s += rect(90, 485, 1420, 285, C.white, C.border, 28, 2); s += pill(120, 505, 300, "PROMOTION RECORD", C.ink, C.white);
  const meta = [
    ["SOURCE", "immutable source + digest"],
    ["OWNERSHIP", "publisher + review owner"],
    ["REACH", "capability + data classes"],
    ["PROVENANCE", "signature + origin"],
    ["LIFECYCLE", "install · update · rollback · revoke"],
    ["EVALUATION", "post-change regression suite"],
  ];
  meta.forEach(([label, value], i) => {
    const col = i % 3, row = Math.floor(i / 3), x = 120 + col * 465, y = 570 + row * 92;
    s += rect(x, y, 430, 76, C.pale, C.border, 14, 1);
    s += text(x + 18, y + 28, `□ ${label}`, "label", "start", C.secondary);
    s += `<text x="${x + 18}" y="${y + 58}" style="font-family:Inter,Arial,sans-serif;font-size:22px;font-weight:500;fill:${C.ink}">${value}</text>`;
  });
  save("fig-ch24-04-agentic-supply-chain-inventory.svg", s + footer("Procedural input may request a tool. It cannot grant itself permission to use one."));
}

// Chapter 24 — incident runbook.
{
  let s = base("Contain, preserve, reconcile, and regress", "An agent-security incident needs an order of operations with an evidence product at every phase.", "Four-phase incident runbook from detection and scheduling stop through revocation and isolation, evidence preservation and effect reconciliation, trusted rebuild, regression, and monitoring.");
  const phases = [
    { label: "PHASE 1", heading: ["Detect + stop"], body: ["stop scheduling", "freeze risky capability"], accent: C.red },
    { label: "PHASE 2", heading: ["Revoke +", "isolate"], body: ["credentials · workers", "tool / asset block"], accent: C.orange },
    { label: "PHASE 3", heading: ["Preserve +", "scope"], body: ["hashes · receipts", "tenants · targets"], accent: C.lilac },
    { label: "PHASE 4", heading: ["Reconcile +", "rebuild"], body: ["effect count", "trusted image + policy"], accent: C.mint },
    { label: "PERMANENT", heading: ["Regress +", "monitor"], body: ["minimized fixture", "release gate + slice"], accent: C.lilac },
  ];
  const x0 = 55, y = 220, w = 270, h = 410, gap = 35;
  phases.forEach((phase, i) => {
    const x = x0 + i * (w + gap);
    s += rect(x, y, w, h, C.white, phase.accent, 24, 3);
    s += pill(x + 24, y + 22, 142, phase.label, phase.accent, phase.accent === C.red || phase.accent === C.orange ? C.white : C.secondary);
    s += lines(x + 24, y + 112, phase.heading, "heading", 38);
    const bodyY = y + (phase.heading.length === 1 ? 184 : 220);
    s += lines(x + 24, bodyY, phase.body, "small", 38);
    if (i < phases.length - 1) {
      const nextX = x0 + (i + 1) * (w + gap);
      s += arrow(x + w + 4, y + 205, nextX - 10, y + 205, C.purple, false);
    }
  });
  save("fig-ch24-05-agent-security-incident-runbook.svg", s + footer("The invariant is the authoritative effect count and receipt—not the last assistant message."));
}

// Chapter 25 — one deadline.
{
  let s = base("Allocate one user deadline exactly once", "Every downstream call receives remaining time—not a fresh timeout.", "Horizontal journey deadline partitioned into acceptance, queue, model, tool and retry, human wait, verification, and terminal-state reserve, contrasted with stacked fresh timeouts.");
  const parts = [["ACK", 100, C.lilac], ["QUEUE", 150, C.mint], ["MODEL", 200, C.lilac], ["TOOL + RETRY", 330, C.orange], ["HUMAN WAIT", 230, C.pale], ["VERIFY", 190, C.mint], ["RECEIPT RESERVE", 200, C.ink]];
  let x = 70; parts.forEach(([label, w, fill]) => { s += rect(x, 260, w, 145, fill, fill === C.ink ? C.ink : C.border, 8, 1); s += text(x + w / 2, 330, label, "label", "middle", fill === C.ink ? C.white : C.secondary); x += w; });
  s += arrow(70, 455, 1530, 455, C.purple, false, "remaining budget moves forward");
  s += rect(150, 555, 1300, 130, C.redSoft, C.red, 26, 2); s += text(800, 605, "ANTI-PATTERN", "label", "middle", C.red); s += text(800, 650, "gateway timeout + queue timeout + model timeout + tool timeout = journey overrun", "body", "middle");
  save("fig-ch25-05-one-deadline-budget.svg", s + footer("Reserve time to persist a truthful terminal state even when useful work must stop."));
}

// Chapter 25 — degraded modes.
{
  let s = base("Design the lower-authority product before the outage", "A degraded mode states what remains, what is stale, which effects did not run, and how work resumes.", "Four dependency cards map provider, fresh data, write service, and enforcement failure to safe reduced-authority behavior.");
  const modes = [
    [70, "MODEL / PROVIDER", "Use cached artifact", ["label age + source", "disable fresh claims"], C.lilac],
    [455, "FRESH DATA", "Read cached snapshot", ["mark stale / unverified", "no automatic publish"], C.orange],
    [840, "WRITE SERVICE", "Draft only", ["queue or stop effects", "show no receipt"], C.mint],
    [1225, "ENFORCEMENT", "Stop authority", ["inspect-only if safe", "never bypass control"], C.red],
  ];
  modes.forEach(([x, label, heading, body, accent]) => s += card({ x, y: 225, w: 320, h: 410, label, heading, body, accent }));
  s += text(800, 730, "Resume automatically only when the control contract explicitly permits it.", "body", "middle");
  save("fig-ch25-06-degraded-mode-matrix.svg", s + footer("The correct response to lost authorization, audit, sandbox, or credentials is less authority."));
}

// Chapter 26 — task envelope.
{
  let s = base("A cross-level handoff is a signed task envelope", "Send the minimum contract. Reauthorize at the receiving boundary.", "Annotated task envelope grouping identity, scope and capabilities, artifact integrity, time and budget, policy and evidence, and callback authenticity, contrasted with ambient delegation.");
  s += rect(160, 190, 1000, 500, C.white, C.lilac, 32, 3); s += pill(195, 220, 310, "CANONICAL ENVELOPE", C.ink, C.white);
  const fields = [[215, 330, "IDENTITY", "task · requester · delegator"], [675, 330, "SCOPE", "tenant · resource · workspace"], [215, 430, "CAPABILITY", "allow · deny · output contract"], [675, 430, "INTEGRITY", "input hashes · schema version"], [215, 530, "TIME + BUDGET", "deadline · nonce · expiry"], [675, 530, "EVIDENCE", "terminal states · required proof"], [445, 630, "CALLBACK", "receiver identity + signature"]];
  fields.forEach(([x, y, label, value]) => { s += text(x, y, label, "label"); s += text(x, y + 38, value, "small"); });
  s += card({ x: 1220, y: 250, w: 310, h: 360, label: "DENIED", heading: "Ambient handoff", body: ["entire transcript", "shared credentials", "“handle it”", "no expiry or proof"], accent: C.red });
  s += arrow(1160, 440, 1215, 440, C.red, true, "reject");
  save("fig-ch26-04-cross-level-task-envelope.svg", s + footer("Delegation preserves requester, scope, budget, expiry, evidence, and receiver authentication."));
}

// Chapter 26 — upgrade and downshift lifecycle.
{
  let s = base("Agency can move up—and should move down", "Add authority for a real environmental or organizational requirement; remove it when trajectories stabilize.", "Bidirectional lifecycle from instrumenting a current path through isolating higher authority and measuring trajectories to converting stable branches into deterministic nodes and narrower tools.");
  const top = [[55, "INSTRUMENT", "current path"], [360, "UPGRADE", "real trigger"], [665, "ISOLATE", "higher authority"], [970, "MEASURE", "trajectories"], [1275, "STABLE", "stable branch"]];
  top.forEach(([x, label, heading], i) => { s += card({ x, y: 220, w: 260, h: 190, label, heading, body: [], accent: C.orange }); if (i < top.length - 1) s += arrow(x + 260, 315, top[i + 1][0] - 5, 315); });
  const bottom = [[970, "DOWNSHIFT", "deterministic node"], [665, "NARROW", "tool + context"], [360, "VERIFY", "lower cost + risk"]];
  bottom.forEach(([x, label, heading], i) => { s += card({ x, y: 535, w: 260, h: 190, label, heading, body: [], accent: C.mint }); if (i < bottom.length - 1) s += arrow(x, 630, bottom[i + 1][0] + 265, 630); });
  s += arrow(1405, 410, 1100, 535, C.purple, false, "stable");
  s += arrow(360, 630, 185, 415, C.purple, false, "repeat");
  save("fig-ch26-05-upgrade-downshift-lifecycle.svg", s + footer("Downshifting reduces authority, variance, latency, cost, and evaluation surface."));
}

// Back matter — consolidated knobs.
{
  let s = base("The twelve knob families", "Every increase needs an owner, enforcement point, evidence, and rollback path.", "Indexed reference grid covering model, runtime, context, tools, skills, memory, permissions, human control, evaluation, observability, deployment, and cost.");
  const knobs = ["MODEL", "RUNTIME", "CONTEXT", "TOOLS", "SKILLS", "MEMORY", "PERMISSIONS", "HUMAN CONTROL", "EVALUATION", "OBSERVABILITY", "DEPLOYMENT", "COST"];
  knobs.forEach((k, i) => {
    const col = i % 4, row = Math.floor(i / 4), x = 55 + col * 385, y = 170 + row * 195;
    const accent = i % 3 === 0 ? C.lilac : i % 3 === 1 ? C.mint : C.orange;
    s += rect(x, y, 350, 180, C.white, accent, 22, 3);
    s += pill(x + 20, y + 16, 92, `${String(i + 1).padStart(2, "0")}`, accent, C.secondary);
    s += text(x + 22, y + 96, k, "heading");
    s += lines(x + 22, y + 133, ["default → change", "risk → evidence"], "small", 30);
  });
  save("fig-ch27-03-consolidated-knobs-reference.svg", s + footer("A knob without an enforced ceiling is ambient authority disguised as configuration."));
}

// Back matter — evidence-bearing quickstart.
flow("fig-ch27-04-evidence-bearing-quickstart.svg", "Build the first vertical slice in five milestones", "Each milestone ends with a visible artifact and a release gate—not merely another integration.", "Five-milestone quickstart from UI and typed state through read tools and semantic artifacts, governed writes and interrupts, durability and recovery, and evaluation and operations.", [
  { label: "MILESTONE 1", heading: "Surface + state", body: ["UI shell", "typed task contract"] },
  { label: "MILESTONE 2", heading: "Read + render", body: ["one read tool", "semantic artifact"] },
  { label: "MILESTONE 3", heading: "Write + review", body: ["trusted mutation", "bound interrupt"] , accent: C.orange},
  { label: "MILESTONE 4", heading: "Resume + recover", body: ["checkpoint", "one failure path"] },
  { label: "MILESTONE 5", heading: "Evaluate + operate", body: ["trace + ledger", "20-case suite"] , accent: C.mint},
], "Only after the Level 1 slice is proven should you add a bounded machine worker or organizational front door.");

console.log("Generated 20 final deterministic editorial SVGs.");

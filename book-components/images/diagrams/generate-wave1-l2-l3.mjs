import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const out = dirname(fileURLToPath(import.meta.url));
const C = {
  bg: "#FAFAFC", ink: "#11143D", text: "#010507", secondary: "#57575B",
  border: "#DBDBE5", lilac: "#BEC2FF", lilacSoft: "#EEE6FE",
  mint: "#85ECCE", mintSoft: "#E7FBF5", red: "#FA5F67", orange: "#FFAC4D",
  white: "#FFFFFF", pale: "#EDEDF5", purple: "#6857D9",
};

const esc = (s) => String(s).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
const tspans = (lines, x, y, cls = "body", gap = 28, anchor = "start") =>
  `<text x="${x}" y="${y}" class="${cls}" text-anchor="${anchor}">${lines.map((line, i) => `<tspan x="${x}" dy="${i ? gap : 0}">${esc(line)}</tspan>`).join("")}</text>`;
const rect = (x, y, w, h, fill = C.white, stroke = C.border, rx = 26, sw = 2, extra = "") =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" ${extra}/>`;
const pill = (x, y, w, label, fill = C.pale, color = C.secondary) =>
  `${rect(x, y, w, 36, fill, fill, 18, 1)}<text x="${x + w / 2}" y="${y + 25}" class="label" text-anchor="middle" style="fill:${color}">${esc(label)}</text>`;
const arrow = (x1, y1, x2, y2, color = C.purple, dashed = false, label = "") =>
  `<path d="M${x1} ${y1} L${x2} ${y2}" fill="none" stroke="${color}" stroke-width="4" ${dashed ? 'stroke-dasharray="10 8"' : ""} marker-end="url(#arrow-${color.slice(1)})"/>${label ? `<text x="${(x1+x2)/2}" y="${(y1+y2)/2-10}" class="small" text-anchor="middle">${esc(label)}</text>` : ""}`;
const card = ({x,y,w,h,label,heading,lines=[],accent=C.lilac,fill=C.white,dark=false}) => {
  const fg = dark ? C.white : C.ink;
  const headingLines = Array.isArray(heading) ? heading : [heading];
  const bodyY = y + 128 + (headingLines.length - 1) * 28;
  return `${rect(x,y,w,h,fill,accent,28,dark?0:2)}${pill(x+22,y+20,Math.min(w-44, Math.max(110,label.length*10+30)),label,accent,dark?C.ink:C.secondary)}
  ${tspans(headingLines,x+24,y+92,"heading",28,"start").replace('class="heading"',`class="heading" style="fill:${fg}"`)}
  ${tspans(lines,x+24,bodyY,"small",26,"start").replace('class="small"',`class="small" style="fill:${dark?C.white:C.secondary}"`)}`;
};
const header = (title, subtitle, desc) => `<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">
<title id="title">${esc(title)}</title><desc id="desc">${esc(desc)}</desc><defs>
${[C.purple,C.mint,C.red,C.ink].map(color=>`<marker id="arrow-${color.slice(1)}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M0 0L10 5L0 10Z" fill="${color}"/></marker>`).join("")}
<style>.title{font:700 50px 'Plus Jakarta Sans',Arial,sans-serif;fill:${C.ink}}.subtitle{font:400 23px 'Plus Jakarta Sans',Arial,sans-serif;fill:${C.secondary}}.heading{font:700 25px 'Plus Jakarta Sans',Arial,sans-serif;fill:${C.ink}}.body{font:500 20px 'Plus Jakarta Sans',Arial,sans-serif;fill:${C.ink}}.small{font:400 17px 'Plus Jakarta Sans',Arial,sans-serif;fill:${C.secondary}}.label{font:700 14px 'Spline Sans Mono',monospace;letter-spacing:1px;fill:${C.secondary}}</style></defs>
<rect width="1600" height="900" fill="${C.bg}"/><text x="80" y="82" class="title">${esc(title)}</text><text x="80" y="122" class="subtitle">${esc(subtitle)}</text>`;
const finish = (footer) => `${rect(260,790,1080,72,C.ink,C.ink,24,0)}<text x="800" y="835" class="body" text-anchor="middle" style="fill:${C.white}">${esc(footer)}</text></svg>`;
const save = (name, body) => writeFileSync(join(out,name), body);

function flow(name, title, subtitle, desc, nodes, footer, opts={}) {
  const gap = 28, x0 = 70, y = opts.y ?? 270, h = opts.h ?? 300;
  const w = (1460 - gap*(nodes.length-1))/nodes.length;
  let s = header(title,subtitle,desc);
  nodes.forEach((n,i)=>{
    const x=x0+i*(w+gap);
    s += card({x,y,w,h,label:n.label,heading:n.heading,lines:n.lines,accent:n.accent??(i%2?C.mint:C.lilac),fill:n.fill??C.white,dark:n.dark});
    if(i<nodes.length-1) s += arrow(x+w,y+h/2,x+w+gap-4,y+h/2,n.arrowColor??C.purple,n.dashed,n.edge??"");
  });
  s += finish(footer); save(name,s);
}

// Chapter 11: attack path.
flow("fig-ch11-02-repository-exfiltration.svg","Context stayed in scope. Process authority did not.","A repository instruction becomes an exfiltration route when shell, credentials, and egress share one ambient boundary.","Six-step attack path from an untrusted repository note through an allowed shell and inherited credential to an approved host.",[
  {label:"UNTRUSTED INPUT",heading:"Migration note",lines:["Requests diagnostics","inside the repository"],accent:C.orange},
  {label:"MODEL CONTEXT",heading:"Instruction selected",lines:["Looks relevant","does not grant authority"]},
  {label:"ALLOWED TOOL",heading:"Shell starts",lines:["Same OS user","broad process reach"],accent:C.lilac},
  {label:"AMBIENT IDENTITY",heading:"Token inherited",lines:["No action lease","secret enters process"],accent:C.red},
  {label:"SIDE EFFECT",heading:"Bundle created",lines:["Token appears","in diagnostic output"],accent:C.red},
  {label:"ALLOWED EGRESS",heading:"Support host",lines:["Host is allowlisted","payload is not safe"],accent:C.red},
],"A working directory narrows context. Only enforced process, identity, and egress boundaries narrow authority.",{h:290});

// Chapter 11: ten-part harness.
{
  const title="A machine agent is a ten-part harness";
  let s=header(title,"The model supplies adaptive judgment inside a system that owns authority, evidence, and recovery.","Ten connected harness components from run intake and context assembly through execution, persistence, observability, verification, and recovery.");
  const items=[
    ["01","Run intake",["identity · workspace","policy · budget"]],["02","Context assembly",["instructions · memory","retrieved evidence"]],["03","Model adapter",["provider · stream","structured proposals"]],["04","Control loop",["act · ask · retry","delegate · stop"]],["05","Capability registry",["files · shell · browser","CLI · MCP · services"]],
    ["10",["Verification +","recovery"],["postconditions · evidence","discard · revert · compensate"]],["09","Interaction + evidence",["plan · approval · diff","denial · cost · result"]],["08","Persistence",["checkpoint · worktree","artifact · operation ID"]],["07","Execution broker",["identity · sandbox","lease · network · budget"]],["06","Policy + approval",["allow · deny · narrow","pause · bind grant"]],
  ];
  items.forEach((it,i)=>{const row=i<5?0:1,col=i<5?i:i-5,x=55+col*308,y=190+row*265;s+=card({x,y,w:270,h:205,label:it[0],heading:it[1],lines:it[2],accent:i===2?C.lilac:i===7?C.red:(i%2?C.mint:C.lilac)});});
  for(let i=0;i<4;i++) s+=arrow(325+i*308,292,347+i*308,292);
  for(let i=5;i<9;i++) s+=arrow(325+(i-5)*308,557,347+(i-5)*308,557,C.purple,false);
  // The row transition arrows own narrow vertical rails. Their labels sit in
  // separate gutter badges with at least 25 px horizontal clearance.
  s+=arrow(1440,395,1440,455,C.purple,false);
  s+=pill(1270,407,145,"EFFECT BOUNDARY",C.lilacSoft,C.secondary);
  s+=arrow(160,455,160,395,C.mint,false);
  s+=pill(185,407,140,"EVIDENCE LOOP",C.mintSoft,C.secondary);
  s+=finish("The harness—not the model—decides what enters, what can execute, what proves success, and what survives failure."); save("fig-ch11-03-ten-part-harness.svg",s);
}

// Chapter 11: ledger request swimlane.
{
  const title="One ledger request crosses six ownership boundaries";
  let s=header(title,"The user experiences one task. The system changes identities, capabilities, and enforcement profiles.","Swimlane sequence for a ledger category-budget change from request through registry, read-only planning, install approval, isolated mutation, deterministic verification, and review.");
  const lanes=["CopilotKit + user","Run registry","Model + context","Policy + approval","Isolated worker","Verifier + artifacts"];
  lanes.forEach((l,i)=>{const y=180+i*88;s+=rect(50,y,1500,72,i%2?C.white:C.pale,C.border,18,1);s+=pill(68,y+18,205,l,i===3?C.mint:i===4?C.lilac:C.white);});
  const events=[[0,250,"Goal + scope"],[1,430,"Resolve abc123"],[2,625,"Read-only plan"],[3,820,"Approve install"],[4,1035,"Patch worktree"],[5,1240,"Checks + digest"],[0,1430,"Review / discard"]];
  events.forEach(([lane,x,label],i)=>{const y=216+lane*88;s+=`<circle cx="${x}" cy="${y}" r="15" fill="${i===3?C.mint:i===4?C.lilac:C.ink}"/>`;s+=`<text x="${x}" y="${y-24}" class="small" text-anchor="middle">${esc(label)}</text>`;if(i<events.length-1)s+=arrow(x+16,y,events[i+1][1]-18,216+events[i+1][0]*88,C.purple,false);});
  s+=finish("A pull request is a new external-write intent—not an automatic consequence of a verified local patch."); save("fig-ch11-04-ledger-request-boundaries.svg",s);
}

// Chapter 12: same model, different harness.
{
  let s=header("Same model. Different product.","Repeatability comes from the harness around probabilistic judgment.","Split comparison showing identical models and tasks under an ambient permissive harness and a pinned governed harness.");
  s+=card({x:70,y:190,w:700,h:520,label:"AMBIENT HARNESS",heading:"Looks fast. Cannot be reproduced.",lines:["Vague goal · mutable base","Always-on terminal","Policy mixed into instructions","Self-updating skills","Model decides whether tests are enough","Unknown effect and recovery state"],accent:C.red,fill:C.white});
  s+=card({x:830,y:190,w:700,h:520,label:"GOVERNED HARNESS",heading:"Bounded enough to operate.",lines:["Acceptance criteria · immutable base","Provenance on context","Pinned and reviewed skills","Capabilities change by phase","Typed intent + bound approval","Independent verifier + receipts"],accent:C.mint,fill:C.white});
  s+=`<circle cx="800" cy="390" r="58" fill="${C.ink}"/><text x="800" y="384" class="label" text-anchor="middle" style="fill:${C.white}">SAME</text><text x="800" y="410" class="label" text-anchor="middle" style="fill:${C.white}">MODEL</text>`;
  s+=finish("The model proposes. The harness supplies memory, capability, restraint, proof, and recovery."); save("fig-ch12-01-same-model-different-harness.svg",s);
}

flow("fig-ch12-02-skill-promotion-pipeline.svg","Treat skills like executable supply-chain artifacts","Discovery, review, promotion, use, and revocation are separate authority phases.","Eight-step pipeline for promoting an agent skill from discovery through integrity verification, capability inventory, disposable testing, ownership, registry publication, and controlled runtime resolution.",[
  {label:"01 DISCOVER",heading:"Candidate",lines:["source + license","never auto-run"],accent:C.orange},
  {label:"02 PIN",heading:"Integrity",lines:["commit · digest","immutable input"]},
  {label:"03 INSPECT",heading:"Contents",lines:["scripts · hooks","deps · tools"]},
  {label:"04 TEST",heading:"Disposable run",lines:["static checks","adversarial fixtures"],accent:C.red},
  {label:"05 PROMOTE",heading:"Registry",lines:["owner · expiry","approved capability"],accent:C.mint},
  {label:"06 RESOLVE",heading:"Runtime use",lines:["ID + version","policy-bound"],accent:C.lilac},
],"A privileged persistent agent must never search, install, and execute an unreviewed skill in one step.",{h:300});

// Chapter 12: capability staircase.
{
  let s=header("Capabilities change by trusted phase","Retrieved content cannot promote itself into a more powerful execution profile.","Four-phase capability staircase for research, proposal, approved mutation, and verification, with tools, credentials, writes, and network constraints at each phase.");
  const phases=[
    {x:80,y:540,w:330,h:180,label:"01 RESEARCH",head:"Read evidence",lines:["tools: repo read + web GET","credentials: none","writes: none","network: allowlisted docs"]},
    {x:430,y:430,w:330,h:290,label:"02 PROPOSAL",head:"Build intent",lines:["tools: semantic diff","credentials: none","writes: task state only","network: none"]},
    {x:780,y:300,w:350,h:420,label:"03 APPROVED MUTATION",head:"Change candidate",lines:["tools: install + patch broker","credential: one-use lease","writes: scoped worktree","network: pinned registry"]},
    {x:1150,y:190,w:370,h:530,label:"04 VERIFICATION",head:"Prove outcome",lines:["tools: fixed check pipeline","credentials: none","writes: verifier artifacts","network: off by default"]},
  ];
  phases.forEach((p,i)=>{s+=card({x:p.x,y:p.y,w:p.w,h:p.h,label:p.label,heading:p.head,lines:p.lines,accent:i===2?C.mint:C.lilac});});
  s+=arrow(240,250,850,250,C.red,true,"injected document cannot skip phases");
  s+=`<path d="M850 250L825 235L825 265Z" fill="${C.red}"/><text x="545" y="215" class="small" text-anchor="middle">Trusted runtime state and policy move the run forward.</text>`;
  s+=finish("The model can request a phase change. It cannot grant the capability set to itself."); save("fig-ch12-03-phase-capability-staircase.svg",s);
}

// Chapter 13: combined-control attack tree.
{
  let s=header("Least privilege is the intersection—not the sum—of controls","Every individual rule can say “allowed” while the combined route still leaks data.","Attack tree showing how an outward symlink, an unconstrained terminal, ambient data, and an allowlisted GET host combine into exfiltration, alongside independent controls that break the route.");
  s+=card({x:70,y:190,w:300,h:500,label:"OBJECTIVE",heading:"Exfiltrate outside file",lines:["docs/vendor → symlink","terminal reads target","content enters query","GET reaches allowed host"],accent:C.red});
  const attacks=["Path allowlist","Read-only classification","GET-only egress","No write tool"];
  attacks.forEach((a,i)=>{
    const y=190+i*125, portY=y+55;
    s+=rect(430,y,360,110,C.white,C.red,24,2);
    s+=pill(448,y+12,92,`CHECK ${i+1}`,C.red,C.secondary);
    s+=`<text x="454" y="${y+78}" class="body">${esc(a)}</text>`;
    s+=pill(610,y+12,158,"REPORTS SUCCESS","#FFF0F1",C.secondary);
    s+=`<circle cx="370" cy="${portY}" r="6" fill="${C.red}"/>`;
    s+=arrow(382,portY,418,portY,C.red,true);
  });
  s+=card({x:860,y:190,w:670,h:500,label:"INDEPENDENT REPAIRS",heading:"Break the route at several boundaries",lines:["1  Mount does not expose outside directory","2  Path broker rejects resolved symlink","3  Terminal shares filesystem containment","4  Worker starts without ambient tokens","5  Fetch service limits path, query, and credentials","6  Sensitive reads and egress cannot coexist by default","7  Canary telemetry observes read and outbound paths"],accent:C.mint,fill:C.mintSoft});
  s+=finish("Two checks in the same process and identity are not independent enforcement points."); save("fig-ch13-02-combined-control-exfiltration.svg",s);
}

// Chapter 14: operating models.
{
  let s=header("Choose the operating model, not the logo","Overlap in file and command access hides different lifecycles, trust boundaries, and ownership.","Three equal non-ranking cards compare a managed coding workflow, an open provider-flexible harness, and a persistent gateway workspace.");
  const cards=[
    {x:70,label:"MANAGED CODING WORKFLOW",heading:"Claude Code",lines:["Lifecycle: terminal + IDE","Model posture: Claude product","Persistence: sessions + worktrees","Extension: hooks · MCP · subagents","Team still owns: identity · network","secrets · verification"]},
    {x:545,label:"OPEN COMPOSABLE HARNESS",heading:"Hermes Agent",lines:["Lifecycle: CLI + custom runtime","Model posture: provider flexible","Persistence: sessions + optional checkpoints","Extension: tools · skills · MCP · backends","Team still owns: deployment · isolation","policy · adapter"]},
    {x:1020,label:"PERSISTENT GATEWAY",heading:"OpenClaw",lines:["Lifecycle: long-lived gateway","Model posture: configurable","Persistence: workspace + sessions + memory","Extension: channels · nodes · browser · tools","Team still owns: dedicated identity","state · egress · tenancy"]},
  ];
  cards.forEach((c,i)=>s+=card({x:c.x,y:190,w:410,h:500,label:c.label,heading:c.heading,lines:c.lines,accent:i===0?C.lilac:i===1?C.mint:C.orange}));
  s+=finish("This is a dated shape comparison—not a benchmark, security score, or universal ranking."); save("fig-ch14-01-machine-harness-operating-models.svg",s);
}

// Chapter 15: topology with absent runtime.
flow("fig-ch15-01-source-present-topology.svg","What the Hermes–CopilotKit source proves","Solid edges are tracked in the pinned repository. Dashed edges cross into the absent external runtime.","Architecture flow from CopilotKit React UI through Next.js and the Hermes AG-UI client to an absent external adapter and Hermes loop, returning events to cards, diffs, and a PDF renderer.",[
  {label:"SOURCE-PRESENT",heading:"CopilotKit UI",lines:["shared ledger context","cards · diff · PDF"]},
  {label:"SOURCE-PRESENT",heading:"Next.js route",lines:["registered default agent","AGENT_URL client"]},
  {label:"SOURCE-PRESENT",heading:"@ag-ui/hermes",lines:["protocol client","not the worker"]},
  {label:"ABSENT",heading:"External adapter",lines:["fork not pinned","runtime unavailable"],accent:C.red,dashed:true},
  {label:"ABSENT",heading:"Hermes loop",lines:["model + tools","machine operations"],accent:C.red},
],"The repository proves an inspectable UI/protocol seam. It does not prove an end-to-end machine run.",{h:310});

// Chapter 15: readiness staircase.
{
  let s=header("Readiness is a chain of different claims","Each stage requires new evidence; no label silently inherits the meaning of the next.","Six-stage staircase from registered through reachable, authenticated, authorized, contained, and verified, with the evidence required at each transition.");
  const stages=[
    ["01","Registered",["registry entry","source/config","evidence"]],
    ["02","Reachable",["bounded health","call succeeds","runtime evidence"]],
    ["03","Authenticated",["caller identity","verified","denial evidence"]],
    ["04","Authorized",["canonical action","allowed","grant evidence"]],
    ["05","Contained",["process stays","inside scope","proxy denial"]],
    ["06","Verified",["postconditions","actually pass","verifier artifacts"]],
  ];
  stages.forEach((st,i)=>{const x=70+i*248,y=570-i*70,h=190+i*70;s+=card({x,y,w:220,h,label:st[0],heading:st[1],lines:st[2],accent:i<2?C.lilac:i<4?C.mint:C.orange});});
  s+=finish("Configured-ready and HTTP-reachable are useful facts. Neither means ready to execute safely."); save("fig-ch15-02-readiness-staircase.svg",s);
}

// Chapter 15: supervision broker.
{
  let s=header("The supervision broker owns the authority chain","CopilotKit projects durable run state; trusted services authenticate, decide, execute, and verify.","Swimlane sequence linking CopilotKit, authenticated gateway, policy and approval, isolated worker broker, verifier and artifact store, target system, and an action ledger with identity badges.");
  const lanes=["CopilotKit UI","Auth gateway","Policy + approval","Worker broker","Verifier + artifacts","Target + ledger"];
  lanes.forEach((l,i)=>{const x=50+i*258;s+=rect(x,180,230,520,i%2?C.white:C.pale,C.border,22,1);s+=pill(x+18,192,194,l,i===2?C.mint:i===3?C.lilac:C.white);});
  const steps=[
    [0,300,"GUI + session"],[1,380,"resolve run/workspace"],[2,460,"canonical intent + grant"],[3,540,"isolated attempt + lease"],[4,620,"checks + artifacts"],[5,690,"receipt + audit"],
  ];
  steps.forEach(([lane,y,label],i)=>{const x=165+lane*258;s+=rect(x-104,y-56,208,32,C.white,C.border,12,1);s+=`<text x="${x}" y="${y-34}" class="label" text-anchor="middle">${esc(label)}</text><circle cx="${x}" cy="${y}" r="13" fill="${i===2?C.mint:i===3?C.lilac:C.ink}"/>`;if(i<steps.length-1)s+=arrow(x+14,y,165+(lane+1)*258-14,steps[i+1][1],C.purple);});
  s+=finish("Visibility requests control. Only the broker’s trusted path grants and spends machine authority."); save("fig-ch15-03-supervision-broker.svg",s);
}

// Chapter 15: six-state wireframe.
{
  let s=header("Design the supervision surface by durable state","One task changes what the user must know and what controls are safe to offer.","Six schematic CopilotKit panels for planning, intent proposed, waiting for approval, executing, verifying, and review or terminal states.");
  const states=[
    ["01 PLANNING","Scope before authority",["repo: ledger · base abc123","budget: 12 min · read-only","[ Narrow scope ]"]],
    ["02 INTENT PROPOSED","Canonical action",["npm install chart-helper@2.1","network: pinned registry","policy: review required"]],
    ["03 WAITING","Bound approval",["digest: 91b… · expires 14:32","eligible: repository maintainer","[ Approve ]  [ Reject ]"]],
    ["04 EXECUTING","Broker evidence",["attempt 02 · heartbeat 8s","tool: package broker","cancel scope: current tool"]],
    ["05 VERIFYING","Independent checks",["lint ✓ · tests running","network assertion ✓","artifact digest pending"]],
    ["06 REVIEW","Effect + recovery",["content-addressed diff","target receipts + known effects","[ Discard ]  [ Merge ]"]],
  ];
  states.forEach((st,i)=>{const col=i%3,row=Math.floor(i/3),x=55+col*515,y=175+row*285;s+=card({x,y,w:480,h:245,label:st[0],heading:st[1],lines:st[2],accent:i===2?C.mint:i===3?C.orange:C.lilac,fill:C.white});});
  s+=finish("Historical controls are read-only unless the server confirms a current pending decision."); save("fig-ch15-04-supervision-states.svg",s);
}

// Chapter 16: failure timeline.
{
  let s=header("One logical run can have several process attempts","Leases, fencing, idempotency, and reconciliation—not model memory—settle failure.","Timeline where a browser disconnects, worker A completes a package script, the gateway restarts, the lease expires, worker B claims the run, and worker A's late state write is rejected by fencing.");
  const lanes=["Browser","Gateway","Queue + lease","Worker A","Worker B","Target filesystem"];
  lanes.forEach((l,i)=>{const y=185+i*85;s+=`<text x="70" y="${y+6}" class="label">${esc(l)}</text><line x1="240" y1="${y}" x2="1515" y2="${y}" stroke="${C.border}" stroke-width="2"/>`;});
  const ev=[[0,320,"disconnect",C.red],[3,480,"script commits",C.orange],[1,620,"restart",C.red],[2,780,"lease expires",C.red],[4,950,"claim token 2",C.mint],[3,1130,"late write token 1",C.red],[2,1320,"reject stale fence",C.ink],[5,1450,"reconcile receipt",C.mint]];
  ev.forEach(([lane,x,label,color],i)=>{const y=185+lane*85;s+=`<circle cx="${x}" cy="${y}" r="13" fill="${color}"/><text x="${x}" y="${y-18}" class="small" text-anchor="middle">${esc(label)}</text>`;if(i<ev.length-1)s+=arrow(x+14,y,ev[i+1][1]-14,185+ev[i+1][0]*85,C.purple,true);});
  s+=finish("Run ID stays stable. Attempt IDs, fencing tokens, and operation receipts tell operators what actually repeated."); save("fig-ch16-01-duplicate-delivery-timeline.svg",s);
}

// Chapter 16: state machine.
{
  let s=header("A durable run cannot jump over evidence","The connection can disappear. State guards remain server-side.","State machine for queued, planning, waiting for approval, executing, verifying, review, and evidence-specific terminal outcomes, with grant, receipt, and verifier guards.");
  const nodes=[
    {x:60,y:260,w:190,h:110,label:"STATE",heading:"Queued",lines:["lease required"]},
    {x:290,y:260,w:190,h:110,label:"STATE",heading:"Planning",lines:["scope fixed"]},
    {x:520,y:260,w:220,h:110,label:"STATE",heading:"Waiting",lines:["live grant required"],accent:C.mint},
    {x:780,y:260,w:210,h:110,label:"STATE",heading:"Executing",lines:["receipt required"],accent:C.orange},
    {x:1030,y:260,w:210,h:110,label:"STATE",heading:"Verifying",lines:["verifier result"],accent:C.lilac},
    {x:1280,y:260,w:240,h:110,label:"STATE",heading:"Review",lines:["effect reconciled"]},
  ];
  nodes.forEach((n,i)=>{s+=card(n);if(i<nodes.length-1)s+=arrow(n.x+n.w,n.y+55,nodes[i+1].x-5,nodes[i+1].y+55,C.purple,false);});
  const terms=["completed_verified","completed_unverified","failed_no_effect","failed_partial_effect","outcome_unknown","cancelled_with_effect"];
  terms.forEach((t,i)=>{const x=80+(i%3)*500,y=510+Math.floor(i/3)*95;s+=rect(x,y,450,70,C.white,i===4?C.red:C.border,20,2);s+=`<text x="${x+225}" y="${y+43}" class="label" text-anchor="middle">${esc(t.toUpperCase())}</text>`;});
  s+=arrow(1400,370,1280,510,C.purple,false);
  s+=pill(1035,425,205,"TERMINAL FROM EVIDENCE",C.pale,C.secondary);
  s+=finish("A cancelled stream is not a cancelled worker, and a “done” message is not a verifier result."); save("fig-ch16-02-durable-run-state-machine.svg",s);
}

// Level 3 intro: exploded message anatomy.
{
  let s=header("A simple channel request carries an authority chain","The message is only the entry point; identity, data, delegation, approval, and retention live elsewhere.","Exploded anatomy of an operations-agent channel request with callouts for requester access, agent principal, delegated machine worker, target ticket authority, approver eligibility, and retention policy.");
  s+=card({x:435,y:300,w:730,h:230,label:"SHARED CHANNEL",heading:"@OperationsAgent investigate onboarding",lines:["Ask the repository worker to inspect releases.","Prepare a ticket if you find a likely cause."],accent:C.lilac,fill:C.white});
  const calls=[
    {x:60,y:185,label:"WHO ASKED?",lines:["stable principal","data access"],from:[390,260],to:[435,370],accent:C.lilac},
    {x:60,y:555,label:"WHAT MAY BE SEEN?",lines:["customer events","destination disclosure"],from:[390,630],to:[435,465],accent:C.mint},
    {x:1210,y:185,label:"WHO ACTS?",lines:["agent service identity","credential mode"],from:[1210,260],to:[1165,370],accent:C.lilac},
    {x:1210,y:555,label:"WHO APPROVES?",lines:["eligible principal","current policy"],from:[1210,630],to:[1165,465],accent:C.mint},
    {x:435,y:140,label:"WHERE WORK RUNS",lines:["Level 2 task envelope","separate worker policy"],from:[600,290],to:[780,300],accent:C.lilac},
    {x:435,y:600,label:"WHAT PERSISTS",lines:["thread · transcript","memory · audit · ticket"],from:[600,600],to:[780,530],accent:C.mint},
  ];
  calls.forEach(({x,y,label,lines,from,to,accent})=>{
    s+=card({x,y,w:330,h:150,label,heading:lines[0],lines:[lines[1]],accent});
    const color=accent===C.mint?C.mint:C.purple;
    s+=`<path d="M${from[0]} ${from[1]} L${to[0]} ${to[1]}" fill="none" stroke="${color}" stroke-width="4" stroke-dasharray="10 8"/>`;
    s+=`<circle cx="${to[0]}" cy="${to[1]}" r="7" fill="${color}"/>`;
  });
  s+=finish("Organizational agency begins when shared authority is explainable, enforceable, and reconstructable."); save("fig-level3-01-message-authority-anatomy.svg",s);
}

// Chapter 17: actor chain.
flow("fig-ch17-01-organizational-actor-chain.svg","Preserve the organizational actor chain","Every consequential operation must retain who asked, who acted, what policy applied, and what the target accepted.","Flow from authenticated channel event through stable application principal, agent proposal, policy and credential mode, target operation, and authoritative receipt, with a blocked confused-deputy route.",[
  {label:"PLATFORM EVENT",heading:"Who asked?",lines:["tenant · user ID","channel · thread"]},
  {label:"IDENTITY MAP",heading:"Stable principal",lines:["current roles","tenant attributes"],accent:C.mint},
  {label:"AGENT PROFILE",heading:"Who proposes?",lines:["owner · tools","policy version"]},
  {label:"POLICY + MODE",heading:"Who may act?",lines:["agent-owned · OBO","approval-minted"],accent:C.mint},
  {label:"TARGET",heading:"What accepted?",lines:["resource · operation ID","result receipt"],accent:C.ink,dark:true,fill:C.ink},
],"A cheerful channel response is not proof that the target accepted the operation.",{h:310});

// Chapter 17: memory promotion.
{
  let s=header("Conversation is not institutional memory","Each store has a different owner, purpose, retention policy, and deletion path.","Seven storage lanes distinguish platform history, run state, transcript, working artifact, candidate memory, reviewed institutional memory, and audit; an explicit promotion path links candidate to institutional memory.");
  const stores=[
    ["PLATFORM","History",["workspace retention","editable/deletable"]],["RUN","State",["pause · resume","task-scoped"]],["PRODUCT","Transcript",["interaction review","separate retention"]],["WORK","Artifact",["report · plan · diff","candidate output"]],["CANDIDATE","Memory",["source + scope","not yet trusted"]],["REVIEWED","Institutional",["owner · effective","date","access · correction","· expiry"]],["SECURITY","Audit",["operational events","not conversation","memory"]],
  ];
  stores.forEach((st,i)=>{const x=42+i*220;s+=card({x,y:230,w:195,h:300,label:st[0],heading:st[1],lines:st[2],accent:i===5?C.mint:i===6?C.orange:C.lilac});});
  s+=arrow(1020,570,1240,570,C.mint,false,"evidence · classify · review · promote");
  s+=arrow(1460,550,1460,680,C.red,true,"separate retention");
  s+=finish("Deleting a thread does not automatically delete derived memory, artifacts, checkpoints, or audit records."); save("fig-ch17-02-memory-promotion.svg",s);
}

// Chapter 18: semantic approval across channels.
{
  let s=header("Render semantics, not pixels","One approval contract becomes platform-native UI with explicit fallbacks.","Three platform-neutral schematic cards show the same semantic approval rendered for Slack, Discord, and Microsoft Teams while preserving action, target, consequence, actor, expiry, and approve or reject controls.");
  const platforms=[
    ["SLACK ADAPTER","Thread card",["Block-style fields","native actions","ephemeral where supported"]],
    ["DISCORD ADAPTER","Interaction response",["fast acknowledgement","component actions","ephemeral depends on context"]],
    ["TEAMS ADAPTER","Adaptive surface",["tenant + app identity","inline card or safe web fallback","capabilities verified per tenant"]],
  ];
  platforms.forEach((p,i)=>{const x=70+i*510;s+=card({x,y:180,w:460,h:540,label:p[0],heading:p[1],lines:["Action: create synthetic ticket","Target: project ONBOARDING","Consequence: organizational write","Actor: OperationsAgent","Expires: 14:32 UTC",...p[2],"[ Approve ]    [ Reject ]"],accent:i===0?C.lilac:i===1?C.mint:C.orange});});
  s+=finish("Required semantics stay constant. Modal, file, ephemeral, streaming, and identity behavior must be capability-gated."); save("fig-ch18-02-cross-channel-semantic-approval.svg",s);
}

// Chapter 18: identifiers and restart.
{
  let s=header("Five identifiers protect different failure modes","Locks and ingestion dedup do not make an external write exactly once.","Identifier chain maps platform event ID, agent run ID, proposal ID, idempotency key, and target operation ID, then sequences a restart, ineligible click, eligible click, duplicate delivery, lost response, and reconciliation.");
  const ids=[
    ["EVENT ID","Delivery retry"],["RUN ID","One execution"],["PROPOSAL ID","Reviewed intent"],["IDEMPOTENCY KEY","One side effect"],["TARGET OP ID","Accepted effect"],
  ];
  ids.forEach((id,i)=>{const x=60+i*305;s+=card({x,y:180,w:275,h:170,label:`0${i+1}`,heading:id[0],lines:[id[1]],accent:i===3?C.mint:C.lilac});if(i<4)s+=arrow(x+275,265,x+300,265);});
  const seq=["render action","restart bot","deny wrong user","approve eligible user","retry event","lost response","reconcile receipt"];
  seq.forEach((e,i)=>{const x=75+i*215;s+=rect(x,500,190,100,C.white,i===2?C.red:i===6?C.mint:C.border,22,2);s+=pill(x+20,516,150,`STEP ${i+1}`,i===2?"#FA5F6726":i===6?C.mintSoft:C.pale);s+=`<text x="${x+95}" y="575" class="small" text-anchor="middle">${esc(e)}</text>`;if(i<6)s+=arrow(x+190,550,x+210,550);});
  s+=finish("The channel message converges on the target receipt; the effect count—not the button click—proves idempotency."); save("fig-ch18-03-durable-identifiers-restart.svg",s);
}

// Chapter 19: approval UI and trusted record.
{
  let s=header("Persist the proposal before rendering the button","The approval card is a projection of a trusted record, never the authorization record itself.","Side-by-side schematic shows a human-readable approval card and the server-side canonical proposal record containing identity, digest, target sensitivity, policy, eligibility, expiry, idempotency, and authoritative status.");
  s+=card({x:80,y:180,w:620,h:540,label:"CHANNEL PROJECTION",heading:"Post synthetic ledger adjustment",lines:["Requested by: Maya Chen","Acting principal: Finance Ledger Agent","Credential mode: agent service identity","Target: Ledger / synthetic-1042","Action: adjustment of $24.00","Rule: finance manager ≠ requester","Expires: 14:32 UTC","opaque action reference only","[ Approve ]    [ Reject ]"],accent:C.lilac});
  s+=card({x:820,y:180,w:700,h:540,label:"TRUSTED PROPOSAL RECORD",heading:"proposal_7f2 · revision 3",lines:["tenant · workspace · channel · thread","requester principal + agent principal","tool name/version + canonical arguments","action digest + target sensitivity","credential mode + policy version","eligible approver rule + quorum","expiry + one-use status","idempotency key + target operation ID","authoritative status: proposed"],accent:C.mint,fill:C.mintSoft});
  s+=arrow(700,450,815,450,C.purple,false,"render");
  s+=arrow(815,530,700,530,C.mint,false,"reload + reauthorize");
  s+=finish("A button carries an opaque routing value. A trusted service binds identity, policy, proposal, grant, and effect."); save("fig-ch19-02-approval-record-and-ui.svg",s);
}

// Chapter 19: channel projection vs audit timeline.
{
  let s=header("The channel card is not the audit log","Conversation is a status surface. Governance evidence lives in an independent operational record.","Split timeline contrasts editable channel status updates with append-oriented proposal, policy, approval, execution, target receipt, and reconciliation events.");
  s+=card({x:70,y:180,w:610,h:500,label:"CHANNEL PROJECTION",heading:"Useful, visible, mutable",lines:["proposal card rendered","observer sees generic denial","eligible approval recorded","status changes to executing","final ticket link displayed","platform edit/delete/retention applies"],accent:C.lilac});
  s+=card({x:920,y:180,w:610,h:500,label:"OPERATIONAL AUDIT",heading:"Restricted, correlated evidence",lines:["proposal.created · digest + revision","policy.decided · principal + version","approval.denied / granted","execution.dispatched · idempotency key","target.accepted · operation receipt","reconciliation.result · effect state"],accent:C.mint,fill:C.mintSoft});
  s+=arrow(680,320,915,320,C.purple,false,"status projection");
  s+=arrow(915,570,680,570,C.mint,false,"authoritative state");
  s+=`<path d="M800 230V650" stroke="${C.red}" stroke-width="3" stroke-dasharray="10 8"/><text x="800" y="705" class="label" text-anchor="middle">SEPARATE RETENTION · ACCESS · INTEGRITY</text>`;
  s+=finish("Do not call a channel message immutable, tamper-evident, or proof of target acceptance."); save("fig-ch19-03-audit-vs-channel-timeline.svg",s);
}

console.log("Generated Wave 1 Level 2/3 diagrams.");

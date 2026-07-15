import { posix } from "node:path";

export type MachineRisk = "read" | "write" | "external" | "privileged";

export interface MachinePolicy {
  readonly version: string;
  readonly paths: {
    readonly read: readonly string[];
    readonly write: readonly string[];
    readonly deny: readonly string[];
  };
  readonly commands: readonly {
    readonly executable: string;
    readonly subcommands: readonly string[];
    readonly maxArgs: number;
    readonly risk: MachineRisk;
  }[];
  readonly network: readonly {
    readonly protocol: "https:";
    readonly hostname: string;
    readonly methods: readonly ("GET" | "POST" | "PUT" | "DELETE")[];
  }[];
  readonly approvalRequiredFor: readonly MachineRisk[];
}

export type MachineIntent =
  | {
      readonly kind: "path";
      readonly operation: "read" | "write";
      readonly path: string;
    }
  | {
      readonly kind: "command";
      readonly executable: string;
      readonly args: readonly string[];
    }
  | { readonly kind: "network"; readonly url: string; readonly method: string };

export interface PolicyDecision {
  readonly outcome: "allow" | "deny" | "approval";
  readonly risk: MachineRisk;
  readonly reason: string;
}

function normalizedRelativePath(candidate: string): string | null {
  if (candidate.includes("\0") || candidate.startsWith("/")) return null;
  const normalized = posix.normalize(candidate.replaceAll("\\", "/"));
  if (normalized === ".." || normalized.startsWith("../")) return null;
  return normalized.replace(/^\.\//, "");
}

function matchesRule(path: string, rule: string): boolean {
  return rule.endsWith("/**")
    ? path === rule.slice(0, -3) || path.startsWith(rule.slice(0, -2))
    : path === rule;
}

function decide(
  risk: MachineRisk,
  policy: MachinePolicy,
  reason: string,
): PolicyDecision {
  return policy.approvalRequiredFor.includes(risk)
    ? { outcome: "approval", risk, reason }
    : { outcome: "allow", risk, reason };
}

export function evaluateMachineIntent(
  policy: MachinePolicy,
  intent: MachineIntent,
): PolicyDecision {
  if (intent.kind === "path") {
    const path = normalizedRelativePath(intent.path);
    if (!path)
      return {
        outcome: "deny",
        risk: "privileged",
        reason: "path escapes workspace",
      };
    if (policy.paths.deny.some((rule) => matchesRule(path, rule))) {
      return {
        outcome: "deny",
        risk: "privileged",
        reason: "path is explicitly denied",
      };
    }
    const allowed = policy.paths[intent.operation].some((rule) =>
      matchesRule(path, rule),
    );
    if (!allowed)
      return {
        outcome: "deny",
        risk: intent.operation,
        reason: "path is not allowlisted",
      };
    return decide(
      intent.operation,
      policy,
      `${intent.operation} path is allowlisted`,
    );
  }

  if (intent.kind === "command") {
    if (
      intent.executable.includes("/") ||
      intent.args.some((arg) => arg.includes("\0"))
    ) {
      return {
        outcome: "deny",
        risk: "privileged",
        reason: "command must use structured argv",
      };
    }
    const rule = policy.commands.find(
      (entry) => entry.executable === intent.executable,
    );
    if (!rule || intent.args.length > rule.maxArgs) {
      return {
        outcome: "deny",
        risk: "privileged",
        reason: "command is not allowlisted",
      };
    }
    const subcommand = intent.args[0];
    if (subcommand && !rule.subcommands.includes(subcommand)) {
      return {
        outcome: "deny",
        risk: rule.risk,
        reason: "subcommand is not allowlisted",
      };
    }
    return decide(rule.risk, policy, "command and argv are allowlisted");
  }

  let url: URL;
  try {
    url = new URL(intent.url);
  } catch {
    return { outcome: "deny", risk: "external", reason: "invalid URL" };
  }
  const method = intent.method.toUpperCase();
  const rule = policy.network.find(
    (entry) =>
      entry.protocol === url.protocol &&
      entry.hostname === url.hostname &&
      entry.methods.includes(method as "GET" | "POST" | "PUT" | "DELETE"),
  );
  if (!rule)
    return {
      outcome: "deny",
      risk: "external",
      reason: "network destination is not allowlisted",
    };
  return decide("external", policy, "network destination is allowlisted");
}

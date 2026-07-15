export type ToolEffect = "read" | "write" | "external" | "privileged";
export type ApprovalMode = "never" | "conditional" | "always";

export interface ToolRiskMetadata {
  readonly effect: ToolEffect;
  readonly reversible: boolean;
  readonly approval: ApprovalMode;
  readonly dataClass: "public" | "internal" | "sensitive";
}

export const LEVEL_1_TOOL_RISKS = {
  get_visible_ledger: {
    effect: "read",
    reversible: true,
    approval: "never",
    dataClass: "sensitive",
  },
  search_transactions: {
    effect: "read",
    reversible: true,
    approval: "never",
    dataClass: "sensitive",
  },
  propose_transaction: {
    effect: "write",
    reversible: true,
    approval: "always",
    dataClass: "sensitive",
  },
} as const satisfies Readonly<Record<string, ToolRiskMetadata>>;

export type Level1ToolName = keyof typeof LEVEL_1_TOOL_RISKS;

export function getLevel1ToolRisk(toolName: Level1ToolName): ToolRiskMetadata {
  return LEVEL_1_TOOL_RISKS[toolName];
}

export type StateActor = "agent" | "ui";
export type FieldOwner = StateActor | "shared" | "derived";
export type LedgerTaskStatus =
  | "idle"
  | "reading"
  | "ready"
  | "waiting_for_approval"
  | "committing"
  | "retrying"
  | "cancel_requested"
  | "cancelled"
  | "failed"
  | "complete";

export interface LedgerState {
  readonly schemaVersion: 1;
  readonly revision: number;
  readonly objective: string;
  readonly status: LedgerTaskStatus;
  readonly selectedTransactionId: string | null;
  readonly dateRange: { readonly from: string; readonly to: string };
  readonly draftSummary: string;
}

export interface LedgerStateChanges {
  objective?: string;
  status?: LedgerState["status"];
  selectedTransactionId?: string | null;
  dateRange?: LedgerState["dateRange"];
  draftSummary?: string;
}

export interface LedgerStatePatch {
  readonly baseRevision: number;
  readonly changes: LedgerStateChanges;
}

export const LEDGER_STATE_OWNERSHIP = {
  schemaVersion: "derived",
  revision: "derived",
  objective: "ui",
  status: "agent",
  selectedTransactionId: "ui",
  dateRange: "shared",
  draftSummary: "agent",
} as const satisfies Readonly<Record<keyof LedgerState, FieldOwner>>;

function assertMayWrite(
  actor: StateActor,
  owner: FieldOwner,
  field: string,
): void {
  if (owner !== "shared" && owner !== actor) {
    throw new Error(`${actor} cannot update ${field}; it is ${owner}-owned`);
  }
}

export function applyLedgerStatePatch(
  state: LedgerState,
  actor: StateActor,
  patch: LedgerStatePatch,
): LedgerState {
  if (patch.baseRevision !== state.revision) {
    throw new Error(
      `stale state patch: expected revision ${state.revision}, got ${patch.baseRevision}`,
    );
  }

  let next = state;
  const changes = patch.changes;

  if (changes.objective !== undefined) {
    assertMayWrite(actor, LEDGER_STATE_OWNERSHIP.objective, "objective");
    next = { ...next, objective: changes.objective };
  }
  if (changes.status !== undefined) {
    assertMayWrite(actor, LEDGER_STATE_OWNERSHIP.status, "status");
    next = { ...next, status: changes.status };
  }
  if (changes.selectedTransactionId !== undefined) {
    assertMayWrite(
      actor,
      LEDGER_STATE_OWNERSHIP.selectedTransactionId,
      "selectedTransactionId",
    );
    next = { ...next, selectedTransactionId: changes.selectedTransactionId };
  }
  if (changes.dateRange !== undefined) {
    assertMayWrite(actor, LEDGER_STATE_OWNERSHIP.dateRange, "dateRange");
    next = { ...next, dateRange: changes.dateRange };
  }
  if (changes.draftSummary !== undefined) {
    assertMayWrite(actor, LEDGER_STATE_OWNERSHIP.draftSummary, "draftSummary");
    next = { ...next, draftSummary: changes.draftSummary };
  }

  return { ...next, revision: state.revision + 1 };
}

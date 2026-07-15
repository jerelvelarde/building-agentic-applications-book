import { describe, expect, it } from "vitest";
import {
  applyLedgerStatePatch,
  type LedgerState,
} from "../src/level-1/shared-state.js";

const STATE: LedgerState = {
  schemaVersion: 1,
  revision: 4,
  objective: "Review July spending",
  status: "idle",
  selectedTransactionId: null,
  dateRange: { from: "2026-07-01", to: "2026-07-31" },
  draftSummary: "",
};

describe("applyLedgerStatePatch", () => {
  it("rejects a stale revision", () => {
    expect(() =>
      applyLedgerStatePatch(STATE, "ui", {
        baseRevision: 3,
        changes: { objective: "Old edit" },
      }),
    ).toThrow("stale");
  });

  it("rejects an agent write to a UI-owned field", () => {
    expect(() =>
      applyLedgerStatePatch(STATE, "agent", {
        baseRevision: 4,
        changes: { objective: "Overwrite" },
      }),
    ).toThrow("ui-owned");
  });
});

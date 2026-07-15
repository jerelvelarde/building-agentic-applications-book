import { describe, expect, it } from "vitest";
import {
  BudgetExceededError,
  RunBudgetGuard,
} from "../src/production/run-budget.js";
import {
  evaluateTrajectory,
  LEDGER_TRAJECTORY_CONTRACT,
  SAFE_LEDGER_TRAJECTORY,
} from "../src/production/trajectory.js";

describe("production guards", () => {
  it("evaluates a deterministic safe trajectory", () => {
    expect(
      evaluateTrajectory(SAFE_LEDGER_TRAJECTORY, LEDGER_TRAJECTORY_CONTRACT),
    ).toEqual({ passed: true, violations: [] });
  });

  it("detects a write without its required approval", () => {
    const result = evaluateTrajectory(
      [
        { kind: "tool", name: "search_transactions", outcome: "success" },
        { kind: "tool", name: "create_transaction", outcome: "success" },
      ],
      LEDGER_TRAJECTORY_CONTRACT,
    );
    expect(result.passed).toBe(false);
    expect(result.violations).toContain(
      "create_transaction ran without approve_transaction",
    );
  });

  it("stops before a step crosses the cost budget", () => {
    const guard = new RunBudgetGuard(
      { maxSteps: 3, maxCostUsd: 0.05, maxDurationMs: 10_000 },
      () => 100,
    );
    guard.consume(0.03);
    expect(() => guard.consume(0.03)).toThrow(BudgetExceededError);
    expect(guard.snapshot().steps).toBe(1);
  });
});

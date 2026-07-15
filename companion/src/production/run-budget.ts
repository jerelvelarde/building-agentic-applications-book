export interface RunBudget {
  readonly maxSteps: number;
  readonly maxCostUsd: number;
  readonly maxDurationMs: number;
}

export class BudgetExceededError extends Error {
  override readonly name = "BudgetExceededError";
}

export class RunBudgetGuard {
  private steps = 0;
  private costUsd = 0;
  private readonly startedAt: number;

  constructor(
    private readonly budget: RunBudget,
    private readonly now: () => number = Date.now,
  ) {
    this.startedAt = now();
  }

  consume(costUsd: number): void {
    if (!Number.isFinite(costUsd) || costUsd < 0)
      throw new Error("step cost must be non-negative");
    const nextSteps = this.steps + 1;
    const nextCost = this.costUsd + costUsd;
    const elapsed = this.now() - this.startedAt;
    if (nextSteps > this.budget.maxSteps)
      throw new BudgetExceededError("step budget exceeded");
    if (nextCost > this.budget.maxCostUsd)
      throw new BudgetExceededError("cost budget exceeded");
    if (elapsed > this.budget.maxDurationMs)
      throw new BudgetExceededError("time budget exceeded");
    this.steps = nextSteps;
    this.costUsd = nextCost;
  }

  snapshot() {
    return {
      steps: this.steps,
      costUsd: this.costUsd,
      elapsedMs: this.now() - this.startedAt,
    };
  }
}

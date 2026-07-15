import { describe, expect, it, vi } from "vitest";
import {
  GovernedWriteGate,
  type Principal,
  type WriteRequest,
} from "../src/level-3/governed-action.js";

const NOW = 1_800_000_000_000;
const REQUEST: WriteRequest = {
  requestId: "req-42",
  actionId: "linear.create_issue:v1",
  toolName: "create_linear_issue",
  arguments: { title: "Fix checkout" },
  requestedBy: "user-requester",
  eligibleApproverIds: ["user-approver"],
  eligibleApproverRoles: ["incident-commander"],
  expiresAt: NOW + 60_000,
  idempotencyKey: "linear:req-42",
};

function registerGate() {
  const gate = new GovernedWriteGate<{ issueId: string }>(() => NOW);
  gate.register(REQUEST);
  return gate;
}

const UNAUTHORIZED: Principal = { id: "user-observer", roles: ["viewer"] };
const APPROVER: Principal = { id: "user-approver", roles: [] };

describe("GovernedWriteGate", () => {
  it("rejects a click from an unauthorized principal", () => {
    const gate = registerGate();
    expect(() =>
      gate.approve(REQUEST.requestId, UNAUTHORIZED, REQUEST.actionId),
    ).toThrow("eligible approver");
  });

  it("suppresses a replay without repeating the write", async () => {
    const gate = registerGate();
    const grant = gate.approve(REQUEST.requestId, APPROVER, REQUEST.actionId);
    const effect = vi.fn(() => Promise.resolve({ issueId: "CPK-2026" }));

    await expect(gate.execute(grant, effect)).resolves.toEqual({
      issueId: "CPK-2026",
    });
    await expect(gate.execute(grant, effect)).resolves.toEqual({
      issueId: "CPK-2026",
    });
    expect(effect).toHaveBeenCalledTimes(1);
    expect(gate.audit().at(-1)?.event).toBe("replay_suppressed");
  });
});

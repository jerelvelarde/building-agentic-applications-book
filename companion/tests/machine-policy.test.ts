import { describe, expect, it } from "vitest";
import {
  evaluateMachineIntent,
  type MachinePolicy,
} from "../src/level-2/machine-policy.js";

const POLICY: MachinePolicy = {
  version: "book-2026-01",
  paths: {
    read: ["src/**", "package.json"],
    write: ["src/**"],
    deny: [".env", ".git/**"],
  },
  commands: [
    {
      executable: "npm",
      subcommands: ["test", "run"],
      maxArgs: 3,
      risk: "write",
    },
  ],
  network: [
    { protocol: "https:", hostname: "api.github.com", methods: ["GET"] },
  ],
  approvalRequiredFor: ["write", "external", "privileged"],
};

describe("evaluateMachineIntent", () => {
  it("denies protected paths before applying allow rules", () => {
    expect(
      evaluateMachineIntent(POLICY, {
        kind: "path",
        operation: "read",
        path: ".env",
      }).outcome,
    ).toBe("deny");
  });

  it("requires approval for an allowlisted write command", () => {
    expect(
      evaluateMachineIntent(POLICY, {
        kind: "command",
        executable: "npm",
        args: ["test"],
      }).outcome,
    ).toBe("approval");
  });

  it("denies a network host that is not exactly allowlisted", () => {
    expect(
      evaluateMachineIntent(POLICY, {
        kind: "network",
        url: "https://api.github.com.attacker.test",
        method: "GET",
      }).outcome,
    ).toBe("deny");
  });
});

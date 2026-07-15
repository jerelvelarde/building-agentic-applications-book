import { mkdtemp, mkdir, realpath, symlink, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { resolveWorkspacePath } from "../src/level-2/workspace.js";

async function createWorkspaceFixture() {
  const root = await mkdtemp(join(tmpdir(), "agent-book-workspace-"));
  const outside = await mkdtemp(join(tmpdir(), "agent-book-outside-"));
  await mkdir(join(root, "src"));
  await writeFile(join(root, "src", "safe.ts"), "export {};\n");
  await writeFile(join(outside, "secret.txt"), "not for the agent\n");
  await symlink(outside, join(root, "escape"));
  return { root, outside };
}

describe("resolveWorkspacePath", () => {
  it("resolves a real file inside the workspace", async () => {
    const { root } = await createWorkspaceFixture();
    const expected = await realpath(join(root, "src", "safe.ts"));
    await expect(
      resolveWorkspacePath(root, "src/safe.ts", "read"),
    ).resolves.toBe(expected);
  });

  it("rejects a symlink that resolves outside the workspace", async () => {
    const { root } = await createWorkspaceFixture();
    await expect(
      resolveWorkspacePath(root, "escape/secret.txt", "read"),
    ).rejects.toThrow("outside workspace");
  });

  it("rejects a write through a symlinked parent", async () => {
    const { root } = await createWorkspaceFixture();
    await expect(
      resolveWorkspacePath(root, "escape/new.txt", "write"),
    ).rejects.toThrow("outside workspace");
  });
});

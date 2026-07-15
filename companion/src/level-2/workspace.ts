import { realpath } from "node:fs/promises";
import { dirname, isAbsolute, relative, resolve } from "node:path";

function isWithin(root: string, candidate: string): boolean {
  const path = relative(root, candidate);
  return path === "" || (!path.startsWith("..") && !isAbsolute(path));
}

export async function resolveWorkspacePath(
  workspaceRoot: string,
  requestedPath: string,
  mode: "read" | "write",
): Promise<string> {
  if (isAbsolute(requestedPath) || requestedPath.includes("\0")) {
    throw new Error("workspace path must be a safe relative path");
  }

  const root = await realpath(workspaceRoot);
  const lexicalTarget = resolve(root, requestedPath);
  if (!isWithin(root, lexicalTarget)) throw new Error("path escapes workspace");

  if (mode === "read") {
    const target = await realpath(lexicalTarget);
    if (!isWithin(root, target))
      throw new Error("symlink resolves outside workspace");
    return target;
  }

  // A new write target may not exist, so resolve its existing parent. This
  // catches a symlinked directory that points outside the workspace.
  const parent = await realpath(dirname(lexicalTarget));
  if (!isWithin(root, parent))
    throw new Error("write parent resolves outside workspace");
  return lexicalTarget;
}

import { spawnSync } from "node:child_process";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const generators = [
  "../generate-final-deterministic.mjs",
  "../generate-wave1-l2-l3.mjs",
];

for (const generator of generators) {
  const result = spawnSync(process.execPath, [resolve(here, generator)], {
    cwd: resolve(here, "../../.."),
    stdio: "inherit",
  });

  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}

const validation = spawnSync(process.execPath, [resolve(here, "validate.mjs")], {
  cwd: resolve(here, "../../.."),
  stdio: "inherit",
});

process.exit(validation.status ?? 1);

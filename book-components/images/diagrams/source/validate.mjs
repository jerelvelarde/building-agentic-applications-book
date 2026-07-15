import { existsSync, readFileSync, readdirSync } from "node:fs";
import { basename, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const diagramDir = resolve(here, "..");
const registry = JSON.parse(readFileSync(resolve(here, "registry.json"), "utf8"));
const failures = [];
const generatedOwners = new Map();

for (const generator of registry.generators) {
  const sourcePath = resolve(here, generator.source);
  if (!existsSync(sourcePath)) failures.push(`missing generator: ${generator.source}`);

  for (const output of generator.outputs) {
    if (generatedOwners.has(output)) failures.push(`duplicate owner: ${output}`);
    generatedOwners.set(output, generator.id);
    if (!existsSync(resolve(diagramDir, output))) failures.push(`missing generated SVG: ${output}`);
  }
}

const svgFiles = readdirSync(diagramDir).filter((name) => name.endsWith(".svg")).sort();
for (const name of svgFiles) {
  const source = readFileSync(resolve(diagramDir, name), "utf8");
  if (!/viewBox="0 0 1600 900"/.test(source)) failures.push(`${name}: expected 1600 x 900 viewBox`);
  if (!/<title(?:\s|>)/.test(source)) failures.push(`${name}: missing title`);
  if (!/<desc(?:\s|>)/.test(source)) failures.push(`${name}: missing desc`);
  if (/FINAL EDITION|REVIEW EDITION/i.test(source)) failures.push(`${name}: stale edition wording`);
}

for (const output of generatedOwners.keys()) {
  if (!svgFiles.includes(output)) failures.push(`registry output not in inventory: ${output}`);
}

if (failures.length) {
  console.error(`Diagram validation failed with ${failures.length} finding(s):`);
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}

console.log(`Diagram validation passed: ${svgFiles.length} SVGs; ${generatedOwners.size} generated; ${svgFiles.length - generatedOwners.size} hand-authored.`);
console.log(`Registry: ${basename(resolve(here, "registry.json"))}`);

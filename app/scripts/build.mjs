/**
 * Build a completely static prototype without any package installation.
 *
 * Copies one EXISTING repository illustration as a TEMPORARY scene backdrop.
 * The final scenes and sprite PNGs will be designed after interaction testing.
 * Nothing is deployed or uploaded by running this script.
 */
import { cp, mkdir, rm, stat } from "node:fs/promises";
import { dirname, resolve, join } from "node:path";
import { fileURLToPath } from "node:url";

const scriptFolder = dirname(fileURLToPath(import.meta.url));
const appRoot = resolve(scriptFolder, "..");
const repositoryRoot = resolve(appRoot, "..");
const destination = join(appRoot, "dist");
const sceneSource = join(repositoryRoot, "assets", "images", "available-capacity.png");

// A missing placeholder illustration must fail the build visibly rather than
// producing a broken but apparently successful prototype.
const sourceStat = await stat(sceneSource);
if (!sourceStat.isFile()) throw new Error("Temporary PNG scene is missing");

await rm(destination, { recursive: true, force: true });
await mkdir(join(destination, "assets"), { recursive: true });

for (const name of ["index.html", "styles.css", "manifest.webmanifest", "icon.svg", "sw.js"]) {
  await cp(join(appRoot, name), join(destination, name));
}
await cp(join(appRoot, "src"), join(destination, "src"), { recursive: true });
await cp(sceneSource, join(destination, "assets", "scene.png"));

process.stdout.write("Built local-only Phase 0 prototype in app/dist (not deployed).\n");

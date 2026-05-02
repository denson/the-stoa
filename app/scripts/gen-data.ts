// gen-data: build the typed agent data file from canonical substrate.
//
// Reads canonical role files (`MAJOR_*.md`, `CAPTAIN_*.md`) from the
// substrate directory, validates their frontmatter against a Zod schema,
// extracts the descriptive role from the body, and emits a typed
// TypeScript module at `app/src/data/generated/agents.ts` shaped to
// `StoaDataV2` (see `app/src/data/types-v2.ts`).
//
// Design notes:
//   - Substrate path defaults to `../substrate/` relative to the repo root
//     (i.e. `app/` and `substrate/` are siblings in the-stoa). Override via
//     the `AGENT_SUBSTRATE_PATH` env var (no `VITE_` prefix — this is a
//     build script, not client code).
//   - Only top-level role files are consumed; subdirectories like
//     `arcs/`, `templates/`, `v1-historical/`, `superseded/` are skipped.
//   - The pure pipeline (discover, parse, assemble, emit) lives in
//     `gen-data-lib.ts` so Vitest can exercise it without invoking this
//     script's main(). This file is the thin entry: paths in, summary out.
//   - The generated file is committed to git per the localhost-only
//     deployment posture (decided 2026-05-02).
//
// Re-run manually with `npm run gen-data`. `predev` and `prebuild` hooks
// auto-run it before `npm run dev` and `npm run build`.

import * as path from "node:path";
import { generate } from "./gen-data-lib.js";

// ---------------------------------------------------------------------------
// Paths
// ---------------------------------------------------------------------------

const scriptDir = import.meta.dirname;
const repoRoot = path.resolve(scriptDir, "..", "..");
const defaultSubstratePath = path.resolve(repoRoot, "substrate");
const substratePath = process.env.AGENT_SUBSTRATE_PATH
  ? path.resolve(process.env.AGENT_SUBSTRATE_PATH)
  : defaultSubstratePath;

const outputPath = path.resolve(
  scriptDir,
  "..",
  "src",
  "data",
  "generated",
  "agents.ts",
);

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

try {
  console.log(`[gen-data] substrate: ${substratePath}`);
  const summary = generate({ substratePath, outputPath });
  console.log(`[gen-data] discovered ${summary.fileCount} role file(s)`);
  console.log(`[gen-data] wrote ${outputPath}`);
  console.log(
    `[gen-data] roster: ${summary.majorCount} MAJOR(s), ` +
      `${summary.captainCount} CAPTAIN(s); ` +
      `COLONEL reserved-empty; HUMAN stub; LIEUTENANT empty`,
  );
} catch (err) {
  console.error(err instanceof Error ? err.message : String(err));
  process.exit(1);
}

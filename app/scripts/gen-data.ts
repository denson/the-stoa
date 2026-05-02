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
//   - Schema validation at the ingestion boundary is the load-bearing
//     property: a malformed role file fails the build with a descriptive
//     error rather than silently propagating a broken record downstream.
//   - The generated file is committed to git per the localhost-only
//     deployment posture (decided 2026-05-02).
//
// Re-run manually with `npm run gen-data`. `predev` and `prebuild` hooks
// auto-run it before `npm run dev` and `npm run build`.

import * as fs from "node:fs";
import * as path from "node:path";
import matter from "gray-matter";
import {
  agentSchema,
  frontmatterSchema,
  stoaDataV2Schema,
} from "./schemas.js";
import type {
  Agent,
  AgentRank,
  StoaDataV2,
} from "../src/data/types-v2.js";
import { z } from "zod";

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
// Discovery
// ---------------------------------------------------------------------------

type RoleFile = {
  filename: string;
  fullPath: string;
  rank: Extract<AgentRank, "MAJOR" | "CAPTAIN">;
  mnemonic: string;
};

function discoverRoleFiles(dir: string): RoleFile[] {
  if (!fs.existsSync(dir)) {
    throw new Error(
      `Substrate directory not found: ${dir}\n` +
        `Set AGENT_SUBSTRATE_PATH or run from the-stoa repo root.`,
    );
  }
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const files: RoleFile[] = [];
  for (const entry of entries) {
    if (!entry.isFile()) continue;
    const match = entry.name.match(/^(MAJOR|CAPTAIN)_([A-Z][A-Z0-9_-]*)\.md$/);
    if (!match) continue;
    files.push({
      filename: entry.name,
      fullPath: path.join(dir, entry.name),
      rank: match[1] as "MAJOR" | "CAPTAIN",
      mnemonic: match[2]!,
    });
  }
  files.sort((a, b) => a.filename.localeCompare(b.filename));
  return files;
}

// ---------------------------------------------------------------------------
// Parse + validate
// ---------------------------------------------------------------------------

const NAME_SUFFIX_TOKEN = "{{NAME_SUFFIX}}";

/** Pull the descriptive role from the role file's `| **Descriptive role** | XXX |` row. */
function extractDescriptiveRole(body: string, filename: string): string {
  const match = body.match(
    /^\|\s*\*\*Descriptive role\*\*\s*\|\s*([A-Z][A-Z0-9_-]*)\s*\|/m,
  );
  if (!match) {
    throw new Error(
      `[${filename}] could not find a "| **Descriptive role** | XXX |" row in the body. ` +
        `Every role file must declare its descriptive role in the header table.`,
    );
  }
  return match[1]!;
}

function buildAgent(file: RoleFile): Agent {
  const raw = fs.readFileSync(file.fullPath, "utf8");
  const parsed = matter(raw);
  const body = parsed.content;

  let tools: string[] = [];
  let modelTier: string | undefined;

  // CAPTAINs carry frontmatter (Claude Code sub-agent metadata); MAJORs do not.
  if (file.rank === "CAPTAIN") {
    const fmResult = frontmatterSchema.safeParse(parsed.data);
    if (!fmResult.success) {
      throw new Error(
        `[${file.filename}] frontmatter validation failed:\n` +
          z.prettifyError(fmResult.error),
      );
    }
    tools = fmResult.data.tools;
    modelTier = fmResult.data.model;
  } else if (Object.keys(parsed.data).length > 0) {
    // MAJORs: warn-loud if frontmatter ever appears so format drift is caught.
    throw new Error(
      `[${file.filename}] MAJOR role files are not expected to carry YAML frontmatter ` +
        `(found keys: ${Object.keys(parsed.data).join(", ")}). ` +
        `If MAJORs should now have frontmatter, update the schema to match.`,
    );
  }

  const descriptiveRole = extractDescriptiveRole(body, file.filename);

  // The frontmatter `name` field embeds a `{{NAME_SUFFIX}}` template token
  // (resolved at deploy time by install.sh). The canonical filename has no
  // suffix; use that for `filename`.
  const canonicalFilename = file.filename;

  const agent: Agent = {
    rank: file.rank,
    mnemonic: file.mnemonic,
    descriptiveRole,
    body,
    tools,
    filename: canonicalFilename,
    ...(modelTier !== undefined ? { modelTier } : {}),
  };

  // Self-check the assembled record against the output schema. Catches
  // anything the body extractors produced that doesn't match types-v2.ts.
  const check = agentSchema.safeParse(agent);
  if (!check.success) {
    throw new Error(
      `[${file.filename}] assembled Agent record fails schema:\n` +
        z.prettifyError(check.error),
    );
  }
  return agent;
}

// ---------------------------------------------------------------------------
// Roster assembly
// ---------------------------------------------------------------------------

function assembleStoaData(agents: Agent[]): StoaDataV2 {
  const majors = agents.filter((a) => a.rank === "MAJOR");
  const captains = agents.filter((a) => a.rank === "CAPTAIN");

  // HUMAN slot: stub for now. Substrate carries no Human records; the
  // PRINCIPAL's name is learned through onboarding (planning v2 §3) and
  // doesn't live in canonical role files. Slot is populated with a single
  // anonymous PRINCIPAL placeholder so the rank ladder renders correctly.
  const data: StoaDataV2 = {
    roster: [
      {
        rank: "HUMAN",
        agents: [{ rank: "HUMAN", descriptiveRole: "PRINCIPAL" }],
      },
      {
        // COLONEL is reserved future agent rank. v1 used "Colonel" to mean
        // the human; v2 corrects that. Slot is visible but empty by design.
        rank: "COLONEL",
        reserved: true,
        agents: [],
      },
      { rank: "MAJOR", agents: majors },
      { rank: "CAPTAIN", agents: captains },
      // LIEUTENANTs (skills) are out of scope for Arc 10 — Arc 13 territory.
      { rank: "LIEUTENANT", agents: [] },
    ],
  };
  return data;
}

// ---------------------------------------------------------------------------
// Output writer
// ---------------------------------------------------------------------------

function emitTypeScript(data: StoaDataV2): string {
  const stamp = new Date().toISOString();
  const header = [
    "// AUTO-GENERATED by app/scripts/gen-data.ts — DO NOT EDIT BY HAND.",
    "//",
    "// Regenerate with: `npm run gen-data` (also auto-runs via predev/prebuild).",
    "// Source of truth: canonical role files in `substrate/` at repo root.",
    `// Generated: ${stamp}`,
    "",
    'import type { StoaDataV2 } from "../types-v2";',
    "",
  ].join("\n");
  const body = `export const stoaData: StoaDataV2 = ${JSON.stringify(data, null, 2)};\n`;
  return header + body;
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main(): void {
  console.log(`[gen-data] substrate: ${substratePath}`);
  const files = discoverRoleFiles(substratePath);
  if (files.length === 0) {
    throw new Error(
      `[gen-data] no MAJOR_*.md or CAPTAIN_*.md files found in ${substratePath}`,
    );
  }
  console.log(`[gen-data] discovered ${files.length} role file(s)`);
  const agents = files.map(buildAgent);
  const data = assembleStoaData(agents);

  const result = stoaDataV2Schema.safeParse(data);
  if (!result.success) {
    throw new Error(
      `[gen-data] assembled StoaDataV2 fails schema:\n` +
        z.prettifyError(result.error),
    );
  }

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, emitTypeScript(data), "utf8");
  console.log(`[gen-data] wrote ${outputPath}`);
  console.log(
    `[gen-data] roster: ${agents.filter((a) => a.rank === "MAJOR").length} MAJOR(s), ` +
      `${agents.filter((a) => a.rank === "CAPTAIN").length} CAPTAIN(s); ` +
      `COLONEL reserved-empty; HUMAN stub; LIEUTENANT empty (Arc 13 wires skills)`,
  );
}

try {
  main();
} catch (err) {
  console.error(err instanceof Error ? err.message : String(err));
  process.exit(1);
}

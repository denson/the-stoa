// gen-data-lib: pure library of the gen-data adapter.
//
// Split out of `gen-data.ts` so the parser, schema validator, roster
// assembler, and emitter can be exercised by Vitest without invoking the
// script's main() (which would read the real substrate and exit on error).
//
// `gen-data.ts` remains the thin script entry: it resolves paths, calls
// `generate(...)`, and handles process exit. Everything testable lives
// here.
//
// Design notes:
//   - Functions take their inputs as arguments (no module-level path
//     resolution). Tests can call them with synthetic fixtures.
//   - Schema validation at the ingestion boundary is the load-bearing
//     property: a malformed role file fails with a descriptive error.
//   - The emitted file's header is deterministic — no timestamp, no other
//     run-varying token. Same substrate -> byte-identical output.

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
// Discovery
// ---------------------------------------------------------------------------

export type RoleFile = {
  filename: string;
  fullPath: string;
  rank: Extract<AgentRank, "MAJOR" | "CAPTAIN">;
  mnemonic: string;
};

export function discoverRoleFiles(dir: string): RoleFile[] {
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

/** Pull the descriptive role from the role file's `| **Descriptive role** | XXX |` row. */
export function extractDescriptiveRole(body: string, filename: string): string {
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

export function buildAgent(file: RoleFile): Agent {
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

export function assembleStoaData(agents: Agent[]): StoaDataV2 {
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
      // LIEUTENANTs (skills) — substrate currently carries none; slot is
      // visible but empty until skills are authored.
      { rank: "LIEUTENANT", agents: [] },
    ],
  };
  return data;
}

// ---------------------------------------------------------------------------
// Output
// ---------------------------------------------------------------------------

export function emitTypeScript(data: StoaDataV2): string {
  const header = [
    "// AUTO-GENERATED by app/scripts/gen-data.ts — DO NOT EDIT BY HAND.",
    "//",
    "// Regenerate with: `npm run gen-data` (also auto-runs via predev/prebuild).",
    "// Source of truth: canonical role files in `substrate/` at repo root.",
    "",
    'import type { StoaDataV2 } from "../types-v2";',
    "",
  ].join("\n");
  const body = `export const stoaData: StoaDataV2 = ${JSON.stringify(data, null, 2)};\n`;
  return header + body;
}

// ---------------------------------------------------------------------------
// Orchestration
// ---------------------------------------------------------------------------

export type GenerateOptions = {
  substratePath: string;
  outputPath: string;
};

export type GenerateResult = {
  fileCount: number;
  majorCount: number;
  captainCount: number;
};

/**
 * Run the full pipeline: discover -> parse -> assemble -> validate -> emit.
 * Throws on any error; callers handle process exit if desired.
 */
export function generate(opts: GenerateOptions): GenerateResult {
  const files = discoverRoleFiles(opts.substratePath);
  if (files.length === 0) {
    throw new Error(
      `[gen-data] no MAJOR_*.md or CAPTAIN_*.md files found in ${opts.substratePath}`,
    );
  }
  const agents = files.map(buildAgent);
  const data = assembleStoaData(agents);

  const result = stoaDataV2Schema.safeParse(data);
  if (!result.success) {
    throw new Error(
      `[gen-data] assembled StoaDataV2 fails schema:\n` +
        z.prettifyError(result.error),
    );
  }

  fs.mkdirSync(path.dirname(opts.outputPath), { recursive: true });
  fs.writeFileSync(opts.outputPath, emitTypeScript(data), "utf8");

  return {
    fileCount: files.length,
    majorCount: agents.filter((a) => a.rank === "MAJOR").length,
    captainCount: agents.filter((a) => a.rank === "CAPTAIN").length,
  };
}

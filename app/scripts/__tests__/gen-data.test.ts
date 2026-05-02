// Tests for the gen-data adapter (Arc 10) — exercise the parse pipeline
// against synthetic fixtures so the adapter's invariants (Zod-validated
// frontmatter, body extraction, schema-conformant output) can be checked
// without running the script's main() or touching the real substrate.

import { describe, it, expect, beforeEach, afterEach } from "vitest";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import {
  discoverRoleFiles,
  buildAgent,
  assembleStoaData,
  emitTypeScript,
  generate,
  extractDescriptiveRole,
  type RoleFile,
} from "../gen-data-lib.js";
import { stoaDataV2Schema } from "../schemas.js";

// ---------------------------------------------------------------------------
// Fixture helpers
// ---------------------------------------------------------------------------

let fixtureDir: string;

beforeEach(() => {
  fixtureDir = fs.mkdtempSync(path.join(os.tmpdir(), "stoa-gen-data-"));
});

afterEach(() => {
  fs.rmSync(fixtureDir, { recursive: true, force: true });
});

function writeFixture(filename: string, contents: string): string {
  const fullPath = path.join(fixtureDir, filename);
  fs.writeFileSync(fullPath, contents, "utf8");
  return fullPath;
}

const captainFixture = (mnemonic: string, role: string): string =>
  `---
name: CAPTAIN_${mnemonic}
description: "Test captain ${mnemonic}."
tools: Read, Write, Bash
model: sonnet
---

# CAPTAIN_${mnemonic} — ${role}

| | |
|---|---|
| **Rank** | CAPTAIN |
| **Mnemonic** | ${mnemonic} |
| **Descriptive role** | ${role} |

Body prose for the test fixture. First paragraph after the table.
`;

const majorFixture = (mnemonic: string, role: string): string =>
  `# MAJOR_${mnemonic} — ${role}

| | |
|---|---|
| **Rank** | MAJOR |
| **Mnemonic** | ${mnemonic} |
| **Descriptive role** | ${role} |

Body prose for the test fixture.
`;

// ---------------------------------------------------------------------------
// discoverRoleFiles
// ---------------------------------------------------------------------------

describe("discoverRoleFiles", () => {
  it("finds MAJOR and CAPTAIN files and ignores everything else", () => {
    writeFixture("MAJOR_TEST.md", majorFixture("TEST", "ARCHITECT"));
    writeFixture("CAPTAIN_TEST.md", captainFixture("TEST", "EXECUTOR"));
    writeFixture("README.md", "# not a role file");
    writeFixture("ONBOARDING.md", "# also not a role file");
    writeFixture("CAPTAIN_lowercase.md", "should not match — must be UPPER");

    const files = discoverRoleFiles(fixtureDir);

    expect(files).toHaveLength(2);
    expect(files.map((f) => f.filename).sort()).toEqual([
      "CAPTAIN_TEST.md",
      "MAJOR_TEST.md",
    ]);
  });

  it("returns role files sorted by filename for deterministic ordering", () => {
    writeFixture("CAPTAIN_ZULU.md", captainFixture("ZULU", "ZULUER"));
    writeFixture("CAPTAIN_ALPHA.md", captainFixture("ALPHA", "ALPHAER"));
    writeFixture("MAJOR_BRAVO.md", majorFixture("BRAVO", "BRAVOER"));

    const files = discoverRoleFiles(fixtureDir);
    expect(files.map((f) => f.filename)).toEqual([
      "CAPTAIN_ALPHA.md",
      "CAPTAIN_ZULU.md",
      "MAJOR_BRAVO.md",
    ]);
  });

  it("throws a descriptive error when the substrate directory does not exist", () => {
    const missing = path.join(fixtureDir, "does-not-exist");
    expect(() => discoverRoleFiles(missing)).toThrow(
      /Substrate directory not found/,
    );
  });
});

// ---------------------------------------------------------------------------
// extractDescriptiveRole
// ---------------------------------------------------------------------------

describe("extractDescriptiveRole", () => {
  it("pulls the descriptive role from the header table", () => {
    const body = `| | |
|---|---|
| **Rank** | CAPTAIN |
| **Mnemonic** | TEST |
| **Descriptive role** | EXECUTOR |
`;
    expect(extractDescriptiveRole(body, "test.md")).toBe("EXECUTOR");
  });

  it("throws when no descriptive role row exists", () => {
    const body = "no header table here";
    expect(() => extractDescriptiveRole(body, "test.md")).toThrow(
      /could not find a "\| \*\*Descriptive role\*\*/,
    );
  });
});

// ---------------------------------------------------------------------------
// buildAgent
// ---------------------------------------------------------------------------

describe("buildAgent", () => {
  it("produces a v2 Agent record from a CAPTAIN file", () => {
    const fullPath = writeFixture(
      "CAPTAIN_TEST.md",
      captainFixture("TEST", "EXECUTOR"),
    );
    const file: RoleFile = {
      filename: "CAPTAIN_TEST.md",
      fullPath,
      rank: "CAPTAIN",
      mnemonic: "TEST",
    };

    const agent = buildAgent(file);

    expect(agent.rank).toBe("CAPTAIN");
    expect(agent.mnemonic).toBe("TEST");
    expect(agent.descriptiveRole).toBe("EXECUTOR");
    expect(agent.filename).toBe("CAPTAIN_TEST.md");
    expect(agent.tools).toEqual(["Read", "Write", "Bash"]);
    expect(agent.modelTier).toBe("sonnet");
    expect(agent.body).toContain("Body prose for the test fixture");
  });

  it("produces a v2 Agent record from a MAJOR file (no frontmatter)", () => {
    const fullPath = writeFixture(
      "MAJOR_TEST.md",
      majorFixture("TEST", "ARCHITECT"),
    );
    const file: RoleFile = {
      filename: "MAJOR_TEST.md",
      fullPath,
      rank: "MAJOR",
      mnemonic: "TEST",
    };

    const agent = buildAgent(file);

    expect(agent.rank).toBe("MAJOR");
    expect(agent.mnemonic).toBe("TEST");
    expect(agent.descriptiveRole).toBe("ARCHITECT");
    expect(agent.tools).toEqual([]);
    expect(agent.modelTier).toBeUndefined();
  });

  it("rejects a CAPTAIN file with malformed frontmatter (missing required field)", () => {
    const malformed = `---
description: "missing the name field entirely"
tools: Read
---

# CAPTAIN_BROKEN — TEST

| | |
|---|---|
| **Rank** | CAPTAIN |
| **Descriptive role** | TEST |
`;
    const fullPath = writeFixture("CAPTAIN_BROKEN.md", malformed);
    const file: RoleFile = {
      filename: "CAPTAIN_BROKEN.md",
      fullPath,
      rank: "CAPTAIN",
      mnemonic: "BROKEN",
    };

    expect(() => buildAgent(file)).toThrow(
      /CAPTAIN_BROKEN\.md.*frontmatter validation failed/s,
    );
  });

  it("rejects a CAPTAIN file with the wrong type for `tools`", () => {
    const malformed = `---
name: CAPTAIN_BROKEN
description: "tools should not be a number"
tools: 42
---

# CAPTAIN_BROKEN — TEST

| | |
|---|---|
| **Rank** | CAPTAIN |
| **Descriptive role** | TEST |
`;
    const fullPath = writeFixture("CAPTAIN_BROKEN.md", malformed);
    const file: RoleFile = {
      filename: "CAPTAIN_BROKEN.md",
      fullPath,
      rank: "CAPTAIN",
      mnemonic: "BROKEN",
    };

    expect(() => buildAgent(file)).toThrow(/frontmatter validation failed/);
  });

  it("rejects a MAJOR file that has unexpected frontmatter (drift detection)", () => {
    const drifted = `---
unexpected: "MAJORs are not supposed to carry frontmatter"
---

# MAJOR_DRIFT — TEST

| | |
|---|---|
| **Descriptive role** | TEST |
`;
    const fullPath = writeFixture("MAJOR_DRIFT.md", drifted);
    const file: RoleFile = {
      filename: "MAJOR_DRIFT.md",
      fullPath,
      rank: "MAJOR",
      mnemonic: "DRIFT",
    };

    expect(() => buildAgent(file)).toThrow(
      /MAJOR role files are not expected to carry YAML frontmatter/,
    );
  });

  it("rejects a file whose body has no `Descriptive role` row", () => {
    const noRole = `---
name: CAPTAIN_NOROLE
description: "no role row in body"
tools: Read
---

# CAPTAIN_NOROLE

just prose, no header table at all
`;
    const fullPath = writeFixture("CAPTAIN_NOROLE.md", noRole);
    const file: RoleFile = {
      filename: "CAPTAIN_NOROLE.md",
      fullPath,
      rank: "CAPTAIN",
      mnemonic: "NOROLE",
    };

    expect(() => buildAgent(file)).toThrow(
      /could not find a "\| \*\*Descriptive role\*\*/,
    );
  });
});

// ---------------------------------------------------------------------------
// assembleStoaData
// ---------------------------------------------------------------------------

describe("assembleStoaData", () => {
  it("produces a roster with the v2 5-rank ladder in canonical order", () => {
    const data = assembleStoaData([]);

    expect(data.roster.map((slot) => slot.rank)).toEqual([
      "HUMAN",
      "COLONEL",
      "MAJOR",
      "CAPTAIN",
      "LIEUTENANT",
    ]);
  });

  it("renders the COLONEL slot as reserved with no agents", () => {
    const data = assembleStoaData([]);
    const colonel = data.roster.find((s) => s.rank === "COLONEL")!;

    expect(colonel).toBeDefined();
    expect((colonel as { reserved?: boolean }).reserved).toBe(true);
    expect(colonel.agents).toEqual([]);
  });

  it("seeds a single anonymous PRINCIPAL in the HUMAN slot", () => {
    const data = assembleStoaData([]);
    const human = data.roster.find((s) => s.rank === "HUMAN")!;

    expect(human.agents).toHaveLength(1);
    expect(human.agents[0]).toEqual({
      rank: "HUMAN",
      descriptiveRole: "PRINCIPAL",
    });
  });

  it("partitions input agents into MAJOR and CAPTAIN slots", () => {
    const major = {
      rank: "MAJOR" as const,
      mnemonic: "TEST",
      descriptiveRole: "ARCHITECT",
      body: "",
      tools: [],
      filename: "MAJOR_TEST.md",
    };
    const captain = {
      rank: "CAPTAIN" as const,
      mnemonic: "TEST",
      descriptiveRole: "EXECUTOR",
      body: "",
      tools: ["Read"],
      filename: "CAPTAIN_TEST.md",
    };

    const data = assembleStoaData([major, captain]);

    expect(data.roster.find((s) => s.rank === "MAJOR")?.agents).toEqual([major]);
    expect(data.roster.find((s) => s.rank === "CAPTAIN")?.agents).toEqual([captain]);
    expect(data.roster.find((s) => s.rank === "LIEUTENANT")?.agents).toEqual([]);
  });

  it("produces output that validates against stoaDataV2Schema", () => {
    const data = assembleStoaData([]);
    const result = stoaDataV2Schema.safeParse(data);
    expect(result.success).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// emitTypeScript
// ---------------------------------------------------------------------------

describe("emitTypeScript", () => {
  it("emits a header with the regen command and source-of-truth note", () => {
    const out = emitTypeScript(assembleStoaData([]));
    expect(out).toContain("AUTO-GENERATED");
    expect(out).toContain("npm run gen-data");
    expect(out).toContain("Source of truth");
  });

  it("does not include a timestamp in the header (stoa--b3f)", () => {
    const out = emitTypeScript(assembleStoaData([]));
    expect(out).not.toMatch(/Generated:/);
    // ISO-8601 timestamp guard: `YYYY-MM-DDTHH:MM:SS...`
    expect(out).not.toMatch(/\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/);
  });

  it("is byte-deterministic across calls with the same input", () => {
    const data = assembleStoaData([]);
    const a = emitTypeScript(data);
    const b = emitTypeScript(data);
    expect(a).toBe(b);
  });
});

// ---------------------------------------------------------------------------
// generate (full pipeline)
// ---------------------------------------------------------------------------

describe("generate", () => {
  it("runs the full pipeline against a synthetic substrate and writes a valid file", () => {
    writeFixture("MAJOR_TEST.md", majorFixture("TEST", "ARCHITECT"));
    writeFixture("CAPTAIN_TEST.md", captainFixture("TEST", "EXECUTOR"));

    const outputPath = path.join(fixtureDir, "out", "agents.ts");
    const summary = generate({ substratePath: fixtureDir, outputPath });

    expect(summary).toEqual({
      fileCount: 2,
      majorCount: 1,
      captainCount: 1,
    });

    const written = fs.readFileSync(outputPath, "utf8");
    expect(written).toContain("AUTO-GENERATED");
    expect(written).toContain('"rank": "MAJOR"');
    expect(written).toContain('"rank": "CAPTAIN"');
  });

  it("is byte-idempotent: re-running with the same substrate yields identical output", () => {
    writeFixture("CAPTAIN_TEST.md", captainFixture("TEST", "EXECUTOR"));
    const outputPath = path.join(fixtureDir, "out", "agents.ts");

    generate({ substratePath: fixtureDir, outputPath });
    const first = fs.readFileSync(outputPath, "utf8");

    generate({ substratePath: fixtureDir, outputPath });
    const second = fs.readFileSync(outputPath, "utf8");

    expect(second).toBe(first);
  });

  it("throws when the substrate has no role files", () => {
    expect(() =>
      generate({
        substratePath: fixtureDir,
        outputPath: path.join(fixtureDir, "out", "agents.ts"),
      }),
    ).toThrow(/no MAJOR_\*\.md or CAPTAIN_\*\.md files found/);
  });
});

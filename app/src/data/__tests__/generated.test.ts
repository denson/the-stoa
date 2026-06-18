// Shape-invariant tests for the generated agents.ts module — sanity check
// that the gen-data adapter produced the v2 5-rank ladder we expect from
// the canonical substrate. Catches regressions if a substrate role file is
// accidentally deleted, duplicated, or renamed without updating the rest
// of the system.

import { describe, it, expect } from "vitest";
import { stoaData } from "../generated/agents";
import { stoaDataV2Schema } from "../../../scripts/schemas";
import type { Agent, RosterSlot } from "../types-v2";

describe("the generated v2 roster", () => {
  it("exposes all five ranks in canonical top-to-bottom order", () => {
    expect(stoaData.roster.map((slot) => slot.rank)).toEqual([
      "HUMAN",
      "COLONEL",
      "MAJOR",
      "CAPTAIN",
      "LIEUTENANT",
    ]);
  });

  it("validates against stoaDataV2Schema", () => {
    const result = stoaDataV2Schema.safeParse(stoaData);
    if (!result.success) {
      throw new Error(
        "generated stoaData failed schema validation:\n" +
          JSON.stringify(result.error.issues, null, 2),
      );
    }
    expect(result.success).toBe(true);
  });

  it("seats one anonymous PRINCIPAL in the HUMAN slot", () => {
    const human = slotFor("HUMAN");
    if (human.rank !== "HUMAN") throw new Error("HUMAN slot discriminator wrong");
    expect(human.agents).toHaveLength(1);
    expect(human.agents[0]).toEqual({
      rank: "HUMAN",
      descriptiveRole: "PRINCIPAL",
    });
  });

  it("renders the COLONEL slot as reserved-empty (planning v2 §2)", () => {
    const colonel = slotFor("COLONEL");
    if (colonel.rank !== "COLONEL") throw new Error("COLONEL slot discriminator wrong");
    expect(colonel.reserved).toBe(true);
    expect(colonel.agents).toEqual([]);
  });

  it("seats CHIRON, HAMILTON, PLINY, and POLYBIUS at MAJOR rank", () => {
    const slot = slotFor("MAJOR");
    if (slot.rank !== "MAJOR") throw new Error("MAJOR slot discriminator wrong");
    const mnemonics = slot.agents.map((a) => a.mnemonic).sort();
    expect(mnemonics).toEqual(["CHIRON", "HAMILTON", "PLINY", "POLYBIUS"]);
    for (const m of slot.agents) {
      expect(m.rank).toBe("MAJOR");
    }
  });

  it("seats the canonical 12 CAPTAINs", () => {
    const slot = slotFor("CAPTAIN");
    if (slot.rank !== "CAPTAIN") throw new Error("CAPTAIN slot discriminator wrong");
    const mnemonics = slot.agents.map((a) => a.mnemonic).sort();
    expect(slot.agents).toHaveLength(12);
    expect(mnemonics).toEqual([
      "ADA",
      "ARGUS",
      "BARTLEBY",
      "CATO",
      "CURATOR",
      "DAEDALUS",
      "HERALD",
      "NOMOS",
      "STRABO",
      "TIRO",
      "VERA",
      "ZENO",
    ]);
    for (const c of slot.agents) {
      expect(c.rank).toBe("CAPTAIN");
    }
  });

  it("populates the LIEUTENANT slot with at least one skill (Arc 17.1)", () => {
    const slot = slotFor("LIEUTENANT");
    if (slot.rank !== "LIEUTENANT") {
      throw new Error("LIEUTENANT slot rank discriminator did not match");
    }
    // Arc 17.1 made the gen-data adapter read all substrate skills as
    // LIEUTENANTs. (agent-author retired Arc 61; the 2 check skills had their
    // SKILL.md removed in Arc 63 — kept as operator tools under skills/check-*/
    // but no longer rendered as LIEUTENANTs — + gauntlet-setup ported in; net
    // LIEUTENANT churn handled by re-deriving from the dir.)
    // Arc 64 (stoa--p41.2 pass B): save-verdict fully removed (Bash-only module
    // now), and validate-spec + inspect-script-output had their SKILL.md removed
    // (kept as operator-tool check.sh under skills/{validate-spec,inspect-script-
    // output}/, no longer rendered as LIEUTENANTs) — net LIEUTENANT delta -3,
    // re-derived from the dir.
    // Don't over-specify count — substrate may grow more.
    expect(slot.skills.length).toBeGreaterThan(0);
    for (const skill of slot.skills) {
      expect(skill.rank).toBe("LIEUTENANT");
      expect(skill.name).toMatch(/^[a-z][a-z0-9-]*$/); // kebab-case
      expect(skill.description.length).toBeGreaterThan(0);
      expect(skill.body.length).toBeGreaterThan(0);
      expect(skill.filename).toBe("SKILL.md");
    }
  });

  it("gives every agent a non-empty body and a descriptive role", () => {
    const allAgents = stoaData.roster.flatMap((slot) =>
      slot.rank === "MAJOR" || slot.rank === "CAPTAIN"
        ? (slot.agents as Agent[])
        : [],
    );
    for (const agent of allAgents) {
      expect(agent.body.length).toBeGreaterThan(0);
      expect(agent.descriptiveRole).toMatch(/^[A-Z][A-Z0-9_-]*$/);
      expect(agent.filename).toMatch(
        /^(MAJOR|CAPTAIN)_[A-Z][A-Z0-9_-]*\.md$/,
      );
    }
  });
});

function slotFor(rank: RosterSlot["rank"]): RosterSlot {
  const slot = stoaData.roster.find((s) => s.rank === rank);
  if (!slot) throw new Error(`no slot for rank ${rank}`);
  return slot;
}

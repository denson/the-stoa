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
    expect(human.agents).toHaveLength(1);
    expect(human.agents[0]).toEqual({
      rank: "HUMAN",
      descriptiveRole: "PRINCIPAL",
    });
  });

  it("renders the COLONEL slot as reserved-empty (planning v2 §2)", () => {
    const colonel = slotFor("COLONEL");
    expect((colonel as { reserved?: boolean }).reserved).toBe(true);
    expect(colonel.agents).toEqual([]);
  });

  it("seats POLYBIUS and PLINY at MAJOR rank", () => {
    const majors = slotFor("MAJOR").agents as Agent[];
    const mnemonics = majors.map((a) => a.mnemonic).sort();
    expect(mnemonics).toEqual(["PLINY", "POLYBIUS"]);
    for (const m of majors) {
      expect(m.rank).toBe("MAJOR");
    }
  });

  it("seats the canonical 10 CAPTAINs", () => {
    const captains = slotFor("CAPTAIN").agents as Agent[];
    const mnemonics = captains.map((a) => a.mnemonic).sort();
    expect(captains).toHaveLength(10);
    expect(mnemonics).toEqual([
      "ADA",
      "ARGUS",
      "BARTLEBY",
      "CATO",
      "CURATOR",
      "DAEDALUS",
      "HERALD",
      "PLINY",
      "STRABO",
      "VERA",
    ]);
    for (const c of captains) {
      expect(c.rank).toBe("CAPTAIN");
    }
  });

  it("leaves the LIEUTENANT slot empty (skills not yet authored in substrate)", () => {
    expect(slotFor("LIEUTENANT").agents).toEqual([]);
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

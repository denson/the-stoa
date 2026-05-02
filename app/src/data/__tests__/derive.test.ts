// Tests for the body-first-paragraph synthesis helper (Arc 12) — the
// substitute for an Agent.description field that types-v2 doesn't yet
// carry. Components consume `deriveRoleSummary` to render the role blurb
// on agent cards, so the contract is small but load-bearing for display.

import { describe, it, expect } from "vitest";
import { deriveRoleSummary, agentSlug } from "../derive";
import type { Agent } from "../types-v2";

// ---------------------------------------------------------------------------
// deriveRoleSummary
// ---------------------------------------------------------------------------

describe("deriveRoleSummary", () => {
  it("returns the first prose paragraph after the header table", () => {
    const body = `# CAPTAIN_TEST — EXECUTOR

| | |
|---|---|
| **Rank** | CAPTAIN |
| **Mnemonic** | TEST |
| **Descriptive role** | EXECUTOR |

You are CAPTAIN_TEST, the EXECUTOR. This is the first paragraph.

This is the second paragraph and should not appear.
`;
    expect(deriveRoleSummary(body)).toBe(
      "You are CAPTAIN_TEST, the EXECUTOR. This is the first paragraph.",
    );
  });

  it("collapses a multi-line first paragraph into a single space-joined string", () => {
    const body = `| **Descriptive role** | TEST |

Line one of the paragraph.
Line two of the same paragraph.
Line three of the same paragraph.

Second paragraph follows.
`;
    expect(deriveRoleSummary(body)).toBe(
      "Line one of the paragraph. Line two of the same paragraph. Line three of the same paragraph.",
    );
  });

  it("stops at a horizontal rule (---) after the first paragraph", () => {
    const body = `| **Descriptive role** | TEST |

The descriptive paragraph.

---

## A new section follows
`;
    expect(deriveRoleSummary(body)).toBe("The descriptive paragraph.");
  });

  it("stops at a section heading (##) after the first paragraph", () => {
    const body = `| **Descriptive role** | TEST |

The descriptive paragraph.

## Section heading
`;
    expect(deriveRoleSummary(body)).toBe("The descriptive paragraph.");
  });

  it("returns an empty string when the body has no header table", () => {
    const body = "just prose with no table at all";
    expect(deriveRoleSummary(body)).toBe("");
  });

  it("returns an empty string when nothing follows the header table", () => {
    const body = `| **Descriptive role** | TEST |
`;
    expect(deriveRoleSummary(body)).toBe("");
  });

  it("returns an empty string for an empty body", () => {
    expect(deriveRoleSummary("")).toBe("");
  });

  it("ignores leading H1 headings (the role-file title line)", () => {
    const body = `# CAPTAIN_TEST — EXECUTOR

| **Descriptive role** | EXECUTOR |

This is the actual role summary.
`;
    expect(deriveRoleSummary(body)).toBe("This is the actual role summary.");
  });

  it("handles CRLF line endings (Windows-authored files)", () => {
    const body =
      "| **Descriptive role** | TEST |\r\n\r\nFirst paragraph on Windows.\r\n\r\nSecond paragraph.";
    expect(deriveRoleSummary(body)).toBe("First paragraph on Windows.");
  });
});

// ---------------------------------------------------------------------------
// agentSlug
// ---------------------------------------------------------------------------

describe("agentSlug", () => {
  it("strips the trailing .md from an agent's canonical filename", () => {
    const agent: Agent = {
      rank: "CAPTAIN",
      mnemonic: "ADA",
      descriptiveRole: "EXECUTOR",
      body: "",
      tools: [],
      filename: "CAPTAIN_ADA.md",
    };
    expect(agentSlug(agent)).toBe("CAPTAIN_ADA");
  });

  it("leaves a filename without the .md suffix unchanged", () => {
    const agent: Agent = {
      rank: "MAJOR",
      mnemonic: "PLINY",
      descriptiveRole: "ORCHESTRATOR",
      body: "",
      tools: [],
      filename: "MAJOR_PLINY",
    };
    expect(agentSlug(agent)).toBe("MAJOR_PLINY");
  });
});

// Zod schemas for the gen-data adapter.
//
// Two layers:
//   1. `frontmatterSchema` — validates raw YAML frontmatter pulled out of a
//      CAPTAIN_*.md file. MAJOR_*.md files have no frontmatter (their identity
//      is in the body), so this schema is only applied to CAPTAINs.
//   2. The output schemas (`agentSchema`, `humanSchema`, `*SlotSchema`,
//      `stoaDataV2Schema`) — mirror the TypeScript types in
//      `app/src/data/types-v2.ts` and validate the assembled `StoaDataV2`
//      object before it is serialized to disk.
//
// `types-v2.ts` is canonical (Arc 9 is upstream of Arc 10); these schemas
// mirror those types. If they drift, the TS types win and the schemas get
// updated — not the other way around.

import { z } from "zod";

// ---------------------------------------------------------------------------
// Frontmatter (raw CAPTAIN role file YAML)
// ---------------------------------------------------------------------------

/**
 * Normalize a tools value into a string[]. YAML parses
 * `tools: Bash, Read, Grep, Glob` as a single comma-joined string;
 * a future role file might use proper YAML list syntax (`[Bash, Read]`)
 * which gray-matter parses as an array. Accept both.
 */
const toolsField = z
  .union([z.string(), z.array(z.string())])
  .transform((value) =>
    Array.isArray(value)
      ? value.map((tool) => tool.trim()).filter((tool) => tool.length > 0)
      : value
          .split(",")
          .map((tool) => tool.trim())
          .filter((tool) => tool.length > 0),
  );

export const frontmatterSchema = z.object({
  name: z.string().min(1),
  description: z.string().min(1),
  tools: toolsField,
  model: z.string().min(1).optional(),
});

export type Frontmatter = z.infer<typeof frontmatterSchema>;

// ---------------------------------------------------------------------------
// Output: rank + agent + human (mirrors types-v2.ts)
// ---------------------------------------------------------------------------

export const rankSchema = z.enum([
  "HUMAN",
  "COLONEL",
  "MAJOR",
  "CAPTAIN",
  "LIEUTENANT",
]);

export const agentRankSchema = z.enum([
  "COLONEL",
  "MAJOR",
  "CAPTAIN",
  "LIEUTENANT",
]);

/**
 * Mnemonic and descriptive-role tokens are uppercase ASCII. The spec
 * (planning v2 §3) uses both kebab-case (`CHIEF-OF-STAFF`) and underscore
 * (`FILE_CLERK`) forms in canonical examples, so the regex permits both.
 */
const upperToken = /^[A-Z][A-Z0-9_-]*$/;

export const agentSchema = z.object({
  rank: agentRankSchema,
  mnemonic: z.string().regex(upperToken),
  descriptiveRole: z.string().regex(upperToken),
  body: z.string(),
  tools: z.array(z.string()),
  filename: z.string().min(1),
  projectScope: z.string().optional(),
  callableLieutenants: z.array(z.string()).optional(),
  requiredReading: z.array(z.string()).optional(),
  modelTier: z.string().optional(),
});

export const humanSchema = z.object({
  rank: z.literal("HUMAN"),
  name: z.string().optional(),
  descriptiveRole: z.literal("PRINCIPAL"),
});

// ---------------------------------------------------------------------------
// Output: slots (mirrors types-v2.ts RosterSlot discriminated union)
// ---------------------------------------------------------------------------

export const humanSlotSchema = z.object({
  rank: z.literal("HUMAN"),
  reserved: z.literal(false).optional(),
  agents: z.array(humanSchema),
});

export const colonelSlotSchema = z.object({
  rank: z.literal("COLONEL"),
  reserved: z.literal(true),
  agents: z.tuple([]),
});

export const agentSlotSchema = z.object({
  rank: z.enum(["MAJOR", "CAPTAIN", "LIEUTENANT"]),
  reserved: z.literal(false).optional(),
  agents: z.array(agentSchema),
});

export const rosterSlotSchema = z.union([
  humanSlotSchema,
  colonelSlotSchema,
  agentSlotSchema,
]);

export const stoaDataV2Schema = z.object({
  roster: z.array(rosterSlotSchema),
});

export type StoaDataV2Schema = z.infer<typeof stoaDataV2Schema>;

// One-line role summary derived from a v2 Agent's body (planning v2 §11).
//
// Components consume this to render the role blurb on agent cards and
// detail pages. Lifted from Arc 11's sample.ts shim per Arc 12's Colonel
// call (description-field option b): body-first-paragraph synthesis is
// canonical until/unless `Agent.description` is added to types-v2.

import type { Agent } from "./types-v2";

/**
 * Returns the first prose paragraph that follows the role file's header
 * table (the rank/mnemonic/role/lives-at table at the top of every role
 * file). Falls back to an empty string if no such paragraph exists.
 *
 * The natural v2 source for this would be a frontmatter `description`
 * field on Agent; that field doesn't exist yet (Arc 10 hand-back §1,
 * deferred — Arc 12 Colonel call confirmed the synthesis path).
 */
export function deriveRoleSummary(body: string): string {
  const lines = body.split(/\r?\n/);
  let sawTable = false;
  let inTable = false;
  const paragraph: string[] = [];
  for (const raw of lines) {
    const line = raw.trim();
    if (line.startsWith("# ")) continue;
    if (line.startsWith("|")) {
      sawTable = true;
      inTable = true;
      continue;
    }
    if (inTable && line === "") {
      inTable = false;
      continue;
    }
    if (!sawTable) continue;
    if (line === "") {
      if (paragraph.length > 0) break;
      continue;
    }
    if (line.startsWith("---") || line.startsWith("##")) {
      if (paragraph.length > 0) break;
      continue;
    }
    paragraph.push(line);
  }
  return paragraph.join(" ");
}

/**
 * Convenience: agent slug used as URL segment + roster identifier.
 * Strips the trailing `.md` from the canonical filename.
 */
export function agentSlug(agent: Agent): string {
  return agent.filename.replace(/\.md$/, "");
}

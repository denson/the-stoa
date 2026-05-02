// Descriptive-role accent colors, keyed by v2 Agent.descriptiveRole strings.
//
// v2 retires the v1 archetype enum (Arc 11 hand-back #1); this module
// replaces the v1 archetype color map. Each entry is a [light, dark]
// pair, matched by useTheme() at render time (mirrors the old archColors
// shape so the Components.tsx call sites stay simple).
//
// Coverage: every descriptiveRole present in the current v2 substrate
// roster has an explicit entry. New roles fall back to a neutral
// gray-ink pair so the display never crashes on unknown values.

const NEUTRAL: [string, string] = ["#76736B", "#A6A39B"];

/**
 * Light/dark color pair for each known descriptive role.
 *
 * The role names are in canonical SCREAMING-KEBAB-CASE per types-v2.ts.
 * Most roles inherit colors from the v1 archetype palette; three new v2
 * roles (CHIEF-OF-STAFF, FILE_CLERK, SPEC-CHECKER) get distinct hues so
 * agents at the same rank but different jobs read apart at a glance.
 * PRINCIPAL gets a warm gold accent that matches the HUMAN-rank treatment.
 */
export const roleColors: Record<string, [string, string]> = {
  PRINCIPAL:        ["#8A6B2C", "#D9B96A"],   // gold-ink — matches HUMAN rank pill
  ORCHESTRATOR:     ["#5B4D86", "#9D8FCB"],
  "CHIEF-OF-STAFF": ["#3E5078", "#8FA3CB"],   // cool-blue, distinct from ORCHESTRATOR
  ARCHITECT:        ["#2E6E63", "#6FB5A8"],
  "PLAN-CRITIC":    ["#6E4A2E", "#C29A75"],
  EXECUTOR:         ["#4A6E2E", "#8FB575"],
  VERIFIER:         ["#785637", "#C29A75"],
  REVIEWER:         ["#6E2E4A", "#C7889F"],
  "SPEC-CHECKER":   ["#8C3F5C", "#D49AB0"],   // pink-rose, kin to REVIEWER
  SCOUT:            ["#2E6E4A", "#75C29A"],
  FILE_CLERK:       ["#4A6E78", "#8FB5C2"],   // teal-gray, kin to SCOUT
  INTAKE:           ["#6E6E2E", "#C2C275"],
  SYNTHESIST:       ["#4A2E6E", "#A88FCB"],
};

export function roleColorFor(descriptiveRole: string, dark: boolean): string {
  const pair = roleColors[descriptiveRole] ?? NEUTRAL;
  return pair[dark ? 1 : 0];
}

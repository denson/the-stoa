// Reusable UI components for The Stoa. Inline styles are preserved for design
// fidelity (matching the hifi prototype pixel-perfectly per the handoff README);
// a future arc may refactor to CSS modules or Tailwind.
//
// Color sourcing: every theme-aware color comes from a CSS variable defined in
// src/styles/tokens.css. Dark mode toggles via :root[data-theme="dark"] alone.
// The role accent colors (per descriptiveRole, light/dark pair) live in JS —
// see src/data/colors.ts.
//
// ---------------------------------------------------------------------------
// data-testid naming convention (acb-008, updated for v2 vocabulary in Arc 12)
// ---------------------------------------------------------------------------
// Every load-bearing interactive surface in the app carries a `data-testid`
// attribute under one consistent rule so downstream Claude Code skill
// consumers (Chrome MCP scripts, future component tests) can target elements
// deterministically without DOM-scraping inline styles.
//
//   Convention: kebab-case; entity-then-id; identifiers preserved as-is.
//
//   • Static surfaces use the entity name alone: `theme-toggle`,
//     `new-agent-button`, `settings-button`, `search-trigger`, `palette-input`,
//     `back-to-team`, `filter-clear`, `colonel-reserved-card`.
//   • Dynamic surfaces append the identifier verbatim — agent slugs
//     (filename minus `.md`, e.g. `MAJOR_PLINY`, `CAPTAIN_ADA`) are NOT
//     re-cased: `agent-card-MAJOR_PLINY`, `skill-card-format-validate`,
//     `meta-card-fix-now-discipline`, `tab-team`, `filter-role-EXECUTOR`,
//     `lieutenant-chip-LINT_YAML`, `human-card-PRINCIPAL`.
//   • Palette result rows disambiguate by entity type:
//     `palette-result-agent-{slug}` vs `palette-result-skill-{name}`.
//
// Migration note (Arc 12): v1 testids `officer-card-*` and
// `filter-archetype-*` were renamed to `agent-card-*` and `filter-role-*`
// to match v2 vocabulary; the descriptive-role identifier is the v2 string
// (SCREAMING-KEBAB-CASE, e.g. `EXECUTOR`, `CHIEF-OF-STAFF`), not the v1
// archetype enum (lowercase `executor`).

import { useState } from "react";
import {
  Search,
  Edit,
  Copy,
  Code,
  Plus,
  ArrowRight,
  X,
  Filter,
  Settings,
  Check,
  FileText,
  Package,
  Users,
  Sun,
  Moon,
} from "lucide-react";
import type { LucideProps } from "lucide-react";
import type { Agent, Human, Rank } from "./data/types-v2";
import type { Skill } from "./data/display-extras";
import { useTheme } from "./hooks/useTheme";
import { roleColorFor } from "./data/colors";
import { agentSlug, deriveRoleSummary } from "./data/derive";

// ---------------------------------------------------------------------------
// Mark (placeholder logo) — columnar/peristyle motif evoking The Stoa.
// ---------------------------------------------------------------------------
export function Mark({ size = 28 }: { size?: number }) {
  return (
    <svg width={size * 0.5} height={size} viewBox="0 0 64 96" style={{ color: "var(--fg-1)" }}>
      <g fill="currentColor">
        <rect x="6" y="14" width="52" height="6" />
        <path d="M10 20 Q10 24 14 24 L50 24 Q54 24 54 20 Z" />
        <rect x="16" y="24" width="32" height="56" />
        <rect x="12" y="80" width="40" height="4" />
        <rect x="6" y="84" width="52" height="6" />
      </g>
    </svg>
  );
}

// ---------------------------------------------------------------------------
// Button
// ---------------------------------------------------------------------------
type ButtonVariant = "primary" | "secondary" | "ghost" | "danger";
type ButtonSize = "sm" | "md" | "lg";

interface ButtonProps {
  variant?: ButtonVariant;
  size?: ButtonSize;
  children: React.ReactNode;
  onClick?: () => void;
  leading?: React.ReactNode;
  style?: React.CSSProperties;
}

export function Button({
  variant = "primary",
  size = "md",
  children,
  onClick,
  leading,
  style = {},
}: ButtonProps) {
  const base: React.CSSProperties = {
    fontFamily: "Inter, sans-serif",
    fontWeight: 500,
    borderRadius: 6,
    cursor: "pointer",
    lineHeight: 1.2,
    border: "1px solid transparent",
    display: "inline-flex",
    alignItems: "center",
    gap: 6,
    transition: "all 180ms",
  };
  const sizes: Record<ButtonSize, React.CSSProperties> = {
    sm: { fontSize: 12, padding: "4px 10px" },
    md: { fontSize: 13, padding: "7px 13px" },
    lg: { fontSize: 14, padding: "9px 16px" },
  };
  // Note: `--fg-on-accent` is reused for the danger variant. Per ARGUS F4 /
  // design §0.6 disposition #4: semantically the token is named for accent
  // buttons, but the visual impact on danger is sub-perceptible (light
  // `#FFFFFF` is byte-identical; dark `#FAF9F6` is near-white on saturated
  // danger-red). If a future arc adds `--fg-on-danger`, the swap is one-line.
  const variants: Record<ButtonVariant, React.CSSProperties> = {
    primary: { background: "var(--accent)", color: "var(--fg-on-accent)", borderColor: "var(--accent)" },
    secondary: { background: "transparent", color: "var(--fg-1)", borderColor: "var(--border-2)" },
    ghost: { background: "transparent", color: "var(--fg-1)" },
    danger: { background: "var(--danger)", color: "var(--fg-on-accent)", borderColor: "var(--danger)" },
  };
  return (
    <button onClick={onClick} style={{ ...base, ...sizes[size], ...variants[variant], ...style }}>
      {leading}
      {children}
    </button>
  );
}

// ---------------------------------------------------------------------------
// Theme toggle — sun/moon icon button. Shows the *target* mode (currently dark
// renders <Sun/> meaning "click to go light"). Matches the JSX prototype.
// ---------------------------------------------------------------------------
export function ThemeToggle() {
  const { dark, toggle } = useTheme();
  return (
    <button
      data-testid="theme-toggle"
      onClick={toggle}
      title={dark ? "Switch to light" : "Switch to dark"}
      style={{
        background: "transparent",
        border: "1px solid var(--border-1)",
        borderRadius: 6,
        padding: "5px 8px",
        cursor: "pointer",
        color: "var(--fg-2)",
        display: "inline-flex",
        alignItems: "center",
      }}
    >
      {dark ? <Sun size={14} /> : <Moon size={14} />}
    </button>
  );
}

// ---------------------------------------------------------------------------
// Rank pill — covers all five v2 ranks (planning v2 §2). Border tokens added
// in acb-001 (MAJOR/CAPTAIN/LIEUTENANT) and Arc 12 (HUMAN/COLONEL) preserve
// the warm-tint per-rank coding.
// ---------------------------------------------------------------------------
const rankStyles: Record<Rank, { bg: string; fg: string; border: string }> = {
  HUMAN:      { bg: "var(--rank-human-bg)",      fg: "var(--rank-human)",      border: "var(--rank-human-border)" },
  COLONEL:    { bg: "var(--rank-colonel-bg)",    fg: "var(--rank-colonel)",    border: "var(--rank-colonel-border)" },
  MAJOR:      { bg: "var(--rank-major-bg)",      fg: "var(--rank-major)",      border: "var(--rank-major-border)" },
  CAPTAIN:    { bg: "var(--rank-captain-bg)",    fg: "var(--rank-captain)",    border: "var(--rank-captain-border)" },
  LIEUTENANT: { bg: "var(--rank-lieutenant-bg)", fg: "var(--rank-lieutenant)", border: "var(--rank-lieutenant-border)" },
};

export function RankPill({ rank }: { rank: Rank }) {
  const s = rankStyles[rank];
  return (
    <span
      style={{
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: 10,
        fontWeight: 600,
        letterSpacing: "0.06em",
        textTransform: "uppercase",
        padding: "2px 7px",
        borderRadius: 999,
        border: `1px solid ${s.border}`,
        background: s.bg,
        color: s.fg,
        whiteSpace: "nowrap",
      }}
    >
      {rank}
    </span>
  );
}

// ---------------------------------------------------------------------------
// Role text label — renders the agent's descriptiveRole as a small accent.
// Replaces v1's ArchetypeText: the v2 descriptiveRole supersedes the v1
// archetype enum (Arc 11 hand-back #1, Arc 12 retirement).
// ---------------------------------------------------------------------------
export function RoleText({ role }: { role: string }) {
  const { dark } = useTheme();
  const color = roleColorFor(role, dark);
  return (
    <span
      style={{
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: 10.5,
        color,
        textTransform: "lowercase",
      }}
    >
      {role.toLowerCase()}-role
    </span>
  );
}

// ---------------------------------------------------------------------------
// Chip — skill variant uses --accent-soft-border; meta variant consolidates
// onto accent-soft-2 / fg-1 / border-2 (design §0.5 Lock 2).
// ---------------------------------------------------------------------------
type ChipVariant = "tool" | "skill" | "meta";

const chipVariants: Record<ChipVariant, { bg: string; fg: string; border: string }> = {
  tool: { bg: "var(--bg-inset)", fg: "var(--fg-2)", border: "var(--border-1)" },
  skill: { bg: "var(--accent-soft)", fg: "var(--accent)", border: "var(--accent-soft-border)" },
  meta: { bg: "var(--accent-soft-2)", fg: "var(--fg-1)", border: "var(--border-2)" },
};

export function Chip({
  children,
  variant = "tool",
  onClick,
}: {
  children: React.ReactNode;
  variant?: ChipVariant;
  onClick?: () => void;
}) {
  const v = chipVariants[variant];
  return (
    <span
      onClick={onClick}
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 6,
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: 11,
        fontWeight: 500,
        padding: "3px 9px",
        borderRadius: 4,
        background: v.bg,
        color: v.fg,
        border: `1px solid ${v.border}`,
        cursor: onClick ? "pointer" : "default",
      }}
    >
      {children}
    </span>
  );
}

// ---------------------------------------------------------------------------
// Agent card — replaces v1 OfficerCard. Consumes v2 Agent directly; the
// one-line role summary is synthesized from agent.body via deriveRoleSummary
// (Arc 12 Colonel-call decision: synthesis path, no description field on
// types-v2). Slug (filename minus `.md`) drives both the testid and the URL.
// ---------------------------------------------------------------------------
export function AgentCard({
  agent,
  onClick,
}: {
  agent: Agent;
  onClick?: () => void;
}) {
  const [hover, setHover] = useState(false);
  const { dark } = useTheme();
  const accent = roleColorFor(agent.descriptiveRole, dark);
  const slug = agentSlug(agent);
  const summary = deriveRoleSummary(agent.body);
  return (
    <div
      data-testid={`agent-card-${slug}`}
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        background: hover ? "var(--bg-inset)" : "var(--bg-surface)",
        border: "1px solid var(--border-1)",
        borderLeft: `3px solid ${accent}`,
        borderRadius: 10,
        padding: "16px 18px 14px",
        cursor: "pointer",
        boxShadow: "var(--shadow-1)",
        display: "flex",
        flexDirection: "column",
        gap: 8,
        transition: "background 180ms",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
        <RankPill rank={agent.rank} />
        <RoleText role={agent.descriptiveRole} />
      </div>
      <div
        style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontWeight: 700,
          fontSize: 14.5,
          letterSpacing: "0.02em",
          color: "var(--fg-1)",
        }}
      >
        {slug}
      </div>
      <div
        style={{
          fontFamily: "Inter, sans-serif",
          fontSize: 12.5,
          color: "var(--fg-2)",
          lineHeight: 1.45,
          textWrap: "pretty",
        }}
      >
        {summary}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Human card — the PRINCIPAL framework (planning v2 §3). Visually distinct
// from agent cards: ink-blue accent stripe, inline "the human served by the
// system" caption, no click target (humans don't have detail pages).
// ---------------------------------------------------------------------------
export function HumanCard({ human }: { human: Human }) {
  const accent = "var(--rank-human)";
  return (
    <div
      data-testid={`human-card-${human.descriptiveRole}`}
      style={{
        background: "var(--bg-surface)",
        border: "1px solid var(--border-1)",
        borderLeft: `3px solid ${accent}`,
        borderRadius: 10,
        padding: "16px 18px 14px",
        boxShadow: "var(--shadow-1)",
        display: "flex",
        flexDirection: "column",
        gap: 8,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
        <RankPill rank="HUMAN" />
        <RoleText role={human.descriptiveRole} />
      </div>
      <div
        style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontWeight: 700,
          fontSize: 14.5,
          letterSpacing: "0.02em",
          color: "var(--fg-1)",
        }}
      >
        {human.name ?? "(name not yet captured)"}
      </div>
      <div
        style={{
          fontFamily: "Inter, sans-serif",
          fontSize: 12.5,
          color: "var(--fg-2)",
          lineHeight: 1.45,
          textWrap: "pretty",
        }}
      >
        The human served by the system. PRINCIPAL is the only role a human
        occupies; agents rank below.
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Reserved-COLONEL card — the empty rank slot (planning v2 §2). COLONEL is
// a reserved future agent rank; no agent currently inhabits it. The card is
// dimmed and non-interactive; the tooltip distinguishes the human PRINCIPAL
// from the reserved agent rank (the v1-vs-v2 vocabulary correction).
// ---------------------------------------------------------------------------
export function ReservedColonelCard() {
  return (
    <div
      data-testid="colonel-reserved-card"
      title="COLONEL is a reserved agent rank (between MAJOR and HUMAN). No agent currently holds it. Distinct from PRINCIPAL, which is the human's role."
      style={{
        background: "var(--bg-sunken)",
        border: "1px dashed var(--border-2)",
        borderRadius: 10,
        padding: "16px 18px 14px",
        boxShadow: "none",
        display: "flex",
        flexDirection: "column",
        gap: 8,
        opacity: 0.75,
        cursor: "help",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
        <RankPill rank="COLONEL" />
      </div>
      <div
        style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontWeight: 600,
          fontSize: 13.5,
          letterSpacing: "0.02em",
          color: "var(--fg-3)",
        }}
      >
        Reserved
      </div>
      <div
        style={{
          fontFamily: "Inter, sans-serif",
          fontSize: 12.5,
          color: "var(--fg-3)",
          lineHeight: 1.45,
          textWrap: "pretty",
        }}
      >
        Reserved for future agent rank — no current inhabitants.
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Skill card
// ---------------------------------------------------------------------------
export function SkillCard({ skill, onClick }: { skill: Skill; onClick?: () => void }) {
  const [hover, setHover] = useState(false);
  return (
    <div
      data-testid={`skill-card-${skill.name}`}
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        background: hover ? "var(--bg-inset)" : "var(--bg-surface)",
        border: "1px solid var(--border-1)",
        borderRadius: 10,
        padding: "16px 18px",
        cursor: "pointer",
        boxShadow: "var(--shadow-1)",
        display: "flex",
        flexDirection: "column",
        gap: 8,
        transition: "background 180ms",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 8, justifyContent: "space-between" }}>
        <div
          style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontWeight: 600,
            fontSize: 14,
            color: "var(--fg-1)",
          }}
        >
          {skill.name}
        </div>
        <span
          style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 10,
            color: "var(--fg-3)",
            textTransform: "uppercase",
            letterSpacing: "0.08em",
          }}
        >
          {skill.kind}
        </span>
      </div>
      <div
        style={{
          fontFamily: "Inter, sans-serif",
          fontSize: 12.5,
          color: "var(--fg-2)",
          lineHeight: 1.45,
          display: "-webkit-box",
          WebkitLineClamp: 3,
          WebkitBoxOrient: "vertical",
          overflow: "hidden",
        }}
      >
        {skill.description}
      </div>
      {skill.callable_by.length > 0 && (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 5, marginTop: 2 }}>
          <span
            style={{
              fontFamily: "Inter, sans-serif",
              fontSize: 10.5,
              color: "var(--fg-3)",
              marginRight: 2,
            }}
          >
            callable by
          </span>
          {skill.callable_by.map((o) => (
            <Chip key={o} variant="tool">
              {o}
            </Chip>
          ))}
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Re-exports for icon components used across the app — Lucide React drop-in
// replacements for the inline SVG `Icon` component in the handoff prototype.
// Maps documented in the handoff README.
// ---------------------------------------------------------------------------
export const icons = {
  search: Search,
  edit: Edit,
  copy: Copy,
  code: Code,
  plus: Plus,
  arrowRight: ArrowRight,
  x: X,
  filter: Filter,
  settings: Settings,
  check: Check,
  file: FileText,
  package: Package,
  users: Users,
  sun: Sun,
  moon: Moon,
} as const;

export type IconProps = LucideProps;

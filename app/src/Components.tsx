// Reusable UI components for The Stoa. Ported from the design handoff bundle's
// Components.jsx. Inline styles are preserved for design fidelity (matching the
// hifi prototype pixel-perfectly per the handoff README); v0.2 may refactor to
// CSS modules or Tailwind.
//
// Color sourcing: every theme-aware color comes from a CSS variable defined in
// src/styles/tokens.css. The old `palette` JS const has been deleted (acb-001);
// dark mode now toggles via :root[data-theme="dark"] alone. Archetype accent
// colors are the only per-mode pair that lives in JS — see `archColors` below.
//
// ---------------------------------------------------------------------------
// data-testid naming convention (acb-008)
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
//     `back-to-team`, `filter-clear`.
//   • Dynamic surfaces append the identifier verbatim — snake-case officer /
//     skill names from the data layer are NOT re-cased: `officer-card-ADA`,
//     `skill-card-format-validate`, `meta-card-fix-now-discipline`,
//     `tab-team`, `filter-archetype-executor`, `lieutenant-chip-LINT_YAML`.
//   • Palette result rows disambiguate by entity type:
//     `palette-result-officer-{name}` vs `palette-result-skill-{name}`.
//
// See agents/specs/acb-008-skill-affordances.md §3 for the canonical table.

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
import type { Officer, Skill, Rank, Archetype } from "./data/types";
import { useTheme } from "./hooks/useTheme";

// ---------------------------------------------------------------------------
// Archetype accent colors — [light, dark] pair per archetype.
// Lives in the components layer (presentation concern, not data). Consumed by
// ArchetypeText, OfficerCard, FilterSidebar via useTheme() + archColorFor().
// data.archetypes (in src/data/sample.ts) keeps the light-only string-per-arch
// shape for the FilterSidebar's archetype enumeration; cleanup deferred to
// acb-002 (per ARGUS F8 disposition).
// ---------------------------------------------------------------------------
export const archColors: Record<Archetype, [string, string]> = {
  orchestrator: ["#5B4D86", "#9D8FCB"],
  architect:    ["#2E6E63", "#6FB5A8"],
  verifier:     ["#785637", "#C29A75"],
  executor:     ["#4A6E2E", "#8FB575"],
  reviewer:     ["#6E2E4A", "#C7889F"],
  "plan-critic":["#6E4A2E", "#C29A75"],
  researcher:   ["#2E4A6E", "#7CA1D4"],
  curator:      ["#4A2E6E", "#A88FCB"],
  intake:       ["#6E6E2E", "#C2C275"],
  scout:        ["#2E6E4A", "#75C29A"],
};

export function archColorFor(archetype: Archetype, dark: boolean): string {
  return archColors[archetype][dark ? 1 : 0];
}

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
// Rank pill — borders use --rank-*-border tokens (added in acb-001 per
// design §0.5 Lock 1) preserving the v0.1 warm-tint per-rank border coding.
// ---------------------------------------------------------------------------
const rankStyles: Record<Rank, { bg: string; fg: string; border: string }> = {
  major: { bg: "var(--rank-major-bg)", fg: "var(--rank-major)", border: "var(--rank-major-border)" },
  captain: { bg: "var(--rank-captain-bg)", fg: "var(--rank-captain)", border: "var(--rank-captain-border)" },
  lieutenant: { bg: "var(--rank-lieutenant-bg)", fg: "var(--rank-lieutenant)", border: "var(--rank-lieutenant-border)" },
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
// Archetype text label
// ---------------------------------------------------------------------------
export function ArchetypeText({ archetype }: { archetype: Archetype }) {
  const { dark } = useTheme();
  const color = archColorFor(archetype, dark);
  return (
    <span
      style={{
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: 10.5,
        color,
        textTransform: "lowercase",
      }}
    >
      {archetype}-archetype
    </span>
  );
}

// ---------------------------------------------------------------------------
// Chip — skill variant uses --accent-soft-border (token added in acb-001 per
// ARGUS F1 disposition) preserving the v0.1 cool-blue accent-family border.
// Meta variant consolidates onto accent-soft-2 / fg-1 / border-2 (Colonel-
// approved, design §0.5 Lock 2).
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
// Officer card
// ---------------------------------------------------------------------------
/**
 * Officer card. Requires a <ThemeProvider> ancestor (consumes useTheme() for
 * archetype color resolution). When v0.3 component tests arrive, wrap with a
 * renderWithTheme helper.
 */
export function OfficerCard({
  officer,
  onClick,
}: {
  officer: Officer;
  onClick?: () => void;
}) {
  const [hover, setHover] = useState(false);
  const { dark } = useTheme();
  const archColor = archColorFor(officer.archetype, dark);
  return (
    <div
      data-testid={`officer-card-${officer.name}`}
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        background: hover ? "var(--bg-inset)" : "var(--bg-surface)",
        border: "1px solid var(--border-1)",
        borderLeft: `3px solid ${archColor}`,
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
        <RankPill rank={officer.rank} />
        <ArchetypeText archetype={officer.archetype} />
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
        {officer.name}
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
        {officer.role}
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

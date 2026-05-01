// Reusable UI components for The Stoa. Ported from the design handoff bundle's
// Components.jsx. Inline styles are preserved for design fidelity (matching the
// hifi prototype pixel-perfectly per the handoff README); v0.2 may refactor to
// CSS modules or Tailwind.

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
} from "lucide-react";
import type { LucideProps } from "lucide-react";
import type { Officer, Skill, Rank, Archetype } from "./data/types";

// ---------------------------------------------------------------------------
// Palette — kept in sync with src/styles/tokens.css. Inline references for
// components that need raw hex values; see tokens.css for CSS-variable usage.
// ---------------------------------------------------------------------------
export const palette = {
  bgApp: "#FAF9F6",
  bgSurface: "#FFFFFF",
  bgSunken: "#F2F0EB",
  bgInset: "#ECE9E1",
  fg1: "#1B1A17",
  fg2: "#45433E",
  fg3: "#76736B",
  fg4: "#A6A39B",
  border1: "#E4E1D8",
  border2: "#D4D0C5",
  border3: "#BFBAAD",
  accent: "#2B4A7F",
  accentHover: "#233C68",
  accentSoft: "#E6EBF3",
  rankMaj: "#8A6B2C",
  rankMajBg: "#F5EBD3",
  rankMajBorder: "#E5D6A8",
  rankCap: "#5C5F66",
  rankCapBg: "#ECEDEF",
  rankCapBorder: "#D9DBDF",
  rankLt: "#8A4A2C",
  rankLtBg: "#F2E2D5",
  rankLtBorder: "#E5C9B3",
} as const;

// ---------------------------------------------------------------------------
// Mark (placeholder logo) — columnar/peristyle motif evoking The Stoa.
// ---------------------------------------------------------------------------
export function Mark({ size = 28 }: { size?: number }) {
  return (
    <svg width={size * 0.5} height={size} viewBox="0 0 64 96" style={{ color: palette.fg1 }}>
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
  const variants: Record<ButtonVariant, React.CSSProperties> = {
    primary: { background: palette.accent, color: "#fff", borderColor: palette.accent },
    secondary: { background: "transparent", color: palette.fg1, borderColor: palette.border2 },
    ghost: { background: "transparent", color: palette.fg1 },
    danger: { background: "#9B3A3A", color: "#fff", borderColor: "#9B3A3A" },
  };
  return (
    <button onClick={onClick} style={{ ...base, ...sizes[size], ...variants[variant], ...style }}>
      {leading}
      {children}
    </button>
  );
}

// ---------------------------------------------------------------------------
// Rank pill
// ---------------------------------------------------------------------------
const rankStyles: Record<Rank, { bg: string; fg: string; border: string }> = {
  major: { bg: palette.rankMajBg, fg: palette.rankMaj, border: palette.rankMajBorder },
  captain: { bg: palette.rankCapBg, fg: palette.rankCap, border: palette.rankCapBorder },
  lieutenant: { bg: palette.rankLtBg, fg: palette.rankLt, border: palette.rankLtBorder },
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
export function ArchetypeText({ archetype, color }: { archetype: Archetype; color: string }) {
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
// Chip
// ---------------------------------------------------------------------------
type ChipVariant = "tool" | "skill" | "meta";

const chipVariants: Record<ChipVariant, { bg: string; fg: string; border: string }> = {
  tool: { bg: palette.bgInset, fg: palette.fg2, border: palette.border1 },
  skill: { bg: palette.accentSoft, fg: palette.accent, border: "#B7C5DA" },
  meta: { bg: "#F1EEF7", fg: "#5B4D86", border: "#E0DAEC" },
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
export function OfficerCard({
  officer,
  archColor,
  onClick,
}: {
  officer: Officer;
  archColor: string;
  onClick?: () => void;
}) {
  const [hover, setHover] = useState(false);
  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        background: hover ? palette.bgApp : palette.bgSurface,
        border: `1px solid ${palette.border1}`,
        borderLeft: `3px solid ${archColor}`,
        borderRadius: 10,
        padding: "16px 18px 14px",
        cursor: "pointer",
        boxShadow: "0 1px 2px rgba(20,18,12,0.04)",
        display: "flex",
        flexDirection: "column",
        gap: 8,
        transition: "background 180ms",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
        <RankPill rank={officer.rank} />
        <ArchetypeText archetype={officer.archetype} color={archColor} />
      </div>
      <div
        style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontWeight: 700,
          fontSize: 14.5,
          letterSpacing: "0.02em",
          color: palette.fg1,
        }}
      >
        {officer.name}
      </div>
      <div
        style={{
          fontFamily: "Inter, sans-serif",
          fontSize: 12.5,
          color: palette.fg2,
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
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        background: hover ? palette.bgApp : palette.bgSurface,
        border: `1px solid ${palette.border1}`,
        borderRadius: 10,
        padding: "16px 18px",
        cursor: "pointer",
        boxShadow: "0 1px 2px rgba(20,18,12,0.04)",
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
            color: palette.fg1,
          }}
        >
          {skill.name}
        </div>
        <span
          style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 10,
            color: palette.fg3,
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
          color: palette.fg2,
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
              color: palette.fg3,
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
} as const;

export type IconProps = LucideProps;

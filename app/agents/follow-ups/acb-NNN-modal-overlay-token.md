# Follow-up: Make modal overlay theme-aware

**Status:** Open. Filed during acb-001-darkmode close-out (2026-05-01).
**Severity:** Low — visually serviceable in both modes; not a regression.
**Suggested ticket id:** `acb-NNN-modal-overlay-token` (assign in next batch).

## Background

`src/App.tsx:801` (`CommandPalette` modal) uses `background: "rgba(20,18,12,0.35)"` as the modal backdrop. This is a warm-paper rgba preserved from v0.1. It does not flow through tokens, so it does not change with `data-theme`.

In dark mode the `backdrop-filter: blur(12px)` carries most of the visual work; the warm-paper tint reads as a slight warm wash over the near-black bg. Acceptable but not ideal — the design.md §3.3 (line 400) explicitly accepted this for acb-001 to keep scope tight. ARGUS / VERA / CATO all flagged it as a follow-up candidate.

Not a §5 #7 violation — the spec post-condition specifies hex literals, not rgba.

## Why deferred (not fixed in acb-001)

- Spec §5 #7 grep post-condition is hex-only; rgba slipped past the contract by design.
- Introducing a new token mid-arc would expand scope post-Colonel-lock.
- Visually serviceable in both modes; not a regression of v0.1.

## Concrete plan

1. Add `--modal-overlay` token to BOTH `:root` (light) and `:root[data-theme="dark"]` blocks of `src/styles/tokens.css`.
   - Light value: `rgba(20, 18, 12, 0.35)` (preserves v0.1 byte-identical).
   - Dark value: `rgba(0, 0, 0, 0.55)` (cool darkening over dark surface; sample value — verify visually).
2. Replace the inline rgba at `src/App.tsx:801` with `var(--modal-overlay)`.
3. Visually verify the modal backdrop reads correctly in both modes on the dev server.
4. Optional: scan for other `rgba(...)` literals in `src/` that should also flow through tokens (`grep -rE 'rgba\(' src/`).

## Out of scope

- Restructuring `CommandPalette` UX.
- Other modal patterns (none currently).

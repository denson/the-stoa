# Arc 38 build directive — Substrate architecture bundle (TIRO + bj5 + gq1)

**Status:** LOCKED at dispatch authoring (2026-05-17). A1-A20 are not DAEDALUS-revisable; sub-decisions inside A5/A8/A11/A13 are DAEDALUS discretion unless surfaced as PRINCIPAL-gate per `operating-disciplines.md` §25.

**Work-unit:** `stoa--ojz` (parent of the 3-candidate bundle; closes on ship). Source tickets closing alongside per A19: `stoa--ojz` (C1) + `stoa--bj5` (C2) + `stoa--gq1` (C3).

**Candidates (3 substantial substrate-architecture canon items):**

| C | Ticket | Topic | Primary surface |
|---|---|---|---|
| C1 | stoa--ojz (P2) | CAPTAIN_TIRO new role file — bw substrate specialist (read-direct + write-advisory split) | `substrate/CAPTAIN_TIRO.md` (new) + install.sh AGENT/CAPTAIN deploy wiring + cross-refs from MAJOR_POLYBIUS.md + MAJOR_PLINY.md + operating-disciplines.md §12 bw cookbook |
| C2 | stoa--bj5 (P2) | User-tier substrate drift detection | `substrate/skills/check-substrate-updates/` extension (per-file-marker scheme for substitution-tracking) + add user-tier to consumer-workspaces.txt (or equivalent user-tier registry) |
| C3 | stoa--gq1 (P3) | Substrate-component design principles | new `operating-disciplines.md` section (agent-installable distribution model + composability framing) |

**Context:** Per the-stoa SPECIFICATION.md §13.5 Pass 4 of the make-the-team-meet-the-spec workplan. After Arc 38 + Arc 39 + Arc 40 + Arc 41 ship: zero open substrate-canon tickets at the-stoa except deferred-with-gating per §13.9. Substrate then ready for Pass 8 mech-check + Pass 10 behavioral validation via stellation dispatch.

**Spec-state at dispatch:** SPECIFICATION.md at HEAD `68c0c12` — post-R1-R4 audit-iteration cadence; structural §12 fully closed at §12-level; one known soft-residue at §13.10 bullet 4 (NC8 / stoa--bbi) accepted per PRINCIPAL option (b). Iteration cadence converged 49→5→2→1; spec considered ready for Arc 38 dispatch.

---

## A1 — One arc, one gauntlet (LOCKED)

Arc 38 ships as a single end-to-end gauntlet (DAEDALUS → ARGUS → ADA → VERA → CATO → ZENO → PLINY signoff → PR merge). All 3 candidates ship in one PR. Mirrors Arc 32 / Arc 34 / Arc 37 bundling shape.

**Estimated arc size:** medium-large. 3 candidates of different shapes (new role file + skill extension + new canon section). Comparable to or slightly smaller than Arc 37 (6 candidates) by total surface; comparable to Arc 36 v2 (2 Parts with substantial Part 2 spike) by per-candidate complexity. Realistic gauntlet wall-clock: 90-180 min including verifier round. Expect ARGUS NEEDS_REVISION cycles for the mixed-shape coordination per SPEC_AUDIT_R2 W2 finding (workplan-shape feedback that PRINCIPAL did not pick to re-bundle).

---

# PART 1 — C1: CAPTAIN_TIRO bw substrate specialist seat (stoa--ojz)

## A2 — TIRO role + read-direct / write-advisory split (LOCKED from SPECIFICATION.md §4.6)

CAPTAIN_TIRO is a new substrate-specialist seat for bw substrate operations. Per the-stoa SPECIFICATION.md §4.6:

- **TIRO does reads directly when delegated.** Any seat (POLYBIUS, PLINY, other CAPTAINs) dispatches TIRO with a bw query ("all open P2 tickets at the-stoa", "comment history on stoa--y14", "tickets blocked-by stoa--bj5") + TIRO returns a clean structured answer. TIRO's whole-context priming on bw mechanics + correct completeness flags (e.g., `bw list --status open --all` per cookbook §12.1) absorbs the audit-completeness failure mode that motivated this seat (2026-05-17 empirical anchor: user-tier POLYBIUS demonstrated the failure 3 times on a single day before the spec-audit cadence caught it).
- **TIRO never writes for another seat.** Writes (create, comment, close, dep add, sync) are authored by the seat that owns the work. Rationale: (a) authorship attribution stays clean — a comment from POLYBIUS_the_stoa is genuinely from that seat, not via TIRO proxy; (b) Arc 36 §7.1 5th beat + §7.7 author-tag canon stays meaningful (proxy-writes would muddy timeline-arithmetic for radio-check + heartbeat thresholds); (c) accountability for state changes stays with the seat making the change.
- **TIRO advises on write syntax.** Any seat can ask TIRO "what's the canonical command to close stoa--y14 with an audit comment?" + TIRO returns the syntax (positional `bw comment <id> "text"` not `-m` flag; `--reason` flag on close; HEREDOC pattern for multi-line; the `bw dep add <X> blocks <Y>` direction gotcha; etc.). The asking seat then executes the command itself.

The split is PRINCIPAL-locked per SPECIFICATION.md §4.6. ADA must NOT widen TIRO to execute writes for another seat.

## A3 — TIRO toolset (LOCKED from SPECIFICATION.md §2.2)

TIRO's bounded toolset: **Bash, Read, Grep, Glob**. No Write/Edit (TIRO doesn't author content; advises on syntax + returns query results).

DAEDALUS may surface as PRINCIPAL-gate whether WebSearch/WebFetch should be added (for live bw upstream docs lookup when local cookbook is insufficient). Default per spec: not included. If DAEDALUS wants to add, surface — don't widen unilaterally.

## A4 — TIRO role file structure (precedent: CAPTAIN_BARTLEBY)

Closest substrate precedent: `substrate/CAPTAIN_BARTLEBY.md` — file-clerk with bounded toolset that returns focused file:line citations to the dispatching seat. TIRO mirrors this shape: bounded specialist that returns structured answers on demand.

DAEDALUS authors `substrate/CAPTAIN_TIRO.md` following the standard CAPTAIN envelope (read-before-write discipline; standard sections; scope-honest verdict format) with TIRO-specific content:

- Role description (read-direct + write-advisory split per A2)
- Bounded toolset (per A3)
- bw subcommand reference with the documented gotchas (`--all` flag for completeness; `dep add` direction; positional `comment` syntax; `--reason` flag; HEREDOC patterns; bw worktreeconfig recovery if it re-surfaces)
- When TIRO IS the right dispatch (queries, audits, completeness checks; multi-store cross-reference reads)
- When TIRO is NOT the right dispatch (writes — TIRO returns syntax advice; the dispatching seat executes; PRINCIPAL-gated decisions; substantive design)
- Return shape conventions (structured answer + cite-comments to bw output where useful)
- Standard CAPTAIN envelope cross-refs to `MAJOR_PLINY.md` + `operating-disciplines.md`

## A5 — TIRO install.sh wiring (DAEDALUS sub-decision)

`substrate/install.sh` AGENT/CAPTAIN deploy needs to include TIRO. Per Arc 27 stoa--uly precedent for new agent additions:

- Add `CAPTAIN_TIRO` to the canonical agent list in install.sh.
- Verify install.sh dry-run lists TIRO at all 3 target modes (project / sub-project / user-tier).
- Per Arc 27 stoa--uly convention: SKILL.md / role-file frontmatter MUST carry `author: Denson Smith` (the IMMUTABLE rule per CLAUDE.md; ADA must verify pre-commit).

DAEDALUS picks the exact insertion locus in install.sh + verifies the dry-run flow. If install.sh has a per-tier deploy split that requires TIRO at some tiers but not others (e.g., user-tier may not need TIRO if user-tier POLYBIUS handles bw queries directly), surface as design decision.

## A6 — TIRO cross-refs (LOCKED)

Cross-refs from existing substrate canon to new TIRO seat:

- **`substrate/MAJOR_POLYBIUS.md` §7** (POLYBIUS-pair coordination) — cross-ref noting TIRO is the delegated bw-query specialist for cross-tier or cross-project bw queries; especially for audit-completeness work.
- **`substrate/MAJOR_PLINY.md` §5** (gauntlet pipeline) or §6 (Communication) — cross-ref noting PLINY dispatches TIRO for bw queries during arc execution; consults TIRO for write syntax.
- **`substrate/operating-disciplines.md` §12** (bw cookbook) — note that the cookbook is reference material; TIRO is the specialist seat agents delegate to for the read use cases the cookbook covers.
- **`substrate/CAPTAIN_*.md`** (gauntlet seats — DAEDALUS picks which need cross-refs; ADA + ARGUS + VERA + CATO + ZENO commonly use bw for ticket reads + verdict writes) — light cross-ref note: "for bw audits, delegate to CAPTAIN_TIRO per `operating-disciplines.md` §12 + `substrate/CAPTAIN_TIRO.md`."

DAEDALUS picks exact wording + insertion points; ADA implements per design.md.

---

# PART 2 — C2: User-tier substrate drift detection (stoa--bj5)

## A7 — bj5 scope (LOCKED from SPECIFICATION.md §12.5 + bj5 ticket body)

Extend `substrate/skills/check-substrate-updates/` to detect drift in user-tier substrate (`~/.claude/` per Denson Smith's machine; the global PRINCIPAL config). Currently the skill is project-tier only per `substrate/consumer-workspaces.txt` ("User-tier check is future work"). The empirical anchor: 2026-05-14 PRINCIPAL discovered `~/.claude/MAJOR_POLYBIUS.md` was 71 lines / 2 sections stale; nothing flagged it because user-tier was out of scope of the drift-check.

## A8 — Per-file-marker scheme (DAEDALUS sub-decision)

The blocker per the bj5 ticket body + `agents/design/stoa--lyh/design.md` §10.2: user-tier deployed files have install.sh substitutions (`{{USER_TIER_DIR}}` → real path) that can't be cleanly reversed for the diff against canon source. Four candidate fix-shapes DAEDALUS picks from (or invents a 5th):

- **(α) Embedded marker** — install.sh adds a marker comment at the top of each deployed file recording the substitutions applied. check.sh reads the marker + normalizes the deployed file before diffing. Pros: self-contained per file; survives file moves. Cons: pollutes deployed file content with non-canon comment; requires marker parsing.
- **(β) Sidecar file** — install.sh writes a `.substrate-state` sidecar next to each deployed file recording substitutions. check.sh reads the sidecar to normalize. Pros: doesn't pollute deployed content. Cons: 2-file pairs to maintain; sidecar can be deleted independently of file.
- **(γ) Manifest file per workspace** — install.sh writes one manifest at workspace root (`.claude/.substrate-manifest`) recording all substitutions across all deployed files. check.sh reads the manifest. Pros: single source-of-truth per workspace. Cons: manifest can drift from actual file state if files are edited or moved.
- **(δ) Reverse-substitution attempt** — check.sh tries to un-substitute the deployed file by detecting known substitution-target patterns (e.g., `$HOME/.claude/`) + reverting them to canonical (`{{USER_TIER_DIR}}/`). Pros: no marker overhead. Cons: heuristic; can fail when substitution patterns are ambiguous (e.g., `~/.claude/` literal in canon source that shouldn't be reverted).

User-tier POLYBIUS leans (γ) manifest — single-source-of-truth shape matches the rest of the substrate's design (one canon source; one deployed manifest per workspace; clean drift detection). DAEDALUS picks; documents rationale + chosen shape's failure modes per ADA build.

If the spike during Phase 1 reveals an entirely different approach (e.g., bw 0.14.0 added a built-in substitution-tracking mechanism the substrate can adopt), surface as PRINCIPAL-gate per §25 — don't pick unilaterally.

## A9 — User-tier registry (LOCKED scope, DAEDALUS picks shape)

Add user-tier to the drift-check scope. Current `substrate/consumer-workspaces.txt` enumerates project-tier + sub-project consumer workspaces; needs to grow a user-tier section OR a separate user-tier registry OR an entry-with-tier-tag.

DAEDALUS picks the registry shape (extend existing file vs new file vs annotation). Constraints: must not break existing consumer-workspaces.txt parsing in check.sh; must support per-tier processing in check.sh + apply.sh + revert.sh.

## A10 — bj5 implementation: extend check.sh + apply.sh + revert.sh (LOCKED scope, DAEDALUS picks per-script changes)

The 3 existing scripts in `substrate/skills/check-substrate-updates/` need parallel updates:

- **check.sh** — read user-tier substrate per the new registry shape; apply the A8 per-file-marker scheme; report CURRENT vs DIFFERS per file.
- **apply.sh** — walk user-tier drift surfacings; apply substitutions per A8 marker scheme; per-file consent + diff display per existing apply.sh pattern.
- **revert.sh** — undo most-recent apply at user-tier (same as project-tier behavior; just scoped to user-tier registry).

DAEDALUS designs the per-script changes coherently; ADA implements; ZENO mechanical-checks the install.sh dry-run + check.sh / apply.sh / revert.sh smoke-runs.

---

# PART 3 — C3: Substrate-component design principles (stoa--gq1)

## A11 — gq1 scope + insertion locus (LOCKED scope, DAEDALUS picks insertion)

Per the stoa--gq1 ticket body (from `_drafts/ticket_substrate_component_design_principles.md` archived 2026-05-13 → formal ticket): the Ariadne distribution-shaping work (HUMAN_relay_user_polybius_ariadne_distribution_and_mcp_2026-05-13 Findings 2 + 3) surfaced two generalizable substrate-architecture principles applicable to any future Stoa-team component intended for agent-installation:

**Principle 1 — Agent-installable distribution model.** The user-experience flow for any agent-installable substrate component:

1. User encounters component (URL, word-of-mouth).
2. User pastes URL to their AI.
3. User asks "do I need this?"
4. AI fetches README + AGENTS.md + skills/ materials.
5. AI evaluates against user's domain.
6. AI returns yes / no / try-the-demo recommendation.
7. If yes + consent → AI installs + runs demo.

**Principle 2 — Composability framing.** The AI is the primary reader at the repo. The human is the decision-authority who acts on the AI's recommendation.

These principles need to be canonified as substrate canon so future component-shipping arcs apply them consistently.

DAEDALUS picks insertion locus in `operating-disciplines.md`. Candidates:
- **(α)** New top-level section after §30 (four-layer identity model) — e.g., new §31 "Substrate-component design principles for agent-installable distribution."
- **(β)** Subsection of existing §29 (multi-team interoperation) — substrate components ARE the artifacts that flow between teams.
- **(γ)** New top-level section before §29 — design-principles are upstream of multi-team interop (you design components before they interoperate).

User-tier POLYBIUS leans (α) new §31 — clean separation; consistent with prior new-section additions (§27 Arc 33 mechanical/agent split; §28 Arc 35 trailer canon; §29 Arc 37 multi-team interop; §30 Arc 37 four-layer identity). DAEDALUS picks final.

## A12 — gq1 content shape (LOCKED from ticket body)

New section body covers:

- Principle 1 (the 7-step agent-installable flow) with concrete instances.
- Principle 2 (AI-as-primary-reader + human-as-decision-authority) with rationale.
- Worked example: Ariadne Core as the originating empirical anchor (HUMAN_relay link).
- Cross-refs to: §29 (multi-team interop — substrate components are the interop currency); §17 (base-vs-custom — custom agents are project-tier substrate components); §27 (mechanical-script / agent-inspection — the script/agent pattern is itself a substrate-component pattern); §28 (Co-Authored-By trailer — substrate-component attribution).

DAEDALUS picks exact wording + how concrete vs abstract the principles read; ADA implements per design.md.

## A13 — gq1 cross-component-evidence question (DAEDALUS sub-decision)

The ticket cites Ariadne distribution as the originating empirical anchor (N=1). The principles are *suggestive* across multiple substrate-domains (Stoa substrate itself; Ariadne; Railway; future components). DAEDALUS decides whether to:

- **(i) Cite Ariadne only** — honest N=1; future evidence accretes via additional component-shipping arcs.
- **(ii) Cite Ariadne + Stoa substrate-deploy as parallel empirical instances** — substrate itself follows a similar flow (install.sh deploys; consumer workspace runs it; check-substrate-updates audits drift). The Stoa-substrate instance pre-dates the Ariadne instance; both are independent observations.
- **(iii) Cite Ariadne + speculate on Railway as third instance** — Railway substrate-skill (`~/.claude/skills/railway-access/SKILL.md`) is sibling-shaped; could be cited as anticipated future instance.

User-tier POLYBIUS leans (ii) — substrate itself is the clean parallel instance + N=2 is more honest than N=1-with-speculation. DAEDALUS picks; documents rationale.

---

# Universal / self-applied decisions (apply to all 3 Parts)

## A14 — Self-application (LOCKED)

**TIRO self-application — chicken/egg.** TIRO IS the deliverable of C1; the team can't dispatch TIRO during the arc that ships it. The team uses `bw list --all` directly per the existing cookbook + spec §4.6 (same pattern as the spec-audit cadence used over the last 4 audit passes). Friction observed during the arc IS empirical-anchor reinforcement for TIRO's value; surface as audit-feedback in the design.md or build commit if friction surfaces.

**bj5 self-application — partial.** If ADA implements check-substrate-updates user-tier extension AND runs it against the-stoa's own user-tier substrate during Phase 3 verification, that's first-worked-example self-application. Not strictly required; opportunistic. If it surfaces user-tier drift unrelated to Arc 38, surface as Pass 8 spec-recon scope or new follow-up ticket.

**gq1 self-application — none.** Design-principles canon doesn't have obvious self-application within the arc that ships it. Acceptable.

PLINY signoff verifies the chicken/egg framing held (no proxy-write to TIRO; team used direct bw correctly per cookbook).

## A15 — §28 Co-Authored-By trailer + §5.10 signoff-accuracy + §5.11 paste archival + §19.6 attestation honesty (LOCKED, self-applied)

Per Arc 35 §28 + Arc 36 §7.7 + MAJOR_PLINY.md §5.10 + §5.11 + operating-disciplines.md §19.6.

**§28 trailer discipline:** every CAPTAIN commit inside `arc-38/build` carries `Co-Authored-By: CAPTAIN_<MNEMONIC>_the-stoa <captain-<mnemonic>@the-stoa.local>` trailer per Arc 35 canon. ADA + DAEDALUS commits MUST carry trailers. PLINY's PR-merge step MUST preserve trailers — per stoa--6wp (Arc 40 C4 follow-up to Arc 37's bb12806 regression), do NOT use `gh pr merge --body` with a custom body that overrides GitHub's trailer-concatenation. Either omit `--body` (let GitHub auto-populate from source commits including trailers) OR include trailers explicitly in the `--body` HEREDOC. **This is the first arc that should ship trailer-clean on the squash-merge body forward of the Arc 37 bb12806 regression** (Arc 40 ships the canon fix; Arc 38 should apply the discipline ahead of that).

**§5.10 signoff-accuracy + §19.6 attestation-honesty:** PLINY's signoff live-verifies cleanup claims (arc-38/build local + remote deleted; worktree removed; PR merged; main fast-forwarded). Attestations cite live-verified state at attestation time, NOT assumed-from-context (do NOT echo the dispatch-authoring SHA `68c0c12` as verified-at-attestation state; re-run `git rev-parse HEAD` at attestation time).

**§5.11 paste archival:** activation pastes (`HUMAN_paste-{polybius,pliny}-arc-38-instruction.md`) archived to `substrate/arcs/arc-38/pastes/` on arc close. Applied via `git mv` per §5.11 load-bearing note (preserves `git log --follow` history continuity).

## A16 — `[from: <self>]` author-tag convention + §11 step 1.5 renewal cron (LOCKED, self-applied)

Per Arc 36 §7.1 5th beat + §7.7 + §11 step 1.5.

**Author-tag canon:** POLYBIUS coordination heartbeats on the work-unit ticket (stoa--ojz) carry `[from: polybius-the-stoa]` per Arc 36 §7.1 5th beat. PLINY heartbeats carry `[from: pliny-the-stoa]` (over-compliance per A2.5 hard-lock; acceptable; the convention scope is POLYBIUS-on-POLYBIUS but PLINY tagging is harmless). DAEDALUS / ADA / CATO / VERA / ZENO comments classified §7.7 case 4 (non-POLYBIUS substance comments; do not enter timeline-arithmetic).

**Renewal cron:** POLYBIUS schedules the one-shot renewal cron per `operating-disciplines.md` §11 step 1.5 at +144h from polling-cron creation. Arc 38 is short (~90-180 min); renewal won't fire; but the canon application forward is what matters. Bug #40228 surveillance per stoa--pqn (Arc 41 C5): `CronCreate durable: true` may not persist; MAJOR_POLYBIUS.md §9 step 7 PRINCIPAL-consent re-setup is the load-bearing recovery if the cron is lost.

## A17 — Cite-comment discipline (LOCKED)

Cross-references between new `substrate/CAPTAIN_TIRO.md` + new operating-disciplines.md §31 (gq1) + extended check-substrate-updates skill (bj5) + the 4 cross-ref additions (A6) must resolve via cite at every read-site. Same pattern as Arcs 26 / 28 / 29 / 30 / 31 / 32 / 33 / 34 / 35 / 36 v2 / 37 cite-comments.

## A18 — Authorship attribution (IMMUTABLE per CLAUDE.md)

File-frontmatter `author:` fields remain Denson Smith per substrate/CLAUDE.md IMMUTABLE rule. **New role file `substrate/CAPTAIN_TIRO.md` MUST carry `author: Denson Smith` frontmatter** per Arc 27 stoa--uly convention. ADA verifies pre-commit; ZENO mechanical-checks in Phase 3.

Git commit `Author:` remains PRINCIPAL per `~/.claude/CLAUDE.md` absolute rule. Co-Authored-By trailers per A15 + Arc 35 §28 are the seat-identity signal layered on top; Author: is never overridden.

## A19 — Source-ticket closure (LOCKED)

On Arc 38 ship: close all 3 source tickets with cross-ref to merge commit + audit comment per candidate.

- **stoa--ojz** (C1 work-unit + parent) closes with cross-ref + audit comment naming the new CAPTAIN_TIRO.md role file + install.sh wiring + cross-refs landed.
- **stoa--bj5** (C2) closes with cross-ref + audit comment naming the per-file-marker scheme + user-tier registry + check.sh/apply.sh/revert.sh extensions landed.
- **stoa--gq1** (C3) closes with cross-ref + audit comment naming the new operating-disciplines.md section.

Tag `[for: user-tier-polybius]` on stoa--ojz (the work-unit) inviting QA pass per the established pattern.

## A20 — Pre-branch hygiene + worktree convention + out-of-scope hard-locks (LOCKED, self-applied)

Per MAJOR_PLINY.md §5.9 + §5.9.4 + operating-disciplines.md §25.

PLINY runs the two-check rule before creating `arc-38/build`. Builds in `.claude/worktrees/arc-38-build/` (NOT in main worktree). User-tier POLYBIUS confirmed at dispatch authoring: local main = origin/main at `68c0c12`; no orphan arc-build branches.

**Out-of-scope (HARD-LOCKED):**

- DO NOT bundle additional candidates (3 is locked; Arc 39 + Arc 40 + Arc 41 have their own candidates per §13.6 + §13.7 + §13.8).
- DO NOT widen TIRO to execute writes for another seat (read-direct + write-advisory split is PRINCIPAL-locked per SPECIFICATION.md §4.6).
- DO NOT extend TIRO to non-bw subsystems (future arc; per §4.6 "pattern generalizes" notes for git / cron / worktree specialists).
- DO NOT restructure `check-substrate-updates` beyond what bj5 requires (the existing project-tier scope is unchanged + extended; not rewritten).
- DO NOT add validate-spec skill (that's Pass 9 / §13.11; not Arc 38 scope).
- DO NOT touch substrate/install.sh beyond what TIRO + bj5 require (per the install.sh "smoke test before any substrate change ships" CLAUDE.md rule).
- DO NOT touch the stellation workspace.
- DO NOT propose NC8 (Arc 38 PRINCIPAL accepted option (b) per spec §13.10 bullet 4 known-residue parenthetical; not Arc 38's responsibility).

If DAEDALUS or any CAPTAIN surfaces a scope concern touching A20, treat as substance disagreement: confirm A20 wording, file follow-up ticket if the concern has merit, do NOT expand this arc.

---

## Phase structure

**Phase 1 — Design (DAEDALUS + ARGUS).**

DAEDALUS reads this directive + the 3 source tickets + relevant substrate canon per the Read order. Produces `agents/design/stoa--ojz/design.md` covering all 3 candidates — each as its own section with: exact wording for canon edits, A5 install.sh wiring choice, A8 per-file-marker scheme choice, A11 §31 insertion locus, A13 N-evidence framing, cite-comment plan, self-application notes per A14.

For C2 specifically: include a brief spike step before Part 2 design is finalized — `ls substrate/skills/check-substrate-updates/` to verify current structure; `cat substrate/consumer-workspaces.txt` to verify registry shape; if anything has changed since the bj5 ticket was filed (2026-05-14), surface in design.md.

ARGUS cold-audits design.md. Expected NEEDS_REVISION on at least one of {A5 install.sh wiring choice, A8 per-file-marker scheme, A11 §31 insertion locus, A13 N-evidence framing} given the bundle's mixed-shape coordination (SPEC_AUDIT_R2 W2 noted this).

**Phase 2 — Build (ADA in `.claude/worktrees/arc-38-build/`).**

ADA implements all 3 candidates per approved design.md. ADA's commits carry Co-Authored-By trailers per §28 (Arc 35 canon). Coordinated commits per candidate OR single coherent commit — ADA picks based on diff coherence; documents rationale in PR description.

**Phase 3 — Verify (VERA + CATO + ZENO).**

VERA exercises probes from design.md (one per candidate at minimum; specifically: TIRO role file structural conformance to CAPTAIN envelope; bj5 check.sh dry-run + per-file-marker round-trip on a user-tier test file; gq1 §31 cross-ref resolution). CATO cold-reads diff for craft + scope + wording. ZENO mechanical spec-vs-result check.

**CATO is MANDATORY** for this arc (substrate canon work + new role file + new canon section + tool extension; wording precision matters; first arc forward of the Arc 37 bb12806 trailer regression + spec-audit-iteration cadence — extra craft scrutiny justified).

**Phase 4 — Ship + close.**

PLINY:

- Opens PR with arc title.
- Merges via `gh pr merge --squash --delete-branch`. **DO NOT use `--body` override** per stoa--6wp regression cite; let GitHub auto-populate from source commits OR include trailers in HEREDOC if `--body` is needed.
- Verifies cleanup live per §5.10 (arc-38/build local + remote deleted; worktree removed; PR merged; main fast-forwarded; squash-merge body carries §28 trailers from source commits).
- Verifies §28 trailers preserved on the squash-merge commit (run `git log -1 --pretty='%B' <squash-sha> | grep -i "co-authored"` post-merge to confirm; if empty, surface as stoa--6wp-class regression).
- Closes 3 source tickets per A19 with cross-refs + audit comments.
- Tag `[for: user-tier-polybius]` on stoa--ojz inviting QA pass.
- Paste archival per A15 + §5.11.

---

## DAEDALUS sub-decisions summary

- **A5** — TIRO install.sh wiring (insertion locus; per-tier deploy decisions)
- **A8** — C2 per-file-marker scheme (α/β/γ/δ or invented 5th; recommend γ manifest per user-tier lean)
- **A11** — C3 §31 insertion locus (α new §31 / β subsection of §29 / γ before §29; recommend α per user-tier lean)
- **A13** — C3 N-evidence framing (i Ariadne only / ii Ariadne + Stoa substrate / iii Ariadne + Railway speculation; recommend ii per user-tier lean)

Plus DAEDALUS-discretion items: TIRO role file exact wording; bj5 per-script change shapes; gq1 section body exact prose; cross-ref insertion points across 4-5 substrate files.

If any pick exceeds DAEDALUS discretion, treat as PRINCIPAL-gate per §25 — halt + escalate immediately rather than proceed-then-flag.

---

## Read order for DAEDALUS

1. This directive (load-bearing spec for all 3 candidates).
2. `bw show stoa--ojz` (C1 work-unit + parent; carries the TIRO empirical anchor).
3. `bw show stoa--bj5` (C2 work-unit; carries the 2026-05-14 71-line user-tier drift empirical anchor).
4. `bw show stoa--gq1` (C3 work-unit; carries the Ariadne distribution-shaping principles).
5. **`the-stoa/SPECIFICATION.md` §4.6** (TIRO scope-lock from PRINCIPAL 2026-05-17) + **§9.1** (bw tools + specialist-delegation framing) + **§12.5** (Arc 38 candidates context) + **§13.5** (Pass 4 Arc 38 enumeration) + **§14** (PRINCIPAL editing notes — context on the spec's structural shape).
6. **`HUMAN_paste-polybius-arc-38-instruction.md`** in the project root — POLYBIUS's activation paste; same content frame as this directive.
7. **`substrate/CAPTAIN_BARTLEBY.md`** — closest CAPTAIN-shape precedent for TIRO (bounded-toolset file-clerk specialist).
8. **`substrate/skills/check-substrate-updates/`** — current skill structure (check.sh / apply.sh / revert.sh / consumer-workspaces.txt) for bj5 extension surface.
9. **`substrate/consumer-workspaces.txt`** — current registry shape for the user-tier addition.
10. **`substrate/operating-disciplines.md`** — primary surface for canon edits:
    - §12 (bw cookbook — TIRO cite target)
    - §17 + §23 (base-vs-custom — gq1 cross-ref)
    - §27 (mechanical-script / agent-inspection split — gq1 cross-ref + the substrate-canon-pattern precedent)
    - §28 (Co-Authored-By trailer — A15 self-applied; gq1 cross-ref for substrate-component attribution)
    - §29 (multi-team interoperation — gq1 cross-ref; insertion-locus candidate β)
    - §30 (four-layer identity — sibling Arc 37 canon)
    - §31 (NEW — gq1 lands here per user-tier lean for A11 α)
11. **`substrate/MAJOR_POLYBIUS.md` §7** + **`substrate/MAJOR_PLINY.md` §5 + §6** — TIRO cross-ref targets per A6.
12. **`substrate/install.sh`** — TIRO wiring + bj5 wiring if registry shape requires install.sh changes.
13. **`substrate/arcs/arc-27-build-directive.md`** (stoa--uly precedent for new skill/agent addition) + **`substrate/arcs/arc-37-build-directive.md`** (most recent 6-candidate bundle precedent for §13.5 Pass 4 framing).
14. **`SPEC_AUDIT_R4.md` + `SPEC_AUDIT_R3.md` + `SPEC_AUDIT_R2.md` + `SPEC_AUDIT.md`** — context on the 4-pass audit-iteration cadence + the substrate-principle refinement evidence (stoa--bbi N=4 anchor). Arc 38 is the FIRST forward arc after the iteration converged; the audit-cadence framing is informative for understanding the spec's structural shape.
15. **`stoa--6wp`** ticket body + Arc 37 `bb12806` empirical anchor — the squash-merge `--body` regression PLINY must avoid in Phase 4.

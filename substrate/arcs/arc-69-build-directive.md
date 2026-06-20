# Arc 69 build directive — Substrate-hygiene cleanup (batched small-bug sweep)

**Audience:** the fresh Claude Code sessions opened to build Arc 69 (PLINY_the-stoa + the floor-manager POLYBIUS_the-stoa).
**Authored by:** Polybius_the_Stoa (user-level Stoa agent, sid 990b0750-5572-4836-b9c7-18d626a12e96) on behalf of the PRINCIPAL (Denson Smith).
**Status:** FINALIZED on the PRINCIPAL go (2026-06-20: "set up and run the substrate-hygiene cleanup arc now"). NOT yet dispatched — staged pending NOMOS-on-the-directive, then committed + launched.
**Builds on:** current the-stoa main (`8e4b20c`). Project-tier charter: **`stoa--csn`** (carries the full organized bug cluster + DC0).

**You are MAJOR_PLINY for the the-stoa Arc 69 engagement.** Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role. Open Claude Code in `C:\Users\denso\claude_projects\the-stoa\`.

**Your one job:** sweep a cluster of ~12 small, independent substrate-hygiene bugs — each filed with its own `file:line` repro — fixing the confirmed-live, confirmed-small ones and **surfacing for re-scope any that turn out bigger-than-a-cleanup**. This is a BUG-SWEEP, not a feature arc. Then return cleanly.

**This is a substrate-tooling/canon arc — run the full gauntlet** (DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS). **Standard POLYBIUS+PLINY team** — this arc fixes bugs, it does NOT design a custom agent or workflow, so **CHIRON/HAMILTON are NOT in it** (per the variable-composition trigger). Cluster A (author-gate) is LOAD-BEARING — CATO/NOMOS carry extra weight there.

---

## Comms — async with Polybius_the_Stoa via bw (`stoa--*`)

Coordinate on the charter **`stoa--csn`** (the organized cluster + DC0 live there). Polybius_the_Stoa (the user-level owner) monitors + interjects; the floor-manager runs independent verification at each hand-back and relays up. The PRINCIPAL is NOT the relay — beadwork is. Asymmetric polling: don't poll while working; do poll when waiting via `CronCreate */5`. `bw comment <id> "text"` is **positional, no `-m`**. Run `bw prime` at activation.

**DOGFOOD:** every seat signs bw comments `[from: <NAME> | sid <session-id>]` (your sid via the deployed `whoami` skill / `$CLAUDE_CODE_SESSION_ID`).

---

## Read first

1. **The charter `stoa--csn`** — the full bug cluster organized into 4 sub-clusters + DC0 (the grounding/re-scope rule). Then **`bw show` EACH ticket** below for its specific `file:line` repro before touching it.
2. The touched surfaces: the **author-gate** (`substrate/hooks/` — the PreToolUse authorship gate + its tests at `substrate/hooks/tests/`), **`substrate/install.sh`**, the **`save-verdict` module** (`substrate/modules/save-verdict.md` + the byte-aligned region shared with `CAPTAIN_ARGUS/VERA/CATO.md` §7), **`substrate/skills/team-launcher/launch-team.ps1`**, **`substrate/skills/check-bw-release/`**, **`substrate/skills/check-substrate-updates/`**, **`substrate/MAJOR_POLYBIUS.md`**, **`substrate/skills/validate-spec/`**.

---

## The bug cluster (build target — `bw show` each for the repro)

- **Cluster A — author-gate (LOAD-BEARING; runs on every commit):** `stoa--a2x` (false-positive on ownership prose), `stoa--y12` (cfg extractor misses `Copyright (c) <year> <name>` — true-positive MISS), `stoa--ez9` (hard-blocks legit citation/audit prose — no reviewed-allow path), `stoa--iyl` (install.sh allow-list seeds git-identity, not artifact-author → false-blocks PRINCIPAL commits).
- **Cluster B — save-verdict module:** `stoa--luo` (`attach_status` prose-contract → mechanize rc-capture). *(`stoa--qsf` — the probe-id lowercase-`p` regex — was found ALREADY-FIXED during directive grounding: the canonical `modules/save-verdict.md` regex is already case-insensitive `^[pP]`; the only residual was deploy-drift in the retired old Python skill. Closed-superseded; NOT a build target.)*
- **Cluster C — install.sh / check robustness:** `stoa--3nh` (FAIL-LOUD on empty MAJOR/CAPTAIN glob), `stoa--kr7` (sweep residual POLYBIUS/PLINY-only MAJOR refs off install.sh non-enumeration paths), `stoa--p41.3` (check-bw-release curl `--max-time`).
- **Cluster D — tooling/doc:** `stoa--p41.4` (MAJOR_POLYBIUS doc-wording for retired check tools), `stoa--waa` (launcher unquoted multi-word prompts — CONFIRM live post-Arc-68), `stoa--vr1` (validate-spec residue), `stoa--tg7` (apply.sh/install.sh/revert.sh commits omit the §28.9 seat trailer).

---

## Design items — DAEDALUS resolves in Phase A (surface at the design hand-back)

- **DC0 — GROUND each ticket FIRST (the gate on the whole sweep).** For every ticket: confirm it is still LIVE (not already fixed by Arcs 66–68 — `stoa--waa` and `stoa--p41.4` especially, post-Arc-68/launcher-rewrite) AND that it is a SMALL, independent, one-spot fix. Produce a per-ticket verdict: FIX (live + small), ALREADY-FIXED (close with the landing ref), or RE-SCOPE (bigger-than-a-cleanup → ticket-and-skip, do NOT force into the sweep). The sweep ships ONLY the FIX set; ALREADY-FIXED and RE-SCOPE are dispositioned, not forced.
- **DC1 — Cluster A is LOAD-BEARING; do no harm.** The author-gate fires on every commit. Each Cluster-A fix must ADD the missed/allow case WITHOUT re-opening a false-block or breaking the existing 16/16 author-gate tests. Every Cluster-A change carries a NEW author-gate test fixture proving both directions (the case it now allows/catches AND a control it still blocks/allows). The `stoa--ez9` "reviewed-allow path" is the one genuine DESIGN question — how to let legitimate source-citation/audit prose through without a hole a real authorship-violation could ride; DAEDALUS designs it explicitly (a narrow, reviewed mechanism, not a blanket bypass).
- **DC2 — one ticket = one minimal, independent change.** Keep each fix's diff small + self-contained so CATO can review per-fix, not as a tangled blob. No drive-by refactors.
- **DC3 — save-verdict (Cluster B) edits the byte-aligned region.** `modules/save-verdict.md` shares a byte-aligned procedure with `CAPTAIN_ARGUS/VERA/CATO.md` §7 (canonical-template-alignment). Any change there must re-align ALL four homes — do not fix one and skip the alignment.

---

## Deliverables (land together)

1. The FIX-set changes, per cluster (the confirmed-live small fixes).
2. NEW author-gate test fixtures for every Cluster-A change (both-directions per DC1).
3. Each FIX ticket updated with the landing change; ALREADY-FIXED tickets closed with the ref; RE-SCOPE tickets commented with the reason + their proper next-step.
4. Consistency: no stale refs left in touched docs; `install.sh` SKILL_NAMES/HOOK_NAMES unaffected unless a ticket explicitly targets them.

---

## Verification / Definition of done

- **Per-ticket:** each FIX-set ticket's specific repro (from its body) is exercised and shown fixed — for Cluster A, the actual false-positive/miss case runs through the real gate.
- **Author-gate (Cluster A) — no regression:** the existing author-gate test suite stays GREEN, plus the new both-directions fixtures pass. The reviewed-allow path (`ez9`) does NOT open a hole — VERA proves a real authorship-violation control STILL blocks.
- **save-verdict (Cluster B):** the four byte-aligned homes are re-aligned (grep/diff proves identity); `canonical-template-alignment.md` honored.
- **Full close-gate suite:** `npm run gen-data` deterministic, `vitest`, author-gate tests, the stop-hook tests — all green.
- **Canon greps clean;** **NOMOS CONFORMANT** on the final commit; commits carry `Author=PRINCIPAL` + the seat-identity Co-Authored-By trailer per §28.9.
- Committed + pushed to `the-stoa` main; `stoa--csn` updated with the landing SHA + the per-ticket disposition; each swept ticket closed.

---

## Out of scope

- **The roadmap/epic items** (debloat epic, ksge calibration, CHIRON/HAMILTON roadmaps, agent-git-sub-identity, the bw-detach tool gap) — NOT in this sweep.
- **The deferred CRLF rollout** (`u--ug1`, deferred to 2026-07-07).
- **Anything DC0 flags RE-SCOPE** — surface + ticket, do not force a bigger change into the sweep.
- **The remaining obsolete-skills module-migration sweep** (`stoa--xrq` follow-up) — note it; only fold in if a ticket here genuinely touches it.

---

## Discipline

- Full gauntlet — tooling + canon; NOT mechanical. Standard POLYBIUS+PLINY (no CHIRON/HAMILTON).
- GROUND-then-fix (DC0): never fix a ticket without confirming it is live + small first.
- One-ticket-one-change (DC2); do-no-harm on the load-bearing author-gate (DC1).
- Fix-now for tiny related defects spotted in the same file; ticket-with-plan if scope-different.
- bw syntax: positional `bw comment`; `bw prime` at activation; `--reason` on close.

## Suggested phasing

- **Phase A — ground + design (DAEDALUS).** Per-ticket DC0 verdict (FIX / ALREADY-FIXED / RE-SCOPE); for the FIX set, the concrete edit plan per cluster (incl. the `ez9` reviewed-allow design + the Cluster-A test fixtures + the save-verdict 4-home alignment). Surface to the floor-manager for a go/no-go before build.
- **Phase B — build (ADA).** Cluster by cluster: A (author-gate + tests) → B (save-verdict, aligned) → C (install.sh/check) → D (tooling/doc).
- **Phase C — verify (ARGUS/VERA/CATO + NOMOS).** Per-ticket repro; author-gate no-regression + both-directions; save-verdict alignment; full close-gate suite; ground-truth.
- **Phase D — ship.** Commit + push; update `stoa--csn` with the SHA + per-ticket disposition; close the swept tickets.

Standby, run.

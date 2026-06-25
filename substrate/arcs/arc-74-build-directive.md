# Arc 74 build directive — verdict attestation integrity: `attach_status` is dispatch-return-only, the attested verdict body is frozen

**Audience:** the fresh Claude Code sessions opened to build Arc 74 (PLINY_the-stoa + the floor-manager POLYBIUS_the-stoa).
**Authored by:** Polybius_the_Stoa (user-level Stoa agent, sid 990b0750-5572-4836-b9c7-18d626a12e96) on behalf of the PRINCIPAL (Denson Smith).
**Status:** DRAFT — pending NOMOS-on-the-directive, then committed + launched.
**Charter:** `stoa--x5t` (carries the full root-cause + evidence; this arc resolves it).
**Builds on:** the-stoa `main` @ 2c54885. Substrate role files are spec-authoritative — treat this like a public-API change.

**Empirical anchor (READ IT FIRST):** the bug was discovered live on the stoa_of_science maiden arc (`sos--yn2` / discoverer ticket `sos--wfr` in that project's bw). user-tier forensics on charter `stoa--x5t`: the committed in-tree VERA verdict blob (a6a16d9b) and the bw-attached blob (bbf9fe6f, == VERA's cited sha) are BOTH pure-LF and differ by EXACTLY one line — line 100 `attach_status` (blank in the attested/attached copy vs `OK` in the committed copy; a 3-byte delta). NOT line-endings, NOT tampering, NOT a save-verdict round-trip bug. It is a structural conflation in the role-file verdict format.

---

## Why this arc exists (hold it)

The reviewer-seat **Verdict format** block (`CAPTAIN_VERA.md` §6 L225-258; `CAPTAIN_ARGUS.md` + `CAPTAIN_CATO.md` parallel) is used as THREE things at once: (a) the block the seat ends its dispatch with (the **dispatch return**), (b) the `bw comment` posted to the ticket, and (c) the `<verdict-body>` that the §7 `printf` writes to the `.md`, **sha-round-trips, and `bw attach`es**. That block **includes `attach_status` / `attach_failure`** (VERA L254-255). But `attach_status`'s value is only known AFTER the `bw attach` — which in §7 happens AFTER the body is written and hashed. So whenever `attach_status` is filled into the body, the post-fill body diverges from the cited/attested sha by exactly that field. `save-verdict.md` clause (d) ALREADY says `attach_status` belongs in the dispatch return — the role-file §6 format silently contradicts it by putting the field inside the block that becomes the attested artifact.

The bug is **benign** (the attestation is valid against the byte-canonical bw-attached copy; build correctness was triple-corroborated on sos--yn2) and **non-blocking** — but it defeats the per-verdict sha tamper-evidence for any arc that **tracks verdicts in-tree** (a pattern that is now in use), and it bit the maiden arc's audit trail. Fix-now: make committed-sha == attested-sha hold going forward.

## Your one job

Make `attach_status` / `attach_failure` **dispatch-return-only** and make the **sha-attested verdict body frozen at the round-trip**, consistently across the three reviewer role files + the module — WITHOUT touching the byte-aligned §7 bash region's semantics. Specifically: separate the attested verdict body (printf'd → hashed → attached → optionally posted as a bw comment) from the post-attach dispatch-return addendum that carries `attach_status`/`attach_failure`. The attested body must NEVER contain a field whose value is only knowable after the attach.

## Full gauntlet (DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS). Standard POLYBIUS+PLINY team — a substrate-canon edit, not a custom agent/workflow, so no CHIRON/HAMILTON.

---

## Comms — async with Polybius_the_Stoa via bw (`stoa--*`)

Coordinate on the charter `stoa--x5t`. Polybius_the_Stoa (user-level owner) monitors + interjects; the floor-manager runs independent verification at each hand-back and relays up; the PRINCIPAL is NOT the relay — beadwork is. `bw comment <id> "text"` is positional, no `-m`; no backticks or `$()` in comment bodies. Run `bw prime` at activation. Every seat signs `[from: <NAME> | sid <session-id>]` (sid via the `whoami` skill).

---

## Read first

1. **Charter `stoa--x5t`** (the root-cause + evidence + this concrete plan).
2. **`substrate/CAPTAIN_VERA.md` §6 (L225-258) + §7 (the byte-aligned region L272+)** — the verdict format that conflates attested-body with dispatch-return, AND the printf/sha/attach bash region that must NOT change. Then the parallel **`CAPTAIN_ARGUS.md`** (attach_status L237; bash region L287+) and **`CAPTAIN_CATO.md`** (attach_status L200; bash region L252+).
3. **`substrate/modules/save-verdict.md`** — clause (d) (attach_status belongs in the dispatch return) + the byte-aligned region + the exit-code/attach-failure posture (which STAYS unchanged in substance).
4. **`substrate/modules/canonical-template-alignment.md`** — the P8 byte-alignment discipline the build-time `diff` enforces across the §7 region in all four homes.

---

## Design items — DAEDALUS resolves in Phase A (surface at the design hand-back)

- **DC1 — separate the attested body from the dispatch-return addendum (the core fix, all 3 reviewer role files).** Restructure each reviewer's §6 so the block that is (i) printf'd as `<verdict-body>`, (ii) sha-round-tripped, (iii) `bw attach`ed, and (iv) optionally posted as a bw comment EXCLUDES `attach_status`/`attach_failure`. Place `attach_status`/`attach_failure` in a clearly-labeled **dispatch-return-only addendum** the seat emits AFTER the §7 attach (it reports the attach outcome; it is never part of the sha-attested artifact). Keep the change identical in shape across VERA/ARGUS/CATO. State explicitly in each role file: the printf'd verdict body is FROZEN at the sha round-trip — never post-edit it (no post-attach body mutation).
- **DC2 — `save-verdict.md` reinforcement.** Make explicit that the `<verdict-body>` written by the §7 printf is frozen at the round-trip and that `attach_status`/`attach_failure` are dispatch-return-only (clause d), and that the bw-attached copy is the byte-canonical attested artifact. Reinforce, do not contradict, the existing durability contract.
- **DC3 — byte-aligned region must stay aligned (LOAD-BEARING constraint).** The §7 `printf → sha → attach` bash region (the SAVE-VERDICT-BYTE-ALIGNED-REGION between the BEGIN/END sentinels) should NOT need changing — it never wrote `attach_status` into the body. Confirm this. If the fix DOES require any change inside the sentinels, it MUST be re-aligned byte-identically across all four homes (save-verdict.md + the three role files) so the build-time P8 `diff` passes. Prefer a fix that leaves the region untouched.
- **DC4 — optional mechanical guard (design call).** Now that the attested body excludes the post-attach field, a `committed-sha == cited/attested-sha` check becomes meaningful. DAEDALUS decides whether to add one and where it lives (a close-gate / NOMOS-on-merge assertion, or a save-verdict note that the bw-attached copy is the attested canonical) — do NOT bolt a check into the byte-aligned region if it would force a re-align for marginal value. A documented invariant may be sufficient; justify the choice.
- **DC5 — honest stance + scope guard.** This is process/canon hygiene — `not threat-ratified` (no runtime attacker, no attack path; §35.5 carve-out). The bug was benign (attestation valid against the bw attachment). State plainly that the fix makes committed-sha == attested-sha hold for in-tree-tracked verdicts going forward; it does NOT change the durability contract, the attach-failure posture, the exit-code map, or the dispatch-return `attach_status` field itself (which stays — it just must not live in the attested body). Zero scope beyond the 3 role files + save-verdict.md (+ a guard if DC4 adds one).

---

## Deliverables (land together)

1. `CAPTAIN_VERA.md` + `CAPTAIN_ARGUS.md` + `CAPTAIN_CATO.md` — §6 restructured (attested body vs dispatch-return addendum), frozen-body statement added, parallel across all three.
2. `substrate/modules/save-verdict.md` — the DC2 reinforcement (+ DC4 guard if chosen).
3. Charter `stoa--x5t` updated with the landing SHA + per-DC disposition.

---

## Verification / Definition of done

- **Mechanical (close-gate):**
  - `attach_status`/`attach_failure` removed from the sha-attested verdict body in all 3 reviewer role files; present only in the dispatch-return addendum; the change is parallel/consistent across VERA/ARGUS/CATO.
  - The §7 byte-aligned region: UNCHANGED (the build-time P8 `canonical-template-alignment` `diff` over the four homes still passes) — or, if necessarily touched, re-aligned byte-identically across all four (P8 passes either way).
  - **`npm run gen-data` is deterministic + the FULL app test suite is green** (editing role files re-derives the whole roster — run the full suite as the regression bar, not just "this arc edited no X"; per the gen-data-regen + full-suite-verify disciplines). The author-gate + stop-hook + any verdict-format/corpus tests green.
  - A demonstration probe: a verdict authored under the NEW format, sha-round-tripped and committed, has committed-sha == cited/attested-sha (the sos--yn2 divergence cannot recur).
  - `Author=PRINCIPAL` + the §28.9 seat trailer on the build commit(s); **NOMOS CONFORMANT** on the final commit.
- **Judgment (honest stance):** a benign-but-real attestation-integrity hygiene fix; the durability contract / attach-failure posture / exit-code map / the dispatch-return `attach_status` field are all preserved unchanged. No over-claim.

---

## Out of scope (do NOT fold in)

- The §7 `printf → sha → attach` bash procedure semantics, the durability contract (`save-verdict.md` clause d / `MAJOR_PLINY.md` §5.16 retry-on-attach-fail), the exit-code map, and the dispatch-return `attach_status` FIELD itself — all STAY.
- The `sos--77g` AST read-only-guard hardening (a different stoa_of_science follow-up).
- Any change to verdict CONTENT/probe semantics, or to other role files beyond the 3 reviewers + save-verdict.md.
- The redeploy/propagation step (the-stoa `.claude/` self-apply + re-running `install.sh` into stoa_of_science) — that is the user-tier post-merge sequence, NOT a build deliverable.

---

## Discipline

- Full gauntlet — a substrate-canon edit to verdict-integrity-critical role files; treat like a public-API change. Standard POLYBIUS+PLINY (no CHIRON/HAMILTON).
- Keep the byte-aligned §7 region untouched if at all possible; if touched, re-align all four homes (P8 `diff` passes).
- Parallel/consistent across VERA/ARGUS/CATO — the same restructuring in all three (a divergence between reviewers is an automatic route-back).
- Run the FULL app test suite (gen-data deterministic + vitest) as the regression bar, not a narrow "we only edited role files" claim.
- One coherent slice — the 3 role files + save-verdict.md (+ an optional DC4 guard). No drive-by scope.
- bw syntax: positional `bw comment`, no backticks/`$()`; `bw prime` at activation; `--reason` on close.

## Suggested phasing

- **Phase A — design (DAEDALUS).** Resolve DC1-DC5; DC1 (the body/return separation) + DC3 (byte-alignment preserved) are load-bearing. Surface to the floor-manager for go/no-go before build.
- **Phase B — build (ADA).** Restructure the 3 reviewer §6 blocks + the save-verdict.md reinforcement (+ DC4 guard if chosen).
- **Phase C — verify (ARGUS/VERA/CATO + NOMOS).** P8 byte-alignment intact; gen-data deterministic + full suite green; the committed-sha == attested-sha demonstration; parallel across the 3 reviewers.
- **Phase D — ship.** Commit; update `stoa--x5t` with the SHA + dispositions; hand back to the floor-manager for relay-up to user-tier for the close-gate + merge. (Post-merge, user-tier runs the `.claude/` self-apply + re-runs `install.sh` into stoa_of_science.)

Standby, run.

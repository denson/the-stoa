# Arc 68 design-rev2 — Launcher-correctness (chain-of-command-at-launch · gauntlet-by-default · variable team composition)

**Ticket:** `stoa--pk4` · **Author:** Denson Smith (the PRINCIPAL) · **Seat:** CAPTAIN_DAEDALUS_the_stoa
**Builds on:** the-stoa main `3435fe3` (directive committed) + the SHIPPED Arc-67 identity layer (`stoa--p7c`, `stoa--reg`).
**Supersedes:** design-rev1 (this is a revision folding the ARGUS conditions C1–C7 + the BLESSED C2 resolution Option B + the FM say-path dependency).
**Status:** design hand-back for Polybius_the_Stoa / floor-manager go/no-go before Phase B (ADA build). C2 resolved (Option B, BLESSED by FM + user-tier). DC0/DC2 enforcement-model subsection marked ACK-PENDING (the PRINCIPAL prevention-vs-detection ack is in flight; expected outcome: advisory residual stands).

---

## §0 Changes from rev1 (changelog — one line per fold, for fast ADA/VERA/CATO diff)

- **Option B (C2/r4/RQ1 — BLESSED by FM + user-tier):** the bare-word SAY path stays a single bare word (`polybius`/`pliny`); the L1 chain preamble is injected ONLY on the arc/paste paths (which already force `-Layout Windows`). The say path establishes the chain VIA the role file (L2 canon, exactly what DC1 prescribes). Panes default preserved; no `-Layout Windows` forcing for standard say launches. §2.0 (L1 row + table), §2.1 (Edit B), §2.5, §6 W2, §7 RQ1 all updated. `stoa--waa` stays a separate P3 ticket, NOT pulled in.
- **FM say-path-not-thinner dependency (load-bearing):** §2.5 made concrete — the MAJOR_POLYBIUS.md + MAJOR_PLINY.md edits + §37 now SUBSTANTIVELY carry the chain (who reports to whom; PLINY surfaces to POLYBIUS not PRINCIPAL; gauntlet-by-default), not a bare `§37` cross-ref stub. NEW probe **P8** asserts the role files + §37 carry the say-path chain substantively (not just a cross-ref token).
- **C1 (r1, load-bearing):** P6(a) rewritten to FORCE + PROVE the bash-fallback branch writes a real `stoa--reg` row through git-bash `bw` on a **pwsh-bw-unreachable shim** (cannot pass via the `Get-Command` branch). The Windows-backslash-temp-path-into-git-bash-`bw` unknown is proven, not assumed; fix (a) converts `$tmp` to a git-bash-acceptable path form before `bash -lc`.
- **C3 (r5):** §2.2 / §5 / §6 record explicitly that DoD bullet 4 is met via the ACCEPTED ADVISORY branch (clause-(E)-text-reaches-model on the working Stop channel), NOT selective firing on the AR-7 shape — clause (E) fires on EVERY orchestrator Stop turn (W1/W4 residual). No wording implies selective AR-7 detection.
- **C4 (r2):** dropped the false "`$tmp` has no spaces by construction" rationale in §2.6; the real safety is the single-quote-wrap of the interpolands (Windows paths cannot contain a single-quote). Rationale corrected.
- **C5 (r3):** `record-seat.ps1` `$ticket` (a hardcoded constant at L58) is now PARAMETERIZED (`-Ticket` param, default `stoa--reg`) so P6(b) has a real injection point to drive the PATH-miss vs missing-ticket vs bw-error distinction. §2.6 + rewritten P6(b) specify it.
- **C6 (r6):** §37 inserts in `operating-disciplines.md` BETWEEN §36 (ends L1659) and the trailing un-numbered appendices (Agent-regime inverses L1660, Empirical lineage L1671), NOT at EOF. Verified the line numbers this turn. §2.5 placement instruction corrected.
- **C7 (r7):** a FRESH stop-hook test fixture for clause (E) is authored (none exists to extend — tests dir has only `run-author-gate-tests.sh` + fixtures + README). §2.2 + §2.8 + P5 specify the synthetic Stop event JSON shape + the assertion + the runner.
- **Ack-isolation (user-tier instruction):** all ack-sensitive DC0/DC2 enforcement-model content is now confined to **§2.0b (ACK-PENDING)**; the C1/C2/C4–C7 folds live in self-contained, ack-INDEPENDENT sections (§2.1, §2.5, §2.6, §2.8). If the PRINCIPAL ack changes the prevention-vs-detection model, only §2.0b needs revision.

---

## §1 Problem restatement

A Stoa team is brought up by `launch-team.ps1` + activation text. Today that text is *advisory*: a seat that is activated with an incomplete brief can (AR-7 / nws-iey, 2026-06-20) run SOLO as its own orchestrator, spawn CAPTAINs directly with no PLINY, and self-certify with one checker (no gauntlet). The launcher must STRUCTURALLY guarantee the by-the-book forge along three axes — (1) the chain PRINCIPAL→POLYBIUS→PLINY→CAPTAINs is established at launch so PRINCIPAL is never pointed at PLINY and seats are not co-equal panes; (2) the full gauntlet (DAEDALUS→ARGUS→ADA→VERA→CATO→NOMOS) is the default, opt-OUT requiring an explicit POLYBIUS/PRINCIPAL waiver, not a seat's silent solo opt-in; (3) team composition is variable — an arc designing custom **agents** pulls in MAJOR_CHIRON, an arc designing custom **workflows** pulls in MAJOR_HAMILTON (either/both/neither), placed in the chain, recorded to the ONE registry `stoa--reg`. Plus a folded-in live defect: `record-seat.ps1` calls `& bw` in pwsh where `bw` is on the bash PATH only, and its try/catch collapses CommandNotFound into the benign "no registry ticket" warning — a fail-OPEN that hid a total registry-write failure.

**Imported assumptions (named, per §6.1):**
- A1: "Structural" cannot mean "a seat is technically unable to emit non-gauntlet text" — a launcher + an activation paste are ultimately TEXT a seat could ignore (the directive DC0 says so explicitly). I read the PRINCIPAL's bar as *"the by-the-book path is the ONLY path the tooling lays down, the deviation is loud, recorded, and waiver-gated, and the AR-7 shape is detected after the fact by an independent checker"* — not "deviation is impossible." Where I claim structural vs advisory is itemized honestly in §2.0. **(This reading is what §2.0b ack-pending elaborates; the ack may sharpen prevention-vs-detection but does not change the C1/C2/C4–C7 folds.)**
- A2: the build runs in the `arc-68-build` worktree; the launcher edits are to `substrate/skills/...` source (deployed by `install.sh`), NOT to a live `.claude/`.
- A3: hooks deploy by the `*.sh` glob (`install.sh` L877, no HOOK_NAMES list) and default INERT (`ENABLE_HOOKS=0`, HARD SAFETY CONSTRAINT). Any new hook therefore needs NO `install.sh` name-list edit and ships disarmed — consistent with the existing convention.
- A4: `record-seat.ps1` ships *beside* `launch-team.ps1` inside the `team-launcher` skill dir; it is NOT a separate `SKILL_NAMES` entry. No `install.sh` skill-list edit is needed for the PATH fix.

---

## §2 Approach

### §2.0 DC0 — STRUCTURAL vs CONVENTIONAL: the layered model (ack-independent structure)

**Decision: a LAYERED model — three structural layers + one honestly-named advisory residual.** No single mechanism reaches the PRINCIPAL's "structurally impossible" bar; the layers compound so the by-the-book path is the default the tooling lays down AND the AR-7 deviation is loud + recorded + independently detected. **The LAYER STRUCTURE below is ack-independent (it is the design's spine); the ENFORCEMENT-CLASS wording for L3 / the residual — prevention-vs-detection framing — is isolated in §2.0b ACK-PENDING.**

| Layer | Mechanism | Enforcement class | What it actually forces |
|---|---|---|---|
| **L1 — Activation injection** | launcher injects a fixed **chain-of-command preamble** into the **arc + paste** seat activation prompts (the paths that already force `-Layout Windows`). The **say path stays a bare word** and inherits the chain via L2 (Option B). | **Structural-at-launch** (the launcher cannot emit an arc/paste seat without the preamble; it is concatenated in code, not authored per-arc) | Every arc/paste-launched seat is TOLD its place + who it reports to; the say-launched seat gets the same chain via the role file it loads. A seat *can* still ignore text → not absolute. |
| **L2 — Role-file canon** | the chain + gauntlet-by-default land as `operating-disciplines.md` §37 canon, **substantively carried** (not just cross-ref'd) in `MAJOR_POLYBIUS.md` / `MAJOR_PLINY.md`; the SAY-TRIGGER default loads the role file, so the **bare-word say path establishes the full chain via canon** — exactly what directive DC1 prescribes. | **Structural-via-canon** (any activation that reads the role file inherits it; this is the SOLE chain-establishment path for the bare-word say launch under Option B, so the canon MUST genuinely carry the chain — §2.5) | The default say activation cannot come up WITHOUT the chain in its loaded context. |
| **L3 — Recorded signal + independent detector** | the launcher writes a `gauntlet`/`composition` field into the `stoa--reg` row at launch; the existing **Stop self-check hook** gains clause **(E)** on the CONFIRMED-WORKING `decision:block`+`reason` channel. | *(enforcement-class wording → §2.0b ACK-PENDING)* | The deviation is SURFACED every orchestrator-Stop turn; correction is the seat's. |
| **Residual (advisory, NAMED)** | a determined seat can still ignore the preamble, run solo, and dismiss the Stop-hook flag | *(enforcement-class wording → §2.0b ACK-PENDING)* | NOT closed. Honestly named (§6 weak point W1). |

**Why this shape:** it reuses the proven Arc-46/50/63 hook pattern (Stop `decision:block`+`reason` is the only confirmed-working injection channel; PostToolUse `additionalContext` is BROKEN #55889 — so the detector MUST ride Stop, not PostToolUse). It adds NO new armed-by-default surface (hooks ship INERT). It avoids over-claiming (see §2.0b + §6 W1).

**DC0 drives DC1 (L1+L2), DC2 (L3 detector + recorded signal), DC3/DC4 (the composition is the same recorded signal extended).**

### §2.0b DC0/DC2 ENFORCEMENT MODEL — prevention vs detection (ACK-PENDING — the ONLY ack-sensitive subsection)

> **ACK-PENDING NOTICE.** This subsection is the single content unit contingent on the PRINCIPAL prevention-vs-detection ack (in flight via user-tier). The expected outcome is that the advisory residual **stands** — both tiers judged it DoD-conformant (DoD bullet 4 explicitly accepts "honestly document the residual convention-only gap if the mechanism is advisory"). If the ack instead demands prevention (e.g. a hard pre-action block rather than a Stop-turn detector), ONLY this subsection is revised; the C1/C2/C4–C7 folds in §2.1/§2.5/§2.6/§2.8 are ack-independent and final. ADA: build §2.1/§2.5/§2.6/§2.8 against the conditions regardless; treat THIS subsection's enforcement wording as the releasing-go/no-go's last word.

**Enforcement-class wording for the §2.0 table rows L3 + Residual (expected-standing model):**

- **L3 enforcement class = Structural-detection, advisory-correction.** Clause (E) fires reliably on the working channel; it cannot *prevent* the dispatch, only flag it at turn-end — bounded, fail-open, once-per-turn, exactly like clauses A/D today. **It fires on EVERY orchestrator-class Stop turn (no transcript classification of "dispatched-CAPTAINs-without-PLINY"); it does NOT selectively detect the AR-7 shape (C3/r5 — see §2.2 + §6 W1/W4).**
- **Residual enforcement class = Convention-only.** A determined seat can ignore the preamble, run solo, and dismiss the Stop-hook flag. The mitigation is detection (L3) + the loud-recorded-deviation property, NOT impossibility. Honestly named (§6 W1).
- **The PRINCIPAL's bar (A1 reading), restated as the claim the go/no-go weighs:** "the by-the-book path is the ONLY path the tooling lays down; the deviation is loud, recorded, waiver-gated, and detected-on-the-working-channel after the fact" — this is DETECTION + recorded-deviation, NOT PREVENTION. §35.5's honest-claim discipline is the canon precedent for naming this rather than papering it. **If the ack demands prevention, the revision lands HERE (e.g. swap clause (E) for a PreToolUse Agent-dispatch gate that hard-blocks a POLYBIUS-class seat from spawning CAPTAINs absent a recorded PLINY) — flagged as the localized rework surface, not built unless the ack so directs.**

### §2.1 DC1 — chain-of-command establishment (ack-independent)

**Edit A (launcher: shared preamble builder).** Add a helper + a fixed template above `Get-SeatPrompt`:

- `launch-team.ps1` — insert after the `$recordSeat` line (~L109), a script-scope here-string `$ChainPreamble` keyed per role, and a function `Get-ChainPreamble([string]$role, [string]$slug)`:

```
CHAIN OF COMMAND (Stoa, established at launch — do not deviate):
  PRINCIPAL -> POLYBIUS (chief/floor-manager) -> PLINY (orchestrator) -> CAPTAINs.
You are <ROLE_LINE>.   # role-specific line, see below
You coordinate via bw (positional `bw comment`), NOT by the PRINCIPAL relaying messages.
The full gauntlet (DAEDALUS->ARGUS->ADA->VERA->CATO->NOMOS) is the DEFAULT; running solo
with one checker requires an explicit POLYBIUS/PRINCIPAL waiver recorded on bw.
```

Role-specific `<ROLE_LINE>` (selected by `$seat.Role`):
- `floor-manager` → `POLYBIUS_<slug>: you SUPERVISE PLINY (direct + independently verify hand-backs via bw). The PRINCIPAL/user-tier addresses YOU; you never dispatch CAPTAINs yourself.`
- `orchestrator` → `PLINY_<slug>: you take direction from + surface to POLYBIUS via bw, NOT the PRINCIPAL. You spin up the CAPTAINs and run the gauntlet.`
- `team-architect` (CHIRON) / `workflow-architect` (HAMILTON) → see §2.3.

**Edit B (Option B — wire the preamble into the ARC + PASTE paths ONLY; leave the SAY path a bare word).** This is the BLESSED C2 resolution. In `Get-SeatPrompt` (L169-173):

- **`$seat.Prompt` (arc path):** PREPEND the preamble — `return (Get-ChainPreamble $seat.Role $Slug) + "`n" + [string]$seat.Prompt`. The arc path already forces `-Layout Windows` (L122-125), so the multi-line preamble passes robustly through the per-seat pwsh window (which quotes — L205-212).
- **paste path (`-AutoPaste`/`$seat.Paste`, the Windows per-seat pwsh path L205-212):** the brief content is read from the paste file; the preamble is prepended to that content in the Windows path. The paste path is Windows-only by construction (`-AutoPaste` warns + falls back outside `-Layout Windows`, L165-167), so it inherits the same robust quoting.
- **say path (`$Activation -eq 'say' -and $seat.Say`):** **return the bare word UNCHANGED** — `return [string]$seat.Say`. **NO preamble prepend. NO `-Layout Windows` force for say launches.** The Panes default (L72) is preserved exactly as today. **The chain is established for this path via L2 canon (§2.5):** the CLAUDE.md say-trigger loads `MAJOR_POLYBIUS.md`/`MAJOR_PLINY.md` as its first action, and those role files (post-arc) substantively carry the chain (who reports to whom, surface-up direction, gauntlet-by-default) + reference §37. This is exactly directive DC1's "the SAY-TRIGGER default ALSO establishes the chain via the role file."

> **REMOVED from rev1 (C2/Option B):** the rev1 Edit-B say-path preamble-prepend AND the rev1 say-path "force `-Layout Windows` when preamble injected" guard are GONE. Rationale: a multi-word say prompt re-splits unquoted in the wt panes path (L191 `$wtArgs += $p`, the `stoa--waa` break), so prepending a preamble to the say word would have forced Windows on every standard say launch — silently abolishing the documented Panes default (the r4 finding). Option B sidesteps this entirely by keeping the say path single-token. **`stoa--waa` (the wt-pane unquoted-resplit fix) is therefore NOT needed by this arc and stays a separate P3 ticket.**

**Edit C (L2 canon — the say-path's SOLE chain-establishment carrier under Option B).** Because Option B leans the say path's ENTIRE chain-establishment on the role file, `MAJOR_POLYBIUS.md`/`MAJOR_PLINY.md` + §37 MUST substantively carry the chain — not a bare cross-ref. See §2.5 (made concrete + the say-path-not-thinner dependency + probe P8).

### §2.2 DC2 — gauntlet-by-default mechanism (ack-independent mechanics; enforcement framing → §2.0b)

Three coordinated pieces:

**Piece 1 — recorded signal (launcher → registry).** Extend the per-seat launch record with a launch-level `gauntlet` field. In the `record-seat` call (L237) the launcher passes a new `-Gauntlet` value; default `required`. A solo/waiver launch sets `-Gauntlet waived:<reason>`. (Schema add is additive — see DC4 §2.4; does NOT reopen the Arc-67 schema, it adds optional fields.)

**Piece 2 — activation default (L1 preamble + L2 canon).** The preamble's gauntlet line names the full gauntlet as the default in every arc/paste seat's loaded context; the say-launched seat gets the gauntlet-by-default from §37 + the role file (L2). Opt-out is textual + must cite a waiver.

**Piece 3 — independent detector (NEW Stop-hook clause E, the structural-detection layer).** Add a clause **(E)** to `stop-self-check.sh`'s `REASON`, appended the SAME way clause (D) is appended (L106-115) and riding the SAME `decision:block`+`reason` working channel as clauses A/B/C/D (L120):

```
(E) If THIS turn you (a POLYBIUS- or PLINY-class seat) dispatched CAPTAINs via the Agent tool,
    confirm a PLINY orchestrator is in the chain (you are not a POLYBIUS that spawned CAPTAINs
    directly) AND the gauntlet shape is the full DAEDALUS->ARGUS->ADA->VERA->CATO->NOMOS unless an
    explicit POLYBIUS/PRINCIPAL waiver is recorded on bw. A solo-with-one-checker close is the
    AR-7 failure shape (stoa--pk4) — if that is what happened, STOP and route through the gauntlet
    or record the waiver before ending the turn. (Legitimate early-arc solo build-sessions where
    no CAPTAINs exist: this does not apply — proceed.)
```

- **C3/r5 — HONEST RECORD (ack-independent fact; weighed by the go/no-go in §2.0b).** Clause (E) is a **reminder-class** clause (matching A's "treat as no-op if NOMOS not deployed" degradation), NOT a transcript-parsing classifier. It is appended to `REASON` and therefore **fires on EVERY orchestrator-class Stop turn**, regardless of whether CAPTAINs were actually dispatched-without-PLINY this turn. The hook does NOT mechanically inspect the transcript to *prove* the AR-7 shape occurred. **Therefore DoD bullet 4 ("demonstrate the mechanism fires on the AR-7 failure shape") is met via the ACCEPTED ADVISORY branch — the clause-(E) text REACHES THE MODEL on the working Stop channel on every orchestrator Stop turn — NOT via selective detection of the AR-7 shape.** The selective sense (fire only when the AR-7 shape actually happened) is the unmechanized residual W1; nothing in this design claims it. VERA's P5 asserts exactly the advisory bar (clause text present in the emitted `decision:block` JSON), the same falsifiable bar clauses A/D meet.
- **No new hook file** — clause (E) extends the existing `stop-self-check.sh`. Ships INERT with the rest (ENABLE_HOOKS=0). FAIL-OPEN preserved. **A FRESH stop-hook test fixture is authored for clause (E) — see §2.8 (C7).**

**Waiver path (opt-out, gated):** a non-gauntlet launch is `launch-team.ps1 ... -GauntletWaiver "<reason>"` (new switch), which (a) records `gauntlet=waived:<reason>` to the row and (b) the preamble's gauntlet line is replaced with `GAUNTLET WAIVED by launch flag: <reason> (POLYBIUS/PRINCIPAL-authorized).`. Absent the flag, default is `required`. A *seat* cannot grant itself the waiver — only the launch flag (driven by POLYBIUS/PRINCIPAL) writes it. That is the "opt-out requires explicit waiver, not silent solo opt-in" guarantee, at the structural-at-launch tier. (Note: the waiver line lands in the preamble, which is on arc/paste paths only under Option B; a waived SAY launch records `gauntlet=waived:<reason>` to the row + relies on the role-file gauntlet canon — a waived launch is an explicit POLYBIUS/PRINCIPAL action that will not use the bare-say convenience path in practice. Named in §6 W2.)

### §2.3 DC3 — variable composition model + chain placement (ack-independent)

**Composition model — named compositions keyed to the WORK (precise trigger, NOT "design-heavy"):**

Add a `-Composition` param to `launch-team.ps1`:

```
[ValidateSet('standard','custom-agent','custom-workflow','custom-agent+workflow')]
[string] $Composition = 'standard'
```

Seat-set per composition (built where the default `$Seats` is constructed, L128-141, BEFORE the `-OnlySeat` filter so the existing floor-manager-first single-seat launch still works):

| `-Composition` | Seats added beyond POLYBIUS+PLINY | Trigger (precise) |
|---|---|---|
| `standard` | none | default; Arc 68 itself uses this |
| `custom-agent` | **MAJOR_CHIRON** (team-architect) | the arc DESIGNS custom agents |
| `custom-workflow` | **MAJOR_HAMILTON** (workflow-architect) | the arc DESIGNS custom workflows |
| `custom-agent+workflow` | CHIRON + HAMILTON | the arc designs both |

**Are CHIRON/HAMILTON launcher-spun terminal seats or PLINY-dispatched? → launcher-spun TERMINAL seats.** Rationale (ARGUS-DISCHARGED against role files): both `MAJOR_CHIRON.md` and `MAJOR_HAMILTON.md` say they "live at a top-level Claude Code session in a project-tier directory; engaged at design-time" — i.e. MAJOR-rank terminal seats, not `Agent`-tool sub-agents. They cannot be PLINY-dispatched. So the launcher spins them up as terminal seats, same as POLYBIUS/PLINY.

**WHERE in the chain (placement):** CHIRON/HAMILTON answer to **POLYBIUS** (both role files §1: "You answer to MAJOR_POLYBIUS"). They are **design-time peers that feed POLYBIUS**, parallel to PLINY, not under PLINY:

```
PRINCIPAL -> POLYBIUS ──┬── PLINY -> CAPTAINs            (run-time pipeline)
                        ├── CHIRON  (design-time: the cast)     ┐ answer to POLYBIUS;
                        └── HAMILTON(design-time: choreography) ┘ co-design; step back, then PLINY runs it
```

The CHIRON/HAMILTON `<ROLE_LINE>` in the preamble:
- CHIRON → `MAJOR_CHIRON: design-time team-architect. You answer to POLYBIUS; you co-design the cast with HAMILTON, then step back so PLINY runs the team. You do NOT dispatch CAPTAINs.`
- HAMILTON → `MAJOR_HAMILTON: design-time workflow-architect. You answer to POLYBIUS; you co-design the choreography with CHIRON, then step back so PLINY runs the team.`

**How the launcher PLACES them (activation):** CHIRON/HAMILTON have **no CLAUDE.md say-trigger** (ARGUS-DISCHARGED: no `chiron`/`hamilton` bare-word in any CLAUDE.md). So the say-word path does NOT work for them — the launcher MUST seed a full activation prompt naming the role file. Add seat definitions analogous to the `-ArcId` arc seats (L118-121):

```powershell
# in the composition block, when $Composition includes custom-agent:
@{ Name = "CHIRON_$Slug"; Role = 'team-architect';
   Prompt = "Read .claude/MAJOR_CHIRON.md and assume the team-architect role for $Slug" + $(if($ArcId){" on arc $ArcId; read your brief: git show beadwork:attachments/$ArcId/HUMAN_paste-chiron-$ArcId-instruction.md and follow it."}else{"."}) }
# analogous HAMILTON_$Slug with Role='workflow-architect' + MAJOR_HAMILTON.md
```

(These carry `$seat.Prompt`, so the §2.1 Edit-B arc-path preamble-prepend applies — they inherit the chain preamble with their CHIRON/HAMILTON `<ROLE_LINE>`.) Because they carry full multi-word prompts, they REQUIRE `-Layout Windows` exactly like the `-ArcId` path — extend the L125 force-Windows guard to also fire when `$Composition -ne 'standard'`. **(This is the arc/paste class, which under Option B already forces Windows — so no NEW say-path UX regression is introduced by composition launches; the Windows-forcing is an explicit property of the multi-word-prompt class only.)**

**Record the composition to `stoa--reg`** — each composed seat is recorded by the existing post-launch `record-seat` loop (L230-252); it already records every seat in `$Seats`, so CHIRON/HAMILTON are recorded automatically once added to `$Seats`. The NEW fields (`composition`, `gauntlet`, `chain_role`) are passed through — see DC4.

### §2.4 DC4 — registry + manifest coordination (ONE registry) (ack-independent)

**Reuse `stoa--reg`; ADD optional fields (additive, does NOT rebuild the Arc-67 schema).** `record-seat.ps1`'s `$row` (L92-102) gains three optional fields:

```
composition = $Composition   # 'standard'|'custom-agent'|'custom-workflow'|'custom-agent+workflow'  (default 'standard')
gauntlet    = $Gauntlet      # 'required' | 'waived:<reason>'                                       (default 'required')
chain_role  = $ChainRole     # 'floor-manager'|'orchestrator'|'team-architect'|'workflow-architect' (its place in the chain; defaults to $Role)
```

New `record-seat.ps1` params: `[string]$Composition='standard'`, `[string]$Gauntlet='required'`, `[string]$ChainRole=''` (falls back to `$Role`). All optional with safe defaults → **a caller that does not pass them (incl. the desktop self-record path + the builder-deploy `u--9s2` follow-on) still writes valid rows** (older rows simply omit the new keys; JSONL tolerates heterogeneous rows). This is the non-divergence guarantee the directive asks for: `u--9s2`'s cookie-cutter can adopt the SAME `record-seat.ps1` + SAME registry and either set or omit these fields.

**Manifest-shape coordination note (for `u--9s2`, not built here):** the composition is expressed PER-SEAT (each row carries `composition`+`chain_role`), NOT as a separate manifest object. This keeps ONE registry, one row-shape; a "composition" is just the set of alive rows sharing a `(project, machine, launched-at-window)` with the same `composition` value. No second artifact. (W3 names the read-side weak point.)

### §2.5 Canon edits (operating-disciplines.md §37 + SUBSTANTIVE role-file chain — the say-path-not-thinner dependency)

> **C6/r6 PLACEMENT (verified this turn — exact line numbers):** `operating-disciplines.md` is 1681 lines. §36 ("Threat-remediation escalation") is the LAST NUMBERED section; its content ends at L1656, followed by a `---` horizontal rule at L1658. Two UN-numbered appendices then follow: **"## Agent-regime inverses (the positive framing)" at L1660** and **"## Empirical lineage" at L1671**. The new §37 MUST be inserted **at L1659 (between §36's trailing `---` at L1658 and the appendix at L1660)** — NOT at EOF. Appending at EOF would break the numbered sequence by burying §37 after the appendices. (rev1's "free at EOF" assumption is OVERTURNED.)

Add a new section **`## 37. Launcher-correctness — chain-of-command-at-launch, gauntlet-by-default, variable composition`** at the L1660 insertion point. Three subsections:

- **37.1 Chain-of-command at launch** — PRINCIPAL→POLYBIUS→PLINY→CAPTAINs; PRINCIPAL never addresses PLINY; seats are not co-equal panes; the launcher injects the L1 preamble on arc/paste paths + the say-trigger default establishes the chain via the role file (L2). Cross-ref the L1/L2 layers + §2.0b enforcement framing.
- **37.2 Gauntlet-by-default** — full gauntlet is the default; opt-out requires an explicit POLYBIUS/PRINCIPAL waiver recorded on bw (`-GauntletWaiver` → `gauntlet=waived:<reason>`); a seat cannot self-grant solo. The Stop-hook clause (E) is the independent detector (honest: detection + surface, not prevention; fires every orchestrator Stop turn — C3). Cross-ref §6 (redundancy IS the safety property) + §35.5 (honest-claim precedent).
- **37.3 Variable team composition** — the precise trigger (custom-agent→CHIRON, custom-workflow→HAMILTON, either/both/neither; NOT generic "design-heavy"); CHIRON/HAMILTON are launcher-spun terminal design-time seats answering to POLYBIUS; recorded per-seat to `stoa--reg`.

**SUBSTANTIVE role-file chain edits (the FM say-path-not-thinner dependency — load-bearing under Option B).** Because the bare-word say path's ONLY chain-establishment is the role file it loads, these edits MUST state the chain SUBSTANTIVELY (who reports to whom, the surface-up direction, the gauntlet-by-default), NOT merely a `§37` cross-ref token:

- **`MAJOR_POLYBIUS.md`** — at the chain/activation section (§9 area), add a substantive paragraph (not a stub):
  > "CHAIN OF COMMAND (established at launch): PRINCIPAL → you (POLYBIUS, chief/floor-manager) → PLINY (orchestrator) → CAPTAINs. The PRINCIPAL/user-tier addresses YOU; you supervise PLINY (direct + independently verify hand-backs via bw) and any design-time architects (CHIRON for custom agents, HAMILTON for custom workflows) the composition includes — they answer to you, parallel to PLINY. You never dispatch CAPTAINs yourself. The full gauntlet is the default; a solo/non-gauntlet run requires YOUR explicit waiver recorded on bw. The launcher establishes this chain at launch (L1 preamble on arc/paste; this canon on the say path). Full canon: `operating-disciplines.md` §37."
- **`MAJOR_PLINY.md`** — at the §17/§41 area where "you receive directives from MAJOR_POLYBIUS" is stated, add a substantive paragraph (not a stub):
  > "CHAIN OF COMMAND (established at launch): you (PLINY, orchestrator) take direction from and SURFACE TO POLYBIUS via bw — NOT the PRINCIPAL. You spin up the CAPTAINs and run the full gauntlet (DAEDALUS→ARGUS→ADA→VERA→CATO→NOMOS), which is the DEFAULT; running solo with one checker requires an explicit POLYBIUS/PRINCIPAL waiver recorded on bw — you do not self-grant it. The launcher establishes this chain at launch (L1 preamble on arc/paste; this canon on the bare-word say path). Full canon: `operating-disciplines.md` §37."

These paragraphs are what makes the say-path NOT thinner: a seat launched by the bare word `polybius`/`pliny` loads its role file as the say-trigger's first action and reads the FULL chain there, identical in substance to what the L1 preamble carries on the arc/paste paths. **Probe P8 asserts this substantively (not just a `§37` token).**

### §2.6 The record-seat pwsh-PATH defect fix (folded-in, DC-adjacent) (ack-independent)

**Coupled fixes at the call site — TARGETED, not a registry/schema rebuild. Folds C4 (rationale) + C5 (parameterize the ticket).**

**C5/r3 — parameterize the ticket (gives P6(b) a real injection point).** `record-seat.ps1` L58 hardcodes `$ticket = 'stoa--reg'`. Replace with a param + default so a probe can drive a bogus ticket without editing the script under test:

```powershell
# in param(...) block, after the existing params:
[string] $Ticket = 'stoa--reg'
# ... and at L58, REMOVE the hardcoded `$ticket = 'stoa--reg'`; use $Ticket throughout:
$ticket = $Ticket
```

(All existing uses of `$ticket` — the `$readPath`, the attach call, the warning strings — now resolve to `$Ticket`. Default preserves every existing caller's behavior; a probe passes `-Ticket bogus--nope` to force the exit-`<N>` real-attach-failure branch distinctly from the PATH-miss branch.)

**Fix (a) — make `bw` pwsh-resolvable AND prove the bash-fallback handles the Windows temp path (C1/r1).** Replace the bare `& bw attach ...` (`record-seat.ps1` L118-128) with a resolution that finds `bw` even when it is on the bash PATH only, and that converts the Windows backslash temp path to a git-bash-acceptable form before `bash -lc`:

```powershell
# Resolve bw: pwsh PATH first, else the bash PATH (git-bash / WSL installs bw there on Windows).
$bwCmd = Get-Command bw -ErrorAction SilentlyContinue
if ($bwCmd) {
  & $bwCmd.Source attach $ticket $tmp --name $attachName
  $bwExit = $LASTEXITCODE
} else {
  # bw not on the pwsh PATH (the affected-machine case — bw is on the bash PATH only).
  $bash = Get-Command bash -ErrorAction SilentlyContinue
  if ($bash) {
    # git-bash bw does NOT reliably accept a Windows backslash path (C:\Users\...\Temp\...).
    # Convert to a git-bash-acceptable POSIX form: backslashes->slashes, C: -> /c.
    # (cygpath is the robust tool if present; else a deterministic transform.)
    $cyg = Get-Command cygpath -ErrorAction SilentlyContinue
    if ($cyg) {
      $tmpBash = (& $cyg.Source -u $tmp).Trim()
    } else {
      $tmpBash = $tmp -replace '\\','/' -replace '^([A-Za-z]):','/$1'  # C:/... -> /C/...
    }
    # Single-quote-wrap the interpolands (the real injection-safety; see rationale below).
    & $bash.Source -lc "bw attach '$ticket' '$tmpBash' --name '$attachName'"
    $bwExit = $LASTEXITCODE
  } else {
    $bwExit = $null   # genuine: no bw resolvable any way -> distinct from a bw error
  }
}
```

> **C4/r2 — CORRECTED rationale (the false "no spaces by construction" claim is DROPPED).** `$tmp = Join-Path ([System.IO.Path]::GetTempPath()) "stoa-seat-registry.jsonl"` (L108). `GetTempPath()` includes the user-profile dir, which CAN contain a space (a Windows username with a space). So `$tmp` is NOT space-free by construction. **The actual safety is the SINGLE-QUOTE WRAP of `'$tmpBash'` / `'$ticket'` / `'$attachName'` inside the `bash -lc` string: a Windows path cannot contain a single-quote character, so the single-quoted interpoland is safe against word-splitting regardless of embedded spaces.** A future edit that drops the single-quotes reintroduces the break — the quotes are load-bearing, not decorative. (§8.6 destructive-path hygiene note: the attach is not a destructive `rm`/overwrite-by-`$VAR` op; it writes the stored attachment path verbatim. The probe path is a fixed-literal filename.)

**Fix (b) — fail-LOUD with the REAL error; distinguish the three cases** (replace the collapsed catch L118-128, wrapping the resolve+invoke block above):

```powershell
$attachOk = $false; $failReason = ''
try {
  # ... the resolve+invoke block (fix a) above sets $bwExit ...
  if ($bwExit -eq 0)        { $attachOk = $true }
  elseif ($null -eq $bwExit){ $failReason = "bw NOT FOUND on the pwsh PATH or via bash — this is a PATH/resolution failure, NOT a missing-ticket case. On this machine bw is on the bash PATH only; the launcher must invoke it pwsh-resolvably (Arc 68 / stoa--pk4)." }
  else                      { $failReason = "bw attach to '$ticket' exited $bwExit (e.g. no such ticket on THIS bw store, or a bw error). If '$ticket' genuinely does not exist on this workspace's bw store, this is the benign no-registry-ticket case; otherwise it is a real attach failure." }
} catch {
  $failReason = "bw attach threw: $($_.Exception.Message)"
}
if (-not $attachOk) {
  Write-Warning "record-seat: could not record seat '$Seat' to '$ticket'. $failReason"
  exit 1
}
```

- The **mis-attribution is the named hazard** — fix (b) ensures a CommandNotFound/PATH-miss is reported AS a PATH failure (not "expected on a workspace without the registry ticket"), so a total registry-write failure can never again hide behind the benign label.
- **Launcher side (`launch-team.ps1` L242/L246):** update the two warning strings so they no longer assert "expected/benign on a workspace without the stoa--reg ticket" unconditionally — instead echo `record-seat`'s own exit + let its specific message stand. Change to: `Write-Warning "record-seat.ps1 returned non-zero for seat '$name' (see its message above for the specific cause: PATH-miss vs missing-ticket vs bw error); seat LAUNCHED but NOT recorded."`. (The launch stays best-effort — never rethrow — but the cause is now legible.)

**Scope guard:** this touches ONLY the bw-invocation + error-attribution + the `-Ticket` param at the `record-seat.ps1` call site (L46-54 param block, L58, L118-128) + the two launcher warning strings + new optional params from DC4. It does NOT touch the read-modify-rewrite logic (L66-111), the registry schema beyond the additive DC4 fields, or the `bw attach --name` path convention — staying clear of the "do not rebuild the Arc-67 identity layer" out-of-scope line.

### §2.7 install.sh + consistency sweep (ack-independent)

- **install.sh:** NO name-list edit needed — `record-seat.ps1` ships beside `launch-team.ps1` in the existing `team-launcher` skill (in `SKILL_NAMES`); the Stop-hook clause is an edit to an existing hook (deployed by the `*.sh` glob). **Verify** the dry-run still reports the same skill/hook counts (probe P7).
- **Consistency sweep (no stale framing):** grep the touched files for stale "two-seat default" / "PRINCIPAL coordinates the panes" / co-equal-panes framing and reconcile:
  - `team-launcher/SKILL.md` L4 (description "POLYBIUS + PLINY by default") + L29 → add the variable-composition + chain-establishment note; keep POLYBIUS+PLINY as the *standard* composition, not "the" fixed default. **Also note the Option-B property: the say path stays bare-word (Panes default preserved); the chain preamble rides arc/paste launches only.**
  - `gauntlet-setup/SKILL.md` — reconcile §"Mandatory content checklist" with the launcher's new structural guarantees: the chain-of-command + gauntlet-default are now launcher-injected (L1, arc/paste) + canon (L2, all paths), so the human-authored brief checklist becomes a *belt-and-suspenders confirm*. Add a line pointing at §37 + the `-Composition`/`-GauntletWaiver` flags. Update failure-mode #8 ("chain-of-command set up wrong") to note the launcher now establishes it.
  - `launch-team.ps1` synopsis/.NOTES — document the new `-Composition`, `-GauntletWaiver`, the chain preamble (arc/paste only), the say-path-bare-word/Panes-preserved property, and the CHIRON/HAMILTON placement.

### §2.8 Fresh stop-hook test fixture for clause (E) (C7/r7 — authored, not extended)

> **C7/r7 (verified this turn):** `substrate/hooks/tests/` contains ONLY `run-author-gate-tests.sh` (PreToolUse author-gate), a `fixtures/` dir, and `README.md`. There is NO existing stop-self-check test to extend. Author a FRESH fixture + runner. `_hooklib.sh` provides `read_stdin_event` / `event_field` / `allow`; `stop-self-check.sh` reads the Stop event JSON from stdin and emits `{"decision":"block","reason":...}` (L120).

Author:
1. **A synthetic Stop event JSON fixture** (`substrate/hooks/tests/fixtures/stop-event-orchestrator.json`) with the Stop-event shape the hook reads via `event_field`:
```json
{ "session_id": "stoa-pk4-clauseE-fixture", "transcript_path": "/tmp/stoa-pk4-fixture-transcript.txt", "cwd": "/tmp/stoa-pk4-fixture-cwd", "stop_hook_active": false }
```
   (`transcript_path` points at a fixture file the test creates with a known size so the turn-key/sentinel is deterministic; `stop_hook_active:false` so the hook does not early-`allow` at L48-49.)
2. **A runner** (`substrate/hooks/tests/run-stop-self-check-tests.sh`, modeled on `run-author-gate-tests.sh`) that:
   - **Assertion 1 (clause E present, first call blocks):** `echo "$(cat fixtures/stop-event-orchestrator.json)" | bash ../stop-self-check.sh` → assert stdout parses as JSON with `.decision == "block"` AND `.reason` CONTAINS the clause-(E) sentinel string `solo-with-one-checker close is the AR-7 failure shape`.
   - **Assertion 2 (infinite-block guard, second same-turn call allows):** run the SAME event a SECOND time (same session_id + same transcript size → same turn-key) → assert the output is the `allow` shape (no `decision:block`, or the documented allow output), proving the once-per-turn sentinel intact.
   - CLEANUP: remove the fixture transcript + the per-turn sentinel the run created (fixed-literal paths under the fixture/tmp dir).

This fixture is what P5 runs against. It is authored as part of the build (ADA), not assumed to exist.

---

## §3 Out of scope (deliberately not designed)

- **Re-building the Arc-67 identity layer** (mint/name/record/whoami/sign-everywhere/`stoa--reg` schema) — reused; only additive optional fields added. *Reason:* directive out-of-scope line 1.
- **The builder-deploy cookie-cutter BUILD (`u--9s2`)** — only kept the registry+`record-seat.ps1` adoptable (DC4). *Reason:* directive out-of-scope line 2.
- **Cross-machine `--resume`/cloud-sync** — sessions are local-only (verified Arc-67). *Reason:* directive out-of-scope line 3.
- **A full `operating-disciplines.md` audit** beyond §37's three disciplines. *Reason:* directive out-of-scope line 4.
- **The `apply.sh`/`install.sh` seat-trailer signing gap (`stoa--tg7`)** — design touches no commit sites. *Reason:* directive out-of-scope line 5.
- **The wt-pane unquoted-resplit fix (`stoa--waa`)** — Option B keeps the say path single-token, removing the ONLY reason this arc would have needed it. *Reason:* stays a separate P3 ticket; not pulled into this arc.
- **A mechanical transcript-parsing classifier** that PROVES "POLYBIUS dispatched CAPTAINs without a PLINY." *Reason:* the Stop hook reads its event JSON, not the full transcript of Agent dispatches; a reliable classifier is a larger detection arc. Named as residual W1, not built.
- **A PreToolUse Agent-dispatch hard-block (prevention)** — only built IF the PRINCIPAL ack (§2.0b) demands prevention over detection; not in the expected-standing model. *Reason:* ack-pending; localized to §2.0b.
- **Arming hooks** (`ENABLE_HOOKS=1`) — HARD SAFETY CONSTRAINT; hooks ship INERT.

---

## §4 Verification probes (concrete, VERA-runnable)

All run from the `arc-68-build` worktree root unless noted. `-DryRun` can ONLY prove printed-command + activation shape (it early-returns before launch AND before record — directive DoD note); the REAL round-trip is exercised by calling `record-seat.ps1` directly without spawning agents.

**P1 — DryRun command + activation shape (custom-agent composition).**
`& ./skills/team-launcher/launch-team.ps1 -ProjectDir <tmp> -Slug probe -Composition custom-agent -DryRun`
ASSERT the printed output (a) lists a `CHIRON_probe` seat with a space-free `--name` + a `--session-id <uuid>`; (b) forces `-Layout Windows` (composition launch = arc/paste class); (c) the printed activation/prompt for the CHIRON seat (an arc-class `$seat.Prompt` seat) contains the chain preamble line `CHAIN OF COMMAND (Stoa, established at launch`. FALSIFIES "composition seats are not added / preamble not injected on the arc/paste class".

**P2 — Chain-of-command structural grep (PLINY routes up, never to PRINCIPAL).**
DryRun an ARC launch (`-ArcId <test>`); grep the printed PLINY activation for `take direction from + surface to POLYBIUS via bw, NOT the PRINCIPAL` and ASSERT NO occurrence of any "surface to PRINCIPAL"/"PRINCIPAL addresses you" line in the PLINY seat's prompt. Grep the POLYBIUS seat's prompt for `you SUPERVISE PLINY`. FALSIFIES the AR-7 mis-routing on the preamble-bearing paths.

**P3 — Standard SAY launch stays bare-word + preserves Panes (Option B property).**
`& ./skills/team-launcher/launch-team.ps1 -ProjectDir <tmp> -Slug probe -Activation say -DryRun` (default Layout = Panes). ASSERT the printed wt command (a) does NOT force `-Layout Windows` (stays Panes); (b) the POLYBIUS seat's positional prompt is the BARE word `polybius` (no multi-line preamble prepended); (c) the PLINY seat's is the bare word `pliny`. FALSIFIES "Option B regressed — the say path carries a preamble / forces Windows / abolishes the Panes default."

**P4 — REAL composition-record round-trip (no live agents).** The load-bearing real-execution probe.
Call directly:
`& ./skills/team-launcher/record-seat.ps1 -Seat CHIRON_probe -Name CHIRON_probe -SessionId <uuid> -Project probe -Machine $(hostname) -Role team-architect -Composition custom-agent -Gauntlet required -ChainRole team-architect -Tier project`
then read back: `git show beadwork:attachments/stoa--reg/seat-registry.jsonl | ConvertFrom-Json | Where seat -eq CHIRON_probe`. ASSERT the round-tripped row carries `composition=custom-agent`, `gauntlet=required`, `chain_role=team-architect`. Then re-record the same seat and ASSERT no duplicate (idempotent replace, existing L77-89 logic). CLEANUP: remove the probe row via the existing read-modify-rewrite (fixed-literal temp path). FALSIFIES "the composition is not actually persisted / the new fields don't round-trip".

**P5 — Gauntlet-by-default detector: clause (E) present + reaches model on the working Stop channel (advisory bar — C3).**
Use the FRESH fixture + runner from §2.8: `bash skills/.../tests/run-stop-self-check-tests.sh` (or directly `cat fixtures/stop-event-orchestrator.json | bash hooks/stop-self-check.sh`). ASSERT the emitted JSON is `decision:block` and its `reason` contains clause `(E)` with the text `solo-with-one-checker close is the AR-7 failure shape`. Run a SECOND time same turn-key → ASSERT `allow` (infinite-block guard intact). FALSIFIES "the detector clause is absent or rides a broken channel" — it rides the SAME confirmed-working `decision:block`+`reason` channel as A/D. **(Honest scope per §2.2/C3: this proves the clause is INJECTED on the working channel + REACHES the model on EVERY orchestrator Stop turn — the accepted advisory branch DoD bullet 4 is met by. It does NOT claim selective firing on the AR-7 shape / mechanical transcript classification — W1.)**

**P6 — record-seat PATH-fix probe (the folded-in defect).**
- **(a) FORCE + PROVE the bash-fallback writes a real row on a pwsh-bw-unreachable shim (C1/r1 — the load-bearing real-execution probe).** The fix's PRIMARY path on the bug machine is the bash-fallback, and the Windows-backslash-temp-path-into-git-bash-`bw` is the dry-run-cannot-reach unknown — PROVE it, do not let it pass via the `Get-Command` branch. Procedure:
  1. **Make `bw` unreachable from the pwsh `Get-Command` resolution** so the fallback is the ONLY path: in the probe shell, prepend a temp dir that does NOT contain `bw` and remove the `bw`-carrying dir from `$env:PATH` for the duration (OR set `$env:PATH` to a minimal value lacking the bw dir but retaining the `bash` dir), then assert `Get-Command bw -ErrorAction SilentlyContinue` returns `$null` AND `Get-Command bash` returns non-null. (This shims the affected-machine state without editing the script.)
  2. Run `record-seat.ps1 -Seat probeFallback -Name probeFallback -SessionId <uuid> -Project probe -Machine $(hostname) -Role team-architect -Composition custom-agent -Tier project` — with `bw` pwsh-unreachable, execution MUST take the `bash -lc` fallback that converts `$tmp` to the `/c/...` POSIX form.
  3. **ASSERT a real row round-trips:** `git show beadwork:attachments/stoa--reg/seat-registry.jsonl | ConvertFrom-Json | Where seat -eq probeFallback` returns the row (proving git-bash `bw` accepted the converted temp path AND the attach committed). ASSERT exit 0 + the success `Write-Host`.
  4. CLEANUP: remove the `probeFallback` row; restore `$env:PATH`.
  FALSIFIES "the bash-fallback (the primary path on the bug machine) cannot write a real row — the backslash-temp-path-into-git-bash-bw breaks." A pass here is the C1 proof the design owes.
- **(b) Error-attribution: PATH-miss vs missing-ticket vs bw-error (C5/r3 — uses the new `-Ticket` param as the injection point).**
  - PATH-miss case: re-run (a)'s pwsh-bw-unreachable shim BUT also shim `bash` unreachable (remove both) → assert `$bwExit -eq $null` path → ASSERT the warning is the PATH-miss message (`PATH/resolution failure, NOT a missing-ticket case`) and does NOT emit the old unconditional "expected/benign on a workspace without the stoa--reg ticket" string.
  - missing-ticket / bw-error case: `record-seat.ps1 ... -Ticket bogus--nope` (the parameterized injection point) with `bw` resolvable → ASSERT the warning is the `bw attach to 'bogus--nope' exited <N>` message (the exit-`<N>` branch), distinct from the PATH-miss message.
  FALSIFIES "the mis-attribution (fail-open hiding a fail) survives" + "the three cases are not distinguishable / P6(b) has no real injection point".
- **(c)** Grep `record-seat.ps1` to ASSERT the old collapsed catch message `expected on a workspace without the registry ticket` no longer appears as the SOLE/unconditional attribution (it may appear only inside the exit-`<N>` branch's conditional guidance).

**P7 — install.sh count stability + consistency sweep.**
`bash install.sh --target project --project-dir <tmp> --dry-run` (or the existing smoke path) ASSERT skill count + hook count UNCHANGED from main (record-seat is intra-skill; clause E is intra-hook). Then grep the touched docs: ASSERT no remaining stale `PRINCIPAL coordinates the panes` / co-equal-panes framing in `team-launcher/SKILL.md`, `gauntlet-setup/SKILL.md`, `launch-team.ps1`. FALSIFIES "a new skill/hook silently changed the deploy plan" + "stale framing left behind".

**P8 — SAY-PATH chain established SUBSTANTIVELY via canon (the FM say-path-not-thinner dependency — NEW).**
The Option-B say path's ONLY chain-establishment is the role file + §37. ASSERT they carry the chain SUBSTANTIVELY, not just a cross-ref token:
- `Select-String -Path operating-disciplines.md -Pattern '## 37\. Launcher-correctness'` returns 1 AND the §37 body contains the substantive chain string `PRINCIPAL` AND `POLYBIUS` AND `PLINY` AND `gauntlet` (the chain is stated, not just titled).
- `MAJOR_PLINY.md` — `Select-String -Pattern 'SURFACE TO POLYBIUS'` (or `surface to POLYBIUS .* NOT the PRINCIPAL`) returns ≥1 AND the same paragraph contains `gauntlet` + `default` (the surface-up direction + gauntlet-by-default are stated in the role file, not just `§37`).
- `MAJOR_POLYBIUS.md` — `Select-String -Pattern 'you supervise PLINY'` (case-insensitive) returns ≥1 AND the paragraph names CHIRON/HAMILTON answering to POLYBIUS.
- Confirm `operating-disciplines.md.*§37` appears in BOTH role files (the cross-ref is ALSO present) — but the assertions above prove the substance is present BEYOND the token.
FALSIFIES "the say path is thinner — the role file carries only a bare `§37` stub so a bare-word say launch comes up without the chain substantively in its loaded context."

**P9 — od §37 placement (C6 — before the trailing appendices).**
ASSERT `## 37. Launcher-correctness` appears in `operating-disciplines.md` at a line BEFORE `## Agent-regime inverses (the positive framing)` AND before `## Empirical lineage` (e.g. compare the `Select-String` line numbers: §37's line < the Agent-regime-inverses line). FALSIFIES "§37 was appended at EOF after the un-numbered appendices, breaking the numbered sequence."

**Full-suite backstop (banked lesson):** VERA/CATO ALSO run the project's existing app/gen-data + any launcher smoke suite IN ADDITION to P1-P9 — the bespoke probes prove the new thing works; the full suite catches what the shared-machinery edit (record-seat.ps1 is shared with the desktop self-record + `u--9s2`) breaks elsewhere.

---

## §5 Threat → mitigation map (§6.12 / §35.4)

**Classification (PROPOSED by DAEDALUS; ARGUS CONFIRMED in the rev1 critique):** Arc 68 is **launcher-tooling + process/role-file hardening with no runtime attack path** — it hardens how a team is brought up; it does not defend a credentialed surface, a parser, or an external input against an adversary. Per **§35.5 self-reference carve-out**, this class is `not threat-ratified (process change, no runtime attack path)`.

> **`not threat-ratified (process change, no runtime attack path)`** — the three guarantees + the record-seat fix harden activation correctness + registry-write honesty; there is no attacker and no runtime attack path for a `M<n>` map to defeat. AR-7 is a *correctness/discipline failure shape*, not a security threat; the gauntlet-by-default detector (clause E) addresses an internal process-deviation, not an adversary. **No threat-anchored probe is required** (§6.13 / §35.5 — the layer verifies named-threat COVERAGE, not threat-defeat-in-general; threat-enumeration completeness stays ARGUS's residual).

**ARGUS confirmation (rev1 verdict, carried forward):** the carve-out was CONFIRMED. The `bash -lc` interpolands in fix (a) (`$ticket`/`$tmpBash`/`$attachName`) are script-internal — `$ticket` is now the `-Ticket` param but defaults to / is set by the launcher (not agent/caller-untrusted in the launch flow); the probe drives it to a fixed test value. None is adversary-controlled untrusted input; the single-quote-wrap (C4) is the word-splitting safety. **No injection surface; carve-out stands.** (Note for ARGUS re-confirm: the C5 parameterization makes `$ticket` a param — please re-confirm this does not open an injection surface; my judgment: it is launcher-set + single-quote-wrapped, no untrusted reach.)

---

## §6 Self-assessed weak points

- **W1 — the gauntlet-default detector is detection, not prevention (the load-bearing residual; the ack-sensitive surface, isolated to §2.0b).** Clause (E) injects a self-check on the working Stop channel on EVERY orchestrator-class Stop turn; it does NOT mechanically parse the transcript to PROVE "POLYBIUS dispatched CAPTAINs without a PLINY," and it does NOT selectively fire only on the AR-7 shape. A determined seat can read the clause and dismiss it. **DoD bullet 4 is met via the ACCEPTED ADVISORY branch (clause-(E)-text-reaches-model), NOT selective detection (C3/r5 recorded).** *Why this shape anyway:* the directive's DoD explicitly accepts "honestly document the residual convention-only gap if the mechanism is advisory" (bullet 4); a reliable transcript classifier is a separate detection arc; detection-on-a-working-channel + recorded-deviation is strictly more than today's nothing. NAMED, not hidden. The prevention-vs-detection framing is isolated in §2.0b so the PRINCIPAL ack revises only that subsection.
- **W2 — under Option B, a WAIVED bare-say launch carries the waiver only in the row, not the preamble.** The waiver line lives in the L1 preamble, which rides arc/paste paths only; a `-GauntletWaiver` say launch records `gauntlet=waived:<reason>` to the row + relies on §37 role-file canon for the gauntlet-by-default context. *Why this shape anyway:* a waiver is an explicit POLYBIUS/PRINCIPAL action that in practice uses the arc/paste path (it carries a brief), not the bare-say convenience path; the row records the waiver authoritatively regardless. If a waived bare-say launch must ALSO carry the waiver text in-prompt, that requires the `stoa--waa` quoting fix (out of scope) — flag to ARGUS if the floor-manager wants belt+suspenders here. **Residual question RQ1.**
- **W3 — per-seat composition fields have no atomic "this is ONE composition" grouping.** Expressing composition per-row (DC4) keeps ONE registry but means the read side infers a composition from `(project, machine, launched-at-window)` + matching `composition` value — a window heuristic, not a composition-id. *Why this shape anyway:* it avoids a second manifest artifact (the directive's ONE-registry + non-divergence-with-`u--9s2` constraint), and the launch loop records all seats in one pass so the window is tight. If `u--9s2` needs a hard composition-id, that's an additive field later, not a rebuild.
- **W4 — clause (E) cannot distinguish a legitimate solo build-session from the AR-7 failure.** `MAJOR_PLINY.md` L44/L163 explicitly bless "build sessions for early arcs where no CAPTAINs exist do the work directly." Clause (E) will nudge those too (it fires every orchestrator Stop turn — W1). *Why this shape anyway:* it is a reminder, not a block (degrades like clause A); the clause text now carries an explicit "legitimate early-arc solo build-sessions: this does not apply — proceed" carve-out line (§2.2), so a legitimate solo seat reads it, recognizes it does not apply, and proceeds — bounded false-positive cost, same property as the PostToolUse NOMOS reminder's bounded no-op.
- **W5 — the bash-fallback path-conversion (C1 fix a) rests on a transform I have NOT executed against a live git-bash `bw` this turn.** I specified `cygpath -u` (robust if present) with a deterministic `C:\ -> /c/` fallback, and P6(a) PROVES it round-trips a real row. *Why this shape anyway:* the design names the proof obligation (P6(a) is the load-bearing probe) rather than asserting the transform works; if P6(a) fails, the transform is the single thing to adjust (e.g. force `cygpath` as a hard dependency, or use `bw`'s own path-acceptance form), localized to fix (a). NAMED as the build-time-verified unknown, with the probe that resolves it.

---

## §7 Residual questions for ARGUS
- RQ1 (W2): under Option B, should a WAIVED bare-say launch ALSO carry the waiver text in-prompt (belt+suspenders), which would require folding the out-of-scope `stoa--waa` quoting fix — or is the row-recorded waiver + §37 canon sufficient? My call: row + canon sufficient; flagged for the floor-manager's belt+suspenders preference.
- RQ2 (§5): re-confirm the `not threat-ratified (process change)` carve-out HOLDS after the C5 `-Ticket` parameterization (I judge `$ticket` stays launcher-set + single-quote-wrapped, no untrusted reach — but the param is new since rev1's confirmation).
- RQ3 (§2.0b / W1): re-confirm detection-on-Stop-channel + recorded-deviation is the right claim for the go/no-go to weigh — the §2.0b ACK-PENDING marking localizes any prevention-demand rework; please confirm the isolation is clean (only §2.0b touches if the ack flips to prevention).
- RQ4 (C3/r5): confirm no wording anywhere in rev2 implies SELECTIVE AR-7 detection (I scrubbed §2.0/§2.0b/§2.2/§5/§6 to say "fires every orchestrator Stop turn / accepted advisory branch" — flag any residual over-claim).

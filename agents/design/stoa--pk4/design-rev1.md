# Arc 68 design-rev1 — Launcher-correctness (chain-of-command-at-launch · gauntlet-by-default · variable team composition)

**Ticket:** `stoa--pk4` · **Author:** Denson Smith (the PRINCIPAL) · **Seat:** CAPTAIN_DAEDALUS_the_stoa
**Builds on:** the-stoa main `3435fe3` (directive committed) + the SHIPPED Arc-67 identity layer (`stoa--p7c`, `stoa--reg`).
**Status:** design hand-back for Polybius_the_Stoa / floor-manager go/no-go before Phase B.

---

## §1 Problem restatement

A Stoa team is brought up by `launch-team.ps1` + activation text. Today that text is *advisory*: a seat that is activated with an incomplete brief can (AR-7 / nws-iey, 2026-06-20) run SOLO as its own orchestrator, spawn CAPTAINs directly with no PLINY, and self-certify with one checker (no gauntlet). The launcher must STRUCTURALLY guarantee the by-the-book forge along three axes — (1) the chain PRINCIPAL→POLYBIUS→PLINY→CAPTAINs is established at launch so PRINCIPAL is never pointed at PLINY and seats are not co-equal panes; (2) the full gauntlet (DAEDALUS→ARGUS→ADA→VERA→CATO→NOMOS) is the default, opt-OUT requiring an explicit POLYBIUS/PRINCIPAL waiver, not a seat's silent solo opt-in; (3) team composition is variable — an arc designing custom **agents** pulls in MAJOR_CHIRON, an arc designing custom **workflows** pulls in MAJOR_HAMILTON (either/both/neither), placed in the chain, recorded to the ONE registry `stoa--reg`. Plus a folded-in live defect: `record-seat.ps1` calls `& bw` in pwsh where `bw` is on the bash PATH only, and its try/catch collapses CommandNotFound into the benign "no registry ticket" warning — a fail-OPEN that hid a total registry-write failure.

**Imported assumptions (named, per §6.1):**
- A1: "Structural" cannot mean "a seat is technically unable to emit non-gauntlet text" — a launcher + an activation paste are ultimately TEXT a seat could ignore (the directive DC0 says so explicitly). I read the PRINCIPAL's bar as *"the by-the-book path is the ONLY path the tooling lays down, the deviation is loud, recorded, and waiver-gated, and the AR-7 shape is detected after the fact by an independent checker"* — not "deviation is impossible." Where I claim structural vs advisory is itemized honestly in §2.0.
- A2: the build runs in the `arc-68-build` worktree; the launcher edits are to `substrate/skills/...` source (deployed by `install.sh`), NOT to a live `.claude/`.
- A3: hooks deploy by the `*.sh` glob (`install.sh` L877, no HOOK_NAMES list) and default INERT (`ENABLE_HOOKS=0`, HARD SAFETY CONSTRAINT). Any new hook therefore needs NO `install.sh` name-list edit and ships disarmed — consistent with the existing convention.
- A4: `record-seat.ps1` ships *beside* `launch-team.ps1` inside the `team-launcher` skill dir; it is NOT a separate `SKILL_NAMES` entry. No `install.sh` skill-list edit is needed for the PATH fix.

---

## §2 Approach

### §2.0 DC0 — STRUCTURAL vs CONVENTIONAL: the central decision (resolve FIRST)

**Decision: a LAYERED model — three structural layers + one honestly-named advisory residual.** No single mechanism reaches the PRINCIPAL's "structurally impossible" bar; the layers compound so the by-the-book path is the default the tooling lays down AND the AR-7 deviation is loud + recorded + independently detected.

| Layer | Mechanism | Enforcement class | What it actually forces |
|---|---|---|---|
| **L1 — Activation injection** | launcher injects a fixed **chain-of-command preamble** into EVERY seat's activation prompt (say + paste + arc paths) | **Structural-at-launch** (the launcher cannot emit a seat without the preamble; it is concatenated in code, not authored per-arc) | Every launched seat is TOLD its place + who it reports to. A seat *can* still ignore text → not absolute. |
| **L2 — Role-file canon** | the chain + gauntlet-by-default land as `operating-disciplines.md` canon referenced from `MAJOR_POLYBIUS.md`/`MAJOR_PLINY.md`; the SAY-TRIGGER default loads the role file, so the bare-word path inherits the chain too | **Structural-via-canon** (any activation that reads the role file inherits it; covers the no-`-ArcId` say path the injection preamble is thinner on) | The default activation cannot come up WITHOUT the chain in its loaded context. |
| **L3 — Recorded signal + independent detector** | the launcher writes a `gauntlet`/`composition` field into the `stoa--reg` row at launch; the existing **Stop self-check hook** (`decision:block`+`reason`, a CONFIRMED-WORKING channel) gains a clause that fires the AR-7 shape ("a POLYBIUS-class seat that dispatched CAPTAINs this turn with no PLINY / no gauntlet recorded") | **Structural-detection, advisory-correction** (the detector fires reliably; it cannot *prevent* the dispatch, only flag it at turn-end — bounded, fail-open, once-per-turn, exactly like clause A/D today) | The deviation is DETECTED + surfaced every turn it occurs; correction is the seat's. |
| **Residual (advisory, NAMED)** | a determined seat can still ignore the preamble, run solo, and dismiss the Stop-hook flag | **Convention-only** | NOT closed. Honestly named (§6 weak point W1). The mitigation is detection (L3) + the loud-recorded-deviation property, not impossibility. |

**Why this shape:** it reuses the proven Arc-46/50/63 hook pattern (Stop `decision:block`+`reason` is the only confirmed-working injection channel; PostToolUse `additionalContext` is BROKEN #55889 — so the detector MUST ride Stop, not PostToolUse). It adds NO new armed-by-default surface (hooks ship INERT). It avoids over-claiming: the directive's DoD explicitly accepts "honestly document the residual convention-only gap if the mechanism is advisory" (DoD bullet 4), and §35.5's honest-claim discipline is the canon precedent for naming the residual rather than papering it.

**DC0 drives DC1 (L1+L2), DC2 (L3 detector + recorded signal), DC3/DC4 (the composition is the same recorded signal extended).**

### §2.1 DC1 — chain-of-command establishment

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

**Edit B (wire the preamble into every prompt path).** In `Get-SeatPrompt` (L169-173), PREPEND `Get-ChainPreamble $seat.Role $Slug` to the returned prompt for ALL three return cases (`$seat.Prompt` arc path, the say-word path, AND a new branch so even a bare say-word seat carries the preamble):

- `$seat.Prompt` (arc path): `return (Get-ChainPreamble $seat.Role $Slug) + "`n" + [string]$seat.Prompt`
- say path: keep the bare word as the LAST line (the CLAUDE.md say-trigger matches the bare word at end), preamble first: `return (Get-ChainPreamble $seat.Role $Slug) + "`n" + [string]$seat.Say`
  - **Constraint check (verify-then-execute):** the say-trigger relies on the bare word `polybius`/`pliny` being recognized. A multi-line prompt with the word at the END must still fire the CLAUDE.md auto-load. This is the **one place** the launcher's wt-pane path is brittle (panes re-split multi-word prompts on spaces — same break the `-ArcId` path forces `-Layout Windows` for, L122-125). **Decision:** when the preamble is injected into a say-word seat AND `$Layout` is Panes/Tabs, force the same `-Layout Windows` fallback the arc path uses (extend the L125 guard), OR pass the preamble through the Windows per-seat pwsh path which quotes robustly (L205-212). The say-word path already only fires reliably in Windows layout for multi-word content — make that explicit. (See W2.)

**Edit C (L2 canon, the say-trigger backstop).** Because the bare-word say-trigger ultimately loads `MAJOR_POLYBIUS.md`/`MAJOR_PLINY.md`, the chain must ALSO be canon in those role files (so the no-preamble path still establishes it). See §2.5.

### §2.2 DC2 — gauntlet-by-default mechanism

Three coordinated pieces:

**Piece 1 — recorded signal (launcher → registry).** Extend the per-seat launch record with a launch-level `gauntlet` field. In the `record-seat` call (L241) the launcher passes a new `-Gauntlet` value; default `required`. A solo/waiver launch sets `-Gauntlet waived:<reason>`. (Schema add is additive — see DC4 §2.4; does NOT reopen the Arc-67 schema, it adds optional fields.)

**Piece 2 — activation default (L1 preamble).** The preamble's gauntlet line (above) names the full gauntlet as the default path in every seat's loaded context. Opt-out is textual + must cite a waiver.

**Piece 3 — independent detector (NEW Stop-hook clause, the structural-detection layer).** Add a clause **(E)** to `stop-self-check.sh`'s `REASON` checklist, riding the SAME `decision:block`+`reason` working channel as clauses A/B/C/D:

```
(E) If THIS turn you (a POLYBIUS- or PLINY-class seat) dispatched CAPTAINs via the Agent tool,
    confirm a PLINY orchestrator is in the chain (you are not a POLYBIUS that spawned CAPTAINs
    directly) AND the gauntlet shape is the full DAEDALUS->ARGUS->ADA->VERA->CATO->NOMOS unless an
    explicit POLYBIUS/PRINCIPAL waiver is recorded on bw. A solo-with-one-checker close is the
    AR-7 failure shape (stoa--pk4) — if that is what happened, STOP and route through the gauntlet
    or record the waiver before ending the turn.
```

- This is a **reminder-class** clause (matching A's "treat as no-op if NOMOS not deployed" degradation), NOT a transcript-parsing classifier. Honest scope: the hook does NOT mechanically inspect the transcript to *prove* CAPTAINs were dispatched-without-PLINY; it injects the self-check the seat must address. (Mechanical transcript classification of "dispatched CAPTAINs without a PLINY" is the unmechanized residual — W1.) **This satisfies the DoD's "demonstrate the mechanism fires on the AR-7 failure shape" via the demonstrable fact that the clause is PRESENT in the injected `reason` JSON and reaches the model on the working Stop channel** — VERA's probe P5 asserts exactly that (the clause text is in the emitted JSON), which is the same falsifiable bar clauses A/D are held to.
- **No new hook file** — clause (E) extends the existing `stop-self-check.sh`. Ships INERT with the rest (ENABLE_HOOKS=0). FAIL-OPEN preserved.

**Waiver path (opt-out, gated):** a non-gauntlet launch is `launch-team.ps1 ... -GauntletWaiver "<reason>"` (new switch), which (a) records `gauntlet=waived:<reason>` to the row and (b) the preamble's gauntlet line is replaced with `GAUNTLET WAIVED by launch flag: <reason> (POLYBIUS/PRINCIPAL-authorized).` Absent the flag, default is `required`. A *seat* cannot grant itself the waiver — only the launch flag (driven by POLYBIUS/PRINCIPAL) writes it. That is the "opt-out requires explicit waiver, not silent solo opt-in" guarantee, at the structural-at-launch tier.

### §2.3 DC3 — variable composition model + chain placement

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

**Are CHIRON/HAMILTON launcher-spun terminal seats or PLINY-dispatched? → launcher-spun TERMINAL seats.** Rationale (verify against role files): both `MAJOR_CHIRON.md` and `MAJOR_HAMILTON.md` say they "live at a top-level Claude Code session in a project-tier directory; engaged at design-time" — i.e. they are MAJOR-rank terminal seats, not `Agent`-tool sub-agents. They cannot be PLINY-dispatched (PLINY dispatches CAPTAINs; CHIRON/HAMILTON are MAJORs at design-time, peers of the architecture phase). So the launcher spins them up as terminal seats, same as POLYBIUS/PLINY.

**WHERE in the chain (placement):** CHIRON/HAMILTON answer to **POLYBIUS** (both role files §1: "You answer to MAJOR_POLYBIUS, who reviews your roster/workflow decisions"). They are **design-time peers that feed POLYBIUS**, parallel to PLINY, not under PLINY. Chain placement:

```
PRINCIPAL -> POLYBIUS ──┬── PLINY -> CAPTAINs            (run-time pipeline)
                        ├── CHIRON  (design-time: the cast)     ┐ answer to POLYBIUS;
                        └── HAMILTON(design-time: choreography) ┘ co-design; step back, then PLINY runs it
```

The CHIRON/HAMILTON `<ROLE_LINE>` in the preamble:
- CHIRON → `MAJOR_CHIRON: design-time team-architect. You answer to POLYBIUS; you co-design the cast with HAMILTON, then step back so PLINY runs the team. You do NOT dispatch CAPTAINs.`
- HAMILTON → `MAJOR_HAMILTON: design-time workflow-architect. You answer to POLYBIUS; you co-design the choreography with CHIRON, then step back so PLINY runs the team.`

**How the launcher PLACES them (activation):** CHIRON/HAMILTON have **no CLAUDE.md say-trigger** (verified: no `chiron`/`hamilton` bare-word in CLAUDE.md; their role files say "auto-loaded via CLAUDE.md ref, or by PRINCIPAL prompt"). So the say-word path does NOT work for them — the launcher MUST seed a full activation prompt naming the role file. Add seat definitions analogous to the `-ArcId` arc seats (L118-121):

```powershell
# in the composition block, when $Composition includes custom-agent:
@{ Name = "CHIRON_$Slug"; Role = 'team-architect';
   Prompt = "Read .claude/MAJOR_CHIRON.md and assume the team-architect role for $Slug" + $(if($ArcId){" on arc $ArcId; read your brief: git show beadwork:attachments/$ArcId/HUMAN_paste-chiron-$ArcId-instruction.md and follow it."}else{"."}) }
# analogous HAMILTON_$Slug with Role='workflow-architect' + MAJOR_HAMILTON.md
```

(The `Get-SeatPrompt` preamble-prepend from §2.1 Edit B applies to these too — they inherit the chain preamble with their CHIRON/HAMILTON `<ROLE_LINE>`.) Because they carry full multi-word prompts, they REQUIRE `-Layout Windows` exactly like the `-ArcId` path — extend the L125 force-Windows guard to also fire when `$Composition -ne 'standard'`.

**Record the composition to `stoa--reg`** — each composed seat is recorded by the existing post-launch `record-seat` loop (L230-252); it already records every seat in `$Seats`, so CHIRON/HAMILTON are recorded automatically once added to `$Seats`. The NEW fields (`composition`, `gauntlet`, `chain_role`) are passed through — see DC4.

### §2.4 DC4 — registry + manifest coordination (ONE registry)

**Reuse `stoa--reg`; ADD optional fields (additive, does NOT rebuild the Arc-67 schema).** `record-seat.ps1`'s `$row` (L92-102) gains three optional fields:

```
composition = $Composition   # 'standard'|'custom-agent'|'custom-workflow'|'custom-agent+workflow'  (default 'standard')
gauntlet    = $Gauntlet      # 'required' | 'waived:<reason>'                                       (default 'required')
chain_role  = $ChainRole     # 'floor-manager'|'orchestrator'|'team-architect'|'workflow-architect' (its place in the chain; defaults to $Role)
```

New `record-seat.ps1` params: `[string]$Composition='standard'`, `[string]$Gauntlet='required'`, `[string]$ChainRole=''` (falls back to `$Role`). All optional with safe defaults → **a caller that does not pass them (incl. the desktop self-record path + the builder-deploy `u--9s2` follow-on) still writes valid rows** (the older rows simply omit the new keys; JSONL tolerates heterogeneous rows). This is the non-divergence guarantee the directive asks for: `u--9s2`'s cookie-cutter can adopt the SAME `record-seat.ps1` + SAME registry and either set or omit these fields.

**Manifest-shape coordination note (for `u--9s2`, not built here):** the composition is expressed PER-SEAT (each row carries `composition`+`chain_role`), NOT as a separate manifest object. This keeps ONE registry, one row-shape; a "composition" is just the set of alive rows sharing a `(project, machine, launched-at-window)` with the same `composition` value. No second artifact. (W3 names the read-side weak point.)

### §2.5 Canon edits (operating-disciplines.md + role-file refs)

Add a new section **`## 37. Launcher-correctness — chain-of-command-at-launch, gauntlet-by-default, variable composition`** to `operating-disciplines.md` (next free number; §36 is the last). Three subsections:

- **37.1 Chain-of-command at launch** — PRINCIPAL→POLYBIUS→PLINY→CAPTAINs; PRINCIPAL never addresses PLINY; seats are not co-equal panes; the launcher injects the preamble + the say-trigger default loads it via the role file. Cross-ref the L1/L2 layers.
- **37.2 Gauntlet-by-default** — full gauntlet is the default; opt-out requires an explicit POLYBIUS/PRINCIPAL waiver recorded on bw (`-GauntletWaiver` launch flag → `gauntlet=waived:<reason>` row); a seat cannot self-grant solo. The Stop-hook clause (E) is the independent detector (honest: detection + surface, not prevention). Cross-ref §6 (redundancy IS the safety property) + §35.5 (honest-claim precedent).
- **37.3 Variable team composition** — the precise trigger (custom-agent→CHIRON, custom-workflow→HAMILTON, either/both/neither; NOT generic "design-heavy"); CHIRON/HAMILTON are launcher-spun terminal design-time seats answering to POLYBIUS; recorded per-seat to `stoa--reg`.

**Role-file references (no canon duplication — point at §37):**
- `MAJOR_POLYBIUS.md` — at the chain/activation section (§9 area), add one line: "You supervise PLINY and any design-time architects (CHIRON/HAMILTON) the composition includes; the launcher establishes this chain at launch — `operating-disciplines.md` §37."
- `MAJOR_PLINY.md` — at §17/§41 area where "you receive directives from MAJOR_POLYBIUS" is stated, add: "The launcher establishes this chain at launch; the full gauntlet is the default (§37.2). You surface to POLYBIUS, never PRINCIPAL — `operating-disciplines.md` §37."

### §2.6 The record-seat pwsh-PATH defect fix (folded-in, DC-adjacent)

**Two coupled fixes at the call site — TARGETED, not a registry/schema rebuild:**

**Fix (a) — make `bw` pwsh-resolvable.** Replace the bare `& bw attach ...` (`record-seat.ps1` L120) with a resolution that finds `bw` even when it is on the bash PATH only:

```powershell
# Resolve bw: pwsh PATH first, else the bash PATH (git-bash / WSL installs bw there on Windows).
$bwCmd = Get-Command bw -ErrorAction SilentlyContinue
if ($bwCmd) {
  & $bwCmd.Source attach $ticket $tmp --name $attachName
  $bwExit = $LASTEXITCODE
} else {
  # bw not on the pwsh PATH — try invoking through bash (where the launcher's machine has it).
  $bash = Get-Command bash -ErrorAction SilentlyContinue
  if ($bash) {
    & $bash.Source -lc "bw attach '$ticket' '$tmp' --name '$attachName'"
    $bwExit = $LASTEXITCODE
  } else {
    $bwExit = $null   # genuine: no bw resolvable any way -> distinct from a bw error
  }
}
```

(Path quoting note: `$tmp` is the fixed-literal temp path `stoa-seat-registry.jsonl` under the temp dir, no spaces by construction — §8.6 destructive-path hygiene is preserved; the bash `-lc` string interpolates fixed names, not user-controlled content.)

**Fix (b) — fail-LOUD with the REAL error; distinguish the three cases** (replace the collapsed catch L118-128):

```powershell
$attachOk = $false; $failReason = ''
try {
  # ... the resolve+invoke block above ...
  if ($bwExit -eq 0)        { $attachOk = $true }
  elseif ($null -eq $bwExit){ $failReason = "bw NOT FOUND on the pwsh PATH or via bash — this is a PATH/resolution failure, NOT a missing-ticket case. On this machine bw is on the bash PATH only; the launcher must invoke it pwsh-resolvably (Arc 68 / stoa--pk4)." }
  else                      { $failReason = "bw attach to '$ticket' exited $bwExit (e.g. no such ticket on THIS bw store, or a bw error). If '$ticket' genuinely does not exist on this workspace's bw store, this is the benign no-registry-ticket case; otherwise it is a real attach failure." }
} catch {
  $failReason = "bw attach threw: $($_.Exception.Message)"
}
if (-not $attachOk) {
  Write-Warning "record-seat: could not record seat '$Seat' to $ticket. $failReason"
  exit 1
}
```

- The **mis-attribution is the named hazard** — fix (b) ensures a CommandNotFound/PATH-miss is reported AS a PATH failure (not "expected on a workspace without the registry ticket"), so a total registry-write failure can never again hide behind the benign label.
- **Launcher side (`launch-team.ps1` L243/L246):** update the two warning strings so they no longer assert "expected/benign on a workspace without the stoa--reg ticket" unconditionally — instead echo `record-seat`'s own exit + let its specific message stand. Change to: `Write-Warning "record-seat.ps1 returned non-zero for seat '$name' (see its message above for the specific cause: PATH-miss vs missing-ticket vs bw error); seat LAUNCHED but NOT recorded."` (The launch stays best-effort — never rethrow — but the cause is now legible.)

**Scope guard:** this touches ONLY the bw-invocation + error-attribution at the `record-seat.ps1` call site (L118-128) + the two launcher warning strings + new optional params from DC4. It does NOT touch the read-modify-rewrite logic (L66-111), the registry schema beyond the additive DC4 fields, or the `bw attach --name` path convention — staying clear of the "do not rebuild the Arc-67 identity layer" out-of-scope line.

### §2.7 install.sh + consistency sweep

- **install.sh:** NO name-list edit needed — `record-seat.ps1` ships beside `launch-team.ps1` in the existing `team-launcher` skill (in `SKILL_NAMES`); the Stop-hook clause is an edit to an existing hook (deployed by the `*.sh` glob). **Verify** the dry-run still reports the same skill/hook counts (probe P7).
- **Consistency sweep (no stale framing):** grep the touched files for stale "two-seat default" / "PRINCIPAL coordinates the panes" / co-equal-panes framing and reconcile:
  - `team-launcher/SKILL.md` L4 (description "POLYBIUS + PLINY by default") + L29 → add the variable-composition + chain-establishment note; keep POLYBIUS+PLINY as the *standard* composition, not "the" default that implies fixed.
  - `gauntlet-setup/SKILL.md` — reconcile §"Mandatory content checklist" with the launcher's new structural guarantees: the chain-of-command + gauntlet-default are now launcher-injected (L1) + canon (L2), so the human-authored brief checklist becomes a *belt-and-suspenders confirm* rather than the sole carrier. Add a line pointing at §37 + the `-Composition`/`-GauntletWaiver` flags. Update failure-mode #8 ("chain-of-command set up wrong") to note the launcher now injects it.
  - `launch-team.ps1` synopsis/.NOTES — document the new `-Composition`, `-GauntletWaiver`, the chain preamble, and the CHIRON/HAMILTON placement.

---

## §3 Out of scope (deliberately not designed)

- **Re-building the Arc-67 identity layer** (mint/name/record/whoami/sign-everywhere/`stoa--reg` schema) — reused; only additive optional fields added. *Reason:* directive out-of-scope line 1.
- **The builder-deploy cookie-cutter BUILD (`u--9s2`)** — only kept the registry+`record-seat.ps1` adoptable (DC4). *Reason:* directive out-of-scope line 2.
- **Cross-machine `--resume`/cloud-sync** — sessions are local-only (verified Arc-67). *Reason:* directive out-of-scope line 3.
- **A full `operating-disciplines.md` audit** beyond §37's three disciplines. *Reason:* directive out-of-scope line 4.
- **The `apply.sh`/`install.sh` seat-trailer signing gap (`stoa--tg7`)** — design touches no commit sites. *Reason:* directive out-of-scope line 5.
- **A mechanical transcript-parsing classifier** that PROVES "POLYBIUS dispatched CAPTAINs without a PLINY." *Reason:* the Stop hook reads its event JSON, not the full transcript of Agent dispatches; a reliable classifier is a larger detection arc. Named as residual W1, not built.
- **Arming hooks** (`ENABLE_HOOKS=1`) — HARD SAFETY CONSTRAINT; hooks ship INERT.

---

## §4 Verification probes (concrete, VERA-runnable)

All run from the `arc-68-build` worktree root unless noted. `-DryRun` can ONLY prove printed-command + activation shape (it early-returns before launch AND before record — directive DoD note); the REAL round-trip is exercised by calling `record-seat.ps1` directly without spawning agents.

**P1 — DryRun command + activation shape (custom-agent composition).**
`& ./skills/team-launcher/launch-team.ps1 -ProjectDir <tmp> -Slug probe -Composition custom-agent -DryRun`
ASSERT the printed output (a) lists a `CHIRON_probe` seat with a space-free `--name` + a `--session-id <uuid>`; (b) forces `-Layout Windows`; (c) the printed activation/prompt for each seat contains the chain preamble line `CHAIN OF COMMAND (Stoa, established at launch`. FALSIFIES "composition seats are not added / preamble not injected".

**P2 — Chain-of-command structural grep (PLINY routes up, never to PRINCIPAL).**
DryRun a standard launch; grep the printed PLINY activation for `take direction from + surface to POLYBIUS via bw, NOT the PRINCIPAL` and ASSERT NO occurrence of any "surface to PRINCIPAL"/"PRINCIPAL addresses you" line in the PLINY seat's prompt. Grep the POLYBIUS seat's prompt for `you SUPERVISE PLINY`. FALSIFIES the AR-7 mis-routing.

**P3 — SAY-TRIGGER default ALSO establishes the chain (L2 canon).**
`Select-String -Path operating-disciplines.md -Pattern '## 37\. Launcher-correctness'` returns 1; `Select-String MAJOR_PLINY.md -Pattern 'operating-disciplines.md.*§37'` returns ≥1; `Select-String MAJOR_POLYBIUS.md -Pattern 'operating-disciplines.md.*§37'` returns ≥1. FALSIFIES "the bare-word say path comes up without the chain in canon".

**P4 — REAL composition-record round-trip (no live agents).** The load-bearing real-execution probe.
Call directly:
`& ./skills/team-launcher/record-seat.ps1 -Seat CHIRON_probe -Name CHIRON_probe -SessionId <uuid> -Project probe -Machine $(hostname) -Role team-architect -Composition custom-agent -Gauntlet required -ChainRole team-architect -Tier project`
then read back: `git show beadwork:attachments/stoa--reg/seat-registry.jsonl | ConvertFrom-Json | Where seat -eq CHIRON_probe`. ASSERT the round-tripped row carries `composition=custom-agent`, `gauntlet=required`, `chain_role=team-architect`. Then re-record the same seat and ASSERT no duplicate (idempotent replace, existing L77-89 logic). CLEANUP: re-record with `status` semantics OR remove the probe row (use the existing read-modify-rewrite; fixed-literal temp path). FALSIFIES "the composition is not actually persisted / the new fields don't round-trip".

**P5 — Gauntlet-by-default detector fires on the AR-7 shape (Stop-hook clause E present + reaches model).**
Feed a synthetic Stop event to `stop-self-check.sh` (the hook reads stdin JSON; tests dir has the pattern) with a fresh session+transcript so the sentinel does not suppress: `echo '<event-json>' | bash hooks/stop-self-check.sh`. ASSERT the emitted JSON is `decision:block` and its `reason` contains clause `(E)` with the text `solo-with-one-checker close is the AR-7 failure shape`. Run a SECOND time same turn-key → ASSERT `allow` (infinite-block guard intact). FALSIFIES "the detector clause is absent or rides a broken channel" — it rides the SAME confirmed-working `decision:block`+`reason` channel as A/D. (Honest scope per §2.2: this proves the clause is INJECTED on the working channel, the bar clauses A/D are held to; it does not claim mechanical transcript classification — W1.)

**P6 — record-seat PATH-fix probe (the folded-in defect).**
(a) Positive: run P4's `record-seat.ps1` call; ASSERT exit 0 + the success `Write-Host` (proves bw is now resolved pwsh-side via `Get-Command`/bash fallback, not failing CommandNotFound).
(b) Error-attribution: invoke `record-seat.ps1` against a deliberately-nonexistent ticket (`-Seat probe2 ... ` but with `$ticket` forced to a bogus id via a test shim, OR run on a workspace with no such ticket) and ASSERT the warning text distinguishes the case — it says either the PATH-miss message or the `bw attach ... exited <N>` message, and does NOT emit the old unconditional "expected/benign on a workspace without the stoa--reg ticket" string for a PATH failure. FALSIFIES "the mis-attribution (fail-open hiding a fail) survives".
(c) Grep `record-seat.ps1` to ASSERT the old collapsed catch message `expected on a workspace without the registry ticket` no longer appears as the SOLE/unconditional attribution (it may appear only inside the exit-`<N>` branch's conditional guidance).

**P7 — install.sh count stability + consistency sweep.**
`bash install.sh --target project --project-dir <tmp> --dry-run` (or the existing smoke path) ASSERT skill count + hook count UNCHANGED from main (record-seat is intra-skill; clause E is intra-hook). Then grep the touched docs: ASSERT no remaining stale `PRINCIPAL coordinates the panes` / co-equal-panes framing in `team-launcher/SKILL.md`, `gauntlet-setup/SKILL.md`, `launch-team.ps1`. FALSIFIES "a new skill/hook silently changed the deploy plan" + "stale framing left behind".

**Full-suite backstop (banked lesson):** VERA/CATO ALSO run the project's existing app/gen-data + any launcher smoke suite IN ADDITION to P1-P7 — the bespoke probes prove the new thing works; the full suite catches what the shared-machinery edit (record-seat.ps1 is shared with the desktop self-record + `u--9s2`) breaks elsewhere.

---

## §5 Threat → mitigation map (§6.12 / §35.4)

**Classification (PROPOSED by DAEDALUS; ARGUS CONFIRMS per §35.1):** Arc 68 is **launcher-tooling + process/role-file hardening with no runtime attack path** — it hardens how a team is brought up; it does not defend a credentialed surface, a parser, or an external input against an adversary. Per **§35.5 self-reference carve-out**, this class is `not threat-ratified (process change, no runtime attack path)`.

> **`not threat-ratified (process change, no runtime attack path)`** — the three guarantees + the record-seat fix harden activation correctness + registry-write honesty; there is no attacker and no runtime attack path for a `M<n>` map to defeat. AR-7 is a *correctness/discipline failure shape*, not a security threat; the gauntlet-by-default detector (clause E) addresses an internal process-deviation, not an adversary. **No threat-anchored probe is required** (§6.13 / §35.5 — the layer verifies named-threat COVERAGE, not threat-defeat-in-general; threat-enumeration completeness stays ARGUS's residual).

This explicit classification IS the required record (§35.5). ARGUS: please confirm the carve-out or, if you judge a runtime attack path exists (e.g. the bash `-lc` invocation in fix (a) as an injection surface), raise it `load_bearing: true`. (DAEDALUS pre-empts: fix (a)'s `-lc` string interpolates only fixed-literal names — `$ticket`/`$attachName` are script constants, `$tmp` is a fixed-literal temp path — no caller/agent-controlled content reaches the bash string, so I judge no injection surface; flagged here for ARGUS confirmation.)

---

## §6 Self-assessed weak points

- **W1 — the gauntlet-default detector is detection, not prevention (the load-bearing residual).** Clause (E) injects a self-check on the working Stop channel; it does NOT mechanically parse the transcript to PROVE "POLYBIUS dispatched CAPTAINs without a PLINY." A determined seat can read the clause and dismiss it. *Why this shape anyway:* the directive's DoD explicitly accepts "honestly document the residual convention-only gap if the mechanism is advisory" (bullet 4); a reliable transcript classifier is a separate detection arc (§35.5's during-build/Arc-B pattern is the precedent); and detection-on-a-working-channel + recorded-deviation is strictly more than today's nothing. NAMED, not hidden.
- **W2 — the say-trigger + multi-line preamble interaction is the most brittle launcher mechanic.** Prepending a multi-line preamble to a bare say-word risks (a) breaking wt-pane passing (the L122-125 known break) and (b) the CLAUDE.md say-trigger not firing if the bare word is no longer the whole prompt. *Why this shape anyway:* I force `-Layout Windows` for any preamble-injected/composition launch (extending the existing L125 guard), which is the proven-robust path; and the L2 canon backstop means even a misfired preamble still establishes the chain once the role file loads. But VERA must verify P1's printed shape carefully, and ARGUS should weigh whether forcing Windows for the *standard say-trigger* launch is too heavy (it changes the default panes UX). **Residual question for ARGUS.**
- **W3 — per-seat composition fields have no atomic "this is ONE composition" grouping.** Expressing composition per-row (DC4) keeps ONE registry but means the read side infers a composition from `(project, machine, launched-at-window)` + matching `composition` value — a window heuristic, not a composition-id. *Why this shape anyway:* it avoids a second manifest artifact (the directive's ONE-registry + non-divergence-with-`u--9s2` constraint), and the launch loop records all seats in one pass so the window is tight. If `u--9s2` needs a hard composition-id, that's an additive field later, not a rebuild.
- **W4 — clause (E) cannot distinguish a legitimate solo build-session from the AR-7 failure.** `MAJOR_PLINY.md` L44/L163 explicitly bless "build sessions for early arcs where no CAPTAINs exist do the work directly." Clause (E) will nudge those too. *Why this shape anyway:* it is a reminder, not a block (degrades like clause A), so a legitimate solo seat reads it, recognizes it does not apply, and proceeds — bounded false-positive cost, same property as the PostToolUse NOMOS reminder's bounded no-op.

---

## §7 Residual questions for ARGUS
- RQ1 (W2): is forcing `-Layout Windows` for the standard say-trigger launch (when the preamble is injected) acceptable, or should the preamble be SHORTER / passed differently so panes still work? Weigh default-UX cost vs chain-establishment robustness.
- RQ2 (§5): confirm the `not threat-ratified (process change)` carve-out, OR judge whether fix (a)'s `bash -lc` is a runtime injection surface (I judge not — fixed-literal interpolation only).
- RQ3 (W1): is detection-on-Stop-channel + recorded-deviation a sufficient read of "structurally guarantee" for the PRINCIPAL's bar, or does the floor-manager want the residual escalated before build?

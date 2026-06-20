# Arc 68 build directive — Launcher-correctness (chain-of-command at launch · gauntlet-by-default · variable team composition)

**Audience:** the fresh Claude Code sessions opened to build Arc 68 (PLINY_the-stoa + the floor-manager POLYBIUS_the-stoa).
**Authored by:** Polybius_the_Stoa (user-level Stoa agent, sid 990b0750-5572-4836-b9c7-18d626a12e96) on behalf of the PRINCIPAL (Denson Smith) via Polybius the Grand.
**Status:** FINALIZED on the brief's §ADDITIONAL LAUNCHER-CORRECTNESS REQUIREMENTS (2026-06-20) — the WHAT is PRINCIPAL-locked; the HOW is your team's design. NOT yet dispatched — staged pending a PRINCIPAL scope-nod, then committed + launched.
**Builds on:** current the-stoa main (`244180e`) + the SHIPPED Arc 67 identity layer. This arc does NOT re-build identity (mint/name/record + whoami + sign-everywhere + the `stoa--reg` registry all landed in Arc 67 / `stoa--p7c`, CLOSED). It adds the LAUNCHER-CORRECTNESS layer ON TOP. Project-tier charter: **`stoa--pk4`**. User-tier anchor (visible only to user-tier): `u--5f0`.

**You are MAJOR_PLINY for the the-stoa Arc 68 engagement.** Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role. Open Claude Code in `C:\Users\denso\claude_projects\the-stoa\`.

**Your one job:** make the team-launcher + its activation STRUCTURALLY guarantee the by-the-book forge, so a seat CANNOT silently run solo: (1) **complete activation that establishes the chain** PRINCIPAL→POLYBIUS→PLINY→CAPTAINs — PRINCIPAL is never pointed at PLINY, the seats are not co-equal panes; (2) **gauntlet-by-default** — the full gauntlet is the default, not a seat's discretionary call; (3) **variable team composition** — the launcher supports launching + placing additional seats in the chain by composition (precise trigger: an arc designing custom **agents** pulls in MAJOR_CHIRON; an arc designing custom **workflows** pulls in MAJOR_HAMILTON — either, both, or neither), not a hard-wired two-seat default. Then return cleanly.

**This is a substrate-canon arc — run the full gauntlet** (DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS). It touches the team-launcher tooling, the `gauntlet-setup` skill, `operating-disciplines.md` canon, and the MAJOR role files. **Arc 68's own design is DAEDALUS-led with the standard POLYBIUS+PLINY team** — this arc BUILDS the variable-composition machinery (launcher tooling); it does not itself design a custom agent or a custom workflow, so CHIRON/HAMILTON are NOT pulled into Arc 68's design phase. (They are the seats the machinery composes in FUTURE custom-agent / custom-workflow arcs — see DC3.)

---

## Comms — async with Polybius_the_Stoa via bw (`stoa--*`)

Coordinate on the charter ticket **`stoa--pk4`** (it carries the locked scope + the AR-7 motivating case — you cannot see the user-tier `u--5f0`). Polybius_the_Stoa (the user-level seat that owns this arc) monitors + interjects; the floor-manager runs independent verification at each hand-back and relays up. The PRINCIPAL is NOT the relay — beadwork is. Asymmetric polling: don't poll while working; do poll when waiting via `CronCreate */5`. `bw comment <id> "text"` is **positional, no `-m`**. Run `bw prime` at activation.

**DOGFOOD:** from turn one, every seat signs bw comments `[from: <NAME> | sid <session-id>]` — your sid via the deployed `whoami` skill (reads `$CLAUDE_CODE_SESSION_ID`). This arc HARDENS the activation that the dogfood rides on; live the chain you are building.

---

## Read first (the spec)

1. **The charter `stoa--pk4`** — body + comments: the locked 3-guarantee scope + the AR-7/nws-iey case study (a solo POLYBIUS, incomplete activation, direct CAPTAIN-spawn, self-cert with one CATO). That failure is what the launcher must make STRUCTURALLY IMPOSSIBLE.
2. **`substrate/skills/team-launcher/launch-team.ps1`** — the current launcher (post-Arc-67: mints `--session-id`/`--name`, records to `stoa--reg`, carries `-ArcId`/`-OnlySeat`/`-AutoPaste`/`-Layout`). This is the artifact that grows the chain-establishment + composition machinery.
3. **`substrate/skills/team-launcher/SKILL.md`** + **`substrate/skills/gauntlet-setup/SKILL.md`** — the activation-brief pattern (two briefs, FM-first-then-PLINY, the chain-of-command + polling disciplines the briefs already encode). The gauntlet-setup skill ALREADY documents much of the correct chain; this arc moves it from "the human authors it per-arc" toward "the launcher structurally guarantees it."
4. **`substrate/MAJOR_POLYBIUS.md` + `substrate/MAJOR_PLINY.md`** — the chain-of-command roles (POLYBIUS supervises; PLINY takes direction from POLYBIUS, surfaces to POLYBIUS not PRINCIPAL; PLINY runs the gauntlet). The canon that the activation must reliably establish.
5. **`substrate/operating-disciplines.md`** — the chain-of-command / surface-up / gauntlet disciplines (§7 routing, the relevant gauntlet sections). Where the "gauntlet-by-default" + "variable composition" canon lands.
6. **CHIRON + HAMILTON role files** (`substrate/MAJOR_CHIRON.md`, `substrate/MAJOR_HAMILTON.md`) — the seats the variable-composition machinery must be able to launch + place in FUTURE custom-agent (CHIRON) / custom-workflow (HAMILTON) arcs. DAEDALUS reads them to design the composition + chain placement; they are NOT participants in Arc 68's own design.

---

## Settled — do NOT re-litigate (PRINCIPAL-locked WHAT + verified facts)

### The three launcher-correctness guarantees (PRINCIPAL, locked)
1. **CHAIN OF COMMAND AT LAUNCH.** PRINCIPAL addresses ONLY POLYBIUS; POLYBIUS supervises PLINY (directs + verifies hand-backs via bw); PLINY spins up the CAPTAINs. The launch + activation make this explicit so PRINCIPAL is **never pointed at PLINY** and the seats know their place — NOT co-equal independent panes the PRINCIPAL coordinates separately.
2. **GAUNTLET-BY-DEFAULT.** The full gauntlet is the DEFAULT, not a seat's discretionary call. A seat must not be able to silently run solo with one self-chosen checker.
3. **VARIABLE TEAM COMPOSITION.** The team is NOT always POLYBIUS+PLINY. The precise trigger (PRINCIPAL, 2026-06-20): an arc that designs custom **AGENTS** pulls in **MAJOR_CHIRON** (team-architect); an arc that designs custom **WORKFLOWS** pulls in **MAJOR_HAMILTON** (workflow architect) — either, both, or neither. The launcher supports launching + PLACING these in the chain by composition. (NOT generic "design-heavy" — Arc 68 itself is launcher tooling and uses the standard two-seat team.)

### Verified facts — do NOT re-derive (confirmed vs Claude Code 2.1.170 + live test, Arc 67)
- `claude --session-id <uuid>` pins a known id at launch; `--name <name>` MUST be **space-free** (wt arg-splitting; use underscores); `--remote-control [name]` bridges to desktop/phone.
- Sessions are **LOCAL-ONLY** — no cloud sync, no cross-machine `--resume`. A session-id is a same-machine handle; cross-machine continuity stays on bw + handoffs. Do NOT design around cloud-resume.
- `$CLAUDE_CODE_SESSION_ID` is a **native** Bash-subprocess env var (since CC v2.1.132): a terminal seat reads its OWN sid; a sub-agent reads its CALLER's sid. The `whoami` skill (Arc 67) is built on this — the older nonce-grep recipe is RETIRED.
- The identity layer is SHIPPED — reuse it; do not re-open the schema/registry debate (`stoa--reg` is the registry).

---

## Design items — your team's HOW (DAEDALUS resolves in Phase A; surface at the design hand-back)

- **DC0 — the central tension: STRUCTURAL vs CONVENTIONAL enforcement.** "Structurally guarantee" / "structurally impossible" is the PRINCIPAL's bar, but a launcher + an activation paste are ultimately TEXT a seat could ignore. DAEDALUS decides HOW FAR structural goes — launcher-injected activation preamble, a templated chain-of-command block every brief inherits, role-file canon, and/or a HOOK (cf. the existing Stop self-check / PreToolUse gates) that detects "a POLYBIUS seat that dispatched CAPTAINs without a PLINY / without the gauntlet." Name the residual convention-only gap honestly (what the launcher CAN'T force) rather than over-claiming structural where it is advisory.
- **DC1 — chain-of-command establishment.** How does the launch make the chain explicit + durable? Options to weigh: a launcher-injected preamble in each seat's activation that states the seat's place + who it reports to + who reports to it; the PLINY activation explicitly "you take direction from POLYBIUS via bw, NOT from PRINCIPAL; surface to POLYBIUS"; the POLYBIUS activation "you supervise PLINY; PRINCIPAL addresses you." Ensure the SAY-TRIGGER default (bare `polybius`/`pliny`) ALSO establishes the chain (via the role file), not only the bespoke `-AutoPaste` brief path.
- **DC2 — gauntlet-by-default mechanism.** How is the gauntlet made non-discretionary? A launch-recorded `gauntlet=required` signal + a checker that flags a solo-with-one-CATO close? An activation that structurally names the gauntlet phases as the default path? Opt-OUT requires explicit POLYBIUS/PRINCIPAL waiver (not a seat's silent opt-in to solo). Tie to DC0 — decide launcher vs hook vs canon, and what is genuinely enforced vs strongly-defaulted.
- **DC3 — variable composition model + chain placement.** Extend the launcher (it already has `-Seats`/`-OnlySeat`) to support named compositions keyed to the WORK: a custom-**AGENT**-design composition adds CHIRON; a custom-**WORKFLOW**-design composition adds HAMILTON (either / both / neither) — the precise trigger, NOT generic "design-heavy". Decide: are CHIRON/HAMILTON terminal seats the launcher spins up, or PLINY-dispatched? WHERE do they sit in the chain (report to PLINY? to POLYBIUS?)? How does the launcher PLACE them (their activation + chain position)? Record the composition into `stoa--reg`.
- **DC4 — registry + manifest coordination (ONE registry).** The composition/placement reuses `stoa--reg` (the Arc-67 registry). Coordinate the composition-manifest shape with the builder-deploy cookie-cutter follow-on (user-tier `u--9s2`) so the two do NOT diverge — one registry, one manifest model. (Do not BUILD the builder-deploy work; only keep this registry adoptable by it.)

---

## Deliverables (land together)

1. **Launcher** — `substrate/skills/team-launcher/launch-team.ps1`: chain-establishment in activation (DC1), gauntlet-by-default signal (DC2), variable-composition support + chain placement incl. CHIRON/HAMILTON (DC3), composition recorded to `stoa--reg` (DC4). Update `substrate/skills/team-launcher/SKILL.md`.
2. **`gauntlet-setup` skill** — `substrate/skills/gauntlet-setup/SKILL.md`: reconcile with the launcher's new structural guarantees (the skill currently carries the chain-of-command + two-brief discipline as human-authored checklist; align it with what the launcher now guarantees).
3. **Canon** — `operating-disciplines.md`: the gauntlet-by-default + variable-composition + chain-of-command-at-launch disciplines (new section or extend the relevant §7 routing / gauntlet sections). Reference from `MAJOR_POLYBIUS.md` / `MAJOR_PLINY.md` where each seat's chain role is stated.
4. **Enforcement surface (per DC0/DC2)** — whatever the design lands as the structural mechanism (hook, recorded signal, activation template). If a hook: deploy via the established hook path; honest fail-open per the existing hook convention.
5. **Dangling refs / consistency** — `install.sh` (any new skill/hook in the name lists), role-file cross-refs, no stale "two-seat default" or "PRINCIPAL coordinates the panes" framing left in the touched docs.

---

## Verification / Definition of done

The launcher's `-DryRun` early-returns before opening sessions, so it can ONLY prove the printed command + activation shape — NOT a live multi-seat chain. Gate the verifiable parts on REAL execution (banked lesson: a DoD that gates on `--dry-run` cannot test what the dry-run skips):

- **Command + activation shape (`-DryRun`):** the printed launch for a custom-agent / custom-workflow composition includes the CHIRON/HAMILTON seats with space-free `--name` + `--session-id`, and each seat's activation carries the chain-of-command preamble (who it reports to). (This is what the dry-run can verify.)
- **Composition record — REAL execution:** VERA exercises the variable-composition record path FOR REAL (records a synthetic custom-agent/workflow composition's seats → `stoa--reg` and reads them back, with chain positions) WITHOUT spawning live agents.
- **Chain-of-command text — structural check:** grep/inspect the generated activations to prove the PLINY activation routes PLINY→POLYBIUS (never PLINY→PRINCIPAL) and the POLYBIUS activation owns supervision; the SAY-TRIGGER default path ALSO establishes the chain via the role file.
- **Gauntlet-by-default (per DC0/DC2):** demonstrate the chosen mechanism actually fires on the AR-7 failure shape (a POLYBIUS that dispatched CAPTAINs without a PLINY / without the gauntlet is flagged), OR honestly document the residual convention-only gap if the mechanism is advisory.
- **Canon greps:** `operating-disciplines.md` carries the three disciplines; role files reference them; no stale two-seat/co-equal-panes framing remains in touched files.
- **NOMOS CONFORMANT** on the final commit. Commits carry `Author=PRINCIPAL` + the seat-identity Co-Authored-By trailer per §28.9.
- Committed + pushed to `the-stoa` main; charter `stoa--pk4` updated with the landing SHA.

---

## Out of scope

- **Re-building the Arc 67 identity layer** — mint/name/record/whoami/sign-everywhere/`stoa--reg` are SHIPPED; reuse, don't rebuild.
- **The builder-deploy cookie-cutter BUILD (`u--9s2`)** — only keep the composition/registry adoptable by it (DC4); do not build the builder launcher here.
- **Cross-machine `--resume` / cloud-sync** — not a thing; continuity stays on bw + handoffs.
- **A full `operating-disciplines.md` audit** beyond the three disciplines — fix-now/ticket anything found, don't expand scope.
- **The apply.sh/install.sh seat-trailer signing gap (`stoa--tg7`)** — a separate parked tooling ticket; do not fold it in unless the design genuinely touches those commit sites.

---

## Discipline

- Full gauntlet — canon + tooling; NOT mechanical. Arc 68's design is DAEDALUS-led with the standard POLYBIUS+PLINY team (this arc is launcher tooling, not custom-agent/workflow design).
- Verify-then-execute; one-job-per-agent (resist drifting into the builder-deploy work).
- Fix-now for small related defects; ticket-with-plan if scope-different.
- DOGFOOD the chain you are building: every seat signs id+name; PLINY surfaces to POLYBIUS, not PRINCIPAL.
- bw syntax: positional `bw comment`; `bw prime` at activation; `--reason` on close.
- The irony is the point: this is the arc that abolishes the solo-POLYBIUS — run it by-the-book or it refutes itself.

## Suggested phasing

- **Phase A — design (DAEDALUS).** Resolve DC0–DC4: the structural-vs-conventional decision (DC0) first, then the chain-establishment, gauntlet-default mechanism, composition model, and registry coordination. Produce the concrete edit plan + surface to Polybius_the_Stoa / the floor-manager for a go/no-go before build.
- **Phase B — tooling (ADA).** Launcher chain-establishment + gauntlet-default signal + variable-composition; gauntlet-setup skill reconciliation; any hook.
- **Phase C — canon (ADA).** operating-disciplines disciplines + role-file references.
- **Phase D — verify (ARGUS/VERA/CATO + NOMOS).** Dry-run shape; REAL composition-record round-trip; chain-of-command structural greps; gauntlet-default mechanism fires on the AR-7 shape; ground-truth.
- **Phase E — ship.** Commit + push; update `stoa--pk4` with the SHA.

Standby, run.

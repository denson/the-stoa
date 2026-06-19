# Arc 67 design-rev1 — Session-identity deployment pattern (stoa--p7c)

**Author:** Denson Smith (synthesis, structural choices, hand-off contracts). Design seat: CAPTAIN_DAEDALUS_the-stoa.
**Charter:** `stoa--p7c` · **Directive:** `substrate/arcs/arc-67-build-directive.md` @ bd15fc3 · **Branch:** `arc-67/build`.
**Operating mode:** autonomous (surfaces at hand-back for go/no-go; no mid-design round-trip).

---

## §1. Problem restatement

Make Stoa agent **identity** first-class and durable so a message on the shared `cm-` commons (or any bw store) carries a structural, machine-resolvable signal of *which seat / role / project / machine* authored it. Four PRINCIPAL-locked requirements (the WHAT is locked; this doc designs the HOW):

1. **LAUNCH** — `launch-team.ps1` ALWAYS mints a per-seat UUID, assigns a space-free human-friendly name, launches `claude` with `--session-id <uuid>` + `--name <name>` (+ optional `--remote-control`), and RECORDS `seat→{session-id, name, project, machine}` durably to a portable bw registry.
2. **WHOAMI** — a new python skill any seat runs to discover its own session-id (nonce-grep), for desktop-UI-created sessions that could not pin `--session-id` at creation.
3. **SIGN-EVERYWHERE** — broaden op-disc §28 so every seat carries its session-id + name in ALL channels (bw comments, git trailers, recordkeeping), preserving the §28 absolute: git `Author:` stays the PRINCIPAL's identity.
4. **REGISTRY** — `seat→{id,name,project,machine}` lives in **bw** (git-synced, portable; session-ids are per-machine so the roster must survive cross-machine).

**Imported assumptions (named, not smoothed):**
- *A1 — session-ids are same-machine handles only.* No cross-machine `--resume`/cloud-sync; the registry records ids for liveness/audit on the minting machine, NOT for cross-machine session resumption. Continuity stays on bw + handoffs. (Directive Settled facts.)
- *A2 — DC1 folds stoa--fpj.* The substrate launcher (171L) lacks `-ArcId`/`-OnlySeat` the deployed copy (200L) has; a blind `install.sh` of the 171L source would REGRESS deployed consumers. Resolving the SSoT inversion is in-scope regardless of fold-vs-sequence.
- *A3 — the origindex builder-publish security model is ORTHOGONAL* (network-access identity: Tailscale/SSO; defines no seat registry). Do not force-converge. The convergence target is the FUTURE builder-deploy launcher, which adopts THIS registry.
- *A4 (design-time empirical, load-bearing — see DC4):* a **sub-agent**'s transcript is NOT `<slug>/<uuid>.jsonl`; it is `<slug>/<parent-session-id>/subagents/agent-<id>.jsonl`. Sub-agent CAPTAINs therefore have **no terminal session-id** to discover. This is the concrete mechanism behind the DC3 terminal-vs-sub-agent signing split, verified live this design pass (my own nonce landed in `…/a3e23bca…/subagents/agent-a3161877da446846e.jsonl`).

---

## §2. Approach

### DC1 — FOLD stoa--fpj into the launcher rewrite (RESOLUTION: FOLD)

**Decision: FOLD.** One coherent rewrite of `substrate/skills/team-launcher/launch-team.ps1` that (a) backports the deployed copy's `-ArcId`/`-OnlySeat` params + their two logic blocks, AND (b) adds the new mint-UUID / assign-name / record-to-registry machinery. Result: one launcher that is both correct AND the substrate SSoT.

**Rationale.** The 200L deployed copy is a strict superset of the 171L substrate source: the diff is exactly the two params (L64-65), the `-ArcId` gauntlet-seat block (L89-104), the `-OnlySeat` filter (L121-125), the `Get-SeatPrompt` `$seat.Prompt` branch (L138), and the two Write-Host `(activation prompt seeded)` annotations + the `$anyPrompt` final-message branch. None of that conflicts with the session-id machinery (which adds a per-seat `SessionId` field + the `--session-id` token + a post-loop record step). Folding is a clean superset-merge, NOT a tangled rewrite — the diff stays readable. **Fold-vs-sequence recommendation: FOLD; no sequencing needed.** (If ARGUS judges the combined diff unreadable, the fallback is: land the 200L deployed copy verbatim into substrate first as a pure SSoT-reconciliation commit, then layer session-id on top — but I do not recommend it; it doubles the commit count for no readability gain.) Either way the SSoT inversion is resolved in this arc; a blind `install.sh` of today's 171L source would strip `-ArcId`/`-OnlySeat` from every deployed consumer.

**Start the rewrite from the 200L deployed copy** (`~/.claude/skills/team-launcher/launch-team.ps1`), not the 171L substrate source — the deployed copy already has the correct `-ArcId`/`-OnlySeat` behavior; we add session-id to it and write the result back to substrate.

### DC2 — registry: a dedicated bw ticket whose attachment is a JSONL manifest on the beadwork branch (RESOLUTION)

**Decision.** The registry is a **single dedicated bw ticket** (`stoa--reg`, title `Stoa seat registry — seat→{session-id,name,project,machine}`) whose **durable payload is a JSONL manifest attached on the `beadwork` branch** at `attachments/stoa--reg/seat-registry.jsonl`. One row per active seat; append-by-rewrite (read current, append/replace the row, re-attach). bw comments on the ticket are NOT the roster rows (comments are an append-only log, awkward to query/dedupe); they are a human-readable change-log. The machine-readable roster is the attached JSONL.

**Why this shape over the alternatives:**
- *vs comments-as-rows:* comments cannot be updated or removed (a stale/dead seat row would accumulate forever); JSONL is rewriteable, so liveness updates and seat retirement are clean.
- *vs a file committed to `main`:* the beadwork branch is the git-synced portable store that already travels cross-machine (it carries all bw state); `bw attach` writes there and commits with a single-line intent. Putting the roster on `main` would couple roster churn to code history. **`bw attach` is the native, already-portable write path** — verified: `bw attach <id> <file> --name <path>` stores bytes at `attachments/<id>/<path>` on beadwork and commits.
- *vs converging with the origindex security model:* orthogonal (A3) — that is network identity, not a seat roster.

**Record schema (one JSON object per line):**
```json
{"seat":"POLYBIUS_the-stoa","name":"Polybius_the_Stoa","session_id":"990b0750-5572-4836-b9c7-18d626a12e96","project":"the-stoa","machine":"<hostname>","role":"floor-manager","tier":"project","launched_at":"2026-06-19T21:00:00Z","status":"alive"}
```
Fields: `seat` (the canonical `ROLE_slug` mnemonic, the `[for:]` address), `name` (human-friendly, space-free, non-unique), `session_id` (the unique handle; per-machine), `project` (slug), `machine` (hostname — disambiguates per-machine ids), `role`, `tier`, `launched_at` (ISO-8601 Z), `status` (`alive` | `retired`). `session_id` may be `null` for a seat that has not yet self-discovered (e.g. a desktop session pre-whoami); `name`+`seat`+`machine` still identify it.

**Write recipe (how a seat records itself) — the REAL-execution-testable path:**
A tiny helper `record-seat.ps1` (ships beside the launcher in the team-launcher skill dir) that:
1. `git show beadwork:attachments/stoa--reg/seat-registry.jsonl` → current manifest (empty string if absent).
2. Drop any existing line whose `(seat,machine)` matches (idempotent re-record / liveness refresh).
3. Append the new JSON line; write to a temp file.
4. `bw attach stoa--reg <temp> --name seat-registry.jsonl` (overwrites the stored path verbatim; commits to beadwork).

This is callable **standalone, without spawning a live agent session** — the launcher calls it per seat after computing `{seat,name,session_id,project,machine}`, and VERA calls it directly with a synthetic row (see P3). The launcher's `-DryRun` PRINTS the intended `record-seat.ps1` invocation but does NOT execute it (consistent with dry-run-prints-only); the REAL round-trip is exercised by calling `record-seat.ps1` directly.

**Read recipe (PRINCIPAL: "which seat owns which project / is it alive"):**
`git show beadwork:attachments/stoa--reg/seat-registry.jsonl` → pipe through `jq` (or PowerShell `ConvertFrom-Json`) filtered on `project` / `status=="alive"`. Documented in the registry's own bw-ticket body + the team-launcher SKILL.md.

**Adoptability by the future builder-deploy launcher (DC2 single-roster requirement):** the schema is launcher-agnostic (`seat`/`project`/`machine` carry no the-stoa-specific assumption) and the write recipe is a standalone PS1 the builder launcher calls the same way. One registry, one ticket, one schema — the builder-deploy work ADOPTS `record-seat.ps1` + `stoa--reg`, it does not stand up a second roster.

### DC3 — sign-everywhere: BROADEN §28 via a new sibling subsection §28.9 (RESOLUTION)

**Decision.** Add a new subsection **§28.9 "Session-identity sign-everywhere (all seats, all channels)"** rather than rewriting §28.1–§28.8 (which are git-trailer-specific and empirically anchored; rewriting them risks losing the squash-merge anchors). §28.9 broadens scope to: ALL seats, ALL channels, carrying **session-id + name** (not just the seat mnemonic). The §28 absolute is restated verbatim and PRESERVED: git `Author:` stays PRINCIPAL; id+name layer ON TOP, never in place of.

**The terminal-vs-sub-agent signing distinction (the real gap, A4):**

| Seat class | Has terminal session-id? | bw-comment sign format | git trailer |
|---|---|---|---|
| **Terminal seat** (top-level session: POLYBIUS/PLINY, any `--session-id`-launched or whoami-discoverable seat) | YES | `[from: <Name> \| sid <session-id> \| <project>]` | existing §28.1 `Co-Authored-By` + optional `Stoa-Session-Id: <sid>` trailer |
| **Ephemeral sub-agent CAPTAIN** (Agent-tool dispatch: ADA/VERA/CATO/ARGUS/DAEDALUS/…) | NO (transcript is `…/<parent-sid>/subagents/agent-<id>.jsonl`; no own terminal session-id) | `[from: CAPTAIN_<MNEMONIC>_<slug>]` (seat mnemonic; no sid — sid is unavailable by construction) | existing §28.1 `Co-Authored-By: CAPTAIN_<MNEMONIC>_<slug>` (unchanged) |

This is dogfooded by THIS design: I am an ephemeral sub-agent, so I sign `[from: CAPTAIN_DAEDALUS_the-stoa]` with no sid — exactly the sub-agent row. Terminal seats (the floor-manager, PLINY) sign with sid, as they already did on this charter ticket.

**Concrete formats + placement per channel (§28.9 body):**
- **bw comments** — first line of every comment is the sign-tag above. (Already in live practice on this ticket; §28.9 makes it canon.)
- **git trailers** — unchanged from §28.1 for CAPTAINs; terminal seats committing directly (POLYBIUS housekeeping) MAY add `Stoa-Session-Id: <sid>` as a second trailer (the floor-manager already did this on bd15fc3's parent — `Stoa-Session-Id: 990b0750-…`). Author stays PRINCIPAL.
- **recordkeeping** — the registry row (DC2) is the durable record; `session_id` + `name` + `seat` are its identifying fields.

**Q5 (id+name as the canonical `[for:]` routing address):** the `seat` field (`ROLE_slug`) is the routing address; `[for: POLYBIUS_the-stoa]` resolves against the registry's `seat` column. §28.9 states this so the convention is the address.

**Role-file references (per-seat application of §28.9):** add a one-line pointer in each MAJOR_*.md and CAPTAIN_*.md comms/discipline section: *"Sign every bw comment + commit per op-disc §28.9 (terminal seats: `[from: Name | sid <id> | project]`; sub-agent CAPTAINs: `[from: CAPTAIN_<MNEMONIC>_<slug>]`)."* Concretely: `MAJOR_POLYBIUS.md`, `MAJOR_PLINY.md` (terminal class), and the CAPTAIN role files' existing §6.5 heartbeat/bw-comment disciplines (sub-agent class) get the pointer. This is a *pointer*, not a re-statement, to keep §28.9 the SSoT.

### DC4 — whoami skill: python, conservative subsequent-turn flush, terminal-only (RESOLUTION)

**Decision.** A python skill `substrate/skills/whoami/` (SKILL.md + `whoami.py`) implementing the nonce-grep recipe with the **conservative model: emit nonce on one turn, grep on a subsequent invocation** — with a built-in flush-retry loop so a single skill run can still succeed if the nonce has flushed. Verified live this pass: my same-turn grep found NOTHING; the subsequent bash call found it. The conservative model is correct; the retry loop makes it robust without forcing a two-turn UX.

**The load-bearing refinement (A4):** the recipe "session id = filename minus `.jsonl`" is ONLY valid for a **top-level terminal session** transcript (`<slug>/<uuid>.jsonl`). A sub-agent's nonce lands in `<slug>/<parent-sid>/subagents/agent-<id>.jsonl` — basename `agent-<id>`, which is NOT a session-id. So whoami MUST:
1. Emit a unique nonce: `SELFID-<uuid4>` (uuid4 handles concurrent same-dir sessions — no collision).
2. Grep the store for the nonce across `~/.claude/projects/C--Users-denso-claude-projects*/` (the `*` glob covers the user-tier slug + every per-project slug).
3. **Filter to top-level matches only:** a match path of the form `<store>/<slug>/<uuid>.jsonl` (parent dir == a project-slug dir, basename is a UUID, NOT under a `subagents/` segment) → report `<uuid>` as the session-id.
4. **If the only match is under a `subagents/` segment** → report: *"You are an ephemeral sub-agent; you have no terminal session-id. Sign with your seat mnemonic per §28.9."* (Exit non-zero / distinct status so a caller can branch.)
5. **If no match yet** → flush-retry: sleep + re-grep up to N times; if still nothing, instruct the caller to re-run on the next turn (the conservative fallback).

**Output contract:** on success, print the bare session-id to stdout (and optionally `--verbose` prints the matched store path); on sub-agent detection, print the sub-agent notice to stderr + exit code 2; on not-yet-flushed, exit code 3 with the re-run instruction. The bare-id stdout is what a terminal seat captures to self-record into the registry (DC2 write recipe).

**Store-root portability:** the skill resolves the store root from `$HOME/.claude/projects` (not the hard-coded `C:\Users\denso\…`), so it works for any PRINCIPAL; the slug glob is `C--*claude-projects*` derived from `$HOME` → portable.

---

## A3 threat→mitigation map

Per op-disc §35.1 + DAEDALUS §6.12: this arc is a **process / role-file / tooling hardening** change. It adds an identity/provenance CONVENTION; it introduces **no runtime attack surface** (no new network endpoint, no credential flow, no privilege boundary). Classification:

> **not threat-ratified (process + tooling change; no runtime attack path).** The sign-everywhere convention is provenance metadata, not an authentication or authorization control — it is forgeable by design (an agent could write a false `[from:]`), exactly as the charter's "convention vs enforcement" Q3 notes. No named threat is *defeated* by a mechanism here; the registry/sign-everywhere improve *auditability*, they do not gate access. The Remote-Control remote-approve gap is explicitly noted-not-solved (out of scope). ARGUS confirms this classification (§35.5 self-carve-out: I propose, ARGUS confirms; I cannot grant my own carve-out).

No `M<n>` rows; no threat-anchored probe required (§6.13 self-carve-out applies). If ARGUS judges any element security-relevant (e.g. the forgeable-provenance property rising to a named threat on the shared `cm-` commons), that is the residual I flag for ARGUS below.

---

## §3. Verification probes (VERA executes; labelled P1..P9)

**P1 — launcher dry-run command shape (the ONLY thing dry-run can prove).**
`pwsh -File substrate/skills/team-launcher/launch-team.ps1 -DryRun -ArcId arc-67 -Slug the-stoa` → printed `wt`/`pwsh` command for EACH seat contains `--session-id <uuid>` (a real GUID shape) AND `--name <space-free-name>`. Assert: grep the dry-run stdout for `--session-id` followed by a `[0-9a-f-]{36}` token, and `--name` followed by a token containing no spaces. Two seats → two `--session-id` occurrences.

**P2 — dry-run prints the record step but does NOT execute it.**
Same dry-run run: stdout names the `record-seat.ps1` invocation (a `[dry-run]` line), AND `git show beadwork:attachments/stoa--reg/seat-registry.jsonl` is UNCHANGED by the dry-run (no synthetic row written). Confirms the DoD constraint that dry-run early-returns before any real write.

**P3 — registry write, REAL execution (no live spawn).**
Call `record-seat.ps1` directly with a synthetic row: `pwsh -File .../record-seat.ps1 -Seat TESTSEAT_probe -Name Test_Probe -SessionId 00000000-0000-0000-0000-000000000000 -Project the-stoa -Machine $(hostname) -Role probe -Tier test`. Then `git show beadwork:attachments/stoa--reg/seat-registry.jsonl | jq -c 'select(.seat=="TESTSEAT_probe")'` returns the row with all fields. Then re-run with a different `SessionId` for the SAME `(seat,machine)` → assert the manifest has exactly ONE `TESTSEAT_probe` row (idempotent replace, not append). **Cleanup:** remove the synthetic row + re-attach (fixed literal path `attachments/stoa--reg/seat-registry.jsonl`, no `$VAR` in the destructive step). This is the REAL mint+record round-trip without spawning an agent.

**P4 — whoami REAL round-trip (terminal seat).**
The running VERA/dogfood terminal session runs the whoami skill; assert it returns a 36-char UUID that matches an actual `<slug>/<uuid>.jsonl` file on disk (`test -f "$HOME/.claude/projects/<slug>/<returned-id>.jsonl"`). For the subsequent-turn flush case, the retry loop must succeed within N retries or the probe re-runs on the next turn (documented as a two-call probe).

**P5 — whoami sub-agent detection.**
Run whoami from inside an Agent-tool sub-agent (or simulate by greping a nonce known to be in a `subagents/` path); assert it returns the sub-agent notice + exit code 2, NOT a bogus `agent-<id>` "session-id". (Guards against A4 regression.)

**P6 — §28.9 broadening + Author-stays-PRINCIPAL absolute preserved.**
`grep -n "session-id" substrate/operating-disciplines.md` shows §28.9 exists; grep confirms §28.9 contains both the terminal-seat format `[from:` ... `sid` and the sub-agent format `[from: CAPTAIN_`; AND §28.9 restates "Author: stays PRINCIPAL". Role files (`MAJOR_POLYBIUS.md`, `MAJOR_PLINY.md`, the CAPTAIN role files' §6.5) each contain a §28.9 pointer.

**P7 — no cross-machine-resume promise (grep clean-check).**
`grep -rni "resume" substrate/skills/whoami/ substrate/skills/team-launcher/ ` and the §28.9 text → every "resume" hit (if any) is same-machine-correct usage; NO text promises cross-machine session resume. Expected: zero cross-machine-resume claims.

**P8 — substrate session-id reference clean-check.**
`grep -rn "session-id\|--session-id\|whoami" substrate/` returns ONLY intended references (the launcher, whoami skill, §28.9, team-launcher SKILL.md, role-file pointers) — no stray/dangling refs.

**P9 — install.sh deploys whoami; launcher interim-note resolved.**
`whoami` is in `SKILL_NAMES` in `substrate/install.sh` (grep). The launcher's old L49-50 interim-seat-name note (`adopt the formal Role_Project_Instance id when stoa--p7c lands`) is RESOLVED — replaced with a pointer to §28.9 + the registry (grep confirms the "interim ... when stoa--p7c lands" phrasing is gone). `install.sh --dry-run` (subproject + project tier) still passes its A–E recompose checks (full-suite, not just "this arc touched no X").

**Full-suite belt-and-suspenders:** VERA runs the project's existing install.sh smoke test + `npm run gen-data` (the launcher/skill changes are gen-data-adjacent only via skill rendering; gen-data re-derives the whole roster and surfaces any pre-existing drift — assert from a FULL suite run, not "this arc edited no agent frontmatter").

---

## §4. Self-assessed weak points (what I'd want ARGUS to attack hardest)

1. **WEAK — sub-agent whoami detection rests on the `subagents/` path convention (A4), which is a Claude Code internal I verified live ONCE on this machine/version (2.1.170).** If Claude Code changes the sub-agent transcript layout, P5 breaks and whoami could return a bogus `agent-<id>`. *Why this shape anyway:* the skill FAILS SAFE (reports "sub-agent, no terminal id") rather than emitting a wrong id, and the detection is a path-shape check (`subagents/` segment OR basename-not-a-UUID) that degrades gracefully — an unrecognized shape → "no terminal id" notice, never a false positive. ARGUS: attack the path-shape assumption + whether the glob `C--*claude-projects*` over-matches (it matches worktree-suffixed slugs like `…-the-stoa--claude-worktrees-…` — is that ever a false store for a seat?).

2. **WEAK — the registry write is a read-modify-rewrite of one JSONL attachment with no locking; two seats recording concurrently (the launcher mints both POLYBIUS and PLINY ~simultaneously) could race and lose a row.** *Why this shape anyway:* `bw attach` commits to the beadwork branch, so a concurrent write surfaces as a git conflict (loud, not silent) and the launcher records seats with a `-StaggerSeconds` gap already (4s default); the dogfood seed is 2 seats, low contention. But ARGUS should weigh whether the launcher should serialize the two record-seat calls explicitly (it can — they run in the parent PS1, not in the spawned sessions) vs. each spawned session self-recording (which WOULD race). **Design intent: the LAUNCHER records both seats serially from the parent process** (it knows both ids — it minted them), so no race; self-recording via whoami is the FALLBACK only for desktop sessions. ARGUS: confirm the launcher-records-serially path is the primary and is actually race-free.

3. **WEAK — sign-everywhere is convention, not enforcement (Q3 explicitly flagged this as fragile).** A seat can forge or omit a `[from:]` tag; §28.9 makes it canon but not structural. *Why this shape anyway:* the directive locks the WHAT to a convention (the rejected-overkill was per-agent GitHub accounts); the optional `prepare-commit-msg` backstop (§28.1) is the structural half for git trailers, and the registry gives an audit cross-check (a `[from:]` can be validated against `stoa--reg`). Full structural enforcement (a bw write-wrapper) is out of this arc's locked scope. ARGUS: is the forgeable-provenance property a named threat on the shared `cm-` commons that should escalate, or correctly accepted as convention?

---

## §5. Out of scope (deliberate; with one-line reasons)

- **Cross-machine `--resume` / cloud-sync** — not a thing (A1); continuity stays on bw+handoffs.
- **The builder-deploy cookie-cutter BUILD** — only the registry is designed to be ADOPTABLE by it (DC2); not built here.
- **Remote-Control unattended remote-approve gap** — permission-gated by Claude Code; noted, not solved (directive out-of-scope).
- **A structural bw write-wrapper for sign-everywhere enforcement** — Q3's "prefer structural" ideal; this arc lands the convention + the git-trailer backstop only; the wrapper is a follow-up.
- **The p7c commons-rollout (`cm-` update-path post)** — a SHIP-time item; surfaced to Polybius_the_Stoa, not designed into the build.
- **Full op-disc audit beyond §28** — flag drive-bys (see Follow-ups), don't expand.
- **The `decision-surface` skill SKILL_NAMES drift** (see Follow-ups) — a pre-existing inconsistency unrelated to identity; ticket, don't fix in this arc's diff.

---

## §6. Concrete edit plan (what ADA builds)

1. **`substrate/skills/team-launcher/launch-team.ps1`** — rewrite FROM the 200L deployed copy: keep `-ArcId`/`-OnlySeat` + their blocks; add (a) a `-RemoteControl` switch (optional), (b) per-seat `SessionId = [guid]::NewGuid()` minted in the seat-build, (c) `--session-id $($seat.SessionId)` appended in BOTH the wt panes/tabs arg array (after `--name`) AND the Windows per-seat `$cmd` string, (d) optional `--remote-control` token where `-RemoteControl`, (e) after the launch loop (non-dry-run), call `record-seat.ps1` serially for each seat with `{seat,name,session_id,project,machine,role,tier,launched_at,status:alive}`, (f) dry-run prints both the `wt`/`pwsh` line (with `--session-id`) AND a `[dry-run] record-seat: …` line but executes neither. Replace the L49-50 interim-name NOTE with a §28.9 + registry pointer.
2. **`substrate/skills/team-launcher/record-seat.ps1`** (new, beside the launcher) — the standalone read-modify-rewrite-attach helper (DC2 write recipe); params `-Seat -Name -SessionId -Project -Machine -Role -Tier`; idempotent on `(seat,machine)`.
3. **`substrate/skills/team-launcher/SKILL.md`** — document the new launch behavior (mint+name+record), the `-RemoteControl` switch, the registry read recipe, and update the cross-ref (drop "adopt the formal id later" → "id scheme landed; see §28.9 + stoa--reg").
4. **`substrate/skills/whoami/SKILL.md` + `whoami.py`** (new) — DC4; add `whoami` to `install.sh` `SKILL_NAMES`.
5. **`substrate/operating-disciplines.md`** — new §28.9 (DC3 sign-everywhere, all-seats/all-channels, terminal-vs-sub-agent table, Author-stays-PRINCIPAL restated, Q5 routing-address line).
6. **Role files** — §28.9 pointer in `MAJOR_POLYBIUS.md`, `MAJOR_PLINY.md`, and the CAPTAIN role files' existing §6.5 bw-comment discipline.
7. **`substrate/install.sh`** — `whoami` into `SKILL_NAMES`.
8. **Registry stand-up** — create bw ticket `stoa--reg`; seed `attachments/stoa--reg/seat-registry.jsonl` with this arc's own seats (dogfood: the floor-manager + PLINY rows, sids already known from this ticket's comments).

---

## §7. Residual questions for ARGUS

- **R1 (escalation candidate):** Is the forgeable-provenance property of sign-everywhere a NAMED threat on the shared `cm-` commons (multi-principal store) that should escalate, or correctly accepted as convention per the charter's locked WHAT? (See WEAK-3.) I classify it `not threat-ratified (process change)`; ARGUS confirms or escalates.
- **R2:** Is FOLD (DC1) the right call, or does the combined diff cross ARGUS's readability threshold (→ sequence stoa--fpj first)? My read: superset-merge, fold is clean. Needs ARGUS + floor-manager adjudication if disputed.
- **R3:** Does the launcher-records-serially-from-parent design (WEAK-2) actually eliminate the registry race, or does ARGUS want explicit serialization / a self-record-only model?

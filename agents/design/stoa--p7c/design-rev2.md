# Arc 67 design-rev2 — Session-identity deployment pattern (stoa--p7c)

**Author:** Denson Smith (synthesis, structural choices, hand-off contracts). Design seat: CAPTAIN_DAEDALUS_the-stoa.
**Charter:** `stoa--p7c` · **Directive:** `substrate/arcs/arc-67-build-directive.md` @ bd15fc3 · **Branch:** `arc-67/build`.
**Operating mode:** autonomous (surfaces at hand-back for go/no-go; no mid-design round-trip).
**Supersedes:** design-rev1 (committed 5d7c067) — see `## Δ from rev1` immediately below. rev1 is kept on the audit trail per the per-arc design-canon convention; rev2 is the build-against artifact.

---

## Δ from rev1 (exactly what changed; exactly what did NOT)

**CHANGED — the sub-agent-identity treatment ONLY (PRINCIPAL design input @ 21:30:03Z, floor-manager-confirmed @ 21:31:36Z on this arc's live seats):**

rev1 treated a sub-agent CAPTAIN as having **no discoverable id** — it signed with only its seat mnemonic, and `whoami` fail-safed to a "you are a sub-agent, no terminal session-id" exit-2 notice. The PRINCIPAL input replaces fail-safe-to-no-id with **traceable caller-sid chaining**: a sub-agent does NOT need its own terminal session-id; it instead reports (a) WHAT it is (subagent TYPE/mnemonic + its `agent-id`) and (b) the session-id of the AGENT THAT CALLED IT (the **caller-sid** = parent terminal session-id). The sub-agent transcript path `<caller-sid>/subagents/agent-<id>.jsonl` ENCODES BOTH, so the same nonce-grep self-discovers both pieces; combined with the type the sub-agent already knows, that is the full signature. This is strictly better than fail-safe-to-no-id (provenance now chains to a revivable parent terminal session) and uses **no new mechanism** — same nonce-grep, different path-parse.

Concretely the three loci that move:
- **DC4 `whoami.py` sub-agent branch** — was an exit-2 fail-safe notice; is now a **SUCCESS path** that parses the path and emits a structured `{caller_sid, agent_id, kind:"subagent"}` identity (§ DC4 below + P5).
- **DC3 §28.9 sub-agent table row** — was "no sid"; now carries `agent-id` + `caller-sid`, and the sub-agent sign format becomes `[from: CAPTAIN_<MNEMONIC>_<slug> (subagent) | agent-id <id> | caller-sid <parent-sid>]` (§ DC3 below).
- **P5 probe** — was "asserts whoami returns the sub-agent notice + exit-2"; now asserts whoami's sub-agent branch returns the structured `caller-sid + agent-id` identity (§3 below).
- **A4** (the imported empirical) is re-framed from "sub-agents have no terminal id → fail safe" to "the path encodes caller-sid + agent-id → self-discoverable provenance" (§1 below).
- **§6 edit-plan bullets** for `whoami.py` + the §28.9 row updated to the new treatment.

**Dogfooded live this design pass:** I am an ephemeral sub-agent. My own nonce landed at `…/C--Users-denso-claude-projects-the-stoa/a3e23bca-779d-4ffc-b720-58262af14cdb/subagents/agent-ade09f63b0810d686.jsonl` — dir = `a3e23bca-779d-4ffc-b720-58262af14cdb` (PLINY's terminal sid = my caller-sid), file = `agent-ade09f63b0810d686` (my agent-id). I signed this pass's bw comments with the new format, proving the scheme by living it.

**NOT changed (carried forward verbatim from rev1; not re-opened):**
- **DC1 FOLD** (rewrite from the 200L deployed copy; superset-merge; no sequencing).
- **DC2 registry** (dedicated bw ticket `stoa--reg` + JSONL manifest on beadwork via standalone `record-seat.ps1`; REAL-execution-testable without live spawn; idempotent on `(seat,machine)`).
- **DC3 terminal-seat** sign format + the §28.9-as-new-sibling-subsection decision + the `Author:`=PRINCIPAL-preserved absolute.
- **DC4 terminal-seat** whoami path (top-level `<slug>/<uuid>.jsonl` → bare id) + the conservative subsequent-turn flush + retry model.
- **§5 out-of-scope**, the probes P1–P4 + P6–P9, and **§7 residuals R1/R2/R3**.
- **R1 STAYS DISTINCT AND UNRESOLVED.** The caller-sid amendment resolves DC3/DC4 sub-agent-identity ONLY. A self-reported caller-sid is still **convention, not enforcement** — a buggy or hostile agent could mis-state it. R1 (forgeable provenance on the multi-principal `cm-` commons) remains ARGUS's convention-vs-enforcement call, exactly as rev1 framed it. This rev2 does **not** try to solve forgeable-provenance.

---

## §1. Problem restatement

Make Stoa agent **identity** first-class and durable so a message on the shared `cm-` commons (or any bw store) carries a structural, machine-resolvable signal of *which seat / role / project / machine* authored it. Four PRINCIPAL-locked requirements (the WHAT is locked; this doc designs the HOW):

1. **LAUNCH** — `launch-team.ps1` ALWAYS mints a per-seat UUID, assigns a space-free human-friendly name, launches `claude` with `--session-id <uuid>` + `--name <name>` (+ optional `--remote-control`), and RECORDS `seat→{session-id, name, project, machine}` durably to a portable bw registry.
2. **WHOAMI** — a new python skill any seat runs to discover its own identity (nonce-grep): a terminal seat discovers its session-id; a sub-agent discovers its caller-sid + agent-id. For desktop-UI-created sessions that could not pin `--session-id` at creation.
3. **SIGN-EVERYWHERE** — broaden op-disc §28 so every seat carries its identity in ALL channels (bw comments, git trailers, recordkeeping), preserving the §28 absolute: git `Author:` stays the PRINCIPAL's identity.
4. **REGISTRY** — `seat→{id,name,project,machine}` lives in **bw** (git-synced, portable; session-ids are per-machine so the roster must survive cross-machine).

**Imported assumptions (named, not smoothed):**
- *A1 — session-ids are same-machine handles only.* No cross-machine `--resume`/cloud-sync; the registry records ids for liveness/audit on the minting machine, NOT for cross-machine session resumption. Continuity stays on bw + handoffs. (Directive Settled facts.)
- *A2 — DC1 folds stoa--fpj.* The substrate launcher (171L) lacks `-ArcId`/`-OnlySeat` the deployed copy (200L) has; a blind `install.sh` of the 171L source would REGRESS deployed consumers. Resolving the SSoT inversion is in-scope regardless of fold-vs-sequence.
- *A3 — the origindex builder-publish security model is ORTHOGONAL* (network-access identity: Tailscale/SSO; defines no seat registry). Do not force-converge. The convergence target is the FUTURE builder-deploy launcher, which adopts THIS registry.
- *A4 (design-time empirical, load-bearing — see DC3/DC4):* a **sub-agent**'s transcript is NOT `<slug>/<uuid>.jsonl`; it is `<slug>/<caller-sid>/subagents/agent-<id>.jsonl`. The path **encodes the sub-agent's full provenance**: the dir component is the **caller-sid** (the parent terminal session that dispatched it — a real, revivable session), and the file basename is `agent-<id>` (the sub-agent's `agent-id`). So a sub-agent CAPTAIN does not need (and cannot have) its own terminal session-id; instead it self-discovers `caller-sid + agent-id` from the same nonce-grep and signs with both. Verified live this design pass: my own nonce landed in `…/a3e23bca-779d-4ffc-b720-58262af14cdb/subagents/agent-ade09f63b0810d686.jsonl` — caller-sid `a3e23bca…` (PLINY's terminal session), agent-id `ade09f63b0810d686`.

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

The registry rows are for **terminal seats** (they have a `session_id`); ephemeral sub-agents are not registry rows — their provenance is signed inline (caller-sid + agent-id) and is anchored to their parent's registry row via the caller-sid, so the roster stays small and live-seat-shaped. (This is unchanged from rev1's intent and is reinforced by the caller-sid amendment: a sub-agent's caller-sid IS a terminal seat that the registry already tracks.)

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

**Decision.** Add a new subsection **§28.9 "Session-identity sign-everywhere (all seats, all channels)"** rather than rewriting §28.1–§28.8 (which are git-trailer-specific and empirically anchored; rewriting them risks losing the squash-merge anchors). §28.9 broadens scope to: ALL seats, ALL channels, carrying **identity** (terminal seats: session-id + name; sub-agents: agent-id + caller-sid) — not just the seat mnemonic. The §28 absolute is restated verbatim and PRESERVED: git `Author:` stays PRINCIPAL; identity layers ON TOP, never in place of.

**The terminal-vs-sub-agent signing distinction (the real gap, A4 — AMENDED for caller-sid chaining):**

| Seat class | Has own terminal session-id? | Self-discovered identity | bw-comment sign format | git trailer |
|---|---|---|---|---|
| **Terminal seat** (top-level session: POLYBIUS/PLINY, any `--session-id`-launched or whoami-discoverable seat) | YES | `session_id` = basename of `<slug>/<uuid>.jsonl` | `[from: <Name> \| sid <session-id> \| <project>]` | existing §28.1 `Co-Authored-By` + optional `Stoa-Session-Id: <sid>` trailer |
| **Ephemeral sub-agent CAPTAIN** (Agent-tool dispatch: ADA/VERA/CATO/ARGUS/DAEDALUS/…) | NO (by construction) | `caller-sid` = dir component AND `agent-id` = basename of `<slug>/<caller-sid>/subagents/agent-<id>.jsonl` | `[from: CAPTAIN_<MNEMONIC>_<slug> (subagent) \| agent-id <id> \| caller-sid <parent-sid>]` | existing §28.1 `Co-Authored-By: CAPTAIN_<MNEMONIC>_<slug>` (unchanged) |

This is dogfooded by THIS design pass: I am an ephemeral sub-agent, so I sign `[from: CAPTAIN_DAEDALUS_the-stoa (subagent) | agent-id ade09f63b0810d686 | caller-sid a3e23bca-779d-4ffc-b720-58262af14cdb]` — exactly the sub-agent row. My caller-sid `a3e23bca…` IS PLINY's terminal session (the seat that dispatched me), which the registry tracks as a terminal row — so my provenance chains to a revivable parent. Terminal seats (the floor-manager, PLINY) sign with sid, as they already did on this charter ticket.

**caller-sid: self-discovery PRIMARY, brief-passed cross-check OPTIONAL (the HOW decision).**
The sub-agent's caller-sid is obtained by **self-discovery as the primary, authoritative source** (parse the nonce-grep match path's dir component). The dispatch brief MAY *also* pass the caller-sid as a stated cross-check, but self-discovery is canonical when the two are present. **Rationale:** self-discovery is robust to brief-omission (a sub-agent dispatched without a caller-sid in its brief STILL self-signs correctly — the path always encodes it), whereas a brief-passed value is only as good as the dispatcher remembering to include it and getting it right. The brief-passed value, when present, is a useful belt-and-suspenders cross-check: if self-discovered caller-sid ≠ brief-stated caller-sid, that is a signal worth surfacing (e.g. a mis-dispatched or re-parented agent). So: **self-discovery primary; brief-passed optional cross-check; mismatch is a surface-able anomaly, not a hard error** (whoami prints both and flags the divergence rather than failing, because the path is ground truth and the brief is the weaker source). This keeps the scheme working even where MAJOR_PLINY's dispatch brief omits the caller-sid entirely — the common case for ad-hoc dispatches.

**Concrete formats + placement per channel (§28.9 body):**
- **bw comments** — first line of every comment is the sign-tag above (terminal or sub-agent form). (Already in live practice on this ticket; §28.9 makes it canon.)
- **git trailers** — unchanged from §28.1 for CAPTAINs; terminal seats committing directly (POLYBIUS housekeeping) MAY add `Stoa-Session-Id: <sid>` as a second trailer (the floor-manager already did this on bd15fc3's parent — `Stoa-Session-Id: 990b0750-…`). Author stays PRINCIPAL. (Sub-agent CAPTAINs commit via the existing §28.1 `Co-Authored-By` trailer; agent-id/caller-sid are a bw-comment-channel signal, not a git trailer — git commits already chain to the worktree/branch, and adding agent-id to every trailer is noise the §28.1 anchors don't need.)
- **recordkeeping** — the registry row (DC2) is the durable record for terminal seats; sub-agent provenance is the inline sign-tag, anchored to its caller's registry row via caller-sid.

**Q5 (id+name as the canonical `[for:]` routing address):** the `seat` field (`ROLE_slug`) is the routing address; `[for: POLYBIUS_the-stoa]` resolves against the registry's `seat` column. §28.9 states this so the convention is the address. A sub-agent is addressed by its `seat` mnemonic the same way; its agent-id/caller-sid are provenance, not a routing key (sub-agents are ephemeral — you address the seat, not the instance).

**Role-file references (per-seat application of §28.9):** add a one-line pointer in each MAJOR_*.md and CAPTAIN_*.md comms/discipline section: *"Sign every bw comment + commit per op-disc §28.9 (terminal seats: `[from: Name | sid <id> | project]`; sub-agent CAPTAINs: `[from: CAPTAIN_<MNEMONIC>_<slug> (subagent) | agent-id <id> | caller-sid <parent-sid>]`)."* Concretely: `MAJOR_POLYBIUS.md`, `MAJOR_PLINY.md` (terminal class), and the CAPTAIN role files' existing §6.5 heartbeat/bw-comment disciplines (sub-agent class) get the pointer. This is a *pointer*, not a re-statement, to keep §28.9 the SSoT.

### DC4 — whoami skill: python, conservative subsequent-turn flush; terminal seats → session-id, sub-agents → caller-sid + agent-id (RESOLUTION, AMENDED)

**Decision.** A python skill `substrate/skills/whoami/` (SKILL.md + `whoami.py`) implementing the nonce-grep recipe with the **conservative model: emit nonce on one turn, grep on a subsequent invocation** — with a built-in flush-retry loop so a single skill run can still succeed if the nonce has flushed. Verified live this pass: my same-turn grep found NOTHING; the subsequent bash call found it. The conservative model is correct; the retry loop makes it robust without forcing a two-turn UX.

**The load-bearing refinement (A4, AMENDED — the sub-agent branch is now a SUCCESS path):** the recipe "session id = filename minus `.jsonl`" is ONLY valid for a **top-level terminal session** transcript (`<slug>/<uuid>.jsonl`). A sub-agent's nonce lands in `<slug>/<caller-sid>/subagents/agent-<id>.jsonl`, whose path ENCODES the sub-agent's full provenance. So whoami MUST:
1. Emit a unique nonce: `SELFID-<uuid4>` (uuid4 handles concurrent same-dir sessions — no collision).
2. Grep the store for the nonce across `~/.claude/projects/C--Users-denso-claude-projects*/` (the `*` glob covers the user-tier slug + every per-project slug).
3. **Classify the match by path shape:**
   - **Top-level terminal match** — `<store>/<slug>/<uuid>.jsonl` (parent dir is a project-slug dir, basename is a UUID, NOT under a `subagents/` segment) → emit a `terminal` identity: `{kind:"terminal", session_id:"<uuid>"}`. Print the bare `<uuid>` to stdout; exit 0.
   - **Sub-agent match** — `<store>/<slug>/<caller-sid>/subagents/agent-<id>.jsonl` (a `subagents/` segment is present; basename is `agent-<id>`) → **parse the path** and emit a `subagent` identity: `{kind:"subagent", caller_sid:"<caller-sid>", agent_id:"<id>"}`, where `caller_sid` is the directory component immediately under `<slug>` (the parent terminal session-id) and `agent_id` is the basename with the `agent-` prefix and `.jsonl` suffix stripped. Print a structured line to stdout (e.g. `subagent caller-sid=<caller-sid> agent-id=<id>`, or `--json` for the object); **exit 0 — this is a SUCCESS path, not a fail-safe.** The caller's sign-tag is then `[from: <SEAT> (subagent) | agent-id <id> | caller-sid <caller-sid>]` (the seat mnemonic is known to the caller; whoami supplies the two path-derived fields).
4. **Optional brief-passed caller-sid cross-check:** if invoked with `--expect-caller-sid <sid>`, compare the self-discovered `caller_sid` against it; on mismatch, print BOTH and a `caller-sid-divergence` warning to stderr but still exit 0 with the self-discovered (ground-truth) value (per the DC3 self-discovery-primary decision).
5. **If no match yet** → flush-retry: sleep + re-grep up to N times; if still nothing, exit 3 with the re-run instruction (the conservative subsequent-turn fallback).

**Output contract:**
- Terminal success → bare session-id (uuid) on stdout, exit 0. (`--verbose` also prints the matched store path; `--json` prints `{"kind":"terminal","session_id":"…"}`.)
- Sub-agent success → `subagent caller-sid=<caller-sid> agent-id=<id>` on stdout, exit 0. (`--json` prints `{"kind":"subagent","caller_sid":"…","agent_id":"…"}`.)
- Not-yet-flushed → exit 3 with the re-run instruction on stderr.
- A caller branches on `kind` (or on exit-3) to decide its sign-tag form. The bare-id stdout (terminal case) is what a terminal seat captures to self-record into the registry (DC2 write recipe); the sub-agent case does NOT write a registry row (it signs inline).

**Why the sub-agent branch is exit-0 (not the rev1 exit-2):** rev1's exit-2 encoded "this is a degenerate/failure case — no id available." The amendment establishes that a sub-agent's identity is fully available (caller-sid + agent-id from the path), so the sub-agent case is a normal, successful discovery with a *different identity shape* than a terminal seat — not an error. Reserving a non-zero exit for the genuine failure (no match → exit 3) keeps the exit-code semantics clean: 0 = identity discovered (of either kind), 3 = not-yet-flushed, retry.

**Store-root portability:** the skill resolves the store root from `$HOME/.claude/projects` (not the hard-coded `C:\Users\denso\…`), so it works for any PRINCIPAL; the slug glob is `C--*claude-projects*` derived from `$HOME` → portable.

---

## A3 threat→mitigation map

Per op-disc §35.1 + DAEDALUS §6.12: this arc is a **process / role-file / tooling hardening** change. It adds an identity/provenance CONVENTION; it introduces **no runtime attack surface** (no new network endpoint, no credential flow, no privilege boundary). The caller-sid amendment does not change this classification — caller-sid chaining is provenance metadata derived from a local filesystem path, not an access control. Classification:

> **not threat-ratified (process + tooling change; no runtime attack path).** The sign-everywhere convention (including caller-sid chaining) is provenance metadata, not an authentication or authorization control — it is forgeable by design (an agent could write a false `[from:]`, including a false caller-sid), exactly as the charter's "convention vs enforcement" Q3 notes. No named threat is *defeated* by a mechanism here; the registry/sign-everywhere improve *auditability*, they do not gate access. The Remote-Control remote-approve gap is explicitly noted-not-solved (out of scope). ARGUS confirms this classification (§35.5 self-carve-out: I propose, ARGUS confirms; I cannot grant my own carve-out).

No `M<n>` rows; no threat-anchored probe required (§6.13 self-carve-out applies). If ARGUS judges any element security-relevant (e.g. the forgeable-provenance property — now including a forgeable caller-sid — rising to a named threat on the shared `cm-` commons), that is residual **R1** below. The amendment does NOT close R1; a self-reported caller-sid is convention, not enforcement.

---

## §3. Verification probes (VERA executes; labelled P1..P9)

**P1 — launcher dry-run command shape (the ONLY thing dry-run can prove).**
`pwsh -File substrate/skills/team-launcher/launch-team.ps1 -DryRun -ArcId arc-67 -Slug the-stoa` → printed `wt`/`pwsh` command for EACH seat contains `--session-id <uuid>` (a real GUID shape) AND `--name <space-free-name>`. Assert: grep the dry-run stdout for `--session-id` followed by a `[0-9a-f-]{36}` token, and `--name` followed by a token containing no spaces. Two seats → two `--session-id` occurrences.

**P2 — dry-run prints the record step but does NOT execute it.**
Same dry-run run: stdout names the `record-seat.ps1` invocation (a `[dry-run]` line), AND `git show beadwork:attachments/stoa--reg/seat-registry.jsonl` is UNCHANGED by the dry-run (no synthetic row written). Confirms the DoD constraint that dry-run early-returns before any real write.

**P3 — registry write, REAL execution (no live spawn).**
Call `record-seat.ps1` directly with a synthetic row: `pwsh -File .../record-seat.ps1 -Seat TESTSEAT_probe -Name Test_Probe -SessionId 00000000-0000-0000-0000-000000000000 -Project the-stoa -Machine $(hostname) -Role probe -Tier test`. Then `git show beadwork:attachments/stoa--reg/seat-registry.jsonl | jq -c 'select(.seat=="TESTSEAT_probe")'` returns the row with all fields. Then re-run with a different `SessionId` for the SAME `(seat,machine)` → assert the manifest has exactly ONE `TESTSEAT_probe` row (idempotent replace, not append). **Cleanup:** remove the synthetic row + re-attach (fixed literal path `attachments/stoa--reg/seat-registry.jsonl`, no `$VAR` in the destructive step). This is the REAL mint+record round-trip without spawning an agent.

**P4 — whoami REAL round-trip (terminal seat).**
The running VERA/dogfood terminal session runs the whoami skill; assert it returns a 36-char UUID that matches an actual `<slug>/<uuid>.jsonl` file on disk (`test -f "$HOME/.claude/projects/<slug>/<returned-id>.jsonl"`) and exits 0 with `kind=terminal`. For the subsequent-turn flush case, the retry loop must succeed within N retries or the probe re-runs on the next turn (documented as a two-call probe).

**P5 — whoami sub-agent branch returns the structured caller-sid + agent-id identity (AMENDED).**
Run whoami from inside an Agent-tool sub-agent (or simulate by greping a nonce known to be in a `<slug>/<caller-sid>/subagents/agent-<id>.jsonl` path). Assert ALL of:
  (a) **exit code 0** (success path — NOT the rev1 exit-2 fail-safe);
  (b) `kind == "subagent"`;
  (c) `caller_sid` equals the directory component under `<slug>` (a real UUID-shaped parent session-id), and it matches a top-level `<slug>/<caller_sid>.jsonl` file on disk (proving the caller-sid chains to a revivable terminal session);
  (d) `agent_id` equals the basename with `agent-` prefix and `.jsonl` suffix stripped;
  (e) the emitted sign-tag matches `[from: <SEAT> (subagent) | agent-id <id> | caller-sid <caller-sid>]`.
**Dogfood reference value (this design pass, live):** whoami from THIS DAEDALUS sub-agent returns `caller_sid=a3e23bca-779d-4ffc-b720-58262af14cdb`, `agent_id=ade09f63b0810d686`, and `a3e23bca-779d-4ffc-b720-58262af14cdb.jsonl` exists top-level in the the-stoa store (PLINY's revivable terminal session). VERA re-executes the same recipe and asserts the structured success, NOT a sub-agent notice. (Guards against an A4 regression AND against any reversion to the rev1 fail-safe.)
**Optional cross-check sub-probe (P5b):** invoke whoami with `--expect-caller-sid <wrong-uuid>` from the same sub-agent; assert it still exits 0 with the self-discovered (correct) `caller_sid` and emits a `caller-sid-divergence` warning to stderr (proving self-discovery is primary and the brief-passed value is a non-fatal cross-check).

**P6 — §28.9 broadening + Author-stays-PRINCIPAL absolute preserved.**
`grep -n "session-id" substrate/operating-disciplines.md` shows §28.9 exists; grep confirms §28.9 contains both the terminal-seat format `[from:` … `sid` AND the sub-agent format `[from: CAPTAIN_` … `(subagent)` … `agent-id` … `caller-sid`; AND §28.9 restates "Author: stays PRINCIPAL". Role files (`MAJOR_POLYBIUS.md`, `MAJOR_PLINY.md`, the CAPTAIN role files' §6.5) each contain a §28.9 pointer carrying the amended sub-agent format.

**P7 — no cross-machine-resume promise (grep clean-check).**
`grep -rni "resume" substrate/skills/whoami/ substrate/skills/team-launcher/` and the §28.9 text → every "resume" hit (if any) is same-machine-correct usage; NO text promises cross-machine session resume. Expected: zero cross-machine-resume claims.

**P8 — substrate session-id reference clean-check.**
`grep -rn "session-id\|--session-id\|whoami\|caller-sid" substrate/` returns ONLY intended references (the launcher, whoami skill, §28.9, team-launcher SKILL.md, role-file pointers) — no stray/dangling refs.

**P9 — install.sh deploys whoami; launcher interim-note resolved.**
`whoami` is in `SKILL_NAMES` in `substrate/install.sh` (grep). The launcher's old L49-50 interim-seat-name note (`adopt the formal Role_Project_Instance id when stoa--p7c lands`) is RESOLVED — replaced with a pointer to §28.9 + the registry (grep confirms the "interim … when stoa--p7c lands" phrasing is gone). `install.sh --dry-run` (subproject + project tier) still passes its A–E recompose checks (full-suite, not just "this arc touched no X").

**Full-suite belt-and-suspenders:** VERA runs the project's existing install.sh smoke test + `npm run gen-data` (the launcher/skill changes are gen-data-adjacent only via skill rendering; gen-data re-derives the whole roster and surfaces any pre-existing drift — assert from a FULL suite run, not "this arc edited no agent frontmatter").

---

## §4. Self-assessed weak points (what I'd want ARGUS to attack hardest)

1. **WEAK — sub-agent whoami detection AND the caller-sid path-parse rest on the `<slug>/<caller-sid>/subagents/agent-<id>.jsonl` convention (A4), a Claude Code internal verified live on this machine/version (2.1.170).** If Claude Code changes the sub-agent transcript layout, the path-parse breaks and whoami could mis-derive caller-sid or agent-id. *Why this shape anyway:* the parse is keyed on the explicit `subagents/` path segment + the `agent-` basename prefix, both of which are stable structural markers (not positional guesses); if the shape is unrecognized, whoami falls through to the no-match/exit-3 path rather than emitting a wrong identity. **NEW RISK the amendment introduces:** rev1 fail-safed to "no id" (a SAFE wrong answer — under-claims); rev2 now EMITS a caller-sid + agent-id, so a layout change that still *looks* like a subagent path but encodes a different dir semantics could emit a *confidently wrong* caller-sid (a chain to the wrong "parent"). Mitigation in-design: P5(c) asserts the derived caller-sid matches an actual top-level `<slug>/<caller-sid>.jsonl` on disk — so a derived caller-sid that does NOT correspond to a real terminal session is caught at verify time, and whoami SHOULD apply the same on-disk existence check at runtime (emit the caller-sid only if `<slug>/<caller-sid>.jsonl` exists; else degrade to seat-mnemonic-only + a warning). ARGUS: weigh whether whoami MUST do the runtime existence check (I recommend yes — it converts a confidently-wrong caller-sid back into a safe degrade) and whether the `C--*claude-projects*` glob over-matches worktree-suffixed slugs.

2. **WEAK — the registry write is a read-modify-rewrite of one JSONL attachment with no locking; two seats recording concurrently (the launcher mints both POLYBIUS and PLINY ~simultaneously) could race and lose a row.** *Why this shape anyway:* `bw attach` commits to the beadwork branch, so a concurrent write surfaces as a git conflict (loud, not silent) and the launcher records seats with a `-StaggerSeconds` gap already (4s default); the dogfood seed is 2 seats, low contention. **Design intent: the LAUNCHER records both seats serially from the parent process** (it knows both ids — it minted them), so no race; self-recording via whoami is the FALLBACK only for desktop sessions. The caller-sid amendment REDUCES this surface slightly: sub-agents no longer self-record at all (they sign inline, no registry row), so the only registry writers are terminal seats. ARGUS: confirm the launcher-records-serially path is the primary and is actually race-free.

3. **WEAK — sign-everywhere is convention, not enforcement (Q3 explicitly flagged this as fragile), and the caller-sid is ITSELF self-reported convention.** A seat can forge or omit a `[from:]` tag, including a false caller-sid; §28.9 makes it canon but not structural. *Why this shape anyway:* the directive locks the WHAT to a convention (the rejected-overkill was per-agent GitHub accounts); the optional `prepare-commit-msg` backstop (§28.1) is the structural half for git trailers, and the registry gives an audit cross-check (a `[from:]`'s caller-sid can be validated against `stoa--reg` + the on-disk transcript). Full structural enforcement (a bw write-wrapper) is out of this arc's locked scope. **This is the R1 surface and the amendment does NOT change it** — caller-sid chaining improves *traceability when honestly reported* but adds no enforcement; a hostile agent can still mis-state its caller-sid. ARGUS: is the forgeable-provenance property (now including forgeable caller-sid) a named threat on the shared `cm-` commons that should escalate, or correctly accepted as convention? (This is R1 — kept distinct, unresolved.)

---

## §5. Out of scope (deliberate; with one-line reasons)

- **Cross-machine `--resume` / cloud-sync** — not a thing (A1); continuity stays on bw+handoffs.
- **The builder-deploy cookie-cutter BUILD** — only the registry is designed to be ADOPTABLE by it (DC2); not built here.
- **Remote-Control unattended remote-approve gap** — permission-gated by Claude Code; noted, not solved (directive out-of-scope).
- **A structural bw write-wrapper for sign-everywhere enforcement** — Q3's "prefer structural" ideal; this arc lands the convention + the git-trailer backstop only; the wrapper is a follow-up. **(This is the structural answer to R1 — explicitly out of scope; caller-sid chaining does NOT substitute for it.)**
- **The p7c commons-rollout (`cm-` update-path post)** — a SHIP-time item; surfaced to Polybius_the_Stoa, not designed into the build.
- **Full op-disc audit beyond §28** — flag drive-bys (see Follow-ups), don't expand.
- **The `decision-surface` skill SKILL_NAMES drift** (see Follow-ups) — a pre-existing inconsistency unrelated to identity; ticket, don't fix in this arc's diff.

---

## §6. Concrete edit plan (what ADA builds)

1. **`substrate/skills/team-launcher/launch-team.ps1`** — rewrite FROM the 200L deployed copy: keep `-ArcId`/`-OnlySeat` + their blocks; add (a) a `-RemoteControl` switch (optional), (b) per-seat `SessionId = [guid]::NewGuid()` minted in the seat-build, (c) `--session-id $($seat.SessionId)` appended in BOTH the wt panes/tabs arg array (after `--name`) AND the Windows per-seat `$cmd` string, (d) optional `--remote-control` token where `-RemoteControl`, (e) after the launch loop (non-dry-run), call `record-seat.ps1` serially for each seat with `{seat,name,session_id,project,machine,role,tier,launched_at,status:alive}`, (f) dry-run prints both the `wt`/`pwsh` line (with `--session-id`) AND a `[dry-run] record-seat: …` line but executes neither. Replace the L49-50 interim-name NOTE with a §28.9 + registry pointer.
2. **`substrate/skills/team-launcher/record-seat.ps1`** (new, beside the launcher) — the standalone read-modify-rewrite-attach helper (DC2 write recipe); params `-Seat -Name -SessionId -Project -Machine -Role -Tier`; idempotent on `(seat,machine)`.
3. **`substrate/skills/team-launcher/SKILL.md`** — document the new launch behavior (mint+name+record), the `-RemoteControl` switch, the registry read recipe, and update the cross-ref (drop "adopt the formal id later" → "id scheme landed; see §28.9 + stoa--reg").
4. **`substrate/skills/whoami/SKILL.md` + `whoami.py`** (new) — DC4; implement BOTH branches: terminal match → bare session-id (exit 0); sub-agent match → **parse `<slug>/<caller-sid>/subagents/agent-<id>.jsonl` → structured `{kind:"subagent", caller_sid, agent_id}` (exit 0, SUCCESS path, NOT the rev1 exit-2 fail-safe)**, with the optional `--expect-caller-sid` cross-check and the recommended runtime on-disk caller-sid existence check (WEAK-1); no-match → exit 3 retry. Document the sub-agent sign-tag `[from: <SEAT> (subagent) | agent-id <id> | caller-sid <caller-sid>]`. Add `whoami` to `install.sh` `SKILL_NAMES`.
5. **`substrate/operating-disciplines.md`** — new §28.9 (DC3 sign-everywhere, all-seats/all-channels, the **amended** terminal-vs-sub-agent table where the sub-agent row carries `agent-id` + `caller-sid` and the sub-agent sign format is `[from: CAPTAIN_<MNEMONIC>_<slug> (subagent) | agent-id <id> | caller-sid <parent-sid>]`, the self-discovery-primary/brief-cross-check note, Author-stays-PRINCIPAL restated, Q5 routing-address line).
6. **Role files** — §28.9 pointer in `MAJOR_POLYBIUS.md`, `MAJOR_PLINY.md`, and the CAPTAIN role files' existing §6.5 bw-comment discipline (the pointer carries the **amended** sub-agent format).
7. **`substrate/install.sh`** — `whoami` into `SKILL_NAMES`.
8. **Registry stand-up** — create bw ticket `stoa--reg`; seed `attachments/stoa--reg/seat-registry.jsonl` with this arc's own TERMINAL seats (dogfood: the floor-manager + PLINY rows, sids already known from this ticket's comments). Sub-agents are NOT seeded (they sign inline; their caller-sid anchors to a seeded terminal row).

---

## §7. Residual questions for ARGUS

- **R1 (escalation candidate — UNCHANGED by the amendment, kept distinct):** Is the forgeable-provenance property of sign-everywhere a NAMED threat on the shared `cm-` commons (multi-principal store) that should escalate, or correctly accepted as convention per the charter's locked WHAT? (See WEAK-3.) **The caller-sid amendment does NOT resolve this** — a self-reported caller-sid is still convention, not enforcement; a buggy/hostile agent could mis-state it. I classify it `not threat-ratified (process change)`; ARGUS confirms or escalates. This stays exactly as rev1 framed it; rev2 deliberately did not touch it.
- **R2:** Is FOLD (DC1) the right call, or does the combined diff cross ARGUS's readability threshold (→ sequence stoa--fpj first)? My read: superset-merge, fold is clean. Needs ARGUS + floor-manager adjudication if disputed.
- **R3:** Does the launcher-records-serially-from-parent design (WEAK-2) actually eliminate the registry race, or does ARGUS want explicit serialization / a self-record-only model? (Note: the amendment shrank this surface — sub-agents no longer self-record.)

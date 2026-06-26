# design-rev2 — on-demand radio-check seat-liveness (stoa--fii)

- **Arc:** stoa--fii — `stoa--fii/radio-check-liveness`
- **Architect:** CAPTAIN_DAEDALUS_the_stoa (subagent) | caller-sid 62a49ed0-cf37-4b6a-896d-3cebda142d5c
- **Author (of this artifact + everything it specifies):** Denson Smith
- **Consumers:** ARGUS (critique) → ADA (build) → VERA (probe execution) → CATO (diff review) → NOMOS (close-gate)
- **Supersedes:** design-rev1.md. This is the canonical artifact downstream ADA/VERA/CATO/NOMOS cite. rev1 was NEEDS-REVISION (ARGUS, 2026-06-26T16:34:56Z) — design sound + human-simple, three targeted fixes folded below.

---

## Changes from rev1 (diff intent for CATO / NOMOS)

Three fixes from the ARGUS verdict (`verdicts/stoa--fii/argus-20260626T163456Z.md`), folded into the rev1 design with NO redesign. The shape, the helper-vs-protocol call, the §35 threat structure, and the scope fences are all unchanged from rev1.

- **r2 (most important — honest-claim discipline).** M1 in rev1 overclaimed past stoa--reg's already-ratified forgeable-provenance boundary ("audit-only ... forgeable metadata, not an authentication or authorization control"). bw stores a comment as `{text, timestamp}` only; the `[from:|sid]` is self-declared forgeable body text, and the registry `session_id` is world-readable JSONL. So a sid-match catches a STALE / TYPO / WRONG sid, but does NOT defeat a deliberate impersonator who copies the registry sid. **Re-scoped M1 throughout** — the §2.6 M1 row, the §2.3 step-4 / §2.4 sid-match prose, and P2's framing — to **"audit-only sid-match: catches accidental stale/typo/wrong-sid false-alive, NOT a deliberate impersonator,"** explicitly mirroring stoa--reg's ratified forgeable-provenance boundary. No authentication is claimed. P2 still asserts the stale/wrong-sid mismatch is flagged-not-tallied; it no longer implies impersonation is defeated, and now explicitly notes a COPIED registry sid is NOT blockable.
- **r1 (load-bearing). jq is NOT installed on this machine** (verified absent in both bash and PowerShell — `jq: command not found`, exit 127). The rev1 resolve-step (L47) and probes P1/P4 invoked jq, so they were non-runnable as written. **Made the resolve-step and P1/P4 jq-free as the primary/canonical path** — `grep` / `Select-String` / `git grep` against the JSONL (one row per line, plain-text greppable; verified live against the real registry). jq is mentioned only as an OPTIONAL convenience if present; the canonical human-simple path never REQUIRES it. (The pre-existing stoa--reg read-recipe also assumes jq — substrate-wide, out of THIS arc's scope; the new protocol text stands on its own without jq.)
- **r3 (precision). op-disc §7 is RELOCATED to a module** (`.claude/modules/two-polybius-coordination.md`; only stub anchors remain in core op-disc). **Repointed the cross-ref to the right homes** (core §7 stub + the §7.1 module body + a back-pointer from §38) and made it explicitly DISAMBIGUATE the shared `[radio-check]` token: §7/module = the PERIODIC two-POLYBIUS handshake (`[radio-check <self-seat-slug>]`); §38 = the ON-DEMAND seat-liveness ping (`[radio-check] [for: <seat>]`). Confirmed §37 is still the highest § (so §38 is the correct next integer) and confirmed the JSONL field is `session_id` (greppable), addressed colloquially as "sid" in tags.

---

## 1. Problem restatement

`stoa--reg` already answers **WHO is on the roster** — one durable JSONL row per terminal seat (`{seat, name, session_id, project, machine, role, tier, ..., launched_at, status}`). It does **not** reliably answer **"is this seat alive RIGHT NOW?"** The `status` field is a launch-time / stand-down-time stamp, not a live-presence signal: a seat whose Claude session crashed, hung, or was closed still shows `status:alive` until something rewrites the row.

This arc adds the missing **WHETHER-alive-now** answer as an **on-demand radio-check PING over beadwork** — a coordinator (typically user-tier POLYBIUS, or any seat that needs to know) posts a `[radio-check]` ping addressed to the seats it cares about; live seats answer within a reasonable window; non-answerers are tallied **PRESUMED dead**. Recovery of a presumed-dead seat is **relaunch of a REPLACEMENT** via `team-launcher` — never resurrection of the dead session.

**Imported assumptions (named, not smoothed):**
- **A. The ping is purely on-demand.** There is NO periodic sweep, NO `last_seen`, NO TTL, NO continuous monitor, and NO passive liveness field on the `stoa--reg` row. The directive (Polybius the Grand, 2026-06-26T15:41) scrapped all passive machinery; NOMOS confirmed CONFORMANT x2. Liveness is *answered by the live ping, never stored.* This is the load-bearing scope boundary; §6 (out-of-scope) restates it as a hard line.
- **B. Terminal seats poll bw; sub-agent CAPTAINs do not.** A radio-check can only reach seats that read bw on a cadence — i.e. TERMINAL seats (POLYBIUS, PLINY, and any launcher-spun architect seats), which are exactly the `stoa--reg` rows. A sub-agent CAPTAIN mid-dispatch does not poll (memory: "holds can't catch an in-flight sub-agent"), so the radio-check addresses **registry rows (terminal seats)**, not sub-agents. This bounds what "alive" even means here.
- **C. The honest-claim boundary mirrors the existing `stoa--reg` audit-only note.** A non-answer is *presumed* dead, not *proven* dead — a seat can be alive-but-slow, between turns, or briefly heads-down. The presumption is an operational default that triggers a verification/replacement decision, not a fact. The SAME audit-only boundary governs the ack's self-declared sid (see §2.4 / M1): provenance tags are forgeable body text, not authenticated identity.

The restatement converges with the brief and the re-forged directive; no divergence to surface. Imported assumptions A/B/C are the implicit scope the brief left for the design to make explicit.

---

## 2. Approach

### 2.1 The shape, in one paragraph

A **documented bw protocol** — NOT a new skill. A coordinator posts one `[radio-check]` bw comment naming the target seats by their `seat` (ROLE_slug) routing address; each named live seat, on its next poll, posts one `[radio-check-ack]` reply; after a stated window the coordinator reads the ticket, tallies which named seats answered, and marks the silent ones **PRESUMED dead**; for each presumed-dead seat user-tier POLYBIUS relaunches a replacement via `team-launcher` and the new seat self-records a fresh `stoa--reg` row. The protocol lives as a new top-level section in `operating-disciplines.md`; `stoa--reg`'s ticket body gains a one-paragraph WHO-vs-WHETHER + honest-claim note; `team-launcher/SKILL.md` gains a short "recovery = relaunch a replacement" cross-ref.

### 2.2 Helper-vs-protocol decision (my design call)

**Decision: documented bw protocol, NO new skill / script.** Justification:
- The entire protocol is **a handful of bw operations a terminal seat already performs every poll**: `bw comment` to ping, `bw comment` to ack, `bw show` to read the ticket, `git show beadwork:…/seat-registry.jsonl | grep` to resolve the target seat list. There is no compute a helper would encapsulate that the seat does not already do.
- A skill would have to be *invoked* — but the answerer half is not invoked, it is a polling-discipline behavior (recognize a `[radio-check]` addressed to me → reply). A skill cannot make a seat answer; only the role-file/op-disc discipline can. So the load-bearing half is documentation regardless.
- The brief's win condition is **human-simple**. A documented convention a human (or coordinator seat) can run by hand with two `bw comment`s beats a script that adds an install.sh deploy target, a Windows-path surface, and a maintenance burden — for zero capability gain.
- **Counter-considered and rejected:** a `radio-check.ps1` that posts the ping + sleeps the window + tallies. Rejected because (a) it would bake in a fixed window (the protocol wants a *coordinator-chosen* window), (b) it cannot make answerers answer, (c) a sleeping script is the passive-machinery smell the directive scrapped — it drifts toward "monitor" exactly the way scope-OUT warns against. The tally is a human/coordinator read, deliberately.

This is the honest-middle call: the protocol is the product; a helper does not earn its keep.

### 2.3 The protocol spec (ping → answer → window → tally)

**Roles:** *Coordinator* = the seat that needs to know (user-tier POLYBIUS, a floor-manager, or any terminal seat). *Target* = each seat the coordinator names.

**Step 1 — PING.** The coordinator resolves the current target seats from the registry. The registry is line-oriented JSONL (one seat per line, plain text), so the canonical resolve is **jq-free** — `grep` (bash) or `Select-String` (PowerShell). jq is NOT required (and is not installed on this host); use it only as an optional convenience if present.

bash (canonical):
```
git show beadwork:attachments/stoa--reg/seat-registry.jsonl | grep '"project":"the-stoa"' | grep '"status":"alive"'
```
PowerShell (canonical):
```
git show beadwork:attachments/stoa--reg/seat-registry.jsonl | Select-String '"project":"the-stoa"' | Select-String '"status":"alive"'
```
optional, ONLY if jq is installed:
```
git show beadwork:attachments/stoa--reg/seat-registry.jsonl | jq -c 'select(.project=="the-stoa" and .status=="alive")'
```
Each matched line is one seat row; read its `"seat":"…"` and `"session_id":"…"` fields by eye (or `grep -o '"seat":"[^"]*"'` / `grep -o '"session_id":"[^"]*"'`). The coordinator then posts ONE bw comment on the coordination ticket (default: `stoa--reg`, or the active arc ticket), naming each target by its `seat` routing address and stating the window:
```
bw comment stoa--reg "[radio-check] [for: POLYBIUS_the-stoa] [for: PLINY_the-stoa] window: 15min from 2026-06-26T17:00Z. Answer with [radio-check-ack]. [from: <coordinator-seat> | sid <sid>]"
```
The `[for: <seat>]` tags ARE the address (per `stoa--reg`: "the `seat` field (ROLE_slug) is the `[for:]` routing address"). One ping comment covers many targets.

**Step 2 — ANSWER.** Each named target, on its next bw poll, recognizes a `[radio-check]` addressed to its own seat and posts ONE reply on the same ticket:
```
bw comment stoa--reg "[radio-check-ack] [for: <coordinator-seat>] alive, sid <my-sid>. [from: POLYBIUS_the-stoa | sid 4f60c468-… | the-stoa]"
```
The ack carries the answerer's `seat` + live `sid` so the coordinator can run the **audit-only sid-match** in step 4 (catches a stale/typo/wrong sid — see M1, §2.6; this is NOT authentication and does not defeat a deliberate impersonator). A target NOT named in the ping does not answer (avoids ack-storms).

**Step 3 — WINDOW.** A **coordinator-chosen "reasonable window"**, stated in the ping. Default **15 minutes**; the coordinator may widen it for known-slow conditions (a seat mid-long-dispatch, overnight low-activity). The window is *stated in the ping*, never a fixed constant baked into a tool — this keeps it on-demand and prevents drift into a TTL. Rationale for the 15-min default: the team's pull-heartbeat floor is 60 min and routine polls are faster; 15 min comfortably exceeds a normal poll interval while staying responsive. The coordinator waits the window by reading the ticket again after it elapses (a `bw show`), NOT by a sleeping process.

**Step 4 — TALLY.** After the window, the coordinator reads the ticket:
```
bw show stoa--reg
```
and, by eye, inspects the comments since the ping for a `[radio-check-ack]` from each named target, then classifies each:
- **ANSWERED within window** → confirmed *present*, with an **audit-only sid check**: compare the ack's self-declared `sid` to the registry `session_id` for that `seat`. A MATCH is consistent with the recorded session answering. A MISMATCH (or an ack from a `sid` not in the registry) is NOT tallied alive — it is **flagged for escalation** (re-ping / investigate). NOTE the honest boundary: the sid is self-declared forgeable body text; the match catches an *accidental* stale/typo/wrong sid, it does NOT prove identity and does NOT defeat a deliberate impersonator who copies the registry sid (see M1, §2.6).
- **SILENT past window** → **PRESUMED dead** (honest-claim boundary: presumed, not proven — §2.4).

The tally is a coordinator judgment read, not an automated verdict.

### 2.4 The honest-claim boundary (exact text + placement)

This MIRRORS the existing `stoa--reg` audit-only honesty note. Two placements:

**(a) In `stoa--reg` ticket body** — appended after the existing HONEST-CLAIM BOUNDARY paragraph. Exact text to add (ADA posts this via `bw comment stoa--reg` AND it is folded into the canonical ticket-body description if the body is edited):
> WHO vs WHETHER-ALIVE-NOW: this registry is the durable WHO (the roster). It does NOT carry a live-presence field — `status` is a launch/stand-down stamp, not a heartbeat. To answer "is this seat alive RIGHT NOW?" use the on-demand radio-check ping (`operating-disciplines.md` §38). HONEST-CLAIM BOUNDARY (radio-check): a non-answer within the window is **PRESUMED dead, NOT proven dead** — a seat can be alive-but-slow, between turns, or briefly heads-down. The presumption triggers a verify/replace decision; it is not a fact. The ack's self-declared `sid` is checked against the registry `session_id` as an **audit-only** signal (catches a stale/typo/wrong sid) — this is the SAME forgeable-provenance boundary this contract already ratifies for the provenance tag: it is **not an authentication or authorization control** and does NOT defeat a deliberate impersonator who copies the registry sid. Liveness is answered by the live ping, never stored on the row.

**(b) In `operating-disciplines.md` §38** — the protocol section carries the same boundary inline as its closing clause (see §2.5 build plan), including the audit-only sid-match honesty.

### 2.5 Recovery path (relaunch a replacement, no resurrection)

A presumed-dead seat is **never resurrected** (its session is gone; its `sid` is dead). **User-tier POLYBIUS** (the seat that owns launching the team) relaunches a **REPLACEMENT**:

1. **Confirm the presumption** (recommended for the honest-claim boundary): re-ping the single silent seat with a widened window, or check for any fresh bw activity from it. If still silent, proceed.
2. **Relaunch via `team-launcher`** — bring up a fresh terminal seat for the dead role:
   ```
   .claude/skills/team-launcher/launch-team.ps1 -ProjectDir C:\Users\denso\claude_projects\the-stoa -Slug the-stoa
   ```
   (or a targeted single-seat relaunch using the same say/paste activation; the launcher mints a NEW `sid` and `--name`.)
3. **The replacement self-records / launcher-records** a fresh `stoa--reg` row via `record-seat.ps1` — `(seat, machine)` idempotent: the new row REPLACES the dead seat's row for that `(seat, machine)` pair, carrying the new live `sid` and `status:alive`. The dead session's old row is overwritten in place (no orphan).
4. **The dead seat's row is NOT manually flipped to `status:dead` as the liveness mechanism** — liveness is the ping, not the field. The row is simply replaced by the relaunch's idempotent rewrite. (If a coordinator wants a paper-trail of the death, a bw comment on `stoa--reg` is the change-log surface — comments are the human-readable change-log per the ticket contract.)

Recovery doc lands as: §38 recovery subsection in `operating-disciplines.md` + a 3-line cross-ref in `team-launcher/SKILL.md` ("Recovery: a seat presumed-dead by radio-check (§38) is replaced, not resurrected — relaunch here mints a fresh seat + idempotent `(seat,machine)` row.").

### 2.6 Threat → mitigation map (§35 A3 — author duty per §6.12)

Three named threats from the brief's threat-model. I am the upstream classifier proposing these; ARGUS confirms.

| `M<n>` (named threat) | attack-path (how realized) | how-defeated (design mechanism) |
|---|---|---|
| **M1** — a seat ANSWERS but is a zombie/stale (false-alive) via an ACCIDENTAL wrong/stale sid | A hung/looping or wrongly-configured session, or a copy-pasted-from-an-old-ticket ack, emits a `[radio-check-ack]` carrying a `sid` that is not the seat's current registry `session_id`, so a careless coordinator counts a dead-in-practice or wrong session as alive. | The ack MUST carry the answerer's `sid`; the coordinator runs an **audit-only sid-match** — compare the ack's self-declared `sid` to the registry `session_id` for that `seat`. A mismatch, or an ack from a sid not in the registry, is NOT tallied alive — it is **flagged for escalation** (re-ping / investigate), never confirmed. This catches the **accidental stale / typo / wrong-sid false-alive** path. **HONEST SCOPE (mirrors stoa--reg's ratified forgeable-provenance boundary):** bw stores a comment as `{text, timestamp}` only — the `[from:|sid]` is self-declared forgeable body text with NO bw-enforced author identity, and the registry `session_id` is world-readable JSONL. So the sid-match is **AUDIT-ONLY — it does NOT defeat a deliberate impersonator who copies the registry sid, and is NOT an authentication or authorization control.** A truly hung session simply will not poll/answer and falls to SILENT→presumed-dead. M1 defeats only the *accidental-wrong-sid* slice; it makes no authentication claim. |
| **M2** — honest-claim boundary erodes into "non-answer = proven dead" (false-dead → wrongful replacement) | A coordinator treats a single silent window as proof of death and relaunches a replacement against a seat that was merely alive-but-slow, double-seating the role (two live sessions, `--name` collision risk). | The honest-claim boundary text (§2.4) is canon in BOTH `stoa--reg` and §38: non-answer = PRESUMED, not proven. The recovery path §2.5 step 1 makes "confirm the presumption (re-ping with widened window)" an explicit pre-relaunch step. The `(seat,machine)`-idempotent record-seat write means even a wrongful relaunch overwrites rather than duplicates the row (bounds the blast radius). |
| **M3** — the protocol drifts back toward passive machinery / scope-creep | A future edit adds `last_seen`, a TTL, a periodic sweep, or a passive liveness field "for convenience," re-introducing the scrapped machinery. | §38 opens with an explicit SCOPE-FENCE clause naming the OUT items (no `last_seen` / TTL / sweep / continuous monitor / passive field; window is coordinator-stated per-ping, never a baked constant; tally is a read, never a sleeping process). The `stoa--reg` note states "liveness is answered by the live ping, never stored on the row." These give ARGUS/CATO/NOMOS a named anchor to flag any re-creep against. |

**Process-change carve-out (PROPOSED, ARGUS CONFIRMS — CONFIRMED rev1):** This arc is, in the main, a **doc/protocol/role-file change with NO new runtime attack surface** — `not threat-ratified (process change, no runtime attack path)` per §35.5. The three rows above are the security-relevant slices the brief named explicitly; they get maps + probes. The remaining content (the §38 prose, the SKILL.md cross-ref) is the carved-out process change. I cannot grant myself the carve-out; ARGUS confirms it (CONFIRMED in the rev1 verdict).

---

## 3. Verification probes (VERA executes these verbatim)

All probes run against the worktree `C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/stoa--fii-build` and the live the-stoa beadwork. Probe IDs are stable so the verdict's threat-coverage line can cite them. **All probes are jq-free** (jq is not installed on this host); use `grep` (bash) or `Select-String` (PowerShell).

### P1 — end-to-end radio-check happy path (DoD #1, #4)
**This is the core end-to-end demonstration.** Two live registry seats exist right now (`POLYBIUS_the-stoa` sid `4f60c468-9286-441f-8ffe-bf5979a65470`, `PLINY_the-stoa` sid `62a49ed0-cf37-4b6a-896d-3cebda142d5c`) plus a guaranteed-silent target. The FM (`POLYBIUS_the-stoa`) has committed to answering a REAL ack, so P1 is a live end-to-end demo (the simulated-ack path in step 3 remains the fallback if a peer cannot be driven).
Steps:
1. Resolve targets (jq-free): `git show beadwork:attachments/stoa--reg/seat-registry.jsonl | grep '"project":"the-stoa"' | grep '"status":"alive"'` — observe ≥2 alive the-stoa seats; read each line's `"seat"` and `"session_id"`.
2. Coordinator posts the ping naming TWO live seats AND one seat that does not exist / is dead (e.g. a known-dead `CHIRON_the-stoa`), with a SHORT window for test purposes:
   `bw comment stoa--fii "[radio-check] [for: POLYBIUS_the-stoa] [for: PLINY_the-stoa] [for: CHIRON_the-stoa] window: 10min. Answer [radio-check-ack]. [from: VERA-probe | sid <vera-sid>]"`
3. Within the window, the two live terminal seats post `[radio-check-ack] [for: VERA-probe] alive, sid <their-sid>` (the FM has committed to a real ack — prefer the live answer; if VERA cannot drive a given seat, simulate that seat's ack as a separate bw comment carrying that seat's registry `session_id`, which is the protocol's exact wire shape).
4. After the window, `bw show stoa--fii` and tally by eye.
**Expected observations (acceptance):**
- (a) Both named LIVE seats produced a `[radio-check-ack]` whose `sid` MATCHES their registry `session_id` → tallied **alive**.
- (b) The named DEAD/absent seat produced NO ack within the window → tallied **PRESUMED dead**.
- (c) The tally is derivable purely from reading the ticket comments + the registry — no passive field consulted, no jq required.

### P2 — M1 threat-anchored probe (audit-only sid-match: accidental wrong/stale sid flagged, NOT impersonation defeated)
**Drives the M1 attack path (the ACCIDENTAL-wrong-sid slice M1 is honestly scoped to), asserts both halves (attack-blocked + legit-unaffected), AND records the forgeable-text limit.**
1. **(attack-blocked = accidental wrong-sid flagged, not tallied)** Post an ack for `POLYBIUS_the-stoa` carrying a WRONG sid (a sid not equal to its registry `session_id`, e.g. a random GUID): `bw comment stoa--fii "[radio-check-ack] [for: VERA-probe] alive, sid 00000000-0000-0000-0000-000000000000. [from: POLYBIUS_the-stoa | sid 00000000-…]"`. Apply the §2.3 step-4 audit-only sid-match. **Expected:** the sid does NOT match the registry `session_id` for `POLYBIUS_the-stoa` → this ack is NOT tallied alive; it is flagged for escalation. The *accidental*-false-alive path is caught.
2. **(legit-unaffected)** Post a correct ack carrying the TRUE registry sid `4f60c468-9286-441f-8ffe-bf5979a65470`. **Expected:** matches → tallied alive. Legitimate acks are NOT broken by the sid-match check.
3. **(forgeable-text limit — honest-scope assertion, NOT a defeat claim)** Confirm canon does NOT claim the sid-match defeats impersonation: grep §38 / the `stoa--reg` note for the audit-only honesty wording (e.g. "audit-only", "not an authentication", "does not defeat a deliberate impersonator" or wording-equivalent). **Expected:** the audit-only boundary is stated; canon makes NO authentication claim. A deliberate impersonator copying the registry sid would NOT be blocked — and the design says so. (VERA must NOT assert M1 "defeats impersonation"; it defeats only stale/typo/wrong-sid.)
**Acceptance:** §38 / `stoa--reg` text states the audit-only sid-match rule AND its forgeable-text limit explicitly such that step 1 is flagged, step 2 passes, and step 3 confirms no over-claim.

### P3 — M2 threat-anchored probe (honest-claim boundary holds; false-dead is presumed not proven)
**Drives the M2 attack path, asserts both halves.**
1. **(attack-blocked = wrongful-replacement blocked)** Grep the shipped canon for the honest-claim boundary text in BOTH homes:
   - `operating-disciplines.md` §38 contains "PRESUMED dead, NOT proven" (or wording-equivalent) AND a pre-relaunch "confirm the presumption / re-ping with widened window" recovery step.
   - `stoa--reg` body/comment contains the mirrored WHO-vs-WHETHER + "presumed … not … proven" note.
   **Expected:** both present → a coordinator following canon does NOT treat one silent window as proof; the wrongful-immediate-replacement path is gated by the confirm-the-presumption step.
2. **(legit-unaffected)** Confirm the recovery path still permits relaunch AFTER the presumption is confirmed (the §2.5 path is not so cautious it blocks legitimate replacement). **Expected:** §2.5 documents a concrete relaunch command reachable after step 1.
**Acceptance:** both halves of the boundary present in canon; recovery remains executable for genuine deaths.

### P4 — M3 threat-anchored probe (no passive machinery / scope-fence holds)
**Drives the M3 attack path (scope-creep), asserts both halves. jq-free.**
1. **(attack-blocked)** Grep the arc's changed files for the scrapped passive-machinery vocabulary used in an IN-SCOPE (non-negating) sense: `last_seen`, `TTL`, `sweep`, `continuous monitor`, `passive liveness field`. **Expected:** every occurrence is inside a NEGATING / OUT / scope-fence context (mirrors NOMOS's directive audit method). NO in-scope re-introduction. Specifically: the `stoa--reg` JSONL row schema is UNCHANGED — `git show beadwork:attachments/stoa--reg/seat-registry.jsonl | head -1 | grep -o '"[a-z_]*":'` returns the SAME key set as pre-arc (12 keys: `seat, name, session_id, project, machine, role, tier, composition, gauntlet, chain_role, launched_at, status`) — no new liveness key.
2. **(legit-unaffected)** §38 SCOPE-FENCE clause is present and names the OUT items explicitly. **Expected:** the fence exists as a positive anchor.
**Acceptance:** zero in-scope passive-machinery; registry schema key set unchanged (jq-free grep-of-keys); scope-fence present.

### P5 — full existing suite + deploy-plan + author audit (DoD #5, #6; regression backstop)
1. **Author audit (DoD #5):** every file ADA touched — grep for author-like fields (`author`, `owner`, `creator`, `maintainer`, `by`, `copyright`); any present names **Denson Smith**. The `team-launcher/SKILL.md` frontmatter `author: Denson Smith` is UNCHANGED. No foreign author introduced.
2. **Deploy implication (DoD #6 — note, not in-arc action):** `operating-disciplines.md` deploys via a plain `cp` of the whole file (install.sh L1069) — a NEW INLINE top-level section needs **no install.sh array change** (unlike a relocated module, which would need an `OPDISC_MODULES` entry). VERA confirms: `bash substrate/install.sh --dry-run --target project --project-dir <tmp> | grep operating-disciplines` lists the file in the deploy plan (it already does). The deployed `.claude/` regen on main is the post-merge §18.1 self-apply — OUT of this arc's worktree scope; VERA notes it for the close-gate, does not execute it here.
3. **App adapter (DoD #6 implication):** if any substrate frontmatter changed (it should NOT — only prose added), `npm run gen-data` stays green. Since this arc adds prose + a SKILL cross-ref only (no frontmatter schema change), run `npm run gen-data` and confirm no roster diff / Zod failure.
4. **Full suite:** run the project's existing test suite (per the gauntlet-verify discipline: full suite IN ADDITION to bespoke probes) — confirm no regression introduced by the edits.

---

## 4. Concrete file-level build plan (for ADA)

| File | Change | Detail |
|---|---|---|
| `substrate/operating-disciplines.md` | **ADD** a new top-level section — **§38 "On-demand radio-check seat-liveness"** (place after §37; §37 is verified the current highest §, so §38 is the correct next integer). | Subsections: (38.1) WHO-vs-WHETHER framing + SCOPE-FENCE clause (names OUT items — M3 anchor); (38.2) the protocol (ping → answer → window → tally, with the **jq-free** worked `bw comment` / `grep` / `Select-String` examples from §2.3 — jq mentioned only as optional convenience); (38.3) the **audit-only sid-match** rule + its forgeable-text limit (M1 — explicitly NOT authentication, does NOT defeat a deliberate impersonator, mirrors stoa--reg's ratified boundary); (38.4) honest-claim boundary (M2, the §2.4(b) text, incl. the audit-only sid honesty); (38.5) recovery = relaunch a replacement (the §2.5 path); (38.6) cross-refs — `stoa--reg`, `team-launcher` SKILL, the §35 threat-map provenance, AND the **§7 disambiguation pointer** (see next row). Add a §0.5 relocation-index / TOC entry consistent with the file's existing §-header convention. |
| `substrate/operating-disciplines.md` §7 stub (core file, L183-200) | **ADD** a one-line disambiguating cross-ref **in the core §7 stub** (NOT only in the module — the stub is the in-core surface where a poll-filter / reader first lands). | The §7 token is `[radio-check <self-seat-slug>]` — the **PERIODIC two-POLYBIUS** peer-failure handshake/heartbeat (relocated to `.claude/modules/two-polybius-coordination.md` §7.1). §38's token is `[radio-check] [for: <seat>]` — the **ON-DEMAND** seat-liveness ping any coordinator addresses to named registry seats. Add to the §7 stub: "Distinct from §38 (on-demand radio-check seat-liveness): §7's `[radio-check <self-seat-slug>]` is the PERIODIC two-POLYBIUS handshake; §38's `[radio-check] [for: <seat>]` is the ON-DEMAND liveness ping — same `radio-check` token, different scope; do not conflate in poll-filters." |
| `substrate/modules/two-polybius-coordination.md` §7.1 | **ADD** the same one-line disambiguation **in the module body** (where the actual `[radio-check <self-seat-slug>]` token lives, so a reader who follows the stub into the module also sees it). | One line near §7.1's token definition: "NOTE — distinct from `operating-disciplines.md` §38: §7.1's `[radio-check <self-seat-slug>]` is the PERIODIC two-POLYBIUS peer-failure handshake; §38's `[radio-check] [for: <seat>]` is the ON-DEMAND seat-liveness ping. Same token prefix, different protocol." |
| `stoa--reg` ticket | **ADD** the WHO-vs-WHETHER + honest-claim note (incl. audit-only sid honesty). | Post via `bw comment stoa--reg "<§2.4(a) text> [from: ...]"`. If the canonical ticket-body description is editable in this workflow, also fold the note into the body after the existing HONEST-CLAIM BOUNDARY paragraph. Do NOT touch the JSONL attachment schema. |
| `substrate/skills/team-launcher/SKILL.md` | **ADD** a 3-line "Recovery" cross-ref. | Under a new bullet near the recovery/cross-references area: "Recovery (radio-check, op-disc §38): a seat presumed-dead by an on-demand radio-check is REPLACED, not resurrected — relaunch here mints a fresh seat + an idempotent `(seat,machine)` registry row that overwrites the dead row." Frontmatter `author: Denson Smith` UNCHANGED. |
| **No new skill / script.** | — | Per §2.2: documented protocol, not a helper. No install.sh `SKILL_NAMES` change; no new file under `substrate/skills/`. |
| **No `stoa--reg` schema change.** | — | The JSONL row keys are unchanged (12 keys). Liveness is the ping, never a field. |

**Deploy note for ADA/VERA (DoD #6):** `operating-disciplines.md` deploys via plain `cp` (install.sh L1069); a NEW INLINE section needs no array edit. `two-polybius-coordination.md` is a RELOCATED module already in `OPDISC_MODULES` (install.sh L1266) — editing its body (not adding a module) needs no array change. The deployed `.claude/operating-disciplines.md` + `.claude/modules/` regen on main is the post-merge §18.1 self-apply — not an in-worktree action. `team-launcher/SKILL.md` is already in `SKILL_NAMES` (editing it, not adding a file, so no array change). If §38 is ever made a relocated module instead of inline (NOT this design's choice), it WOULD need an `OPDISC_MODULES` entry at install.sh L1266 — flagged so a future arc does not miss it.

---

## 5. Self-assessed weak points

1. **VERA driving real peer seats is not guaranteed (but a real demo is now reachable).** P1/P2 assume VERA can either elicit acks from the live FM/PLINY or faithfully simulate each seat's ack with the correct registry sid. The FM (`POLYBIUS_the-stoa`) has committed to answering a REAL ack, so P1 upgrades to a live end-to-end demo; if VERA cannot drive a given seat, the simulated-ack path is the wire-shape-faithful fallback (it posts the exact bytes a real seat would). **Why this shape anyway:** the protocol's correctness is in the *coordinator's tally logic* (audit-only sid-match, window, presumed-dead), which is fully exercisable by simulated acks; eliciting a real peer ack is a nice-to-have integration check, not the load-bearing assertion. ARGUS confirmed the simulated-ack fallback ACCEPTABLE in rev1.

2. **The audit-only sid-match defeats only the ACCIDENTAL wrong-sid slice — NOT a deliberate impersonator, and not a hung-but-real-sid session.** bw comments carry no enforced author identity; the `[from:|sid]` is forgeable body text and the registry sid is world-readable, so an attacker who copies the registry sid is NOT caught. A session that is alive-enough-to-have-a-sid-but-too-hung-to-answer simply will not ack and falls to SILENT→presumed-dead (the correct outcome — it gets replaced). **Why this shape anyway:** proving identity or liveness-of-mind over a forgeable-text channel is unsolvable without authenticated comments or a passive heartbeat — exactly the machinery scope-OUT scrapped, and exactly the boundary stoa--reg's own contract already ratified as "audit-only, not an authentication control." M1 is honestly scoped to the accidental-false-alive slice and the design states the limit in canon (P2 step 3 asserts it). This is the r2 fix; the honest framing is the correct boundary, not a gap to close in this arc.

3. **The "coordinator-chosen window" is judgment, not a constant — a careless coordinator could pick too-short a window and over-tally dead.** **Why this shape anyway:** a baked constant IS the TTL the directive scrapped; the window MUST be per-ping to stay on-demand. M2's confirm-the-presumption step is the backstop against a too-short window causing wrongful replacement. The 15-min default + the M2 re-ping guard is the proportionate mitigation; making the window rigid would violate scope.

4. **`stoa--reg` body-edit vs comment-only.** I specified the honest-claim note go into BOTH the ticket body (if editable in this workflow) and a comment. If the workflow only permits comments (not body edits), the canonical-record half lands as a comment only, which is the human-readable change-log surface, not the contract body. **Why this shape anyway:** the comment is always achievable and the change-log is the contract-sanctioned surface; the body-edit is the stronger placement when available. ARGUS confirmed this is NOT load-bearing in rev1; either satisfies DoD #3.

---

## 6. Out of scope (HARD fence — restated for ADA + ARGUS)

- **Periodic sweep / continuous monitoring** — scrapped by the directive; §38 is on-demand only.
- **`last_seen` field, TTL, any passive liveness field on the `stoa--reg` row** — the JSONL schema is NOT extended (12 keys unchanged). Liveness is the ping, never stored.
- **A launcher-folded sweep** — the launcher's only role here is RECOVERY (relaunch a replacement), not monitoring.
- **A radio-check skill / script** — documented protocol only (§2.2 decision).
- **Resurrecting a dead session** — recovery is replacement only.
- **Authentication of acks / non-forgeable provenance** — the ack's sid is audit-only forgeable body text (M1 honest scope, r2); making it authenticated would require a new identity mechanism stoa--reg explicitly does not provide. OUT of this human-simple arc; if a future arc wires the sid into an access/authz decision, stoa--reg's R1 re-opens as a named runtime threat.
- **Sub-agent liveness** — sub-agent CAPTAINs do not poll bw mid-dispatch; the radio-check addresses terminal seats (registry rows). Sub-agent presence is the orchestrator's heartbeat surface (§18), out of scope here.
- **The pre-existing stoa--reg jq-based read-recipe** — the substrate-wide assumption that jq is present (it is not, on this host) lives in the existing stoa--reg ticket body; fixing it is OUT of this arc's scope. THIS design's protocol text stands on its own jq-free (r1).
- **The deployed `.claude/` regen on main** — the post-merge §18.1 self-apply, out of the build worktree's scope (noted for the close-gate, §4).

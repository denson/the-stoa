# Arc 67 build directive — Session-identity deployment pattern (pin + name + record at launch · whoami self-discovery · sign-everywhere · portable bw registry)

**Audience:** the fresh Claude Code sessions opened to build Arc 67 (PLINY_the-stoa + the floor-manager POLYBIUS_the-stoa).
**Authored by:** Polybius_the_Stoa (user-level Stoa agent, sid 990b0750-5572-4836-b9c7-18d626a12e96) on behalf of the PRINCIPAL (Denson Smith) via Polybius the Grand.
**Status:** FINALIZED on the locked brief (the WHAT is PRINCIPAL-locked; the HOW is your team's design). NOT yet dispatched — staged pending a scope-nod, then committed + launched.
**Builds on:** current the-stoa main. The user-tier anchor (visible only to user-tier) is `u--5f0`; this arc's project-tier charter is the EXISTING **`stoa--p7c`** ('Persistent agent-identity scheme') — the epic this arc implements. The launcher itself flags this at `substrate/skills/team-launcher/launch-team.ps1:49-50`.

**You are MAJOR_PLINY for the the-stoa Arc 67 engagement.** Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role. Open Claude Code in `C:\Users\denso\claude_projects\the-stoa\`.

**Your one job:** make Stoa agent IDENTITY first-class and durable — (1) the team-launcher ALWAYS mints a session-id + assigns a human-friendly name + launches with `--session-id`/`--name` and RECORDS the seat→{id,name,project,machine} mapping to a portable bw registry; (2) a `whoami` skill so a desktop-created session can DISCOVER its own id; (3) a sign-everywhere convention so every seat carries its id+name in all bw comments, git trailers, and recordkeeping. Then return cleanly.

**This is a substrate-canon arc — run the full gauntlet** (DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS). It touches the team-launcher tooling, a new skill, and `operating-disciplines.md` canon. Surface the open design items (below) at the DAEDALUS hand-back before locking the build.

---

## Comms — async with Polybius_the_Stoa via bw (`stoa--*`)

Coordinate on the charter ticket **`stoa--p7c`**. Polybius_the_Stoa (the user-level seat that owns this arc) monitors and interjects; the floor-manager runs independent verification at each hand-back and relays up. The PRINCIPAL is not the relay — beadwork is. Asymmetric polling: don't poll while working; do poll when waiting (between phases / after surface) via `CronCreate */5`. `bw comment <id> "text"` is **positional, no `-m`**. Run `bw prime` at activation.

**DOGFOOD the thing you are building:** from turn one, every seat signs its bw comments with `[from: <NAME> | sid <session-id>]` — discover your own id via the whoami recipe in §Settled. This arc builds the sign-everywhere convention; the team proves it by living it.

---

## Read first (the spec)

1. **The charter ticket `stoa--p7c`** — body + ALL comments: they carry the original design context + 5 open questions (schema · persistence · convention-vs-enforcement · **reuse §28** · make-the-id-the-`[for:]`-address) and the generation-marker naming (POLYBIUS-A2A_the_younger / Polybius the Grand). The brief (your locked WHAT) RESOLVES these in a **session-id-centric** direction (session-id = the unique handle; the name is human-friendly + non-unique) — you implement that resolution, you do NOT re-open the schema debate. Q5 (the id+name becomes the canonical `[for: agent]` routing address) is IN SCOPE via sign-everywhere. The p7c rollout requirement (post the user-tier update path on the commons `cm-` channel for an already-installed team) is a SHIP-time item — surface to Polybius_the_Stoa; do NOT expand the build into it.
2. **`substrate/skills/team-launcher/launch-team.ps1`** — the launch script (171 lines). The `claude` invocation lines (~L128 panes/tabs, ~L145 windows) are where `--session-id` joins the existing `--name`. L49-50 names the stoa--p7c hook this arc lands. NOTE: the **deployed** copy at `~/.claude/skills/team-launcher/launch-team.ps1` is 200 lines and carries `-ArcId`/`-OnlySeat` (14 refs) the 171-line substrate source LACKS — see Design item DC1 (stoa--fpj fold).
3. **`substrate/skills/team-launcher/SKILL.md`** — the skill doc; update for the new launch behavior.
4. **`substrate/operating-disciplines.md` §28** (line ~1119, "Per-CAPTAIN git seat identity via Co-Authored-By trailer") — currently CAPTAINs-only + git-trailer-only. The sign-everywhere convention BROADENS this — see DC3.
5. **`substrate/MAJOR_*.md` / `substrate/CAPTAIN_*.md` role files** — where the sign-everywhere convention is referenced for each seat (the per-seat application of DC3).
6. **`stoa--fpj`** (bw) — the launch-team.ps1 SSoT-inversion bug this arc folds in (DC1).

---

## Settled — do NOT re-litigate (PRINCIPAL-locked WHAT + verified facts)

### The four requirements (PRINCIPAL, locked)
1. **LAUNCH:** `team-launcher` (and any builder/provisioning launch) ALWAYS: mints a UUID, assigns a human-friendly name, launches with `--session-id` + `--name` (+ `--remote-control` where appropriate), and RECORDS seat → {session-id, name, project, machine} durably to the registry.
2. **WHOAMI:** a python skill/script any agent runs to discover its own session id (the nonce-grep recipe), for desktop-created sessions that could not pin `--session-id` at creation.
3. **SIGN-EVERYWHERE:** update the skills / operating-disciplines / role-file convention so every seat includes its session-id + name in ALL bw comments, git trailers, and recordkeeping.
4. **REGISTRY:** the seat→id→project mapping is the durable roster (answers "which seat owns which project / is it alive"). It MUST be portable — live in **bw** (git-synced), since session-ids are per-machine and the roster must survive across machines.

### Verified facts — do NOT re-derive (confirmed vs Claude Code 2.1.170 + live test)
- `claude --session-id <uuid>` **pins** a known id at launch. `--name <name>` sets a human-friendly name — **MUST be space-free** (Windows Terminal splits args on spaces; use underscores, e.g. `Polybius_the_Stoa`). `--remote-control [name]` bridges a terminal session into the desktop/phone Code tab.
- **Sessions are LOCAL-ONLY** — no cloud sync; **cross-machine `--resume` is NOT supported.** A session-id is a **same-machine handle**. Cross-machine continuity stays on **bw + handoffs** (a fresh session elsewhere resumes the WORK, not the transcript). **Do NOT design around cloud-resume.**
- A **desktop-UI-created session cannot set `--session-id`** at creation → it must DISCOVER its id.
- **whoami nonce-grep recipe:** (1) emit a unique nonce into your own transcript — `echo "SELFID-<uuid>"` via Bash (the tool-call input is logged to your `.jsonl`); (2) on a subsequent turn, `grep -l "SELFID-<uuid>" ~/.claude/projects/C--Users-denso-claude-projects*/*.jsonl`; (3) your session id = matching filename minus `.jsonl`. The transcript filename **is** the id. Store root: `C:\Users\denso\.claude\projects\<slug>\` — the `*` glob covers BOTH the user-tier slug `C--Users-denso-claude-projects` AND per-project slugs (e.g. `…-the-stoa`). **Empirical refinement (Polybius_the_Stoa, this arc):** the nonce flushed and resolved INTRA-TURN (a same-turn grep found it) — "subsequent turn" is conservative. DAEDALUS decides whether the skill keeps the conservative subsequent-turn guidance for robustness or greps same-turn with a flush-retry loop.
- **Remote Control's remote surface is permission-gated** (a session launched `--dangerously-skip-permissions` locally still prompts on the remote side; no remote-approve mechanism → unattended remote-driven sessions stall). Relevant only if you wire RC into launches; do not try to solve the remote-approve gap here.

---

## Design items — your team's HOW (surface resolutions at the DAEDALUS hand-back)

- **DC1 — FOLD `stoa--fpj` into the launcher rewrite (lean: FOLD).** The substrate source (171L) lacks the `-ArcId`/`-OnlySeat` params the deployed copy (200L) has — the substrate is NOT currently the SSoT. Since this arc rewrites `launch-team.ps1` anyway (to add the session-id machinery), do the SSoT backport in the SAME coherent rewrite: bring `-ArcId`/`-OnlySeat` into the substrate source AND add the mint/name/record machinery, so one launcher is both correct AND the SSoT. *DAEDALUS confirms fold-vs-sequence; if folding bloats the diff unmanageably, sequence stoa--fpj first — surface to Polybius_the_Stoa.* Resolving stoa--fpj's SSoT inversion is IN SCOPE either way (a blind install.sh of the 171L source would regress deployed copies).
- **DC2 — registry format + location (in bw; ONE shared roster).** It MUST live in bw (portable). Whether the roster is a dedicated bw ticket (comments = roster rows), a manifest file attached to a bw ticket on the beadwork branch, or another bw-native shape is DAEDALUS's call. Design it as the SINGLE shared seat-registry that the FORTHCOMING builder-deploy cookie-cutter work will ADOPT (one registry, not two). **Correction to the brief's premise (verified by Polybius_the_Stoa):** `user-beadwork/plans/origindex-builder-publish-security-model.md` is a *network-access* identity model (Tailscale/WireGuard mesh + SSO, builder DB + published slices) — it defines NO seat-instance registry and is ORTHOGONAL to this roster. Do NOT force-converge this registry with that security model; the convergence target is the future builder-deploy launcher, which should reuse THIS registry.
- **DC3 — sign-everywhere convention: BROADEN §28.** §28 today is CAPTAINs-only + git-trailer-only. Broaden it (extend §28, or a sibling section — DAEDALUS's call) to: ALL seats; ALL channels (bw comments + git trailers + recordkeeping); carrying session-id + name (not only the seat mnemonic). Define the concrete FORMAT + PLACEMENT for each channel — e.g. bw comment `[from: <NAME> | sid <session-id>]`, a git trailer, and the registry record — and where each role file references it. Preserve the §28 absolute that git `Author:` stays the PRINCIPAL's identity; id+name are layered ON TOP, never in place of it.
- **DC4 — whoami skill shape.** Python skill (consistent with the substrate skill convention). Implements the nonce-grep recipe; handles concurrent same-dir sessions (unique nonce) and the multi-slug store glob. Decide the flush model (subsequent-turn vs same-turn-with-retry) per the empirical refinement above. Output: the bare session id (and optionally the matched store path) so a seat can self-record into the registry.

---

## Deliverables (land together)

1. **Launcher rewrite** — `substrate/skills/team-launcher/launch-team.ps1`: mint a per-seat UUID, pass `--session-id <uuid>` alongside `--name`, optional `--remote-control`, and RECORD seat→{session-id,name,project,machine} to the bw registry; FOLD the stoa--fpj `-ArcId`/`-OnlySeat` backport (DC1). Update `substrate/skills/team-launcher/SKILL.md`.
2. **New `whoami` skill** — `substrate/skills/whoami/` (SKILL.md + python), the nonce-grep self-discovery (DC4). Add to `install.sh` `SKILL_NAMES` so it deploys to every workspace.
3. **Sign-everywhere canon** — broaden `operating-disciplines.md` §28 (DC3) + reference it in the role files so every seat signs with id+name across bw/git/recordkeeping.
4. **The bw registry** — stand up the portable seat-registry (DC2) and seed it with the arc's own seats (dogfood). Document how a seat records itself + how PRINCIPAL reads "which seat owns which project / is it alive."
5. **Dangling refs / consistency** — `install.sh` (whoami in SKILL_NAMES; launcher unaffected by recompose), any cross-refs to the interim seat-name scheme (launch-team.ps1:49-50 stoa--p7c note → resolved).

---

## Verification / Definition of done

The launcher's `-DryRun` early-returns before opening sessions, so it can ONLY prove the printed command shape — it CANNOT exercise the registry-write or a live session. Gate the verifiable parts on REAL execution (banked lesson: a DoD that gates on `--dry-run` cannot test what the dry-run skips):

- **Launcher command shape (`-DryRun`):** the printed `wt`/`pwsh` command includes `--session-id <uuid>` + `--name <space-free-name>` for each seat. (This is ALL the dry-run can verify.)
- **Registry write — REAL execution:** VERA exercises the mint+record path FOR REAL (records a synthetic seat→{id,name,project,machine} row to the bw registry and reads it back) WITHOUT spawning a live agent session. Design the record step (DC2) so this is possible — do NOT make a full live-session spawn the only verification path.
- **whoami — REAL execution:** a real nonce-grep round-trip returns the correct session id for the running session (the dogfood VERA itself can run).
- **Sign-everywhere canon:** §28 broadened as specified; role files reference it; the §28 git-`Author:`-stays-PRINCIPAL absolute is preserved. Grep proves no seat references the retired interim-name scheme as canonical.
- **No cross-machine-resume promise** anywhere in the new canon/skill/launcher text (grep for "resume" in the touched files → only same-machine-correct usage).
- **`grep -rn "session-id\|--session-id\|whoami" substrate/` returns only intended references.**
- **NOMOS CONFORMANT** on the final commit. Commits carry Author=PRINCIPAL + the CAPTAIN seat-identity Co-Authored-By trailer per §28.
- Committed + pushed to `the-stoa` main; charter ticket updated with the landing SHA; `stoa--fpj` closed (folded) or sequenced per DC1.

---

## Out of scope

- **Cross-machine `--resume` / cloud-sync** — explicitly NOT a thing; do not design for it (continuity stays on bw+handoffs).
- **The builder-deploy cookie-cutter BUILD** — only design the registry to be adoptable by it (DC2); do not build the builder launcher here.
- **Remote-Control unattended remote-approve** — a known permission-gate constraint; note it, do not solve it.
- **A full `operating-disciplines.md` audit** beyond the §28 broadening — flag anything found via fix-now/ticket, don't expand scope.

---

## Discipline

- Full gauntlet — canon + tooling; NOT mechanical.
- Verify-then-execute; one-job-per-agent (resist drifting into the builder-deploy work).
- Fix-now for small related defects; ticket-with-plan if scope-different.
- DOGFOOD the sign-everywhere convention from turn one (every seat signs id+name).
- bw syntax: positional `bw comment`; `bw prime` at activation; `--reason` on close.

## Suggested phasing

- **Phase A — design (DAEDALUS).** Resolve DC1–DC4 with Polybius_the_Stoa; produce the concrete edit plan (launcher rewrite incl. stoa--fpj fold, whoami skill, §28 broadening, registry shape). Surface for a Colonel call before build.
- **Phase B — tooling + skill (ADA).** Launcher rewrite, whoami skill, install.sh SKILL_NAMES.
- **Phase C — canon (ADA).** §28 broadening + role-file references + the registry stand-up.
- **Phase D — verify (ARGUS/VERA/CATO/ZENO + NOMOS).** Dry-run command shape; REAL registry-write round-trip; REAL whoami round-trip; canon greps; ground-truth.
- **Phase E — ship.** Commit + push; update the charter ticket with the SHA; close/sequence stoa--fpj.

Standby, run.

# Arc 25 build directive — Credential discipline as substrate canon

**Audience:** the fresh Claude Code session opened to build Arc 25 deliverables (MAJOR_PLINY).
**Authored by:** user-tier MAJOR_POLYBIUS + the PRINCIPAL (Denson Smith).
**Status:** active directive. **Arc 24 (`stoa--cm3`) is CLOSED** — precondition satisfied.
**Bw ticket:** `stoa--p5g` (the work-unit; itself the arc's coherent scope — no parent epic needed for this arc).
**Builds on:** Arcs 1-24 (the-stoa main as of Arc 24 ship commit).

**Your one job:** canonicalize the credential-discipline architecture into substrate so every future team inherits it. The empirical anchor is the 2026-05-15 → 2026-05-16 railway_stoa → sector-4 deploy arc, which produced the canonical pattern (GCP Secret Manager + GitHub Actions WIF + CI-mediated deploys, agents NEVER hold credentials) after testing-and-rejecting five named anti-patterns. The substrate currently has zero credential-discipline canon. Every workspace that handles credentialed operations re-derives the architecture from scratch and re-makes the same mistakes. This arc closes that gap.

One ticket, one coherent push:
- **stoa--p5g** (P1) — Substrate fix: credential discipline — batch or env-inject, never per-call prompts. The ticket body + three comments carry the full architectural decision-trail (initial scope → wrapper-launch proposed → wrapper-launch rejected on PRINCIPAL's empirical rule → final CI-mediated canon + 5 named anti-patterns + 2 Railway-specific footnote candidates). **DAEDALUS treats the ticket body + comments as primary input prose.**

This is a focused arc. ~10-15 substrate-prose deliverables across ~6 files. Smaller than Arc 24. Architectural decisions are already locked in `stoa--p5g` comments — your Phase 1 work is structural (turning the locked decisions into file-by-file edit specs), not deliberative.

---

## Comms — autonomous mode via bw, radio-check protocol

POLYBIUS (user-tier CoS — note: this arc is dispatched from USER-tier POLYBIUS, not project-tier; user-tier has downward read+write into project bw) and you communicate via comments on `stoa--p5g`. PRINCIPAL is **not** the relay for routine status — beadwork is.

**bw command syntax** is in `substrate/MAJOR_PLINY.md` §6.1. Critical: `bw comment <id> "text"` is positional, no `--body` flag. `bw close <id> --reason "text"` — `--reason` is a flag.

**Polling discipline** per `substrate/operating-disciplines.md` §7 (surface-and-wait + radio-check). On dispatch, post an initialization handshake comment on `stoa--p5g` naming your cron id (if you set one up) and your cadence. Heartbeat every ≤30 min unless surface-and-wait-blocked.

POLYBIUS is in autonomous mode for this engagement. PRINCIPAL is exception-handler — project-direction calls, ship/no-ship, substance disagreement after one round, authorship/copyright/Denson-final-say content, irreducible ambiguity, peer silence > 60 min, arc closes.

**Note on this arc specifically:** the discipline you're building is meta-load-bearing — once landed, every future arc that touches credentialed ops will use this discipline. The CAPTAIN envelopes you edit in Phase 2 are the envelopes Phase 3 verifiers (themselves CAPTAINs) read at dispatch time. Self-referential, not circular. Same dynamic as Arc 24's heartbeat-discipline edit.

---

## Read first

Before any design or build work, read in order:

1. **`stoa--p5g` ticket body + all three comments in full.** This is the primary spec. The ticket body has the initial scope; comment 1 (2026-05-15T22:54Z) refined to the wrapper-launch proposal; comment 2 (2026-05-16T05:53Z) carries the **FINAL ARCHITECTURE DECISION** that supersedes wrapper-launch — read this comment **with extra care**, it's the load-bearing architectural artifact; comment 3 (2026-05-16T08:05Z) adds Railway-specific footnote candidates for the substrate doc.

2. **The worked example workflow** at `github.com/denson/sector-4/.github/workflows/deploy-dev-ariadne.yml`. This is the canonical CI-mediated deploy workflow built during railway--r9z, validated end-to-end (run 25956772075 + the post-fix dev Ariadne deployment serving healthy responses as of arc dispatch). The new substrate-tier skill (per A4 below) points at this workflow as the canonical worked example.

3. **`substrate/operating-disciplines.md`** — read in full to understand existing sections + numbering conventions. New "Credential discipline" section appends.

4. **All CAPTAIN role files (`substrate/CAPTAIN_*.md`)** — inventory at dispatch time (A6). Envelopes for DAEDALUS, ADA, ARGUS, BARTLEBY receive cross-references (per A5).

5. **`~/.claude/CLAUDE.md`** (user-tier, read-only context) — find the existing "refusal-as-signal" harness rule. Per A3 it promotes to substrate canon.

6. **`~/.claude/skills/railway-access/SKILL.md`** (user-tier, to be deleted per A8) — read once to confirm it documents the now-rejected parent-shell-env pattern. ADA deletes in Phase 2.

7. **`railway_stoa/railway--r9z` and `railway_stoa/railway--7r6`** (cross-workspace context) — the worked-example trail. Not edited; referenced.

8. **`ariadne-core-workspace/ariadne--u83`** (cross-workspace context) — the 502 follow-up that surfaced the Railway-reference-resolution behavior captured as footnote-candidate in `stoa--p5g` comment 3. Not edited; referenced.

---

## Phase A — Architectural decisions (LOCKED pre-dispatch)

Settled during ticket evolution + this directive authoring. You do NOT surface these as design questions.

### A1. One arc, four phases, one gauntlet — LOCKED

`stoa--p5g` is a coherent single work-unit (no children). Single DAEDALUS design covering all substrate touch-points. Single ARGUS audit. Single ADA worktree on `arc-25/build`. Verifiers (VERA / CATO / ZENO) each one pass over the integrated diff.

Phasing:

| Phase | Seat(s) | Output |
|---|---|---|
| 1 | DAEDALUS + ARGUS | `agents/design/arc-25/design.md` — integrated design covering: new operating-disciplines.md "Credential discipline" section, new substrate-tier `credential-discipline` skill, CAPTAIN envelope cross-references, install.sh delta if needed, ~/.claude/skills/railway-access/ deletion. ARGUS cold-audits before ADA dispatches. |
| 2 | ADA | feature branch `arc-25/build` covering all substrate edits + railway-access skill deletion. |
| 3 | VERA + CATO + ZENO | parallel verification pass. VERA probes per-file content + verifies install.sh dry-run still lists everything correctly + verifies the new skill renders. CATO cold-reads entire diff for wording drift / cross-reference correctness / scope creep. ZENO checks spec-vs-result. |
| 4 | PLINY + smoke + ship | smoke beats (install.sh dry-run, grep for "refusal-as-signal" in operating-disciplines.md, grep for "CI-mediated" in CAPTAIN envelopes). PR opened. PLINY runs `gh pr merge` after clean PASS. `stoa--p5g` closes. |

### A2. operating-disciplines.md gets a new section: "Credential discipline" — LOCKED

Section authors:
- **The canonical pattern:** CI-mediated deploys. Agents NEVER hold credentials. Sensitive secrets live in a cloud-native secrets manager (GCP Secret Manager is the worked example; AWS Secrets Manager / Azure Key Vault are equivalents). CI authenticates via Workload Identity Federation (no static cloud-key on dev machines or in GitHub). Per-service tokens that lack WIF support (e.g. Railway API tokens) live in GitHub Actions encrypted secrets. Routing identifiers live in GitHub Actions variables. Deployed services receive runtime secrets as env vars set by the workflow at deploy time.
- **The five named anti-patterns** (with the shared root cause — "any credential in agent-reachable scope eventually surfaces"):
  1. Per-call `op` invocation (per-PID biometric prompt on Windows → auth fatigue → refusal-as-signal violation)
  2. File-on-disk credential (agent reads via cat, grep, debug scripts)
  3. Parent-shell env injection (agent reads via printenv, Get-ChildItem Env)
  4. `op run` wrapper at Claude Code launch (1Password's recommended pattern; same runtime-env exposure as parent-shell-env even though it eliminates disk-at-rest exposure; rejected on PRINCIPAL's empirical rule that "every prior agent-credential-access has eventually leaked")
  5. Local MCP-server-as-credential-broker (broker on same host as agent; agent can read broker's source, infer policy, potentially inspect process state)
- **The universal rule:** agents do non-credentialed work; CI or humans do credentialed setup. Cross-reference to the new credential-discipline substrate-skill (per A4).

Section number: assigned at design time based on current operating-disciplines.md state. DAEDALUS picks; ARGUS confirms the placement is consistent with existing section logic.

### A3. Refusal-as-signal promotes from user-tier harness-rule to substrate operating-disciplines.md — LOCKED

Currently lives in `~/.claude/CLAUDE.md` as a harness-rule (agent refuses when asked to do credentialed work that bypasses the canonical pattern; refusal is the signal, not a problem to route around). Promotes to substrate-canon for every seat as part of (or adjacent to) the new "Credential discipline" section. Triggered halt with no retry, no fallback, no improvisation.

DAEDALUS decides whether refusal-as-signal is a subsection within "Credential discipline" or a peer section that cross-references it. Both are defensible; pick one and document the rationale.

### A4. New substrate-tier skill: `substrate/skills/credential-discipline/SKILL.md` — LOCKED

Worked example skill. Documents:
- The architectural pattern (referencing the new operating-disciplines.md section)
- gcloud commands for WIF pool + provider + service account setup (or pointer to GCP console walkthrough)
- GitHub Actions YAML template for `google-github-actions/auth@v2` + `get-secretmanager-secrets@v2`
- Railway-specific patterns for token-based services that lack WIF (PAT in GH Secrets, account-scoped tokens with `--project/--environment/--service` flags)
- The two Railway-specific footnote candidates from `stoa--p5g` comment 3:
  1. **Reference variables resolve only at deploy-time, not at CLI-time.** `railway variable list/get` returns null VALUE for reference-typed variables. To get a resolved value in CI, fetch from the SOURCE service where the variable is a literal.
  2. **Anti-pattern: `railway run --service NAME -- cmd`.** This does NOT exec inside the service container — it runs on the local shell with the service's env vars injected. Same reference-resolution limitation. Named in the skill as misleading-but-syntactically-valid.

Skill metadata follows existing substrate-skill conventions (check other `substrate/skills/*/SKILL.md` files for the canonical structure). Authorship: Denson Smith per substrate/CLAUDE.md.

### A5. CAPTAIN envelope updates: DAEDALUS, ADA, ARGUS, BARTLEBY — LOCKED

Each envelope receives a short section (or addition to existing section) directing: when dispatch involves credentialed operations, brief MUST direct the work to CI-mediated form. Never "agent runs CLI X with credentials." Always "agent authors the CI workflow that does X; CI runs the workflow." Cross-reference the new substrate-skill (A4).

Per-CAPTAIN wording adapts to seat:
- DAEDALUS: when designing for credentialed ops, design.md MUST specify CI-mediated path.
- ADA: when implementing credentialed ops, refuse the manual path; produce the CI workflow instead.
- ARGUS: when auditing a design for credentialed ops, FLAG any non-CI-mediated approach as a load-bearing risk.
- BARTLEBY: when surfacing credentialed-resource locations, include cross-ref to the credential-discipline skill.

VERA / CATO / ZENO / STRABO / CURATOR / HERALD — envelopes NOT touched in this arc unless DAEDALUS surfaces an empirically-justified reason. Scope is locked to the four seats whose role is directly credentialed-ops-adjacent.

### A6. CAPTAIN inventory taken at dispatch time — LOCKED

Substrate may have grown new CAPTAINs since Arc 24 close. Whatever exists in `substrate/CAPTAIN_*.md` at dispatch time gets the envelope update if the seat matches the four named in A5. New CAPTAINs not yet enumerated: PLINY decides whether they're in scope based on whether their core role touches credentialed ops.

### A7. install.sh deploys the new skill — LOCKED

`substrate/install.sh` deploys substrate-skills to user-tier and project-tier on standard install. ADA verifies install.sh dry-run lists the new `credential-discipline/SKILL.md` file in its deploy manifest. If install.sh requires an explicit skill enumeration (vs glob-discovery), ADA adds the line.

### A8. ~/.claude/skills/railway-access/SKILL.md decision: DELETE — LOCKED

The skill documents a now-rejected pattern (parent-shell-env). CI-mediated pattern doesn't need a workspace-local Railway-credential skill. ADA deletes the skill file in Phase 2 as part of the integrated diff.

**Cross-coordination:** `railway_stoa/railway--dwc` is the port-skill ticket that planned to port railway-access to workspace-tier. After Arc 25 closes, user-tier POLYBIUS comments on `railway--dwc` with reason "obviated by CI-mediated pattern; close." That coordination is OUT OF SCOPE for Arc 25 PLINY — leave to user-tier POLYBIUS.

### A9. Worked-example file is denson/sector-4 deploy workflow — LOCKED

Stable at `.github/workflows/deploy-dev-ariadne.yml` in `github.com/denson/sector-4` main HEAD (~564 lines, validated end-to-end). The new credential-discipline skill (A4) points at that path + the GitHub URL. If denson/sector-4 is private (it is), the skill notes the visibility constraint but the URL is still load-bearing (PRINCIPAL can grant repo access if needed).

### A10. Authorship attribution immutable per substrate/CLAUDE.md — LOCKED

All new files and edits credit Denson Smith. Skill metadata, new operating-disciplines section, any new templates. No exception.

### A11. No substrate-tier behavioral changes outside the credential discipline — LOCKED

Scope is locked to: operating-disciplines.md new section, refusal-as-signal promotion, new credential-discipline skill, CAPTAIN envelopes for DAEDALUS/ADA/ARGUS/BARTLEBY, install.sh delta, railway-access skill deletion. No drive-by edits to other operating-disciplines sections, other CAPTAIN files, MAJOR_PLINY/MAJOR_POLYBIUS, templates, or app/. If DAEDALUS surfaces a scope concern (e.g., MAJOR_PLINY needs a cross-ref), file a follow-up ticket; don't expand this arc.

---

## Files Phase 2 ADA touches (anticipated; DAEDALUS finalizes)

1. `substrate/operating-disciplines.md` — append "Credential discipline" section + refusal-as-signal subsection (or peer section).
2. `substrate/skills/credential-discipline/SKILL.md` — NEW file.
3. `substrate/CAPTAIN_DAEDALUS_*.md` — envelope addition.
4. `substrate/CAPTAIN_ADA_*.md` — envelope addition.
5. `substrate/CAPTAIN_ARGUS_*.md` — envelope addition.
6. `substrate/CAPTAIN_BARTLEBY_*.md` — envelope addition.
7. `substrate/install.sh` — possibly: new skill entry. ADA confirms whether glob-discovery handles it automatically.
8. `~/.claude/skills/railway-access/SKILL.md` — DELETE (+ its directory if empty).

Estimated diff: ~300-500 net lines added across the 6-7 substrate files, plus the deletion. Small-to-medium arc.

---

## Cross-references

- `stoa--p5g` — work-unit ticket (THE spec; primary input)
- `railway_stoa/railway--r9z` — worked-example arc (CI workflow built + validated)
- `railway_stoa/railway--7r6` — workflow-tightening follow-up (NOT in Arc 25 scope; lives on railway_stoa)
- `railway_stoa/railway--dwc` — port-railway-access-skill ticket (close-post-arc-25, owned by user-tier POLYBIUS — NOT this arc)
- `ariadne-core-workspace/ariadne--u83` — 502 follow-up that surfaced Railway reference-resolution behavior (closed; referenced)
- `github.com/denson/sector-4/.github/workflows/deploy-dev-ariadne.yml` — canonical worked example
- `https://developer.1password.com/docs/cli/app-integration-security/` — context for why `op run` wrapper was rejected
- `https://www.anthropic.com/engineering/claude-code-sandboxing` — structural reference for proxy pattern (mentioned in `stoa--p5g` comment 2)

---

## What's NOT in this arc's scope

- HashiCorp Vault Cloud, 1Password Connect Server, per-machine cloud-vault setups — explicitly named NOT-substrate-default in `stoa--p5g` comment 2. Future patterns if scale ever justifies them, but NOT canonized in this arc.
- Modifying the railway--r9z deploy workflow (lives in denson/sector-4, not in the-stoa).
- Closing `railway--dwc` on railway_stoa (user-tier POLYBIUS does that post-arc).
- Re-evaluating Arc 24's heartbeat discipline or any prior arc's deliverables.
- Adding credential-discipline cross-refs to MAJOR_PLINY.md or MAJOR_POLYBIUS.md — out of scope unless DAEDALUS surfaces empirical justification AND files a follow-up ticket.

---

## Smoke beats (Phase 4)

1. `install.sh --dry-run` lists `substrate/skills/credential-discipline/SKILL.md` in the deploy manifest.
2. `grep -r "refusal-as-signal" substrate/operating-disciplines.md` → 1+ hits.
3. `grep -r "CI-mediated" substrate/CAPTAIN_DAEDALUS_*.md substrate/CAPTAIN_ADA_*.md substrate/CAPTAIN_ARGUS_*.md substrate/CAPTAIN_BARTLEBY_*.md` → 1+ hits per file.
4. `grep "agents NEVER" substrate/operating-disciplines.md` → at least one hit (the load-bearing universal rule should be present and emphatic).
5. `~/.claude/skills/railway-access/SKILL.md` no longer exists (delete confirmed).
6. New skill renders coherently when read end-to-end (CATO/ZENO already covered this; smoke is just a final eyeball).

PLINY runs the smoke beats themselves (no separate seat). PR opens. After clean PASS verdicts from all three verifiers, PLINY runs `gh pr merge`. `stoa--p5g` closes with reference to the merge commit + the arc directive.

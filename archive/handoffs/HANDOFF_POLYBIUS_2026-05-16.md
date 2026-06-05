# HANDOFF — POLYBIUS — 2026-05-16

**For:** the next user-tier POLYBIUS session resuming this multi-workspace engagement after compaction or session boundary.
**Author:** the user-tier POLYBIUS in this conversation, 2026-05-16 UTC.
**Supersedes:** `HANDOFF_POLYBIUS_2026-05-14.md` — most of its open threads are now resolved or evolved; cite-don't-restate.
**Authoring discipline:** `stoa--7e3` handoff-author principles — highest value-per-token first; indirection over inlining; cite memories don't restate; honor value/effort.

---

## ⚡ Live relay channel — read this first

**The 2026-05-16 user-tier POLYBIUS session that authored this handoff is being kept alive by PRINCIPAL** as a relay channel during your transition. PRINCIPAL's intent: if you (the next POLYBIUS) have questions where the original session's conversation transcript would be the fastest path to an answer, PRINCIPAL will relay your question to the prior session and relay the answer back.

What that prior session has in-context that this handoff does NOT fully capture:
- The full conversation transcript with PRINCIPAL across the 2026-05-15→2026-05-16 engagement (the railway--r9z workflow patches as they were made, the dev Ariadne 502 debugging trail at log-line resolution, the architectural-decision conversation that produced stoa--p5g's three locked comments, the Arc 25 dispatch-and-correction trail).
- In-context memory of which specific tool calls landed which specific outcomes.
- The "running-agent" pre-Arc-25 version of MAJOR_POLYBIUS.md (since the user-tier substrate was refreshed AFTER that session was already loaded).

**When to relay vs. when to just act:** if the answer is in this handoff or in any bw ticket, just act — that's the durable substrate. Only ask PRINCIPAL to relay when you suspect a conversational nuance not captured in bw is load-bearing for the next decision. The prior session will time out eventually; don't depend on it.

---

## Where things stand — one paragraph

The user-tier engagement of 2026-05-15→16 produced four landed deliverables: (1) a fresh dev Ariadne instance on Railway serving healthy responses at `https://ariadne-core-production-cd25.up.railway.app`, (2) a shipped CI deploy workflow at `denson/sector-4/.github/workflows/deploy-dev-ariadne.yml` validated end-to-end, (3) substrate canon for **credential discipline** (the-stoa main commit `50d70f2` — operating-disciplines.md §20 + the new `credential-discipline` substrate-tier skill + 4 CAPTAIN envelope updates + refusal-as-signal promoted to substrate canon + railway-access skill DELETED), and (4) user-tier substrate refreshed (~13 files updated; Arc 25 canon now active for every future user-tier session). The credential architecture is **GCP Secret Manager + GitHub Actions Workload Identity Federation + agents NEVER hold credentials** — see §20 for the five named anti-patterns and the universal rule. Sector-4 game team (s4--bbz) is unblocked on retrieval and ready to resume MVP build.

## What you'd most likely do next (recommendation, not prescription)

PRINCIPAL gave no specific direction at session-close — the engagement ended on a clean "call it." When PRINCIPAL re-engages, the menu is roughly:

1. **Resume sector-4 game build (s4--bbz)** — the original reason dev Ariadne was deployed. Sector-4 team is fully unblocked. PRINCIPAL drops into `C:\Users\denso\claude_projects\sector-4` with the PLINY paste to resume.
2. **Apply Arc-25 drift in consumer workspaces** — `railway--l7o`, `ariadne--kwo`, `s4--3jp` each carry a pointer ticket. Each consumer-workspace PLINY/POLYBIUS applies via the apply.sh consent walk on their next activation. Cheap; high-leverage (closes the meta-loop).
3. **Workflow tightening (railway--7r6)** — the `Verify DATABASE_URL_PRIVATE binding` step is too lenient (checks key presence, not resolved value). One-line jq fix to the deploy workflow. Tiny.
4. **Pick off an Arc-25 follow-up** — `stoa--3ml` (stale thesis line), `stoa--58b` (PLINY cross-ref to §20), `stoa--n2e` (POLYBIUS cross-ref to §20.3), `stoa--ezp` (pre-existing skills authorship audit), `stoa--6k1` (P10 spec refinement). All P3/P4. Small individually; could batch into a v2 mini-arc.
5. **stoa--bj5** (still open from prior handoff) — bring user-tier substrate into drift-check scope; v0 of the skill skips user-tier. This session had to manually diff user-tier drift; closing this gap means the next handoff doesn't need to.

## The credential discipline arc (Arc 25) — shipped, and what's open

**Shipped + propagated.** the-stoa main `50d70f2` ("arc-25: credential discipline as substrate canon (build)"); stoa--p5g CLOSED. Substrate canon now carries §20 "Credential discipline" (the canonical CI-mediated pattern + five named anti-patterns with shared root cause + universal rule), §20.3 refusal-as-signal as substrate canon (was a user-tier harness-rule), §20.4 preventive↔responsive boundary, §20.5 Railway empirical footnotes (reference variables resolve only at deploy-time; `railway run --service` does NOT exec inside container). New substrate-tier skill at `substrate/skills/credential-discipline/SKILL.md` (gcloud WIF + GitHub Actions YAML pinned at @v3, sector-4 worked-example pointer). Four CAPTAIN envelope additions (DAEDALUS §6.6 / ADA §5.7 / ARGUS §6.8 / BARTLEBY §6.7 + `credential_leak` verdict tag).

**Open follow-ups:**
- **the-stoa:** `stoa--3ml` (P4, thesis line), `stoa--58b` (P3, PLINY cross-ref), `stoa--n2e` (P3, POLYBIUS cross-ref), `stoa--ezp` (P4, skills authorship audit), `stoa--6k1` (P4, P10 spec refinement), `stoa--myd` (P4, N=1 multi-checker accretion — future arcs add evidence per §6.7.1 three-condition gate).
- **railway_stoa:** `railway--l7o` (P3, Arc-25 drift apply), `railway--7r6` (P2, workflow tightening).
- **ariadne-core-workspace:** `ariadne--kwo` (P3, Arc-25 drift apply).
- **sector-4:** `s4--3jp` (P3, Arc-25 drift apply).

**Already closed (cross-workspace owned by user-tier):**
- `railway--dwc` (port-railway-access-skill) — obviated by §20; closed with cross-ref.
- The user-tier `~/.claude/skills/railway-access/` skill — DELETED by ADA per Arc 25 A8.

## The dev Ariadne deployment (railway--r9z + ariadne--u83) — shipped

**Dev Ariadne URL:** `https://ariadne-core-production-cd25.up.railway.app`
- `/api/health` returns `{"status":"healthy","version":"0.1.0","commit":"4870c7e","engine":"markitdown","embedding_enabled":true}`
- `/.well-known/ariadne-config` returns Auth0 issuer/client_id/audience (OIDC discovery wired)
- Embedding pipeline: ON (Gemini, 1536 dimensions)
- Volume: `/data/bw-repos` attached (empty; sector-4 seeds as part of narrative+corpus phase)
- Auto-deploys from main of `github.com/denson/ariadne-core` (same image as prod)

**The 502 root-cause story** (ariadne--u83, CLOSED): ariadne-core's `DATABASE_URL_PRIVATE` Railway-reference was malformed as `${{Postgres.DATABASE}}` (missing `_URL`); resolved to empty string; psycopg pool tried Unix socket fallback; PoolTimeout. Fix: change reference to `${{Postgres.DATABASE_URL}}`. Diagnosis-and-fix took ~6 turns from log-read to healthy response.

## The CI deploy workflow (railway--r9z) — shipped

Lives at `denson/sector-4/.github/workflows/deploy-dev-ariadne.yml` (~564 lines, HEAD `c65d8d4`). Validated end-to-end (run `25956772075`). Architecture: WIF auth → fetch 6 secrets from GCP Secret Manager → set them on ariadne-core Railway service → trigger redeploy → wait for SUCCESS → smoke test `/api/health` + `/.well-known/ariadne-config`. **Note:** smoke step caught the 502 at first run — the workflow is doing its job; the bug was config not workflow.

**6 patches landed during first-runs** (caught by user-tier POLYBIUS as VERA-on-real-runner; the railway_stoa team's static review missed them): YAML expression escape, `| sh` → `| bash`, PATH propagation, `RAILWAY_TOKEN` → `RAILWAY_API_TOKEN`, jq loosening for null reference values, self-inflicted `${{...}}` in comment. Full trail in railway--r9z bw.

**Follow-ups:**
- `railway--7r6` (P2) — assert resolved value in verify step
- `railway--prn` (P3) — bump google-github-actions/auth + get-secretmanager-secrets v2→v3 (now warning-deprecated)

## Where the bw repos live

| Repo | Local path | bw prefix | Last-arc commit |
|---|---|---|---|
| **the-stoa** | `C:\Users\denso\claude_projects\the-stoa\` | `stoa--` | `50d70f2` (Arc 25 + drift apply ahead) |
| **ariadne-core-workspace** | `C:\Users\denso\claude_projects\ariadne-core-workspace\` | `ariadne--` | (drift behind 50d70f2; apply via ariadne--kwo) |
| **beadwork-demo-aresense** | `C:\Users\denso\claude_projects\beadwork-demo-aresense\` | `aresense-` (SINGLE-dash) | NOT-STOA-DEPLOYED (no role files; only skills) |
| **railway_stoa** | `C:\Users\denso\claude_projects\railway_stoa\` | `railway--` | (drift behind 50d70f2; apply via railway--l7o) |
| **sector-4** | `C:\Users\denso\claude_projects\sector-4\` | `s4--` | (drift behind 50d70f2; apply via s4--3jp) |
| **user-beadwork** | `C:\Users\denso\claude_projects\user-beadwork\` | `u--` | (user-tier substrate; refreshed 2026-05-16) |
| **beadwork-skills** | `C:\Users\denso\claude_projects\beadwork-skills\` | n/a | (sibling, no bw) |

`sector-4` is **new since the 2026-05-14 handoff** — it was created mid-engagement for the Sector 4 Lockdown game demo. Its team (project-tier POLYBIUS + PLINY) has been paused during the credential-discipline thread; unblocked now.

## Auth + credential state — UPDATED ARCHITECTURE (read carefully)

**This is the biggest delta from the 2026-05-14 handoff.** The prior handoff's credential-state advice (`.railway_token_cache` on disk, `op` per-call, parent-shell-env) is now CATEGORICALLY REJECTED as named anti-patterns in operating-disciplines.md §20. The canonical pattern is now:

- **For deploys + cloud-API work (Railway, GCP, embedding APIs):** CI-mediated only. Agent authors the GitHub Actions workflow; CI runs it. WIF for GCP-native (no static keys); GitHub Actions encrypted secrets for PAT-only services like Railway. No agent-side credentials. Period.
- **Secrets manager:** GCP Secret Manager in project `gen-lang-client-0086715174` (consolidated — also hosts prod Gemini API key). 6 secrets live there for Ariadne: `ariadne-dev-embedding-api-key`, `ariadne-dev-image-enrichment-api-key`, `ariadne-dev-upload-signing-secret`, `ariadne-dev-auth0-domain`, `ariadne-dev-auth0-client-id`, `ariadne-dev-auth0-audience`. All version 2 (PRINCIPAL destroyed v1s during setup).
- **WIF provider:** `projects/831054054648/locations/global/workloadIdentityPools/github/providers/github-oidc` (configured for denson/sector-4 repo).
- **GH service account:** `github-actions-secret-reader@gen-lang-client-0086715174.iam.gserviceaccount.com` (Secret Manager Secret Accessor role, scoped).
- **Railway API token:** account-scoped, stored as `RAILWAY_API_TOKEN` GitHub Actions secret in denson/sector-4. CLI calls use `--project/--environment/--service` flags.

**The `ariadne` CLI auth state** noted in the prior handoff is stale by ~24h — re-derive if needed (`ariadne login --host https://ariadne-core-production.up.railway.app`). The CLI is still stale (predates uuo-3/4) per `ariadne--k3c`; for ariadne API work, use raw API via curl/httpx — but that's a sector-4-team concern, not POLYBIUS.

## State that shapes POLYBIUS behavior

- **The credential-discipline canon is now load-bearing.** When any future engagement involves credentialed third-party API calls, §20 is the authoritative reference. The `credential-discipline` skill auto-triggers on relevant requests (deploy, authenticate, set up CI, rotate token, etc.). Cross-reference to it in any dispatch brief that touches credentialed ops.
- **The check-for-changes-above pattern (MAJOR_POLYBIUS.md §14)** continues to be a soft nudge. Arc 25's drift sweep was triggered manually — if it had been auto-triggered on activation, this would be a tighter loop. `stoa--bj5` is the work to close that.
- **Sector-4 workspace is a `sector-4` not `sector_4`** — bw prefix is `s4--`. Initial creation had a `s4-` (single-dash) error; re-init with `--prefix s4-` gave the correct `s4--xyz` IDs. Don't repeat that.
- **The discipline of authoring directives BEFORE dispatching is paying off.** Arc 25 PLINY ran heads-down with locked A-decisions for ~15 min wall-clock end-to-end. The investment in directive-authoring is the load-bearing reason gauntlet arcs are fast.

## Memories that shape POLYBIUS — cite, don't duplicate

Load-bearing this session (in `~/.claude/CLAUDE.md` + project `MEMORY.md`):
- *Provide pastes proactively* — restate prompts in code-block form, don't expect PRINCIPAL recall.
- *Long dispositions via bw, not paste-relay* — the lesson PRINCIPAL re-surfaced mid-engagement (I had over-stuffed an initial PLINY paste; lean version + bw drift content was the fix).
- *Agents merge PRs in ariadne workspace* — PLINY/CAPTAINs run `gh pr merge`, not PRINCIPAL clicking. Arc 25's PLINY did exactly this.
- *User-tier approves technical-tier decisions itself* — only project-direction calls go to PRINCIPAL; technical-tier dispositions are user-tier's job. Followed throughout this engagement.
- *No agent-fatigue framing* — never recommend pausing "because of lot of work today." Engagement closed on clean substantive ground, not fatigue.
- *Tell agents what to use, not what not to use* — directive-authoring discipline.
- *Session-state continuum for sequential dispatches* — leaving this session running for relay is exactly this pattern.
- *Discord channel monitor project* — paused indefinitely; not relevant.

These are durable canon — go to memory not to this doc.

## Hygiene loose ends

- **One A3 directive inaccuracy** (refusal-as-signal source-location): the Arc 25 directive's A3 said refusal-as-signal "currently lives in `~/.claude/CLAUDE.md` as a harness-rule." PLINY's standdown noted this was incorrect (the rule's actual source location differs). Not blocking — Arc 25 still landed the right canon. Worth a note for next-arc directive-template review.
- **Running-agent caveat:** the user-tier substrate refresh wrote new files to `~/.claude/` AFTER the 2026-05-16 POLYBIUS session loaded its role file. That session is operating on pre-Arc-25 MAJOR_POLYBIUS.md in-context. Your fresh session inherits the post-Arc-25 version automatically — no action needed.
- **The drift-application work in consumer workspaces** is queued via the three pointer tickets (railway--l7o, ariadne--kwo, s4--3jp). Each consumer workspace's PLINY applies. If those workspaces don't activate for a while, the drift compounds with future arcs.
- **stoa--bj5** (user-tier in drift-check scope) — still open from 2026-05-14 handoff. The manual-diff workaround used this session highlighted the cost of not closing it.

## Honest caveats

- **Curated, not exhaustive.** The conversation transcript that produced this handoff carries diagnostic-level detail (which log lines surfaced which root causes, which exact tool-call patches fixed which workflow steps, the per-turn dispatch-and-correction trail). The durable substance is in: bw tickets (especially stoa--p5g, ariadne--u83, railway--r9z, the arc-25 directive at substrate/arcs/arc-25-build-directive.md), the operating-disciplines.md §20, and the credential-discipline skill. Go there, not to memory.
- **The Arc 25 TIMING_LOG at commit 49b1dd5** is a structured retrospective from the-stoa POLYBIUS — read it for the gauntlet-shape insights (estimate-vs-actual + 5 observations + 4-way convergence finding on P10). Higher signal than a generic "how did it go" question.
- **PRINCIPAL chose autonomous-but-relay for the standdown.** This is the session-state continuum at "leave intact" — prior session preserved as relay channel rather than terminated. When PRINCIPAL stops needing the relay, prior session times out organically. Don't ask PRINCIPAL to "shut it down" — that's not the pattern.

End handoff.

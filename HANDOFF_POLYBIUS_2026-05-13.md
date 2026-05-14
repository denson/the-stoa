# HANDOFF — POLYBIUS — 2026-05-13

**For:** the next POLYBIUS session resuming this multi-workspace engagement after compaction.
**Author:** the POLYBIUS in this conversation, 2026-05-13 evening UTC.
**Authoring discipline:** stoa--7e3 handoff-author principles applied (highest value-per-token first; indirection over inlining; cite memories don't restate; honor value/effort).

---

## What you were in the middle of when I wrote this

**Immediate next action — pending PRINCIPAL ratification:** wipe the Railway pgvector DB. PRINCIPAL said "we can clear the db" because the existing 16624 chunks / 5502 docs / 24 collections in pgvector are stale prior-iteration content (PRINCIPAL called it "Conan stuff"). I drafted the SQL but did NOT yet execute. The SQL is:

```sql
BEGIN;
TRUNCATE TABLE chunks, documents, collections, search_log, document_interactions
    RESTART IDENTITY CASCADE;
SELECT (SELECT count(*) FROM chunks), (SELECT count(*) FROM documents),
       (SELECT count(*) FROM api_keys) AS preserved;
COMMIT;
```

Tables to PRESERVE: `api_keys` (empty anyway — Auth0 validates JWTs at runtime), `schema_migrations` (3 rows), `jobs` (0), `bw_ingest_retry_*` (both 0).

**After the wipe, open question:** how to trigger re-ingest of the 417-ticket bw substrate now living at `/data/bw-repos/aresense` on Railway. Three candidate paths I sketched but didn't investigate:
- A. Restart ariadne-core service (if startup scans bw, auto-reingests) — risk: ~1-2 min downtime
- B. Find/use a `/api/bw/projects/<slug>/reingest-all` endpoint if it exists (need to check Ariadne source)
- C. Manually walk 417 tickets via API (last resort)

**PRINCIPAL is making the wipe + re-ingest call**, not POLYBIUS. Surface the plan again when resuming.

---

## Where the 4 bw repos live (per PRINCIPAL ask 2026-05-13 evening)

Each repo also has a `[REMINDER] Local clone path` ticket filed in its own bw substrate today; the IDs are noted below for in-repo lookup.

| Repo | Local path | bw prefix | Reminder ticket |
|---|---|---|---|
| **the-stoa** | `C:\Users\denso\claude_projects\the-stoa\` | `stoa--` | `stoa--i6c` |
| **ariadne-core-workspace** (private; nested public `ariadne-core/` inside) | `C:\Users\denso\claude_projects\ariadne-core-workspace\` | `ariadne--` | `ariadne--4vm` |
| **beadwork-demo-aresense** (factory demo + corpus) | `C:\Users\denso\claude_projects\beadwork-demo-aresense\` | `aresense-` (SINGLE-dash) | `aresense-z7r` |
| **railway_stoa** | `C:\Users\denso\claude_projects\railway_stoa\` | `railway--` | `railway--fbi` |

`user-beadwork` (`C:\Users\denso\claude_projects\user-beadwork\`) also exists — user-tier substrate; haven't worked in it this session.

---

## 1Password friction mitigation (active in this session)

PRINCIPAL flagged the per-session 1Password unlock as friction. I cached the Railway token to disk for this session:

- File: `C:/Users/denso/.railway_token_cache` (mode 600)
- Use: `export RAILWAY_API_TOKEN=$(cat C:/Users/denso/.railway_token_cache)` before any `railway` CLI call
- Risk: token-on-disk in plaintext. Acceptable for short session use; **delete at session end** or re-create per-session
- Permanent fix (queued discussion): OS keyring or service-account, captured as agent-credentials architectural concern in `RAILWAY_KNOWLEDGE.md` Part 7 #6 (in railway_stoa)

---

## Just-shipped this session (high-level — read source for detail)

| Work | Where | Anchor |
|---|---|---|
| Arc 23 + Arc 24 substrate canon | the-stoa main | merge commits `1ff9f3f`, `16146a4`; TIMING_LOGs at `7ecdbef`, `b527bc1` |
| Five Arc 25+ substrate-canon tickets filed (handoff-author skill, two-team pattern, memory-as-alignment, multi-team interop, operating-mode progression) | the-stoa bw | `stoa--7e3, 86k, wad, kt6, ntn` (all P2) |
| railway_stoa workspace created + initialized | github.com/denson/railway_stoa (private) | initial commit + 4 seed tickets |
| beadwork-demo-aresense made public + GitHub remote pushed | github.com/denson/beadwork-demo-aresense (public) | main + beadwork branch live on origin |
| Factory-demo content migrated from ariadne-core to beadwork-demo-aresense | both repos | beadwork-demo-aresense `cb76b59`; ariadne-core scrub `229d23f` |
| Railway-side aresense slug created at `/data/bw-repos/aresense` with persistent volume | Railway production | volume attach + bw init done; corpus fetched via beadwork-branch fetch |
| Railway corpus verified clean of Conan content | Railway pgvector + bw | word-boundary regex grep returned 0 matches both sides |

---

## Substrate queue going into Arc 25+ (cite, don't restate)

All open substrate tickets in the-stoa bw — see each via `bw show <id>` for detail:

**Arc 25 candidate bundle (substrate-canon for deployment + identity model):**
- `stoa--7e3` handoff-author skill (THE skill for making this kind of doc canonical — would deploy the 6 principles I'm using right now)
- `stoa--86k` two-team-per-project deployment pattern
- `stoa--wad` memory as user-alignment layer
- `stoa--kt6` multi-team interoperation pattern
- `stoa--ntn` operating-mode progression (pair-programming → full-team → semi-autonomous)

**Smaller follow-ups (P3, ride along):**
- `stoa--3sz`, `stoa--dhc`, `stoa--5sr` — Arc 24 follow-ups (probe-spec, python-vs-jq SSOT, Edit-tool worktree-path)
- `stoa--53u` idle-state retrospective-narrative confabulation (P2 — distinct subtype from stoa--ioy)
- `stoa--tvc` bw-fit matrix extension (descendant→ancestor blocks; aresense seeder empirical anchor)
- `stoa--ezj` probe PRINCIPAL-intent + probe CATEGORY before OPTIONS
- `stoa--gq1` substrate-component design principles (agent-installable distribution + composability)

**Parked (separate themes):**
- `stoa--jru` Arc 22 epic + `stoa--cgn` + `stoa--e39` (coordination hygiene)
- `stoa--vz9` epic (op-disc promotion)
- `stoa--kjo` epic (per-agent git identity)

---

## Key conversational decisions you should know about

- **Ariadne-core stays generic; demos live in their own repos.** PRINCIPAL framed: "factory demo is just ariadne with a particular set of agents/skills/tools that turn it into a game. We can just as easily turn a deployment into a real system for helping run a real factory or many other types of tasks." Pattern: `<substrate>-demo-<domain>` for future demos.

- **Stoa = forge; project teams are deployed FROM Stoa**, specialized by their files + tools + memories at deployment time, NOT by core role-file rewrites. Don't extend core CAPTAIN role files with project-specific content. (Earlier I made this mistake; PRINCIPAL corrected; closed wrong-shaped tickets stoa--jwj, stoa--0nt, stoa--t7r, stoa--0tr.)

- **Memory is the user-alignment layer.** Don't try to normalize memories across users; per-user accumulation is the alignment mechanism working correctly. (`stoa--wad` substrate-canon ticket.)

- **Confabulation discipline applies to POLYBIUS too** — the "discipline cluster" stoa--ioy/nvl/53u/ezj + MCP-confabulation subtype caught me multiple times this session (substrate-feature pollution in nvl, "pre-record" framing, X-tracker-as-Anthropic, demo-shape options that missed the right category). Apply rigorously.

- **Parked Railway projects are not abandoned.** Don't propose deletion of the 7 default-named Railway projects (pleasant-enthusiasm, cozy-curiosity, etc.) — PRINCIPAL convention is hands-off.

---

## Memories that shape POLYBIUS behavior (cite, don't duplicate)

The user-tier `~/.claude/CLAUDE.md` + the project memory index at `C:\Users\denso\.claude\projects\C--Users-denso-claude-projects\memory\MEMORY.md` carry standing disciplines. Load-bearing for THIS session's work pattern:

- "Provide pastes proactively"
- "Agents merge PRs in ariadne workspace"
- "User-tier approves technical-tier decisions itself"
- "Long dispositions via bw, not paste-relay"
- "No agent-fatigue framing"
- "Tell agents what to use, not what not to use"

Don't restate these here; they're in the durable canon. Just know they're load-bearing.

---

## What I would do next session (recommendation, not prescription)

1. **Resume the Railway DB wipe + re-ingest discussion** with PRINCIPAL. The wipe SQL is drafted; the re-ingest mechanism is unknown. Sequence: confirm wipe, execute, then investigate re-ingest mechanism.
2. **Once corpus is re-ingested**: drive Q1 query against the deployment to verify end-to-end flow works.
3. **Then**: factory-demo skill body refinement against the Q1-Q4 actual-execution learnings. The skill body in beadwork-demo-aresense/.claude/skills/factory-demo-walkthrough/ may need updates based on what actually surfaces from queries.

Defer: Arc 25 dispatch (substrate-canon tickets are ready; just need PRINCIPAL nod to author the directive). Defer: railway_stoa specialist-team work (PRINCIPAL hasn't surfaced specific Railway pain to specialize against beyond the credential-friction concern).

---

## Honest caveats on this handoff

- **It's curated, not exhaustive.** I left out a lot of conversational nuance (operating-mode discussions, the SendMessage gap investigation, the various confabulation corrections). Those live in this conversation's transcript (which won't survive compaction); the substrate canon captures the durable lessons. If the next session wants more nuance, ask PRINCIPAL.
- **The "next action" framing assumes PRINCIPAL is still in the loop.** If you're resuming with no PRINCIPAL input, surface the wipe-pending state to PRINCIPAL before doing anything destructive.
- **The handoff-author skill (stoa--7e3) is queued but not deployed.** If a future PLINY-stoa session ships Arc 25 bundling stoa--7e3, the canonical skill exists and the next handoff is more procedural. Until then, handoffs are authored ad-hoc applying the principles manually (as this one was).

End handoff.

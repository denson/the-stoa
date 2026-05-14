# HANDOFF — POLYBIUS — 2026-05-14

**For:** the next POLYBIUS session resuming this multi-workspace engagement after compaction.
**Author:** the POLYBIUS in this conversation, 2026-05-14 UTC.
**Supersedes:** `HANDOFF_POLYBIUS_2026-05-13.md` — its entire open thread (wipe Railway pgvector + figure out re-ingest) is **fully resolved**; it became the `ariadne--uuo` arc.
**Authoring discipline:** `stoa--7e3` handoff-author principles — highest value-per-token first; indirection over inlining; cite memories don't restate; honor value/effort.

---

## Where things stand — one paragraph

The 05-13 handoff's open thread is done. It turned into the **`ariadne--uuo` arc**: the bw-ingest pipeline now embeds clean content (no YAML-metadata pollution) and has an in-place `/reembed` mechanism. That arc is **shipped** (ariadne-core `cc851ef`), the production `aresense` corpus is **migrated** (857 YAML-pollution chunks → 0), and the **factory demo is re-runnable on a clean corpus**. Separately this session: the SendMessage-phantom gap was fixed in substrate canon, and a substrate-drift sweep found + closed staleness in every tier. All substrate is current.

## What you'd most likely do next (recommendation, not prescription)

PRINCIPAL was given this menu and chose "refresh the handoff" first — **the direction call is still open. Surface the menu again when you resume.**

1. **Re-run the factory demo end-to-end** *(recommended)* — it's the payoff of the whole `uuo` arc. PRINCIPAL started it long ago, hit the Beat-1 YAML wall, and everything since fixed that. Finally testable. Also yields real data on whether `ariadne--15q` (chunk-clustering) degrades the demo in practice. Trigger: open `beadwork-demo-aresense`, invoke `factory-demo-walkthrough`.
2. **Dispatch the ariadne team on the `uuo` follow-ups** — `ariadne--15q` (chunk-clustering, P2) is the meatiest.
3. **Arc 25** — the substrate-canon bundle (`stoa--7e3` handoff-author skill, `86k`, `wad`, `kt6`, `ntn`) has been queued + ready since 05-13; needs the arc directive authored + PRINCIPAL nod.

## The `ariadne--uuo` arc — shipped, and what's open

**Shipped + migrated.** PR-A (uuo-1/2/5) + PR-B (uuo-3/4) merged at ariadne-core `cc851ef`; full `aresense` corpus re-embedded. Gates 1 (pollution removed) + 2 (metadata surfaced) PASS; gate 3 (no-regression) FAILED on beat2 (H2+H6 decision ticket dropped rank 1→3 via uuo-2 contextual-header chunk-clustering) — PRINCIPAL dispositioned accept-with-follow-up. **Full picture: `ariadne-core-workspace/agents/verification/ariadne--uuo/validation.md`** — read it, don't re-derive.

**Open follow-ups (ariadne-core-workspace bw):**
- `ariadne--15q` — uuo-2 chunk-clustering / result-diversity collapse (P2; DAEDALUS design question — diversification vs. rethink the header)
- `ariadne--629` — `documents.metadata.labels` empty in `/api/search` results; pre-existing, **demo-affecting** (Beat 2 depends on labels) (P3)
- `ariadne--k3c` — ariadne-core-client republish: uuo-3/4 merged but not on PyPI → installed CLI is stale (P3)
- `ariadne--uav` — design §6.4 "fingerprint stable" prose doc-sync (P3)
- `ariadne--rb3` — `test_smoke_beats.py` CWD-dependent skip (P4)

## SendMessage phantom + substrate drift — fixed this session

- **SendMessage is a phantom here.** Real Claude Code "Agent Teams" tool, gated behind `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` (off). The `Agent` tool description + every agent-return footer reference it anyway. Canon now covers it: `operating-disciplines.md §18.6` + `MAJOR_PLINY.md §5.8.2/§5.8.7`. **You will see the footer — ignore it.** Agents are stateless; continuity = bw + on-disk artifacts + self-contained cold-pickup briefs.
- **Substrate drift sweep.** Found + re-synced: ariadne-core-workspace (~2 arcs stale), the-stoa's own `.claude/` (~20 arcs stale), user-tier `~/.claude/` (2 sections stale). **All current now.** the-stoa HEAD ≈ `a6bc8c3`. The `check-substrate-updates` skill works (exercised 4× this session); `.substrate-last-check` baselines grounded in consumer workspaces. Open: `stoa--bj5` — user-tier isn't yet in the drift-check scope.

## Where the bw repos live

| Repo | Local path | bw prefix | Local-path reminder ticket |
|---|---|---|---|
| **the-stoa** | `C:\Users\denso\claude_projects\the-stoa\` | `stoa--` | `stoa--i6c` |
| **ariadne-core-workspace** | `C:\Users\denso\claude_projects\ariadne-core-workspace\` | `ariadne--` | `ariadne--4vm` |
| **beadwork-demo-aresense** | `C:\Users\denso\claude_projects\beadwork-demo-aresense\` | `aresense-` (SINGLE-dash) | `aresense-z7r` |
| **railway_stoa** | `C:\Users\denso\claude_projects\railway_stoa\` | `railway--` | `railway--fbi` |

`user-beadwork` (`C:\Users\denso\claude_projects\user-beadwork\`, prefix `u--`) — user-tier substrate.
**Changes since 05-13:** `beadwork-skills` moved OUT of ariadne-core-workspace to its own sibling (`C:\Users\denso\claude_projects\beadwork-skills\`); `bw-skills` deleted (archived graveyard, fully on private GitHub).

## Auth + credential state

- **`ariadne` CLI** — authed as densonsmith2@gmail.com, token expires **~2026-05-15 05:50 UTC**. Re-auth: `ariadne login --host https://ariadne-core-production.up.railway.app` (browser flow — POLYBIUS runs the command, PRINCIPAL completes the Google sign-in).
- **Railway** — token cached at `C:/Users/denso/.railway_token_cache` (mode 600, plaintext — delete or re-create per session). `export RAILWAY_API_TOKEN=$(cat ...)` before `railway` CLI calls.
- **The `ariadne` CLI is stale** (predates uuo-3/4). For ariadne API work, use the **raw API via curl/httpx** — token via `ariadne_core_client.auth.get_access_token(host)`, bootstrap path `ariadne-core/client/src`. Tracked: `ariadne--k3c`.

## State that shapes POLYBIUS behavior

- The check-for-changes-above pattern is **operational** — but it's a soft nudge (`MAJOR_POLYBIUS.md §14`: read `.substrate-last-check` on activation). If drift recurs despite §14 being deployed, that's the signal it needs harder enforcement.
- Ariadne-core stays generic; the factory demo lives in `beadwork-demo-aresense`. `uuo` touched the generic ingest pipeline, not the demo.
- The factory demo's **"create a memory" capstone beat** (PRINCIPAL wants the user to create a memory = a ticket, demonstrating create-and-ingest) was proposed but never built — pending demo-design work.

## Memories that shape POLYBIUS — cite, don't duplicate

Load-bearing this session (in `~/.claude/CLAUDE.md` + project `MEMORY.md`): *Provide pastes proactively · Agents merge PRs in ariadne workspace · User-tier approves technical-tier decisions itself · Long dispositions via bw not paste-relay · No agent-fatigue framing · Tell agents what to use not what not to use.* They're durable canon — don't restate.

## Hygiene loose ends

- `.railway_token_cache` on disk — delete at session end per the credential discipline.
- 5 stale worktrees in `ariadne-core-workspace/.claude/worktrees/` (now gitignored) — `git worktree prune` candidates; `lucid-lalande-b1801f` held the `uuo` design work, now done.

## Honest caveats

- **Curated, not exhaustive.** The conversational nuance (SendMessage diagnostic detail, the drift-discovery sequence, the `uuo` gauntlet rounds) lives in this conversation's transcript, which won't survive compaction. The bw tickets + `validation.md` + the canon carry the durable substance — go there, not to memory.
- The "what's next" direction call is genuinely open — PRINCIPAL deferred it to refresh this handoff. Re-surface the menu above.

End handoff.

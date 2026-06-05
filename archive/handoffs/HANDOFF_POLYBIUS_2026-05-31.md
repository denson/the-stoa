# HANDOFF — user-tier POLYBIUS — 2026-05-31 (→ 2026-06-01 UTC)

## In flight (read first)

- **Dynamic-workflows adoption program (the session's headline thread).** We evaluated Anthropic's **dynamic workflows** (research-preview feature; the `Workflow` tool + `/deep-research` bundled example) against the gauntlet and concluded: workflows do NOT replace the gauntlet — they are an *execution substrate* for its methodology. Prototyped + battle-tested it live. Durable home: **`stoa--04n`** (workflow-composer skill forge-promotion, design ready). The skill draft is UNCOMMITTED at `substrate/skills/workflow-composer/SKILL.md`; Stage-A design at `agents/design/stoa--04n/design.md`. **Next session decision:** whether to forge-harden the skill (`stoa--04n`, an arc) and/or run the real `/gauntlet` as a workflow battle-test.
- **Arc 52 (threat-defeat prevention) = SHIPPED + MERGED** this session (cc4b3e6 + d8e1f13). Epic **`stoa--yfv`** stays OPEN for **Arc B (detection)**. Next session may dispatch Arc B when PRINCIPAL wants it — now verified by an Arc-A-hardened gauntlet.

## Just closed

- **Arc 52 ARC A (threat-defeat prevention)** — merged `cc4b3e6` (4-file substrate change, A1–A4 prevention layer binding security mitigations to named threats before build; pure-additive 228 ins) + `d8e1f13` (deploy self-apply: NOMOS envelope + `.claude/` sync). Full 3-tier gauntlet (user-tier POLYBIUS close-gate ← floor-manager ← PLINY_the-stoa); 3 design revs; my close-gate re-ran NOMOS's 4 probes independently + threat-vs-implementation alignment, PASS; PRINCIPAL ship-go. Source: `u--ith` + `u--tgc` (origindex-trw incident) in user-beadwork.
- **`stoa--zep`** (NOMOS deploy-gap — the gauntlet found one of its OWN verify seats undeployed here) → CLOSED; NOMOS now deployed (12 envelopes, collision-free, dispatchable next session).
- **ksge battle-test PASS settled** — `stoa--q3l` CLOSED; actionable punch-list preserved as epic **`stoa--7b1`** (7 children; D5/D6 cross-linked to `stoa--wq0`). PRINCIPAL confirmed the substrate's been in real use since the test.
- **3 N=1 accretion tickets filed** from the workflows thread: **`stoa--q36`** (workflows execute direction, never set it), **`stoa--ilt`** (review-surface as general principle), **`stoa--aox`** (mechanical discipline-enforcement spectrum — deterministic gate / checker-agent / schema-field). NOTE: `stoa--aox` is now N=2 — `u--ith` #5 (threat-coverage verdict assertion) independently arrived at its tier-iii schema-field; cross-linked.

## Open decisions for next session

1. **Arc B (detection)** dispatch — `stoa--yfv` children `.1`(#5 verdict threat-coverage assertion — ties to `stoa--aox`), `.2`(#4 probes), `.5`(#6 close-gate re-derivation), `.6`(#7 culture). Prevention-before-detection lock satisfied; Arc B is now unblocked.
2. **`stoa--04n`** workflow-composer forge-promotion (an arc per §18.2) — or keep prototyping the real `/gauntlet` workflow first. The roadmap (Phases 1–5) is in the strategy doc below.
3. **`stoa--7b1`** ksge calibration — two P2 recurrence-class items (`.1` ARGUS §4/§7 coherence, `.2` save-verdict `.gitignore`) are the fix-now priorities.

## Load-bearing context (cite, don't duplicate)

- **Strategy doc:** `docs/sessions/2026-05-30-stoa-workflows-integration-strategy.md` — the full Stoa+workflows hybrid plan: 3-layer model (inner gauntlet / discipline-enforcement / outer loop), the task-shape taxonomy (coding + non-coding), phased roadmap, guardrails. READ THIS FIRST for the workflows thread.
- **External-review packet:** `docs/sessions/2026-05-31-threat-defeat-directive-external-review-packet.md` — the §5.4 cold-review that caught Arc 52's keystone inversion (it's reusable as a worked example of external directive review).
- **New canon shipped this session:** `operating-disciplines.md` §35 (threat-defeat prevention) + `MAJOR_PLINY.md` §5.13 (A1 pre-ADA ratification-restatement beat) + `CAPTAIN_DAEDALUS.md` §3/§6.12 + `CAPTAIN_ARGUS.md` §6.9.
- **Memory (NEW this session):** `feedback-ticket-ids-need-human-descriptions.md` — bare bw IDs are agent-facing; always surface as `<id> (plain description)` to PRINCIPAL. Applies to every human-facing surface.

## Non-obvious state

- **Uncommitted working-tree (deliberate, NOT lost):** `substrate/skills/workflow-composer/` (skill prototype — ships via its own `stoa--04n` arc, not direct-commit per §18.2); `agents/design/stoa--04n/`; the two `docs/sessions/*.md` (committable §18.1 housekeeping whenever); arc-process verdict artifacts under `agents/verdicts|verification|save-verdict/` (untracked by design).
- **Arc 52 close-out complete:** worktree `arc-52-build` removed, branch `arc-52/build` deleted, pastes archived to `docs/archived-pastes/`, my close-gate Monitor (cron `d7eaaf6f`) torn down. NO active crons.
- **3-tier gauntlet was novel for the-stoa** this arc (prior arcs ran 2-tier). The floor-manager seat gave author≠close-gate independence — worth repeating for canon-touching arcs. Activation pastes for that pattern are the archived `docs/archived-pastes/HUMAN_paste-*-arc-52-*.md` (template basis for future 3-tier arcs).
- **lost-voice deploy:** PRINCIPAL was deploying a fresh Stoa team to the lost-voice project via `install.sh` in parallel — independent repo, cleared as safe (current battle-tested substrate; nothing from this session's prototypes leaks into a fresh deploy).
- **Recurring Windows bug:** `stoa--wq0` (save-verdict heredoc/apostrophe + `/tmp`) recurred during Arc 52 (ARGUS verdict authoring); already logged, post-arc fix.
- **main HEAD = `d8e1f13`**, synced with origin/main.

## Generational lineage

Prior session id: `990b0750-5572-4836-b9c7-18d626a12e96`. Successor: a **fresh session + bare "polybius" activation is likely preferred** — this is a clean engagement boundary (Arc 52 shipped + closed, no mid-arc state to preserve). `claude --resume 990b0750-5572-4836-b9c7-18d626a12e96` is available if the successor wants this session's in-context nuance (e.g. the workflows-exploration reasoning that isn't fully in the strategy doc), but the durable substrate (strategy doc + bw tickets + new canon) carries the load-bearing state. Decay-not-termination per §16.2 Mode 3 — this session can stay open as a relay channel during the transition if the successor has questions.

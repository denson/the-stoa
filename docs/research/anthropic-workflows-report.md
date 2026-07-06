# Anthropic Workflows — how they work + best practices in Claude Code desktop

**Report to:** Denson Smith (PRINCIPAL)
**From:** Polybius_the_Stoa (user-tier)
**Date:** 2026-07-05
**Why this exists:** you flagged that "the pattern to make things deterministic is with anthropic workflows — they are new." This is the research you asked for. Web-verified via gsearch 2026-07-05 (sources at the bottom); mechanics cross-checked against the Claude Code Workflow tool spec I run under (primary source, authoritative for the desktop feature's exact API).

---

## TL;DR (read this first)

"Anthropic workflows" is **two things wearing one name**, and the distinction is the whole ballgame for us:

1. **The design pattern** — from Anthropic's *Building Effective Agents* (the canonical "workflows vs. agents" split). A **workflow** is a system where the LLM and tools are orchestrated through **predefined code paths** the developer writes. An **agent** is a system where the LLM **dynamically directs its own** process. Workflows trade autonomy for **predictability, low latency, low cost, and easy debugging.**

2. **The Claude Code feature** — the desktop/CLI now ships a native **Workflow** primitive that operationalizes that pattern: Claude (or you) writes a **JavaScript orchestration script** that deterministically fans out, pipelines, loops, and verifies **subagents**. The control flow lives in the script (deterministic, repeatable); only the **leaf tasks** spend LLM tokens, each in its own isolated context window.

**The precise, honest claim about "deterministic":** a workflow makes the **orchestration deterministic** — same script + same inputs → same execution graph, every run, resumable, journaled. It does **not** make an individual LLM leaf-verdict bit-for-bit reproducible; leaf outputs are still probabilistic. What it buys you is **structural determinism + a large reliability gain** (voting, adversarial verify, schema-enforced handoffs). That's the right tool for our authorship gate — but for the reason below, not the reason "it makes the LLM deterministic."

**The single most load-bearing fact for us:** workflows run **in-harness on your subscription OAuth (no `ANTHROPIC_API_KEY`).** This is exactly the constraint that killed the CI-agent approach. A Claude Code workflow runs where Claude Code is already authed — your desktop, your Max subscription, no metered key, no secret in a runner. **That is why this is the pattern for our gate.**

---

## 1. What "Anthropic workflows" actually means

### 1a. The pattern (Building Effective Agents)

Anthropic's guidance draws a sharp line based on **who controls the runtime path**:

| | Workflow | Agent |
|---|---|---|
| **Control flow** | Predefined in code (DAG / state machine) | LLM decides each step dynamically |
| **Determinism** | High — repeatable execution graph | Low — different path each run |
| **Latency / cost** | Low, predictable | High, variable |
| **Debuggability** | Easy (it's just code) | Hard (open-ended loop) |
| **Use when** | Steps are mappable and predictable | Task is ambiguous, path can't be hardcoded |

Anthropic's own headline advice: **"Don't build agents for everything."** Favor deterministic workflows; add autonomy only where the task genuinely can't be scripted. The canonical workflow building blocks:

- **Prompt chaining** — linear steps, each consuming the last, with **programmatic gates** (if/else) between them.
- **Routing** — a classifier node sends input down a specialized path.
- **Parallelization** — *sectioning* (split a big task into independent chunks) and **voting** (run the same prompt N times for consistency / evaluation).
- **Orchestrator-workers** — a central node decomposes and delegates to workers, then synthesizes.
- **Evaluator-optimizer** — generate → critique against a rubric (LLM *or* a deterministic test script) → refine in a loop.

### 1b. The feature (Claude Code Workflow primitive)

The desktop CLI operationalizes the pattern. The mental-model shift the docs keep repeating: **"the script is the plan."** Instead of Claude holding a huge orchestration in its live context (which floods the window and drifts), Claude writes a JS script to `.claude/workflows/` and a background runtime executes it. Your main session stays clean — it only receives the finalized, verified result.

---

## 2. How the Claude Code workflow feature works (mechanics)

Grounded in the tool spec I run under (authoritative), corroborated by the web:

- **The script.** Plain JavaScript (not TypeScript — no type annotations). Must open with a pure-literal `export const meta = { name, description, phases }`. The body uses these hooks:
  - `agent(prompt, opts)` — spawn one subagent in its **own isolated context window**. With `opts.schema` (a JSON Schema) the subagent is **forced to return validated structured data**, not prose — the reliability keystone. Returns its final text (or the validated object) to a **script variable**, not to your main context.
  - `pipeline(items, stage1, stage2, …)` — run each item through all stages independently, **no barrier between stages** (item A can be in stage 3 while item B is still in stage 1). This is the **default** for multi-stage work.
  - `parallel(thunks)` — run concurrently **with a barrier** (awaits all). Use only when you genuinely need every result together (dedup, early-exit, cross-item comparison).
  - `phase(title)` / `log(msg)` — progress grouping + narration.
  - `budget` — a hard token ceiling you can scale depth against.
- **Isolated context + parallelism.** Each `agent()` is a fresh subagent; they don't pollute each other's history ("no hallucination leak"). Concurrency is capped (~min(16, cores−2)); excess queues.
- **Git worktrees for conflict prevention.** `agent(…, {isolation: 'worktree'})` runs a mutating agent on its own temporary branch/worktree; merges back only after verification. Use **only** when agents write files in parallel and would otherwise collide — it's expensive.
- **Adversarial verify / wave model.** The signature quality pattern: for every finding an agent produces, spawn **independent skeptic agents prompted to refute it**; keep it only if it survives a majority vote. Perspective-diverse verifiers (correctness / security / repro) catch failure modes redundancy can't.
- **Journaling + resume.** Runs can go for hours (100k-line migrations). The runtime **journals** every completed `agent()` call; if it's interrupted (laptop closed, net drop, manual kill) you resume and it **skips completed steps** — same script + same args → 100% cache hit.
- **Dynamic vs. committed (the two modalities):**
  - **Dynamic (AI-authored):** you type a goal (trigger word `workflow`, or high-reasoning `ultracode`); Claude writes and runs the script on the fly. Best for one-off complex tasks (security audits, ports).
  - **Committed (human-authored):** you write the script, check it into `.claude/workflows/`, and **every run executes the identical graph.** Best for standardized, repeatable pipelines (PR review, refactors, CI-style test-and-repair). **This is the modality that gives repeatable-across-runs, repeatable-across-people determinism** — because the execution graph is version-controlled.
- **Live control.** `/workflows` opens a dashboard while agents run in the background; you can pause / restart-a-failed-agent / kill / save the generated script to `.claude/workflows/` to commit it.

---

## 3. What "deterministic" does and does not mean here (the crux)

Be precise, because it's easy to over-claim:

- ✅ **Control-flow determinism** — the orchestration graph is code. Same script + same inputs → same sequence of steps, same fan-out, same gates, every run. Committed to git → every teammate/agent runs the exact same graph. Journaled → resumable and auditable.
- ✅ **Reliability determinism (statistical)** — voting (run the same check N times, require majority), adversarial verify (survive refutation), and schema-enforced handoffs make the *aggregate verdict* far more stable and far less likely to be a one-off hallucination.
- ❌ **Output determinism (bit-for-bit)** — a single LLM leaf call is still probabilistic. Workflows do **not** turn an LLM judgment into a reproducible pure function. Anything that must be truly reproducible/unbypassable has to be a **deterministic code check** at a leaf (string match, regex, test suite), not an LLM call.

**Design rule that falls out of this:** put the **high-risk, must-be-exact** decision in a **deterministic code leaf**; wrap the **fuzzy residual** in a workflow that raises its reliability via voting/verify. Don't ask the LLM layer to be exact — ask the code layer to be exact and the LLM layer to be *good and repeatable in shape*.

---

## 4. Auth model — the fact that decides our architecture

| | Desktop / local CLI workflow | GitHub Actions (`anthropics/claude-code-action@v1`) |
|---|---|---|
| **Credential** | Browser OAuth → your **Claude.ai / Max** login | `ANTHROPIC_API_KEY` **or** `CLAUDE_CODE_OAUTH_TOKEN` |
| **Billing** | Flat subscription, no per-token | Pay-per-token (API key) |
| **Interactive** | Yes | No (headless, trigger-driven) |
| **Key in a secret store?** | **No** | **Yes** |

- **Local/desktop Claude Code needs no API key.** First `claude` launch does an OAuth browser callback against your subscription; usage draws on your Max caps, not per-token. Workflows run **in this same authed harness.** No standing secret, nothing for a runner to hold.
- **The CI escape hatch (know it, but note the ToS teeth):** `claude setup-token` on your desktop exports a subscription **OAuth token** (`sk-ant-oat01-…`) you *can* drop into a GitHub secret as `CLAUDE_CODE_OAUTH_TOKEN` — running Claude Code agentically in CI **without a metered API key.** **BUT** every source flags the same constraint: the subscription OAuth token is licensed for **individual, interactive human use.** Routing an automated pipeline — especially one other people can trigger — through it **risks an account ban** under Anthropic's ToS. So it is *technically* a no-metered-key path, but it is **not** a clean, policy-safe way to put agent adjudication on a shared CI merge gate. It's a personal-automation tool, not a team gate primitive.

**Net for us:** the policy-safe, key-free home for LLM adjudication is **in-harness on the desktop** (a workflow you run / a scheduled local sweep), **not** a CI runner — exactly the split we'd already landed on.

---

## 5. Best practices in Claude Code desktop

Distilled from the web guidance + the tool spec:

1. **Pipeline by default; barrier only when you must.** Reach for `parallel()` (a barrier) only when a stage genuinely needs *all* prior results at once (dedup, early-exit, cross-item comparison). Otherwise `pipeline()` — no wasted wall-clock.
2. **Bind agent handoffs to JSON Schemas.** Free-text handoffs are the #1 multi-agent failure. Structured output (`schema`) validated at the tool layer means the model retries on mismatch and downstream stages get valid data.
3. **Adversarial verify + voting for anything that matters.** Don't trust a single agent's finding — spawn independent refuters, require a majority, and default findings to "refuted" when a verifier is uncertain. Use perspective-diverse verifiers for multi-failure-mode claims.
4. **Loop-until-dry, not fixed-count, for discovery.** For unknown-size problems (find all X), keep spawning finders until K consecutive rounds surface nothing new; dedup against *everything seen*, not just what was confirmed, or it never converges.
5. **Worktree isolation only for parallel file-mutation.** It's expensive (~200–500ms + disk per agent); use it strictly when agents write and would collide, and `log()` anything you cap so silent truncation doesn't read as full coverage.
6. **Commit the workflow for repeatability.** Author it, check it into `.claude/workflows/`, and every run — every teammate, every CI-style invocation — executes the identical graph. This is where cross-run/cross-person determinism actually comes from.
7. **Budget-guard dynamic loops.** Scale finder depth against a token target; guard `while` loops on `budget.total` so an unbounded run doesn't hit the agent cap.
8. **Keep `CLAUDE.md` tight** (the guidance repeats: long context guides get ignored/diluted); start big changes with `/plan` (approving a text plan is far cheaper than unwinding a bad diff); resume long runs with `claude --resume`; `/compact` or `/undo` instead of re-prompting into a filled context after 2–3 failed iterations.
9. **Monitor with `/workflows`.** Watch live, pause/kill/restart individual agents, save a good dynamic script to disk to make it a committed pipeline.

---

## 6. What this means for our authorship gate (stoa--p0e)

This closes the loop on the design we reshaped under your two constraints (no standing API key; nothing-has-to-be-100%). Workflows **fit**, with the roles assigned correctly:

- **The high-risk, must-be-exact case → deterministic code leaf, made unbypassable by GitHub, no LLM.** The author-*field* check (author/owner/creator/byline/RSS-`<author>`/package/LICENSE, etc.) is a string/structured check. It runs as a plain CI status check (no key, never flaky) and is made **unbypassable** via a Repository Ruleset with an **empty bypass list** + no-direct-push. Workflows add nothing here and shouldn't — this must be code, not a model.
- **The fuzzy residual (body-prose "is this mis-crediting a person") → a committed Claude Code workflow, in-harness, no key.** This is where "anthropic workflows" is exactly your instinct realized: a **committed `.claude/workflows/` script** that fans out finders over changed prose, runs **adversarial-verify + voting** to keep false-flags down, emits a **schema-validated report**, and runs **on your subscription auth** — never a metered key, never a CI secret. Its determinism = the **repeatable execution graph** (same script, same shape, every run) + statistical reliability from voting; **not** a claim that the LLM verdict is exact. That's the correct, honest shape given "nothing has to be 100% — the report can only help."
- **Where it runs:** in-session, or a scheduled local sweep on the desktop — the policy-safe key-free home. **Not** a CI merge gate (the `setup-token` OAuth path *could* technically run it in Actions, but the ToS "individual interactive use" limit makes that unsafe for a shared gate — surfaced in §4).

**One-line reconciliation for the ticket:** *CI = deterministic author-field check, unbypassable via empty-bypass ruleset, no key. Body-prose = a committed Claude Code **workflow** (adversarial-verify + voting + schema output) run in-harness on subscription auth — deterministic in orchestration, best-effort in verdict, zero standing secret.*

---

## Sources (gsearch / Vertex-grounded, 2026-07-05)

- Anthropic, *Building Effective Agents* (workflows-vs-agents; the five workflow patterns; ACI / poka-yoke best practices).
- Claude Code Dynamic Workflows write-ups (mechanics: script-holds-the-plan, isolated context, worktrees, adversarial verify, journaling/resume, `.claude/workflows/`, `/workflows` dashboard, dynamic vs committed) — multiple 2026 secondary sources, cross-checked against the Workflow tool spec (primary).
- Claude Code auth comparison: desktop OAuth/subscription (no key) vs `claude-code-action@v1` in GitHub Actions (`ANTHROPIC_API_KEY`, or `claude setup-token` → `CLAUDE_CODE_OAUTH_TOKEN` with the individual-use ToS caveat).

*Version/date specifics in secondary blogs (exact CLI version strings, "introduced mid-2026") are unverified against official changelogs; the mechanics and the auth model above are corroborated across independent sources and the tool spec.*

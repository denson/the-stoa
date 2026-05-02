# Envelope Lifecycle — read first

This is the meta aspect note. Every envelope's body references it. Every agent reads it at session start. Short, load-bearing.

---

## The three-layer model

The operating model has three layers. Keep them straight.

- **Envelope** — tool container plus system-prompt skeleton. One file at `.claude/agents/<name>.md` with YAML frontmatter (name, description, tools, model) and a body. **Agent definitions are frozen at Claude Code session start.** Envelope files cannot be hot-swapped, widened, or narrowed at runtime. A session running envelope X runs envelope X until the session ends.
- **Letter** — single-focus instruction note for one task. Lives at `agents/aspects/<role>/<aspect>.md`. Composed by Pliny per-ticket and pasted into a sub-agent's brief. A letter is the procedure that runs inside an envelope for one particular job. Different letters can run in the same envelope across many tickets.
- **Skill** — reusable named operation. Lives at `{{SKILLS_DIR}}` or elsewhere in the plugin. Invoked by envelopes; can be referenced by letters. Skills are reusable across envelopes and projects.

An envelope is the container. A letter is the procedure for this task. A skill is a named reusable operation either can call.

---

## Recognize-a-gap rule (every agent)

Before you act on a brief, confirm the task fits your envelope's tools.

If it doesn't — the brief expects you to run a shell command but your envelope is read-only, or it assumes a tool you don't have, or the work genuinely needs a capability you haven't been granted — **stop. Do not improvise with the tools you have, and do not refuse the task silently.**

Return to your caller (Pliny, in almost all cases) with an envelope-gap flag using the template below. Pliny will do one of three things: rewrite the brief so it fits your existing envelope, dispatch a different envelope that already fits, or orchestrate authoring a new envelope (see "Envelope authoring" below — Pliny orchestrates, the workspace executor writes).

---

## Envelope-gap comment template

Use this format exactly. Pliny parses it; machine-friendly structure saves round-trips.

    envelope gap: <one-line summary>

    envelope in session: <your envelope name, e.g. VERA-readonly>
    task needs: <what the brief expects you to do>
    tool missing: <specific tool(s) your envelope doesn't have>
    suggested envelope shape: <your proposal, if you have one — e.g., "VERA-probe already has Bash + WebFetch; try that" or "need a new CATO-database envelope with psql access">

You write this as part of your normal return message. **Do not invoke `bw` yourself** — you don't run beadwork. Pliny records the gap on the ticket as a comment with `--author <your-role>` when reconciling your output.

---

## Per-context executor envelopes (workspace = the workspace executor)

The **executor role** in the pipeline (`Pliny → Ada ↔ Vera ↔ Cato → Pliny`) is filled by a different envelope depending on which git repo you're working in. "Ada" is the conceptual role name throughout these docs; the concrete envelope varies:

- **Workspace (`{{WORKSPACE_REPO}}/`)** → the rostered workspace executor envelope. Meta-editor scope: envelopes in `.claude/agents/`, meta-aspects in `agents/aspects/_meta/`, regular aspect notes, workspace `CLAUDE.md`, planning notes. Read-only on `.claude/settings.json` and `.claude/settings.local.json`.

Each executor envelope lives in its own context's `.claude/agents/` directory and is loaded only there. Filesystem absence enforces scope: Claude Code's project-agent discovery walks up from CWD but **stops at git-repository boundaries** (the nearest `.git/` directory). So a workspace-level envelope under `{{WORKSPACE_REPO}}/.claude/agents/` is not visible to a Claude Code session whose CWD is inside a nested git repo — there's a `.git/` boundary in between. The envelope you can dispatch is exactly the one whose file lives inside the current context's git repo.

> **Footnote on the boundary rule.** The git-repo-boundary behavior is sourced from GitHub issue [anthropics/claude-code#35561](https://github.com/anthropics/claude-code/issues/35561), which documents that discovery stops at git boundaries (and proposes extending it — that proposal is not implemented as of writing). The official subagents docs do not currently specify this behavior, so it is "documented in an issue but not in the canonical reference" — re-verify if the docs are updated.

---

## Envelope authoring (Pliny orchestrates; the workspace executor writes)

When the gap is real and no existing envelope fits, Pliny orchestrates and the workspace executor does the writing. Steps:

1. **Pliny confirms the gap is real.** A large fraction of apparent gaps are briefing errors — the existing envelope can do the job if the brief is rewritten. Try that first. Only proceed to authoring when rewriting the brief won't close the gap.
2. **Pliny gets {{USER_NAME}} sign-off before writing.** A new envelope is a capability-escalation event. It needs explicit approval in chat, not inference.
3. **Pliny creates a beadwork ticket and worktree, then dispatches the executor** (the workspace executor at workspace level; a scoped Ada at other levels) with a brief that specifies:
   - Envelope name, scope, tool list (minimal — start narrow and widen only on evidence).
   - Required body sections: role paragraph + explicit reference to this file ("Before acting, re-read `agents/aspects/_meta/envelope-lifecycle.md`") + authorship rule + web-search rule + boot snippet + return format.
4. **The executor drafts the envelope file** at `.claude/agents/<NAME>.md` with the YAML frontmatter (`name`, `description`, `tools`, `model`) and body sections above. Commits to the feature branch in the worktree.
5. **The full pipeline runs** as for any deliverable: Vera verifies the envelope satisfies the brief, Cato reviews the diff (paying special attention to the `tools` list as a capability-escalation surface). Pliny merges to workspace `master` under commit-rule (a) — closed-ticket deliverable — after Cato passes. Vera's verification of the new envelope MUST include a deterministic format-load assertion on the frontmatter (`yaml.safe_load`) per the standing requirement in VERA's "Deterministic format validation" section — this catches the YAML-frontmatter-parse failure mode.
6. **Pliny brings the envelope into service.** Two options:
   - **Local restart.** Have {{USER_NAME}} restart the Claude Code session. Agent definitions load at session start, so the new envelope is invisible until restart. This interrupts any in-flight work — use when the restart is cheap.
   - **Cloud session (escape hatch).** Spin the sub-task as a `claude --remote` cloud session. Cloud sessions clone the repo fresh on VM startup, so the new envelope is available without restarting this local session. Requires: envelope commit pushed to the remote, network egress, per-session cost. Propose this path to {{USER_NAME}} and get explicit approval before using — cloud sessions have their own cost and security envelope.

---

## Envelope hygiene (Pliny + the workspace executor)

Rules, terse:

- **One concrete task justifies one envelope.** Don't pre-author envelopes speculatively. The envelope matrix grows by evidence, not prediction.
- **Prefer widening a brief or reusing an existing envelope over creating a new one.** Envelopes proliferate quickly if you're not disciplined; each new variant is a cognitive load on everyone reading the matrix.
- **Minimal tools, then widen.** A new envelope starts with the smallest tool set that could do the task. Grow on evidence that the smaller set blocks something real.
- **Envelopes hold tools, not procedures.** Procedures live in letters. If you find yourself encoding a multi-step procedure in an envelope body, that's a letter trying to escape — extract it into `agents/aspects/<role>/<name>.md` and have the envelope reference it.
- **Retire unused envelopes.** When an envelope has had no activity for a long stretch, archive it rather than leaving it in the matrix. Dead envelopes are clutter that misleads Pliny about what's actually available.

---

## Session restart checklist (Pliny only)

Before asking {{USER_NAME}} to restart to load a new envelope:

- [ ] Envelope file is committed to the workspace repo.
- [ ] Any in-flight tickets are at a clean checkpoint (`needs:{{USER_NAME_LOWER}}` or `needs:pliny` held by Pliny, not mid-execution with the executor).
- [ ] Ticket trail records what you were about to do next so the post-restart session can resume cleanly.
- [ ] If a cloud session is the alternative, you've weighed both and recommended one to {{USER_NAME}}.

---

## See also

The envelope lifecycle is structurally upstream of the team's numbered disciplines — gap routing, the three-layer model, and envelope authoring are mechanisms the gates lean on rather than gates themselves. The catalog cross-references this file as the source for the envelope shape every officer's seat depends on.

- `agents/aspects/_meta/discipline-catalog.md` — the canonical index for T / P / X / M disciplines
- `agents/aspects/_meta/discipline-catalog.md` §"T1 — Dispatch packet shape" — the dispatch-packet's routing-slip shape leans on each officer's envelope-gap discipline (envelope-gap routing IS the structural enforcement when a brief falls outside the dispatched envelope's tools)
- `agents/aspects/_meta/discipline-catalog.md` §"M1 — Multi-Major architecture" — pair-programmer Major envelopes are authored via the same lifecycle described here (Pliny orchestrates, the workspace executor writes, CO sign-off gates capability-escalation)

## What this file is NOT

- Not a substitute for workspace `CLAUDE.md` (authorship rule, platform paths, web-search rule). Every envelope still references `CLAUDE.md` directly.
- Not the beadwork workflow doc. Baton labels, ticket lifecycle, `bw` commands live elsewhere in the project's workflow documentation.

This file covers one thing: how envelopes relate to letters and skills, and what to do when your envelope doesn't fit the task.

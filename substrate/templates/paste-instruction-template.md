# Paste-instruction template — MAJOR_PLINY activation

The template MAJOR_POLYBIUS fills per session to produce the paste-instruction that activates MAJOR_PLINY (the ORCHESTRATOR) in a fresh terminal. The static `MAJOR_PLINY.md` role file is universal; the wrapper that activates it is session-specific. POLYBIUS fills the slots from its conversation with the PRINCIPAL, writes the filled result to disk under `HUMAN_paste-orchestrator-instruction.md`, and hands the PRINCIPAL a one-line pointer.

Architecture authority: `user-beadwork/plans/three-role-recursive-architecture.md` (v2). The string-substitution mechanism is settled in §8 ("Custom paste-instruction templating mechanism") and traces back to `u--7yg.13`. The on-disk-with-short-paste pattern is the **durable-substrate-with-short-prompts** discipline (v2 §8) — substantive content lives on disk; the chat paste is one line.

---

## Substitution slots

| Slot | Meaning | Example |
|---|---|---|
| `{{PROJECT_NAME}}` | the project the orchestrator is running in | `agent-character-builder` |
| `{{SESSION_INTENT}}` | the PRINCIPAL's stated immediate intent for this session, in one or two sentences | `Ship the v0.2 character profile UI per acb-101.` |
| `{{BW_PREFIX}}` | the short form of the beadwork prefix (without the trailing dash); the template adds `--` after it for the visual ticket-ID format | `acb` |
| `{{ROLE_FILE_PATH}}` | path to `MAJOR_PLINY.md` from the orchestrator session's working directory; usually `.claude/MAJOR_PLINY.md` at project root, or `~/.claude/MAJOR_PLINY.md` for a user-tier orchestrator | `.claude/MAJOR_PLINY.md` |
| `{{PENDING_DIRECTIVES}}` | optional — specific bw ticket IDs POLYBIUS wants the orchestrator to read first | `acb-101, acb-102` |
| `{{ON_DISK_PATH}}` | path where POLYBIUS saves the filled paste-instruction so the PRINCIPAL can re-paste during compact-or-clear recovery without POLYBIUS in the loop | `HUMAN_paste-orchestrator-instruction.md` |

`{{PENDING_DIRECTIVES}}` is optional. If empty, omit the trailing clause entirely rather than leaving an empty slot in the rendered output.

### Per-slot rationale

A future POLYBIUS reading this template should understand *why* each slot is filled the way it is. The slots aren't decorative — each one is a load-bearing piece of context the orchestrator needs to start work cleanly.

- **`{{PROJECT_NAME}}`** scopes the orchestrator's identity. `MAJOR_PLINY.md` is universal; "for `<project>`" tells the activated session which beadwork prefix is its scope and which working tree it's authoritative for.
- **`{{SESSION_INTENT}}`** is the most consequential slot. A vague intent produces a vague PLINY activation that drifts toward generic Claude Code behavior in its first turn. Press the PRINCIPAL for specificity during the interview; if specificity isn't yet possible, write the intent as `Orient and recommend a first arc — <topic> is not yet scoped.` That phrasing is honest about the lack of specificity rather than smoothing it.
- **`{{BW_PREFIX}}`** lets the orchestrator find the right beadwork on first read. Without it, PLINY may read a wrong-tier beadwork and act on stale tickets.
- **`{{ROLE_FILE_PATH}}`** is `.claude/MAJOR_PLINY.md` after install at project-tier, or `~/.claude/MAJOR_PLINY.md` at user-tier. At sub-project tier the file is suffixed: `.claude/MAJOR_PLINY_<subproject-slug>.md` (sub-project install.sh deploys both MAJORs with the slug suffix; see `MAJOR_POLYBIUS.md` §10). The orchestrator reads this file as its first action; getting the path wrong means the role doesn't load.
- **`{{PENDING_DIRECTIVES}}`** is how POLYBIUS hands the orchestrator a specific starting point when one exists. Empty is fine — orchestrator will sweep the beadwork in priority order.
- **`{{ON_DISK_PATH}}`** is the recovery substrate. After `/compact` or `/clear`, the PRINCIPAL re-pastes the contents of this file to re-activate the orchestrator without coming back to POLYBIUS. Keep the path stable across a session — `HUMAN_paste-orchestrator-instruction.md` at project root is the convention.

---

## Template

```
Read {{ROLE_FILE_PATH}} and assume the orchestrator role for {{PROJECT_NAME}}.

Your immediate intent for this session: {{SESSION_INTENT}}

Check beadwork ({{BW_PREFIX}}-- prefix) for pending directives from MAJOR_POLYBIUS{{PENDING_DIRECTIVES_CLAUSE}}.

If compaction or /clear erases your role, re-read this paste from {{ON_DISK_PATH}} in the project root.
```

`{{PENDING_DIRECTIVES_CLAUSE}}` expands to ` — start with: {{PENDING_DIRECTIVES}}` when pending directives are named; otherwise it expands to empty string and the preceding sentence ends after `MAJOR_POLYBIUS`.

---

## Worked example

Suppose the interview produced:

- Project: `agent-character-builder`
- Intent: ship the v0.2 character profile UI per the existing `acb-101` ticket
- Beadwork prefix: `acb`
- Role file path: `.claude/MAJOR_PLINY.md`
- Pending directives: `acb-101`
- On-disk path: `HUMAN_paste-orchestrator-instruction.md`

The filled paste-instruction:

```
Read .claude/MAJOR_PLINY.md and assume the orchestrator role for agent-character-builder.

Your immediate intent for this session: Ship the v0.2 character profile UI per acb-101.

Check beadwork (acb-- prefix) for pending directives from MAJOR_POLYBIUS — start with: acb-101.

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-orchestrator-instruction.md in the project root.
```

POLYBIUS writes that exact string to `HUMAN_paste-orchestrator-instruction.md` at the project root. The PRINCIPAL gets a one-line chat paste to drop into the new terminal:

```
Read HUMAN_paste-orchestrator-instruction.md and execute.
```

The substantive content stays on disk — re-readable, durable, version-controllable. The chat paste is one line.

**Cookbook:** the activated session reads `operating-disciplines.md` §12 (bw cookbook) for canonical bw operations. The activation paste does not duplicate cookbook content; the cookbook is part of the substrate the activated agent loads.

---

## Where the filled paste-instruction lives

POLYBIUS writes the filled version to the on-disk path (default `HUMAN_paste-orchestrator-instruction.md` at the project root). The `HUMAN_*` prefix marks the file as a message-for-humans per spec §3, distinct from agent envelopes (`MAJOR_*.md`, `CAPTAIN_*.md`).

The PRINCIPAL may re-paste the one-line pointer (or, if the pointer mechanism isn't working, the file's contents directly) without POLYBIUS in the loop during a compact-or-clear recovery. POLYBIUS's job is to keep the on-disk copy *current* — refresh it when intent shifts materially or when new pending directives accumulate.

---

## When to refresh the on-disk copy

- The PRINCIPAL's stated intent shifts materially mid-session (e.g., original was "ship the UI" and the conversation has moved to "fix a bug discovered during the UI shipment").
- A compact-or-clear recovery just happened and the original intent is now stale.
- POLYBIUS has filed new pending directives a re-paste should pick up.

A paste-instruction written at session start may be stale by the third compaction. Refreshing is cheap; running the orchestrator against stale intent is not. This is part of the load-bearing compact-or-clear recovery responsibility documented in `MAJOR_POLYBIUS.md` §6.

---

## Why string substitution rather than per-session LLM generation

Spec §8 (and the closing comment on `u--7yg.13`) settles this: **string substitution.** Reasons:

- **Deterministic.** The same slot values produce the same paste-instruction. Reviewable, predictable, auditable.
- **Version-controllable.** The template stays under `templates/`; changes to it appear in the diff history.
- **Debuggable.** Slot values are visible separately from the template; if the orchestrator activates with the wrong intent, the failure point is obvious.
- **No critical-path failure mode.** LLM-generation would add a generation step on the activation critical path, adding a way for the system to fail at the moment it most needs to come up cleanly.

If a future workflow demonstrates a real need for LLM-generated paste-instructions (e.g., the substitution slots stop being expressive enough for some class of session), revisit then. Until that signal arrives, this is the answer.

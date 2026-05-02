# Paste-instruction template — MAJOR_PLINY activation

This is the template MAJOR_POLYBIUS uses to generate the per-session paste-instruction that activates MAJOR_PLINY in a fresh terminal. The static `MAJOR_PLINY.md` role file is universal; the wrapper that activates it is session-specific. POLYBIUS fills in the slots from the conversation it just had with the Colonel and hands the filled result to the Colonel along with instructions for opening the new terminal.

This file settles spec §10 open question 1 (paste-instruction templating mechanism). Mechanism: string-format substitution. Rationale below.

---

## Substitution slots

| Slot | Meaning | Example |
|---|---|---|
| `{{PROJECT_NAME}}` | the project the orchestrator is running in | `agent-character-builder` |
| `{{SESSION_INTENT}}` | the Colonel's stated immediate intent for this session, in one or two sentences | `Ship the v0.2 character profile UI per acb-101.` |
| `{{BW_PREFIX}}` | the short form of the beadwork prefix (without the trailing dash); the template adds `--` after it for the visual ticket-ID format | `acb` |
| `{{ROLE_FILE_PATH}}` | path to MAJOR_PLINY.md from where the new session opens; usually `.claude/MAJOR_PLINY.md` at project root, or `~/.claude/MAJOR_PLINY.md` for a user-tier orchestrator | `.claude/MAJOR_PLINY.md` |
| `{{PENDING_DIRECTIVES}}` | optional: specific bw ticket IDs POLYBIUS wants PLINY to read first | `acb-101, acb-102` |
| `{{ON_DISK_PATH}}` | path where POLYBIUS saves the filled paste-instruction so the Colonel can re-paste during compact-recovery without POLYBIUS in the loop | `HUMAN_paste-orchestrator-instruction.md` |

`{{PENDING_DIRECTIVES}}` is optional. If empty, omit the trailing clause entirely rather than leaving an empty slot.

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

Suppose the conversation produced:

- Project: `agent-character-builder`
- Intent: ship the v0.2 character profile UI per the existing acb-101 ticket
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

POLYBIUS writes that exact string to `HUMAN_paste-orchestrator-instruction.md` at the project root, then hands the Colonel both the file location and the literal text to paste.

---

## Where the filled paste-instruction lives

POLYBIUS writes the filled version to the on-disk path (default `HUMAN_paste-orchestrator-instruction.md` at the project root). The `HUMAN_*` prefix marks it as a message-for-humans per spec §3, distinct from agent envelopes (`MAJOR_*.md`, `CAPTAIN_*.md`).

The Colonel may re-paste from this file without POLYBIUS in the loop during a compact-or-clear recovery. POLYBIUS's job is to keep the on-disk copy *current* — refresh it when intent shifts materially or when new pending directives accumulate.

---

## When to refresh the on-disk copy

- The Colonel's stated intent shifts materially mid-session (e.g., original was "ship the UI" and the conversation has moved to "fix a bug discovered during the UI shipment").
- A compact-or-clear recovery just happened and the original intent is now stale.
- POLYBIUS has filed new pending directives a re-paste should pick up.

A paste-instruction written at session start may be stale by the third compaction. Refreshing is cheap; running PLINY against stale intent is not.

---

## Why slot-substitution rather than per-session LLM generation

Spec §10 open question 1 left this mechanism undecided: string substitution, LLM generation, or fully ad-hoc. Arc 2 settles on string substitution. Reasons:

- **Deterministic.** The same slot values produce the same paste-instruction. Reviewable, predictable, auditable.
- **Version-controllable.** The template stays under `templates/`; changes to it appear in the diff history.
- **Debuggable.** Slot values are visible separately from the template; if PLINY activates with the wrong intent, the failure point is obvious.
- **No critical-path failure mode.** LLM-generation would add a generation step on the activation critical path, adding a way for the system to fail at the moment it most needs to come up cleanly.

If a future workflow demonstrates a real need for LLM-generated paste-instructions (e.g., the substitution slots stop being expressive enough for some class of session), revisit then. Until that signal arrives, this is the answer.

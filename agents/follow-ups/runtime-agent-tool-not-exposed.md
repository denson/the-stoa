# Follow-up: Runtime `Agent` tool not exposed in `MAJOR_PLINY_agent_character_builder` envelope

**Status:** Open. Filed during acb-001-darkmode dispatch (2026-04-30).
**Severity:** Low — workaround in place.
**Suggested ticket id:** acb-NNN (assign when prioritized; not blocking acb-001).

## Observation

The deployed envelope at `.claude/agents/MAJOR_PLINY_agent_character_builder.md` declares in frontmatter (line 4):

```
tools: Bash, Read, Write, Edit, Grep, Glob, Agent, TodoWrite, WebSearch, WebFetch
```

When that subagent was spawned during acb-001 dispatch, the runtime tool surface exposed only:

```
Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
```

`Agent` and `TodoWrite` were **not present** at runtime, despite being declared in frontmatter.

## Why this matters

Whether or not Pliny *should* dispatch the team is settled by his envelope text (line 18: "You DO NOT dispatch the team"). So the missing `Agent` tool was not load-bearing for acb-001.

But the divergence between **declared** tools and **runtime-exposed** tools is a quiet bug that will bite a future arc where an officer's declared tool is genuinely needed.

## Hypotheses to investigate

1. **Subagent frontmatter handling quirk in Claude Code.** Possibly `Agent` is filtered out of subagent tool grants by default (parent-only tool), regardless of frontmatter declaration. Worth checking the Claude Code subagent docs / source.
2. **`TodoWrite` rename → `TaskCreate`/`TaskUpdate`/etc.** The new task tool family may have replaced `TodoWrite`; envelopes still declaring `TodoWrite` get nothing. If so, every officer envelope needs a frontmatter sweep.
3. **Tool-name casing or namespace mismatch.** The runtime might expect `task` or `agent` lowercase, or namespaced (e.g., `mcp__...__Agent`).

## Action when prioritized

1. Spawn a minimal probe subagent that just lists its own tool surface and compares to its frontmatter declaration.
2. Read current Claude Code subagent docs to confirm whether `Agent` is parent-session-only.
3. Sweep all `*_agent_character_builder.md` envelopes for `TodoWrite` → migrate to the `Task*` family if the rename hypothesis holds.
4. Document the corrected canonical tool list per role in `agents/aspects/_meta/`.

## Workaround in use

For acb-001, the parent Claude Code session orchestrates the team directly via its own `Agent` tool, bypassing Pliny's dispatch role (which is correctly outside Pliny's envelope anyway). This pattern is fine for small mechanical-after-design arcs; it does not scale to full novel-design arcs that need Session B + bw + Captain Nestor.

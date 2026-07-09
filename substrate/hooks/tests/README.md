# Stop self-check regression corpus

This directory is the **regression guard** for the surviving `stop-self-check.sh`
hook. (The author-gate regression corpus that previously lived here was retired
in Arc `stoa--p0e` when the authorship deny-gate was retired; its runner +
fixtures were archived to `substrate/v1-historical/hooks/tests/` — see
`substrate/v1-historical/hooks/RETIREMENT.md`.)

Run it:

```bash
bash substrate/hooks/tests/run-stop-self-check-tests.sh
```

Exit 0 = all pass. Exit non-zero = at least one assertion failed (a regression).

## What it guards — the Stop self-check hook

`run-stop-self-check-tests.sh` exercises the REAL `substrate/hooks/stop-self-check.sh`
end-to-end via stdin (no reimplementation). It asserts the two load-bearing
properties of the Stop self-check:

1. **Clause (E) is injected on the working `decision:"block"` + `reason` channel.**
   The FIRST Stop event of a turn emits `decision:"block"` with a `reason` that
   contains the clause-(E) sentinel string, proving the self-check reminder rides
   the confirmed-working Stop channel (not the upstream-broken `additionalContext`
   channel).
2. **The once-per-turn sentinel prevents an infinite block loop.** The SAME event
   replayed in the SAME turn (same `session_id` + same transcript size → same
   turn-key) ALLOWS the stop (exit 0, empty stdout), proving the per-turn sentinel
   guard is intact — a Stop hook that always blocked would trap the turn in a loop.

Determinism is controlled by pinning the two inputs the hook keys on (`cwd` → a
fixed scratch dir; `transcript_path` → a fixed runner-created file of stable size)
so both invocations resolve to the same sentinel dir + turn-key. The runner cleans
up its scratch dir on exit (fixed-literal paths under a single scratch root — no
`$VAR`-in-destructive-op footgun, `operating-disciplines.md` §8.6).

## Deploy posture — source-only

This `tests/` subdir is **source-only** — it does NOT deploy. `install.sh` globs
`substrate/hooks/*.sh` **non-recursively** and copies `README.md` by basename only,
so this `tests/` subdir is invisible to the hook deploy. (Note: this source-only
property is specific to the NON-recursive hook glob. A skill's `tests/` subtree,
by contrast, DOES deploy via the recursive `cp -R` skill-deploy path — see the
`attribution-advisory` skill.)

## Layout

```
tests/
  README.md                     # this file
  run-stop-self-check-tests.sh  # the runner
  fixtures/
    stop-event-orchestrator.json  # the Stop event fixture (path placeholders substituted at runtime)
```

# design-rev3 — Decision-register CAPTURE (self-correction doctrine slice 2a, the black box capture half)

> Arc 71 / charter `stoa--7gl`. Author of repo: Denson Smith.
> Design seat: CAPTAIN_DAEDALUS_the_stoa (subagent). Operating mode: autonomous.
> Supersedes `design-rev2.md` at DC3 + ONE new probe (P11) ONLY (see delta note). Everything else stands as
> rev2 (which itself stands as rev1 except DC0 + P7). DC0/P7 ARGUS-ratified and floor-manager-GO; the 2b
> boundary + honesty stance unchanged.

---

## rev2 → rev3 delta (what changed, and what did NOT)

The floor-manager's design-gate added a 4th gate item that rev2 does not yet satisfy (it crossed the in-flight
rev2 run — not a rev2 miss): a decision-register entry body will routinely contain BOTH an apostrophe (prose:
"the team's call") AND a bare dollar amount (cost figure: `$50k`). The rev1/rev2 DC3 write contract locked the
backtick / `$()` footguns but did NOT lock the **bare-`$` footgun** — a bare `$` inside a Bash-tool
double-quoted body is shell parameter-expansion exactly like backticks/`$()`, so `$50k` mangles to `0k` (bash
reads `$5`/`$50` as a positional param → empty). A write contract that cannot write its own example content (DC4's
own examples contain apostrophes; cost counter-hypotheses carry dollar figures) is a deliverable defect, not a
polish item. This rev3 hardens DC3 to write such a body unmangled and adds a probe that EXERCISES it.

**Changed (this rev3 restates these in full):**

- **DC3 — the bw-write contract now specifies the ROBUST quoting form** (was: "POSITIONAL, no `-m`, no backticks,
  no `$()`" — which left bare `$` unaddressed). rev3 investigates bw's real capability LIVE (positional-arg
  only — no stdin/file-body sidestep) and specifies the proven save-verdict quoting applied to the positional
  `bw comment` arg: **single-quote the ENTIRE body, escape each embedded apostrophe as `'\''`.** Single quotes
  make `$` AND backticks literal (so `$50k` survives); `'\''` handles the embedded apostrophe. Grounded LIVE
  (result inline below). The verify-then-assert re-read step already in DC3 stays — it now also catches the
  dollar-mangle class.
- **NEW probe P11 — live dollar-AND-apostrophe round-trip.** A probe VERA executes LIVE in Phase C: write a real
  entry whose WARNING or COUNTER-HYPOTHESIS contains BOTH an apostrophe and a bare `$50k`, `bw show` the register
  ticket, assert the apostrophe is present AND the literal `$50k` is present and NOT mangled to `0k`. It can FAIL
  on the dollar-mangle (the naive double-quote baseline mangles — proven below).

**Unchanged — do NOT re-read these as re-opened:**

- **DC0 + P7** (rev2): single-line ` ~ `-delimited OPTIONS; bare-`field()`-recoverable; r3 folded. ARGUS-ratified
  and floor-manager-GO (gate items 1–3). → `design-rev2.md`.
- **§0** problem restatement + A1/A2/A3 honesty posture → `design-rev1.md` §0.
- **§1** approach + the §35.5 `not threat-ratified` carve-out (ARGUS-CONFIRMED) → `design-rev1.md` §1.
- **DC1** write-trigger predicate + over-write guard; **DC2** new-module + two-owner composition; **DC4** the
  "writing is half the value" device + honesty stance (template + prose + corpus-regression-guard, NOT a hard
  gate; no enforced/guaranteed/non-collapsible language); **DC5** corpus + per-class floors → `design-rev1.md`
  §2 (DC1/DC2/DC4/DC5 exactly as written).
- **Probes P1–P6, P8–P10** → `design-rev1.md` §3 (unchanged). **P5** is UNCHANGED — P11 is a NEW, distinct probe
  that ADDS the dollar-AND-apostrophe assertion; P5's "all nine fields land intact" assertion stands as-is. (I
  add P11 rather than mutate P5 so the existing ratified probe set is untouched and the new falsifiable assertion
  is named separately.)
- **§4** weak points (WP-1…WP-5) → `design-rev1.md` §4. rev3 adds no new weak point: the robust quoting is the
  proven save-verdict form, grounded live; it is strictly more correct than the rev2 contract with no new
  assumption beyond "the seats invoke bw through bash" (true — the gauntlet seats run bw via the Bash tool; see
  the DC3 shell-path note).
- **§5** out of scope / the 2b boundary → `design-rev1.md` §5 (zero 2b reach).
- **Honesty stance** unchanged. No new scope. Minimal-sufficient: DC3 + one probe only.

---

## §2 · DC3 — bw-write mechanics + transparency (RESTATED IN FULL; quoting contract HARDENED)

**Mechanics: an inline deterministic template, NOT a helper script — with ALL bw/shell footguns honored.**
*(The inline-template-vs-helper-script tradeoff and its conclusion are UNCHANGED from `design-rev1.md` §2 DC3 —
inline template chosen because it resolves at subproject tier and keeps the DC4 field-writing visible. Restated
here only because DC3 is restated in full; the table and its verdict are exactly as rev1. What changed is the
write-contract quoting, below.)*

### bw real capability — investigated LIVE (rev3, the design call's foundation)

`bw comment --help` and `bw --help` were run live (rev3 design-time). Result:

```
bw comment <id> <text> [flags]
  flags: -a/--author NAME, --json
```

**`bw comment` takes the comment body as a POSITIONAL argument only.** There is **no** `--stdin`, no
`--body-file`, no `--file`, no `-` stdin convention — nothing that would let the body bypass shell argument
quoting. (`bw attach` takes a file PATH, but that attaches a file as an attachment, not a comment body — wrong
construct for a register entry, which is a comment in the stream per DC0; and it does not sidestep the comment
text path.) **Therefore the most-robust option (a stdin/file-body input that sidesteps shell quoting entirely)
does NOT exist for `bw comment`** — the design must solve the quoting at the positional arg.

### The write contract (footguns honored — LOCKED; the quoting form is the rev3 hardening)

The entry body is written with **ONE** `bw comment` call using the **robust single-quote form**:

- **POSITIONAL — never `-m`** (memory: feedback-validate-bw-syntax; `-m` records the literal string "-m" and
  drops the message). Confirmed live: `bw comment` has no `-m` flag.
- **Single-quote the ENTIRE body; escape each embedded apostrophe as `'\''`** (close-quote, escaped-apostrophe,
  reopen-quote — the proven `save-verdict.md` "Quoting caveat" form, applied to the positional `bw comment` arg).
  This is the rev3 change. Concretely the module's template instructs the writer to emit:

  ```bash
  bw comment <register-ticket-id> '<entry body, single-quoted; every embedded apostrophe written as '\''>'
  ```

  - **Single quotes make `$` AND backticks AND `$()` literal** — so a bare dollar amount (`$50k`), a backtick, or
    a `$()` span in the body is written verbatim, NOT shell-expanded. This is what closes the bare-`$`
    (dollar-mangle) footgun the floor-manager's gate item 4 named, and it subsumes the rev1/rev2
    backtick/`$()` lock into one mechanism (single-quoting handles all three shell-substitution footguns at once).
  - **`'\''` handles the embedded apostrophe** — "the team's call" is written `the team'\''s call`. Without this,
    a bare apostrophe would terminate the single-quoted string. This is the one place the body author must
    transform the text: each `'` in the prose becomes `'\''`.
  - **Forbidden (carried from save-verdict):** a `cat <<'EOF' … EOF` heredoc (breaks on apostrophes on Windows
    git-bash). The body goes directly in the single-quoted positional arg.

- **No content restriction.** The body MAY contain apostrophes and dollar amounts freely — that is the point of
  the robust quoting. (Forbidding dollars/contractions in entries is NOT an acceptable resolution: cost
  counter-hypotheses need dollar figures and prose needs contractions. The quoting absorbs them.) The only
  reserved sequences remain the DC0 parse-hygiene rules (no value begins with a reserved `LABEL:` token; ` ~ ` is
  the OPTIONS delimiter) — those are unchanged and orthogonal to shell quoting.

- **Verify-then-assert (memory: feedback-verify-then-assert) — UNCHANGED, now broader-catching:** after the
  write, the agent re-reads the register ticket (`bw show <register-ticket-id>`) to confirm the entry landed
  intact. With the robust quoting this re-read now ALSO catches the dollar-mangle class (a mangled `$50k → 0k`
  shows on re-read), not just the backtick-mangle class. The module states this as a required post-write step.

- **First-use ticket creation:** UNCHANGED from rev1 — if no `decision-register`-labeled ticket exists, create
  it once (`bw create "Decision register (self-correction black box)"` then `bw label <id> +decision-register`),
  then comment. Lookup-or-create sequence is deterministic.

### Shell-path note (honest scope of the quoting contract)

The robust single-quote form is **bash** single-quote semantics. The gauntlet seats invoke `bw` through the
**Bash tool** (bash / git-bash on this Windows host) — that is the path the seats actually use, and the path the
grounding below exercises. The floor-manager noted the seats *could* invoke bw through PowerShell, whose
single-quote escaping differs (`''` doubles a literal apostrophe; `$` is not special in PowerShell single quotes,
so the dollar footgun does not even arise there). The contract specified here is the **bash** form because that
is the seats' actual invocation path; the module states the contract is the bash single-quote form so a reader on
the bash path applies it correctly. A PowerShell-only invocation path is out of scope for slice 2a (the seats run
bw via the Bash tool); if a future deployment drives bw from PowerShell, the bare-`$` footgun is absent there and
the apostrophe rule is PowerShell `''`-doubling — a one-line forward note, not a slice-2a build.

### GROUNDING RESULT (rev3 design-time, run LIVE — not asserted)

Proven that a body carrying BOTH a bare apostrophe AND a bare dollar amount survives the chosen write mechanism
unmangled. Two grounds, both run live:

**(1) Shell round-trip — robust form vs naive baseline.** Body literal: `WARNING: the team's call cost $50k to
revert`.

| Quoting | What the shell rendered | Verdict |
|---|---|---|
| **Naive double-quote** `"...the team's call cost $50k..."` | `WARNING: the team's call cost 0k to revert` | **MANGLED** — `$50` expanded to empty, leaving `0k`. (Proves the bug is real AND that a probe over this can fail.) |
| **Robust single-quote + `'\''`** `'...the team'\''s call cost $50k...'` | `WARNING: the team's call cost $50k to revert` | **CLEAN** — apostrophe intact, `$50k` intact. |

**(2) Live `bw comment` end-to-end on a THROWAWAY ticket.** Created throwaway ticket `stoa--ze5`, wrote via the
robust form a body containing two apostrophes ("team's", "that's") and a bare `$50k`, then `bw show` re-read:

```
DILEMMA: ship now vs slip. WARNING: the team's call cost $50k to revert and that's the accepted downside.
```

Machine assertions on the re-read: apostrophe intact PASS · 2nd apostrophe intact PASS · literal `$50k` present
PASS · no bare `0k` (mangle check) PASS. Throwaway ticket `stoa--ze5` deleted (`bw delete --force`) after
verification — left noted here as the grounding record. **The robust quoting writes the dollar-AND-apostrophe
body intact through the actual `bw comment` path the seats use.**

### Transparency (UNCHANGED from rev1 §2 DC3)

The decision-journal-not-hidden-dossier property — register is a normal bw ticket, single-user user-readable by
default, team-visible by construction with the named all-seats-readable caveat (WP-4). Exactly as
`design-rev1.md` §2 DC3 "Transparency" subsection; rev3 does not touch it.

---

## §3 · P11 — live dollar-AND-apostrophe round-trip (NEW PROBE, RESTATED IN FULL)

> Probe-id: **P11** (new; guards the DC3 quoting hardening). All other probes (P1–P10) are exactly as
> `design-rev1.md` §3 / `design-rev2.md` §3 and are unchanged — including P5 (live entry lands intact). No
> threat-anchored probe applies (the §1 carve-out is unchanged and ARGUS-CONFIRMED; this is process/tooling
> hardening with no runtime attack path).

**P11 — a register entry body containing BOTH an apostrophe and a bare dollar amount lands intact (the
quoting-robustness probe; VERA executes it LIVE in Phase C).**

Setup: at a real (or fixture-simulated) decided-dilemma, write ONE register entry whose `WARNING` (or
`COUNTER-HYPOTHESIS`) field contains BOTH a contraction (apostrophe) AND a bare dollar amount — e.g.
`WARNING: the team's call accepts a $50k revert cost`. The write uses the DC3 robust form (single-quoted body,
embedded apostrophe as `'\''`). To the register ticket (the standing `decision-register`-labeled ticket).

Assertions (the probe FAILS if any does not hold) — run against the `bw show <register-ticket-id>` re-read:

1. **The apostrophe is present and intact** — the re-read contains the literal `team's` (the contraction is not
   dropped or terminated-early). Falsifies "the apostrophe escaping broke the body."
2. **The literal dollar amount is present and NOT mangled** — the re-read contains the literal `$50k` AND does
   NOT contain a bare `0k` (the dollar-mangle signature: `$50` expanded to empty leaving `0k`). This is the
   load-bearing assertion: **it FAILS if the body were written with naive double-quoting** (which mangles `$50k`
   → `0k`, as the grounding baseline proved). A probe that cannot fail on the dollar-mangle is not a probe — this
   one can.
3. **No backtick/`$()` collateral** — if the test body also includes a backtick or `$()` span, the re-read
   contains it verbatim (single-quoting makes all three shell-substitution footguns literal at once). Optional
   strengthening of assertion 2; assertion 2 alone is sufficient to fail on the named gate-item-4 bug.

Pass = assertions 1 and 2 hold (3 if exercised). This proves the DC3 write contract writes its own example
content — a cost counter-hypothesis with a dollar figure and prose with a contraction — without mangling, LIVE,
through the path the seats use. P11 is able to FAIL on exactly the bare-`$` footgun it guards.

*(Design-time grounding already run by DAEDALUS — see DC3 GROUNDING RESULT above: robust single-quote form wrote
`the team's call cost $50k` intact through a live `bw comment` on throwaway ticket `stoa--ze5`; naive
double-quote mangled `$50k → 0k`. VERA re-executes P11 against a real entry on the register ticket in Phase C.)*

---

## Pointers to the unchanged design (rev1/rev2 are authoritative for these)

- **DC0 + P7** → `design-rev2.md` (single-line ` ~ ` OPTIONS; r3 folded; ARGUS-ratified, floor-manager-GO).
- **§0 / §1 / DC1 / DC2 / DC4 / DC5 / §4 / §5** → `design-rev1.md` (DC0/P7 as superseded by rev2; everything
  else as written). The §35.5 `not threat-ratified` carve-out is ARGUS-CONFIRMED and unchanged.
- **Probes P1–P6, P8–P10** → `design-rev1.md` §3 (unchanged). **P5** specifically is UNCHANGED — P11 is additive,
  not a P5 mutation.
- **Honesty stance** (no enforced/guaranteed/non-collapsible) → `design-rev1.md` §0 A3 + DC4 + DC5 honesty
  statements (unchanged).

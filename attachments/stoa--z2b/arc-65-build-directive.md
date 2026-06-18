# Arc 65 build directive — Fix the authorship-gate false-positive (z2b) without re-opening the footgun

**Audience:** the fresh Claude Code session opened to build Arc 65 (PLINY_the-stoa via the gauntlet).
**Prepared at:** the user-tier POLYBIUS (chief-of-staff) seat, with the PRINCIPAL.
**Status:** DRAFT — pending NOMOS verification before dispatch. PRINCIPAL directed: take on z2b (2026-06-18).
**Builds on:** the-stoa main `20267e4` (post-p41). Ticket: `stoa--z2b` (P1). This is a SECURITY-SENSITIVE gate change — read the constraint below before touching anything.

**You are MAJOR_PLINY for the Arc 65 engagement.** Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role. Open Claude Code in `C:\Users\denso\claude_projects\the-stoa\`.

**Your one job:** narrow the authorship-gate matcher so it stops false-positiving on `.md` BODY prose (requirement-text, §28 discipline-docs, verdict-audit prose, markdown-bold seat-attribution), **while still catching a real structured author field that names a person other than the PRINCIPAL** — the regression the gate exists to prevent. Then return cleanly.

---

## THE LOAD-BEARING CONSTRAINT (read first — this is the whole arc)

The authorship-attribution discipline is CRITICAL (global `~/.claude/CLAUDE.md`): falsely crediting another PERSON in an author/owner/creator/copyright field is a reputational + legal risk that has regressed TWICE. The gate is the mechanical backstop against it. **This arc must NOT widen the hole the gate guards.** Every change is judged on TWO directions, BOTH load-bearing:
- **Stop the false-positives** (the `.md`-body prose instances below now PASS).
- **Keep the true-positives** (a real structured author field naming a non-Denson PERSON still BLOCKS — package.json `"author"`, YAML frontmatter `author:`, LICENSE/NOTICE/CITATION.cff, etc.).

A change that achieves the first but weakens the second is a FAIL, not a partial pass. VERA's adversarial true-positive corpus is the #1 DoD.

---

## Comms — async via bw

Coordinate on `stoa--z2b`. Surface to the floor-manager (POLYBIUS_the-stoa), not user-tier direct. `bw comment <id> "text"` is **positional, no `-m`**. Run `bw prime` at activation.

---

## Read first (the spec)

1. **`stoa--z2b`** — the ticket: the false-positive root cause + the empirical instances (Arc-61 directive `**Authored by:**` + verdict V7 `author = Denson Smith; no other person...`) + the floor-manager's N+1 (Arc-64: now blocks VERDICT-record commits — CATO authorship-AUDIT prose in a verdict body). PRINCIPAL chose option (a): **narrow the matcher**; do NOT change the seat-attribution convention (b) or path-exempt (c).
2. **`substrate/hooks/_hooklib.sh`** — `extract_author_fields()`: the python regex `(?ix)(?<![A-Za-z0-9_])["']?(FIELD)["']?\s*[:=]\s*(.*)$` over FIELDS = `authors author owner creator created_by maintainers maintainer by copyright holder vendor publisher`, MULTILINE, anywhere in the blob. This greedy "anywhere + any FIELD + `:`/`=`" match is the root cause.
3. **`substrate/hooks/pretooluse-author-field-audit.sh`** — sub-check 2: `is_author_encoding_file` (matches config files + LICENSE + `*.claude-plugin/*` + **ALL `*.md`**) → `extract_author_fields` on the staged blob → `is_principal(value)` → DENY if not allow-listed. `is_principal` lower-cases + exact-matches the `principal-identity` allow-list (`denson` / `densonsmith2@gmail.com` / `Denson Smith`).
4. **`.claude/hooks/_hooklib.sh` + `.claude/hooks/pretooluse-author-field-audit.sh`** — the DEPLOYED mirrors (the-stoa is the forge; land source + deployed together). `install.sh` deploys `substrate/hooks/` → `<dest>/.claude/hooks/`.
5. **Global `~/.claude/CLAUDE.md`** "Authorship attribution" + the audit checklist (the field/file targets the gate is meant to cover — package.json, pyproject.toml, Cargo.toml, LICENSE, CITATION.cff, plugin/marketplace manifests, SKILL.md frontmatter author lines, etc.).

---

## Settled — do NOT re-litigate

- **Option (a): narrow the matcher.** The seat-attribution convention (`**Authored by:** <seat> + PRINCIPAL`) and the §28 trailer documentation stay as-is — they are CORRECT (no false person; only Denson is ever named as a person). Do NOT change the convention or add path-exemptions for `agents/verdicts/` etc.
- Config-file extraction (JSON / TOML / `package.json` / `pyproject.toml` / `Cargo.toml` / `LICENSE` / `CITATION.cff`) stays — those are structured, no prose false-positives, and they carry the highest-value true-positives.

---

## Deliverables

1. **Narrow the `.md` matching** (in `extract_author_fields` and/or the gate's `.md` handling) so author-like fields are extracted ONLY from structured-author positions, NOT `.md` body prose. DAEDALUS designs the exact strategy (see the design questions) — candidate directions: scan only the YAML frontmatter block (leading `---`…`---`) of `.md` files; AND/OR skip matches inside fenced code blocks + inline-backtick spans + markdown-bold-with-internal-colon (`**…by:**`); keep config-file structured extraction unchanged.
2. **A test corpus** (`substrate/hooks/tests/` or similar) — the load-bearing deliverable:
   - **FALSE-POSITIVE fixtures that must now PASS** (extractor returns nothing / gate allows): the Arc-61 `**Authored by:** user-tier POLYBIUS … + the PRINCIPAL (Denson Smith)`; a directive `Author=PRINCIPAL` + `Co-Authored-By: CAPTAIN_ADA_the-stoa` requirement line; a verdict body `author = Denson Smith; no other person in any author field`; §28 docs `By \`CAPTAIN_<MNEMONIC>_<slug>\`` + `Owner: the workspace's .claude/skills/`.
   - **TRUE-POSITIVE fixtures that must still BLOCK**: `package.json` `"author": "Nate Jones"`; an SKILL.md with YAML frontmatter `author: Some Other Person`; a `LICENSE`/`NOTICE` naming a non-Denson person; a `CITATION.cff` `authors:` non-Denson. Each must still DENY.
3. **Land source + deployed mirror** (`substrate/hooks/` + `.claude/hooks/`); `install.sh` deploys cleanly.
4. **Update the gate header/`.claude/hooks/README.md`** to document the narrowed matching (what it covers, what it deliberately no longer matches, and why — the body-prose carve-out).

---

## Verification / Definition of done

- **Adversarial corpus GREEN BOTH WAYS (the #1 DoD):** every FALSE-POSITIVE fixture PASSES (the 4+ real z2b instances now commit clean) AND every TRUE-POSITIVE fixture still BLOCKS. VERA runs both directions; ARGUS cold-audits for a gap a real violation could slip through.
- **Live re-probe:** stage a file containing the Arc-61 `**Authored by:**` line + a verdict authorship-AUDIT prose line → a real `git commit` is ALLOWED. Stage a `package.json` with `"author": "Not Denson"` → the commit is DENIED. (Use a throwaway branch/file; do not pollute main.)
- The gate still **FAILS-OPEN on script error** (existing design — a matcher bug must not hard-block legit commits; but note: fail-open also means a matcher bug misses violations, so robustness matters).
- `substrate/install.sh --target user --dry-run` deploys the fixed hooks; source + deployed mirror byte-consistent.
- Authorship: the build commit keeps the PRINCIPAL's configured git identity as its author, plus the §28 seat-identity trailer for the building CAPTAIN (ADA); no author-like field in any changed file names a non-PRINCIPAL person. (Ironic self-test: the fixed gate should accept this very commit's prose.)
- **NOMOS CONFORMANT** on the final commit. Committed + pushed; `stoa--z2b` updated with the landing SHA + closed.

---

## Open design questions — surface to the floor-manager at design-lock (before ADA)

- **Q-A (narrowing strategy):** frontmatter-only for `.md` (cleanest, but misses a body `Author: X` prose line) vs body-aware with code-span/bold skipping vs a value-shape heuristic (person-name vs path/seat/clause). Recommend the structural approach (frontmatter + skip code-spans/bold) over a brittle person-name heuristic — but DAEDALUS rules with ARGUS.
- **Q-B (body author lines):** does the gate need to keep catching a body `Author: <person>` line in an `.md` README (global checklist names README author lines), or is that acceptably out of mechanical scope (caught by the audit + NOMOS + human review)? Decide explicitly; do not silently drop coverage.
- **Q-C (value heuristic, optional):** whether to ALSO recognize non-person values (paths, `CAPTAIN_*`/`MAJOR_*` seats, multi-clause prose) as benign in `is_principal`'s caller — belt-and-suspenders, or scope-creep? DAEDALUS's call.

---

## Out of scope

- Changing the seat-attribution convention or adding path-exemptions (PRINCIPAL chose option a, not b/c).
- **The stashed Arc-61 directive-DoD fix** (`git stash@{0}` on main — blocked by z2b): once this arc lands and the gate accepts directive prose, the user-tier seat pops + commits it as a §18 follow-up. NOT this arc's deliverable; noted so it isn't lost.
- `stoa--9s6` / `ruu` / `p41.3-5` / `luo` — separate.

## Discipline

- Full gauntlet (DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS) — this is a SECURITY gate; the adversarial true-positive corpus is load-bearing, not a formality. Surface the design-lock (Q-A/Q-B/Q-C + the corpus design) to the floor-manager before ADA.
- A2/§35 threat-alignment: the threat is "a real author field naming a non-Denson person slips past the narrowed gate" — VERA must drive that attack path (true-positive fixtures), not just the happy path.
- Verify-then-execute; fix-now for small related defects; ticket-with-plan if scope-different.

Standby, run.

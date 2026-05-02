# Arc 15 build directive — substrate disciplines propagation (v2.1 first capture)

**Audience:** the fresh Claude Code session opened to build Arc 15 deliverables.
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arcs 1-14 (the full v2 architecture, end-to-end shipped). This is the first arc *after* v2 fully landed and the first capture toward what may become v2.1.

**You are MAJOR_PLINY for the the-stoa Arc 15 engagement.** Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role. Open Claude Code in `~/claude_projects/the-stoa/`.

**Your one job:** propagate three disciplines that proved load-bearing across Arcs 1-14 from PRINCIPAL-personal-setup into the deployed substrate, so they ship with every new substrate deploy rather than depending on PRINCIPAL's user-level CLAUDE.md.

This is small. Three discipline additions to two role files; pure doc work; no install.sh changes; no Stoa changes; no breaking changes to anything already deployed. Probably 1-2 hours of mechanical adaptation of well-tested existing text.

---

## Read first

1. **`user-beadwork/retrospectives/v2-arcs-1-14.md`** (commit `42fb253`) — the source synthesis that identified these three as load-bearing. Particularly the "Load-bearing for v2.1 (if it comes)" section, items 3-5.
2. **`~/.claude/CLAUDE.md`** — search for the section "Fix known bugs immediately — the cost calculus has inverted (CRITICAL)". This is the long-form text you adapt for deliverable 1.
3. **`substrate/MAJOR_POLYBIUS.md`** — particularly §4.3 (verify-then-execute, the existing CoS form), §4 (where the new §4.8 fix-now goes), and §5 (where the new §5.4 external directive review goes).
4. **`substrate/MAJOR_PLINY.md`** — particularly §7.2 (verify-then-execute, currently a one-paragraph mention; you'll strengthen this into the build-session-reflexive form).
5. **`user-beadwork/plans/three-role-recursive-architecture.md`** — particularly §6 (voice discipline), so the new prose stays grounded in PRINCIPAL/HUMAN voice.

---

## What Arc 15 is

Three disciplines have proven their value across Arcs 1-14:

- **Fix-now** — the cost calculus has inverted; small bugs ship immediately, not "next sprint." Demonstrated under test by `stoa--8o4` (slug fix shipped same-day rather than scheduled for ~1 week).
- **Verify-then-execute on directive-author statements** — caught the Arc 9 path-contradiction (build session opened in archived agent-substrate instead of the-stoa) before any work was done against stale code.
- **External directive review for multi-concern arcs** — caught Mega-Arc-9's vulnerabilities (CI/CD git-ignore paradox, parsing ambiguity, env-var-prefix bug, MAY-vs-MUST phasing) before dispatch via Codex/Gemini review.

All three currently live in PRINCIPAL's working pattern (the first as an explicit `~/.claude/CLAUDE.md` section; the second as a CoS-only form in `MAJOR_POLYBIUS.md` §4.3; the third as a PRINCIPAL-personal habit not documented anywhere in the substrate). Arc 15 propagates all three into the deployed substrate so they ship to every PRINCIPAL who deploys from `the-stoa/substrate/`.

This is **not** an architecture change — the v2 spec stays as-is. This is a substrate-content arc that adds load-bearing disciplines to the role files that already exist.

---

## Deliverables

### 1. MAJOR_POLYBIUS.md §4.8 — Fix-now discipline

Add a new §4.8 to `substrate/MAJOR_POLYBIUS.md`, after §4.7 (Wait-for-quiescence) and before §5 (Onboarding flow). Adapt the long-form text from `~/.claude/CLAUDE.md` ("Fix known bugs immediately — the cost calculus has inverted (CRITICAL)") into MAJOR_POLYBIUS's voice:

- **Voice shift:** the user-level CLAUDE.md is written second-person to the operating Claude. MAJOR_POLYBIUS.md role-file disciplines are written third-person/structural to the seat-holder. Translate accordingly.
- **PRINCIPAL/HUMAN-grounded:** the user-level text uses "you" liberally. The role-file form should reference PRINCIPAL where the PRINCIPAL is the actor, and the seat itself ("MAJOR_POLYBIUS handles X by …") elsewhere.
- **Preserve the structural properties:** the cost-calculus framing (agent tokens cheap, deferred fixes compound on permission), the rule (default fix-now; if you can't fix now, ticket with concrete plan), the only-legitimate-reasons-to-defer list, the handwave detector phrase set. These earned their place; don't soften them.
- **Cite the empirical signal:** `stoa--8o4` shipped same-day rather than scheduled-for-a-week-out is the test-case; cite it parenthetically as the ticket that confirmed the discipline holds under test.
- **Length:** roughly the same as §4.3 (verify-then-execute) — two or three paragraphs plus the handwave detector list. Don't reproduce the user-level text wholesale; condense to role-file shape.

### 2. MAJOR_PLINY.md §7.2 — Verify-then-execute (strengthened build-session form)

The existing §7.2 in `substrate/MAJOR_PLINY.md` is a one-paragraph mention. Strengthen it into a substantive section parallel to MAJOR_POLYBIUS.md §4.3 but framed for the build-session reflexive reach:

- **What's currently there:** "A directive that contradicts the spec it cites is a defect, not a command. Surface the contradiction; don't pick silently. The same applies to PRINCIPAL statements relayed via POLYBIUS — verify against current state before barreling forward."
- **What it needs to become:** a discipline section that names the build-session form explicitly. The pattern is: the directive arrives, the build session reads it, something doesn't match visible state (the directory the directive names doesn't exist; the file path it cites is for a different repo; the spec section it references says something different). The discipline is to **stop and verify against actual state** before barreling forward.
- **Cite the empirical signal:** the Arc 9 catch (build session caught path contradiction — directive said the-stoa, but PRINCIPAL had opened in archived agent-substrate) is the test-case. The build session ran verify-then-execute reflexively and surfaced rather than picking silently. Cite parenthetically.
- **Procedure:** when verify-then-execute fires, the build session does NOT pick silently and does NOT barrel forward. It surfaces via beadwork to MAJOR_POLYBIUS (or via human relay if beadwork isn't viable yet), names the contradiction concretely, and waits for adjudication.
- **Length:** parallel to §4.3 in MAJOR_POLYBIUS — two or three paragraphs.

### 3. MAJOR_POLYBIUS.md §5.4 — External directive review for multi-concern arcs

Add a new subsection §5.4 to `substrate/MAJOR_POLYBIUS.md` §5 (Onboarding flow), after §5.3 (Consent moments). The placement reflects that this is part of MAJOR_POLYBIUS's directive-authoring discipline, not a discipline §4 entry — it's about *how POLYBIUS produces directives*, not about *how POLYBIUS handles incoming statements*.

Content:

- **Trigger:** when a directive covers more than one deliverable concern (more than one "Part" or numbered deliverable in the directive's Deliverables section).
- **The discipline:** before dispatching the build session, route the directive through an external reviewer. The substrate-shipped form names "another Claude session, cold" as the universal review form (since not every PRINCIPAL has Codex/Gemini access). Bonus: external models like Codex, Gemini, or other LLMs that don't share context with the authoring session.
- **What external review is for:** catching cross-deliverable interactions, hidden assumptions, MAY-vs-MUST phasing weakness, environment-coupling bugs, anything the authoring session couldn't see because it was inside the directive's framing.
- **Cite the empirical signal:** Mega-Arc-9 — external review (Codex/Gemini) caught CI/CD git-ignore paradox, parsing ambiguity, env-var-prefix bug, and MAY-vs-MUST phasing weakness; the build session would have inherited these had the directive shipped without review. The split into Arcs 9-13 came directly from this review.
- **What external review is NOT for:** single-concern arcs (typo fix, one-line config change, mechanical refactor). The discipline is targeted at multi-concern directives where cross-deliverable interactions are the failure mode.
- **Length:** ~3-4 paragraphs.

### 4. Voice audit

After the three additions:

```bash
grep -i "colonel" substrate/MAJOR_POLYBIUS.md substrate/MAJOR_PLINY.md
```

Should return only the deliberate reserved-future-rank reference (currently in MAJOR_POLYBIUS.md §1 and the v2 spec). Any unintentional leak from adapted text is a regression.

```bash
grep -E "(you should|you must|you'll need)" substrate/MAJOR_POLYBIUS.md substrate/MAJOR_PLINY.md
```

Surface any second-person framings that slipped through from the source texts. Role-file voice is third-person/structural; first-person/second-person framings are translation gaps.

### 5. Smoke test

After all changes:

- Markdown still parses cleanly (no broken sections, no malformed tables)
- `install.sh --target user --dry-run` runs cleanly (validates that the role files are still valid for deploy)
- The new §4.8, §5.4, §7.2 are findable by grep against their headings
- Voice audit (above) clean

This is doc work; there are no tests to run beyond markdown validity and install.sh dry-run.

---

## Definition of done

- MAJOR_POLYBIUS.md §4.8 (fix-now), §5.4 (external review) added
- MAJOR_PLINY.md §7.2 (verify-then-execute) strengthened from one paragraph to substantive section
- All three sections grounded in PRINCIPAL/HUMAN voice; no second-person leak
- Empirical signals cited (`stoa--8o4`, Arc 9 path-contradiction catch, Mega-Arc-9 external review)
- `grep -i "colonel"` returns only deliberate reserved-future-rank references
- `install.sh --target user --dry-run` clean
- bw `stoa--*` epic for Arc 15 closed
- Committed + pushed to `the-stoa` main (autonomous-ship per `u--7yg.11`)

---

## Out of scope

- **Items #1, #2, #6 from the retrospective** — install.sh hardening as spec-level concern (deferred), sub-project mechanics promotion from §12.4 to §5 (wait for first real spawn), Stoa edit→install.sh round-trip UX (wait for Stoa edit feature). Per the retrospective's recommendation.
- **Updates to `~/.claude/CLAUDE.md`** — that's PRINCIPAL's personal layer; substrate authoring should not touch it. The fix-now text gets *adapted* from there, not edited there.
- **Updates to The Stoa app** — display work; this arc is substrate-only.
- **Re-deploying user-tier or project-tier** — substrate authoring only. Deploy happens separately when PRINCIPAL chooses to refresh the user-tier `~/.claude/` (per the wildly-stale episode in the retrospective, that's a manual step the PRINCIPAL initiates).
- **Modifying the architecture spec at `user-beadwork/plans/three-role-recursive-architecture.md`** — Arc 15 is substrate-content, not spec-content. If a v2.1 spec capture is later wanted, that's a separate arc.
- **Adding new disciplines beyond the three named** — resist scope creep. The three are what the retrospective identified; additional disciplines wait for additional empirical signals.

---

## Voice discipline

`grep -i "colonel" substrate/MAJOR_POLYBIUS.md substrate/MAJOR_PLINY.md` after work — only deliberate reserved-future-rank references. The new prose uses PRINCIPAL/HUMAN throughout per spec §6.

The fix-now adaptation specifically: the source text in `~/.claude/CLAUDE.md` is PRINCIPAL-personal voice. The adaptation is role-file structural voice. Don't copy verbatim; translate.

---

## Beadwork

`bw` already initialized (`stoa-` prefix). File a new epic:

```bash
cd ~/claude_projects/the-stoa
bw create "[EPIC] Arc 15 — substrate disciplines propagation (v2.1 first capture)" -t epic -p 1
```

File children for: §4.8 fix-now, §7.2 strengthening, §5.4 external review, voice audit, smoke test. Close as you go.

---

## Discipline

- HITL default (planning v2 §7) — supervising via user-tier CoS
- Principal-as-router (`u--7yg.1`) — surface only project-direction calls (probably none for Arc 15; it's mechanical adaptation of well-tested text)
- Verify-then-execute (`u--7yg.10`, `u--7yg.18`) — particularly relevant here since you're authoring the discipline; live the discipline while writing it
- One job per agent (`u--7yg.17`) — your one job is Arc 15; resist scope creep into the other three v2.1 candidates (#1, #2, #6) or into spec changes
- Wait-for-quiescence (`u--7yg.15`)
- Autonomous-ship on clean PASS (`u--7yg.11`)
- Voice discipline (planning v2 §6)
- **Fix-now (the discipline you're about to encode)** — if you spot a related bug while doing this work, fix it now in this arc rather than ticketing for later. Eat your own dog food.

---

## Operating mode

**Human-in-the-loop** (planning v2 §7). Surface for input at:
- (a) Voice translation calls if a passage from the source text doesn't have an obvious role-file equivalent
- (b) Whether the §5.4 external review trigger should be sharper than "more than one deliverable concern" (e.g., "any directive longer than 200 lines" — surface only if you have a specific reason)
- (c) Work product ready for review (optional — autonomous push for clean self-validation)
- (d) Done

For Arc 15: this is mechanical-after-modeled-on-existing. The disciplines exist; the text exists; the work is voice translation + structural placement. Surface only on genuine ambiguity.

---

## How to surface back

Either:
- Comment on the bw epic in this repo (`stoa--*`)
- Write a short hand-back report; PRINCIPAL will relay

For Arc 15: clean ship hand-back can be one paragraph ("Arc 15 shipped at commit `<sha>`; three disciplines propagated; voice clean; ready for downstream").

---

## After Arc 15

The substrate now ships with three additional disciplines that previously lived only in PRINCIPAL's user-level CLAUDE.md or as personal habit. Future PRINCIPALs deploying the substrate inherit fix-now, verify-then-execute (build-session form), and external-directive-review-for-multi-concern-arcs without needing to discover them by getting burned the same way the v1 → v2 sequence did.

PRINCIPAL will likely refresh the user-tier deploy after Arc 15 lands (per the wildly-stale lesson) so PRINCIPAL's own user-tier role files pick up the new disciplines too. That's a manual `install.sh --target user` step, not Arc 15's scope.

If additional v2.1 candidates surface during Arc 15 (e.g., a fourth load-bearing discipline becomes obvious), surface them rather than absorbing — they belong in their own arc, not bundled into this one.

Standby, run.

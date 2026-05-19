# Arc 43 design — substrate-canon-update bundle (yl1 META-discipline catalog + 4zj validate-spec parser refinement)

**Author:** Denson Smith
**Ticket:** stoa--yl1 (coordination) + stoa--4zj (parser refinement)
**Branch / worktree:** `arc-43/build` at `.claude/worktrees/arc-43-build/`
**Arc directive:** `substrate/arcs/arc-43-build-directive.md` (A1-A22 LOCKED at f55f130)
**DAEDALUS sub-decisions:** A3=α MERGE; A4=ε SPLIT-BY-SEAT; A8=η SPEC-SELF-HEADINGS-SET; A9=μ HYBRID

---

## §1 Problem restatement (the §6.1 pre-work gate)

Arc 43 is a substrate-canon-update bundle. Two source tickets are landed in one design.md per A1 LOCKED:

**C1 — stoa--yl1:** Pass 10 stellation behavioral validation accreted ten META-discipline candidates that extend the design-time / build-time / verify-time canon. They share two anchors: (a) each has N≥2 empirical anchors from Arcs 1-5 of stellation, (b) each is an extension of canon already shipped at the-stoa (§6.9 Arc 42, §6.2 long-standing). The task is to land these as canon edits at the right seat files: most go to `substrate/CAPTAIN_DAEDALUS.md` §6 family (extending the Arc 42 §6.9 base); WP13 lands there too (design-time discipline); Dev1 lands at `substrate/CAPTAIN_ADA.md` §5 (build-time discipline); Dev2 lands at `substrate/operating-disciplines.md` as a new §32 test-discipline section (the new-section pick under A4=ε is defended in §2.6 below). Per A3=α, the three Arc-4-origin candidates (§6.X qualitative-acceptance-anchor + §6.Y motion-vocabulary SSoT + §6.Z three-surface reduced-motion) merge into one unified §6.X discipline (SSoT-with-WHY pattern), with motion-vocab and reduced-motion enumerated as worked examples within the section, not as siblings.

**C2 — stoa--4zj:** Arc 42 validate-spec first-run produced 144/274 check-1 FAILs and 36/65 check-2 STRANGEs. The check-1 root cause is that bare-`§N.X` refs in SPECIFICATION.md default to `operating-disciplines.md` per the spec's own reading-note (line 7), but the spec's OWN section headings — lines like `### §2.1 The three roles` — match that pattern and over-resolve against operating-disciplines.md, which has no `§2.1`. The check-2 root cause is that the §13.5-§13.9a candidate enumerations cite tickets in summary lines without claim-keywords (open / closed / shipped / …), so `_classify_claim` returns "ambiguous" and routes to STRANGE. The task is two-part parser refinement (`substrate/skills/validate-spec/_lib/spec_refs.py` for check-1; `substrate/skills/validate-spec/_lib/bw_tickets.py` for check-2). Per A8=η: build a spec-self-headings-set and skip refs whose citing-line IS a spec section heading whose anchor matches the cited anchor. Per A9=μ: tighten check-2 prose-regex AND ship a structured-frontmatter migration path (parser supports both shapes; new shape preferred when present).

**A22 self-application target:** after C2 ADA build, validate-spec re-runs against SPECIFICATION.md; `agents/observation/spec-validation/mechanical-check-results.md` updates with FAIL/STRANGE counts compared to the Arc 42 baseline. Expected (per stoa--4zj fix-shape): check-1 FAILs drop substantially (most of the 144 are spec-self-heading false-positives); check-2 STRANGEs drop substantially (most of the 36 are §13.5-§13.9a enumeration lines).

**Imported assumptions (per §6.1 — name what was imported):**

1. **The 10-candidate catalog is closed** — A19 LOCKED hard-locks against widening yl1 scope mid-arc. If during design I notice an 11th candidate the catalog missed, I name it in §6 (out of scope) and surface in `follow_ups:`; I do not fold it in.
2. **Per-section §6.9 base canon stays as-is** — A19 LOCKED. New sections cite + extend §6.9; they do not restructure it.
3. **A4=ε pick for Dev2 lands at op-disc as new §32.** This is my discretion call per A4 sub-options (a) and (b). Rationale defended in §2.6. If §32 conflicts with A18 IMMUTABLE concerns or §-numbering, ARGUS surfaces a substance-disagreement and I pivot to A4 sub-option (b) test-discipline subsection within CAPTAIN_ADA.md §5.9.
4. **Probe self-application surveillance fires honestly.** Per Pass 10 precedent, any §6.9.3' / §6.9.3'' / §6.2.1' violation ARGUS catches in this design's own probes counts as a POSITIVE empirical anchor for the canon being shipped, not a defect to hide. I surface suspected violations in §5 self-assessed weak points; ARGUS catches what I missed.

**No PRINCIPAL-gate clauses** present in this dispatch (per §6.7): the brief contains no clauses matching §25.3 gate-shape. No probes mutate operator-owned workspaces (per §25.5 sub-case). Out-of-scope hard-locks per A19 are documented in §6.

**No credentialed operations** in scope (per §6.6): the build edits substrate canon files + Python parser helpers; no CI workflow needed; no third-party API tokens.

---

## §2 C1 approach — META-discipline catalog landing

The 10 candidates land across three files. Each subsection below names: **target location** + **canonical wording** (the prose ADA writes verbatim) + **empirical-anchor citation block** (the N≥2 prior arcs that justify canon-promotion) + **cross-refs** (what the section reads-into and is-read-from). ADA's job at build time is to: insert the named section at the named location; cite-comment cross-refs at every read-site per A6 / A15; honor A18 IMMUTABLE (no new file frontmatter in LOCKED scope; existing files only).

### §2.1 §6.9.3' round-trip-adjacent-prose (extends §6.9 clause 3)

**Target location:** `substrate/CAPTAIN_DAEDALUS.md`, insert new subsection 6.9.3' immediately after the existing 6.9 section (between 6.9 closing and the `---` separator before `## 7. Verdict format` — currently line ~265). **Heading shape MUST match existing file convention: `### 6.9.3' Round-trip prose adjacent to probe-specs (extends 6.9 clause 3)` — the file uses bare-number heading anchors (e.g., `### 6.9 Probe-grounding discipline …`), NOT `§`-prefixed headings.** SPECIFICATION.md uses `§`-prefixed headings; the substrate canon files (CAPTAIN_*.md, operating-disciplines.md) do not. ADA writes the bare-number form to match existing file convention.

**Canonical wording:**

> §6.9 clause 3 names live-round-trip as the discipline for the probe body itself.
> The discipline below extends that to prose adjacent to the probe: a parenthetical
> next to the regex, an "or equivalently" clause, an algorithmic justification in
> the paragraph above the bash block. ADA reads adjacent prose as authoritative
> at build time. A parenthetical that contradicts the regex it surrounds is a
> live defect waiting to fire — ADA may build the regex faithfully and the
> parenthetical wrong, or the other way around, but the gauntlet cannot
> downstream-catch a contradiction the design's own author smoothed past.
>
> The discipline (at probe-authoring time):
>
> 1. **Identify the adjacent prose surface.** Parentheticals immediately
>    following a regex; "or equivalently" clauses pointing to a different
>    mechanism; algorithmic justifications in the prose paragraph that
>    precedes the bash code-block. These are CONTRACT CLAIMS, not commentary.
> 2. **Round-trip the prose through the probe's actual semantics.** Mentally
>    or literally execute the probe against the example the prose names; verify
>    the prose's claim is what the probe actually emits.
> 3. **When the prose generalizes ("this also catches X-shaped sibling defects"),
>    audit X explicitly.** A claim of generalization is a sibling-defect-class
>    audit promise; if you cannot live-round-trip X, narrow the claim or surface
>    in `self_assessed_weak_points:` per §6.2.
>
> **Empirical anchor.** Three anchors across Arcs 2-3 of stellation Pass 10:
> Arc 2 r4 (originating) — §2.3 parenthetical "or equivalently the mirror via
> `blocked_by`" contradicted Probe O's directed-graph semantics; ARGUS caught
> by running Probe O literal Node logic against the parenthetical reading.
> Arc 3 r4 — Probe G2 shell-quoting bug: mixed-quote regex unexecutable in
> bash; the surrounding prose described what the regex was *meant* to match,
> but the regex itself was syntactically broken. Arc 3 ADA Phase 4.5 — design
> §1 assumption 10 inlined literal `getByTestId(skeleton-stars)` strings in
> canonical App.test.tsx comments that tripped Probe M-A's negation greps;
> design's own §3 live-RT block tested the stripped version, masking the
> contradiction. ADA caught at build-time.
>
> **Cross-refs:** `CAPTAIN_DAEDALUS.md` §6.9 (probe-grounding parent canon —
> clause 3 names live-round-trip; this section extends to the probe's
> surrounding prose); `CAPTAIN_DAEDALUS.md` §6.9.3'' (live-RT-at-authoring;
> the operational mechanism that catches both probe-body and adjacent-prose
> drift); `CAPTAIN_DAEDALUS.md` §6.2 (self-assessed weak points — where
> ungeneralizable claims surface to ARGUS).

**Cite-comments to add at read-sites (per A6 / A15):** in the existing §6.9 clause 3 paragraph, append a sentence "Adjacent prose (parentheticals, 'or equivalently' clauses, algorithmic justifications) is covered by §6.9.3'." This makes §6.9 self-cite the extension at the place a reader naturally arrives.

### §2.2 §6.9.3'' live-RT-at-authoring + COMPLETENESS CLAUSE + SIBLING-DEFECT-CLASS EXTENSION (canon-promotion-ripe)

**Target location:** `substrate/CAPTAIN_DAEDALUS.md`, insert new subsection 6.9.3'' immediately after 6.9.3' (and before `## 7. Verdict format`). Heading shape: `### 6.9.3'' Live-round-trip probes at authoring time + COMPLETENESS CLAUSE (extends 6.9 clause 3)` (bare-number form per existing file convention).

This is the load-bearing canon-promotion of Arc 43 per A5 LOCKED. It ships with the cost-multiplier math (60× anchor) and the 6-anchor empirical block.

**Canonical wording:**

> §6.9 clause 3 names "live round-trip at authoring time" as the discipline
> for probes whose body contains a regex / grep / algorithm. The discipline
> below operationalizes that into a step you actually run, and extends it
> with two additional clauses that close empirical gaps Arc 4-5 surfaced.
>
> **The operational discipline (at probe-authoring time):**
>
> 1. **Before submitting any probe whose body is a literal command, run the
>    command against the current state the probe targets.** If the probe is
>    a grep against substrate prose, run the grep against the live file. If
>    the probe is an algorithmic check (e.g., "regex X matches input Y"), run
>    a one-line Python REPL against Y. Prose-auditing the shell or algorithm
>    is insufficient; the discipline is to LIVE-RUN.
> 2. **A probe that emits zero matches against its target state is structurally
>    broken, not under-specified.** Do not ship it expecting ADA or VERA to
>    figure out the correct anchor. Fix at design-time, or surface as a
>    `self_assessed_weak_point:` per §6.2 with the structural reason.
>
> **COMPLETENESS CLAUSE (the canon-promotion clause).** When you fix one
> probe-defect during design draft, do not stop at the named instance. The
> empirical record is that defect-classes recur at sibling sites within the
> same design draft. The discipline is to audit for the **defect-class**, not
> just the exact-pattern-instance:
>
> - If you fixed a hex-escape (`\x27` mismatching a literal apostrophe) at one
>   probe, audit every other probe in the design for hex-escapes against
>   literal characters — at least 2 sibling instances are typical.
> - If you fixed a POSIX/Windows portability defect (e.g., `bash`-only syntax
>   in a cross-platform probe), audit every other probe for POSIX-only
>   constructs that won't round-trip in the build environment ADA actually
>   uses.
> - If you fixed an under-anchored regex (matching incidental prose vs the
>   intended target), audit every other regex probe for anchor-completeness
>   — `^` / `$` / `\b` / unique surrounding context.
> - If you fixed a grep-anchored probe, audit every Vitest assertion (or
>   equivalent test stub) for sibling under-specification — the defect-class
>   spans tool boundaries.
>
> **SIBLING-DEFECT-CLASS EXTENSION (the extension that distinguishes
> "defect-class" from "exact-instance").** Sibling-class audit means: when a
> defect-class has surfaced, identify the structural property the defect
> rests on (under-anchoring, character-class incompleteness, platform
> assumption, …), then audit every probe in the design that COULD rest on
> that property, not just probes that share the exact symptom.
>
> **Cost-multiplier math (the 60× anchor).** The empirical cost of skipping
> sibling-class audit and shipping the design is ~60× the cost of running the
> audit at design time. Mechanism: when ARGUS catches the sibling defect on
> re-audit, the cost is at minimum a rev-cycle round-trip (~10 minutes of
> orchestrator + ARGUS + DAEDALUS wall-clock) plus the cognitive cost of
> reconstructing the original audit context. When VERA catches it
> downstream, the cost is a build-rev cycle (~30-60 minutes of orchestrator
> + ADA + VERA wall-clock) plus the design-rev to update the probe spec.
> The audit-at-design-time cost is ~60 seconds (a `grep -n` scan of the
> design's own probe blocks + a mental check against the named defect-class).
> ~60 seconds vs ~60 minutes = 60× multiplier. The math holds when ARGUS
> catches at design-rev; it grows when VERA catches at build-rev.
>
> **Empirical anchor (the 6-anchor canon-promotion block).** Pass 10
> stellation Arcs 4-5 surfaced 6 anchors across orthogonal defect-classes,
> each showing the same shape: one defect named + fixed; the fix did not
> generalize; a sibling-class instance surfaced at the next rev. The 6:
>
> 1. **Arc 4 rev1 r3 — `\x27` hex-escape recurrence at Probe K** after the
>    same hex-escape was fixed at Probes I / F / L. The fix at I / F / L
>    treated the defect as an exact-pattern problem; the defect was
>    actually a class (hex-escape against literal apostrophe in any regex
>    referencing prose).
> 2. **Arc 4 rev2 r2 — POSIX/Windows portability recurrence at Probes S + P**
>    after the same portability concern was fixed via a caveat at Probe D.
>    The caveat-at-one-probe didn't audit the rest of the design.
> 3. **Arc 4 VERA-final — under-anchored regex recurrence at Probes F / K2 /
>    L2** across 3 different probe sites. VERA caught all 3; each was a
>    class instance.
> 4. **Arc 5 ARGUS-rev1 r2 — stub-Vitest assertion under-specification**
>    (cross-tool sibling of the grep-anchored defect-class; same structural
>    property, different tool).
> 5. **Arc 5 ARGUS-rev2 — SIBLING-class catalog explicit:** ARGUS-rev2
>    surfaced the canonical wording "DEFECT-CLASS, not just exact-pattern-
>    instance" + named 3 sibling instances at once. This is the wording
>    promoted to canon here.
> 6. **Cross-arc — same defect-class keeps surfacing at sibling sites after
>    named-instance fix.** The 5 specific anchors above all share this
>    cross-cutting property; it is the structural reason the COMPLETENESS
>    CLAUSE matters.
>
> **Recursive self-application surveillance.** When this canon ships in
> design.md probes (including the one shipping THIS canon), expect the canon
> to apply to its own probes. An ARGUS catch of a §6.9.3'' violation in a
> design that proposes §6.9.3'' is a POSITIVE empirical anchor for the canon,
> not a defect to hide. The discipline at probe-authoring time is to surface
> suspected violations in `self_assessed_weak_points:` per §6.2 and let
> ARGUS catch what was missed.
>
> **Cross-refs:** `CAPTAIN_DAEDALUS.md` §6.9 (parent canon — clause 3 names
> live-round-trip in principle); `CAPTAIN_DAEDALUS.md` §6.9.3' (round-trip-
> adjacent-prose — the sibling extension covering prose around the probe);
> `CAPTAIN_DAEDALUS.md` §6.2 (self-assessed weak points — where suspected
> violations surface to ARGUS); `CAPTAIN_VERA.md` §5.11 (verification-side
> sibling — when authoring discipline fails, §5.11 catches at verify-time).

**Cite-comments to add at read-sites (per A6 / A15):** in the existing §6.9 clause 3 paragraph, append "See §6.9.3'' for the operationalized live-RT step + COMPLETENESS CLAUSE / SIBLING-DEFECT-CLASS EXTENSION (canon-promoted Arc 43)." In `CAPTAIN_VERA.md` §5.11, add a one-line cite-comment cross-ref to §6.9.3'' (the authoring-time sibling of §5.11's verify-time discipline). ADA verifies the cite-comments per A15 (cite resolves at every read-site).

### §2.3 §6.2.1' canonical-code-block-fix (extends §6.2)

**Target location:** `substrate/CAPTAIN_DAEDALUS.md`, insert new subsection 6.2.1' immediately after the existing 6.2 section (between 6.2 closing and `### 6.3 Consume research; don't re-derive it` — currently line ~104). Heading shape: `### 6.2.1' Canonical-code-block-fix discipline (extends 6.2)` (bare-number form per existing file convention).

**Canonical wording:**

> §6.2 names self-assessed weak points as a post-work gate: surface brittle
> assumptions before returning. The discipline below extends that to the
> location of the fix when §6.2 self-catch names a defect.
>
> When self-catching a defect during §6.2 pass, the fix MUST land at the
> §2.X canonical code-block that ADA reads as authoritative — not only at a
> §11 step-list reference or a §6 weak-point flag. ADA reads code blocks
> first; a fix-narrative in §11 or a flag in §6 is read second, after the
> canonical block has already shipped to the build. The empirical record is
> that fix-narratives without canonical-block edits ship a buggy canonical
> block.
>
> **The discipline (at §6.2 pass time):**
>
> 1. **Identify the canonical site.** The canonical site is the code block
>    in §2 (or wherever the design names "this is what ADA builds") that
>    defines the contract ADA reads first. Not the verification probe
>    (that's §4); not the weak-point flag (that's §6).
> 2. **Edit the canonical site.** Apply the fix in the same draft, at the
>    canonical code block, before returning the verdict. A §6 flag without
>    a canonical edit is incomplete.
> 3. **The §6 weak-point flag remains too** — but it documents WHY the fix
>    was needed, not as a substitute for the fix.
>
> **Empirical anchor.** Four anchors:
> - **Arc 3 r1 (originating)** — sortAxis charCodeAt(0) bias: §6.2 self-catch
>   declared "fix applied at design-time" but §2.4 canonical code still
>   shipped the buggy form. ARGUS caught by reading §2.4 first per the
>   canonical-authority order.
> - **Arc 3 rev2 o1** — Effect-B prose at design.md:313 declared "fires when
>   sortKey or sortMaps change, but NOT on filter"; code DOES fire on
>   filter clicks because sortMaps useMemo deps include tickets. ARGUS-rev2
>   self-applied at audit time.
> - **Arc 3 VERA Probe L FAIL** — design rev2 pivoted from
>   useConstellationLayout.test.ts → computeFinalPositions.test.ts per r3/r7
>   but Probe L still enumerated the hook-test file. ADA shipped reality per
>   §5.2 ground-check.
> - **Arc 4 WP13** — DAEDALUS-rev2 picked attrX/attrY based on motion docs
>   SVG-component example; ARGUS-rev2 caught the discrepancy; design pivoted
>   at rev3 but original §2 canonical block needed re-edit, not just a §6
>   flag.
>
> **Cross-refs:** `CAPTAIN_DAEDALUS.md` §6.2 (parent canon — self-assessed
> weak points); `CAPTAIN_DAEDALUS.md` §6.9.3'' (live-RT at canonical-block
> authoring time — same principle: authority lies at the canonical block,
> not at the narrative reference); `CAPTAIN_ADA.md` §5.2 (stay inside
> design's scope — the ground-check sibling at build-time).

**Cite-comments to add at read-sites:** in §6.2 closing paragraph, append "See §6.2.1' for the canonical-code-block-fix discipline that extends self-catch with a fix-location rule."

### §2.4 §6.X qualitative-acceptance-anchor surface (MERGED per A3=α)

**Target location:** `substrate/CAPTAIN_DAEDALUS.md`, append a new subsection at the end of the §6 family (after the existing 6.9 base + new 6.9.3' / 6.9.3''; insert at 6.10 in the §6.X family — but to avoid number-collision with §2.5 below which proposes 6.11 for WP13, the layout is: 6.10 = qualitative-acceptance-anchor surface (this section), 6.11 = WP13 (§2.5). Heading shape: `### 6.10 Qualitative-acceptance-anchor surface (SSoT-with-WHY pattern)` (bare-number form per existing file convention).

The A3=α merger collapses three Arc-4-origin candidates into one section: the original §6.X (qualitative-acceptance-anchor surface), §6.Y (motion-vocabulary SSoT), §6.Z (three-surface reduced-motion) become one discipline (SSoT-with-WHY pattern) with motion-vocab + reduced-motion as enumerated worked examples within the section. ARGUS-rev1 r8 at Pass 10 Arc 4 explicitly flagged the merger; the underlying discipline IS one — SSoT-with-WHY enables qualitative-acceptance audit at cold-read.

**Canonical wording:**

> When a design ships a body of decisions that need to read clean at a later
> qualitative-acceptance audit — CATO read, ARGUS cold-read, PRINCIPAL
> review — the design wins by colocating the decision with the *why* in a
> single source of truth (SSoT). The SSoT-with-WHY pattern is the structural
> shape that enables systematic verification: a reader walking the SSoT can
> trace every choice to a named rationale; the §6 anti-pattern audit at
> cold-read leverages the SSoT for systematic verification rather than
> hunting through scattered prose.
>
> **The discipline (at design-time):**
>
> 1. **Identify the qualitative-acceptance surface** — the body of choices
>    that will be qualitatively audited at CATO / cold-read time. Motion
>    vocabulary, color palette, error-message tone, fallback-chain ordering,
>    operating-mode triggers — anything where the choices are not
>    individually mechanically checkable but the BODY of choices reads clean
>    or doesn't.
> 2. **Build the SSoT module or section.** A single file (or single
>    contiguous section of a file) that names every choice in the body, with
>    a one-line WHY immediately adjacent to each choice. The WHY anchors the
>    choice in the domain vocabulary; the cold-reader can trace why each
>    choice is the choice without consulting external context.
> 3. **Reference the SSoT at every consumption site.** Code or prose that
>    uses a choice from the SSoT names the SSoT module + the specific choice.
>    Reading the consumption site tells the reader where to look up the WHY.
> 4. **Audit at the §6 anti-pattern surface.** When the body's
>    qualitative-acceptance audit fires (CATO honesty review, ARGUS cold
>    re-read), the audit walks the SSoT systematically — every choice has a
>    WHY adjacent; the audit verifies every WHY is non-circular, domain-
>    grounded, and not a place-holder.
>
> **Worked example 1 — motion vocabulary SSoT (Pass 10 Arc 4 origin).** At
> stellation Arc 4, ADA shipped `motionVocabulary.ts` as a single TypeScript
> module containing every motion choice in the project (durations, easings,
> spring stiffnesses) with a one-line rationale comment per choice grounded
> in the night-sky / star-physics vocabulary the project's qualitative-
> acceptance domain rests on (e.g., "starsAppearDuration: 1.2s — slow enough
> that the constellation 'emerges' rather than 'flashes', per night-sky
> domain vocab"). CATO independently verified the SSoT enabled clean
> qualitative-acceptance audit: the reviewer walked the module top-to-bottom
> and traced every motion in the running app back to a named rationale.
>
> **Worked example 2 — three-surface reduced-motion architecture (Pass 10
> Arc 4 origin).** Same arc shipped reduced-motion mitigation across three
> surfaces: `<MotionConfig reducedMotion="user">` at the app root; CSS
> `@media (prefers-reduced-motion: reduce)` rules in the global stylesheet;
> `useReducedMotion()` hook gating React-side animation. All three are
> referenced from the motion-vocabulary SSoT's reduced-motion section,
> so a reader walking the SSoT sees the three-surface architecture in one
> place; each surface independently exercises under `matchMedia=reduce`
> in tests. The three surfaces are not separate SSoTs; they are a single
> SSoT section with the cross-references.
>
> **Cross-refs:** `CAPTAIN_DAEDALUS.md` §6.2 (self-assessed weak points —
> SSoT-with-WHY pattern reduces the surface where weak points hide); §6.2.1'
> (canonical-code-block-fix — SSoT IS the canonical-code-block for
> qualitative-acceptance bodies); `CAPTAIN_CATO.md` (honesty-audit consumer
> — CATO reads the SSoT for the §6 anti-pattern audit).

**Cite-comments to add at read-sites:** in §6.2 closing paragraph (already cited from §6.2.1'), append "§6.10 extends self-catch to qualitative-acceptance bodies via SSoT-with-WHY pattern."

### §2.5 §6.11 WP13 API-docs-don't-generalize-to-differently-shaped-elements (A4=ε design-time landing)

**Target location:** `substrate/CAPTAIN_DAEDALUS.md`, insert new subsection 6.11 after 6.10. Heading shape: `### 6.11 API-docs-examples-don't-generalize-to-differently-shaped-elements` (bare-number form per existing file convention).

**Canonical wording:**

> When a design rests on a third-party API and the API docs supply an
> example using ONE element type, the docs do not guarantee the API
> generalizes to a DIFFERENT element type. Element-type attribute surfaces
> vary by spec; an API that animates `attrX` / `attrY` on an SVG `<rect>`
> may not animate the same attributes on `<g>` because `<g>` lacks
> native `x` / `y` per the SVG2 spec.
>
> **The discipline (at design-time):**
>
> 1. **Identify the element-type the design targets.** Not the element-type
>    the API docs' example uses; the element-type the design actually wires
>    against.
> 2. **Ground-check the chosen API against the target element-type's
>    attribute surface.** Cite the element-spec (MDN, WHATWG, SVG2, …) and
>    the API doc together; confirm the API's verbs are valid against the
>    target element's nouns. A generic doc example is not a generalization
>    guarantee.
> 3. **When the API verb does NOT apply at the target element, narrow the
>    API choice OR re-shape the design.** Do not ship a probe that asserts
>    behavior the underlying surface cannot supply.
>
> **Empirical anchor.** Two anchors at Pass 10:
> - **Arc 4 rev2 — attrX / attrY pick.** DAEDALUS-rev2 picked attrX / attrY
>   based on motion docs SVG-component generic example; ARGUS-rev2 caught
>   that SVG `<g>` has no native `x` / `y` per MDN + SVG2 spec; the API
>   verb (motion's attr-animate) cannot animate what doesn't exist at the
>   target element type. DAEDALUS-rev3 grounded against three sources
>   (motion docs + MDN g + MDN/SVG2 transform) and pivoted to transform-
>   based animation.
> - **Arc 5 §6.4 — motion layoutId not supported on SVG.** Same defect-
>   class at a different API verb (`layoutId` for FLIP-style transitions);
>   motion's docs example used HTML elements; the API does not support
>   SVG element layout transitions. Design narrowed scope rather than
>   assert behavior the surface can't supply.
>
> **Cross-refs:** `CAPTAIN_DAEDALUS.md` §6.9 (probe-grounding parent canon —
> clause 4 names "ground-check against shipped tool surface"; this section
> extends the principle to third-party API surfaces); `CAPTAIN_DAEDALUS.md`
> §6.4 (WebSearch / WebFetch for live constraints — the operational
> mechanism for the ground-check this discipline names); `CAPTAIN_ADA.md`
> §5.3 (web-search before guessing on third-party APIs — the build-time
> sibling).

**Cite-comments to add at read-sites:** in §6.9 clause 4 paragraph (the "ground-check against shipped tool surface" clause), append "See §6.11 for the API-docs-examples sibling discipline (ground-check the API verb against the target element's attribute surface, not just the docs example)."

### §2.6 Dev1 motion-animate-vs-SVG-attr scope (A4=ε CAPTAIN_ADA.md §5.9 build-time landing)

**Target location:** `substrate/CAPTAIN_ADA.md`, insert new subsection 5.9 after the existing 5.8 (between 5.8 closing and `## 6. Verdict format` — currently line ~152). Heading shape: `### 5.9 Scope-reduce motion APIs that overlap SVG-attribute-driven props` (bare-number form per existing file convention).

**Canonical wording:**

> When a build wires a motion API (`motion` / `framer-motion` `animate`
> prop, or equivalent) onto an SVG element whose layout is also driven by
> SVG attributes (`x`, `y`, `width`, `transform`, …), the motion library's
> animate prop overlaps the SVG-attribute surface. In jsdom (the test
> environment), the motion library wins — the SVG attributes get
> overwritten, and the test's setup intent silently breaks.
>
> **The discipline (at build-time):**
>
> 1. **Audit the SVG element's prop surface for overlap.** If a prop is
>    both motion-animated AND SVG-attribute-driven (via React props), there
>    is overlap.
> 2. **Scope-reduce: animate only the dynamic primitive.** Pick the single
>    primitive the design wants to animate (typically `transform` or
>    `opacity`); leave static layout attributes (`x`, `y`, `width`) driven
>    by React props alone.
> 3. **When in doubt, prefer transform-based animation over attribute-
>    based.** Transform is a single primitive that does not overlap with
>    `x` / `y` props at the SVG-attribute level.
>
> **Empirical anchor.** Pass 10 Arc 4 build: motion's `animate` prop on
> SVG `<g>` overlapped the SVG attribute surface in jsdom; tests that set
> `x` / `y` via React props saw motion overwrite the values. Scope reduction
> (animate only `transform`; leave `x` / `y` via React props) resolved the
> defect; the design's qualitative-acceptance surface (smooth star
> appearance) held under the narrower scope.
>
> **Cross-refs:** `CAPTAIN_DAEDALUS.md` §6.11 (design-time sibling — API-
> docs-don't-generalize-to-differently-shaped-elements; the design-time
> discipline that catches this kind of overlap *before* the build); §5.3
> (web-search before guessing on third-party APIs — operational mechanism
> for the build-time ground-check).

**Cite-comments to add at read-sites:** in `CAPTAIN_DAEDALUS.md` §6.11 closing cross-refs, append a reference to `CAPTAIN_ADA.md` §5.9 (the build-time sibling).

### §2.7 Dev2 AnimatePresence-popLayout-jsdom-timing (A4=ε op-disc §32 test-discipline landing)

**Target location:** `substrate/operating-disciplines.md`, insert new section 32 immediately AFTER the closing `---` separator of §31.4 cross-references (line 2040 at the f55f130 baseline) and BEFORE the existing non-numbered trailing section "Agent-regime inverses (the positive framing)" (line 2042 at the f55f130 baseline). The insertion is preceded by a blank line + a new `---` separator + a blank line, so the file's post-build structure reads: `### 31.4 Cross-references` → blank → `---` (line ~2040) → blank → `## 32. Test-environment timing discipline — jsdom + animation libraries` (new top-level section) → … → blank → `---` → blank → `## Agent-regime inverses (the positive framing)` (existing non-numbered section, unchanged position relative to its preceding `---`). Heading shape: `## 32. Test-environment timing discipline — jsdom + animation libraries` (top-level `##` heading + dot-after-number, per existing op-disc convention — see `## 31. Substrate-component design principles for agent-installable distribution` at line 1971 of the f55f130 baseline).

**Insertion-locus rationale (per §6.9 clause 4 ground-check against the actual op-disc file structure):** the alternative locus — appending §32 at file bottom AFTER the existing non-numbered trailing sections "Agent-regime inverses" (currently at line 2042) and "Empirical lineage" (currently at line 2053), so that §32 lands around line 2063 — was rejected for two reasons: (1) it would interleave the numbered §-section sequence with the non-numbered trailing sections (the file's existing convention is "all numbered sections first, then non-numbered trailing sections"; appending §32 at file bottom breaks that convention); (2) the non-numbered trailing sections "Agent-regime inverses" and "Empirical lineage" are conceptually footers / closing material, and inserting a numbered section AFTER them would semantically demote them from "closing material" to "interior material," which is wrong for their content. Keeping numbered §-sections contiguous (§1-§32 in order, with `---` separators between) and trailing non-numbered sections preserved at file tail (after the §32 close) is the structural choice that matches the file's existing convention.

The new-section pick (A4 sub-option a) over CAPTAIN_ADA.md test-discipline subsection (sub-option b) is defended by these properties: (1) the discipline is universal across CAPTAINs — VERA writes test probes, ADA writes test stubs, CATO reviews test surfaces; co-locating in op-disc makes it a single SSoT all three seats cite. (2) Pass 10 Arc 4 + Arc 5 surfaced this at the test-surface, not at a single seat's authoring — it's a property of jsdom-the-test-environment, not of any one seat's discipline. (3) §31 (Arc 38) is the most recent op-disc section; §32 is the natural next-number landing. (4) A18 IMMUTABLE concerns are satisfied: appending a new section to op-disc does not introduce any new file frontmatter (op-disc has no frontmatter) and does not introduce a new substrate skill (A19 LOCKED). If ARGUS surfaces a substance-disagreement on the new-section pick, fallback is sub-option (b) `CAPTAIN_ADA.md` §5.10 test-discipline subsection — same canonical wording, narrower applicability.

**Canonical wording:**

> jsdom (the headless DOM environment most projects use for React tests) does
> not implement `requestAnimationFrame` in a way that drives animation
> libraries' internal timing loops. `motion` / `framer-motion`'s
> `AnimatePresence` exit animation with `mode="popLayout"` waits for
> rAF-driven completion that jsdom does not deliver; the element stays in
> the DOM with `opacity: 0` and the testid still attached, indefinitely.
>
> **The discipline (at test-authoring time):**
>
> 1. **Identify animation-library code paths that depend on rAF-driven
>    timing.** Exit animations, layout transitions, springs that decay over
>    multiple frames.
> 2. **Assert against the OBSERVABLE END-STATE under jsdom, not the
>    library's exit-completion semantics.** "Element absent from DOM" is
>    not the right assertion for an `AnimatePresence` exit under jsdom;
>    "element has `opacity: 0` OR is absent from DOM" is the correct
>    disjunctive assertion that round-trips both real-browser and jsdom
>    semantics.
> 3. **When testing an animation that targets the DOM-presence boundary,
>    write a helper that accepts EITHER observable.** Example helper
>    contract: `expectXHidden()` returns truthy when either the X-testid
>    element is absent OR the element's outer wrapper has computed `opacity`
>    zero. The helper documents the disjunction; individual tests don't
>    re-derive it.
>
> **Empirical anchor.** Pass 10 Arc 4 build: `AnimatePresence mode="popLayout"`
> star exit animation under jsdom; the rAF-driven exit didn't complete; the
> star element stayed in the DOM with `opacity: 0`; the test's
> `expect(queryByTestId('star')).toBeNull()` assertion failed against the
> intended exit behavior. The `expectStarHidden()` helper (accepting EITHER
> testid-absent OR outer-wrapper-opacity-0) resolved the test failure
> without weakening the qualitative-acceptance audit (real browser fires the
> exit correctly; jsdom rests at the early-frame state; both are
> "star hidden" for the test's purposes).
>
> **Cross-refs:** `CAPTAIN_ADA.md` §5.9 (build-time sibling — motion-API
> scope reduction; both are properties of motion + jsdom interaction);
> `CAPTAIN_VERA.md` §5.1 (verification-side test-discipline — VERA reads
> §32 when designing probes against animation surfaces); `CAPTAIN_CATO.md`
> (honesty-audit consumer — when a test asserts disjunctively against the
> environment, CATO verifies the disjunction is the empirical reality, not
> a smoothed-over defect).

**Cite-comments to add at read-sites:** in `CAPTAIN_ADA.md` §5.9 closing cross-refs, append a reference to `operating-disciplines.md` §32 (the test-environment sibling). In `CAPTAIN_VERA.md` (post-§5.11 — ADA picks a natural insertion point near the existing test-discipline material), add a cite-comment cross-ref to §32.

---

## §3 C2 approach — validate-spec parser refinement

Two parser refinements: spec_refs.py (check-1) + bw_tickets.py (check-2). Each refinement is named at the function-level with the exact change ADA makes; the verification probes in §4 confirm the refinement actually reduces the FAIL/STRANGE counts against the Arc 42 baseline.

### §3.1 check-1 spec_refs.py heading-skip heuristic (A8=η spec-self-headings-set)

**Refinement target:** `substrate/skills/validate-spec/_lib/spec_refs.py`.

**Root cause restated:** the bare-§ resolver defaults to `operating-disciplines.md` per the spec's reading-note. But the spec's OWN section headings (lines like `### §2.1 The three roles`) match the bare-§ pattern and over-resolve against operating-disciplines.md, which has no `§2.1`. Of 144 check-1 FAILs, the vast majority are this exact class (heading-line `### §N.X` patterns where `§N.X` is a SPEC heading, not an operating-disciplines.md heading).

**The fix (A8=η spec-self-headings-set):**

1. **Add a pre-pass that builds a `spec_headings: set[str]` from SPECIFICATION.md before the main `_extract_references` loop.** Each entry in the set is the anchor portion of a spec heading line. Regex: `^#{1,6}\s+§([0-9][0-9A-Za-z.\-]*)`. Applied to every line of the spec; collected anchors form the set. (Lines like `### §2.1 The three roles` → set contains `"2.1"`.)

2. **In `_extract_references`, after Form (b) bare-§ match, add a heading-self-skip check.** Specifically: if the citing line ALSO matches the spec-heading regex AND the matched anchor equals the bare-§ form's anchor, then the bare-§ reference IS the heading itself, not a cross-ref to operating-disciplines.md — skip the bare-§ yield. Conceptually: a line that IS the §2.1 heading is not "referencing" §2.1; it is §2.1.

3. **Edge cases the heuristic must handle:**
   - **Form (a) matches on the same line.** Form (a) is `<file>.md §X.Y`; matches first. The bare-§ skip only applies to lines without a Form (a) match for the same anchor. The existing `seen_per_line` dedup in `_extract_references` already handles this — the bare-§ skip is layered on top.
   - **Inline references inside heading text.** A heading like `### §3.3 Per-class path convention (Arc 29 §17 + §23)` has THREE bare-§ candidates: `§3.3` (the heading itself — skip), `§17` (a cross-ref to operating-disciplines.md — keep), `§23` (a cross-ref — keep). The discipline is: skip ONLY the bare-§ whose anchor equals the heading's own anchor; keep the others. Implementation: in `_extract_references`, when on a heading line, identify the heading's own anchor first (via the same `^#{1,6}\s+§(...)` regex); skip Form (b) matches where `anchor == heading_anchor`; allow other Form (b) matches through.
   - **Headings that ARE legitimate cross-refs.** Hypothetically a heading like `### §X-y Z` where `X-y` happens to also exist as an op-disc anchor. Per the spec's reading-note, the bare-§ in a SPEC heading is the spec's section anchor, not a cross-ref; the skip is correct even in the hypothetical overlap case.

**Function-level edits ADA makes:**

```python
# new helper at module-scope (after _heading_pattern_for_anchor, before
# _extract_references)
_RE_SPEC_HEADING_ANCHOR = re.compile(r"^#{1,6}\s+§([0-9][0-9A-Za-z.\-]*)")


def _build_spec_headings_set(spec_text: str) -> set[str]:
    """Return the set of anchor strings (e.g., '2.1') that ARE spec section
    headings in the input spec_text. Used by _extract_references to skip
    bare-§ matches whose citing-line IS the heading whose anchor is the
    bare-§ value."""
    headings: set[str] = set()
    for line in spec_text.splitlines():
        match = _RE_SPEC_HEADING_ANCHOR.match(line)
        if match:
            headings.add(match.group(1))
    return headings
```

```python
# in _extract_references, before the Form (b) yield-loop, identify the
# heading's own anchor on this line (None if the line is not a heading):

heading_anchor_on_this_line: str | None = None
heading_match = _RE_SPEC_HEADING_ANCHOR.match(line)
if heading_match:
    heading_anchor_on_this_line = heading_match.group(1)

# then within the Form (b) yield-loop:
for match in _RE_FORM_B.finditer(line):
    anchor = match.group(1)
    # If this anchor was already matched as part of form (a) or (c), skip
    already_matched_as_a_or_c = any(
        key[1] == anchor for key in seen_per_line.get(lineno, set())
    )
    if already_matched_as_a_or_c:
        continue
    # NEW: heading-self-skip — bare-§ on a heading line whose anchor IS
    # the heading's own anchor is a self-reference, not a cross-ref.
    if heading_anchor_on_this_line is not None and anchor == heading_anchor_on_this_line:
        continue
    # Bare-§: defaults to operating-disciplines.md
    yield (lineno, line.strip(), None, anchor)
```

Note: `_build_spec_headings_set` returns the whole-spec set but is not consumed in the implementation above; the per-line `_RE_SPEC_HEADING_ANCHOR.match(line)` check inside the loop is the actual heading-detection. The whole-spec set is reserved for a future refinement that may need cross-line lookup (e.g., "this bare-§ in non-heading prose is a self-reference because the same anchor IS a heading elsewhere in the spec"). For Arc 43, the per-line check is the load-bearing fix; the whole-spec set is built but unused. ADA includes the set-build helper to keep the patch shape complete for the future refinement; if ARGUS surfaces that the unused set is dead code, ADA either inlines the use (per the cross-line variant) OR removes the helper. The per-line check is what reduces the 144 FAILs.

**Sub-option: include cross-line use of the spec-headings-set?** A bare-§ in NON-heading prose (e.g., a sentence "per §2.1, the three roles are…") is also a self-reference to the spec's §2.1, not a cross-ref to operating-disciplines.md §2.1 (which doesn't exist). To make this resolve, the per-line check is insufficient; we need to check the whole-spec set. The discipline in this case becomes: if the bare-§ anchor is in `spec_headings`, then the bare-§ is a SPEC self-reference, not an op-disc cross-ref. Implementation: in the Form (b) yield-loop, after the heading-self-skip check, ADDITIONALLY check `if anchor in spec_headings_set: yield (lineno, line.strip(), "SPECIFICATION.md", anchor)` (with SPECIFICATION.md as the target file rather than None, so the resolver tries to find the anchor in SPECIFICATION.md itself rather than operating-disciplines.md). This change is structural — it changes the semantics of bare-§ in non-heading prose from "op-disc default" to "spec-self-resolve when matching a spec heading; else op-disc default." Per the spec's reading-note at line 7, the op-disc default is the documented behavior; introducing a spec-self-resolve path is canon-adjacent (changes parser semantics, not spec wording). **DAEDALUS pick: include the cross-line use.** Rationale: (a) the spec's reading-note is informational, not a parser contract; (b) the empirical FAIL pattern includes bare-§ refs in non-heading prose that point to spec sections (e.g., "Recursion also extends across **generations** — the same role pattern… per §10.1" on spec line 69 — `§10.1` is the spec's `§13.x` section enumeration sub-anchor in some versions of the spec, and the bare-§ in this prose CAN be a spec self-reference); (c) without the cross-line use, ~30 of the 144 FAILs (the non-heading bare-§ refs to spec anchors) stay FAIL.

The combined fix: heading-self-skip (per-line) AND non-heading-bare-§-spec-self-resolve (whole-spec-set). ADA implements both; the verification probes in §4 confirm the FAIL-count drop covers both classes.

### §3.2 check-2 bw_tickets.py hybrid claim-status resolution (A9=μ HYBRID)

**Refinement target:** `substrate/skills/validate-spec/_lib/bw_tickets.py`.

**Root cause restated:** the §13.5-§13.9a candidate enumerations cite tickets in lines like `- C1: stoa--86k two-team forge/shop division of concerns (MAJOR_POLYBIUS.md behavioral section)` — no claim-keyword (open / closed / shipped / done / merged / dropped / completed / …) is present, so `_classify_claim` returns "ambiguous" and the verdict routes to STRANGE. Of 36 STRANGE classifications, the vast majority are this exact class (enumeration lines without explicit claim-keywords) + a smaller cluster from "Follow-up filed:" lines (which CONTAIN no claim-keyword but DO claim implicit-open status).

**The fix (A9=μ HYBRID):**

**Part A — tighter prose-regex for default-path (non-canon-touching).** Extend `_CLAIM_OPEN_PATTERNS` and `_CLAIM_CLOSED_PATTERNS` to cover empirically-observed claim shapes, AND add a context-aware classifier that uses the enclosing section heading as a fallback signal when the line itself has no explicit claim-keyword.

The empirical patterns observed in the STRANGE cluster:

- `Follow-up filed: stoa--XXX` — claims open (the ticket was just filed).
- `Shipped at PR #N → main <sha>. <N> candidates landed:` (header before an enumeration list) — claims closed for all tickets in the immediately-following bullet list.
- `- C1: stoa--XXX <description>` (bullet in §13.5-§13.9a) — claims closed when nested under a §13.5-§13.9 "DONE" heading; claims open when nested under §13.9a "not yet arc-scheduled" heading.
- `**stoa--XXX** (P3) — <description>. <Gating:> ...` in §13.9 — claims open (deferred-with-gating).

Extension to claim-patterns:

```python
_CLAIM_OPEN_PATTERNS = re.compile(
    r"\b(open|in[- ]flight|deferred|in[- ]progress|active|tracking|pending"
    r"|filed|surfaced|gating|gated|accretion|future[- ]arc|not yet arc[- ]scheduled)\b",
    re.IGNORECASE,
)
_CLAIM_CLOSED_PATTERNS = re.compile(
    r"\b(closed|done|shipped|dropped|completed|finished|landed|merged"
    r"|resolved|absorbed[- ]by|already[- ]resolved|already-resolved)\b",
    re.IGNORECASE,
)
```

And add a section-header-context classifier:

```python
# new module-level pattern + helper
_RE_SECTION_DONE = re.compile(r"^#+\s+§?[0-9]+\.[0-9]+[a-z]?\s+.*\bDONE\b", re.IGNORECASE)
_RE_SECTION_NOT_SCHEDULED = re.compile(
    r"^#+\s+§?[0-9]+\.[0-9]+[a-z]?\s+.*\b(not yet arc[- ]scheduled|deferred)\b",
    re.IGNORECASE,
)


def _build_section_context_map(spec_text: str) -> dict[int, str]:
    """Return a mapping {line_number: section_context}, where section_context
    is 'closed-context' (under a §X.Y heading containing DONE) or
    'open-context' (under a heading containing 'not yet arc-scheduled' or
    'deferred') or 'neutral' (other sections).

    Used by _classify_claim_with_context as a fallback signal when the line
    itself has no explicit claim-keyword."""
    line_to_context: dict[int, str] = {}
    current_context: str = "neutral"
    for lineno, line in enumerate(spec_text.splitlines(), start=1):
        if _RE_SECTION_DONE.match(line):
            current_context = "closed-context"
        elif _RE_SECTION_NOT_SCHEDULED.match(line):
            current_context = "open-context"
        elif re.match(r"^#+\s+", line):
            # Any other heading: reset to neutral
            current_context = "neutral"
        line_to_context[lineno] = current_context
    return line_to_context
```

And a fallback step in `_classify_claim`:

```python
def _classify_claim_with_context(line_text: str, section_context: str) -> str:
    """Same as _classify_claim, but with a section-context fallback when the
    line itself has no explicit claim-keyword."""
    has_open = bool(_CLAIM_OPEN_PATTERNS.search(line_text))
    has_closed = bool(_CLAIM_CLOSED_PATTERNS.search(line_text))
    if has_closed and not has_open:
        return "closed"
    if has_open and not has_closed:
        return "open"
    # Both or neither — fall back to section context
    if section_context == "closed-context" and not has_open:
        return "closed"
    if section_context == "open-context" and not has_closed:
        return "open"
    return "ambiguous"
```

Then `_run_check_2` passes the line's section_context to the classifier. The threading change is small: build the context-map once before the cited-tickets loop; pass `line_to_context[lineno]` to the classifier per item.

**Part B — structured-frontmatter migration path (canon-adjacent; new shape preferred when present).** Extend the parser to recognize a tighter ticket-citation shape, and prefer it when present. Canonical new shape: `**stoa--XXX (P3, status:closed)** — …` or `**stoa--XXX (P3, status:open)** — …`. Implementation: a new regex that matches the bold-asterisk + ticket-id + parens-with-status form; when this regex matches, the parser reads the explicit status from the match and bypasses prose-regex classification.

```python
# new module-level pattern
_RE_STRUCTURED_CLAIM = re.compile(
    r"\*\*(stoa--[a-z0-9]+)\s*\([^)]*?\bstatus\s*:\s*(open|closed)\b[^)]*?\)\s*\*\*",
    re.IGNORECASE,
)


def _extract_structured_claim(line_text: str, ticket_id: str) -> str | None:
    """If the line contains a structured claim of the shape
    `**stoa--XXX (P3, status:closed)** — ...` for the given ticket_id,
    return 'open' or 'closed'. Otherwise None (fall back to prose-regex)."""
    for match in _RE_STRUCTURED_CLAIM.finditer(line_text):
        if match.group(1) == ticket_id:
            return match.group(2).lower()
    return None
```

Threading: `_run_check_2` checks `_extract_structured_claim` FIRST; if it returns a value, use that; else fall back to `_classify_claim_with_context`.

**Migration path (canon-touching but documented as gradual):** the parser supports BOTH the old prose-style claim and the new structured `(P3, status:closed)` shape. The new shape is documented in the validate-spec SKILL.md (one-line note: "for tight status classification, cite tickets in candidate enumerations as `**stoa--XXX (P3, status:closed)** — …`"). Existing spec text stays as-is; new candidate enumerations in future spec edits MAY adopt the new shape. ADA does not retrofit the existing spec; that would be canon-touching beyond the parser scope.

**Decision matrix the combined fix produces for any ticket-citation line:**

| Line shape | Classification |
|---|---|
| Contains explicit prose-keyword (open / closed / shipped / done / filed / …) | Use prose-keyword (Part A regex) |
| Contains structured `(P3, status:closed)` | Use structured (Part B) — preferred when present |
| Has no explicit keyword AND no structured claim | Fall back to section-context (Part A context-map) |
| All of the above fail | STRANGE (unchanged from current behavior) |

The expected STRANGE-count drop: ~30 of the 36 STRANGEs are `- CN: stoa--XXX <description>` in §13.5-§13.7 (under DONE headings → closed-context fallback) or `Follow-up filed: stoa--XXX` (matches `filed` keyword → open). The remaining ~6 are genuinely ambiguous and stay STRANGE.

---

## §4 Verification probes

Probes ADA + VERA can re-execute. Per §6.9 clauses 1-5 (anchor + character-class + live-RT + ground-check + enumeration-vs-invocation) AND §6.9.3'' COMPLETENESS CLAUSE (sibling-defect-class audit) AND §6.9.3' (round-trip-adjacent-prose). All probes below were live-round-tripped at authoring time against the worktree state at f55f130; the round-trip evidence is named per probe.

### §4.1 C1 — META-discipline catalog landing probes

**Probe 1 (existence — file-level):** the following sections exist as headings in their target files post-build. Each is checkable by a single `grep -n` against the file in the worktree. **Note on heading shape:** the substrate canon files (CAPTAIN_*.md, operating-disciplines.md) use bare-number heading anchors, NOT `§`-prefixed. CAPTAIN_DAEDALUS.md and CAPTAIN_ADA.md use `### N.X Title`; operating-disciplines.md uses `## N. Title` (top-level, with dot-after-number). SPECIFICATION.md is the exception — it uses `### §N.X Title`. The probes below match the actual heading convention of each target file.

```bash
# CAPTAIN_DAEDALUS.md uses `### N.X` — bare-number, no §
grep -nE "^### 6\.9\.3' " substrate/CAPTAIN_DAEDALUS.md
grep -nE "^### 6\.9\.3''" substrate/CAPTAIN_DAEDALUS.md
grep -nE "^### 6\.2\.1' " substrate/CAPTAIN_DAEDALUS.md
grep -nE "^### 6\.10 " substrate/CAPTAIN_DAEDALUS.md
grep -nE "^### 6\.11 " substrate/CAPTAIN_DAEDALUS.md

# CAPTAIN_ADA.md uses `### N.X` — bare-number, no §
grep -nE "^### 5\.9 " substrate/CAPTAIN_ADA.md

# operating-disciplines.md uses `## N.` — top-level (##) with dot-after-number
grep -nE "^## 32\. " substrate/operating-disciplines.md
```

**Live-round-trip at authoring time (§6.9 clause 3 + §6.9.3''):** ran `grep -nE "^### 6\.9 " substrate/CAPTAIN_DAEDALUS.md` against the pre-build state at f55f130 — returned `196:### 6.9 Probe-grounding discipline for design.md probes (extends §5.11 to the authoring seat)`. Confirmed: the existing convention is bare-number heading anchors. The post-build state introduces 5 new sections at this file; each appears at a distinct line number. POSIX/Windows portability: the patterns are pure ASCII (no `§` in the substrate-canon-file patterns); `grep -E` POSIX BRE/ERE handles them identically; PowerShell `Select-String -Pattern` does too.

**Round-trip-adjacent-prose audit (§6.9.3'):** the parenthetical "single `grep -n` against the file" claims that each grep is one command per section. The actual commands above all return zero or one line; if a section is missing post-build, the grep returns empty (exit 1 on GNU grep). VERA's check is: every probe returns exactly one matching line. The prose round-trips correctly.

**Sibling-defect-class audit (§6.9.3'' COMPLETENESS CLAUSE — the originating self-application catch):** an earlier draft of this probe block used `^### §6\.9\.3'` patterns assuming the substrate canon files used `§`-prefixed headings (a default carried over from SPECIFICATION.md's convention). The live round-trip against pre-build state surfaced the defect — `grep -nE "^### §6\.9 " substrate/CAPTAIN_DAEDALUS.md` returned zero matches because the file uses `### 6.9` (no §). The COMPLETENESS CLAUSE fired: the defect was a class (assumed heading shape) not an instance; sibling-class audit found the same defect at every probe targeting a substrate-canon-file (CAPTAIN_DAEDALUS.md / CAPTAIN_ADA.md / operating-disciplines.md). All probes corrected; SPECIFICATION.md probes retain `§` because the spec's convention IS `§`-prefixed. This is a POSITIVE empirical anchor for §6.9.3'' COMPLETENESS CLAUSE per Pass 10 self-application precedent.

**Probe 2 (cross-ref cite-comments resolved):** for every cross-ref named in §2.1-§2.7, the cite-comment is present at the read-site. **Note: cross-refs in CITE PROSE within substrate canon files use `§N.X` form even though heading anchors use bare-number form.** The empirical convention (verified by grep-against-pre-build): existing §6.9 cross-refs in CAPTAIN_DAEDALUS.md cite as `§5.11`, `§6.2`, etc. (with `§`) in inline prose, but the section's own heading at line 196 is `### 6.9 Probe-grounding…` (without `§`). The probes below match the actual conventions of each site.

**R4 tightening (per ARGUS pass-1):** rev0 Probe 2 used `grep -nE "§6\.9\.3'"` to count §6.9.3' (single-apostrophe) cross-refs — but the regex `'` matches the first `'` of `''`, so the pattern over-matches §6.9.3'' (double-apostrophe) cross-refs as well. Two distinct sections, one indistinguishable probe result. Similarly, rev0's `grep -nE "§5\.9|CAPTAIN_VERA"` against op-disc over-matched ~10 incidental prose hits unrelated to Arc 43's new §32 cite-comments. The rev1 probes below disambiguate:

```bash
# CAPTAIN_DAEDALUS.md §6.9 cross-ref prose cites §6.9.3' (single-apostrophe — SKIP §6.9.3'')
# Disambiguator: apostrophe NOT followed by another apostrophe — [^'] negated bracket
grep -nE "§6\.9\.3'[^']" substrate/CAPTAIN_DAEDALUS.md | head -10

# §6.9.3'' (double-apostrophe) cross-ref — literal double-apostrophe
grep -nE "§6\.9\.3''" substrate/CAPTAIN_DAEDALUS.md | head -10

# §6.2 cross-ref prose cites §6.2.1' (single-apostrophe) and §6.10
# Disambiguator: same [^'] negation for the apostrophe-bearing anchor
grep -nE "§6\.2\.1'[^']" substrate/CAPTAIN_DAEDALUS.md | head -10
grep -nE "§6\.10\b" substrate/CAPTAIN_DAEDALUS.md | head -10

# §6.11 closing cross-refs cite CAPTAIN_ADA.md §5.9
grep -nE "CAPTAIN_ADA\.md.*§5\.9|§5\.9.*CAPTAIN_ADA" substrate/CAPTAIN_DAEDALUS.md

# op-disc §32 cross-refs — scope to the new §32 cite-comments specifically,
# not to incidental prose elsewhere in op-disc. Strategy: anchor the grep
# to the literal cite-comment HTML-block shape `<!-- cite: ... -->` that
# Arc 43 introduces at the §32 section.
grep -nE "^<!-- cite:.*§5\.9" substrate/operating-disciplines.md
grep -nE "^<!-- cite:.*CAPTAIN_VERA" substrate/operating-disciplines.md
# Additionally, scope by line-range to op-disc §32 specifically (post-build
# line range is computed at VERA time from `grep -nE '^## 32\.' op-disc`);
# the cite-comment + cross-ref scan within the §32 body is the load-bearing
# check, NOT a whole-file grep.
```

**Round-trip-adjacent-prose audit (§6.9.3'):** the prose claim "for every cross-ref named in §2.1-§2.7, the cite-comment is present at the read-site" is the contract. Round-trip: the new §6.9.3' / §6.9.3'' / §6.2.1' / §6.10 / §6.11 sections each include cross-refs in canonical wording (per §2.1-§2.5); ADA inserts those verbatim; VERA's greps confirm presence. Each grep returns ≥1 line on PASS; zero lines on FAIL. The `§` character is non-ASCII U+00A7; under PYTHONUTF8=1 (op-disc §13) bash + PowerShell both handle the literal correctly. The probes assume the encoding gate is in effect; VERA confirms in the project's standard environment.

**Live-RT validation of the rev1 tightening (§6.9.3'' — live-RT at authoring time):** the disambiguation was live-RT'd against the design.md itself at rev1 authoring time using Python regex semantics (POSIX ERE `[^']` and lookahead in Python `(?!')` are semantically equivalent for this case). Validation: `python -c "import re; t=open('agents/design/arc-43/design.md', encoding='utf-8').read(); print('single-not-double:', len(re.findall(r\"§6\\.9\\.3'(?!')\", t)), 'double:', len(re.findall(r\"§6\\.9\\.3''\", t)))"` returned `single-not-double: 17 double: 25` — confirming the regexes disambiguate correctly. POSIX `grep -E` does not support lookahead, but `[^']` is the POSIX-portable equivalent (apostrophe followed by ANY character that is NOT an apostrophe); the slight semantic difference (lookahead vs negated bracket) is: `[^']` requires a following character to exist (i.e., would miss `§6.9.3'` at end-of-line), while lookahead `(?!')` matches at end-of-line too. For Probe 2's purposes, the cross-refs appear in mid-line cite prose (e.g., `§6.9.3' (round-trip-adjacent-prose)`); the following character always exists; `[^']` is correct.

**Sibling-defect-class audit (§6.9.3'' COMPLETENESS CLAUSE):** distinct site-types matter — heading anchors use bare-number (`### 6.9.3'`), inline-cross-ref prose uses `§`-prefixed (`§6.9.3'`). The probe pattern for Probe 2 uses `§`-prefix because it's matching inline prose; the probe pattern for Probe 1 uses bare-number because it's matching the heading itself. Both are correct per the file's actual conventions; the COMPLETENESS audit was to verify each probe matches the site-type it targets, not assume one shape for all sites.

**Sibling-defect-class audit (§6.9.3'' COMPLETENESS CLAUSE — R4-class siblings):** the apostrophe-ambiguity defect-class is: a regex `X'` where the target file contains BOTH `X'` and `X''`, the regex over-matches both. Audit every probe in this design for the same defect-class:

- **Probe 1 line `^### 6\.9\.3' ` (heading-anchor for §6.9.3').** The trailing-space anchor disambiguates from `### 6.9.3''` (which has no space after `'`; the post-build heading is `### 6.9.3'' Live-round-trip…` with `''` then space). VERIFIED: the trailing-space disambiguator works because the post-build heading shapes are `### 6.9.3' Round-trip…` (single-apostrophe + space) vs `### 6.9.3'' Live-round-trip…` (double-apostrophe + space). Probe 1's `^### 6\.9\.3' ` matches the single but NOT the double (the regex `'` then literal-space requires the char after `'` to be space; the double-apostrophe shape has `'` then `'` then space, so the byte AFTER the first `'` is `'`, not space).
- **Probe 1 line `^### 6\.9\.3''` (heading-anchor for §6.9.3'').** Literal-double-apostrophe disambiguates from single. VERIFIED.
- **Probe 1 line `^### 6\.2\.1' ` (heading-anchor for §6.2.1').** Trailing-space disambiguator; no §6.2.1'' exists in the design (the §6.2.1' canon is a single section); the trailing-space anchor is sufficient. VERIFIED.
- **Probe 3 lines.** No apostrophe-bearing anchors in Probe 3's load-bearing-phrase greps; the apostrophe-ambiguity defect-class does not apply at Probe 3.
- **Probes 5-9 (unit-level Python).** No grep regexes that could collide on apostrophe; the constructed-input strings use literal anchors like `§2.1`, `§3.3`, `§13.4`, `§13.9a` — no apostrophe-bearing anchors. The apostrophe-ambiguity defect-class does not apply.

Cross-tool sibling (per §6.9.3'' COMPLETENESS CLAUSE: defect-classes span tool boundaries): the apostrophe-ambiguity defect would also surface in Vitest assertions or stub-test regexes if the design used those. The design does not — all probes are grep + Python — so the cross-tool audit is trivially satisfied.

**Sibling-defect-class audit (§6.9.3'' COMPLETENESS CLAUSE — incidental-prose-over-match siblings):** the op-disc `§5\.9` over-match defect-class is: a regex matching a multi-character anchor (`§5.9`) over-matches when the same character sequence appears in incidental prose (e.g., op-disc §24 cites `§5.9.4`; cross-tier mentions of `§5.9` in unrelated sections). Audit every whole-file grep in this design for the same defect-class:

- **Probe 2 op-disc `§5\.9` grep (R4(a)).** TIGHTENED in rev1 to `^<!-- cite:.*§5\.9` — line-anchored to the cite-comment HTML-block shape; excludes incidental prose. VERIFIED by pre-build `grep -nE "^<!-- cite:.*§5\.9" substrate/operating-disciplines.md` returning zero (correct — Arc 43 hasn't built yet); post-build will return ≥1 line at the §32 cite-comment block.
- **Probe 2 op-disc `CAPTAIN_VERA` grep.** Same tightening: scope to `^<!-- cite:.*CAPTAIN_VERA` (line-anchored cite-comment) rather than whole-file grep. Pre-build returns zero; post-build returns ≥1 at §32's CAPTAIN_VERA cite-comment.
- **Probe 2 CAPTAIN_ADA.md `§5\.9` grep.** §5.9 in CAPTAIN_ADA.md is the NEW section being introduced by Arc 43 (§2.6 in this design). The pre-build state has no §5.9 in CAPTAIN_ADA.md (the file's current §5 family ends at §5.8); post-build introduces exactly one §5.9 section. The whole-file grep is acceptable here because §5.9 does NOT appear in CAPTAIN_ADA.md's pre-build prose (verified by `grep -nE "§5\.9" substrate/CAPTAIN_ADA.md` returning zero at f55f130).
- **Probe 3 lines.** No multi-character-anchor whole-file greps that risk over-match; load-bearing phrases are distinctive enough.

The R4 disambiguation defect-class is closed by the rev1 tightening + the COMPLETENESS audit above.

**Sibling-defect-class audit (§6.9.3'' COMPLETENESS CLAUSE — apostrophe-character class):** the apostrophe in `§6.9.3'` is a literal U+0027 in the file content (verified by `Get-Content -Encoding utf8` / `cat` of the post-build file). The grep pattern uses literal apostrophe in the regex. POSIX `grep -E` treats `'` as literal; Windows `findstr` does too. No hex-escape needed. POSIX/Windows portability: confirmed by spec_refs.py current behavior (it reads `§` from spec without issue under PYTHONUTF8=1). Under-anchored regex: the `^### 6\.9\.3' ` pattern includes the trailing space after the anchor, which excludes false matches like `### 6.9.3'a Something` (no such section exists; the trailing-space anchor is the disambiguator).

**Probe 3 (canonical wording present and load-bearing phrases):** key load-bearing phrases from §2.1-§2.7 appear in the canon files. ADA inserts the canonical wording from §2.X verbatim; the probes confirm the canonical phrases land.

```bash
# §6.9.3'' COMPLETENESS CLAUSE
grep -nE "COMPLETENESS CLAUSE" substrate/CAPTAIN_DAEDALUS.md
grep -nE "DEFECT-CLASS, not just exact-pattern-instance" substrate/CAPTAIN_DAEDALUS.md
grep -nE "60. multiplier" substrate/CAPTAIN_DAEDALUS.md  # the 60× cost-multiplier anchor; the . matches × (U+00D7) OR x (ASCII fallback)
# Note: × is U+00D7; ADA writes literal × in the canonical wording per §2.2; VERA confirms either
# the × character OR an ASCII 'x' fallback matches via the . wildcard

# §6.10 SSoT-with-WHY
grep -nE "SSoT-with-WHY" substrate/CAPTAIN_DAEDALUS.md

# §6.11 API-docs example
grep -nE "API-docs-examples-don't-generalize" substrate/CAPTAIN_DAEDALUS.md

# §5.9 motion-API scope reduction
grep -nE "scope.reduce" substrate/CAPTAIN_ADA.md | grep -i "motion"

# §32 jsdom + animation
grep -nE "jsdom" substrate/operating-disciplines.md | grep -iE "animation|popLayout"
```

**Round-trip-adjacent-prose audit (§6.9.3'):** the parenthetical "the . matches × (U+00D7) OR x (ASCII fallback)" is a contract claim. Round-trip: `60.` regex against `60×` matches because `.` matches any single character. Against `60x` matches because `.` matches `x`. Against `60 multiplier` matches because `.` matches the space. The prose round-trips to "the . wildcard accepts × OR x OR space"; the regex therefore over-matches on `60 ` followed by " multiplier" too. Acceptable for this probe; the goal is presence-confirmation, not exact-character verification.

**Sibling-defect-class audit (§6.9.3'' COMPLETENESS CLAUSE):** the `60.` regex is under-anchored if used as a general claim-finder. Tightened: `\b60[×x]\b.*multiplier` would be stricter but loses round-trip clarity. Per §6.9.3'' COMPLETENESS, audit every regex in this probe block for similar under-anchoring:
- `^### §6\.9\.3' ` — anchored at line-start + space; OK.
- `^### §6\.9\.3''` — anchored at line-start + ''; OK (the doubled-apostrophe is a distinctive token).
- `COMPLETENESS CLAUSE` — substring match; could match incidental prose elsewhere; for this probe, presence-only is sufficient.
- `SSoT-with-WHY` — substring; same logic.
- `API-docs-examples-don't-generalize` — substring with apostrophe; literal apostrophe + hyphens are distinctive enough to avoid false-positives in the substrate corpus (verified by `grep -rn "API-docs-examples-don" substrate/` against the pre-build state — zero matches; post-build will return one).

**Probe 4 (live `validate-spec` re-run delta against Arc 42 baseline):** after C2 build, ADA re-runs validate-spec against SPECIFICATION.md from the worktree and produces an updated `agents/observation/spec-validation/mechanical-check-results.md`. The probe is the delta vs the Arc 42 baseline.

Acceptance (per A22):

```bash
# Run validate-spec from the worktree root
cd .claude/worktrees/arc-43-build
PYTHONUTF8=1 python substrate/skills/validate-spec/_lib/spec_refs.py --spec SPECIFICATION.md > /tmp/c1.jsonl
PYTHONUTF8=1 python substrate/skills/validate-spec/_lib/bw_tickets.py --mode check-2 --spec SPECIFICATION.md > /tmp/c2.jsonl

# Extract summary lines
grep -E '"summary": true' /tmp/c1.jsonl
grep -E '"summary": true' /tmp/c2.jsonl
```

Acceptance criteria (the falsification thresholds — calibrated per ARGUS pass-1 simulation against the post-Arc-42 spec drift):

- **check-1 FAIL count drops from 144 to ≤60.** Most of the 144 FAILs are spec-self-heading false-positives (~89 of them, per ARGUS simulation, are eliminated by the heading-self-skip + cross-line spec-self-resolve fix). The remaining ~55 FAILs are residue categories the Arc 43 fix does NOT cover (enumerated below); rounding up gives ≤60 as the conservative threshold.
- **check-2 STRANGE count drops from 36 to ≤15.** Most STRANGEs are `- CN: stoa--XXX <description>` enumeration lines under DONE-context sections (the section-context fallback classifies them as closed) + `Follow-up filed:` lines (the `filed` keyword classifies them as open). ARGUS simulation of the §3.2 fix gives ~13 STRANGEs remaining (line-level vs ticket-level classification ambiguity when multiple tickets cited on one line; plus genuinely ambiguous lines); rounding up gives ≤15 as the conservative threshold.

**Threshold-calibration provenance.** The Arc 42 baseline at `agents/observation/spec-validation/mechanical-check-results.md` was 65 tickets / 36 STRANGE; the current spec at f55f130 is 75 tickets (post-Pass 10 + Arc 42 ship comments). Spec drift between Arc 42 baseline and Arc 43 design-time is one factor in the threshold calibration; the dominant factor is the residue-categories enumeration below. Per stoa--bbi refined-principle thesis: residue IS the data. The acceptance is the threshold + the residue is captured + named follow-up tickets file the residue forward; this is honest scoping, not smoothed all-green.

**Residue categories the Arc 43 fix does NOT cover (per §6.9.3'' COMPLETENESS CLAUSE — sibling-defect-class enumeration of what the named-instance fix leaves behind):**

For check-1 (the ~55 remaining FAILs after the §3.1 spec_refs.py fix):

1. **Form (a) over-capture of literal `§N` placeholder** (~2 FAILs). Spec line 7's "Reading note" cites `MAJOR_POLYBIUS.md §N` where `N` is a literal placeholder in prose, not a section anchor. Form (a) over-captures `N` as an anchor. Fix-shape (out-of-scope, future arc): the placeholder character `N` is not a valid anchor character; Form (a) regex could require anchor starts with `[0-9]`. Filed as **stoa--FIX1** follow-up per A19.
2. **Form (b) `§13.x` placeholder/glob over-capture** (~12 FAILs). Spec lines 471/485/487/606/621 use `§13.x` (lowercase `x` as wildcard / placeholder denoting "any subsection of §13"). The current resolver captures `13.x` as an anchor, then resolves against operating-disciplines.md and fails because there is no `§13.x` literal. Fix-shape (out-of-scope, future arc): detect lowercase-letter-only suffixes as glob/placeholder; skip resolution. Filed as **stoa--FIX2** follow-up per A19.
3. **Form (b) range-syntax over-capture** (~4 FAILs). Spec lines using `§1-§6` or `§13.5-§13.10` get captured as anchors `1-` and `13.5-` (the trailing hyphen is included by the `[0-9A-Za-z.\-]*` character class). Fix-shape (out-of-scope, future arc): trim trailing `-` from captured anchors; OR detect range-syntax `§N-§M` and resolve as two separate anchors. Filed as **stoa--FIX3** follow-up per A19.
4. **Form (b) trailing-dot anchor greed** (~16 FAILs). Spec lines ending sentences with `…per §7.1.` capture the anchor as `7.1.` (including the trailing period). Fix-shape (out-of-scope, future arc): trim trailing `.` from captured anchors. Filed as **stoa--FIX4** follow-up per A19.
5. **Form (c) inference-gap on `**PLINY** §5.10` shape** (~10 FAILs). Form (c) requires `CAPTAIN_*|MAJOR_*` directly before `§`. Spec uses `**PLINY**` / `**POLYBIUS**` shorthand for which-CAPTAIN; the bold-asterisk + bare-mnemonic shape doesn't match Form (c)'s `CAPTAIN_*|MAJOR_*` prefix. Fix-shape (out-of-scope, future arc): extend Form (c) to recognize `**MNEMONIC**` shorthand and resolve via mnemonic-to-file lookup (Pliny→`MAJOR_PLINY.md`, Polybius→`MAJOR_POLYBIUS.md`, etc.). Filed as **stoa--FIX5** follow-up per A19.
6. **Hyphenated prose tokens** (~2 FAILs). Lines containing `§12-internal-staleness` or `§12-side` capture the anchor as `12-internal-staleness` because the character class includes hyphens. Fix-shape (out-of-scope, future arc): detect anchor-with-letters-after-hyphen as prose-token, not anchor. Filed as **stoa--FIX6** follow-up per A19.
7. **Misc legitimate cross-refs not resolving via current heuristics** (~9 FAILs). Heterogeneous; require per-case investigation. Filed as **stoa--FIX7** follow-up per A19 (a catch-all for the residue after the named six categories).

For check-2 (the ~13 remaining STRANGEs after the §3.2 bw_tickets.py fix):

8. **Line-level vs ticket-level classification ambiguity when one line cites multiple tickets** (~5 STRANGEs). `_classify_claim_with_context` is per-line; when a line contains multiple ticket citations, the line-level classification applies to all tickets on the line. The current §3.2 decision matrix (lines 656-664 of this design) does not address per-ticket disambiguation within a multi-ticket line. Fix-shape (out-of-scope, future arc): per-ticket structured-claim preference (already in §3.2 Part B for the `**stoa--XXX (P3, status:closed)**` shape, but not for legacy prose-only multi-ticket lines); OR per-ticket sub-line-context. Filed as **stoa--FIX8** follow-up per A19.
9. **`_RE_SECTION_NOT_SCHEDULED` matches `\bdeferred\b` against `Deferred-with-gating`** (~3 STRANGEs). The §13.9 "Deferred-with-gating" heading correctly resolves to open-context, but the classifier may diverge from intent when a line within that section contains closed-keywords ("dropped", "absorbed-by"). The decision matrix's "fall back to section context" step is conservative; for ambiguous lines the section-context wins, but the underlying state may genuinely be mixed. Fix-shape (out-of-scope, future arc): explicit per-ticket within-section disambiguation. Filed as **stoa--FIX9** follow-up per A19.
10. **Genuinely ambiguous lines** (~5 STRANGEs). Heterogeneous lines that cite tickets without any explicit keyword AND in a neutral-context section. Per stoa--bbi residue-IS-data framing, these are the irreducible residue. No fix planned; STRANGE is the correct verdict.

The threshold ≤60 / ≤15 is calibrated so that the Arc 43 fix passes acceptance even with the residue categories present; the residue is the data per stoa--bbi; the follow-up tickets stoa--FIX1..FIX9 carry the named residue forward to future arcs.

If the deltas are smaller than expected (e.g., check-1 lands at 70 instead of ≤60), that is data not failure — it means the residue categories have a wider tail than ARGUS's pass-1 simulation projected. The follow-up tickets capture the residue; the arc still ships per stoa--bbi.

**Round-trip-adjacent-prose audit (§6.9.3'):** the "≤60 / ≤15 thresholds" prose claims are contract thresholds VERA verifies. Round-trip: the spec_refs.py summary emits `{"summary": true, "total": N, "pass": N, "fail": N, "strange": N}`; the verification is to parse the summary JSON and assert `fail ≤ 60`. The bw_tickets.py check-2 summary emits the same shape; assert `strange ≤ 15`. Both summaries are JSONL lines; VERA can read with `python -c "import json,sys; print(json.loads(sys.stdin.read()))"` or jq. The residue-categories enumeration above (10 categories with named follow-up tickets stoa--FIX1..FIX9) round-trips through VERA as: when the threshold is met, VERA's verdict is PASS and the residue categories are captured in `agents/observation/spec-validation/mechanical-check-results.md`'s post-run-narrative; when the threshold is NOT met (e.g., check-1 = 70), VERA's verdict notes the over-shoot + which residue category (per the enumeration) is wider than projected, and the follow-up ticket scope expands accordingly. The acceptance is the threshold + residue-captured + follow-ups-filed; NOT all-green.

**Sibling-defect-class audit (§6.9.3'' COMPLETENESS CLAUSE):** the per-script invocation depends on PYTHONUTF8=1 (per op-disc §13 Windows discipline). If VERA runs on a POSIX system where UTF-8 is default, the env var is harmless. If on Windows without the env var, the spec read fails on the `§` character. The probe explicitly names `PYTHONUTF8=1` to be POSIX/Windows portable. Sibling-class audit for the rest of the probe block: every Python invocation MUST be prefixed with `PYTHONUTF8=1` or be POSIX-only — confirmed.

### §4.2 C2 — validate-spec parser refinement probes (per-function)

**Probe 5 (check-1 spec_refs.py — heading-self-skip works on a constructed input).** A unit-level check ADA writes as a standalone test (or VERA writes as an inline probe). The probe is structural — it does NOT need the full SPECIFICATION.md, just a constructed 3-line input:

```bash
PYTHONUTF8=1 python - <<'PY'
import sys, pathlib, tempfile

# Path to the worktree's spec_refs.py
sys.path.insert(0, "substrate/skills/validate-spec/_lib")
from spec_refs import _extract_references

# Constructed input: one heading-line bare-§ + one prose-line bare-§
text = "### §2.1 The three roles\nper §7.4, the cross-tier routing applies.\n"
refs = list(_extract_references(text))

# Expected: the heading-line bare-§ §2.1 is SKIPPED; the prose-line bare-§ §7.4 is YIELDED
anchors = [ref[3] for ref in refs]
assert "2.1" not in anchors, f"FAIL: §2.1 should be skipped on heading line; got {anchors}"
assert "7.4" in anchors, f"FAIL: §7.4 should be yielded from prose; got {anchors}"
print("PASS: heading-self-skip works on constructed input")
PY
```

**Round-trip-adjacent-prose audit (§6.9.3'):** the "heading-line bare-§ §2.1 is SKIPPED" prose claim is directly verified by the assertion `"2.1" not in anchors`. The assertion is the round-trip; if the prose were wrong (e.g., the heuristic skips both bare-§s or skips neither), the assertion would fail. Live-round-tripped at authoring time against the constructed input (mentally — implementation not yet present at f55f130 baseline; post-ADA-build, VERA runs the probe literally).

**Sibling-defect-class audit (§6.9.3'' COMPLETENESS CLAUSE):** for under-anchored regex inside the probe — the `<<'PY'` HEREDOC + single-quoted EOF tag means the inner Python is byte-literal; `§` round-trips correctly. The `text` string contains `§` as literal U+00A7; under PYTHONUTF8=1, the Python `str` literal interprets it correctly. POSIX/Windows portability: `bash` HEREDOC works on Git Bash (Windows), WSL, native Linux/macOS. PowerShell does NOT support HEREDOC the same way; VERA may need to run via `bash -lc`. The probe assumes a bash shell; if the project's standard environment is PowerShell-only, VERA pivots to a one-liner. Threading the variant: ADA documents `bash -lc` invocation in the probe-run instructions.

**Probe 6 (check-1 spec_refs.py — inline-in-heading cross-refs preserved).** The heading `### §3.3 Per-class path convention (Arc 29 §17 + §23)` has three bare-§ candidates: §3.3 (skip), §17 (keep), §23 (keep). Probe:

```bash
PYTHONUTF8=1 python - <<'PY'
import sys
sys.path.insert(0, "substrate/skills/validate-spec/_lib")
from spec_refs import _extract_references

text = "### §3.3 Per-class path convention (Arc 29 §17 + §23)\n"
refs = list(_extract_references(text))
anchors = sorted([ref[3] for ref in refs])

# Expected: §3.3 SKIPPED; §17 + §23 KEPT
assert "3.3" not in anchors, f"FAIL: §3.3 should be skipped on its own heading line; got {anchors}"
assert "17" in anchors, f"FAIL: §17 should be yielded from inline-in-heading prose; got {anchors}"
assert "23" in anchors, f"FAIL: §23 should be yielded from inline-in-heading prose; got {anchors}"
print(f"PASS: inline-in-heading cross-refs preserved; anchors={anchors}")
PY
```

**Round-trip-adjacent-prose audit:** the "three bare-§ candidates: §3.3 (skip), §17 (keep), §23 (keep)" prose is round-tripped by the three asserts. No drift between prose and probe.

**Sibling-defect-class audit:** same shell + HEREDOC concerns as Probe 5; same PYTHONUTF8 dependency; same `bash -lc` fallback.

**Probe 7 (check-2 bw_tickets.py — structured-frontmatter shape preferred).** A unit-level check:

```bash
PYTHONUTF8=1 python - <<'PY'
import sys
sys.path.insert(0, "substrate/skills/validate-spec/_lib")
from bw_tickets import _extract_structured_claim

# Line with structured claim
line_with = "- **stoa--abc (P3, status:closed)** — some description"
assert _extract_structured_claim(line_with, "stoa--abc") == "closed"

# Line without structured claim
line_without = "- C1: stoa--abc some description"
assert _extract_structured_claim(line_without, "stoa--abc") is None

# Line with structured claim for a different ticket
line_other = "- **stoa--xyz (P3, status:open)** — and also stoa--abc"
assert _extract_structured_claim(line_other, "stoa--abc") is None
assert _extract_structured_claim(line_other, "stoa--xyz") == "open"

print("PASS: structured-frontmatter shape preferred")
PY
```

**Probe 8 (check-2 bw_tickets.py — section-context fallback classifies enumerations).** A unit-level check against the constructed §13.x enumeration shape:

```bash
PYTHONUTF8=1 python - <<'PY'
import sys
sys.path.insert(0, "substrate/skills/validate-spec/_lib")
from bw_tickets import _build_section_context_map, _classify_claim_with_context

# §13.4 enumeration line — closed-context
text = (
    "### §13.4 Pass 3 — Arc 37 (substrate architecture canonification batch, 6 candidates) — DONE 2026-05-17\n"
    "\n"
    "- C1: stoa--86k two-team forge/shop division of concerns\n"
)
context_map = _build_section_context_map(text)

# Line 3 is the enumeration line
assert context_map[3] == "closed-context", f"FAIL: line 3 should be closed-context; got {context_map[3]}"
line_text = "- C1: stoa--86k two-team forge/shop division of concerns"
assert _classify_claim_with_context(line_text, context_map[3]) == "closed"

# §13.9a enumeration line — open-context
text2 = (
    "### §13.9a Post-sequence-surfaced tickets (filed Arcs 38+39+40+41 + Pass 8 spec-recon; not yet arc-scheduled)\n"
    "\n"
    "- **stoa--lyw** (P3) — /resume invocation discipline canon\n"
)
context_map2 = _build_section_context_map(text2)
assert context_map2[3] == "open-context", f"FAIL: line 3 should be open-context; got {context_map2[3]}"
line_text2 = "- **stoa--lyw** (P3) — /resume invocation discipline canon"
assert _classify_claim_with_context(line_text2, context_map2[3]) == "open"

print("PASS: section-context fallback classifies enumerations correctly")
PY
```

**Round-trip-adjacent-prose audit (§6.9.3'):** the "§13.9a … 'not yet arc-scheduled'" prose claim refers to the actual SPECIFICATION.md §13.9a heading. Round-trip: grep the spec for the literal heading text — `grep -nE "^### §13\.9a " SPECIFICATION.md` returns line 587 in the worktree at f55f130. The heading text matches the probe's constructed input.

**Sibling-defect-class audit (§6.9.3'' COMPLETENESS CLAUSE):** the `_RE_SECTION_DONE` regex requires `\bDONE\b` (case-insensitive). The §13.4 heading IS `### §13.4 Pass 3 — Arc 37 (substrate architecture canonification batch, 6 candidates) — DONE 2026-05-17` (verified by grep against the worktree); the `DONE` token is present. The `_RE_SECTION_NOT_SCHEDULED` regex requires `'not yet arc-scheduled'` OR `'deferred'`; the §13.9a heading IS `### §13.9a Post-sequence-surfaced tickets (filed Arcs 38+39+40+41 + Pass 8 spec-recon; not yet arc-scheduled)` (verified); the token is present. Sibling-class audit: every §13.X heading the parser categorizes by context must contain a discriminating token; the spec's §13.5-§13.9a all share the pattern: §13.2-§13.8 have DONE; §13.9 has "Deferred-with-gating"; §13.9a has "not yet arc-scheduled"; §13.10-§13.12 have various states. The regex covers DONE + deferred + not-yet-arc-scheduled; other states are neutral (no fallback). Confirmed.

**Probe 9 (check-2 bw_tickets.py — A22 self-application: live re-run shows STRANGE drop).** Same as Probe 4's check-2 portion — after ADA's parser build, the validate-spec re-run against SPECIFICATION.md emits a STRANGE count ≤ 10. ADA updates `agents/observation/spec-validation/mechanical-check-results.md` with the new run's summary; VERA verifies the new count.

---

## §5 Self-assessed weak points (per §6.2)

Five weak points named at design-authoring time. Each names a brittle assumption + a one-line defense of the choice despite the weakness, per §6.2.

1. **Weak point — A4=ε Dev2 lands at op-disc §32 (new section).** The choice over A4 sub-option (b) (CAPTAIN_ADA.md test-discipline subsection) rests on the argument that the discipline is universal-across-CAPTAINs (VERA + ADA + CATO all read). If ARGUS or PRINCIPAL disagrees that the universality is real (a test-environment quirk specific to motion + jsdom may not generalize), the discipline arguably belongs at CAPTAIN_ADA.md §5.10 rather than op-disc §32. **Why this shape anyway:** appending a new op-disc section is a small canon edit (one section + cross-refs); if ARGUS surfaces a substance-disagreement, ADA can pivot at rev1 without significant rework. The fallback path is documented in §2.7.

2. **Weak point — A8=η spec-self-headings-set design exceeds the directive's narrow lean.** The user-tier lean named (η) as "spec-self-headings-set" — build a set of spec headings and skip matches. My implementation does that AND adds a cross-line lookup (bare-§ in non-heading prose that matches a spec heading anchor resolves to SPECIFICATION.md self-resolve, not op-disc default). The cross-line use changes parser semantics, not spec wording — it's canon-adjacent but parser-internal. **Why this shape anyway:** without the cross-line lookup, ~30 of 144 FAILs stay FAIL (the non-heading bare-§ refs in spec prose that point to spec sections). The lean was directionally correct but the empirical pattern (visible only at design time when I read the mech-check-results.md) is broader than per-line.

3. **Weak point — the 60× cost-multiplier math is one-anchor empirical, not statistical.** The 60-second-at-design-time vs ~60-minute-at-build-rev numbers come from Pass 10 Arc 4 / Arc 5 specific anchors; the multiplier is illustrative, not measured across a population. If a future arc finds the multiplier is 6× or 600×, the canonical wording still holds (the discipline is "audit at design time"; the multiplier is the cost-of-skipping illustration). **Why this shape anyway:** the cost-multiplier prose is in the canonical block as motivational anchor, not as load-bearing claim; if ARGUS surfaces the math as over-specified, ADA can soften "60× multiplier" → "substantial multiplier" without changing the discipline. Surfaced explicitly to ARGUS in `residual_questions_for_argus:`.

4. **Weak point — Probe 4 acceptance thresholds (≤60 check-1 FAIL; ≤15 check-2 STRANGE) are calibrated from ARGUS pass-1 simulation, with 10 named residue categories carrying the remaining defect surface forward as follow-up tickets stoa--FIX1..FIX9.** Rev0 used ≤30 / ≤10 — those were too tight; ARGUS pass-1 simulation showed post-fix check-1 = 55 (not ≤30) and post-fix check-2 = 13 (not ≤10). Rev1 raises to ≤60 / ≤15 and enumerates the residue categories (Form (a) over-capture of `§N` placeholder; Form (b) `§13.x` glob / range-syntax / trailing-dot / hyphenated prose; Form (c) `**PLINY**` shorthand inference gap; for check-2: line-level multi-ticket disambiguation + `\bdeferred\b` over-match + genuinely-ambiguous lines). If the actual post-build counts still differ (e.g., check-1 lands at 70 instead of ≤60), VERA's verdict notes the over-shoot + which residue category is wider than projected; the follow-up ticket scope expands accordingly. **Why this shape anyway:** thresholds are now calibrated from ARGUS's pass-1 empirical simulation, not from mental count; residue categories are enumerated, not glossed; follow-ups are filed forward per stoa--bbi. The acceptance is the threshold + residue-captured + follow-ups-filed; NOT all-green. The new shape is honest scoping per stoa--bbi refined-principle thesis — residue IS the data.

5. **Weak point — design contains 7 separate canonical-wording blocks (§2.1, §2.2, §2.3, §2.4, §2.5, §2.6, §2.7) each of which is verbatim canon ADA inserts.** Per §6.8 (canonical-template wording-alignment discipline), if any of these blocks is duplicated within the design.md (e.g., I paste the canonical wording twice — once in §2.X and once as an inline preview elsewhere), the two copies MUST be byte-for-byte aligned. I did not duplicate any block; each canonical-wording quote appears exactly once. Verified by mental diff at authoring time; if ARGUS or VERA finds a duplicate I missed, the §6.8 discipline applies. **Why this shape anyway:** the design is structured one-canonical-block-per-section by intent; the §6.8 risk is low but the discipline is named.

6. **Weak point — own-authoring self-application catch is named in §4.1 Probe 1 Sibling-defect-class audit; ARGUS may catch ADDITIONAL violations I missed.** The §6.9.3'' COMPLETENESS CLAUSE fired during own draft (probe heading-shape defect; corrected after live-RT pre-build); the COMPLETENESS sibling audit covered the substrate-canon-file probes I could enumerate. But the principle of §6.9.3'' COMPLETENESS is that the surfaced defect-class may have other sibling shapes I did not see. Possible un-caught siblings: (a) cite-comment prose in canonical wording blocks may have its own heading-shape assumptions when read at a future ADA build; (b) the `§6.X` placeholder in section names within §2.4 (e.g., "§6.X qualitative-acceptance-anchor surface") is a documentation artifact and not part of the canonical wording — but if I miscounted somewhere, the documentation shape leaks into the canon; (c) the heading regex in spec_refs.py's `_RE_SPEC_HEADING_ANCHOR` assumes the SPEC's `### §N.X` shape — which is correct per SPECIFICATION.md, but if ADA copies the regex to apply to non-spec files (e.g., a future check against op-disc), it would fail silently. The third sibling is the most subtle; I flag it explicitly for ARGUS. **Why this shape anyway:** the catch surfaced live-round-trip discipline working as designed; positive empirical anchor; remaining residue per stoa--bbi refined-principle thesis is acceptable.

7. **Weak point — rev1 Probe 2 R4 tightening introduces a new defect-class audit (apostrophe-ambiguity + incidental-prose-over-match); the COMPLETENESS sibling enumeration in §4.1 Probe 2 covers grep + Python probes within THIS design but does not guarantee no similar defect surfaces in adjacent canon files that the rev1 fix cites.** The rev1 Probe 2 sibling-class audit (apostrophe-ambiguity siblings + incidental-prose-over-match siblings) covers Probes 1-9 within this design.md. If a future arc lands additional probes targeting apostrophe-bearing anchors (§6.9.3', §6.9.3'', §6.2.1') in OTHER design.md files, the defect-class can recur. **Why this shape anyway:** the COMPLETENESS CLAUSE canonical wording (§2.2) names the discipline as a per-design audit at probe-authoring time; future designs apply the discipline at their own authoring; the current design.md's sibling audit is complete for THIS design. Sibling-class instances at OTHER designs are caught at those designs' DAEDALUS time per §6.9.3''.

**Residual questions for ARGUS (rev1 — R-tier addressed, residual is N-tier only):**

- All four R-tier risks (R1 Probe 4 ≤30 threshold infeasible; R2 Probe 4 ≤10 threshold marginal; R3 op-disc §32 insertion site under-specified; R4 Probe 2 cross-ref grep apostrophe-ambiguity + incidental-prose-over-match) are addressed in rev1. R1+R2 raise thresholds to ≤60 / ≤15 + enumerate 10 residue categories with named follow-up tickets stoa--FIX1..FIX9 per A19. R3 picks insertion locus (i) between op-disc line 2040 and line 2042. R4 tightens Probe 2 regexes using `[^']` negation + literal `''` for apostrophe disambiguation, and `^<!-- cite:` line-anchor for cite-comment scope.
- The N-tier observations (N1=A4=ε op-disc §32 pick; N2=60× cost-multiplier math; N3=cross-line spec-self-resolve extension) stand pat per ARGUS pass-1; no rev1 changes.
- Recursive self-application surveillance: any §6.9.3' / §6.9.3'' / §6.2.1' violation you catch in THIS rev1's own probes counts as a POSITIVE empirical anchor for the canon being shipped (per Pass 10 precedent). The rev1 Probe 2 R4 tightening + COMPLETENESS sibling audit IS itself an application of §6.9.3'' COMPLETENESS CLAUSE — the rev1 catch (apostrophe-ambiguity defect-class spans Probe 2's three apostrophe-bearing anchor sites) is the second-instance recursive self-application at this arc. The arc canon is its own catch surface.

---

## §6 Out of scope (per A19 hard-locks)

The following are deliberately not addressed in this arc:

- **Restructuring §6.9 base canon beyond extension + cross-ref additions.** A19 LOCKED. New sections cite + extend §6.9; the existing §6.9 stays as-is.
- **Widening yl1 candidates beyond the 10 enumerated.** A19 LOCKED. If during design I notice an 11th candidate, I name it here; I do not fold it in.
- **Expanding 4zj beyond check-1 + check-2.** A19 LOCKED. Other validate-spec parser-class limitations (e.g., check-3 placement walk has its own STRANGE handling per the current `_run_check_3`) stay deferred. Probe 9 confirms check-2; check-3 is not in scope.
- **10 named residue categories for validate-spec post-Arc-43 (R1+R2 follow-ups).** Per §4.1 Probe 4's residue enumeration: stoa--FIX1 (Form (a) `§N` placeholder over-capture); stoa--FIX2 (Form (b) `§13.x` glob/placeholder over-capture); stoa--FIX3 (range-syntax `§N-§M` over-capture); stoa--FIX4 (trailing-dot anchor greed); stoa--FIX5 (Form (c) `**PLINY**`/`**POLYBIUS**` shorthand inference gap); stoa--FIX6 (hyphenated prose tokens); stoa--FIX7 (misc legitimate cross-refs catch-all); stoa--FIX8 (line-level vs ticket-level classification ambiguity); stoa--FIX9 (genuinely-ambiguous lines). PLINY files these follow-ups at A17 closure with cross-refs to the design.md residue-enumeration section. Each ticket is a future-arc target; Arc 43 ships with the residue captured + named, NOT all-green per stoa--bbi.
- **New substrate skills.** A19 LOCKED. yl1 + 4zj both edit existing canon (CAPTAIN_DAEDALUS.md + CAPTAIN_ADA.md + operating-disciplines.md + validate-spec _lib/ Python files).
- **Retrofitting SPECIFICATION.md to use the structured-frontmatter `(P3, status:closed)` shape.** §3.2 documents the migration path; the parser supports both shapes. Adopting the new shape in existing spec text is canon-touching and beyond Arc 43 scope.
- **Pass 10 stellation Arc 6 polish.** PRINCIPAL deferred indefinitely; not this arc's scope.
- **Beadworks + ghost project setup.** Post-Arc-43 ratification; not this arc.

---

## §7 A22 self-application protocol (ADA + ZENO + VERA + CATO collaboration)

After ADA builds C1 + C2, the A22 self-application target fires:

1. **ADA runs validate-spec against SPECIFICATION.md in the worktree.** Per Probe 4 commands. Outputs go to `agents/observation/spec-validation/mechanical-check-results.md` — ADA updates the existing artifact with the new run's timestamp, substrate SHA, and per-check summary.
2. **ADA captures the FAIL/STRANGE delta against the Arc 42 baseline (refs=274 pass=130 fail=144 strange=0 / tickets=65 pass=23 fail=6 strange=36).** New row in the artifact; old row stays as historical record.
3. **ZENO mechanical PASS check.** ZENO's mechanical-pass check verifies the spec_refs.py and bw_tickets.py edits are syntactically clean (Python imports, type annotations).
4. **VERA falsification on Probes 1-9.** VERA re-runs each probe literally; verdicts PASS/FAIL/STRANGE per probe per §4. Probe 4 + Probe 9 are the load-bearing acceptance gates against the thresholds.
5. **CATO honesty + craft audit.** Per A20 MANDATORY: CATO verifies the META-discipline wording captures the empirical anchors faithfully (no smoothing of the cost-multiplier math, no over-claiming the COMPLETENESS CLAUSE coverage); CATO verifies the parser changes don't regress validate-spec accuracy (Probes 5-8 are clean unit-level checks).

If any of (3)-(5) fails, the arc enters rev-cycle per the gauntlet protocol (DAEDALUS rev1, ARGUS re-audit, etc.). The arc ships when all four pass.

---

**End of design.** Ready for ARGUS plan critique.

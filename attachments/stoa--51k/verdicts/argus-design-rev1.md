# ARGUS plan-critique — Arc 73 / stoa--51k — design-rev1.md (decision-register READER, slice 2b)

status: completed
ticket: stoa--51k
verdict: pass
design_artifact_audited: agents/design/stoa--51k/design-rev1.md
operating-mode: autonomous
overall: RATIFY (no BLOCKERs, no load-bearing RISKs; 2 NOTE-level observations for ADA + 1 promote-or-clear CLEARED for POLYBIUS)

## Per-concern classification

### C1 — DC2 re-verify gate: anti-gaslighting BOTH ways — RATIFY
Both outcomes are stated FIRST-CLASS, not fallback. (a) SUPPORTED -> surface honestly, defeats the USER hindsight self-serving edit (design L88); (b) NOT-SUPPORTED/no-entry -> callback NOT fired, agent OWNS THE GAP, defeats the AGENT false 'I told you so' (L90). The both-directions table (L92-96) carries both directions explicitly. Maps faithfully to doctrine sect6 (longitudinal loop), Resolved (the gate reduces to 'does the logged entry support the callback?'), and sect8 (egoless). The gate keys on the logged WARNING + COUNTER-HYPOTHESIS (the register fields Arc 71 captured FOR this gate), NOT on memory (L79) — the exact non-collapsibility-vs-memory property the doctrine Resolved section demands. SOUND.

### C2 — 'own the gap' is a first-class outcome — RATIFY
L90 + L153 + L168 all state own-the-gap as a first-class honest move, never a degraded fallback. The DC1 no-entry path (L68) routes STRAIGHT to DC2 outcome (b) own-the-gap and explicitly forbids papering it over by reconstructing a warning from memory (that would be the agent false-callback failure DC2 exists to catch). The corpus carries it as its own class (no-entry/, L153) with a floor. SOUND.

### C3 — 'door not a blanket' / no-collusion — RATIFY
L98 states it crisply: own ONLY what is genuinely the agent's; absorbing FALSE blame hands the PRINCIPAL the scapegoat they want — that is collusion, a failure as much as a fake I-told-you-so. This is doctrine sect6 (door, not a blanket) verbatim-in-spirit, paired with 'the call itself was yours.' DC3 (L114) re-applies it at delivery. SOUND.

### C4 — READ-ONLY register (absolute) — RATIFY
DC1 (L54): READS ONLY — NO write-back, NO mutation of the register, ever. Lookup names ONLY bw list / bw show (L58, L71). NO bw comment/edit/label/close against the register anywhere. The single bw comment reference (L69, L212) is the OPTIONAL clarifying QUESTION to the PRINCIPAL on multi-candidate ambiguity — a conversation turn, NOT a register write; P5 (L212) greps the module for any mutating verb targeting the register and confirms the question reference is to conversation not the register ticket. Mechanically auditable; the directive automatic-route-back trigger is NOT reached. SOUND.

### C5 — Weak-point #1 (the --check-corpus overlap PROXY) — RATIFY (POLYBIUS promote-or-clear: CLEARED)
POLYBIUS explicit clear-condition: confirm the proxy is NOWHERE described as deciding a live callback. CONFIRMED across every site:
 - L158: the overlap check is a STRUCTURAL PROXY for supports, not a proof of semantic support — the genuine read is the --judge floor ... it does NOT decide a live callback.
 - L101-102: the crisp record-vs-callback structural check (corpus-deterministic) is SEPARATED from the accreting genuinely-biting judgment (--judge floor).
 - L104 honest-stance LOCKED: rejects any enforced / guaranteed / non-collapsible phrasing.
 - L193 (weak point #1): names the exact risk (mis-reading the proxy as the gate) and points the guard at the honest-stance text.
The overlap check is a NEGATIVE-CONTROL WELL-FORMEDNESS check (a supported/ fixture's author-written WARNING must overlap the author-written COMPLAINT; an unsupported/-by-mismatch one must not) — structurally identical to the Arc-71 vacuity-denylist negative control already shipped and NOMOS-ratified. It proves the corpus exercises BOTH gate directions on real exemplars; it does NOT adjudicate a live callback. Honest-stance integrity intact: nowhere is a judgment read called enforced/guaranteed. SOUND. POLYBIUS: CLEAR.

### C6 — Weak-point #2 (over-fire no-fire vs DC1 own-the-gap boundary) — RATIFY with NOTE-1
The subtlest seam: a FRESH complaint with NO logged decision -> no-fire (DC0, L43); a complaint about a DECIDED-but-UNLOGGED call -> own-the-gap (DC1/DC2, L68). Both are honest outcomes, NEITHER fabricates a warning — so even a MIS-classification across this boundary fails SAFE (silence vs owning a gap; no faked warning either way). The design pins both sides with fixtures (over-fire/ fresh-gripe vs no-entry/ decided-but-unlogged, L154/L153) and the discriminator is named honestly as model judgment (was this a DECIDED dilemma?, L194). The SCENARIO field (L140) must carry whether a decided call exists so the judge can distinguish them.
NOTE-1 (ADA, not a RISK): the no-entry/ fixtures and the over-fire/ fresh-gripe fixtures must make the was-this-a-decided-call cue UNAMBIGUOUS in each SCENARIO string, or the --judge floor measures noise on this boundary rather than the discriminator. A fixture-authoring quality bar, not a design defect — the safe-failure property above means it cannot produce a faked warning regardless. Surfaced so ADA writes the SCENARIO cues deliberately.

### C7 — Weak-point #3 (malformed Arc-71 entry -> field() degrades to empty) — RATIFY
The reader reuses the PROVEN, UNCHANGED field() awk (run-decision-register-corpus.sh:89-98) — confirmed verbatim against the source; no novel extractor introduced (L60, L56). A missing/partial field returns empty -> routes to own-the-gap (L195) — the SAFE direction (no fabricated warning). CONFIRMED this is the safe direction and is specified. One residual the design itself names (L195): a PARTIALLY-parsed entry could surface a TRUNCATED warning; mitigated because the gate keys on WARNING + COUNTER-HYPOTHESIS specifically and an empty either-one routes to own-the-gap. Adequately bounded; the safe-direction property holds. SOUND.

### C8 — Scope fidelity (slice 2b only; DC4 neutral-default ONLY) — RATIFY
DC4 (L124-130) ships the NEUTRAL-DEFAULT v1 ONLY and DEFERS per-user calibration with the doctrine-grounded rationale (no track record yet -> any dose now is a stereotype -> VIOLATES doctrine sect6: calibrate off the REAL track record, not a stereotype). The honest deferral the directive demands, not a handwave — the rationale is load-bearing-correct. Out-of-scope (L233-240) explicitly excludes: per-user calibration, consumer variant, meta-trigger counter (slice 4), broader rollout (slice 4), ANY register write-back. NO out-of-scope item reaches IN. The automatic-route-back triggers are NOT tripped. SOUND.

### C9 — Wiring correctness + gen-data validity — RATIFY with NOTE-2
The complaint-time checkpoint is correctly homed on MAJOR_POLYBIUS (PRINCIPAL-facing seat; complaints come from the PRINCIPAL) as a NEW sect3.7, distinct from the Arc-70/71 DECISION-time checkpoints in sect3.6. CONFIRMED against the live role file: sect3.5 routing-map + relocation-index and sect3.6 (hosting both dilemma-classifier + decision-register with balanced MODULE-INLINE marker pairs) exist exactly as the design describes; the sect3.7 + new routing-map row + new relocation-index row + new MODULE-INLINE pair mirror the shipped pattern 1:1. The PLINY-asymmetry is correctly reasoned: a complaint is NOT a directive-lock event, so the reader is POLYBIUS-ONLY and does NOT wire to PLINY sect5.18 (L179) — sound, and the design names the asymmetry explicitly for confirmation. DC3 reuses the REAL dilemma-classifier sect4 diagnostic tree (verified present: the guilt-lane/shame-lane read-the-person tree) — not an invented one.
NOTE-2 (ADA + VERA, not a RISK): gen-data validity hinges on the new MODULE-INLINE marker pair being BALANCED and the two new table rows being well-formed (the adapter reads the markers; an unbalanced/missing pair breaks recompose). The design names this (L185) and P6 re-runs gen-data deterministically. Mechanical, covered by the probe — surfaced so ADA treats marker-balance + row-validity as a build-time must and VERA asserts P6 green BEFORE close.

## Cross-cutting checks

### Honest-stance integrity — RATIFY
No enforced / guaranteed / non-collapsible phrasing on any judgment read anywhere in the design. The LOCKED honest stance (L16, L104, L173) claims ONLY high-probability + regression-guard + the-record-didnt-lie, frames --judge as a DOGFOOD PROXY (judge==verifier coupling named, L173), and explicitly rejects the fake-certainty the doctrine exists to kill. The exact posture Arc 70/71/72 shipped and NOMOS ratified. CLEAN.

### Corpus completeness / both-directions controls — RATIFY
The anti-gaslighting controls run BOTH ways EXPLICITLY (L156): supported/ carries a USER-hindsight-edit fixture (complaint you-never-warned-me; ENTRY WARNING proves they WERE warned -> gate must SURFACE); unsupported/ carries an AGENT-false-callback fixture (situation tempts I-told-you-so; ENTRY does NOT support -> gate must OWN-THE-GAP). L156 explicitly calls a one-direction-only design INCOMPLETE — the directive incompleteness bar is met. Per-class floors are HONEST (NOT 100%): supported >=3/4, unsupported OWN-THE-GAP >=3/4 (named LOAD-BEARING, the dangerous direction), no-entry >=2/3, over-fire >=2/3 (L162-169); a miss in ANY class exits nonzero. Mirrors the Arc-71 per-class-floor-not-aggregate discipline. CLEAN.

### Buildability for ADA + executable probes for VERA — RATIFY
The deliverable shape (L22-28) is concrete: a named module (complaint-callback.md) with DC0-DC4 + LOCKED stance, a named corpus dir mirroring the shipped Arc-71 runner shape, and explicit role-file edits (L181-185) ADA can apply mechanically. The parse is the proven field() (no new extractor to invent). VERA gets 8 executable probes: P1 (supported surfaces LIVE) + P2 (unsupported owns-the-gap LIVE) — both gate outcomes demonstrated live not asserted; P3 (no-entry owns-the-gap); P4 (over-fire holds); P5 (read-only grep); P6 (gen-data deterministic + markers balanced + rows present); P7 (new corpus at floor); P8 (source-only deploy). Regression bar (L221-229) = all THREE existing corpora (dilemma 19/19, decision-register 18/18, decision-surface 19/19) + gen-data/vitest/author-gate/stop-hook + NOMOS + Author + sect28.9 trailer + both outcomes live. No load-bearing decision left for ADA to invent. CLEAN.

### Authorship attribution — RATIFY
Design L3 names Author of repo: Denson Smith. Corpus README/runner provenance lines (per the Arc-71 precedent) name the PRINCIPAL. No author-like field names anyone other than Denson Smith. No fixture SCENARIO is an authorship claim (fixtures are fictional test input per the Arc-71 runner header). CLEAN.

## audit_block
audit_block:
  risks: []   # no load-bearing risks; 2 NOTE-level observations below, neither load-bearing
  notes:
  - id: note-1
    description: no-entry/ vs over-fire/-fresh-gripe SCENARIO strings must make the was-this-a-DECIDED-call cue unambiguous, or --judge measures noise on the subtlest boundary.
    evidence: design L140 (SCENARIO field), L153/L154 (the two classes), L194 (the discriminator is model judgment)
    load_bearing: false
    rationale_for_not_load_bearing: even a mis-classification across this boundary fails SAFE (no-fire vs own-the-gap; neither fabricates a warning) — a fixture-quality bar, not a correctness defect.
  - id: note-2
    description: the new MODULE-INLINE marker pair must be balanced + the two new sect3.5 table rows well-formed or gen-data recompose breaks.
    evidence: design L185 (named), P6 (L215, re-runs gen-data deterministically)
    load_bearing: false
    rationale_for_not_load_bearing: mechanical + covered by P6; ADA build-time check, VERA asserts before close.
  non_findings:
  - DC2 only catches the user not the agent false callback — DISCHARGED: both-directions table L92-96 + unsupported/ agent-false-callback fixture L156 + own-the-gap floor L167 LOAD-BEARING.
  - register mutated somewhere — DISCHARGED: lookup names only bw list/show; P5 greps for mutating verbs; the one bw comment is the clarifying question to the PRINCIPAL, not a register write.
  - over-claims certainty on a judgment read — DISCHARGED: honest stance LOCKED L104/L173; --judge framed as DOGFOOD PROXY; no enforced/guaranteed/non-collapsible phrasing anywhere.
  - the overlap proxy decides a live callback — DISCHARGED: L158 explicitly it-does-not-decide-a-live-callback; L101-102 separate crisp core from --judge; POLYBIUS promote-or-clear CLEARED.
  - novel parser risk — DISCHARGED: reuses the verbatim proven field() awk at run-decision-register-corpus.sh:89-98; confirmed unchanged against source.
  - wiring on the wrong seat / breaks gen-data — DISCHARGED: POLYBIUS sect3.7 is the right home (PRINCIPAL-facing, complaint-time, distinct from sect3.6 decision-time); PLINY-asymmetry correctly reasoned; marker/row pattern mirrors shipped sect3.6 1:1.
  - scope creep (dose calibration / consumer / slice-4 / write-back folded in) — DISCHARGED: DC4 ships neutral-default v1 ONLY + defers calibration with doctrine rationale; out-of-scope L233-240 excludes all; none reaches in.
  - malformed legacy entry fabricates a warning — DISCHARGED: field() degrades to empty -> own-the-gap, the SAFE direction (no fabricated warning); specified L195.
  threat_coverage_assessment: N/A — this arc carries no threat-ratified mitigation (op-disc sect35.5 carve-out: a process/module change reading a shipped register read-only, no runtime attack-path introduced). No M<n> map required; no threat-anchored probe owed.

## summary

The design is the READER half of the self-correction black box: a complaint-time callback + re-verify gate that pulls the SPECIFIC logged decision-register entry READ-ONLY and asks the doctrine's one question — does the logged WARNING + COUNTER-HYPOTHESIS support the callback? It is sound on every load-bearing axis I was dispatched to stress. The DC2 gate is genuinely anti-gaslighting in BOTH directions — outcome (a) SUPPORTED defeats the user hindsight self-serving edit, outcome (b) NOT-SUPPORTED/no-entry forces OWN-THE-GAP and defeats the agent false I-told-you-so — and both outcomes plus own-the-gap are first-class, never fallbacks. The register access is mechanically read-only (only bw list/show; P5 greps for mutating verbs; the lone bw comment is a clarifying question to the PRINCIPAL, not a register write). The honest stance is LOCKED with no enforced/guaranteed/non-collapsible phrasing on any judgment read, and the --check-corpus overlap check is correctly + consistently caveated as a structural negative-control proxy that does NOT decide a live callback (POLYBIUS promote-or-clear: CLEARED). Scope holds tight to slice 2b — DC4 ships neutral-default v1 ONLY and defers per-user calibration with the doctrine-grounded a-dose-now-would-be-a-stereotype rationale; nothing out-of-scope reaches in; no register write-back anywhere. Wiring is correctly homed on a new MAJOR_POLYBIUS sect3.7 (PRINCIPAL-facing, complaint-time, distinct from the sect3.6 decision-time checkpoints), the PLINY-asymmetry is correctly reasoned, and the marker/row pattern mirrors the shipped sect3.6 1:1 (gen-data validity covered by P6). The parse reuses the verbatim proven field() awk (no novel extractor). The both-directions corpus runs the anti-gaslighting controls BOTH ways with honest per-class floors (not 100%), and VERA gets 8 executable probes with both gate outcomes demonstrated LIVE plus the full three-corpus regression bar. Overall posture: CLEAN — RATIFY. Two NOTE-level observations for ADA/VERA (fixture SCENARIO cue clarity on the no-entry-vs-over-fire boundary; MODULE-INLINE marker balance) are quality bars, not load-bearing risks — both fail SAFE or are probe-covered. No BLOCKERs, no load-bearing RISKs. Ready for build.

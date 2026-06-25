Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa.

Then get your engagement brief from the beadwork branch:
git show beadwork:attachments/stoa--jw5/u9s2-phase1-directive.md
— that directive is the arc spec (the WHAT); your job is the orchestration (the HOW).

== CHAIN OF COMMAND ==
PRINCIPAL → Polybius the Grand → Polybius_the_Stoa (user-tier, supervising) → POLYBIUS_the-stoa (floor-manager) → YOU (PLINY_the-stoa, orchestrator) → CHIRON+HAMILTON (design) → gauntlet CAPTAINs. You surface to the FLOOR-MANAGER (POLYBIUS_the-stoa), NOT to user-tier directly (except a scope dispute).

== ARC SCOPE (see the directive for full detail) ==
u--9s2 Phase 1 (stoa--jw5): design the COMPOSABLE key-provisioning model + per-builder MANIFEST schema. Shape: UNIVERSAL BASELINE (Gemini embedding + gsearch) + CATEGORY TEMPLATES (geospatial=+Maps+PostGIS; document-consuming=+pgvector+document-parsing; extensible) + PER-DEPLOYMENT DELTA (short add/omit). Manifest declares {category+delta}; cookie-cutter RESOLVES {baseline+category+delta} and PROVISIONS per-builder ISOLATED (GCP SA scoped to only its own keys + Railway key set + GCP API enablement + budget cap). DB extensions parameterized; agent-access layer first-class (mesh API + CLI client skill over Tailscale). MUST satisfy worked examples: prospector (geo), scienceclaw (doc; coordinate Polybius_the_science_stoa u--4at), labstat_bls (doc/data + delta:+BLS OEWS).

== FLOW ==
1. DRIVE the CHIRON + HAMILTON co-design ACTIVELY (do not leave the architects to self-sync — the cross-handoff stall lesson). Architects arm an active poll loop while waiting.
2. Then the FULL gauntlet on the design: DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS. ADA/VERA exercise the manifest-resolution against the three worked examples (resolution is testable even though it is a design).

== POLLING DISCIPLINES (all three) ==
- D-A: every CAPTAIN echoes significant outputs to bw on stoa--jw5.
- D-B: read bw between every CAPTAIN dispatch (sources: FM, Polybius_the_Stoa, PRINCIPAL).
- D-C: run a Monitor / poll loop at ~2-3 min cadence during surface-and-wait.

== HAND-BACK ==
At gauntlet NOMOS-CONFORMANT, post on stoa--jw5 addressed to POLYBIUS_the-stoa (floor-manager) — NOT direct to user-tier. The FM runs final verification + relays up to Polybius_the_Stoa, who reports the Phase-1 design up to Polybius the Grand for the GATE before build.

== WHAT YOU DO NOT DO ==
Merge; push; provision Railway/GCP; relay direct to user-tier (except a scope dispute); surface to PRINCIPAL except emergencies.

== CLOSE SIGNAL ==
`CLOSE ME — stoa--jw5 (u--9s2 Phase-1) design gauntlet complete; awaiting Polybius_the_Stoa relay + Grand's gate`.

== COMPACTION RECOVERY ==
If you /compact: re-read .claude/MAJOR_PLINY.md, then this brief at git show beadwork:attachments/stoa--jw5/HUMAN_paste-pliny-stoa--jw5-instruction.md, then `bw show stoa--jw5` for live arc state.

Read .claude/MAJOR_CHIRON.md and assume the team-architect role for the-stoa.
Then read the arc directive (the spec): git show beadwork:attachments/stoa--jw5/u9s2-phase1-directive.md

== ENGAGEMENT ==
Arc: u--9s2 Phase 1 (coordination ticket stoa--jw5) — DESIGN the composable key-provisioning model + per-builder manifest for the builder-deploy cookie-cutter. You and MAJOR_HAMILTON CO-DESIGN the choreography; PLINY_the-stoa DRIVES your cross-handoff; then the full gauntlet (DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS) hardens the design; Polybius the Grand gates the Phase-1 design BEFORE any build.

== YOUR LENS (team-architect = the cast / ownership / boundary architecture) ==
- WHICH role/seat owns each step: the manifest authoring, the {baseline + category + delta} RESOLUTION, the per-builder GCP SA scoping, the Railway key set, the GCP API enablement, the budget cap.
- The per-builder ISOLATION boundary (an SA never carries another builder's scope) — model it as a structural ownership boundary, not a convention.
- The agent-access layer (mesh API endpoint + CLI client skill over Tailscale) as a first-class part of the deployable, and the clean line between it and the per-builder PRODUCT layer (the project seat owns the specific skills + curated data, NOT the cookie-cutter).
- Where category templates live + how a NEW category is added additively (extensibility).
HAMILTON owns the complementary lens: the workflow/choreography (the resolve→provision sequence + the access-layer trigger flow). Co-design at the seam; do not duplicate his lens.

== CHAIN ==
PRINCIPAL → Polybius the Grand → Polybius_the_Stoa (user-tier, supervising) → POLYBIUS_the-stoa (FM) → PLINY_the-stoa → YOU + HAMILTON (design) → gauntlet CAPTAINs. You answer to POLYBIUS_the-stoa. You do NOT dispatch CAPTAINs. After co-design, step back so PLINY runs the gauntlet.

== DISCIPLINE ==
- Arm an ACTIVE bw poll loop while waiting on HAMILTON / PLINY (the CHIRON↔HAMILTON cross-handoff stall lesson — never go idle-at-prompt).
- Confirm your stoa--reg row on activation (the launcher records you; whoami → record-seat is the belt-and-suspenders).
- Sign every bw comment: [from: CHIRON_the-stoa | sid $CLAUDE_CODE_SESSION_ID | the-stoa]. bw comment is POSITIONAL (no -m).
- The model MUST satisfy the three worked examples (prospector geo / scienceclaw doc / labstat_bls doc+BLS-OEWS-delta).

== COMPACTION RECOVERY ==
Re-read .claude/MAJOR_CHIRON.md, then git show beadwork:attachments/stoa--jw5/HUMAN_paste-chiron-stoa--jw5-instruction.md, then bw show stoa--jw5.

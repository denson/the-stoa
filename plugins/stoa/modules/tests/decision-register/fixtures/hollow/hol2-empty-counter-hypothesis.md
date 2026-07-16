SCENARIO: "A decided dilemma (build vs. buy auth) where the agent wrote the entry but left the counter-hypothesis line empty. The DC4 detector negative control for the empty-field case."
EXPECT: write-but-hollow
WHY: NEGATIVE CONTROL for the DC4 detector, empty-field variant. A decided dilemma was correctly written, but the COUNTER-HYPOTHESIS value is empty. --check-corpus MUST flag it hollow (empty counter-hypothesis), proving the detector catches the empty-field hollow pattern, not just the denylist-phrase pattern.
ENTRY:
DR-ID: 2026-06-22T17-35-00Z-hollow-build-vs-buy
WHEN: 2026-06-22T17:35:00Z
CHECKPOINT: explicit-call
DILEMMA: Build our own auth vs. buy a vendor SSO.
WARNING: Buying accepts ongoing per-seat fees and vendor lock-in.
OPTIONS: build own auth ~ buy vendor SSO ~ adopt open-source self-hosted SSO
CHOSEN: buy vendor SSO
COUNTER-HYPOTHESIS:
CONTEXT-LINK: stoa--7gl arc-71 hollow negative control

SCENARIO: "A decided dilemma (which region first) where the agent wrote the entry but the counter-hypothesis reads 'time will tell.' Another DC4 detector negative control on the denylist."
EXPECT: write-but-hollow
WHY: NEGATIVE CONTROL for the DC4 detector, second denylist phrase. A decided dilemma was correctly written, but the COUNTER-HYPOTHESIS is 'time will tell' -- on the vacuity denylist. --check-corpus MUST flag it hollow, confirming the detector catches more than one canonical hollow phrase, not just a single hardcoded string.
ENTRY:
DR-ID: 2026-06-22T17-40-00Z-hollow-region
WHEN: 2026-06-22T17:40:00Z
CHECKPOINT: prioritization
DILEMMA: Launch EU region first vs. US-East first under a fixed team.
WARNING: EU-first defers the larger US-East pipeline by a quarter.
OPTIONS: EU first ~ US-East first ~ thin multi-region beta both
CHOSEN: EU first
COUNTER-HYPOTHESIS: time will tell
CONTEXT-LINK: stoa--7gl arc-71 hollow negative control

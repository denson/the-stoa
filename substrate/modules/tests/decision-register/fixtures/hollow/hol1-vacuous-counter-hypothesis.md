SCENARIO: "A decided dilemma (ship now vs. slip) where the agent wrote the entry but filled the counter-hypothesis with 'we'll see how it goes.' This is the DC4 detector negative control: a real decision, a hollow entry."
EXPECT: write-but-hollow
WHY: NEGATIVE CONTROL for the DC4 vacuity detector. This IS a decided dilemma (all three predicate conditions held, so an entry was correctly written), but the COUNTER-HYPOTHESIS is vacuous ('we'll see') -- it matches the vacuity denylist. --check-corpus MUST flag it hollow, proving the detector catches the canonical hollow pattern it is built to catch. If --check-corpus did NOT flag this, the DC4 detector would be broken.
ENTRY:
DR-ID: 2026-06-22T17-30-00Z-hollow-ship-now
WHEN: 2026-06-22T17:30:00Z
CHECKPOINT: prioritization
DILEMMA: Ship Friday with rough edges vs. slip a week to polish.
WARNING: Some early users hit the rough onboarding flow this week.
OPTIONS: ship Friday, accept rough edges ~ slip one week to polish ~ ship a feature-flagged subset Friday
CHOSEN: ship Friday, accept rough edges
COUNTER-HYPOTHESIS: we'll see how it goes
CONTEXT-LINK: stoa--7gl arc-71 hollow negative control

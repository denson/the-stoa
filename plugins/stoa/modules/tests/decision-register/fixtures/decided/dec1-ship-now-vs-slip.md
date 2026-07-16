SCENARIO: "At a prioritization checkpoint the classifier returned DILEMMA on ship-Friday-with-rough-edges vs. slip-a-week-to-polish. The PRINCIPAL said: ship Friday, accept the rough edges."
EXPECT: write
WHY: A checkpoint fired (prioritization), the classifier returned DILEMMA, AND a path was committed (the PRINCIPAL chose ship-now). All three predicate conditions hold, so a well-formed register entry must be written. The reference ENTRY below is the exemplar --check-corpus validates for nine populated fields + a non-hollow counter-hypothesis.
ENTRY:
DR-ID: 2026-06-22T17-00-00Z-ship-now-vs-slip
WHEN: 2026-06-22T17:00:00Z
CHECKPOINT: prioritization
DILEMMA: Ship Friday with known rough edges (reputation/quality cost) vs. slip a week to polish (momentum/revenue cost). No single right answer; the call is the PRINCIPAL's.
WARNING: The team's call accepts that some early users hit the rough onboarding flow this week; that's the downside being taken on to hold the Friday date.
OPTIONS: ship Friday, accept rough edges (faster, reputational risk) ~ slip one week to polish (slower, momentum cost) ~ ship a feature-flagged subset Friday (partial, added build cost)
CHOSEN: ship Friday, accept rough edges (faster, reputational risk)
COUNTER-HYPOTHESIS: This choice was wrong if week-one onboarding-completion drops below sixty percent OR more than five users file rough-edge complaints in the first three days.
CONTEXT-LINK: stoa--7gl arc-71 prioritization checkpoint

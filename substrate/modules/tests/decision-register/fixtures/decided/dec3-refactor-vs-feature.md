SCENARIO: "At directive-lock the classifier returned DILEMMA on spend-the-sprint-refactoring vs. ship-the-requested-feature. PLINY's locked directive committed a path: do the refactor first."
EXPECT: write
WHY: Directive-lock checkpoint fired, classifier returned DILEMMA, AND the directive commits a path (refactor first). All three conditions hold. The entry captures the accepted cost (a sprint of no new feature) and a concrete counter-hypothesis.
ENTRY:
DR-ID: 2026-06-22T17-10-00Z-refactor-vs-feature
WHEN: 2026-06-22T17:10:00Z
CHECKPOINT: directive-lock
DILEMMA: Spend the sprint paying down the auth-module debt (no visible feature) vs. ship the customer-requested export feature (visible value, debt grows). The team can do one this sprint.
WARNING: Choosing the refactor means the requested export feature slips a full sprint; the requesting customer is told it is delayed, which is the cost being accepted.
OPTIONS: refactor auth debt first (no new feature, lower future risk) ~ ship export feature first (visible value, debt compounds) ~ split the sprint half-and-half (both partial, neither finished)
CHOSEN: refactor auth debt first (no new feature, lower future risk)
COUNTER-HYPOTHESIS: This was wrong if the refactor does not cut auth-related incident count by half over the next two sprints, OR if the delayed customer escalates to churn before the export ships.
CONTEXT-LINK: stoa--7gl arc-71 directive-lock checkpoint

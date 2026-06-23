SCENARIO: "At a team-spin-up checkpoint the classifier returned DILEMMA on which of two over-demanding customers to drop. The PRINCIPAL decided: keep the strategic logo, cut the high-revenue churn-risk account."
EXPECT: write
WHY: Checkpoint fired (team-spin-up), classifier returned DILEMMA, AND the PRINCIPAL committed to a path (cut the churn-risk account). All three conditions hold; an entry must be written with the warning (revenue hit) and a falsifiable counter-hypothesis.
ENTRY:
DR-ID: 2026-06-22T17-05-00Z-which-customer-to-cut
WHEN: 2026-06-22T17:05:00Z
CHECKPOINT: team-spin-up
DILEMMA: Keep the strategic-logo customer (low revenue, high reference value) vs. keep the high-revenue account (large bill, high churn risk and support drain). Capacity allows only one.
WARNING: Cutting the high-revenue account drops near-term recurring revenue by a known amount the PRINCIPAL is accepting in exchange for support-load relief and the strategic logo.
OPTIONS: keep strategic logo, cut churn-risk account (revenue hit, support relief) ~ keep high-revenue account, cut strategic logo (revenue held, reference lost) ~ keep both at reduced SLA (revenue held, quality risk both)
CHOSEN: keep strategic logo, cut churn-risk account (revenue hit, support relief)
COUNTER-HYPOTHESIS: This was wrong if dropping the account fails to recover at least one engineer-week per sprint of support capacity within two months, OR the strategic logo does not produce a single referenceable deal in two quarters.
CONTEXT-LINK: stoa--7gl arc-71 team-spin-up checkpoint

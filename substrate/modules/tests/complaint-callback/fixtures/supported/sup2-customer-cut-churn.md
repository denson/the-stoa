SCENARIO: "A month ago the PRINCIPAL decided to cut the enterprise customer Brightwave to free up roadmap capacity. The decision was logged. Now Brightwave churned and took two referral accounts with them — the referral-network cost that was flagged. The PRINCIPAL is complaining about that decided cut."
COMPLAINT: "Cutting Brightwave backfired — they churned and dragged two referral accounts out with them. That call cost us the referral network."
EXPECT: surface
WHY: A decided call (cut Brightwave) with a logged entry whose WARNING names the now-biting cost — losing Brightwave's referral accounts. The gate returns SUPPORTED; surface the record honestly. The reference ENTRY's WARNING content-overlaps the COMPLAINT (brightwave, referral, accounts, churn) — the deterministic "record supports" exemplar.
ENTRY:
DR-ID: 2026-05-24T14-30-00Z-which-customer-to-cut
WHEN: 2026-05-24T14:30:00Z
CHECKPOINT: prioritization
DILEMMA: Cut the enterprise customer Brightwave to free roadmap capacity (lose their revenue and referral network) vs. keep them and stay capacity-bound (slower roadmap). A value tradeoff; the call is the PRINCIPAL's.
WARNING: Cutting Brightwave accepts losing their referral accounts — Brightwave has historically driven referral signups, and churning them risks the referral accounts they brought leaving too.
OPTIONS: cut Brightwave, reclaim capacity (lose referral network) ~ keep Brightwave, stay capacity-bound (slower roadmap) ~ partially de-scope Brightwave's contract (added negotiation cost)
CHOSEN: cut Brightwave, reclaim capacity (lose referral network)
COUNTER-HYPOTHESIS: This choice was wrong if more than one referral account churns within sixty days of cutting Brightwave.
CONTEXT-LINK: stoa--51k arc-73 prioritization checkpoint

SCENARIO: "On an explicit dilemma-check call the classifier returned DILEMMA on build-our-own-auth vs. buy-a-vendor-SSO. The PRINCIPAL chose: buy the vendor SSO."
EXPECT: write
WHY: Explicit-call checkpoint fired, classifier returned DILEMMA, AND the PRINCIPAL committed (buy). All three conditions hold. The entry records the accepted lock-in cost and a falsifiable counter-hypothesis tied to vendor risk.
ENTRY:
DR-ID: 2026-06-22T17-15-00Z-build-vs-buy-auth
WHEN: 2026-06-22T17:15:00Z
CHECKPOINT: explicit-call
DILEMMA: Build our own auth/SSO (full control, large engineering cost, ongoing security burden) vs. buy a vendor SSO (fast, recurring fee, vendor lock-in). No single right answer; depends on which cost the PRINCIPAL will carry.
WARNING: Buying the vendor SSO accepts ongoing per-seat fees and a hard dependency on one vendor's uptime and pricing; that's the lock-in cost being taken on for speed.
OPTIONS: build own auth (control, high build + security cost) ~ buy vendor SSO (fast, recurring fee, lock-in) ~ adopt an open-source self-hosted SSO (no fee, operational burden on us)
CHOSEN: buy vendor SSO (fast, recurring fee, lock-in)
COUNTER-HYPOTHESIS: This was wrong if the vendor raises per-seat pricing by more than thirty percent at renewal, OR if vendor downtime causes more than two customer-facing auth outages in the first year.
CONTEXT-LINK: stoa--7gl arc-71 explicit-call checkpoint

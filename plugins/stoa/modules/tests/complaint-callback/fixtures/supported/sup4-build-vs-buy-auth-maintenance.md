SCENARIO: "Last month the PRINCIPAL chose to build the authentication system in-house rather than buy a vendor solution, accepting the ongoing maintenance burden. The decision was logged. Now the auth maintenance load is eating two engineers' time every sprint — the maintenance cost that was flagged. The PRINCIPAL is complaining about that decided build call."
COMPLAINT: "Building auth ourselves was a mistake — the maintenance burden is eating two engineers every sprint. Why did we take this on?"
EXPECT: surface
WHY: A decided call (build auth in-house) with a logged entry whose WARNING names the now-biting maintenance burden. The gate returns SUPPORTED; surface the record honestly, forward to the fix ('what now?'), no gloating. The reference ENTRY's WARNING content-overlaps the COMPLAINT (auth, maintenance, burden, engineers) — the deterministic 'record supports' exemplar.
ENTRY:
DR-ID: 2026-05-20T09-45-00Z-build-vs-buy-auth
WHEN: 2026-05-20T09:45:00Z
CHECKPOINT: directive-lock
DILEMMA: Build the authentication system in-house (control and customization, ongoing maintenance) vs. buy a vendor solution (faster, recurring license cost, less control). A value tradeoff.
WARNING: Building auth in-house accepts an ongoing maintenance burden — keeping the auth system patched and secure will consume engineering time every sprint that a vendor would otherwise absorb.
OPTIONS: build in-house, accept maintenance burden (control, ongoing engineer time) ~ buy vendor solution (faster, license cost, less control) ~ build a thin wrapper over an open-source library (middle maintenance)
CHOSEN: build in-house, accept maintenance burden (control, ongoing engineer time)
COUNTER-HYPOTHESIS: This choice was wrong if auth maintenance consumes more than one engineer-week per sprint within two months of shipping.
CONTEXT-LINK: stoa--51k arc-73 directive-lock checkpoint

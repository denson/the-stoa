---
author: Denson Smith
ticket: stoa--jw5 (u--9s2 Phase-1)
seat: CAPTAIN_VERA_the_stoa (VERIFIER)
verifies: agents/design/stoa--jw5/strabo-gcp-budget-cap.md
sampling: full
as_of: 2026-06-25
---

# VERA — STRABO GCP budget-cap citation verification

**Overall verdict: INCOMPLETE (pass on every cited citation; one synthesis
overreach in Q3 must be qualified before the artifact is load-bearing).**

Every one of STRABO's cited URLs was independently re-fetched at the CURRENT
`docs.cloud.google.com` host (the brief-flagged 301 from `cloud.google.com`
confirmed live), and every quoted span STRABO attributed to those pages is
present VERBATIM. No citation was fabricated, stretched, or stale. The
load-bearing architectural conclusion — **a hard per-builder budget cap forces
one GCP project per builder** — SURVIVES verification.

The single reason this is INCOMPLETE rather than a clean `pass`: STRABO's Q3
synthesis sentence "There is NO native, single-switch hard auto-cap at any scope
as of 2026-06-25" is OVERBROAD. A native project-level auto-pause **Spend Caps**
feature DOES exist (Google Cloud Next 2026 / April 2026, **Private Preview**,
service-limited). It does not flip the conclusion (see Q3/Q4 below), but the
absolute "at any scope / no native auto-cap" wording is not supported by the
cited GA pages and is contradicted by the preview feature CHIRON flagged. The
citations are sound; the GENERALIZATION drawn over them overreaches.

---

## Per-claim probes

### Probe 1 — No per-SA hard spend cap; budgets cannot scope to an SA/IAM principal; SA spend bills to its project
- **quadrant_classification:** hard-easy (documentation citation: find the claim, re-fetch + read the scope list — falsifying is cheap once located).
- **source re-fetched:** https://docs.cloud.google.com/billing/docs/how-to/budgets (200 OK, as-of 2026-06-25)
- **supporting text (verbatim):** the page enumerates budget scopes as "organizations, folders, or projects", "one or more services, such as Compute Engine or BigQuery", "Resources that have a specific label applied to them", and reseller "subaccounts". Service account / IAM principal is **NOT** in the enumeration.
- **result: CONFIRMED.** No SA/IAM-principal scope dimension exists; the claim that SA spend bills to its project (not to the SA) is consistent with the page's project-as-billing-unit model.

### Probe 2 — Budget scoping granularity = billing-account / org / folder / project / service / resource-label; per-SA NOT among them
- **quadrant_classification:** hard-easy (documentation citation, same page).
- **source re-fetched:** https://docs.cloud.google.com/billing/docs/how-to/budgets (200 OK, as-of 2026-06-25)
- **supporting text (verbatim):** scopes = entire billing account; "organizations, folders, or projects"; "one or more services"; "Resources that have a specific label applied to them"; reseller "subaccounts".
- **result: CONFIRMED.** Per-SA is not among the enumerated scopes.
- **minor note:** STRABO's artifact additionally lists "savings types" as a scope dimension; the current live page text I retrieved did NOT surface a "savings types" scope. This is a non-material extra item (it does not bear on any of the 5 load-bearing claims) — recorded for honesty, not a falsification.

### Probe 3 — Budgets are ALERTING ONLY; setting a budget does not automatically cap usage/spending; no native hard auto-cap at any scope
- **quadrant_classification:** hard-hard for the SYNTHESIS half ("no native auto-cap at ANY scope" is an unbounded negative-existence claim); hard-easy for the two QUOTED spans.
- **source re-fetched:** https://docs.cloud.google.com/billing/docs/how-to/budgets (200 OK, as-of 2026-06-25)
- **supporting text (verbatim):**
  - "Setting a budget does not automatically cap Google Cloud or Google Maps Platform usage or spending."
  - "Budget alert emails might prompt you to take action to control your costs, but they don't automatically prevent the use or billing of your services when the budget amount or threshold rules are met or exceeded."
- **result: CONFIRMED on the quoted spans; REFUTED on the absolute "no native auto-cap at any scope" synthesis.**
  The two quotes are present verbatim — classic Cloud Billing **budgets** are indeed alerting-only. HOWEVER, an independent current-docs probe (the discrepancy CHIRON raised) establishes that a NATIVE project-level auto-pause feature **Spend Caps** exists: announced Google Cloud Next 2026 (April 2026), **Private Preview**, enforces cost boundaries at the **project level** and **pauses API traffic** (returns client 429/503) rather than tearing resources down, covering a SERVICE-LIMITED list (Google AI Studio, Gemini Enterprise Agent Platform / Vertex, Cloud Run, Cloud Run Functions, Google Maps).
  - I attempted the canonical first-party docs page `https://docs.cloud.google.com/billing/docs/how-to/spend-caps` → **HTTP 404**. There is NO GA documentation page for Spend Caps at the canonical URL; the feature is preview-gated (blog + whitelisted console only). I therefore do NOT treat Spend Caps as a verified GA capability — but its existence as a native project-level auto-cap is sufficient to make STRABO's absolute "no native hard auto-cap at any scope" wording UNSAFE as written.
- **impact:** STRABO's Q3 must be re-worded from "no native hard auto-cap at any scope" to "classic Cloud Billing budgets are alerting-only; the only native project-level auto-cap is the **Spend Caps** Private Preview (service-limited, not GA-documented), and there is no SUB-project or per-SA auto-cap." That qualification does not change the architecture conclusion (Probe 4).

### Probe 4 — Project is the finest scope a budget binds => hard per-builder cap requires one project per builder
- **quadrant_classification:** hard-hard (architectural-synthesis claim built on the prior probes) — sanity-checked, not exhaustively proven.
- **sources re-fetched:** https://docs.cloud.google.com/billing/docs/how-to/budgets + https://docs.cloud.google.com/billing/docs/how-to/disable-billing-with-notifications + https://docs.cloud.google.com/apis/docs/capping-api-usage (all 200 OK, as-of 2026-06-25)
- **supporting text (verbatim, capping-api-usage):** "These limits are intended for granular control of specific service volumes and aren't designed to act as a project-wide spending cap." and "Depending on the API, you can explicitly cap requests by limiting the requests per day, requests per minute, or requests per minute per user." — confirms quotas are request/rate limits, NOT dollar caps (STRABO's Q4 quota footnote holds).
- **result: CONFIRMED — and it SURVIVES the Probe 3 Spend Caps wrinkle.** The finest scope at which any dollar-denominated control (budget or Spend Cap) binds is the **PROJECT**: budgets scope no finer than project; the Spend Caps preview is explicitly project-level; the kill-switch detaches billing per-project; quotas cap request volume not dollars. There is no sub-project ($-)cap and no per-SA ($-)cap. Therefore attaching a real per-builder dollar boundary still requires a per-builder PROJECT. The architecture conclusion holds regardless of whether Spend Caps GA's.

### Probe 5 — budget->PubSub->CloudFunction kill-switch is Google-documented but REACTIVE/LAGGING, not a hard cap
- **quadrant_classification:** hard-easy (documentation citations across two pages).
- **sources re-fetched:** https://docs.cloud.google.com/billing/docs/how-to/disable-billing-with-notifications + https://docs.cloud.google.com/billing/docs/how-to/notify (both 200 OK, as-of 2026-06-25)
- **supporting text (verbatim):**
  - "automatically disable billing on a project when your costs meet or exceed your project budget"
  - "There's a delay between incurring costs and receiving budget notifications, so you might incur additional costs for usage that hasn't arrived at the time that all services are stopped"
  - "Following the steps in this example doesn't guarantee that you won't spend more than your budget"
  - "When you disable billing on a project, you terminate all Google Cloud services in the project, including Free Tier services"
  - (notify page) "It may take several hours before you receive the first Pub/Sub notification."
  - (notify page) "Pub/Sub only guarantees at-least-once delivery. You might receive a message multiple times, and messages might arrive out of order."
- **result: CONFIRMED.** Every quoted caveat is present verbatim. The pattern is Google-documented and explicitly reactive/lagging/project-blast-radius, not a hard cap.

---

## methodology_concerns
1. **Q3 synthesis overreach (load-bearing to wording, not to conclusion).** "No native
   hard auto-cap at any scope" is contradicted by the **Spend Caps** Private Preview
   (native, project-level, auto-pause, service-limited). The cited GA pages support
   "budgets are alerting-only"; they do NOT support the absolute "no native auto-cap."
   STRABO (or CHIRON folding the artifact) should qualify the sentence. The
   architecture conclusion is unaffected because Spend Caps is itself project-level
   (no sub-project / per-SA cap).
2. **Spend Caps is NOT GA-documented.** Canonical `docs.cloud.google.com/billing/docs/how-to/spend-caps`
   returns 404; the feature is preview-gated (blog/whitelist only). It must NOT be
   relied on as a usable hard cap in the Phase-1/Phase-2 build until it GA's. If the
   design later wants Spend Caps as the per-builder cost-control mechanism for the
   covered services (Vertex/Maps are cost-dominant for this workload), that is a
   PREVIEW dependency and should be flagged as such, with the per-builder-project
   kill-switch as the GA fallback.
3. **"savings types" budget scope (Probe 2)** appears in STRABO's artifact but did not
   surface in my re-fetch of the live budgets page. Non-material to all 5 claims;
   recorded for accuracy.

## falsifying_evidence_summary
No CITATION was falsified — all five cited URLs resolve, are current, and contain
the quoted text verbatim. The verdict is INCOMPLETE (not `fail`) because one
SYNTHESIS sentence (Q3, "no native hard auto-cap at any scope") overreaches its
cited support: a native project-level auto-pause **Spend Caps** feature exists in
Private Preview (Google Cloud Next 2026 / April 2026, service-limited; canonical
docs page 404s). This qualifies STRABO's absolute wording but does NOT flip the
architecture conclusion — every dollar-denominated control (budget, Spend Cap,
kill-switch) binds no finer than the PROJECT, and quotas are request/rate limits
not dollar caps, so a hard per-builder cap still mandates one GCP project per
builder.

## verification_artifacts_path
agents/design/stoa--jw5/vera-strabo-citations-verdict.md (this file). All probes
were live WebFetch re-fetches + one gsearch (native Spend Caps locator); no
scripts written.

## summary
STRABO's artifact was re-verified at `sampling: full` against the three distinct
cited primary pages (budgets, disable-billing-with-notifications, notify), all
re-fetched at the current `docs.cloud.google.com` host with the brief-flagged 301
confirmed. The most load-bearing pass: Probe 4 — the one-project-per-builder
conclusion holds, and it holds EVEN AFTER accounting for the native Spend Caps
preview CHIRON flagged, because Spend Caps is itself project-level (no sub-project
or per-SA dollar cap exists). The most important qualification: Probe 3 — STRABO's
"no native auto-cap at any scope" is overbroad and should be narrowed to "classic
budgets are alerting-only; the only native auto-cap is the project-level Spend Caps
Private Preview (service-limited, not GA)." Verdict INCOMPLETE: citations all hold;
fix the one synthesis sentence and flag Spend Caps as a preview dependency before
this artifact gates the build.

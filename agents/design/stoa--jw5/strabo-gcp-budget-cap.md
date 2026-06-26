---
author: Denson Smith
ticket: stoa--jw5 (u--9s2 Phase-1)
seat: CAPTAIN_STRABO_the_stoa (SCOUT, external)
verification_status: needs-vera
as_of: 2026-06-25
---

# STRABO — GCP per-builder budget-cap capability check

**Question.** Does GCP support a per-SERVICE-ACCOUNT hard spend cap? The answer
decides the builder-deploy isolation architecture: a true per-SA hard cap would
permit one-shared-project + per-SA scoping; absence of one forces one GCP
project per builder. This is INDEPENDENT corroboration-or-falsification of
CHIRON's first-pass gsearch (not a rubber-stamp).

**Method.** gsearch (Gemini grounded) to locate canonical pages, then WebFetch
of the literal `cloud.google.com` / `docs.cloud.google.com` docs to confirm each
claim at the primary source. Every load-bearing claim below carries a primary
GCP-docs citation. Secondary sources are not relied on for any verdict.

---

## Verdicts

### Q1 — Per-service-account hard spend cap? → **REFUTED (no such thing exists)**
GCP Cloud Billing budgets cannot be scoped to a service account / IAM principal;
the documented budget-scope dimensions do not include the SA. A service account's
spend is billed to its PROJECT, not to the SA. There is no native per-SA cap.
- [Cloud Billing budgets — how-to (primary)](https://docs.cloud.google.com/billing/docs/how-to/budgets) — fetched 2026-06-25. The page enumerates budget scopes (billing account / org / folder / project / service / labels / reseller subaccounts / savings types) and does NOT list service-account or IAM-principal scoping.

### Q2 — Budget/quota scoping granularity → **CONFIRMED: billing-account / org / folder / PROJECT / service / resource-label (NOT per-SA)**
Primary docs enumerate exactly: entire Cloud Billing account, organizations and
folders, individual projects, services, resource labels (plus reseller
subaccounts and savings types). Per-SA is NOT among them. Resource labels are the
only sub-project attribution axis, and labels are a post-hoc cost-attribution
tool, not an SA-bound enforcement boundary.
- [Cloud Billing budgets — how-to (primary)](https://docs.cloud.google.com/billing/docs/how-to/budgets) — fetched 2026-06-25.

### Q3 — Native auto-pause "spend cap" at project level? → **REFUTED (no native hard auto-cap; budgets are ALERTING only)**
Quoting the primary docs verbatim: *"Setting a budget does not automatically cap
Google Cloud or Google Maps Platform usage or spending. Budgets trigger alerts to
inform you of how your usage costs are trending over time."* And: *"Budget alert
emails ... don't automatically prevent the use or billing of your services when
the budget amount or threshold rules are met or exceeded."* There is NO native,
single-switch hard auto-cap at any scope as of 2026-06-25.
- [Cloud Billing budgets — how-to (primary, quoted)](https://docs.cloud.google.com/billing/docs/how-to/budgets) — fetched 2026-06-25.

### Q4 — Does a hard per-builder cap require ONE GCP PROJECT PER BUILDER? → **CONFIRMED**
Because (Q1) there is no per-SA cap and (Q2) the finest enforcement scope at which
a budget binds is the PROJECT, the only way to attach a real budget boundary to a
single builder is to give that builder its own project. Google's own kill-switch
tutorial (Q5) operates strictly at project granularity — it detaches billing from
a project, shutting down all resources in THAT project. Therefore per-builder
HARD budget isolation ⇒ one GCP project per builder. (Labels give attribution,
not a cap; quotas cap API usage per project/SA but are unit/rate limits, not a
dollar cap.)
- [Cloud Billing budgets — how-to (primary)](https://docs.cloud.google.com/billing/docs/how-to/budgets) — fetched 2026-06-25.
- [Disable billing with notifications (primary, project-scope)](https://docs.cloud.google.com/billing/docs/how-to/disable-billing-with-notifications) — fetched 2026-06-25.

### Q5 — Budget → Pub/Sub → Cloud Function kill-switch: Google-documented? Hard or reactive? → **CONFIRMED as Google-documented; NUANCED: it is REACTIVE (lagging), NOT a hard cap**
Google documents this exact pattern. It is explicitly reactive, not a hard cap.
Primary-source caveats, quoted:
- *"automatically disable[s] billing on a project when your costs meet or exceed your project budget"* — but
- *"There's a delay between incurring costs and receiving budget notifications, so you might incur additional costs for usage that hasn't arrived at the time that all services are stopped."*
- *"Following the steps in this example doesn't guarantee that you won't spend more than your budget."*
- *"This tutorial removes Cloud Billing from your project, shutting down ALL resources."* (project-level blast radius, incl. Free Tier).
- Notification timing: *"It may take several hours before you receive the first Pub/Sub notification"*; Pub/Sub is at-least-once and may arrive out of order.
- [Disable billing with notifications (primary, quoted)](https://docs.cloud.google.com/billing/docs/how-to/disable-billing-with-notifications) — fetched 2026-06-25.
- [Cloud Billing budget notifications (primary, timing/delivery)](https://docs.cloud.google.com/billing/docs/how-to/notify) — fetched 2026-06-25.

---

## CONSEQUENCE FOR DESIGN

**CORROBORATES CHIRON.** Independent current-docs verification confirms CHIRON's
conclusion: GCP has no per-SA spend cap; budgets are alerting-only and scope no
finer than the PROJECT; the only documented "cap" is a project-level, reactive,
lagging kill-switch (budget → Pub/Sub → Cloud Function detaches billing) that
Google itself disclaims as not guaranteeing you stay under budget. Therefore
**per-builder HARD budget isolation MANDATES one GCP project per builder.** The
"one shared project + per-SA scoping" shape cannot deliver a budget cap at all and
is NOT a valid fallback for the LOCK. The kill-switch belongs in the design as a
project-level reactive footnote, NOT as an isolation tier.

**Seam impact (HAMILTON):** provisioning sequence must create/select the
per-builder GCP PROJECT first → SA-in-project → scope-bind → PROJECT-LEVEL budget
+ (optional) project-level kill-switch. The budget-cap step is project-level.

---

## Confidence & gaps
- **Confidence: HIGH.** All five verdicts rest on quoted primary `cloud.google.com`
  docs fetched 2026-06-25, not training memory or gsearch synthesis.
- **Gap (minor):** Quotas (APIs & Services → Quotas) can cap API REQUEST/usage
  volume per project (and some per-SA rate limits exist), but these are
  unit/rate limits, not a DOLLAR cap — they do not change the per-project-budget
  conclusion. Not separately fetched at primary source; flagged for VERA if the
  design later leans on quota-based capping.
- **Falsifier:** this verdict flips only if Google ships a native per-SA dollar
  cap OR a sub-project hard auto-cap. No evidence of either as of 2026-06-25.
- `verification_status: needs-vera` — citations should be VERA-resampled before
  this artifact becomes load-bearing for the build-gate (per §6.6).

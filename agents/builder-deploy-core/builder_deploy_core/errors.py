# author: Denson Smith
# ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR) — promotes the VERIFIED Phase-1 prototypes
# design-ground-truth: agents/design/stoa--pj3/design-rev2.md §2.1 (errors.py) / §2.4.1 (DataIntegrityError)
#
# Single home for the builder-deploy-core exception classes. Five classes total.
# The first four signal a fail-closed REFUSAL of a builder's *input manifest*; the fifth
# (DataIntegrityError, §2.4.1) signals a corrupt *core DATA asset* — a different failure class
# (the cookie-cutter's own ground truth is broken, not the builder's declaration).

from __future__ import annotations


class ResolutionError(Exception):
    """§2.4 ERROR — unknown category; resolve raises, provisioning aborts (fail-closed)."""


class BaselineOmitError(Exception):
    """§2.4 / §2.6 ERROR — delta.omit targets a non-omittable BASELINE entry (fail-closed, WP-6 fix)."""


class UncatalogedServiceError(Exception):
    """§19 G1 / §20 V1 — a service-id absent from the catalog. fail-closed: STOP, do not emit."""


class ValidationError(Exception):
    """§20 V1-V5 ERROR — a generated manifest that fails a validation check. fail-closed (never enters S0)."""


class DataIntegrityError(Exception):
    """§2.4.1 ERROR — a core DATA asset (baseline/kinds/categories/catalog) violates a load-time
    invariant. dataload raises this fail-closed, with NO partial load: a degraded/incomplete DATA
    body never escapes the load boundary. Distinct from the four manifest-refusal errors above: this
    signals the cookie-cutter's own ground truth is broken, not a builder's input."""

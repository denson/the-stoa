# author: Denson Smith
# ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR) — promoted VERBATIM from the VERIFIED Phase-1 prototype
# prototype-source: agents/design/stoa--jw5/discovery-check/generate.py (VERIFIED)
# design-ground-truth: agents/design/stoa--pj3/design-rev2.md §2.1 ; §19 (G1-G4) / §22 / §21.2 / §17.2.3
#
# generate(services_called, catalog, categories, baseline) -> {category, delta:{add,omit}} per §19 G1-G4.
# DETERMINISTIC + PURE: same (services_called, catalog, categories) => byte-identical manifest.
# Baseline is NOT discovered (§19 preamble) — generation determines only the category + delta layer;
# resolve() prepends BASELINE. We READ baseline (for G3's `called \ (baseline u category)`) from the
# dataload-loaded baseline so it stays the single source of truth (the §2 resolver is untouched).
#
# Provisions NOTHING; reads no environment.
#
# PROMOTION (the ONLY logic-byte edit vs the Phase-1 prototype): UncatalogedServiceError moves to the
# shared errors.py home (§2.1) and is imported, not defined locally. The G1-G4 algorithm is verbatim.

from __future__ import annotations

from builder_deploy_core.errors import UncatalogedServiceError


def _ent(e):
    """Normalize a {kind,name} dict to a (kind, name) tuple (the §2.2 entry identity)."""
    return (e["kind"], e["name"])


def _entset(entries):
    return {_ent(e) for e in entries}


def best_fit_emergent_category(called_entries, categories):
    """§19 G2 — the emergent category whose entry-set is the LARGEST SUBSET of called_entries
    (maximal coverage, no over-reach). Ties / no cover -> None (delta carries all).

    Determinism (§19.2): pure max-subset selection; tie broken by category-tag (name) ASCENDING.
    Returns the category name (str) or None.
    """
    called = set(called_entries)
    best_name = None
    best_size = 0
    for cat_name in sorted(categories):                 # category-tag ascending -> deterministic tie-break
        bundle = _entset(categories[cat_name])
        if bundle and bundle <= called:                 # bundle is a SUBSET of called_entries (no over-reach)
            size = len(bundle)
            if size > best_size:                        # strictly-larger wins; sorted() makes ties pick asc tag
                best_name = cat_name
                best_size = size
    return best_name


def generate(services_called, catalog, categories, baseline):
    """§19 G1-G4. Input: builder's services-called set. Output: {category, delta:{add,omit}}.

    G1  called_entries := U over service-id of CATALOG[service-id].entries
          (kind-agnostic union; a service-id absent from catalog -> UncatalogedServiceError, fail-closed)
    G2  category := best_fit_emergent_category(called_entries)   (None if no cover / tie-to-nothing)
    G3  delta.add  := called_entries \\ (BASELINE u CATEGORY[category])
        delta.omit := CATEGORY[category] \\ (called_entries u BASELINE)
    G4  emit { category, delta:{add, omit} }

    baseline: the §3.1 BASELINE entry list (read from the dataload-loaded baseline).
    Returns a manifest dict in the §1.1 shape resolve() already consumes.
    """
    # ---- G1: union typed entries from the catalog (fail-closed on uncataloged) ----
    called_entries = set()
    for sid in services_called:
        record = catalog.get(sid)
        if record is None:                              # §19 G1 / §20 V1 fail-closed
            raise UncatalogedServiceError(
                f"uncataloged service '{sid}' (cannot generate a complete manifest; add to catalog)")
        called_entries |= _entset(record["entries"])

    # ---- G2: best-fit emergent category (largest catalog bundle subset of called) ----
    category = best_fit_emergent_category(called_entries, categories)

    # ---- G3: derive delta (mechanical remainder) ----
    baseline_set = _entset(baseline)
    category_set = _entset(categories[category]) if category is not None else set()

    add_set = called_entries - (baseline_set | category_set)        # called beyond baseline+category
    omit_set = category_set - (called_entries | baseline_set)       # category entries the builder does NOT call
    # G3 invariant (§19.1): omit can NEVER hit a baseline entry — baseline is not in any category
    # (§17.2.3), so category_set is disjoint from baseline_set, and omit_set (subset of category_set)
    # cannot intersect baseline. The §2.6 BaselineOmitError guard is preserved BY CONSTRUCTION.

    def _entries_of(idents):
        # deterministic order (sorted (kind,name) asc) so the emitted manifest is stable (§19.2).
        return [{"kind": k, "name": n} for (k, n) in sorted(idents)]

    delta = {}
    if add_set:
        delta["add"] = _entries_of(add_set)
    if omit_set:
        delta["omit"] = _entries_of(omit_set)

    # ---- G4: emit ----
    manifest = {"category": category, "delta": delta}
    return manifest, sorted(called_entries)

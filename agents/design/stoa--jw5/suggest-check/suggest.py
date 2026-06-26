# author: Denson Smith
# ticket: stoa--jw5 (u--9s2 Phase-1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR) — exercises the SUGGEST front-door's testable core
# design-ground-truth: agents/design/stoa--jw5/design-formal.md §24 (SUGGEST step) /
#                       §25.1 (advisory hints, mis-propose-never-mis-provision) /
#                       §25.2 (catalog is the candidate-service SPACE; uncataloged -> V1 lineage flag)
#
# suggest(project_signals, catalog) -> (proposed_set, evidence, unknown_signals)  per §24.
#
# §24 SUGGEST: the agent EXAMINES the project across 4 signal surfaces (sdk_imports / url_patterns /
# config_keys / data_signals), MATCHES each project signal against the catalog's §25 detection_hints,
# and PROPOSES the candidate service-id set WITH per-candidate evidence (which signal matched which
# hint). The candidate space is CATALOG-BOUNDED (§25.2 invariant 2): only services that EXIST in the
# catalog can be proposed. An examined signal with NO catalog match -> flagged "unknown service — add
# to catalog" (the §20 V1 every-service-cataloged lineage, one layer up).
#
# RECOMMENDATION-ONLY (§24 / §25.1): the output is INERT. It is NOT a DECLARE set; it has NO effect
# downstream until the §26 human-confirm gate ratifies it. This module produces a proposal; confirm.py
# is the ONLY edge from PROPOSE -> DECLARE. suggest() NEVER touches `entries` (the hard recipe) — it
# reads detection_hints ONLY (§25.2 invariant 1, hint-agnostic generation preserved).
#
# Provisions NOTHING; reads NO environment (pure function of (project_signals, catalog)).

from __future__ import annotations

try:
    from catalog_hints import HINT_FIELDS
except ImportError:  # allow import as a package member
    from .catalog_hints import HINT_FIELDS  # type: ignore


# A project_signals dict mirrors the catalog detection_hints surfaces — it is the EXAMINE output:
# what the agent observed the project actually doing, bucketed by the four §24 surfaces.
#   { "sdk_imports": [...], "url_patterns": [...], "config_keys": [...], "data_signals": [...] }
# Each list holds the concrete observed tokens (an imported package, a hit outbound hostname, a read
# config key, a data-flow signal). A token MATCHES a service iff it is a member of that service's
# detection_hints list for the same surface.


def _match_signal_to_services(surface, token, catalog):
    """Return the list of (service_id, matched_hint) the given observed token matches on `surface`.

    A token matches a service iff `token` is in that service's detection_hints[surface] list.
    Exact membership (the §25 hints are concrete recognizable signals). Catalog-bounded by
    construction: we only ever iterate catalog services (§25.2 invariant 2).
    """
    hits = []
    for sid, record in catalog.items():
        hints = record.get("detection_hints") or {}
        for hint in hints.get(surface, []):
            if token == hint:
                hits.append((sid, hint))
    return hits


def suggest(project_signals, catalog):
    """§24 SUGGEST — examine -> match catalog detection_hints -> propose + evidence.

    Inputs:
      project_signals: the EXAMINE output — observed tokens bucketed by the 4 §24 surfaces
                       (sdk_imports / url_patterns / config_keys / data_signals).
      catalog:         the §22 seed catalog EXTENDED with §25 detection_hints (catalog_hints.CATALOG_HINTS).

    Returns (proposed_set, evidence, unknown_signals):
      proposed_set:   sorted list of catalog service-ids the examined signals matched (catalog-bounded).
      evidence:       { service_id: [ (surface, observed_token, matched_hint), ... ] } — WHY each
                      candidate was proposed (per-candidate, §24 S-3 PRESENT-evidence input).
      unknown_signals:[ (surface, observed_token), ... ] — observed tokens that matched NO catalog
                      service (§25.2 invariant 2: "unknown service — add to catalog"; V1 lineage).

    RECOMMENDATION-ONLY: the proposed_set is INERT. It becomes a DECLARE set ONLY via confirm() (§26).
    """
    proposed = set()
    evidence = {}          # service_id -> list of (surface, token, matched_hint)
    unknown = []           # (surface, token) with no catalog match

    for surface in HINT_FIELDS:
        for token in project_signals.get(surface, []):
            hits = _match_signal_to_services(surface, token, catalog)
            if not hits:
                # §25.2 invariant 2: an examined signal with NO catalog match.
                unknown.append((surface, token))
                continue
            for sid, matched_hint in hits:
                proposed.add(sid)
                evidence.setdefault(sid, []).append((surface, token, matched_hint))

    # deterministic evidence order (stable proposal presentation, §24 S-3)
    for sid in evidence:
        evidence[sid] = sorted(evidence[sid])

    return sorted(proposed), evidence, sorted(set(unknown))

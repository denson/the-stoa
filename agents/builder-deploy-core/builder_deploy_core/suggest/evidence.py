# author: Denson Smith
# ticket: stoa--fdf (u--9s2 Phase-2 increment 2.2)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR) — NEW §2.5 / §4-decision #3 artifact
# design-ground-truth: agents/design/stoa--fdf/design-rev2.md §2.5 (anti-rubber-stamp confirm-contract) /
#                      §4-decision #3 (the CandidatePresentation shape + three invariants) / §3 P4a/P4b
#
# The CONFIRM-CONTRACT data layer (§2.5 / §4 #3). The fail-closed PROPERTY (confirm.py) governs WHAT
# counts as a DECLARE; THIS contract governs HOW the proposal is PRESENTED so a human reviews REASONS,
# not a blind yes/no. It is a DATA SHAPE + three machine-checkable invariants (the UX rendering of this
# shape is the only Phase-2-deferred piece; the contract the UX must honor is named here).
#
# Provisions NOTHING; reads NO environment. Pure data + pure functions.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple


# An evidence row is (surface, observed_token, matched_hint) — the §24 S-3 per-candidate WHY:
# which examined surface carried which observed token that matched which catalog detection_hint.
EvidenceRow = Tuple[str, str, str]


@dataclass(frozen=True)
class CandidatePresentation:
    """§4-decision #3 — the gate-presentation record for ONE proposed candidate.

    The human sees, per candidate:
      service_id      — the proposed catalog service.
      entries_preview — the HARD recipe this service WOULD provision if confirmed (from §17.1 entries) —
                        so the human sees the CONSEQUENCE (e.g. google-maps ⇒ provisions MAPS_API_KEY).
                        A list of {kind, name} dicts (the catalog record's `entries`, READ not mutated).
      evidence        — the per-candidate WHY: [(surface, observed_token, matched_hint), …] — reasons,
                        NOT a yes/no. Non-empty for every genuinely-proposed candidate (P4a).
      source          — provenance per candidate: "symbolic" (Layer S, deterministic) | "neuro"
                        (Layer N, LLM-inferred — visibly flagged as lower-confidence for human scrutiny).
    """

    service_id: str
    entries_preview: List[dict]
    evidence: List[EvidenceRow]
    source: str = "symbolic"


def build_presentation(proposed, evidence, catalog, *, sources=None) -> List[CandidatePresentation]:
    """Materialize the §2.5 CandidatePresentation list for a SUGGEST proposal.

    Inputs:
      proposed: the suggest() proposed service-id list.
      evidence: the suggest() evidence dict { sid: [(surface, token, hint), …] }.
      catalog:  the load_catalog() CATALOG dict { sid: {entries, gcp_api, category} } — read for the
                entries_preview (the CONSEQUENCE the human must see). READ-only; never mutated.
      sources:  optional { sid: "symbolic"|"neuro" } provenance map; defaults to "symbolic" per candidate.

    Returns a list of CandidatePresentation, one per proposed candidate, in the proposed (sorted) order.
    This is the materialization invariant-1 (no bulk blind-accept) requires before a CONFIRM is honored.
    """
    sources = sources or {}
    presentation = []
    for sid in proposed:
        record = catalog.get(sid) or {}
        entries_preview = [dict(e) for e in record.get("entries", [])]  # READ copy, never mutate catalog
        presentation.append(
            CandidatePresentation(
                service_id=sid,
                entries_preview=entries_preview,
                evidence=list(evidence.get(sid, [])),
                source=sources.get(sid, "symbolic"),
            )
        )
    return presentation


@dataclass(frozen=True)
class ConfirmContractCheck:
    """The machine-checkable result of validating a confirm-contract presentation against the three
    §4-#3 anti-rubber-stamp invariants. ok == True iff all three hold."""

    ok: bool
    has_per_candidate_evidence: bool   # invariant: every candidate carries non-empty evidence (P4a)
    presentation_materialized: bool    # invariant 1: no bulk blind-accept (presentation exists per candidate)
    sources_flagged: bool              # invariant: every candidate carries a source provenance tag
    detail: Tuple[str, ...] = field(default_factory=tuple)


def check_contract(presentation: List[CandidatePresentation], proposed) -> ConfirmContractCheck:
    """Validate a CandidatePresentation list against the §4-#3 anti-rubber-stamp invariants (P4b).

    Invariant 1 (NO bulk blind-accept): there is a materialized CandidatePresentation for EVERY proposed
      candidate — a CONFIRM against an un-presented proposal cannot be honored (confirm_presented()).
    Per-candidate evidence: every presented candidate carries a non-empty evidence list (reasons, not
      yes/no) — the §24 S-3 PRESENT-evidence input.
    Source-flagged: every candidate carries a source provenance tag (symbolic|neuro) so an LLM-inferred
      candidate is visibly lower-confidence.

    (Invariant 2 — per-candidate EDIT — is exercised by confirm()'s EDIT path; invariant 3 — no-response
     ⇒ ⊥ — is the confirm() fail-closed default. Both are checked in the confirm() layer / P2 probes;
     this function checks the PRESENTATION-shape invariants, P4b.)

    Returns a ConfirmContractCheck (ok iff all hold). Pure; provisions nothing.
    """
    detail = []
    presented_ids = {cp.service_id for cp in presentation}
    materialized = set(proposed) <= presented_ids
    if not materialized:
        detail.append(f"un-presented proposed candidates: {sorted(set(proposed) - presented_ids)}")

    has_evidence = all(len(cp.evidence) > 0 for cp in presentation)
    if not has_evidence:
        detail.append(
            "candidate(s) with empty evidence: "
            + str([cp.service_id for cp in presentation if not cp.evidence])
        )

    sources_flagged = all(cp.source in ("symbolic", "neuro") for cp in presentation)
    if not sources_flagged:
        detail.append(
            "candidate(s) with no/unknown source tag: "
            + str([cp.service_id for cp in presentation if cp.source not in ("symbolic", "neuro")])
        )

    ok = materialized and has_evidence and sources_flagged
    return ConfirmContractCheck(
        ok=ok,
        has_per_candidate_evidence=has_evidence,
        presentation_materialized=materialized,
        sources_flagged=sources_flagged,
        detail=tuple(detail),
    )

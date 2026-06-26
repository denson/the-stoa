# author: Denson Smith
# ticket: stoa--jw5 (u--9s2 Phase-1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR) — exercises the SUGGEST front-door's testable core
# design-ground-truth: agents/design/stoa--jw5/design-formal.md §26 (human-CONFIRM FAIL-CLOSED gate) /
#                       §26.1 (D := confirm(P), the EXCLUSIVE definition) / §26.2 (HITL IS the safety mechanism)
#
# confirm(proposed, human_action) -> DECLARE (list[service_id]) | INERT  per §26.
#
# THE GATE IS THE ONLY EDGE FROM PROPOSE -> DECLARE (§26 C-3 exclusivity). FAIL-CLOSED:
#   confirm(P) = P    iff the human issues CONFIRM on P unedited
#   confirm(P) = P'   iff the human issues EDIT to P' (add/remove services) then CONFIRM
#   confirm(P) = ⊥    (INERT — NO DECLARE produced) on REJECT, no-response, edits-pending, or None
#
# ⊥ (INERT) is the load-bearing safety value: with NO DECLARE set, §18 has no input, so
# §19/§20/§2/§4 never run -> NOTHING provisions (§26.1 / §29.2). There is NO auto-promotion path:
# the ONLY way `proposed` reaches the §18 DECLARE is a human-issued CONFIRM (or EDIT-then-CONFIRM).
#
# Provisions NOTHING; reads NO environment. Pure function of (proposed, human_action).

from __future__ import annotations


class _Inert:
    """The ⊥ sentinel (§26.1). A confirm() result of INERT means NO DECLARE set was produced.

    Distinct from an EMPTY DECLARE list: INERT is "the gate did not pass — nothing flows downstream";
    an empty list would be a CONFIRMED (but empty) DECLARE. The downstream MUST test `is INERT`
    (or is_declare()) before treating a confirm() result as a DECLARE set. Falsy on purpose so a
    naive `if declare:` guard also fails closed.
    """

    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super().__new__(cls)
        return cls._singleton

    def __bool__(self):
        return False

    def __repr__(self):
        return "⊥ (INERT — no DECLARE produced)"


INERT = _Inert()   # the single ⊥ value


# The human actions the §26 C-2 gate recognizes. A "confirm" action carries the ratified set
# (which may be EDITED relative to the proposal — §26.1 P'); every other action -> ⊥.
CONFIRM = "confirm"   # accept the proposal (optionally with an edited `set`) -> DECLARE
REJECT = "reject"     # explicit reject -> ⊥
NO_RESPONSE = "no_response"   # timeout / no human action -> ⊥
EDITS_PENDING = "edits_pending"   # the human is mid-edit, has not ratified -> ⊥


def confirm(proposed, human_action):
    """§26 / §26.1 — the human-CONFIRM FAIL-CLOSED gate. The ONLY PROPOSE -> DECLARE edge.

    Inputs:
      proposed:     the suggest() proposed service-id list (INERT recommendation).
      human_action: one of
        - None                                  -> ⊥ (no human acted; fail-closed)
        - {"action": "confirm"}                  -> DECLARE = proposed (accept unedited)
        - {"action": "confirm", "set": [...]}    -> DECLARE = the EDITED ratified set (§26.1 P')
        - {"action": "reject"}                   -> ⊥
        - {"action": "no_response"}              -> ⊥
        - {"action": "edits_pending"}            -> ⊥
        - any unrecognized action                -> ⊥ (fail-closed default)

    Returns:
      a DECLARE list[service_id] (the §18 `services:` set) on CONFIRM/EDIT-then-CONFIRM;
      INERT (⊥) on everything else.

    FAIL-CLOSED DEFAULT: any input that is not an explicit CONFIRM yields ⊥. There is NO branch that
    promotes `proposed` to DECLARE without an explicit human CONFIRM (§26 C-3 exclusivity). A missing,
    malformed, or unrecognized action falls through to ⊥ — never to silent promotion.
    """
    # C-4 fail-closed: no action at all -> INERT
    if human_action is None:
        return INERT

    action = human_action.get("action") if isinstance(human_action, dict) else None

    if action == CONFIRM:
        # C-3 / §26.1: a CONFIRM is the ONLY path to DECLARE. The ratified set is authoritative:
        # if the human EDITED (supplied an explicit "set"), the edited set becomes DECLARE (P');
        # otherwise the unedited proposal becomes DECLARE (P).
        if "set" in human_action and human_action["set"] is not None:
            ratified = list(human_action["set"])     # the EDITED-confirmed set (add/remove applied)
        else:
            ratified = list(proposed)                # accept unedited
        return sorted(set(ratified))                 # deterministic DECLARE order

    # REJECT / NO_RESPONSE / EDITS_PENDING / anything unrecognized -> ⊥ (INERT), fail-closed.
    return INERT


def is_declare(result):
    """True iff confirm() produced an actual DECLARE set (not ⊥). The downstream MUST gate on this
    before feeding §18 — an INERT result has NO DECLARE and MUST NOT reach generation (§29.2)."""
    return result is not INERT

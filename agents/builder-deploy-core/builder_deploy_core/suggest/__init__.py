# author: Denson Smith
# ticket: stoa--fdf (u--9s2 Phase-2 increment 2.2)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--fdf/design-rev2.md §2.1 (suggest/ sub-package exports)
#
# builder_deploy_core.suggest — the SUGGEST front-door (u--9s2 Phase-2 increment 2.2).
# examine -> suggest -> §26 confirm (fail-closed) -> §27 P3-tagged DECLARE -> the UNCHANGED 2.1
# generate()->resolve() core. Provisions NOTHING; the proposal is INERT until the human-CONFIRM gate.
# generate/resolve are IMPORTED UNMODIFIED (module-identity, the §2-constraint) — this package defines
# NEITHER of its own.

from __future__ import annotations

from builder_deploy_core.suggest.confirm import (
    CONFIRM,
    EDITS_PENDING,
    INERT,
    NO_RESPONSE,
    REJECT,
    confirm,
    confirm_presented,
    is_declare,
)
from builder_deploy_core.suggest.declare import (
    PROVENANCE_P3,
    declare_from_confirm,
    tag_declare,
)
from builder_deploy_core.suggest.evidence import (
    CandidatePresentation,
    ConfirmContractCheck,
    build_presentation,
    check_contract,
)
from builder_deploy_core.suggest.examine import examine
from builder_deploy_core.suggest.suggest import suggest

__all__ = [
    # examine -> suggest -> confirm -> declare
    "examine",
    "suggest",
    "confirm",
    "confirm_presented",
    "is_declare",
    "INERT",
    "declare_from_confirm",
    "tag_declare",
    "PROVENANCE_P3",
    # the §26 action constants
    "CONFIRM",
    "REJECT",
    "NO_RESPONSE",
    "EDITS_PENDING",
    # the §2.5 confirm-contract layer
    "CandidatePresentation",
    "ConfirmContractCheck",
    "build_presentation",
    "check_contract",
]

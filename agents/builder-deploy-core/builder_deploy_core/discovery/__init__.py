# author: Denson Smith
# ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--pj3/design-rev2.md §2.1 / §2.3 (discovery -> resolution edge)
#
# The discovery sub-package: catalog (DATA, in data/) + generate (§19 G1-G4) + validate (§20 V1-V5).
# Depends one-directionally on resolution (the §2-constraint); resolution does not know discovery exists.

from __future__ import annotations

from builder_deploy_core.discovery.generate import (
    UncatalogedServiceError,
    best_fit_emergent_category,
    generate,
)
from builder_deploy_core.discovery.validate import validate

__all__ = ["generate", "best_fit_emergent_category", "validate", "UncatalogedServiceError"]

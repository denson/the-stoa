# author: Denson Smith
# ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--pj3/design-rev2.md §2.1 (package marker; exports)
#
# builder_deploy_core — the builder-deploy resolution + discovery CORE (u--9s2 Phase-2 inc 2.1).
# Pure software: provisions NOTHING, reads no environment beyond its own data/ tree (§2.3).
# Two sub-packages: resolution (the single source-of-truth resolver) and discovery (catalog +
# generate + validate, which IMPORTS resolution and never re-implements it — the §2-constraint).

from __future__ import annotations

from builder_deploy_core.discovery.generate import generate
from builder_deploy_core.discovery.validate import validate
from builder_deploy_core.errors import (
    BaselineOmitError,
    DataIntegrityError,
    ResolutionError,
    UncatalogedServiceError,
    ValidationError,
)
from builder_deploy_core.resolution import (
    check_runtime_completeness,
    derive_sa_scope,
    resolve,
    resolve_with_lint,
)

__all__ = [
    "resolve",
    "resolve_with_lint",
    "derive_sa_scope",
    "check_runtime_completeness",
    "generate",
    "validate",
    "ResolutionError",
    "BaselineOmitError",
    "UncatalogedServiceError",
    "ValidationError",
    "DataIntegrityError",
]

# author: Denson Smith
# ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--pj3/design-rev2.md §2.1.1 (r1 import-time module-global contract)
#
# §2.1.1 rule 1 — SINGLE population site, at import. Python runs this __init__.py before any member of
# the resolution sub-package is usable, so `import builder_deploy_core.resolution` (or any
# `from ...resolution.resolve import ...`) guarantees the §3.3 kind-tables are populated before
# derive_sa_scope / check_runtime_completeness can be called. load_kinds() runs the §2.4.1 fail-closed
# validation, so a malformed/incomplete kinds.toml raises DataIntegrityError at IMPORT — the package
# does not finish importing with degraded tables. No mutation after load (§2.1.1 rule 3).

from __future__ import annotations

from builder_deploy_core import dataload
from builder_deploy_core.resolution import resolve as _resolve_mod

# Populate the §3.3 kind-tables from DATA exactly once (assigns, never appends — §2.1.1 rule 3).
# This replaces the _UNLOADED sentinel in resolve.py with the validated kind-tables.
(
    _resolve_mod.KIND_ENUM,
    _resolve_mod.SCOPE_BEARING_KINDS,
    _resolve_mod.KEY_BEARING_PAIRING,
) = dataload.load_kinds()

# Re-export the resolver surface for callers (`from builder_deploy_core.resolution import resolve, ...`).
from builder_deploy_core.resolution.resolve import (  # noqa: E402  (must follow population)
    check_runtime_completeness,
    derive_sa_scope,
    resolve,
    resolve_with_lint,
)

__all__ = ["resolve", "resolve_with_lint", "derive_sa_scope", "check_runtime_completeness"]

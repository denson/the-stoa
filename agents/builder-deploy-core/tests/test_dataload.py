# author: Denson Smith
# ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--pj3/design-rev2.md §2.4.1 / §3 (P11; P6 READ companion)
#
# Thin pytest runner: §2.4.1 fail-closed load-validation (P11). For each committed corrupt-data/ tree,
# the matching load function RAISES DataIntegrityError naming the breached invariant (no partial load).
# Plus the P6 READ proof: the loader READS data/ (a changed DATA body changes the loaded result).

from __future__ import annotations

from pathlib import Path

import pytest

from builder_deploy_core import dataload
from builder_deploy_core.errors import DataIntegrityError

_CORRUPT = Path(__file__).resolve().parent / "fixtures" / "corrupt-data"


# (tree-name, the load fn that should raise, a substring the error names) — one per §2.4.1 invariant.
CORRUPT_CASES = [
    ("baseline-missing-pgvector", "load_baseline", "pgvector"),
    ("baseline-extra-entry", "load_baseline", "baseline"),
    ("kinds-empty-scope-bearing", "load_kinds", "scope_bearing"),
    ("category-malformed-entry", "load_library", "categories"),
    ("catalog-missing-key", "load_catalog", "category"),
    ("dangling-reference", "load_catalog", "dangling"),
]


@pytest.mark.parametrize("tree,fn_name,names_substr", CORRUPT_CASES)
def test_corrupt_tree_raises_data_integrity(tree, fn_name, names_substr):
    """P11: loading a corrupt DATA tree RAISES DataIntegrityError naming the breached invariant."""
    root = _CORRUPT / tree
    assert root.is_dir(), f"missing corrupt fixture tree: {root}"
    load_fn = getattr(dataload, fn_name)
    with pytest.raises(DataIntegrityError) as exc:
        load_fn(root)
    assert names_substr in str(exc.value), (
        f"{tree}: error did not name the breached invariant '{names_substr}': {exc.value}")


def test_baseline_missing_pgvector_returns_no_partial_baseline():
    """The canonical r2 case: load_baseline on the 4-entry baseline does NOT return a 4-entry table;
    it raises BEFORE any (degraded) table escapes the load boundary (fail-closed, no partial load)."""
    root = _CORRUPT / "baseline-missing-pgvector"
    with pytest.raises(DataIntegrityError):
        result = dataload.load_baseline(root)
        # unreachable; if it ever returned, assert it is NOT the silent 4-entry shrink.
        assert False, f"load_baseline returned a partial table instead of raising: {result}"


# ---- P6: DATA is READ (not a hardcoded literal) ----------------------------
def test_data_is_read_from_disk(tmp_path):
    """P6: the resolver READS data/ rather than a hardcoded literal. Copy a body without a fixed-set
    invariant (the catalog) into a tmp data root, add a seed, and show load_catalog reflects it."""
    import shutil

    src = Path(dataload.__file__).resolve().parent.parent / "data"
    dst = tmp_path / "data"
    shutil.copytree(src, dst)

    # add a NEW catalog seed (a body without a fixed-set invariant) -> load_catalog must reflect it.
    (dst / "catalog" / "extra-seed.toml").write_text(
        'service-id = "extra-seed"\n'
        'gcp_api = "none"\n'
        'category = "none"\n'
        "[[entries]]\n"
        'kind = "db_extension"\n'
        'name = "postgis"\n',
        encoding="utf-8",
    )
    catalog, _categories = dataload.load_catalog(dst)
    assert "extra-seed" in catalog, "load_catalog did not READ the added DATA file"

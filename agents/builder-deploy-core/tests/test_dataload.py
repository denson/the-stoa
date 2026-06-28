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

    src = Path(dataload.__file__).resolve().parent / "data"
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


# ===========================================================================
# stoa--fdf (u--9s2 Phase-2 inc 2.2) — ADDITIVE detection_hints load-validation + the rev2 WP-D2
# tolerance-PIN regression test. The 2.1 cases above are UNCHANGED.
# ===========================================================================

_REAL_DATA = Path(dataload.__file__).resolve().parent / "data"


# ---- P5a POS: load_detection_hints loads every cataloged service's hint set --------------------
def test_load_detection_hints_loads_all_services():
    """P5a (POS): load_detection_hints() loads every cataloged service's hint set from the real catalog
    TOMLs, in the flat { sid: {sdk_imports, url_patterns, config_keys, data_signals} } shape.

    Roster pin (set-equality over the canonical catalog). The roster grew from the original 4 to 6 with
    the stoa--q7f DC3 additive records (vertex-gemini + tailscale); both carry a [detection_hints] block,
    so both appear here. If a future additive catalog record lands without updating this set, the test
    fails LOUD — extend this roster (or move the hints) deliberately, do not silently widen the load."""
    hints = dataload.load_detection_hints()
    assert set(hints.keys()) == {
        "google-maps", "spatial-db", "document-parsing", "bls-oews", "vertex-gemini", "tailscale",
    }, hints.keys()
    for sid, surfaces in hints.items():
        assert set(surfaces.keys()) == {"sdk_imports", "url_patterns", "config_keys", "data_signals"}, sid
        for surface, tokens in surfaces.items():
            assert isinstance(tokens, list) and all(isinstance(t, str) and t for t in tokens), (sid, surface)
    # spot-check a known seed token (transcribed verbatim from the prototype catalog_hints).
    assert "@googlemaps/js-api-loader" in hints["google-maps"]["sdk_imports"]
    assert "api.bls.gov" in hints["bls-oews"]["url_patterns"]


# ---- P5a PIN (rev2 WP-D2): load_catalog ADMITS [detection_hints]; record shape UNCHANGED -------
def test_load_catalog_admits_detection_hints():
    """P5a-PIN (rev2 WP-D2) — PINS load_catalog's tolerance of the additive [detection_hints] key.

    Loads the REAL catalog (each record carrying its [detection_hints] block) through the UNCHANGED
    load_catalog and asserts:
      (a) the load succeeds (no DataIntegrityError);
      (b) every catalog record loads;
      (c) each record's returned shape is the unchanged {entries, gcp_api, category} — NO detection_hints
          key leaks into the catalog output (load_catalog still reads only its four fields).

    Roster pin: the canonical roster grew from the original 4 to 6 with the stoa--q7f DC3 additive records
    (vertex-gemini + tailscale), each carrying a [detection_hints] block that load_catalog must IGNORE.

    INTENT (the documented fail-LOUD tripwire): this test PINS load_catalog's tolerance of the additive
    [detection_hints] key. If a FUTURE strict-key hardening of load_catalog rejects [detection_hints],
    THIS TEST FAILS LOUD — do not silently break the catalog load; extend the hardening to admit
    detection_hints (or move the hints to a separate file) BEFORE landing it. (design-rev2 §2.3.1 — the
    §2-compliant resolution of ARGUS r1: load_catalog is BYTE-UNCHANGED; the tolerance is pinned by a
    test, not by a core edit.)
    """
    catalog, _categories = dataload.load_catalog()  # the real data/ root — records carry [detection_hints]
    assert set(catalog.keys()) == {
        "google-maps", "spatial-db", "document-parsing", "bls-oews", "vertex-gemini", "tailscale",
    }, catalog.keys()
    for sid, record in catalog.items():
        assert set(record.keys()) == {"entries", "gcp_api", "category"}, (
            f"{sid}: load_catalog record shape changed (detection_hints must NOT leak into the catalog "
            f"output): {sorted(record.keys())}")
        assert "detection_hints" not in record, f"{sid}: detection_hints LEAKED into the catalog record"


# ---- P5a NEG (rev2 WP-D2): an unknown sub-key under [detection_hints] -> DataIntegrityError ------
def test_load_detection_hints_unknown_subkey_raises(tmp_path):
    """P5a-NEG (rev2 WP-D2): an unknown sub-key UNDER [detection_hints] raises DataIntegrityError.

    ALL detection_hints validation lives in load_detection_hints (load_catalog is NOT edited). This
    mirrors the §2.4.1 fail-closed precedent load_baseline/load_kinds enforce by set-discipline. Uses a
    FIXED literal synthetic-catalog path under the pytest tmp_path (no $VAR expansion in any op, §8.6)."""
    import shutil

    dst = tmp_path / "data"
    shutil.copytree(_REAL_DATA, dst)
    # corrupt google-maps' [detection_hints] with an unknown sub-key.
    target = dst / "catalog" / "google-maps.toml"
    target.write_text(
        'service-id = "google-maps"\n'
        'gcp_api = "google-maps"\n'
        'category = "geospatial"\n'
        "[[entries]]\n"
        'kind = "gcp_api"\n'
        'name = "google-maps"\n'
        "[[entries]]\n"
        'kind = "gcp_secret"\n'
        'name = "MAPS_API_KEY"\n'
        "[detection_hints]\n"
        'sdk_imports = ["google.maps"]\n'
        'mystery = ["this-is-not-a-known-surface"]\n',   # the unknown sub-key
        encoding="utf-8",
    )
    with pytest.raises(DataIntegrityError) as exc:
        dataload.load_detection_hints(dst)
    assert "mystery" in str(exc.value) or "unknown sub-key" in str(exc.value), exc.value


def test_load_catalog_still_admits_the_corrupt_hints_block(tmp_path):
    """The PIN's flip side: load_catalog (UNCHANGED) STILL loads cleanly even when a [detection_hints]
    block carries an unknown sub-key — because load_catalog ignores the whole block (only
    load_detection_hints validates it). Proves the two loaders are independent (§2.3 / §25.2 invariant 1)."""
    import shutil

    dst = tmp_path / "data"
    shutil.copytree(_REAL_DATA, dst)
    (dst / "catalog" / "google-maps.toml").write_text(
        'service-id = "google-maps"\n'
        'gcp_api = "google-maps"\n'
        'category = "geospatial"\n'
        "[[entries]]\n"
        'kind = "gcp_api"\n'
        'name = "google-maps"\n'
        "[[entries]]\n"
        'kind = "gcp_secret"\n'
        'name = "MAPS_API_KEY"\n'
        "[detection_hints]\n"
        'mystery = ["ignored-by-load_catalog"]\n',
        encoding="utf-8",
    )
    catalog, _ = dataload.load_catalog(dst)  # MUST NOT raise — load_catalog ignores detection_hints
    assert set(catalog["google-maps"].keys()) == {"entries", "gcp_api", "category"}

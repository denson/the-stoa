# author: Denson Smith
# ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--pj3/design-rev2.md §2.6 (locked suite: fixtures-as-DATA, runner-as-code)
#
# conftest: makes the package importable (adds the package root to sys.path so `import
# builder_deploy_core` works from a plain `pytest tests/` without an install), loads the DATA tables
# once, and provides the resolve/generate/validate handles + the fixture paths.

from __future__ import annotations

import sys
import tomllib
from pathlib import Path

import pytest

# Package root = parent of tests/ (holds builder_deploy_core/ and data/).
_PKG_ROOT = Path(__file__).resolve().parent.parent
if str(_PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(_PKG_ROOT))

_FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _read_toml(path: Path) -> dict:
    with open(path, "rb") as fh:
        return tomllib.load(fh)


@pytest.fixture(scope="session")
def data_tables():
    """Load the shipped DATA tables once (baseline, library, catalog, categories)."""
    from builder_deploy_core import dataload
    baseline = dataload.load_baseline()
    library = dataload.load_library()
    catalog, categories = dataload.load_catalog()
    return {
        "baseline": baseline,
        "library": library,
        "catalog": catalog,
        "categories": categories,
    }


@pytest.fixture(scope="session")
def fixtures_dir():
    return _FIXTURES


def load_manifest_fixture(name: str) -> dict:
    """Load a manifest fixture TOML and return (manifest_dict, meta_dict)."""
    doc = _read_toml(_FIXTURES / "manifests" / f"{name}.toml")
    manifest = {"builder": doc.get("builder"), "category": doc["category"], "delta": doc.get("delta") or {}}
    return manifest, doc


def load_expected_set(name: str) -> list:
    """Load an expected resolved-set fixture TOML -> sorted list of (kind,name) tuples."""
    doc = _read_toml(_FIXTURES / "expected" / f"{name}.toml")
    return sorted((e["kind"], e["name"]) for e in doc["entry"])

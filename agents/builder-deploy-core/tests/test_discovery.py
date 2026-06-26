# author: Denson Smith
# ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--pj3/design-rev2.md §2.6 / §3 (P3, P4, P8)
#
# Thin pytest runner: §23.1 generate->resolve->8/6/7 + manifest-equivalence (P3 / DoD #2); V1-V5 +
# NEG-1 (V5 fail-closed) + NEG-2 (UncatalogedServiceError + V1 fail) (P4 / DoD #3); the §2-constraint
# (resolve is the imported resolution callable; discovery defines no resolve) (P8 / DoD #6).

from __future__ import annotations

import pytest

from builder_deploy_core.discovery.generate import UncatalogedServiceError, generate
from builder_deploy_core.discovery.validate import validate
from builder_deploy_core.resolution.resolve import resolve
from conftest import load_expected_set, load_manifest_fixture

# (fixture-name, declared services, expected G2 category, expected len)
GEN = [
    ("prospector", ["google-maps", "spatial-db"], "geospatial", 8),
    ("scienceclaw", ["document-parsing"], "document-consuming", 6),
    ("labstat_bls", ["document-parsing", "bls-oews"], "document-consuming", 7),
]


# ---- P3: generate -> resolve -> 8/6/7 EXACT + equivalence to §8 hand-authored ----
@pytest.mark.parametrize("name,services,exp_cat,exp_len", GEN)
def test_generate_resolves_to_exact_set(name, services, exp_cat, exp_len, data_tables):
    baseline, library = data_tables["baseline"], data_tables["library"]
    catalog, categories = data_tables["catalog"], data_tables["categories"]
    manifest, _called = generate(services, catalog, categories, baseline)
    assert manifest["category"] == exp_cat
    resolved = resolve(manifest, baseline, library)
    expected = load_expected_set(name)
    assert resolved == expected
    assert len(resolved) == exp_len


@pytest.mark.parametrize("name,services,exp_cat,exp_len", GEN)
def test_generated_equivalent_to_hand_authored(name, services, exp_cat, exp_len, data_tables):
    """The GENERATED manifest resolves identically to the §8 hand-authored manifest (alias-aware)."""
    baseline, library = data_tables["baseline"], data_tables["library"]
    catalog, categories = data_tables["catalog"], data_tables["categories"]
    gen_manifest, _ = generate(services, catalog, categories, baseline)
    hand_manifest, _meta = load_manifest_fixture(name)
    assert resolve(gen_manifest, baseline, library) == resolve(hand_manifest, baseline, library)


def test_labstat_generated_delta_add(data_tables):
    """§23.1: labstat_bls generated delta.add == [(thirdparty_rest_key, BLS_OEWS_API_KEY)]."""
    baseline = data_tables["baseline"]
    catalog, categories = data_tables["catalog"], data_tables["categories"]
    manifest, _ = generate(["document-parsing", "bls-oews"], catalog, categories, baseline)
    add = sorted((e["kind"], e["name"]) for e in (manifest.get("delta") or {}).get("add", []))
    assert add == [("thirdparty_rest_key", "BLS_OEWS_API_KEY")]


# ---- P4: V1-V5 pass on every positive --------------------------------------
@pytest.mark.parametrize("name,services,exp_cat,exp_len", GEN)
def test_validate_all_pass(name, services, exp_cat, exp_len, data_tables):
    baseline, library = data_tables["baseline"], data_tables["library"]
    catalog, categories = data_tables["catalog"], data_tables["categories"]
    manifest, called = generate(services, catalog, categories, baseline)
    rows = validate(
        services_called=services, generated_manifest=manifest, catalog=catalog,
        called_entries=called, baseline=baseline, library=library,
        scan_detected=services, declared_services=services)
    for cid, ok, detail in rows:
        assert ok, f"{cid} FAILED: {detail}"


# ---- P4: NEG-1 (undeclared scan drift -> V5 fail-closed) -------------------
def test_neg1_v5_fails_on_undeclared_drift(data_tables):
    baseline, library = data_tables["baseline"], data_tables["library"]
    catalog, categories = data_tables["catalog"], data_tables["categories"]
    services = ["google-maps", "spatial-db"]
    manifest, called = generate(services, catalog, categories, baseline)
    rows = validate(
        services_called=services, generated_manifest=manifest, catalog=catalog,
        called_entries=called, baseline=baseline, library=library,
        scan_detected=["google-maps", "spatial-db", "bls-oews"], declared_services=services)
    v5 = next(r for r in rows if r[0].startswith("V5"))
    assert v5[1] is False
    assert "bls-oews" in v5[2]


# ---- P4: NEG-2 (uncataloged declared -> generate raises + V1 fail) ---------
def test_neg2_generate_raises_uncataloged(data_tables):
    baseline = data_tables["baseline"]
    catalog, categories = data_tables["catalog"], data_tables["categories"]
    with pytest.raises(UncatalogedServiceError) as exc:
        generate(["document-parsing", "totally-uncataloged-svc"], catalog, categories, baseline)
    assert "totally-uncataloged-svc" in str(exc.value)


def test_neg2_v1_fails_naming_uncataloged(data_tables):
    baseline, library = data_tables["baseline"], data_tables["library"]
    catalog, categories = data_tables["catalog"], data_tables["categories"]
    services = ["document-parsing", "totally-uncataloged-svc"]
    partial, called = generate(["document-parsing"], catalog, categories, baseline)
    rows = validate(
        services_called=services, generated_manifest=partial, catalog=catalog,
        called_entries=called, baseline=baseline, library=library)
    v1 = next(r for r in rows if r[0].startswith("V1"))
    assert v1[1] is False
    assert "totally-uncataloged-svc" in v1[2]


# ---- P8: §2-constraint (resolve is the imported resolution callable) -------
def test_constraint_resolve_is_resolution_module():
    """V4's resolve resolves to builder_deploy_core.resolution.resolve — not a discovery-local copy."""
    import importlib

    validate_mod = importlib.import_module("builder_deploy_core.discovery.validate")
    assert validate_mod.resolve.__module__ == "builder_deploy_core.resolution.resolve"


def test_constraint_discovery_defines_no_resolve():
    """discovery/ never DEFINES a resolve (grep -n 'def resolve' discovery/ -> zero), the cheap
    belt-and-suspenders half of P8. Checked here by source inspection of the discovery package files."""
    import pathlib

    import builder_deploy_core.discovery as disc
    disc_dir = pathlib.Path(disc.__file__).resolve().parent
    for py in disc_dir.glob("*.py"):
        text = py.read_text(encoding="utf-8")
        assert "def resolve(" not in text, f"{py.name} defines a resolve()"

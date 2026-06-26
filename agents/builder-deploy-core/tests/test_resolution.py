# author: Denson Smith
# ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--pj3/design-rev2.md §2.6 / §3 (P1, P2, P5)
#
# Thin pytest runner over the fixtures-as-DATA: §8.1/8.2/8.3 exact sets (P1), §8.4 BaselineOmitError
# parametrized over ALL 5 baseline entries (P2 / DoD #1 R1-close generalization), §3.4 runtime-
# completeness, §3.3 kind-dispatch, §5.A SA-scope (P5 / DoD #4). Provisions nothing.

from __future__ import annotations

import pytest

from builder_deploy_core import dataload
from builder_deploy_core.errors import BaselineOmitError
from builder_deploy_core.resolution.resolve import (
    check_runtime_completeness,
    derive_sa_scope,
    resolve,
)
from conftest import load_expected_set, load_manifest_fixture

POSITIVE = ["prospector", "scienceclaw", "labstat_bls"]


# ---- P1: §8.1/8.2/8.3 exact resolved sets (byte-for-byte) -------------------
@pytest.mark.parametrize("name", POSITIVE)
def test_resolution_exact_set(name, data_tables):
    manifest, meta = load_manifest_fixture(name)
    expected = load_expected_set(name)
    got = resolve(manifest, data_tables["baseline"], data_tables["library"])
    assert got == expected
    assert len(got) == meta["expected_len"]


# ---- P2: §8.4 BaselineOmitError, parametrized over ALL 5 baseline entries ---
def test_baseline_omit_canonical_pgvector(data_tables):
    """The §8.4 canonical case: omit pgvector -> raises BaselineOmitError naming it, no set returned."""
    manifest, meta = load_manifest_fixture("badbuilder_pgvector_omit")
    with pytest.raises(BaselineOmitError) as exc:
        resolve(manifest, data_tables["baseline"], data_tables["library"])
    msg = str(exc.value)
    assert "db_extension" in msg and "pgvector" in msg


@pytest.mark.parametrize("entry", list(dataload.EXPECTED_BASELINE))
def test_baseline_omit_guard_fires_for_every_baseline_entry(entry, data_tables):
    """R1-close generalization (DoD #1): for EACH of the 5 baseline entries, an omit-that-entry
    manifest makes resolve() raise BaselineOmitError naming that entry, returning no set."""
    kind, nm = entry
    manifest = {
        "builder": "omit_probe",
        "category": "document-consuming",
        "delta": {"omit": [{"kind": kind, "name": nm}]},
    }
    with pytest.raises(BaselineOmitError) as exc:
        resolve(manifest, data_tables["baseline"], data_tables["library"])
    msg = str(exc.value)
    assert kind in msg and nm in msg


# ---- P5: §3.4 runtime-completeness ----------------------------------------
@pytest.mark.parametrize("name", POSITIVE)
def test_runtime_completeness(name, data_tables):
    manifest, _ = load_manifest_fixture(name)
    resolved = resolve(manifest, data_tables["baseline"], data_tables["library"])
    ok, missing = check_runtime_completeness(resolved)
    assert ok, f"missing pairings: {missing}"


def test_prospector_carries_both_maps_pairing(data_tables):
    """§3.4 / §8.1: prospector carries BOTH (gcp_api, google-maps) AND (gcp_secret, MAPS_API_KEY)."""
    manifest, _ = load_manifest_fixture("prospector")
    resolved = resolve(manifest, data_tables["baseline"], data_tables["library"])
    assert ("gcp_api", "google-maps") in resolved
    assert ("gcp_secret", "MAPS_API_KEY") in resolved


# ---- P5: §3.3 kind-dispatch (labstat_bls thirdparty_rest_key) --------------
def test_labstat_kind_dispatch(data_tables):
    manifest, _ = load_manifest_fixture("labstat_bls")
    resolved = resolve(manifest, data_tables["baseline"], data_tables["library"])
    assert ("thirdparty_rest_key", "BLS_OEWS_API_KEY") in resolved      # (i) present as thirdparty key
    assert ("gcp_api", "BLS_OEWS_API_KEY") not in resolved              # (ii) no gcp_api minted
    s1_apis = [n for (k, n) in resolved if k == "gcp_api"]
    assert "BLS_OEWS_API_KEY" not in s1_apis                            # (iii) excluded from S1 list


# ---- P5: §5.A SA-scope == scope-bearing subset, no foreign entry -----------
@pytest.mark.parametrize("name", POSITIVE)
def test_sa_scope_is_scope_bearing_subset(name, data_tables):
    manifest, _ = load_manifest_fixture(name)
    resolved = resolve(manifest, data_tables["baseline"], data_tables["library"])
    scope = derive_sa_scope(resolved)
    resolved_set = set(resolved)
    assert all(ent in resolved_set for ent in scope)                   # no foreign entry
    expected_scope = sorted(
        (k, n) for (k, n) in resolved
        if k in {"gcp_api", "gcp_secret", "thirdparty_rest_key"})
    assert scope == expected_scope

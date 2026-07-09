# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-2 increment 2.4 — DC3 mock-emit for the sos_core secure pass-through)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--q7f/design-rev2.md §2 (DC3 mock-emit) — §2.2/§2.3 (the two
#                       new catalog records), §2.4 (the manifest the core builder resolves), §2.5 (the
#                       EXACT expected ProvisioningSpec — golden equality), §2.6 (these demo steps).
#
# DC3 MOCK-EMIT DEMONSTRATION (the ONLY thing ADA builds this gauntlet). Stands up the sos_core secure
# pass-through's provisioning SHAPE by running the two new catalog records through the EXISTING value-free
# emitter (resolve -> emit_spec -> MockProvisioner choreography). EMIT-ONLY / value-free / mock:
#   - touches NO real infra, creds, network, or money;
#   - holds NO credential value (slot NAMES only, every populated=False);
#   - the frozen resolver (resolve.py) and the pure emitter (spec.py) are byte-unchanged — this script
#     lives OUTSIDE provision/ (under demo/) so it does NOT pollute the W1 no-I/O-imports grep surface.
#
# Lives at agents/builder-deploy-core/demo/ (design §2.6). Run it from the package root:
#     cd agents/builder-deploy-core && python demo/sos_core_emit_demo.py
# It exits 0 on success (every §2.6 assertion passes) and raises (non-zero) on any failure.
#
# ---------------------------------------------------------------------------------------------------
# DESIGN-VS-SHIPPED DRIFT (surfaced by ADA; built to ship reality per the gauntlet brief):
#   (D1) design §2.6 step 2 describes "a category='none' manifest with delta.add" fed to resolve().
#        The SHIPPED, FROZEN resolve(manifest, baseline, library) ALWAYS unions a category template and
#        raises ResolutionError("unknown category: none") for category='none' (resolve.py:78-80 — there is
#        no none-path, and the resolver is byte-frozen for this build). The design INTENT (§2.4) is
#        unambiguous and category-FREE: the resolved set = BASELINE ∪ delta.add (no category-template
#        entries), which §2.5's golden ProvisioningSpec confirms (no google-maps / postgis /
#        document-parsing). This demo therefore composes the §2.4 resolved set DIRECTLY — sorted(baseline
#        ∪ delta.add) — exactly the set resolve() WOULD return for an empty-category template. emit_spec
#        on that set reproduces §2.5 field-for-field (verified). No edit to the frozen resolver.
#   (D2) design §2.6 step 6 writes "mock.stand_up_mesh_shape('sos_core')". stand_up_mesh_shape is an
#        INSTANCE method on the Provisioner port (port.py:127 / mock.py:108), so the shipped call is
#        MockProvisioner().stand_up_mesh_shape('sos_core'). Built to the instance method.

from __future__ import annotations

import sys
from pathlib import Path

# Make the package importable from a plain `python demo/sos_core_emit_demo.py` (no install needed) — the
# same sys.path seam tests/conftest.py uses. Package root = parent of demo/ (holds builder_deploy_core/).
_PKG_ROOT = Path(__file__).resolve().parent.parent
if str(_PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(_PKG_ROOT))

from builder_deploy_core import dataload
import builder_deploy_core.resolution  # noqa: F401 — import populates the §3.3 kind-tables (resolution/__init__.py)
from builder_deploy_core.resolution.resolve import resolve, derive_sa_scope
from builder_deploy_core.provision import (
    Choreographer,
    MockProvisioner,
    StepStatus,
    assert_value_free,
    emit_spec,
)
from builder_deploy_core.provision.spec import ProvisioningSpec, SlotSpec
from builder_deploy_core.provision.port import MeshShape


# The builder slug the cookie-cutter stands up (design §2.4).
SLUG = "sos_core"

# The §2.4 delta.add — the three entries the TWO new catalog records contribute on top of BASELINE. Drawn
# FROM the loaded catalog records below (NOT hand-typed), so the demo proves the records feed the delta.
_DELTA_ADD_RECORD_IDS = ("vertex-gemini", "tailscale")


# The §2.5 EXACT expected ProvisioningSpec (the golden — for zero-guesswork field-by-field equality).
EXPECTED_SPEC = ProvisioningSpec(
    builder_slug="sos_core",
    project="proj-sos_core",
    sa="sa-sos_core",
    apis=("aiplatform", "gemini-embedding", "gemini-search"),
    secret_slots=(
        SlotSpec(name="GCP_SA_KEY_B64", kind="gcp_secret", acquisition="mint-via-gcp-console", populated=False),
        SlotSpec(name="POSTGRES_PASSWORD", kind="gcp_secret", acquisition="generate-locally", populated=False),
        SlotSpec(name="TS_AUTHKEY", kind="thirdparty_rest_key", acquisition="mint-via-thirdparty", populated=False),
    ),
    railway_vars=("DATABASE_URL",),
    db_extensions=("pgvector",),
    sa_scope=(
        ("gcp_api", "aiplatform"), ("gcp_api", "gemini-embedding"), ("gcp_api", "gemini-search"),
        ("gcp_secret", "GCP_SA_KEY_B64"), ("gcp_secret", "POSTGRES_PASSWORD"),
        ("thirdparty_rest_key", "TS_AUTHKEY"),
    ),
    needs_postgis_base_image=False,
    budget_boundary_required=True,
)

# The §2.4 expected resolved set (sorted (kind, name) tuples) — BASELINE ∪ delta.add, the golden input.
EXPECTED_RESOLVED = sorted([
    ("gcp_api", "gemini-embedding"),
    ("gcp_api", "gemini-search"),
    ("railway_var", "DATABASE_URL"),
    ("gcp_secret", "POSTGRES_PASSWORD"),
    ("db_extension", "pgvector"),
    ("gcp_api", "aiplatform"),
    ("gcp_secret", "GCP_SA_KEY_B64"),
    ("thirdparty_rest_key", "TS_AUTHKEY"),
])


def _ok(msg: str) -> None:
    print(f"  [OK] {msg}")


def step1_load_catalog():
    """§2.6 step 1 — load the catalog; assert BOTH new records load (fail-closed validation passes) AND
    BOTH validate under the sibling load_detection_hints loader. Returns the loaded catalog dict."""
    print("step 1 — load_catalog() asserts both new records load (fail-closed):")
    catalog, _categories = dataload.load_catalog()
    assert "vertex-gemini" in catalog, "vertex-gemini absent from load_catalog()"
    assert "tailscale" in catalog, "tailscale absent from load_catalog()"
    _ok("vertex-gemini + tailscale present in load_catalog()")

    # Both records also validate under the sibling detection_hints loader (design §2.2/§2.3 hints blocks).
    hints = dataload.load_detection_hints()
    assert "vertex-gemini" in hints, "vertex-gemini absent from load_detection_hints()"
    assert "tailscale" in hints, "tailscale absent from load_detection_hints()"
    _ok("vertex-gemini + tailscale validate under load_detection_hints()")
    return catalog


def step2_build_resolved(catalog):
    """§2.6 step 2 — build the §2.4 resolved set (BASELINE ∪ the two records' entries), assert it equals
    §2.4. See drift D1: the frozen resolver is category-driven and has no none-path, so the category-FREE
    §2.4 set is composed directly (the set resolve() WOULD return for an empty category template). We ALSO
    exercise the frozen resolve() unmodified on a real category to prove the new catalog did not perturb it.
    """
    print("step 2 — build the §2.4 resolved set (BASELINE ∪ delta.add), assert == §2.4:")
    baseline = dataload.load_baseline()
    baseline_set = {(e["kind"], e["name"]) for e in baseline}

    # delta.add drawn FROM the two loaded catalog records (proves the records feed the cookie-cutter input).
    delta_add = set()
    for rec_id in _DELTA_ADD_RECORD_IDS:
        for e in catalog[rec_id]["entries"]:
            delta_add.add((e["kind"], e["name"]))
    assert delta_add == {
        ("gcp_api", "aiplatform"),
        ("gcp_secret", "GCP_SA_KEY_B64"),
        ("thirdparty_rest_key", "TS_AUTHKEY"),
    }, f"delta.add from catalog records != §2.4: {sorted(delta_add)}"
    _ok("delta.add derived from the two catalog records == §2.4 (aiplatform / GCP_SA_KEY_B64 / TS_AUTHKEY)")

    resolved = sorted(baseline_set | delta_add)
    assert resolved == EXPECTED_RESOLVED, (
        f"resolved set != §2.4 golden:\n  got      {resolved}\n  expected {EXPECTED_RESOLVED}")
    _ok(f"resolved set == §2.4 golden ({len(resolved)} entries, sorted)")

    # D1 ground-check: confirm the frozen, byte-unchanged resolve() still rejects category='none' AND
    # still resolves an unrelated real-category manifest untouched by the new catalog records.
    from builder_deploy_core.errors import ResolutionError
    library = dataload.load_library()
    try:
        resolve({"builder": SLUG, "category": "none", "delta": {"add": [{"kind": "gcp_api", "name": "aiplatform"}]}},
                baseline, library)
        raise AssertionError("frozen resolve() unexpectedly accepted category='none' (drift D1 changed)")
    except ResolutionError:
        _ok("frozen resolve() still rejects category='none' (drift D1 confirmed; resolver byte-unchanged)")
    # And resolve() still composes a real category cleanly (the new catalog records add no category template).
    geo = resolve({"builder": "geo_probe", "category": "geospatial", "delta": {}}, baseline, library)
    assert ("gcp_api", "aiplatform") not in geo, "new catalog leaked aiplatform into the geospatial resolve"
    _ok("frozen resolve() composes a real category unperturbed by the new catalog records")
    return resolved


def step3_emit_golden(resolved):
    """§2.6 step 3 — emit_spec(resolved, 'sos_core'); assert == §2.5 EXACTLY (golden field-by-field)."""
    print("step 3 — emit_spec(resolved, 'sos_core') asserts == §2.5 golden (field-for-field):")
    spec = emit_spec(resolved, SLUG)
    # Whole-object equality first (frozen dataclasses compare structurally), then field-by-field for a
    # readable failure if anything drifts.
    assert spec == EXPECTED_SPEC, f"emitted spec != §2.5 golden:\n  got      {spec}\n  expected {EXPECTED_SPEC}"
    assert spec.builder_slug == "sos_core"
    assert spec.project == "proj-sos_core"
    assert spec.sa == "sa-sos_core"
    assert spec.apis == ("aiplatform", "gemini-embedding", "gemini-search")
    assert tuple((s.name, s.kind, s.acquisition, s.populated) for s in spec.secret_slots) == (
        ("GCP_SA_KEY_B64", "gcp_secret", "mint-via-gcp-console", False),
        ("POSTGRES_PASSWORD", "gcp_secret", "generate-locally", False),
        ("TS_AUTHKEY", "thirdparty_rest_key", "mint-via-thirdparty", False),
    )
    assert spec.railway_vars == ("DATABASE_URL",)
    assert spec.db_extensions == ("pgvector",)
    assert spec.sa_scope == tuple(derive_sa_scope(resolved))
    assert spec.needs_postgis_base_image is False
    assert spec.budget_boundary_required is True
    _ok("emitted ProvisioningSpec == §2.5 golden, every secret_slot populated=False (NAMES only)")
    return spec


def step4_value_free_spec(spec):
    """§2.6 step 4 — assert_value_free(spec) passes (no ValueLeakError)."""
    print("step 4 — assert_value_free(spec):")
    assert_value_free(spec)
    _ok("assert_value_free(spec) passed (no credential value anywhere — slot NAMES only)")


def step5_drive_mock(resolved, spec):
    """§2.6 step 5 — drive the spec against MockProvisioner. Default (unpopulated) => S2c BLOCKS; then
    populated => S3-S6 run (synthetic ids only, NO value held); assert_value_free on the RunLedger passes.
    """
    print("step 5 — drive against MockProvisioner (unpopulated -> S2c BLOCKS, then populated -> S3-S6 run):")
    slot_names = {s.name for s in spec.secret_slots}

    # (a) default mock: everything unpopulated -> S2c human-gate BLOCKS before S3/S5 (fail-closed).
    blocked_ledger = Choreographer(MockProvisioner()).run(resolved, SLUG)
    assert blocked_ledger.terminal == StepStatus.BLOCKED, (
        f"unpopulated mock did NOT block: terminal={blocked_ledger.terminal}")
    assert set(blocked_ledger.blocked_slots) == slot_names, (
        f"blocked_slots != the secret-slot NAMES: {sorted(blocked_ledger.blocked_slots)}")
    assert not any(a.step in ("S3", "S5") for a in blocked_ledger.actions), "S3/S5 ran past the S2c block"
    _ok(f"unpopulated MockProvisioner() -> terminal BLOCKED at S2c; blocked_slots == {sorted(slot_names)}; no S3/S5")
    assert_value_free(blocked_ledger)
    _ok("assert_value_free(blocked RunLedger) passed")

    # (b) populated mock: the three slot NAMES marked populated (value-free membership marker, NO value) ->
    #     S3-S6 run; the run completes OK; the RunLedger is value-free.
    populated_marker = frozenset({"GCP_SA_KEY_B64", "POSTGRES_PASSWORD", "TS_AUTHKEY"})
    assert_value_free(populated_marker)  # HW-1: the populated set is slot NAMES only, never a value channel
    ledger = Choreographer(MockProvisioner(populated=populated_marker)).run(resolved, SLUG)
    assert ledger.terminal == StepStatus.OK, f"populated run did NOT reach S6 OK: terminal={ledger.terminal}"
    steps_seen = {a.step for a in ledger.actions}
    assert {"S3", "S4", "S5", "S6"} <= steps_seen, f"S3-S6 did not all run: {sorted(steps_seen)}"
    indices = [int(a.step[1:]) for a in ledger.actions]
    assert indices == sorted(indices), f"step indices not monotonic: {indices}"
    _ok("populated MockProvisioner(...) -> terminal OK; S3-S6 all ran; step indices monotonic")
    assert_value_free(ledger)
    _ok("assert_value_free(populated RunLedger) passed (synthetic ids only, NO value held)")
    return ledger


def step6_mesh_shape():
    """§2.6 step 6 — stand_up_mesh_shape('sos_core'); assert the value-free MeshShape scaffold (drift D2:
    instance method on MockProvisioner)."""
    print("step 6 — MockProvisioner().stand_up_mesh_shape('sos_core') asserts the value-free MeshShape:")
    shape = MockProvisioner().stand_up_mesh_shape(SLUG)
    assert isinstance(shape, MeshShape)
    assert shape.builder_slug == "sos_core"
    assert shape.socket_mode == "0600"
    assert shape.transport == "af_unix"
    assert shape.identity_header == "Tailscale-User-Login"
    assert shape.deny_by_default is True
    assert shape.funnel_off is True
    assert shape.verb_placeholder == "<VERB>"
    assert "<VERB>" in shape.routes
    assert "health" in shape.routes
    _ok("MeshShape: socket_mode 0600 / af_unix / Tailscale-User-Login / deny_by_default / funnel_off / <VERB>")
    assert_value_free(shape)
    _ok("assert_value_free(MeshShape) passed (value-free 501-until-T3 scaffold)")
    return shape


def main() -> int:
    print("=" * 88)
    print("DC3 mock-emit demonstration — sos_core secure pass-through (stoa--q7f, design-rev2 §2)")
    print("EMIT-ONLY / value-free / mock — ZERO real infra, creds, network, or money.")
    print("=" * 88)
    catalog = step1_load_catalog()
    resolved = step2_build_resolved(catalog)
    spec = step3_emit_golden(resolved)
    step4_value_free_spec(spec)
    step5_drive_mock(resolved, spec)
    step6_mesh_shape()
    print("=" * 88)
    print("ALL §2.6 ASSERTIONS PASSED — the sos_core provisioning SHAPE emits value-free against the mock.")
    print("=" * 88)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

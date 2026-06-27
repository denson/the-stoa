# author: Denson Smith
# ticket: stoa--k48 (u--9s2 Phase-2 increment 2.3 — provisioning choreography)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--k48/design-rev2.md §8 (the full test inventory) /
#                       §5 (the 3-wall TRIPWIRE) / §12.B (threat-anchored probes) / §15 (ARGUS closures)
#
# The bespoke provision probes (ADA's fixtures = VERA's re-executable probes). Every test maps to a DoD
# 1-10 line. Provisions NOTHING (mock/dry-run/plan-text only). The W1/W2/W3 walls + the M3 threat-anchored
# probe + the strict §7 boundary probe are all encoded here. conftest's data_tables + load_manifest_fixture
# are REUSED.

from __future__ import annotations

import ast
import inspect
import subprocess  # TEST-ONLY: the §8.6 W1 grep-clean guard shells out to grep over provision/. This is
                   # a TEST file, NOT under provision/ — the W1 grep scans provision/ ONLY, so importing
                   # subprocess HERE is permitted (the wall is about the package, not its tests).
from pathlib import Path

import pytest

from builder_deploy_core import dataload
import builder_deploy_core.resolution  # noqa: F401 — import populates the §3.3 kind-tables
from builder_deploy_core.resolution.resolve import (
    check_runtime_completeness,
    derive_sa_scope,
    resolve,
)
from builder_deploy_core.provision import (
    Choreographer,
    MockProvisioner,
    Provisioner,
    StepStatus,
    ValueLeakError,
    assert_value_free,
    emit_spec,
    render_checklist,
    render_credential_attestation,
    render_tripwire_attestation,
    w1_forbidden_tokens,
)
from builder_deploy_core.provision import port as _port_mod
from builder_deploy_core.provision.spec import SlotSpec
from conftest import load_manifest_fixture

POSITIVE = ["prospector", "scienceclaw", "labstat_bls"]

_PROVISION_DIR = Path(_port_mod.__file__).resolve().parent  # builder_deploy_core/provision/


def _resolve_example(name, data_tables):
    manifest, _meta = load_manifest_fixture(name)
    return resolve(manifest, data_tables["baseline"], data_tables["library"])


def _run_mock(resolved, slug, populated=None, fail_at=None):
    pop = frozenset(populated) if populated is not None else frozenset()
    return Choreographer(MockProvisioner(populated=pop, fail_at=fail_at)).run(resolved, slug)


# ===========================================================================
# §8.1 — Golden-file emit fixtures (DoD#1: end-to-end emit, byte-stable)
# The §8 resolved sets (8/6/7) are the LOCKED regression target.
# ===========================================================================
def test_emit_prospector_golden(data_tables):
    resolved = _resolve_example("prospector", data_tables)
    spec = emit_spec(resolved, "prospector")
    assert spec.builder_slug == "prospector"
    assert spec.project == "proj-prospector"
    assert spec.sa == "sa-prospector"
    assert spec.apis == ("gemini-embedding", "gemini-search", "google-maps")
    assert tuple((s.name, s.kind, s.acquisition) for s in spec.secret_slots) == (
        ("MAPS_API_KEY", "gcp_secret", "mint-via-gcp-console"),
        ("POSTGRES_PASSWORD", "gcp_secret", "generate-locally"),
    )
    assert spec.railway_vars == ("DATABASE_URL",)
    assert spec.db_extensions == ("pgvector", "postgis")
    assert spec.needs_postgis_base_image is True
    assert spec.sa_scope == tuple(derive_sa_scope(resolved))
    assert spec.budget_boundary_required is True


def test_emit_scienceclaw_golden(data_tables):
    resolved = _resolve_example("scienceclaw", data_tables)
    spec = emit_spec(resolved, "scienceclaw")
    assert spec.apis == ("document-parsing", "gemini-embedding", "gemini-search")
    assert tuple(s.name for s in spec.secret_slots) == ("POSTGRES_PASSWORD",)
    assert spec.db_extensions == ("pgvector",)
    assert spec.needs_postgis_base_image is False
    assert spec.sa_scope == tuple(derive_sa_scope(resolved))


def test_emit_labstat_bls_golden(data_tables):
    resolved = _resolve_example("labstat_bls", data_tables)
    spec = emit_spec(resolved, "labstat_bls")
    # BLS_OEWS_API_KEY is a thirdparty_rest_key secret slot, NOT an api (the labstat proof into emit).
    assert "BLS_OEWS_API_KEY" not in spec.apis
    assert spec.apis == ("document-parsing", "gemini-embedding", "gemini-search")
    slot_names = {s.name: s for s in spec.secret_slots}
    assert "BLS_OEWS_API_KEY" in slot_names
    assert slot_names["BLS_OEWS_API_KEY"].kind == "thirdparty_rest_key"
    assert slot_names["BLS_OEWS_API_KEY"].acquisition == "mint-via-thirdparty"
    assert spec.needs_postgis_base_image is False


def test_emit_is_deterministic(data_tables):
    """Same input -> byte-identical spec (frozen dataclass equality over sorted tuples)."""
    resolved = _resolve_example("prospector", data_tables)
    assert emit_spec(resolved, "prospector") == emit_spec(resolved, "prospector")


# ===========================================================================
# §8.2 — Ordered / idempotent / fail-closed (DoD#2)
# ===========================================================================
def _all_populated(spec):
    return frozenset(s.name for s in spec.secret_slots)


def test_ledger_step_indices_monotonic(data_tables):
    resolved = _resolve_example("prospector", data_tables)
    spec = emit_spec(resolved, "prospector")
    ledger = _run_mock(resolved, "prospector", populated=_all_populated(spec))
    assert ledger.terminal == StepStatus.OK
    indices = [int(a.step[1:]) for a in ledger.actions]
    assert indices == sorted(indices), f"step indices not monotonic: {indices}"
    # S0 (ensure_sa) precedes the first S2 (ensure_secret_slot); S5 follows any S2/S3.
    first_s2 = next(i for i, a in enumerate(ledger.actions) if a.step == "S2")
    ensure_sa_idx = next(i for i, a in enumerate(ledger.actions) if a.op == "ensure_sa")
    assert ensure_sa_idx < first_s2
    s5_idx = next(i for i, a in enumerate(ledger.actions) if a.step == "S5")
    last_s3 = max(i for i, a in enumerate(ledger.actions) if a.step == "S3")
    assert s5_idx > last_s3


def test_idempotent_rerun_no_widen(data_tables):
    """BIDIRECTIONAL idempotency probe (c2 — the regression guard for c1). Two runs against the same mock
    state assert BOTH directions of create-or-get: the FIRST run reports created=True for EVERY
    create-or-get verb (incl provision_db_service/provision_serving_service — the exact c1 surface), AND
    the SECOND run adds ZERO new create-actions (all SKIPPED). The pre-c1-fix bug only widened the
    no-widen (second-run) direction's slack, so this test MUST fail before the c1 fix and pass after."""
    resolved = _resolve_example("prospector", data_tables)
    spec = emit_spec(resolved, "prospector")
    mock = MockProvisioner(populated=_all_populated(spec))
    choreo = Choreographer(mock)
    first = choreo.run(resolved, "prospector")
    second = choreo.run(resolved, "prospector")
    assert first.terminal == StepStatus.OK and second.terminal == StepStatus.OK

    # S0 budget + S4 select_base_image + S5/S6 are fixed-emit (created=True by design, not create-or-get
    # idempotent ids); the create-or-get verbs (project/sa/api/secret/db/var/ext) are the idempotent set.
    create_or_get_ops = {
        "ensure_project", "ensure_sa", "enable_api", "grant_api_role", "ensure_secret_slot",
        "grant_secret_accessor", "provision_db_service", "provision_serving_service",
        "set_railway_var", "apply_db_extension",
    }

    # (a) ADD direction (c1 guard): on the FIRST run EVERY create-or-get verb reports created=True /
    #     status OK — an INITIAL provision must record the create, not SKIP it.
    first_create_or_get = [a for a in first.actions if a.op in create_or_get_ops]
    assert first_create_or_get, "no create-or-get actions emitted on the first run"
    first_not_created = [a for a in first_create_or_get
                         if not (a.created and a.status == StepStatus.OK)]
    assert first_not_created == [], (
        f"first-run create-or-get verbs NOT created=True: "
        f"{[(a.op, a.target, a.created, a.status) for a in first_not_created]}")
    # the exact c1 surface is asserted explicitly: the S3 db + serving services create on the first run.
    first_ops = {a.op for a in first_create_or_get if a.created and a.status == StepStatus.OK}
    assert "provision_db_service" in first_ops
    assert "provision_serving_service" in first_ops

    # (b) NO-WIDEN direction: the SECOND run creates nothing new (every create-or-get verb SKIPPED).
    rerun_widened = [a for a in second.actions if a.op in create_or_get_ops and a.created]
    assert rerun_widened == [], f"idempotent rerun widened: {[(a.op, a.target) for a in rerun_widened]}"


def test_s2c_blocks_unpopulated(data_tables):
    """NEGATIVE — default mock (unpopulated): run halts at S2c; terminal BLOCKED; every secret slot named;
    NO S3/S5 action present."""
    resolved = _resolve_example("prospector", data_tables)
    spec = emit_spec(resolved, "prospector")
    ledger = _run_mock(resolved, "prospector")  # default: nothing populated
    assert ledger.terminal == StepStatus.BLOCKED
    assert set(ledger.blocked_slots) == {s.name for s in spec.secret_slots}
    assert not any(a.step in ("S3", "S5") for a in ledger.actions)


def test_s0_abort_no_key_materialized(data_tables):
    """NEGATIVE — fail at S0:ensure_sa: ledger has the failed S0 action, terminal FAILED, and ZERO S2
    actions (no key materialized before the per-builder lock)."""
    resolved = _resolve_example("prospector", data_tables)
    spec = emit_spec(resolved, "prospector")
    ledger = _run_mock(resolved, "prospector", populated=_all_populated(spec), fail_at="S0:ensure_sa")
    assert ledger.terminal == StepStatus.FAILED
    assert not any(a.step == "S2" for a in ledger.actions)
    assert any(a.status == StepStatus.FAILED for a in ledger.actions)


# ===========================================================================
# §8.3 — value-free emit (DoD#3 / HW-1)
# ===========================================================================
@pytest.mark.parametrize("name", POSITIVE)
def test_emit_value_free(name, data_tables):
    spec = emit_spec(_resolve_example(name, data_tables), name)
    assert_value_free(spec)  # raises ValueLeakError on any non-name/ref/bool/enum leaf


def test_ledger_value_free(data_tables):
    resolved = _resolve_example("prospector", data_tables)
    spec = emit_spec(resolved, "prospector")
    ledger = _run_mock(resolved, "prospector", populated=_all_populated(spec))
    assert_value_free(ledger)


def test_mock_populated_is_value_free(data_tables):
    """HW-1: every member of a MockProvisioner(populated=...) set is a known slot NAME (the mock cannot
    become a value channel)."""
    resolved = _resolve_example("prospector", data_tables)
    spec = emit_spec(resolved, "prospector")
    populated = _all_populated(spec)
    assert_value_free(populated)  # walks the set; each member must be a name string
    assert populated == {s.name for s in spec.secret_slots}


def test_assert_value_free_raises_on_injected_value():
    """A SlotSpec carrying a non-name leaf (a fake value object) trips assert_value_free."""
    bad = SlotSpec(name="MAPS_API_KEY", kind="gcp_secret", acquisition="mint-via-gcp-console")
    object.__setattr__(bad, "name", 12345)  # inject a non-string value leaf (frozen dataclass bypass)
    with pytest.raises(ValueLeakError):
        assert_value_free(bad)


# ===========================================================================
# §8.4 — per-builder isolation (DoD#4)
# ===========================================================================
def test_isolation_bijective_sa(data_tables):
    resolved = _resolve_example("prospector", data_tables)
    spec = emit_spec(resolved, "prospector")
    ledger = _run_mock(resolved, "prospector", populated=_all_populated(spec))
    assert sum(1 for a in ledger.actions if a.op == "ensure_project") == 1
    assert sum(1 for a in ledger.actions if a.op == "ensure_sa") == 1
    assert spec.sa == "sa-prospector"


def test_isolation_per_secret_accessor(data_tables):
    """M1 attack-blocked: every grant_secret_accessor names exactly ONE secret, never a project wildcard."""
    resolved = _resolve_example("prospector", data_tables)
    spec = emit_spec(resolved, "prospector")
    ledger = _run_mock(resolved, "prospector", populated=_all_populated(spec))
    grants = [a for a in ledger.actions if a.op == "grant_secret_accessor"]
    assert grants, "no grant_secret_accessor action emitted"
    for g in grants:
        keys = dict(g.detail)
        assert "secret" in keys and keys["secret"] == g.target
        assert "*" not in keys["secret"] and "project" not in keys  # no project-wide wildcard
    # M1 legit-unaffected: the builder's OWN resolved secrets DO each get an accessor.
    assert {g.target for g in grants} == {s.name for s in spec.secret_slots}


def test_sa_scope_is_derive_sa_scope(data_tables):
    """emit does NOT re-derive the union — it calls the FROZEN derive_sa_scope."""
    resolved = _resolve_example("prospector", data_tables)
    spec = emit_spec(resolved, "prospector")
    assert spec.sa_scope == tuple(derive_sa_scope(resolved))


def test_budget_boundary_present(data_tables):
    resolved = _resolve_example("prospector", data_tables)
    spec = emit_spec(resolved, "prospector")
    ledger = _run_mock(resolved, "prospector", populated=_all_populated(spec))
    assert any(a.op == "set_budget_boundary" for a in ledger.actions)
    assert spec.budget_boundary_required is True


# ===========================================================================
# §8.5 — SHAPE stands up, domain-empty + THE STRICT §7 BOUNDARY PROBE (DoD#5)
# ===========================================================================
def test_s5_shape_stands_up(data_tables):
    resolved = _resolve_example("prospector", data_tables)
    spec = emit_spec(resolved, "prospector")
    ledger = _run_mock(resolved, "prospector", populated=_all_populated(spec))
    assert any(a.op == "stand_up_mesh_shape" for a in ledger.actions)
    shape = MockProvisioner().stand_up_mesh_shape("prospector")
    assert shape.socket_mode == "0600"
    assert shape.transport == "af_unix"
    assert shape.identity_header == "Tailscale-User-Login"
    assert shape.deny_by_default is True
    assert shape.operators_env == "<BUILDER>_OPERATORS"
    assert shape.funnel_off is True
    assert "health" in shape.routes
    assert shape.verb_placeholder == "<VERB>"


def test_s7_boundary_no_domain_verb_leak(data_tables):
    """THE STRICT CANONICAL PROBE (CHIRON co-confirmed; ARGUS RQ-2 KEEP-STRICT). grep the ENTIRE T1
    SCAFFOLD/TEMPLATE surface (the reusable, builder-agnostic scaffold text + the CLI-client template +
    routes + policy descriptors) for ANY domain route/verb token or builder name. The ONLY concrete route
    allowed in T1 is health. /run IS ON THE LEAK LIST. The builder's own identity field (builder_slug) is
    NOT part of the reusable template surface and is excluded — the leak the probe guards is a domain verb
    or builder NAME baked into the GENERIC template."""
    LEAK_TOKENS = ["/run", "collect", "embed", "ingest", "search",
                   "newswire", "scienceclaw", "prospector"]
    shape = MockProvisioner().stand_up_mesh_shape("prospector")
    # the reusable template surface (excludes builder_slug, which is the builder's own value-free identity)
    surface = (
        shape.client_template
        + " " + " ".join(shape.routes)
        + " " + shape.verb_placeholder
        + " " + shape.identity_header
        + " " + shape.operators_env
        + " " + shape.operators_group
        + " " + shape.transport
        + " " + shape.socket_mode
    )
    hits = [t for t in LEAK_TOKENS if t in surface]
    assert hits == [], f"domain-verb / builder-name leak in the T1 template surface: {hits}"
    # the only concrete route is health; the domain endpoint is the placeholder.
    assert "health" in shape.routes
    assert "<VERB>" in shape.routes


# ===========================================================================
# §8.6 — TRIPWIRE held (DoD#6): the 3 §5 walls + the grep + the r1 grep-clean guard
# ===========================================================================
_PROVISION_MODULES = sorted(p for p in _PROVISION_DIR.glob("*.py"))
_W1_ALLOWED = {"builder_deploy_core", "dataclasses", "enum", "typing", "abc", "__future__"}


def _top_level_imports(py_path: Path):
    """Return the set of top-level module roots imported by py_path (via AST, not string scan)."""
    tree = ast.parse(py_path.read_text(encoding="utf-8"))
    roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.level == 0:
                roots.add(node.module.split(".")[0])
    return roots


def test_tripwire_no_infra_imports():
    """W1 (AST, authoritative): every module under provision/ imports ONLY the allowed roots. sys is
    whitelisted for __main__.py ONLY. The forbidden set is tripwire.w1_forbidden_tokens() (shared SSoT)."""
    forbidden = set(w1_forbidden_tokens())
    for py in _PROVISION_MODULES:
        allowed = set(_W1_ALLOWED)
        if py.name == "__main__.py":
            allowed.add("sys")
        roots = _top_level_imports(py)
        leaked = roots - allowed
        assert not (leaked & forbidden), f"{py.name}: forbidden-I/O import: {leaked & forbidden}"
        assert leaked == set(), f"{py.name}: unexpected import root(s): {leaked}"


def test_tripwire_only_mock_port():
    """W2: only MockProvisioner subclasses Provisioner; Choreographer(None) raises; the mock is
    instantiable (every @abstractmethod incl select_base_image implemented — r3-corroborant)."""
    assert Provisioner.__subclasses__() == [MockProvisioner]
    with pytest.raises(TypeError):
        Choreographer(None)
    MockProvisioner()  # must not raise (all abstract methods implemented)


def test_tripwire_emit_is_pure():
    """W3: emit_spec takes no provisioner parameter (pure transform)."""
    params = list(inspect.signature(emit_spec).parameters)
    assert params == ["resolved", "builder_slug"], params
    assert "provisioner" not in params


def test_w1_attestation_grep_clean():
    """r1 closure (§15.1 / §8.6): the §5 W1 grep run over the WHOLE provision/ tree (checklist.py +
    tripwire.py INCLUDED) returns EMPTY. This is the machine-check that grep and the AST test AGREE. A
    future edit re-introducing the joined literal goes RED here, not just at VERA's manual grep."""
    pattern = r"\b(subprocess|socket|urllib|requests|httpx|gcloud|railway|os\.system|popen)\b"
    # grep over .py SOURCE only (the canonical VERA grep scans source; __pycache__ is a transient
    # build artifact, not source — exclude it so a stale .pyc cannot false-fire the source assertion).
    proc = subprocess.run(
        ["grep", "-rnE", "--include=*.py", pattern, str(_PROVISION_DIR)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 1, (
        f"W1 grep over provision/ source is NON-EMPTY (the joined literal re-appeared):\n{proc.stdout}")
    assert proc.stdout.strip() == ""


# ===========================================================================
# §8.7 — labstat kind-dispatch carried into the choreography (DoD#1 corroborant)
# ===========================================================================
def test_labstat_skips_s1_for_thirdparty(data_tables):
    """labstat_bls: BLS_OEWS_API_KEY appears as an S2 secret slot + an S3 var, NEVER in S1."""
    resolved = _resolve_example("labstat_bls", data_tables)
    spec = emit_spec(resolved, "labstat_bls")
    ledger = _run_mock(resolved, "labstat_bls", populated=_all_populated(spec))
    s1_targets = {a.target for a in ledger.actions if a.step == "S1"}
    assert "BLS_OEWS_API_KEY" not in s1_targets
    s2_secret_targets = {a.target for a in ledger.actions
                         if a.step == "S2" and a.op == "ensure_secret_slot"}
    assert "BLS_OEWS_API_KEY" in s2_secret_targets


# ===========================================================================
# §8.8 — the deploy-help plan dispatch (DoD#7-adjacent, §9)
# ===========================================================================
def test_deploy_help_plan_dispatch(data_tables):
    """Each secret slot's acquisition is the correct DERIVED method. The plan is EMITTED (in the spec),
    never executed."""
    expect = {
        "MAPS_API_KEY": "mint-via-gcp-console",
        "BLS_OEWS_API_KEY": "mint-via-thirdparty",
        "POSTGRES_PASSWORD": "generate-locally",
    }
    for name in POSITIVE:
        spec = emit_spec(_resolve_example(name, data_tables), name)
        for slot in spec.secret_slots:
            assert slot.acquisition == expect[slot.name], (name, slot.name, slot.acquisition)


# ===========================================================================
# §8.9 — the relay-up generators (DoD#10)
# ===========================================================================
def test_render_checklist_is_pure_transform(data_tables):
    spec = emit_spec(_resolve_example("prospector", data_tables), "prospector")
    out1 = render_checklist(spec)
    out2 = render_checklist(spec)
    assert out1 == out2  # deterministic
    # names every secret slot needing human population at S2c, by acquisition method.
    for slot in spec.secret_slots:
        assert slot.name in out1
        assert slot.acquisition in out1


def test_render_credential_attestation(data_tables):
    spec = emit_spec(_resolve_example("prospector", data_tables), "prospector")
    out = render_credential_attestation(spec)
    assert "VALUE-FREE EMIT" in out
    assert "NO AGENT HOLDS A VALUE" in out
    assert "KEYRING" in out.upper() or "WIF" in out
    assert "HARD CAP" in out.upper()
    assert spec.builder_slug in out


def test_render_tripwire_attestation():
    """The attestation cites W1/W2/W3; it cites the wall STRUCTURALLY via the fragment-built token set.
    Adding this generator did NOT re-introduce a joined literal in SOURCE (the r1 regression guard at the
    generator's own source — checked by test_w1_attestation_grep_clean over the whole tree)."""
    out = render_tripwire_attestation()
    assert "W1" in out and "W2" in out and "W3" in out
    assert "w1_forbidden_tokens()" in out  # cites the SSoT by reference
    # the runtime TEXT may list the tokens joined (that is stdout, not source).
    for tok in w1_forbidden_tokens():
        assert tok in out


# ===========================================================================
# §8.12 — M3 runtime-completeness — THE THREAT-ANCHORED PROBE (r2 closure)
# GROUND-CHECK NOTE: the FROZEN check_runtime_completeness returns missing as
#   list[((api_kind, api_name), (secret_kind, secret_name))] — each ident is a (kind,name) TUPLE,
#   NOT a bare name (design-rev2 §8.12 wrote it against bare names). Shipped code is canon; the probe
#   asserts the ACTUAL element shape.
# ===========================================================================
def test_m3_runtime_completeness_drops_paired_secret(data_tables):
    complete = _resolve_example("prospector", data_tables)  # google-maps + MAPS_API_KEY both present
    attack = [e for e in complete if e != ("gcp_secret", "MAPS_API_KEY")]  # paired secret DROPPED

    # (a) attack-blocked
    ok, missing = check_runtime_completeness(attack)  # FROZEN call
    assert ok is False
    assert (("gcp_api", "google-maps"), ("gcp_secret", "MAPS_API_KEY")) in missing

    # (b) legit-unaffected
    ok2, missing2 = check_runtime_completeness(complete)  # FROZEN call, complete set
    assert ok2 is True
    assert missing2 == []


def test_s6_records_runtime_completeness(data_tables):
    """The in-choreography read of the same M3 invariant: S6 calls the FROZEN check_runtime_completeness
    and records a value-free verify action. For the complete prospector set it records runtime_completeness=ok."""
    resolved = _resolve_example("prospector", data_tables)
    spec = emit_spec(resolved, "prospector")
    ledger = _run_mock(resolved, "prospector", populated=_all_populated(spec))
    s6_details = [dict(a.detail) for a in ledger.actions if a.step == "S6"]
    assert any(d.get("runtime_completeness") == "ok" for d in s6_details)

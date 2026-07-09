# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: design-rev4 §3.1 (fail-CLOSED seal-audit; constrained synthetic exemption =
#                       path-bound AND shape-clean) + §5.2 P-M7 EXTENDED. Threat M7: secret-value leakage.
#
# P-M7: (a.1) UNMARKED real-shaped value in a TOML + a log -> build REFUSES (names the path). (a.2 NEW r2)
# a MARKED real-shaped value in fixtures + a MARKED value OUTSIDE fixtures -> build STILL FAILS (the marker
# cannot launder a real shape; a mis-placed marker fails). (b) slot NAMES only + shape-clean marked fixtures
# IN the fixtures path -> build PASSES. Plus the real-build seal-audit over the actual service tree.
#
# All planted (attack) secrets are written to tmp_path — NEVER into the committed tree — so the committed
# tree stays clean and the real-build seal-audit passes.

from __future__ import annotations

from pathlib import Path

import pytest

from secure_core.sealaudit import seal_audit, scan_findings, FIXTURES_SEGMENT, SYNTHETIC_MARKER
from secure_core.errors import SealAuditError

# Real-SHAPED secret VALUES (fake but shape-matching — never real secrets).
REAL_TSKEY = "tskey-auth-kX9fB2cD3eF4gH5jK6mN7pQ8rS9tU0vW1xY"
REAL_B64_BLOB = "A" * 130  # a base64-charset blob above the length floor (SA-key-shaped)


# ---- (a.1) UNMARKED real-shaped value -> build REFUSES -------------------------------------------
def test_pm7_a1_unmarked_tskey_in_toml_fails(tmp_path):
    toml = tmp_path / "vertex-gemini.toml"
    toml.write_text(f'service-id = "vertex-gemini"\nTS_AUTHKEY = "{REAL_TSKEY}"\n', encoding="utf-8")
    with pytest.raises(SealAuditError) as exc:
        seal_audit([str(toml)])
    assert any(f.path == str(toml) for f in exc.value.findings)


def test_pm7_a1_unmarked_sa_key_blob_in_log_fails():
    with pytest.raises(SealAuditError):
        seal_audit([], emitted_logs=[f'{{"phase":"intent","note":"{REAL_B64_BLOB}"}}'])


# ---- (a.2 NEW r2) marked real-shaped / mis-placed -> STILL FAILS ---------------------------------
def test_pm7_a2_marked_real_shaped_in_fixtures_still_fails(tmp_path):
    """A real-SHAPED value carrying the marker, INSIDE the designated fixtures path, STILL FAILS — the
    marker cannot launder a real shape (shape test on the demarked body)."""
    fixtures = tmp_path / "tests" / "fixtures" / "seal_audit"
    fixtures.mkdir(parents=True)
    f = fixtures / "planted.txt"
    f.write_text(f"{SYNTHETIC_MARKER}{REAL_TSKEY}\n", encoding="utf-8")
    # path-bound is satisfied (the FIXTURES_SEGMENT is in the path), yet it must FAIL on the real shape.
    assert FIXTURES_SEGMENT in str(f).replace("\\", "/")
    with pytest.raises(SealAuditError) as exc:
        seal_audit([str(f)], fixtures_dir=fixtures)
    kinds = {fnd.kind for fnd in exc.value.findings}
    assert any("marked_real_shape" in k for k in kinds), kinds


def test_pm7_a2_marked_shapeclean_outside_fixtures_still_fails(tmp_path):
    """A properly-marked, shape-clean value placed OUTSIDE the fixtures path STILL FAILS (mis-placed)."""
    toml = tmp_path / "config.toml"  # NOT under a seal_audit fixtures path
    toml.write_text(f"note = {SYNTHETIC_MARKER}obviously_fake_but_misplaced\n", encoding="utf-8")
    with pytest.raises(SealAuditError) as exc:
        seal_audit([str(toml)])
    assert any(f.kind == "marked_out_of_path" for f in exc.value.findings)


def test_pm7_a2_marker_is_not_an_unconditional_pass_token():
    """Direct assertion the marker is necessary-but-not-sufficient: a marked real-shaped body in a LOG (never
    path-bound) fails on BOTH counts."""
    findings = scan_findings([], emitted_logs=[f"{SYNTHETIC_MARKER}{REAL_TSKEY}"])
    assert findings, "a marked real-shaped value in a log must NOT pass"


# ---- fail-CLOSED on ambiguous high-entropy -------------------------------------------------------
def test_pm7_ambiguous_high_entropy_fails_closed():
    """An unclassified high-entropy blob (not a recognized sha256 digest) FAILS closed."""
    with pytest.raises(SealAuditError):
        seal_audit([], emitted_logs=["x" + "b" * 140])  # 140-char run, not a 64-hex digest


def test_pm7_sha256_digest_is_recognized_safe():
    """A value-free sha256 params_digest (exactly 64 hex) is recognized SAFE — the audit does not false-
    positive on legitimate digests."""
    digest = "a" * 64
    seal_audit([], emitted_logs=[f'{{"params_digest":"{digest}"}}'])  # no raise


# ---- (b) legit: slot NAMES + shape-clean marked fixtures IN the path -> PASSES --------------------
def test_pm7_b_slot_names_and_clean_marked_fixtures_pass(tmp_path):
    # a TOML with slot NAMES only (documented placeholders — a name is not a value)
    toml = tmp_path / "vertex-gemini.toml"
    toml.write_text(
        'service-id = "vertex-gemini"\n'
        'config_keys = ["GCP_SA_KEY_B64", "TS_AUTHKEY"]\n'
        'TS_AUTHKEY = "${TS_AUTHKEY}"\n',  # a slot reference, not a value
        encoding="utf-8",
    )
    # a shape-clean marked fixture INSIDE the designated fixtures path
    fixtures = tmp_path / "tests" / "fixtures" / "seal_audit"
    fixtures.mkdir(parents=True)
    fx = fixtures / "ok.txt"
    fx.write_text(f"{SYNTHETIC_MARKER}obviously_fake_shape_clean_body\n", encoding="utf-8")
    # PASSES (no raise) — the gate did not break a clean build.
    seal_audit([str(toml), str(fx)], emitted_logs=['{"phase":"intent","lane":"lane:science"}'],
               fixtures_dir=fixtures)


# ---- the REAL-BUILD seal-audit: the actual service tree + catalog TOMLs must PASS -----------------
def test_pm7_real_service_tree_and_catalog_pass():
    """The build-completion seal-audit: scan the REAL secure_core source + the two DC3 catalog TOMLs + the
    committed fixtures + a real emitted audit log — all must PASS (no secret VALUE anywhere; slot NAMES
    only)."""
    import secure_core
    pkg_dir = Path(secure_core.__file__).resolve().parent
    tree = [str(p) for p in pkg_dir.glob("*.py")]

    # the two reproduced DC3 catalog TOMLs (the seal-audit scans them per design §3.1)
    worktree = pkg_dir.parents[2]  # .../arc-77-build
    catalog = worktree / "agents" / "builder-deploy-core" / "builder_deploy_core" / "data" / "catalog"
    tree += [str(catalog / "vertex-gemini.toml"), str(catalog / "tailscale.toml")]

    # the committed designated fixtures file (path-bound + shape-clean marked -> exempt)
    committed_fixture = Path(__file__).resolve().parent / "fixtures" / "seal_audit" / "synthetic_ok.txt"
    tree.append(str(committed_fixture))
    assert FIXTURES_SEGMENT in str(committed_fixture).replace("\\", "/")

    # a real emitted audit log (value-free)
    from secure_core.audit import AuditLog
    from secure_core.handler import handle_call
    from secure_core.registry import load_registry
    from conftest import science_headers, legit_recorder, OPERATOR_LOGIN
    audit = AuditLog()
    core = load_registry(operators=[OPERATOR_LOGIN])
    handle_call(core, science_headers(),
                {"provider": "vertex", "operation": "generate_grounded", "skill_id": "gsearch",
                 "params": {"contents": []}},
                egress_fn=legit_recorder(), audit=audit)

    findings = scan_findings(tree, emitted_logs=audit.as_log_lines())
    assert findings == [], f"real-build seal-audit found secret shapes (should be clean): {findings}"

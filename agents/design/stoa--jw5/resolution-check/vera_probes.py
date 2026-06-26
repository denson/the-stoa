# author: Denson Smith
# ticket: stoa--jw5 (u--9s2 Phase-1)
# seat-built-by: CAPTAIN_VERA_the_stoa (VERIFIER) — INDEPENDENT verification, does NOT trust ADA's code
# design-ground-truth: agents/design/stoa--jw5/design-formal.md §2.5/§2.6/§3.1/§3.2/§3.4/§5.A/§12.A
#
# Two jobs:
#  (1) INDEPENDENT re-implementation of resolve() from the §2.5 SPEC (NOT importing ADA's resolve()),
#      cross-checked against the §8 expected sets + a hand-derived (kind,name) set for §8.1.
#      If ADA's resolve() and VERA's independent resolve() ever disagree on a fixture, FALSIFY.
#  (2) THREAT-COVERAGE probes that DRIVE the specific M1-M4/M6 attack-paths (NOT happy-path proxies),
#      per the FM close-gate. Each probe drives the attack and asserts it is defeated.
#
# Pure logic. Provisions nothing. Reads no environment. Run: python vera_probes.py  (exit 0 = all held).

from __future__ import annotations

import sys

# Import ADA's MODULE under test (the thing being verified) + its data records.
from resolve import (
    BASELINE as ADA_BASELINE,
    LIBRARY as ADA_LIBRARY,
    BaselineOmitError,
    ResolutionError,
    check_runtime_completeness,
    derive_sa_scope,
    resolve as ada_resolve,
)
from fixtures import (
    PROSPECTOR_MANIFEST, PROSPECTOR_EXPECTED,
    SCIENCECLAW_MANIFEST, SCIENCECLAW_EXPECTED,
    LABSTAT_BLS_MANIFEST, LABSTAT_BLS_EXPECTED,
)

failures = []


def check(label, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    line = f"  [{status}] {label}"
    if detail:
        line += f" — {detail}"
    print(line)
    if not cond:
        failures.append(label)
    return cond


# ===========================================================================
# PART 1 — VERA's INDEPENDENT resolve() (re-derived from §2.5 spec text, NOT
# copied from resolve.py). Different code path; if it agrees with ADA's on the
# fixtures the resolution rule is corroborated by two independent implementations.
# ===========================================================================

class VeraBaselineOmit(Exception):
    pass


def vera_resolve(manifest, baseline, library):
    """Independent §2.5 implementation. Same spec, different code.
    Steps (verbatim §2.3): GUARD omit∩baseline -> raise; S=BASELINE∪CATEGORY;
    S\\omit; S∪add; sorted."""
    cat = manifest["category"]
    if cat not in library:
        raise ResolutionError(f"unknown category {cat}")
    delta = manifest.get("delta") or {}
    add_list = delta.get("add") or []
    omit_list = delta.get("omit") or []
    # build tuples a different way (list comprehensions over dict items) than ADA
    baseline_pairs = frozenset((d["kind"], d["name"]) for d in baseline)
    omit_pairs = frozenset((d["kind"], d["name"]) for d in omit_list)
    add_pairs = frozenset((d["kind"], d["name"]) for d in add_list)
    # GUARD (step 0) — omit may not touch baseline
    bad = omit_pairs & baseline_pairs
    if bad:
        raise VeraBaselineOmit(f"illegal baseline omit: {sorted(bad)}")
    cat_pairs = frozenset((d["kind"], d["name"]) for d in library[cat])
    acc = (baseline_pairs | cat_pairs) - omit_pairs  # union then subtract
    acc = acc | add_pairs                              # add last (add-wins)
    return sorted(acc)


def part1_independent_resolution():
    print("\n=== PART 1 — INDEPENDENT re-implementation + hand-derivation ===")

    # (a) VERA's independent resolve agrees with the §8 expected sets (two-impl convergence)
    for label, man, exp in [
        ("§8.1 prospector", PROSPECTOR_MANIFEST, PROSPECTOR_EXPECTED),
        ("§8.2 scienceclaw", SCIENCECLAW_MANIFEST, SCIENCECLAW_EXPECTED),
        ("§8.3 labstat_bls", LABSTAT_BLS_MANIFEST, LABSTAT_BLS_EXPECTED),
    ]:
        v = vera_resolve(man, ADA_BASELINE, ADA_LIBRARY)
        a = ada_resolve(man, ADA_BASELINE, ADA_LIBRARY)
        check(f"{label}: VERA-independent resolve == §8 expected ({len(v)})", v == exp,
              f"vera={v}" if v != exp else f"{len(v)} entries")
        check(f"{label}: VERA-independent == ADA resolve (two-impl agreement)", v == a,
              "" if v == a else f"vera={v}\n        ada={a}")

    # (b) HAND-DERIVED §8.1 prospector set, written out by hand from §2.5+§3.1+§3.2,
    #     NOT computed by either resolver. This is the by-hand cross-check the brief asks for.
    #   BASELINE (§3.1) = {(gcp_api,gemini-embedding),(gcp_api,gemini-search),
    #                      (railway_var,DATABASE_URL),(gcp_secret,POSTGRES_PASSWORD),
    #                      (db_extension,pgvector)}
    #   CATEGORY[geospatial] (§3.2) = {(gcp_api,google-maps),(gcp_secret,MAPS_API_KEY),
    #                                  (db_extension,postgis)}
    #   delta = {} -> no omit, no add. resolve = sorted(BASELINE ∪ CATEGORY) = 5+3 = 8.
    hand_prospector = sorted({
        ("gcp_api", "gemini-embedding"),
        ("gcp_api", "gemini-search"),
        ("railway_var", "DATABASE_URL"),
        ("gcp_secret", "POSTGRES_PASSWORD"),
        ("db_extension", "pgvector"),
        ("gcp_api", "google-maps"),
        ("gcp_secret", "MAPS_API_KEY"),
        ("db_extension", "postgis"),
    })
    a_prosp = ada_resolve(PROSPECTOR_MANIFEST, ADA_BASELINE, ADA_LIBRARY)
    check("§8.1 HAND-DERIVED set (8) == ADA resolve()", hand_prospector == a_prosp,
          "" if hand_prospector == a_prosp else f"hand={hand_prospector}\n        ada={a_prosp}")
    check("§8.1 HAND-DERIVED set == §8 expected", hand_prospector == PROSPECTOR_EXPECTED)


# ===========================================================================
# PART 2 — THREAT-COVERAGE probes (drive the SPECIFIC attack-paths, §12.A)
# ===========================================================================

def m4_baseline_omit_fail_closed():
    """M4 attack-path: a manifest delta.omits a baseline necessity -> silent drop -> fail-open.
    DRIVE: try to omit EACH of the 5 §2.6 baseline entries individually + an omit∩add same-entry
    case. Assert EVERY one raises BaselineOmitError (no silent partial set)."""
    print("\n=== M4 — baseline silently omitted / fail-open (drive ALL 5 baseline entries) ===")
    for kind, name in [(d["kind"], d["name"]) for d in ADA_BASELINE]:
        man = {"builder": "attack_omit", "category": "document-consuming",
               "delta": {"omit": [{"kind": kind, "name": name}]}}
        raised = False
        returned = None
        msg = ""
        try:
            returned = ada_resolve(man, ADA_BASELINE, ADA_LIBRARY)
        except BaselineOmitError as e:
            raised = True
            msg = str(e)
        check(f"M4: omit ({kind},{name}) RAISES BaselineOmitError, no set returned",
              raised and returned is None,
              f"names={name in msg}, returned={returned!r}")

    # omit∩add SAME entry on a baseline target: GUARD must still fire (fail-closed wins over add-wins).
    # Attack: author tries to 'omit pgvector but also re-add it' to sneak past the guard or to test
    # whether add-wins masks the illegal omit. Guard is step 0 (before add) -> MUST still raise.
    man = {"builder": "attack_omit_readd", "category": "document-consuming",
           "delta": {"omit": [{"kind": "db_extension", "name": "pgvector"}],
                     "add":  [{"kind": "db_extension", "name": "pgvector"}]}}
    raised = False
    returned = None
    try:
        returned = ada_resolve(man, ADA_BASELINE, ADA_LIBRARY)
    except BaselineOmitError:
        raised = True
    check("M4: omit∩add same baseline entry (pgvector) STILL raises (guard is step-0, fail-closed)",
          raised and returned is None, f"returned={returned!r}")

    # Control: omitting a CATEGORY-template (non-baseline) entry is LEGAL and must NOT raise
    # (proves the guard is scoped to baseline only, not a blanket omit-ban — falsify over-blocking).
    man = {"builder": "legal_omit_postgis", "category": "geospatial",
           "delta": {"omit": [{"kind": "db_extension", "name": "postgis"}]}}
    raised = False
    got = None
    try:
        got = ada_resolve(man, ADA_BASELINE, ADA_LIBRARY)
    except Exception:
        raised = True
    check("M4 control: omitting a CATEGORY entry (postgis) is LEGAL (no raise; postgis dropped)",
          (not raised) and got is not None and ("db_extension", "postgis") not in got,
          f"got={got}")


def m1_cross_builder_lateral():
    """M1 attack-path: builder A's SA reaches into builder B's secrets/scope (lateral movement).
    DRIVE: derive_sa_scope for 2 distinct builders; assert NO entry from B appears in A's scope,
    AND A's scope == exactly the scope-bearing subset of A's OWN resolved set (t0 initial-provision
    derivation per §5.A, which is qualified to initial provision)."""
    print("\n=== M1 — cross-builder lateral movement (prospector vs labstat_bls at t0) ===")
    a_resolved = ada_resolve(PROSPECTOR_MANIFEST, ADA_BASELINE, ADA_LIBRARY)
    b_resolved = ada_resolve(LABSTAT_BLS_MANIFEST, ADA_BASELINE, ADA_LIBRARY)
    a_scope = derive_sa_scope(a_resolved)
    b_scope = derive_sa_scope(b_resolved)

    SCOPE_BEARING = {"gcp_api", "gcp_secret", "thirdparty_rest_key"}
    a_own_scope_bearing = sorted((k, n) for (k, n) in a_resolved if k in SCOPE_BEARING)
    b_own_scope_bearing = sorted((k, n) for (k, n) in b_resolved if k in SCOPE_BEARING)

    # (1) A's scope is EXACTLY the scope-bearing subset of A's own resolved set (no widening)
    check("M1: prospector SA-scope == scope-bearing subset of ITS OWN resolved set (t0, no widen)",
          a_scope == a_own_scope_bearing, f"scope={a_scope}")
    check("M1: labstat_bls SA-scope == scope-bearing subset of ITS OWN resolved set (t0, no widen)",
          b_scope == b_own_scope_bearing, f"scope={b_scope}")

    # (2) The KEY isolation assertion: B's UNIQUE entry (BLS_OEWS_API_KEY) is NOT in A's scope,
    #     and A's UNIQUE entries (google-maps, MAPS_API_KEY) are NOT in B's scope. No lateral reach.
    b_unique = ("thirdparty_rest_key", "BLS_OEWS_API_KEY")
    a_unique = [("gcp_api", "google-maps"), ("gcp_secret", "MAPS_API_KEY")]
    check("M1: builder-B's unique secret (BLS_OEWS_API_KEY) ABSENT from builder-A's SA scope",
          b_unique not in a_scope, f"A_scope={a_scope}")
    check("M1: builder-A's unique entries (google-maps/MAPS_API_KEY) ABSENT from builder-B's SA scope",
          all(e not in b_scope for e in a_unique), f"B_scope={b_scope}")

    # (3) General: no entry in A's scope that isn't in A's own resolved set (no foreign entry at all)
    a_set, b_set = set(a_resolved), set(b_resolved)
    check("M1: every entry in A's scope is a member of A's OWN resolved set (no foreign entry)",
          all(e in a_set for e in a_scope))
    check("M1: every entry in B's scope is a member of B's OWN resolved set (no foreign entry)",
          all(e in b_set for e in b_scope))

    # (4) Symmetric-difference sanity: A_scope ∩ B_scope is only the SHARED baseline scope-bearing
    #     entries (gemini-embedding/search, POSTGRES_PASSWORD) — never a builder-specific one.
    shared = set(a_scope) & set(b_scope)
    expected_shared = {("gcp_api", "gemini-embedding"), ("gcp_api", "gemini-search"),
                       ("gcp_secret", "POSTGRES_PASSWORD")}
    check("M1: A∩B scope overlap is EXACTLY the shared baseline scope-bearing set (no builder-specific leak)",
          shared == expected_shared, f"overlap={sorted(shared)}")


def m3_keyless_maps_caught():
    """M3 attack-path: a key-bearing API (Maps) resolves ENABLED-but-KEYLESS -> deploy then 401.
    DRIVE: construct a resolved set with (gcp_api,google-maps) but WITHOUT (gcp_secret,MAPS_API_KEY)
    and assert check_runtime_completeness FAILS it (invariant actually CATCHES the gap)."""
    print("\n=== M3 — key-bearing API enabled-but-keyless -> 401 (drive the FAILURE the invariant must catch) ===")
    # Take prospector's real resolved set and STRIP the MAPS_API_KEY -> the attack state.
    full = ada_resolve(PROSPECTOR_MANIFEST, ADA_BASELINE, ADA_LIBRARY)
    keyless = [e for e in full if e != ("gcp_secret", "MAPS_API_KEY")]
    check("M3 setup: keyless set has google-maps but NOT MAPS_API_KEY",
          ("gcp_api", "google-maps") in keyless and ("gcp_secret", "MAPS_API_KEY") not in keyless)
    ok, missing = check_runtime_completeness(keyless)
    # The invariant MUST report NOT-ok and name the missing pairing.
    check("M3: runtime-completeness FAILS the keyless set (invariant catches enabled-but-keyless)",
          (ok is False) and (("gcp_api", "google-maps"), ("gcp_secret", "MAPS_API_KEY")) in missing,
          f"ok={ok}, missing={missing}")
    # Positive control: the FULL prospector set PASSES (invariant doesn't false-positive).
    ok_full, missing_full = check_runtime_completeness(full)
    check("M3 control: full prospector set PASSES runtime-completeness (no false-positive)",
          ok_full is True and missing_full == [], f"missing={missing_full}")


def m2_no_credential_value():
    """M2 attack-path: a secret VALUE lands in agent context (transcript/argv/disk).
    DRIVE (design-property): the resolution/derivation layer materializes (kind,name) SLOTS ONLY —
    assert no resolved entry or derived-scope entry carries any value/secret field. The model can
    represent a slot name but has NO place to put a value."""
    print("\n=== M2 — credential VALUE exposure (design-property: only (kind,name) slots, no values) ===")
    all_entries = []
    for man in [PROSPECTOR_MANIFEST, SCIENCECLAW_MANIFEST, LABSTAT_BLS_MANIFEST]:
        all_entries.extend(ada_resolve(man, ADA_BASELINE, ADA_LIBRARY))
        all_entries.extend(derive_sa_scope(ada_resolve(man, ADA_BASELINE, ADA_LIBRARY)))
    # every resolved/derived entry is a 2-tuple of (kind, name) strings — NOTHING else.
    all_2tuple = all(isinstance(e, tuple) and len(e) == 2 and
                     isinstance(e[0], str) and isinstance(e[1], str) for e in all_entries)
    check("M2: every resolved/derived entry is exactly a (kind,name) 2-tuple — no value slot exists",
          all_2tuple, f"sample={all_entries[:3]}")
    # The BASELINE/LIBRARY records themselves carry only {kind,name} — no 'value'/'secret' field.
    val_fields = {"value", "secret", "secret_value", "val", "data", "password", "key_value"}
    leak = []
    for rec in ADA_BASELINE + [e for lst in ADA_LIBRARY.values() for e in lst]:
        for f in val_fields:
            if f in rec:
                leak.append((rec, f))
    check("M2: NO baseline/library record carries a credential-VALUE field (only kind+name)",
          leak == [], f"leaks={leak}")
    # The §4 spec is emit-then-apply: a value-free spec naming SLOTS. The resolution layer has no
    # API that takes or returns a value (sanity: resolve's signature is (manifest,BASELINE,LIBRARY)).
    # NOTE (§5.11 anchoring): inspect a PARAMETER NAME set, NOT the stringified signature.
    # The stringified sig inlines default values incl the baseline entry name 'POSTGRES_PASSWORD',
    # whose substring 'PASSWORD' would false-positive a naive `'password' in sig` match (a probe-
    # anchoring trap: matching data/defaults, not the intended target — a value-bearing parameter).
    import inspect
    param_names = list(inspect.signature(ada_resolve).parameters.keys())
    leak_params = [p for p in param_names
                   if any(tok in p.lower() for tok in ("value", "secret", "password"))]
    check("M2: resolve() has NO value/secret-bearing PARAMETER (slots-only contract)",
          leak_params == [], f"params={param_names}, leak={leak_params}")


def m6_mesh_security_design_property():
    """M6 attack-path: unauthorized party reaches a builder's mesh trigger/data.
    No live mesh in Phase-1 -> DESIGN-PROPERTY probe: grep the spec §7/§4-S5 for the required
    security elements; flag any missing. (This is a hard-easy: detection = read spec; verify = grep.)"""
    print("\n=== M6 — unauthorized mesh access (design-property check against §7/§4 S5) ===")
    import pathlib
    spec = pathlib.Path(__file__).resolve().parent.parent / "design-formal.md"
    text = spec.read_text(encoding="utf-8")
    required = {
        "deny-by-default policy": "deny-by-default",
        "serve-header-trust identity (Tailscale-User-Login)": "Tailscale-User-Login",
        "NEVER WhoIs-on-loopback": "never** WhoIs-on-loopback",
        "0600 AF_UNIX socket": "0600 AF_UNIX socket",
        "<BUILDER>_OPERATORS allowlist": "<BUILDER>_OPERATORS",
        "Funnel OFF": "Funnel OFF",
    }
    for human, needle in required.items():
        present = needle in text
        check(f"M6: spec specifies {human}", present, "" if present else f"MISSING needle {needle!r}")


def main():
    print("=" * 78)
    print("stoa--jw5 VERA INDEPENDENT probes — re-derive resolution + drive M1-M4/M6 attack-paths")
    print("design: agents/design/stoa--jw5/design-formal.md | provisions NOTHING | reads no env")
    print("=" * 78)
    part1_independent_resolution()
    m4_baseline_omit_fail_closed()
    m1_cross_builder_lateral()
    m3_keyless_maps_caught()
    m2_no_credential_value()
    m6_mesh_security_design_property()
    print("\n" + "=" * 78)
    if failures:
        print(f"VERA RESULT: FAIL — {len(failures)} probe assertion(s) falsified:")
        for f in failures:
            print(f"  - {f}")
        print("=" * 78)
        return 1
    print("VERA RESULT: PASS — independent resolution agrees (two-impl + hand-derived);")
    print("             M1-M4/M6 attack-paths driven and defeated.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())

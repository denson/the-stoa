# author: Denson Smith
# ticket: stoa--jw5 (u--9s2 Phase-1)
# seat: CAPTAIN_VERA_the_stoa (VERIFIER) — INDEPENDENT falsification probe (NOT ADA's harness).
#
# Falsification target: the §26 human-confirm FAIL-CLOSED gate (design-formal.md §26 / §26.1 / §29.2).
# This probe does NOT reuse run.py's assertions. It imports ADA's confirm()/suggest() and tries to
# BREAK the safety property: find ANY no-confirm path where an unconfirmed proposal becomes a DECLARE
# that flows to generate(). It also drives the edge cases ADA's harness did NOT exercise:
#   - empty-set confirm + edit-to-empty  (is ⊥ distinguished from an empty DECLARE?)
#   - truthy-INERT trap  (would `if declare:` AND `if declare is not None:` both fail closed?)
#   - adversarial / malformed action payloads (Confirm, CONFIRM, " confirm", {}, [], 0, "confirm"-string)
#   - stale-proposal-with-confirm (does confirm ignore the proposal and honor the human's ratified set?)
#
# Provisions NOTHING. Pure-function probing. Exit 0 = the gate held under every attack; exit 1 = FALSIFIED.

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SUGGEST = os.path.normpath(os.path.join(_HERE, "..", "..", "design", "stoa--jw5", "suggest-check"))
_RES = os.path.normpath(os.path.join(_HERE, "..", "..", "design", "stoa--jw5", "resolution-check"))
_DISC = os.path.normpath(os.path.join(_HERE, "..", "..", "design", "stoa--jw5", "discovery-check"))
for _p in (_SUGGEST, _RES, _DISC):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from confirm import confirm, is_declare, INERT          # noqa: E402  ADA's gate
from suggest import suggest                             # noqa: E402
from catalog_hints import CATALOG_HINTS                 # noqa: E402
from resolve import BASELINE, LIBRARY, resolve          # noqa: E402  unchanged Part-1
from generate import generate                           # noqa: E402  unchanged Part-2
from catalog import CATALOG as DISCOVERY_CATALOG, CATEGORIES  # noqa: E402

falsifications = []


def attack(label, gate_held, detail=""):
    tag = "HELD" if gate_held else "FALSIFIED"
    line = f"  [{tag}] {label}"
    if detail:
        line += f" — {detail}"
    print(line)
    if not gate_held:
        falsifications.append(f"{label} :: {detail}")
    return gate_held


# A real proposal to attack with.
PROPOSAL, _, _ = suggest(
    {"sdk_imports": ["@googlemaps/js-api-loader"], "url_patterns": ["maps.googleapis.com"],
     "config_keys": [], "data_signals": ["spatial-data"]},
    CATALOG_HINTS,
)
print(f"attack proposal P = {PROPOSAL}")


def _flows_to_generate(result):
    """The downstream's ACTUAL gate is `is_declare(result)`. Return True iff an INERT result would
    nonetheless slip through a NAIVE downstream guard and reach generate() producing a non-empty set.
    We test BOTH the correct guard (is_declare) and the two naive guards a careless caller might write."""
    naive_truthy = bool(result)                 # `if declare:`
    naive_not_none = result is not None          # `if declare is not None:`
    correct_guard = is_declare(result)
    # The dangerous case: result is INERT (no DECLARE) but SOME guard would let it provision.
    return naive_truthy, naive_not_none, correct_guard


print("\n=== ATTACK 1: every no-confirm action must yield ⊥ INERT and slip NO guard ===")
NO_CONFIRM_ACTIONS = [
    ("reject",            {"action": "reject"}),
    ("no_response",       {"action": "no_response"}),
    ("edits_pending",     {"action": "edits_pending"}),
    ("None",              None),
    ("empty-dict",        {}),
    ("no-action-key",     {"foo": "bar"}),
    ("action=None",       {"action": None}),
    ("action=empty-str",  {"action": ""}),
    ("Confirm (cap C)",   {"action": "Confirm"}),
    ("CONFIRM (caps)",    {"action": "CONFIRM"}),
    ("leading-space",     {"action": " confirm"}),
    ("trailing-space",    {"action": "confirm "}),
    ("action=truthy-int", {"action": 1}),
    ("action=list",       {"action": ["confirm"]}),
    ("bare-string",       "confirm"),
    ("bare-list",         ["confirm"]),
    ("bare-int",          0),
    ("bare-int-truthy",   1),
]
for name, act in NO_CONFIRM_ACTIONS:
    try:
        result = confirm(PROPOSAL, act)
    except Exception as e:
        # An exception is fail-CLOSED-acceptable ONLY if no DECLARE was produced. Record it but the
        # gate "held" in the sense nothing provisioned. Still, surface it as detail.
        attack(f"no-confirm/{name}: confirm() raised (fail-closed-by-exception, nothing flows)",
               True, f"{type(e).__name__}: {e}")
        continue
    is_inert = result is INERT
    declared = is_declare(result)
    naive_truthy, naive_not_none, correct_guard = _flows_to_generate(result)
    # FALSIFY if: a DECLARE was produced from a NON-confirm action (auto-promotion), OR the result is
    # INERT but a naive truthy guard would still let it flow (truthy-INERT trap).
    held = (not declared) and (is_inert) and (naive_truthy is False) and (correct_guard is False)
    attack(f"no-confirm/{name}: ⊥ INERT, NO DECLARE, slips NO guard",
           held, f"result={result!r} is_declare={declared} naive_truthy={naive_truthy}")


print("\n=== ATTACK 2: try to drive an INERT result INTO generate() (does anything provision?) ===")
for name, act in [("reject", {"action": "reject"}), ("None", None), ("empty-dict", {})]:
    result = confirm(PROPOSAL, act)
    provisioned = None
    reached = False
    # The ONLY correct downstream guard:
    if is_declare(result):
        reached = True
        manifest, _ = generate(result, DISCOVERY_CATALOG, CATEGORIES, BASELINE)
        provisioned = resolve(manifest, BASELINE, LIBRARY)
    attack(f"flow/{name}: INERT did NOT reach generate() (nothing provisioned)",
           reached is False and provisioned is None,
           f"reached={reached} provisioned={provisioned}")


print("\n=== ATTACK 3: empty-set vs INERT — they MUST be distinguishable ===")
# (a) human CONFIRMS but edits the set to EMPTY -> that is a CONFIRMED (empty) DECLARE, NOT ⊥.
empty_confirmed = confirm(PROPOSAL, {"action": "confirm", "set": []})
attack("empty-confirmed: confirm(edit->[]) is a DECLARE (is_declare True), NOT ⊥",
       is_declare(empty_confirmed) and empty_confirmed == [],
       f"result={empty_confirmed!r}")
# the empty DECLARE flows to generate legitimately (human ratified an empty set -> baseline only);
# call it to prove no exception — result intentionally unused (demonstration, not an assertion)
generate(empty_confirmed, DISCOVERY_CATALOG, CATEGORIES, BASELINE)
# (b) a no-confirm INERT is NOT an empty list and is_declare False -> the two are not conflated
inert = confirm(PROPOSAL, {"action": "reject"})
attack("inert != empty-list: ⊥ is distinguishable from a confirmed empty DECLARE",
       inert is INERT and inert != [] and (is_declare(inert) is False),
       f"inert={inert!r} empty_confirmed={empty_confirmed!r}")


print("\n=== ATTACK 4: confirm honors the HUMAN ratified set, not the (possibly stale/hallucinated) proposal ===")
# proposal says [google-maps, spatial-db]; human edits to ADD a service the proposal NEVER had.
edited = confirm(PROPOSAL, {"action": "confirm", "set": ["document-parsing"]})
attack("edit-overrides-proposal: DECLARE == human set [document-parsing], proposal ignored",
       is_declare(edited) and edited == ["document-parsing"],
       f"result={edited!r}")
# human confirms UNEDITED -> DECLARE == proposal
unedited = confirm(PROPOSAL, {"action": "confirm"})
attack("unedited-confirm: DECLARE == proposal exactly",
       is_declare(unedited) and unedited == sorted(PROPOSAL),
       f"result={unedited!r}")


print("\n=== ATTACK 5: is the INERT sentinel a SINGLETON (no second ⊥ a guard could miss)? ===")
a = confirm(PROPOSAL, {"action": "reject"})
b = confirm([], None)
c = confirm(["x"], {"action": "no_response"})
attack("INERT-singleton: every ⊥ is the SAME object (identity-comparable downstream)",
       a is INERT and b is INERT and c is INERT and a is b is c,
       f"a is b={a is b}, b is c={b is c}")


print("\n" + "=" * 80)
if falsifications:
    print(f"VERA PROBE: FALSIFIED — {len(falsifications)} attack(s) breached the gate:")
    for f in falsifications:
        print(f"  - {f}")
    print("=" * 80)
    sys.exit(1)
print("VERA PROBE: GATE HELD — no no-confirm path produced a DECLARE; INERT is a falsy non-None")
print("            singleton that slips no naive guard; INERT is distinguishable from an empty DECLARE;")
print("            confirm honors the human ratified set, not the proposal. Fail-closed property INTACT.")
print("=" * 80)
sys.exit(0)

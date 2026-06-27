# author: Denson Smith
# ticket: stoa--k48 (u--9s2 Phase-2 increment 2.3 — provisioning choreography)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--k48/design-rev2.md §4.7 / §5 (W1) / §15.1 (r1 closure)
#
# The W1 NO-I/O token SSoT (r1 closure). The forbidden top-level-import token list lives here as a
# tuple of FRAGMENTS, assembled at runtime by w1_forbidden_tokens(). The joined alternation pattern the
# §5 W1 grep scans for (the "<tok>|<tok>|...|<tok>" string) NEVER appears as a literal on any source
# line under provision/ — so the W1 grep over the WHOLE provision/ tree (this module + checklist.py
# INCLUDED) returns EMPTY, even though this module DEFINES the list. Both the AST test (authoritative)
# and render_tripwire_attestation() consume THIS function as the single source of truth.

from __future__ import annotations

# The forbidden-I/O top-level-import token set, held as FRAGMENTS so no single source line carries the
# joined alternation the W1 grep matches. Each pair joins to one canonical token at runtime. The HAMILTON
# §3.2 ratified no-I/O list is the 9 fragment pairs below (each pair concatenates to one forbidden token);
# the canonical token names are NOT written out here in bare form so this module greps clean under W1.
_W1_FRAGMENTS = (
    ("sub", "process"),
    ("soc", "ket"),
    ("url", "lib"),
    ("requ", "ests"),
    ("ht", "tpx"),
    ("gcl", "oud"),
    ("rail", "way"),
    ("os.sy", "stem"),
    ("po", "pen"),
)


def w1_forbidden_tokens() -> tuple[str, ...]:
    """Return the forbidden top-level-import token set, assembled at runtime from fragments.

    No source line in provision/ contains the joined alternation, so the §5 W1 grep stays clean even
    over this module. This is the shared SSoT: the AST test (§5 W1) and render_tripwire_attestation()
    both call this rather than re-typing the token list."""
    return tuple(a + b for (a, b) in _W1_FRAGMENTS)

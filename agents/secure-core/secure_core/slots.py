# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: rev2 §1.2.1 (INV-DEST) — url_slots accept ONLY FIXED or ENUM; a free-form / open
#                       string slot type is NOT REPRESENTABLE.
#
# The url_slot types. There are EXACTLY two, both server-pinned: FIXED (a single pinned value) and ENUM (a
# closed choice-set). There is NO free-form / open-string slot constructor — that is INV-DEST made
# STRUCTURAL: a caller-steerable destination component is not representable in the type system. Any url_slot
# value that is not one of these instances is an INV-DEST violation the loader refuses to serve (a plain
# `str` in a url_slot is the canonical "free-form host" attack the loader rejects).

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FIXED:
    """A server-pinned FIXED destination component (e.g. the core's OWN GCP project). NEVER caller-settable
    — a caller cannot select or override a FIXED slot."""

    value: str

    def resolve(self, selection: str | None) -> str:
        # A FIXED slot ignores any caller selection entirely; a caller attempt to select it is rejected
        # upstream (handler) as an INV-DEST violation before we ever get here.
        return self.value


@dataclass(frozen=True)
class ENUM:
    """A server-pinned CLOSED choice-set. The resolved value is choices[0] by default, OR a caller
    selection that MUST be a member of `choices` (validated at the handler). A value outside the closed set
    is not constructable — the destination host-set is finite and server-pinned, so an ENUM selection can
    never introduce an attacker host (INV-DEST)."""

    choices: tuple[str, ...]

    def __init__(self, choices):
        object.__setattr__(self, "choices", tuple(choices))
        if not self.choices:
            raise ValueError("ENUM url_slot must declare at least one choice")

    @property
    def default(self) -> str:
        return self.choices[0]

    def resolve(self, selection: str | None) -> str:
        if selection is None:
            return self.default
        if selection not in self.choices:
            # Signalled to the handler as a Rejected(400) — a selection outside the closed set.
            raise ValueError(f"ENUM selection {selection!r} not in closed choices {self.choices!r}")
        return selection

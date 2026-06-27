# author: Denson Smith
# ticket: stoa--fdf (u--9s2 Phase-2 increment 2.2)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR) — NEW §27 wiring artifact
# design-ground-truth: agents/design/stoa--fdf/design-rev2.md §2.6 (wiring the confirmed DECLARE to the
#                      UNCHANGED 2.1 core) / §27 (P3 provenance) / §3 P5b (P3 tag) / §29.2 (fail-closed) ;
#                      builder_deploy_core.generate / .resolve — IMPORTED UNMODIFIED (the §2-constraint)
#
# Wires the §26-confirmed DECLARE into the UNCHANGED 2.1 core:
#   examine -> suggest -> (proposed) -> §26 confirm -> D -> [P3 tag] -> generate(D) -> resolve() -> 8/6/7
#
# THE §2 CONSTRAINT (load-bearing): generate + resolve are IMPORTED from builder_deploy_core UNMODIFIED
# (module-identity, NOT a copy — this module defines NEITHER of its own). SUGGEST is strictly UPSTREAM
# of DECLARE (§24.0): feeding the CONFIRMED DECLARE into the unchanged generate()->resolve() IS the proof.
#
# Provisions NOTHING; the manifest stays a derived, human-gated T2 artifact (the P3 tag is a PROVENANCE
# label on the DECLARE record, §27 — agent-proposed + human-ratified). Reads no environment beyond the
# DATA tables dataload loads from the package's own data/ tree.

from __future__ import annotations

# --- IMPORT the UNCHANGED 2.1 core (module-identity; NEVER reimplemented/edited — the §2-constraint) ---
from builder_deploy_core.discovery.generate import generate
from builder_deploy_core.resolution.resolve import resolve

from builder_deploy_core.suggest.confirm import is_declare


# §27 provenance label. The confirmed DECLARE is tagged P3 = agent-PROPOSED (SUGGEST) + human-RATIFIED
# (§26 CONFIRM) — distinct from P1 (hand-authored services list) and P2 (a derived/hand-written manifest).
PROVENANCE_P3 = "P3"


def tag_declare(declare_services, provenance: str = PROVENANCE_P3) -> dict:
    """Tag a confirmed DECLARE service-id list with its §27 provenance. Returns a DECLARE record
    { services: [...], provenance: 'P3' }. Pure; the tag is metadata, not a provisioning input."""
    return {"services": sorted(set(declare_services)), "provenance": provenance}


def declare_from_confirm(confirm_result, catalog, categories, baseline, library):
    """§27 wiring — feed a §26 confirm() result into the UNCHANGED generate()->resolve() core.

    GATES ON is_declare() FIRST (§29.2 fail-closed, made executable): an INERT confirm result
    SHORT-CIRCUITS — generate() is NEVER called, nothing resolves, NOTHING flows downstream.

    Inputs:
      confirm_result: the return of confirm()/confirm_presented() — a DECLARE list[service_id] OR INERT.
      catalog, categories, baseline, library: the DATA tables (dataload-loaded), passed UNCHANGED to the
                                              imported generate()/resolve().

    Returns:
      None                                   iff confirm_result is INERT (fail-closed; generate NOT called).
      (declare_record, manifest, resolved)   iff confirm_result is a DECLARE — where
          declare_record = {services, provenance: 'P3'} (the §27 P3-tagged record),
          manifest       = generate(D, catalog, categories, baseline)[0]  (the §19 manifest),
          resolved       = resolve(manifest, baseline, library)           (the §2 resolved set, 8/6/7).
    """
    # §29.2 fail-closed gate: INERT short-circuits — the imported generate() is never reached.
    if not is_declare(confirm_result):
        return None

    declare_record = tag_declare(confirm_result)
    services = declare_record["services"]

    # the UNCHANGED 2.1 core: D -> generate() (§19) -> manifest -> resolve() (§2) -> resolved set.
    manifest, _called = generate(services, catalog, categories, baseline)
    resolved = resolve(manifest, baseline, library)
    return declare_record, manifest, resolved

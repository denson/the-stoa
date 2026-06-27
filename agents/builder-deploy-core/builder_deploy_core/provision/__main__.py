# author: Denson Smith
# ticket: stoa--k48 (u--9s2 Phase-2 increment 2.3 — provisioning choreography)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--k48/design-rev2.md §2 (__main__ — dry-run emit + mock walk repro)
#
# `python -m builder_deploy_core.provision` — the dry-run emit + mock walk repro surface. It loads the
# shipped DATA, resolves a worked example, emits the value-free spec, prints the checklist + attestations,
# and walks the mock choreography (mode-2, populated) printing the ledger. Provisions NOTHING (mock only).
# May import sys (for sys.exit / sys.argv) — sys is NOT a forbidden-I/O token (§5 W1 whitelists sys for
# __main__.py exactly as discovery/__main__.py does).

from __future__ import annotations

import sys

from builder_deploy_core import dataload
from builder_deploy_core.resolution.resolve import resolve
import builder_deploy_core.resolution  # noqa: F401 — import populates the §3.3 kind-tables
from builder_deploy_core.provision import (
    Choreographer,
    MockProvisioner,
    assert_value_free,
    emit_spec,
    render_checklist,
    render_credential_attestation,
    render_tripwire_attestation,
)


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    slug = argv[0] if argv else "prospector"
    category = {
        "prospector": "geospatial",
        "scienceclaw": "document-consuming",
    }.get(slug, "geospatial")

    baseline = dataload.load_baseline()
    library = dataload.load_library()
    manifest = {"builder": slug, "category": category, "delta": {}}
    resolved = resolve(manifest, baseline, library)

    spec = emit_spec(resolved, slug)
    assert_value_free(spec)  # the structural value-free guard (DoD#3)

    print(render_checklist(spec))
    print(render_credential_attestation(spec))
    print(render_tripwire_attestation())

    # mode-2 mock walk (everything populated -> S0..S6 run).
    populated = frozenset(s.name for s in spec.secret_slots)
    ledger = Choreographer(MockProvisioner(populated=populated)).run(resolved, slug)
    assert_value_free(ledger)
    print(f"# mock walk ledger — terminal={ledger.terminal.value}, actions={len(ledger.actions)}")
    for a in ledger.actions:
        print(f"  {a.step} {a.op}({a.target}) -> {a.status.value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

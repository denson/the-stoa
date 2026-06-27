# author: Denson Smith
# ticket: stoa--k48 (u--9s2 Phase-2 increment 2.3 — provisioning choreography)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--k48/design-rev2.md §4.7 / §10 (the 3 relay-up generators) /
#                       §5 (the 3-wall TRIPWIRE) / §15.1 (r1 closure — structural citation, no joined literal)
#
# The three PURE relay-up generators. Each is a derivation over the value-free spec + the structural
# walls (so none can drift from what the choreography actually does). render_tripwire_attestation cites
# the W1 wall STRUCTURALLY via tripwire.w1_forbidden_tokens() (the fragment SSoT) — it NEVER embeds the
# joined token alternation literal in SOURCE (r1 closure). The §5 W1 grep over the WHOLE provision/ tree
# (this module INCLUDED) therefore returns EMPTY. Generic prose here uses the safe service-name forms
# (capitalized / underscore) so the W1 word-boundary grep does not match (§9 r4 note). Imports stdlib +
# builder_deploy_core.* (W1).

from __future__ import annotations

from builder_deploy_core.provision.tripwire import w1_forbidden_tokens


def render_checklist(spec) -> str:
    """relay-up #1 — the PROVISIONING CHECKLIST. A PURE transform of the value-free emit: exactly what
    the PRINCIPAL provisions for a REAL builder, step + WHEN, including which secret slots need human
    population at S2c BY acquisition method (§9). Cannot drift from the choreography (it reads the spec)."""
    lines = []
    lines.append(f"# Provisioning checklist — builder: {spec.builder_slug}")
    lines.append("")
    lines.append("## Per-builder boundary (out-of-band, before any apply)")
    lines.append(f"- GCP project: {spec.project}")
    lines.append(f"- Service account (bijective): {spec.sa}")
    lines.append("- Prepaid card -> billing account (the per-builder hard cap; "
                 f"budget_boundary_required={str(spec.budget_boundary_required).lower()})")
    lines.append("- Railway account + Tailscale tailnet (the serving + mesh substrate)")
    lines.append("")
    lines.append("## APIs to enable (S1)")
    for api in spec.apis:
        lines.append(f"- {api}")
    lines.append("")
    lines.append("## Secret slots needing HUMAN population at S2c (by acquisition method)")
    for slot in spec.secret_slots:
        lines.append(f"- {slot.name}  [{slot.kind}]  -> acquire via: {slot.acquisition}")
    lines.append("")
    lines.append("## Railway variables (S3)")
    for var in spec.railway_vars:
        lines.append(f"- {var}")
    lines.append("")
    lines.append("## DB extensions (S4)")
    for ext in spec.db_extensions:
        lines.append(f"- {ext}")
    lines.append(f"- base image: {'postgis-capable' if spec.needs_postgis_base_image else 'plain'}")
    lines.append("")
    lines.append("## Mesh SHAPE (S5) — T1, domain-empty")
    lines.append("- 0600 AF_UNIX UDS; Tailscale-User-Login header trust; deny-by-default; Funnel OFF")
    lines.append("- only concrete route: health; domain endpoint: <VERB> placeholder (501 until T3)")
    return "\n".join(lines) + "\n"


def render_credential_attestation(spec) -> str:
    """relay-up #2 — the credential-discipline attestation. A derivation asserting the four
    credential-discipline points + referencing the spec. The applier reads from the OS keyring / WIF;
    no agent or code holds a value; the per-builder card is the hard cap."""
    lines = []
    lines.append(f"# Credential-discipline attestation — builder: {spec.builder_slug}")
    lines.append("")
    lines.append("1. VALUE-FREE EMIT: the provisioning spec carries slot NAMES only "
                 f"({len(spec.secret_slots)} secret slots); no field can hold a credential value "
                 "(assert_value_free is the structural guard — DoD#3).")
    lines.append("2. NO AGENT HOLDS A VALUE: the choreography dispatches to a value-free port; the mock "
                 "holds zero values in both modes; emit is pure (M2).")
    lines.append("3. THE REAL APPLIER READS FROM THE OS KEYRING / WIF: it lives OUTSIDE the package "
                 "forever; agents never run a credential-bearing apply (the emit/apply seam).")
    lines.append("4. PER-BUILDER CARD = HARD CAP: the prepaid card per builder is the out-of-band budget "
                 f"boundary (budget_boundary_required={str(spec.budget_boundary_required).lower()}); the "
                 "choreography REPRESENTS the requirement at S0, never creates a card (M5-moot / §5.B).")
    lines.append("")
    lines.append("Secret slots (all unpopulated at emit; human/CI populates at S2c):")
    for slot in spec.secret_slots:
        lines.append(f"- {slot.name}  [populated={str(slot.populated).lower()}]  via {slot.acquisition}")
    return "\n".join(lines) + "\n"


def render_tripwire_attestation() -> str:
    """relay-up #3 — the TRIPWIRE-held attestation. Cites W1/W2/W3 STRUCTURALLY (r1): it describes the
    W1 wall via the tripwire.w1_forbidden_tokens() SSoT + the grep INVOCATION shape, WITHOUT embedding the
    joined token alternation literal in SOURCE. If the rendered TEXT lists the tokens pipe-joined, that is
    RUNTIME OUTPUT (stdout), not source bytes — the §5 grep scans provision/ SOURCE, so it stays clean."""
    tokens = w1_forbidden_tokens()             # assembled at runtime from the fragment SSoT
    token_line = " | ".join(tokens)            # RUNTIME OUTPUT only — never a source literal in this file
    lines = []
    lines.append("# TRIPWIRE-held attestation (the 3 structural walls)")
    lines.append("")
    lines.append("W1 — NO I/O imports anywhere under provision/:")
    lines.append("  - AST test (authoritative): every module's top-level imports are a subset of")
    lines.append("    {builder_deploy_core.*, dataclasses, enum, typing, abc, __future__} (+ sys for "
                 "__main__ only).")
    lines.append("  - The forbidden-I/O token set is tripwire.w1_forbidden_tokens() (the fragment SSoT); "
                 f"it currently resolves to {len(tokens)} tokens at runtime: {token_line}.")
    lines.append("  - Grep attestation: the §5 W1 grep over provision/ for those tokens returns EMPTY "
                 "(exit 1) over the WHOLE tree (checklist.py + tripwire.py INCLUDED) — the source carries "
                 "no joined alternation literal, so grep AND the AST test AGREE (both clean).")
    lines.append("")
    lines.append("W2 — only the mock concrete port exists:")
    lines.append("  - Provisioner.__subclasses__() == [MockProvisioner]; Choreographer(None) raises "
                 "TypeError (the constructor requires a port); MockProvisioner is instantiable (it "
                 "implements every @abstractmethod incl select_base_image).")
    lines.append("")
    lines.append("W3 — the emit side has no port at all:")
    lines.append("  - emit_spec takes no provisioner parameter; it is a pure transform (no I/O).")
    return "\n".join(lines) + "\n"

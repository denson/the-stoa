# author: Denson Smith
# ticket: stoa--k48 (u--9s2 Phase-2 increment 2.3 — provisioning choreography)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--k48/design-rev2.md §4.5 (S0..S6 as pure step functions) /
#                       §6 (S5 T1 SHAPE) / §15.3 (the dispatched-verb audit) / design-formal §4
#
# S0..S6 as pure step functions: (resolved, slug, spec, provisioner) -> list[StepAction]. Each dispatches
# the spec's already-derived fields to the INJECTED port and returns the actions, in step order. The
# fail-closed semantics: S2c emits a BLOCKED action (the choreographer halts before S3); any port raise
# is surfaced by the choreographer as a FAILED action (abort). Imports stdlib + builder_deploy_core.* (W1).

from __future__ import annotations

from builder_deploy_core.resolution.resolve import check_runtime_completeness
from builder_deploy_core.provision.port import StepAction, StepStatus


def _status_for_created(created: bool) -> StepStatus:
    return StepStatus.OK if created else StepStatus.SKIPPED


def s0(resolved, slug, spec, provisioner):
    """S0 — fixed: bijective project + SA + the budget boundary (the §5.B card requirement REPRESENTED).
    Runs BEFORE any S2, so a key is never materialized before the per-builder lock exists."""
    actions = []

    provisioner._maybe_fail("S0", "ensure_project")
    provisioner.ensure_project(slug)
    created = provisioner._created_flag(f"project:{slug}")
    actions.append(StepAction("S0", "ensure_project", spec.project, _status_for_created(created),
                              created=created))

    provisioner._maybe_fail("S0", "ensure_sa")
    provisioner.ensure_sa(slug, spec.project)
    created = provisioner._created_flag(f"sa:{slug}")
    actions.append(StepAction("S0", "ensure_sa", spec.sa, _status_for_created(created),
                              detail=(("project", spec.project),), created=created))

    provisioner._maybe_fail("S0", "set_budget_boundary")
    provisioner.set_budget_boundary(slug, spec.project)
    actions.append(StepAction("S0", "set_budget_boundary", spec.project, StepStatus.OK,
                              detail=(("budget_boundary_required", "true"),), created=True))
    return actions


def s1(resolved, slug, spec, provisioner):
    """S1 — gcp_api: per api enable_api + grant_api_role (idempotent)."""
    actions = []
    for api in spec.apis:
        provisioner._maybe_fail("S1", "enable_api")
        created = provisioner.enable_api(spec.project, api)
        actions.append(StepAction("S1", "enable_api", api, _status_for_created(created), created=created))

        provisioner._maybe_fail("S1", "grant_api_role")
        created = provisioner.grant_api_role(spec.sa, api)
        actions.append(StepAction("S1", "grant_api_role", api, _status_for_created(created),
                                  detail=(("sa", spec.sa),), created=created))
    return actions


def s2(resolved, slug, spec, provisioner):
    """S2 — secret slots: 2a ensure_secret_slot (slot only); 2b grant_secret_accessor per-secret;
    2c is_populated -> if False emit BLOCKED (the choreographer halts before S3). NEVER improvises a
    value. thirdparty_rest_key has NO S1 step (the labstat proof — these slots appear here, not in S1)."""
    actions = []
    blocked = []
    for slot in spec.secret_slots:
        provisioner._maybe_fail("S2", "ensure_secret_slot")
        created = provisioner.ensure_secret_slot(spec.project, slot.name)
        actions.append(StepAction("S2", "ensure_secret_slot", slot.name, _status_for_created(created),
                                  detail=(("kind", slot.kind),), created=created))

        provisioner._maybe_fail("S2", "grant_secret_accessor")
        created = provisioner.grant_secret_accessor(spec.sa, slot.name)
        # per-secret accessor: detail names exactly ONE secret + the SA, never a project wildcard.
        actions.append(StepAction("S2", "grant_secret_accessor", slot.name, _status_for_created(created),
                                  detail=(("sa", spec.sa), ("secret", slot.name)), created=created))

    # 2c — the gate read. Emit a BLOCKED action for every unpopulated slot; the choreographer halts.
    for slot in spec.secret_slots:
        provisioner._maybe_fail("S2", "is_populated")
        if not provisioner.is_populated(slot.name):
            blocked.append(slot.name)
            actions.append(StepAction("S2", "is_populated", slot.name, StepStatus.BLOCKED,
                                      detail=(("acquisition", slot.acquisition),), created=False))
    return actions, tuple(blocked)


def s3(resolved, slug, spec, provisioner):
    """S3 — Railway vars + db/serving services. Injects only THIS builder's SA-key-ref (no cross-builder
    key ref). Secret-backed vars name a source_slot, never a value."""
    actions = []
    provisioner._maybe_fail("S3", "provision_db_service")
    provisioner.provision_db_service(slug, spec.db_extensions, spec.needs_postgis_base_image)
    created = provisioner._created_flag(f"db-service:{slug}")
    actions.append(StepAction("S3", "provision_db_service", f"db-{slug}", _status_for_created(created),
                              created=created))

    provisioner._maybe_fail("S3", "provision_serving_service")
    provisioner.provision_serving_service(slug)
    created = provisioner._created_flag(f"serving-service:{slug}")
    actions.append(StepAction("S3", "provision_serving_service", f"serving-{slug}",
                              _status_for_created(created), created=created))

    service = f"serving-{slug}"
    # railway_var entries (DATABASE_URL) are plain vars; secret-backed vars name a source_slot (the
    # secret slots). Both are S3 actions naming a SOURCE slot, never a value.
    for var in spec.railway_vars:
        provisioner._maybe_fail("S3", "set_railway_var")
        created = provisioner.set_railway_var(service, var)
        actions.append(StepAction("S3", "set_railway_var", var, _status_for_created(created),
                                  detail=(("service", service),), created=created))
    for slot in spec.secret_slots:
        provisioner._maybe_fail("S3", "set_railway_var")
        created = provisioner.set_railway_var(service, slot.name, source_slot=slot.name)
        actions.append(StepAction("S3", "set_railway_var", slot.name, _status_for_created(created),
                                  detail=(("service", service), ("source_slot", slot.name)),
                                  created=created))
    return actions


def s4(resolved, slug, spec, provisioner):
    """S4 — db_extension: apply each resolved extension + select the base image (now an ABC verb, r3)."""
    actions = []
    db_service = f"db-{slug}"
    for ext in spec.db_extensions:
        provisioner._maybe_fail("S4", "apply_db_extension")
        created = provisioner.apply_db_extension(db_service, ext)
        actions.append(StepAction("S4", "apply_db_extension", ext, _status_for_created(created),
                                  detail=(("db_service", db_service),), created=created))

    provisioner._maybe_fail("S4", "select_base_image")
    tag = provisioner.select_base_image(spec.needs_postgis_base_image)
    actions.append(StepAction("S4", "select_base_image", tag, StepStatus.OK,
                              detail=(("needs_postgis_base", str(spec.needs_postgis_base_image).lower()),),
                              created=True))
    return actions


def s5(resolved, slug, spec, provisioner):
    """S5 — fixed T1 SHAPE: stand_up_mesh_shape -> the §7 surface (0600 AF_UNIX + header-trust +
    deny-by-default + <BUILDER>_OPERATORS + Funnel OFF) + the CLI-client template carrying a <VERB>
    placeholder + a generic health route ONLY. Domain-empty."""
    actions = []
    provisioner._maybe_fail("S5", "stand_up_mesh_shape")
    provisioner.stand_up_mesh_shape(slug)
    actions.append(StepAction("S5", "stand_up_mesh_shape", f"mesh-{slug}", StepStatus.OK,
                              detail=(("transport", "af_unix"), ("funnel", "off")), created=True))
    return actions


def s6(resolved, slug, spec, provisioner):
    """S6 — fixed: engine-level verify (re-reads the ledger; NOT a port call) + the FROZEN
    check_runtime_completeness(resolved) read. Report-only; idempotent re-run = no-op. The op string
    "verify" is the ONLY op that is not a port method (r5 reconciled)."""
    actions = []
    actions.append(StepAction("S6", "verify", f"preflight-{slug}", StepStatus.OK,
                              detail=(("checked", "ledger"),), created=False))

    ok, missing = check_runtime_completeness(resolved)   # FROZEN call (read-only)
    # GROUND-CHECK NOTE (design drift, shipped code is canon): check_runtime_completeness returns
    # missing as list[((api_kind, api_name), (secret_kind, secret_name))] — each ident is a (kind,name)
    # tuple, NOT a bare name string (design-rev2 §8.12 wrote the M3 probe against bare names). We build
    # to ship reality: extract the value-free NAME from each ident tuple for the (key, name) detail.
    if not ok:
        for (api_ident, secret_ident) in missing:
            api_name = api_ident[1]
            secret_name = secret_ident[1]
            actions.append(StepAction("S6", "verify", api_name, StepStatus.OK,
                                      detail=(("missing_api", api_name),
                                              ("missing_secret", secret_name)),
                                      created=False))
    else:
        actions.append(StepAction("S6", "verify", f"runtime-complete-{slug}", StepStatus.OK,
                                  detail=(("runtime_completeness", "ok"),), created=False))
    return actions

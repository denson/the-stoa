# author: Denson Smith
# ticket: stoa--k48 (u--9s2 Phase-2 increment 2.3 — provisioning choreography)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--k48/design-rev2.md §3.3 (RunLedger) / §4.6 (Choreographer —
#                       requires the injected port, no default; W2) / §4.5 (ordered/idempotent/fail-closed)
#
# The port-driven ENGINE. Choreographer(provisioner).run(resolved, slug) emits the spec, then walks
# [S0,S1,S2,S3,S4,S5,S6] in fixed order, dispatching each step's actions to the INJECTED port. Stops at
# the first FAILED (a port raise) or BLOCKED (S2c unpopulated) — fail-closed. The constructor REQUIRES a
# port (no default) — W2's teeth: a run cannot start without a port, and the only port in existence is the
# mock. Imports stdlib + builder_deploy_core.* (W1).

from __future__ import annotations

from dataclasses import dataclass

from builder_deploy_core.provision.port import StepAction, StepStatus
from builder_deploy_core.provision.spec import emit_spec
from builder_deploy_core.provision import steps as _steps


@dataclass(frozen=True)
class RunLedger:
    builder_slug: str
    actions: tuple[StepAction, ...]      # every action emitted, in execution order (step-index monotonic)
    terminal: StepStatus                 # OK (S6 reached) | BLOCKED (S2c) | FAILED (a port raise)
    blocked_slots: tuple[str, ...] = ()  # slot NAMES reported BLOCKED-on-human at S2c (value-free)


class Choreographer:
    def __init__(self, provisioner):
        if provisioner is None:
            raise TypeError("Choreographer requires a Provisioner (no default) — W2")
        self.provisioner = provisioner

    def run(self, resolved, slug) -> RunLedger:
        """Emit the spec, then walk S0..S6 in fixed order, dispatching to the port. Stops at the first
        FAILED or BLOCKED (fail-closed). Records each action with its step index. S0<S2<S3/S5 is then a
        checkable property of the ledger (action step-indices monotonic)."""
        spec = emit_spec(resolved, slug)
        actions: list[StepAction] = []

        # Import here to avoid a hard module-load dependency on the concrete mock's failure type.
        from builder_deploy_core.provision.mock import MockProvisionerFailure

        # S0, S1
        for step_fn in (_steps.s0, _steps.s1):
            try:
                actions.extend(step_fn(resolved, slug, spec, self.provisioner))
            except MockProvisionerFailure as exc:
                actions.append(self._failed_action(step_fn, str(exc)))
                return RunLedger(slug, tuple(actions), StepStatus.FAILED)

        # S2 (returns actions + blocked-slot names)
        try:
            s2_actions, blocked = _steps.s2(resolved, slug, spec, self.provisioner)
        except MockProvisionerFailure as exc:
            actions.append(self._failed_action(_steps.s2, str(exc)))
            return RunLedger(slug, tuple(actions), StepStatus.FAILED)
        actions.extend(s2_actions)
        if blocked:
            # S2c BLOCK — halt before S3 (fail-closed human gate). NEVER improvises a value.
            return RunLedger(slug, tuple(actions), StepStatus.BLOCKED, blocked_slots=blocked)

        # S3, S4, S5, S6
        for step_fn in (_steps.s3, _steps.s4, _steps.s5, _steps.s6):
            try:
                actions.extend(step_fn(resolved, slug, spec, self.provisioner))
            except MockProvisionerFailure as exc:
                actions.append(self._failed_action(step_fn, str(exc)))
                return RunLedger(slug, tuple(actions), StepStatus.FAILED)

        return RunLedger(slug, tuple(actions), StepStatus.OK)

    @staticmethod
    def _failed_action(step_fn, detail_msg: str) -> StepAction:
        step = step_fn.__name__.upper()  # "s0" -> "S0"
        # op-vocab coherence (c4): the FAILED action's op must stay inside the canonical vocabulary
        # (the §4.3 ABC verb names + the engine-level "verify"; §3.1). The raising verb is threaded
        # through the MockProvisionerFailure message ("mock fail_at S<n>:<op>") — extract it so op names
        # the verb that raised, and target names the verb the op acted on (the §3.1 target contract),
        # rather than the non-canonical "fail" op / step-name target. Falls back to the engine op
        # "verify" if the message carries no parseable verb (the only other engine-level op).
        op = "verify"
        if ":" in detail_msg:
            op = detail_msg.rsplit(":", 1)[-1].strip()
        return StepAction(step, op, op, StepStatus.FAILED,
                          detail=(("reason", "provisioner_raise"),), created=False)

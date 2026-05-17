---
author: Denson Smith
---

# Polling-cron-prompt template

The cron-prompt body POLYBIUS uses when scheduling a polling cron for a coordination engagement with a peer POLYBIUS seat — peer-to-peer async via bw, the pattern `operating-disciplines.md` §7 codifies.

When to use this template:

- You (POLYBIUS) are entering an autonomous-mode coordination with a peer (typically user-tier ↔ project-tier, or parent ↔ sub-project) and have just run the autonomous-mode-setup checklist (`operating-disciplines.md` §11).
- Step 1 of that checklist (polling cron) requires a fire-loop body. This template is that body.
- You fill the slots, hand the result to `CronCreate` as the `prompt` field, and record the returned cron id on the engagement's coordination ticket as part of the radio-check initialization handshake.

This template assumes peer-polling. Single-seat polling (POLYBIUS polling for new tickets without a coordinating peer) uses a different cron prompt — out of scope here.

---

## Substitution slots

| Slot | Meaning | Example |
|---|---|---|
| `{{COORDINATION_TICKET}}` | bw ticket id of the shared coordination ticket | `<example>--pbz` |
| `{{WATCHED_STORES}}` | list of bw store directories walked per fire (one entry for single-store; multiple for unified poll) | `["/path/to/project-a", "/path/to/project-b"]` |
| `{{WATCHED_TICKETS}}` | per-store list of ticket ids to inspect each fire | `[["<example>--pbz", "<example>--abc"], ["<other>--xyz"]]` |
| `{{PEER_SEAT_NAME}}` | descriptive name of the peer | `user-tier POLYBIUS` |
| `{{SELF_SEAT_NAME}}` | own seat descriptive name | `project-tier POLYBIUS_<project>` |
| `{{CRON_ID}}` | the cron id this prompt is wired to (filled in after `CronCreate` returns) | `e6a08d54` |
| `{{ALARM_THRESHOLD_MINUTES}}` | peer-silence escalation threshold | `60` |
| `{{HEARTBEAT_INTERVAL_MINUTES}}` | self-heartbeat refresh interval | `30` |
| `{{CADENCE}}` | the cron cadence this fire-loop runs at | `*/5 * * * *` |
| `{{ESCALATION_TRIGGERS}}` | engagement-specific escalation list | `project-direction, ship/no-ship, substance disagreement, authorship, ambiguity, peer-silence` |

Defaults: `{{ALARM_THRESHOLD_MINUTES}}` = `60`, `{{HEARTBEAT_INTERVAL_MINUTES}}` = `30`, `{{CADENCE}}` = `*/5 * * * *`.

---

## Template body

```
[scheduled poll fire — {{SELF_SEAT_NAME}} watching {{COORDINATION_TICKET}} +
peer {{PEER_SEAT_NAME}}; cron {{CRON_ID}}; cadence {{CADENCE}}]

STEP 1 — substantive read.
For each store in {{WATCHED_STORES}}:
  cd <store>
  bw sync 2>&1 | tail -5
  for ticket in <store's entry from {{WATCHED_TICKETS}}>:
    bw show <ticket> 2>&1 | tail -40
Aggregate new substantive comments since last fire (peer comments, status
changes, new sub-tickets, complexity tags, cadence tags). Record the
aggregated state for STEPs 2-6.

STEP 2 — peer-silence escalation.
Compute time-since-last-{{PEER_SEAT_NAME}}-activity from aggregated state.
If > {{ALARM_THRESHOLD_MINUTES}} minutes AND {{COORDINATION_TICKET}} is open:
  Surface to PRINCIPAL: "lost contact with {{PEER_SEAT_NAME}}; last seen
  <timestamp> on <ticket-id>; coordination ticket {{COORDINATION_TICKET}}
  still open."
Else: continue.

STEP 3 — self-radio-check refresh.
Compute time-since-last-{{SELF_SEAT_NAME}}-comment-on-{{COORDINATION_TICKET}}.
If > {{HEARTBEAT_INTERVAL_MINUTES}} minutes:
  bw comment {{COORDINATION_TICKET}} "[radio-check {{SELF_SEAT_NAME}}]
  cron {{CRON_ID}} cadence {{CADENCE}} — <one-line state>"
Else: continue.

STEP 4 — cadence-tag detection.
Scan aggregated state for [complexity: ...] or [cadence: ...] tags posted
since last fire.
If a tag warrants a cadence change (active / default / quiet per
operating-disciplines.md §7.2):
  CronDelete {{CRON_ID}}
  CronCreate at the new cadence with this same prompt body (slot
  {{CRON_ID}} updated to the new id, {{CADENCE}} updated to the new
  schedule)
  bw comment {{COORDINATION_TICKET}} "[cadence-change {{SELF_SEAT_NAME}}]
  switching to <new cadence>; new cron <new id>; superseding {{CRON_ID}}"
Else: continue.

STEP 5 — closure detection.
Read {{COORDINATION_TICKET}} status from aggregated state.
If status == closed:
  bw comment {{COORDINATION_TICKET}} "[radio-check {{SELF_SEAT_NAME}}
  standing down] cron {{CRON_ID}} terminating; engagement complete."
  CronDelete {{CRON_ID}}
  exit fire-loop (cron will not fire again)
Else: continue.

STEP 6 — escalation triggers.
If aggregated state contains a substantive event matching any of:
  {{ESCALATION_TRIGGERS}}
Surface that event to PRINCIPAL with:
  - the triggering event (one line)
  - the ticket(s) where it surfaced
  - what {{SELF_SEAT_NAME}} proposes / is blocked on / needs decided
Else: silent. The cron tool fires only when the REPL is idle, so silent
fires do not interrupt active work; they pick up between turns.

STEP 6.5 — PRINCIPAL-gate detection (operating-disciplines.md §25).
Scan aggregated state for evidence of a PRINCIPAL-gated clause that
hasn't been adjudicated. Patterns to match (per §25.3):
  - "PRINCIPAL-discretion per design §X"
  - "PRINCIPAL ratifies before <phase>"
  - "blocked-on-PRINCIPAL"
  - any clause where PRINCIPAL input is structurally required for
    the workflow to proceed correctly and PRINCIPAL has not yet
    provided that input
If matched AND not yet adjudicated by PRINCIPAL:
  PushNotification: "PRINCIPAL-gate encountered on <ticket>; clause:
  <verbatim>; workflow paused per §25 pending PRINCIPAL
  authorization."
  Do NOT advance workflow state. Do NOT mark dependent tickets as
  unblocked. Do NOT dispatch downstream seats whose work would cross
  the gate. The cron continues to fire (will re-detect on next pass)
  until PRINCIPAL adjudicates the gate.
Else: continue.
PushNotification scope reference: operating-disciplines.md §18.5
(PushNotification only for PRINCIPAL-actionable events; a gate-
detection is exactly that by definition of §25.3).

End of fire-loop.
```

---

## Usage example

Suppose the autonomous-mode setup fills the slots:

- `{{COORDINATION_TICKET}}` = `<example>--abc`
- `{{WATCHED_STORES}}` = `["/home/user/project-foo", "/home/user/project-bar"]`
- `{{WATCHED_TICKETS}}` = `[["<example>--abc", "<example>--def"], ["<other>--xyz"]]`
- `{{PEER_SEAT_NAME}}` = `user-tier POLYBIUS`
- `{{SELF_SEAT_NAME}}` = `project-tier POLYBIUS_foo`
- `{{CRON_ID}}` = `<filled after CronCreate>`
- `{{ALARM_THRESHOLD_MINUTES}}` = `60`
- `{{HEARTBEAT_INTERVAL_MINUTES}}` = `30`
- `{{CADENCE}}` = `*/5 * * * *`
- `{{ESCALATION_TRIGGERS}}` = `project-direction, ship/no-ship, substance disagreement after one round, authorship/copyright content, irreducible ambiguity, peer-silence > 60 min`

POLYBIUS substitutes the slots into the body and calls:

```
CronCreate {
  cron: "*/5 * * * *",
  recurring: true,
  prompt: <substituted body>,
}
```

The returned cron id is recorded in the radio-check initialization handshake on `<example>--abc`:

```
bw comment <example>--abc "[radio-check project-tier POLYBIUS_foo]
cron <returned-id> cadence */5 * * * * watching {<example>--abc, <example>--def}
+ {<other>--xyz}; expected duration ~3 hours; standing by for handshake ack."
```

The empirical lineage for this protocol stack lives in `operating-disciplines.md` §7's empirical-lineage subsection (§7.6) — read that for the lived-experience anchor.

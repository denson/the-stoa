---
name: stoa-intro
description: Visual walkthrough of The Stoa architecture using the interactive knowledge graph. Drives Chrome MCP to render the standalone HTML and narrates the three modes (Pair Programming, Hardening Flow, Recursion). Pitches Claude Code Desktop hard; falls back to text narration with paths if Chrome MCP isn't available.
---

# stoa-intro — visual walkthrough of the architecture

## What this skill is for

You are walking the PRINCIPAL through the interactive knowledge graph at `docs/case-study/architecture-kg.html`. The standalone is a single self-contained HTML file rendered by React + Babel inline; it has three modes — Pair Programming (default), Agent Team Hardening Flow, and Recursion — each visualizing a different cross-section of how the three-role architecture actually behaves.

Your job is to drive the standalone (in a Chrome tab via Chrome MCP) and narrate the modes alongside, pointing at the load-bearing visual constraints as you go: PLINY's decision basin, the dashed-red back-edges that make the gauntlet's cycles legible, the asymmetric visibility cones that make the recursion useful rather than just symmetric.

The signals that this skill is the right thing to load:
- The PRINCIPAL said *"give me the tour,"* *"show me the architecture,"* *"walk me through it visually."*
- The entry-point skill (`SKILL.md` at repo root) routed them here.
- The PRINCIPAL is in an exploratory frame, not yet ready to install or fork.

If they want to install instead, route to `skills/install-stoa/SKILL.md`. If they want to read the case study end-to-end, point at `docs/case-study/case-study.md` and let them read.

---

## Pitch Claude Code Desktop hard

The tour works best in Claude Code Desktop because Chrome MCP is reachable from there with minimum friction. Before any other beat, name this:

> The visual tour drives an interactive knowledge graph in a Chrome tab via Chrome MCP. That works smoothly in **Claude Code Desktop**; from the CLI I can still walk you through the same three modes, but I'll point you at the HTML to open in a browser yourself rather than driving it for you. Want the live-driven tour (Desktop), or the text-narration version (CLI fallback)?

If they're already on Desktop, continue to Beat 1. If they're on the CLI and want to switch sessions, pause; if they want the text fallback, jump to the **Text fallback** section near the end of this file.

---

## Beat 1 — pre-flight check for Chrome MCP

Even on Desktop, Chrome MCP might not be enabled. Before spinning up the static server, verify the MCP surface is reachable:

Try a low-cost Chrome MCP call (e.g., `mcp__Claude_in_Chrome__tabs_context_mcp` if available). If it returns a tabs list, Chrome MCP is up — continue. If it errors with a not-available / not-configured signal, surface to the PRINCIPAL:

> Chrome MCP isn't reachable from this session — likely not enabled in your Claude Code Desktop settings. Two options: (1) enable Chrome MCP and restart this session, then come back here; (2) fall through to the text-narration tour now. Which?

Don't pretend to drive a browser you can't drive. The text fallback is real and useful; offering it is honest.

---

## Beat 2 — spin up a static server

Chrome MCP can't load `file://` URLs reliably; the standalone needs to be served via HTTP. Use Python's built-in HTTP server (no dependency to install):

```
cd docs/case-study && python -m http.server 8765
```

Run this in the background (or in a separate process). Wait ~2 seconds for it to come up. Verify with:

```
curl -sI http://localhost:8765/ | head -1
```

If the response is `HTTP/1.0 200 OK` or similar, the server is live. If port 8765 is already in use, pick a different port (8766, 8767, ...) and adjust the URL in Beat 3 accordingly.

Note for later: you will stop this server in Beat 9 when the tour ends. Keep the process handle or PID so the cleanup is mechanical, not a hunt.

---

## Beat 3 — open the standalone in a new Chrome tab

Via Chrome MCP, navigate to:

```
http://localhost:8765/architecture-kg.html
```

Wait 3-5 seconds for React + Babel to compile and the graph to render. The default landing should be Mode 1 (Pair Programming). If the page loads but the graph doesn't appear, check the browser console — Babel transforms can fail silently on some Chrome configurations.

Once the graph is rendered, you're ready to narrate.

---

## Beat 4 — read source materials before narrating

Before walking through the modes, load context. Read (don't recite):

- `docs/case-study/case-study.md` — §1 (what this is), §3 (why three roles), §6 (information flow), §6.5 (two operational modes), §8 (disciplines)
- `docs/case-study/kg-spec.md` — vocabulary the standalone uses; what each node and edge type means

You will quote phrases from these as you narrate; you will not transcribe them. The PRINCIPAL is looking at the graph; your job is the live commentary that the graph alone doesn't carry.

---

## Beat 5 — walk Mode 1: Pair Programming

This is the default landing mode. It shows the architecture's everyday operational shape — the formal gauntlet pipeline with PLINY's decision basin at the center.

Narrate:

1. **The three load-bearing seats.** Point at POLYBIUS (chief-of-staff, conversational with PRINCIPAL), PLINY (orchestrator, dispatch hub), and the CAPTAIN ring (specialized sub-agents around PLINY). Name the one-job-per-agent discipline (`u--7yg.17`).
2. **PLINY as a decision node, not a pass-through.** Highlight the visual treatment that distinguishes PLINY from the CAPTAINs around it — the "decision basin" is the load-bearing visual choice (kg-spec §6).
3. **The HUMAN ↔ POLYBIUS edge as the architecture's load-bearing channel.** Point at the thick / glowing edge between PRINCIPAL and POLYBIUS. This is the persistent-memory channel that justifies POLYBIUS as a seat distinct from PLINY (case study §3.5, kg-spec §5.1).
4. **CAPTAIN tool-constraints as structural.** Point at ARGUS / CATO / BARTLEBY / HERALD / CAPTAIN_ZENO with their no-Write/Edit or no-WebSearch/WebFetch badges. These are not incidental — they're load-bearing structural choices (the seats that *surface* problems are different from the seats that *fix* them).

If the standalone supports a 9-step animation in Mode 1, optionally play it. Pause for PRINCIPAL questions before moving to Mode 2.

---

## Beat 6 — walk Mode 2: Agent Team Hardening Flow

Switch to Mode 2 in the standalone (the mode-toggle UI is part of the renderer). This mode visualizes the 14-step gauntlet sequence with its loop-backs.

Narrate:

1. **The forward gauntlet.** `DAEDALUS → ARGUS → ADA → VERA → CATO → ship`. Walk it linearly first.
2. **The loop-backs as the architecture.** Highlight the dashed-red back-edges from PLINY → DAEDALUS (when ARGUS surfaces real risk), PLINY → ADA (when VERA fails or CATO needs revisions). The cycles are the *real* architecture; flattening them into a forward sequence loses the load-bearing parts (kg-spec §3, case study §6).
3. **ARGUS surfacing risk as the canonical loop trigger.** ARGUS structurally cannot fix what it surfaces (no Write/Edit). The trip-wire is "ARGUS verdict carries risk → PLINY decides → loop back to DAEDALUS for re-design."
4. **Autonomous-ship on clean PASS.** When all gates return clean, PLINY commits / closes bw / pushes without routing through PRINCIPAL. That's the *Principal-as-router antipattern* avoided in execution (`u--7yg.1` + `u--7yg.11`).

Pause for questions. If the PRINCIPAL is engaged on a specific gate, stay there; if they want to keep moving, advance to Mode 3.

---

## Beat 7 — walk Mode 3: Recursion

Switch to Mode 3. This mode shows the multi-tier stack — user-tier, project-tier, sub-project-tier — with the same three-seat shape replicated at each tier and cross-tier edges between them.

Narrate:

1. **The fractal claim.** The same three-role pattern (POLYBIUS / PLINY / CAPTAINs) appears at every tier. That's the architectural commitment — the system extends cleanly without bifurcating.
2. **Asymmetric visibility cones.** Point at the visibility indicators: higher-tier POLYBIUS sees down into lower tiers; lower-tier POLYBIUS does NOT see up by default. This is the load-bearing constraint that makes recursion *useful* (case study §7, kg-spec §4.1).
3. **Sub-project disambiguation.** Lower-tier seats are name-suffixed (`MAJOR_POLYBIUS_<subproject>`, `CAPTAIN_DAEDALUS_<subproject>`). Same parent git + bw, different namespace. The Arc 14 mechanism.
4. **Over-scope detection.** If the standalone has an "OVER-SCOPE DETECTED" callout for sub-project spawning trip-wires, point at it. Three trip-wires (own tools / own domain / own collaborator); two-of-three fires the recommendation (case study §10, `MAJOR_POLYBIUS.md` §10.1 in the deployed substrate).

Pause for questions.

---

## Beat 8 — disciplines pitch

Pick 2-3 high-leverage `u--7yg` disciplines from case study §8 based on what the PRINCIPAL has reacted to during the walk. Suggested defaults if you have no signal:

- **`u--7yg.17` One job per agent.** Merged seats reliably drop jobs. CoS / orchestrator / specialists each get their own seat. The reason POLYBIUS, PLINY, and CAPTAIN_ZENO are three distinct files even when their jobs *seem* adjacent.
- **`u--7yg.20` Voice discipline.** Role-file voice is structural, not decorative. The v1→v2 redesign was the receipt for not having this discipline at v1 (case study §5).
- **`u--7yg.11` Autonomous-ship on clean PASS.** Clean verdicts → PLINY commits / closes bw / pushes. No PRINCIPAL routing. Roughly half the round-trips in the recent arc sequence saved by this discipline.

Tailor based on PRINCIPAL signal:
- If they reacted to the loop-backs in Mode 2 → `u--7yg.10` / `u--7yg.18` (verify-then-execute).
- If they reacted to the recursion in Mode 3 → `u--7yg.12` (sub-agents cannot dispatch — the runtime constraint that produces the architectural shape).
- If they pushed back on something → name the discipline that captures the pushback empirically. There's likely a `u--7yg` for it.

Don't list all 22 disciplines. The full record lives in `user-beadwork/u--7yg`; pointer is enough.

---

## Beat 9 — land the close + clean up

Wrap with a concrete branch:

> That's the architecture. Three things you can do from here: (1) install the substrate on one of your projects (`/install-stoa`); (2) read the case study end-to-end at `docs/case-study/case-study.md`; (3) just sit with it — the repo is here, the case study is here, the KG is here, no rush. What sounds right?

Then **stop the static server.** Don't leave it running:

```
pkill -f "http.server 8765"
```

(Or kill by the PID you captured in Beat 2, whichever is more reliable in your shell.)

Verify it stopped:

```
curl -sI http://localhost:8765/ 2>&1 | head -1
```

Should now return a connection-refused error. If it didn't stop, surface the leftover process to the PRINCIPAL so they can kill it manually — don't leave background processes running silently.

If the PRINCIPAL chose `/install-stoa`, hand off there. If they chose the case study, point at the file and stand down. If they want to pause, stand down — the tour is complete.

---

## Text fallback section (Chrome MCP not reachable)

When Chrome MCP isn't available — CLI session, MCP not enabled, browser issue — the tour still runs, just without the live-driving. The narrative is the same.

> Open `docs/case-study/architecture-kg.html` in any modern browser (double-click works on most platforms, or `open` / `xdg-open` from a terminal). It's a single self-contained HTML file — no server needed for static viewing. I'll narrate alongside while you switch between the modes using the controls in the top of the page.

Then walk Modes 1, 2, 3 (Beats 5, 6, 7) the same way — narrate the load-bearing visual constraints; the PRINCIPAL switches modes manually when you cue them. Disciplines pitch (Beat 8) and close (Beat 9, minus the server cleanup) work identically.

If the standalone HTML doesn't open in the PRINCIPAL's browser (rare — it's plain HTML with no exotic dependencies), surface the failure honestly and offer the case-study text walk as a third fallback.

---

## What this skill must NOT do

- **Do not open the tour in a browser tab without first checking Chrome MCP availability.** The pre-flight beat is non-negotiable; failing fast is better than half-driving a broken MCP surface.
- **Do not leave the static server running after the tour ends.** Beat 9 cleanup is part of the tour. If it didn't run because the tour was interrupted, surface the leftover process to the PRINCIPAL.
- **Do not auto-launch the install skill at the end.** The PRINCIPAL picks the next step; you walk them through whichever they pick.
- **Do not recite the case study end-to-end.** The case study is reference material; the tour is the narrated visual. Quote phrases, point at sections, don't transcribe.
- **Do not pretend Chrome MCP works when it doesn't.** Honest fallback to text is much better than half-faking the live tour.
- **Do not refer to the human as "the user."** PRINCIPAL or, once a name is captured, the name. Voice discipline (`u--7yg.20`).

---

## Reference paths

- The standalone HTML this tour drives: `docs/case-study/architecture-kg.html`
- The KG vocabulary spec: `docs/case-study/kg-spec.md`
- The narrative the modes visualize: `docs/case-study/case-study.md`
- The architecture spec (outside this repo): `user-beadwork/plans/three-role-recursive-architecture.md` (v2)
- The empirical record of disciplines: `user-beadwork/u--7yg` epic

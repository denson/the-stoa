---
name: stoa-intro
description: Visual walkthrough of The Stoa architecture using the interactive knowledge graph. Uses Claude Preview (primary; works in Desktop and CLI) or Chrome MCP (fallback) to render the standalone HTML and narrate the three modes (Pair Programming, Hardening Flow, Recursion). Falls back to text narration with paths if neither preview tool is reachable.
---

# stoa-intro — visual walkthrough of the architecture

## What this skill is for

You are walking the PRINCIPAL through the interactive knowledge graph at `docs/case-study/architecture-kg.html`. The standalone is a single self-contained HTML file rendered by React + Babel inline; it has three modes — Pair Programming (default), Agent Team Hardening Flow, and Recursion — each visualizing a different cross-section of how the three-role architecture actually behaves.

Your job is to drive the standalone in a preview surface and narrate the modes alongside, pointing at the load-bearing visual constraints as you go: PLINY's decision basin, the dashed-red back-edges that make the gauntlet's cycles legible, the asymmetric visibility cones that make the recursion useful rather than just symmetric.

The signals that this skill is the right thing to load:
- The PRINCIPAL said *"give me the tour,"* *"show me the architecture,"* *"walk me through it visually."*
- The entry-point skill (`SKILL.md` at repo root) routed them here.
- The PRINCIPAL is in an exploratory frame, not yet ready to install or fork.

If they want to install instead, route to `skills/install-stoa/SKILL.md`. If they want to read the case study end-to-end, point at `docs/case-study/case-study.md` and let them read.

---

## Preview surfaces — primary, fallback, and text-only

The tour can drive the standalone via three different preview surfaces, in this priority order:

1. **Claude Preview** *(primary)* — the built-in `mcp__Claude_Preview__*` tools. Works in Claude Code Desktop AND the CLI. Repo ships `.claude/launch.json` with a `stoa-kg` server config so `preview_start("stoa-kg")` works out of the box. Screenshots come back inline in the chat — narration and visualization end up in the same scrollback.
2. **Chrome MCP** *(fallback)* — the `mcp__Claude_in_Chrome__*` tools. Desktop only; requires the Chrome MCP extension installed and connected. Drives a real Chrome window the PRINCIPAL can also interact with directly.
3. **Text-only narration** *(last resort)* — narrate the modes from the case study; the PRINCIPAL opens the HTML in their own browser. Works in any session regardless of preview tooling.

Beat 1 detects which is available; Beats 2, 3, 9 have a Path A (Preview) and a Path B (Chrome MCP); the **Text fallback** section near the end covers the third case. Beats 4–8 (the actual narration content) are tool-agnostic — they don't change based on which surface is driving.

---

## Beat 1 — capability detection

Detect which preview surface is reachable, in priority order:

**Try Claude Preview first.** Run `mcp__Claude_Preview__preview_list` (a no-arg, low-cost call). If it returns a list (empty or otherwise) without an MCP-not-available error, Claude Preview is reachable — go to Beat 2 with **Path A**. Most users land here regardless of whether they're on Desktop or CLI.

**If Claude Preview isn't reachable, try Chrome MCP.** Run `mcp__Claude_in_Chrome__tabs_context_mcp`. If it returns a tabs list, Chrome MCP is up — go to Beat 2 with **Path B**. Less common but supported.

**If neither is reachable**, surface honestly:

> I can't reach Claude Preview or Chrome MCP from this session, so I can't drive the visualization for you live. I can still walk you through the three modes from the case study while you open `docs/case-study/architecture-kg.html` in your own browser — same narrative, you switch modes manually. Want that, or would you rather pause and come back later in a session where preview tools are reachable?

Pick their answer. Do NOT pretend to drive a browser you can't drive. If they accept, jump to the **Text fallback** section near the end of this file.

---

## Beat 2 — start the preview server

### Path A — Claude Preview

Call `mcp__Claude_Preview__preview_start` with `name: "stoa-kg"`. The repo ships `.claude/launch.json` with that config (Python http.server on port 8769 serving `docs/case-study/`). Capture the returned `serverId` — you'll pass it to every subsequent Preview call.

If the call errors because Python isn't installed, surface honestly: *"Python isn't on PATH; the preview server needs it. I can fall through to the text-narration tour, or you can install Python and re-run."* If the call errors for other reasons (port collision, etc.), surface the error and offer to fall back to text or Chrome MCP.

### Path B — Chrome MCP

Spin up the Python static server manually:

```
cd docs/case-study && python -m http.server 8769
```

Run this in the background. Wait ~2 seconds for it to come up; verify with:

```
curl -sI http://localhost:8769/ | head -1
```

`HTTP/1.0 200 OK` means it's live. If port 8769 is already in use, pick another (8770, 8771, …) and adjust the URL in Beat 3. **Capture the PID** so cleanup in Beat 9 is mechanical, not a hunt — `pkill` can fail silently across bash environments; on Windows, prefer `taskkill /F /PID <pid>`.

---

## Beat 3 — open the standalone

### Path A — Claude Preview

Navigate to the standalone via `mcp__Claude_Preview__preview_eval`:

```
window.location.href = '/architecture-kg.html'
```

Wait 3–5 seconds for React + Babel to compile, then `mcp__Claude_Preview__preview_screenshot` to confirm the graph rendered. The default landing is Mode 1 (Pair Programming) — you should see PRINCIPAL at top, POLYBIUS below, PLINY's medallion at center surrounded by the CAPTAIN ring, BEADWORK substrate at the bottom.

For mode switching during Beats 5–7, use `preview_click` with `selector: ".mode-tab:nth-child(N)"` (where N is 1 / 2 / 3). The mode tabs are reliable click targets.

### Path B — Chrome MCP

Open a new tab and navigate to:

```
http://localhost:8769/architecture-kg.html
```

Wait 3–5 seconds for React + Babel to compile and the graph to render. Same expected default-landing as above. Switch modes during Beats 5–7 via Chrome MCP click on the same `.mode-tab:nth-child(N)` selector (or by clicking the tab text directly).

---

## Beat 4 — read source materials before narrating

Before walking through the modes, load context. Read (don't recite):

- `docs/case-study/case-study.md` — §1 (what this is), §3 (why three roles), §6 (information flow), §6.5 (two operational modes), §8 (disciplines)
- `docs/case-study/kg-spec.md` — vocabulary the standalone uses; what each node and edge type means

You will quote phrases from these as you narrate; you will not transcribe them. The PRINCIPAL is looking at the graph; your job is the live commentary that the graph alone doesn't carry.

---

## Narration shape — teach concepts, cite the visualization

Beats 5, 6, 7 walk the three modes. Every narration block follows a **Teach / Cite** shape:

> **Teach:** [The architectural claim — what's load-bearing, what consequence it has, what would break if it weren't true]. Multiple sentences. The teaching is the substance.
>
> **Cite:** [Where on the screen the claim is visually shown]. One short clause. Evidence, not the subject.

The visual is **never the subject** of a sentence. The architectural concept always leads. The visualization is a footnote the listener can verify against — not the lesson itself.

There are two adjacent activities, and they produce very different takeaways:

| Genre | What the agent does | What the listener leaves with |
|---|---|---|
| **Museum tour** *(avoid)* | Describes what's on screen, then says what each represents | *"There was a medallion in the middle, the CAPTAINs had badges, BEADWORK was a band at the bottom"* |
| **Whiteboard lecture** *(this skill)* | Teaches the architectural concept; visualization is evidence the agent points to | *"The orchestrator is a decision gate that catches every CAPTAIN verdict; some seats structurally can't fix what they surface; durable substrate makes the team survive across sessions"* |

The visualization is the *same* in both — the narration shape is what differs.

**Diagnostic test before each Teach block.** Ask yourself: *"If the PRINCIPAL closed their eyes right now, would they remember the architectural concept, or just the visual element?"* If the answer is the visual, rewrite — lead with the concept; demote the visual to a side-citation.

This shape applies to Beats 5–8. Beats 1–4 (setup) and Beat 9 (close + cleanup) are procedural and don't need it.

---

## Beat 5 — walk Mode 1: Pair Programming

This is the default landing mode. It shows the architecture's everyday operational shape with PLINY's decision basin at the center.

Following the Teach / Cite shape:

1. **Teach:** Three load-bearing seats, split on one-job-per-agent (`u--7yg.17`). POLYBIUS converses with the PRINCIPAL and holds durable memory across sessions. PLINY dispatches CAPTAINs and reconciles their verdicts. CAPTAINs each carry a single specialty — architect, plan-critic, executor, verifier, reviewer, etc. The v1 architecture tried merging these and the merged seats reliably dropped jobs; the empirical fix was the split.
   **Cite:** the three rank-coded clusters on screen — PRINCIPAL at top in HUMAN-rank shape, POLYBIUS + PLINY at MAJOR rank, the CAPTAIN ring around PLINY.

2. **Teach:** PLINY is a decision gate, not a pass-through. Every CAPTAIN verdict arrives at PLINY for a route-or-loop call — forward to the next gate, loop back if a problem surfaced, or escalate if scope exceeded. That's why the architecture has cycles instead of a forward DAG: PLINY is where the cycles trip. Flattening this into a linear sequence loses the load-bearing parts.
   **Cite:** the medallion shape distinct from the rectangular CAPTAIN cards (kg-spec §6).

3. **Teach:** The PRINCIPAL ↔ POLYBIUS channel is the persistent-memory channel — what justifies POLYBIUS as a seat distinct from PLINY. Conversations compound across sessions because POLYBIUS reads bw at activation, writes as work progresses, and reads again after compaction. Without this channel, POLYBIUS would just be a relay and the PRINCIPAL could talk to PLINY directly, collapsing the CoS seat.
   **Cite:** the thick / glowing edge between PRINCIPAL and POLYBIUS at the top of the graph (case study §3.5 Pattern 1, kg-spec §5.1).

4. **Teach:** Tool constraints on certain CAPTAINs are structural, not incidental. ARGUS audits a design but cannot rewrite it. CATO reviews a diff but cannot patch it. BARTLEBY recons the repo but has no web access. The seats that *surface* problems are deliberately separated from the seats that *fix* them — if ARGUS could fix what it surfaced, the audit would collapse into the build, and the independent verification would be lost.
   **Cite:** the small "no edit" badges on ARGUS / CATO / ZENO and "no web" badges on BARTLEBY / HERALD / ZENO.

If the standalone supports a 9-step animation in Mode 1, optionally play it. Pause for PRINCIPAL questions before moving to Mode 2.

---

## Beat 6 — walk Mode 2: Agent Team Hardening Flow

Switch to Mode 2. This mode visualizes the 14-step gauntlet sequence with its loop-backs.

Following the Teach / Cite shape:

1. **Teach:** The formal gauntlet has six gates in sequence — DAEDALUS designs, ARGUS audits the design, ADA executes, VERA verifies the result, CATO reviews the diff, ZENO mechanically checks for spec drift. Each gate produces a verdict that returns to PLINY for a routing decision. Walking it linearly is useful first as orientation, but linear is misleading: the cycles are the actual architecture.
   **Cite:** the forward path through the captain ring as the animation steps.

2. **Teach:** The loop-backs are what make this an architecture, not a forward DAG. When ARGUS surfaces real risk, PLINY loops back to DAEDALUS for re-design rather than letting risky work move to ADA. When VERA fails or CATO needs revisions, PLINY loops back to ADA. The architecture protects against work moving forward when problems exist — flattening these cycles into a forward sequence would lose what's structural.
   **Cite:** the dashed-red back-edges from PLINY → DAEDALUS and PLINY → ADA (kg-spec §3, case study §6).

3. **Teach:** ARGUS surfacing risk is the canonical loop trigger, and the no-edit constraint on ARGUS is what makes it work. ARGUS can flag a design problem but cannot rewrite the design — the trip-wire is "ARGUS verdict carries risk → PLINY decides → loop back to DAEDALUS for re-design." That structural separation is what keeps the audit independent of the build; if a single seat could both audit and fix, the verdict would collapse into the patch.
   **Cite:** the ARGUS card with its no-edit badge, and the loop-back animation that fires when its verdict carries risk.

4. **Teach:** When all gates return clean and no override flags fire, PLINY commits / closes the bw ticket / pushes — without routing through the PRINCIPAL. This is the *PRINCIPAL-as-router antipattern* avoided in execution: routing every clean ship through human approval turns the human into a pipeline component instead of leaving them in the strategic seat. Empirically, this discipline saved roughly half the round-trips in the recent arc sequence.
   **Cite:** the autonomous-ship branch from the final gate in the animation (`u--7yg.1`, `u--7yg.11`).

Pause for questions. If the PRINCIPAL is engaged on a specific gate, stay there; if they want to keep moving, advance to Mode 3.

---

## Beat 7 — walk Mode 3: Recursion

Switch to Mode 3. This mode shows the multi-tier stack — user-tier, project-tier, sub-project-tier — with the same three-seat shape replicated at each tier.

Following the Teach / Cite shape:

1. **Teach:** The same three-role pattern (POLYBIUS / PLINY / CAPTAINs) appears at every tier. User-tier covers all of one PRINCIPAL's projects. Project-tier scopes to a single project. Sub-project-tier handles work that needs its own tools, domain, or collaborator. The architectural commitment is that the system extends cleanly without bifurcating: there's no special "outer" architecture and "inner" architecture — just the same shape replicated at different scopes.
   **Cite:** the three stacked tiers in the visualization, each containing the same POLYBIUS + PLINY + CAPTAIN-ring pattern.

2. **Teach:** Visibility is asymmetric, and that asymmetry is what makes recursion *useful* rather than just symmetric replication. Higher-tier POLYBIUS sees down into lower-tier work — can read the lower tier's bw, can supervise without interrupting. Lower-tier POLYBIUS does NOT see up by default — keeps the lower tier focused on its own scope. Symmetric visibility would collapse the tiers into one noisy context; the asymmetry is what keeps them coherent and connected.
   **Cite:** the visibility-cone indicators between tiers (case study §7, kg-spec §4.1).

3. **Teach:** Lower-tier seats are name-suffixed to disambiguate (`MAJOR_POLYBIUS_<subproject>`, `CAPTAIN_DAEDALUS_<subproject>`). Same parent git repo, same bw substrate, different role-file namespace — that's the Arc 14 mechanism. The substrate flows down through naming, not through nesting; sub-projects share the durable layer with the parent rather than spinning up an isolated one.
   **Cite:** the name-suffixed labels on the sub-project tier seats.

4. **Teach:** A sub-project spawns when work hits the trip-wires that signal it needs its own scope: own tools, own domain, own collaborator. Two-of-three fires the recommendation. Below the threshold, work stays in the parent project; above, the team triggers a spawn that creates a new tier with its own POLYBIUS and a roster focused on the new scope. The spawn pattern is what keeps the team from collapsing under cross-domain pressure.
   **Cite:** the "OVER-SCOPE DETECTED" callout if visible in the standalone (case study §10, `MAJOR_POLYBIUS.md` §10.1).

Pause for questions.

---

## Beat 8 — disciplines pitch

Pick 2-3 high-leverage disciplines from the empirical record (case study §8) based on what the PRINCIPAL has reacted to during the walk.

**Frame the section explicitly as a few examples from the empirical record** — these are illustrations, not the full list (which has 22 children under `u--7yg` in the user-beadwork sibling repo). Open with framing like:

> Three example disciplines from the empirical record — pulled to illustrate what you've just seen on the graph:

or

> A few representative disciplines that map to the architecture you're looking at:

The framing makes clear these are pulled from a larger trail. Without it, listing tickets reads as a log file dropped into a presentation rather than narrative-with-citations.

**Lead with the discipline name; cite the ticket ID inline in parentheses as a side-citation, not as a section header.** The reader is hearing about disciplines, not browsing a ticket database. Bad: `u--7yg.17 — One job per agent`. Good: `**One job per agent** (u--7yg.17)`.

Suggested defaults if you have no signal:

- **One job per agent** (`u--7yg.17`). Merged seats reliably drop jobs. CoS / orchestrator / specialists each get their own seat. The reason POLYBIUS, PLINY, and CAPTAIN_ZENO are three distinct files even when their jobs *seem* adjacent.
- **Voice discipline** (`u--7yg.20`). Role-file voice is structural, not decorative. The v1→v2 redesign was the receipt for not having this discipline at v1 (case study §5).
- **Autonomous-ship on clean PASS** (`u--7yg.11`). Clean verdicts → PLINY commits / closes bw / pushes. No PRINCIPAL routing. Roughly half the round-trips in the recent arc sequence saved by this discipline.

Tailor based on PRINCIPAL signal:

- If they reacted to the loop-backs in Mode 2 → **Verify-then-execute** (`u--7yg.10` / `u--7yg.18`).
- If they reacted to the recursion in Mode 3 → **Sub-agents cannot dispatch** (`u--7yg.12`) — the runtime constraint that produces the architectural shape.
- If they pushed back on something → name the discipline that captures the pushback empirically. There's likely a `u--7yg` for it.

Close the section by pointing at the full record without listing it: *"The full 22-child trail lives at `user-beadwork/u--7yg` — these are three examples, not the catalog."* That keeps the empirical-rigor signal without dumping the rest as noise.

---

## Beat 9 — land the close + clean up

Wrap with a concrete branch:

> That's the architecture. Three things you can do from here: (1) install the substrate on one of your projects (`/install-stoa`); (2) read the case study end-to-end at `docs/case-study/case-study.md`; (3) just sit with it — the repo is here, the case study is here, the KG is here, no rush. What sounds right?

Then **stop the preview server.** Don't leave it running:

### Path A — Claude Preview

```
mcp__Claude_Preview__preview_stop(serverId)
```

Server lifecycle is managed; no PID hunt. If the call errors, surface and move on — the leftover server expires when the Claude Code session ends.

### Path B — Chrome MCP

Kill by the PID you captured in Beat 2:

- Windows (PowerShell or Git Bash): `taskkill //F //PID <pid>`
- Unix-like: `kill <pid>`

Avoid `pkill -f "http.server"` — it can fail silently across bash environments (empirically observed during the Arc 19 cold-clone test). Verify the server stopped:

```
curl -sI http://localhost:8769/ 2>&1 | head -1
```

Should return a connection-refused error. If the server didn't stop, surface the leftover process to the PRINCIPAL so they can kill it manually — don't leave background processes running silently.

### Hand off

If the PRINCIPAL chose `/install-stoa`, hand off there. If they chose the case study, point at the file and stand down. If they want to pause, stand down — the tour is complete.

---

## Text fallback section (neither preview surface reachable)

When neither Claude Preview nor Chrome MCP is available — older Claude Code without the Preview MCP, no Chrome MCP extension installed, locked-down environment — the tour still runs, just without the live-driving. The narrative is the same.

> Open `docs/case-study/architecture-kg.html` in any modern browser (double-click works on most platforms, or `open` / `xdg-open` from a terminal). It's a single self-contained HTML file — no server needed for static viewing. I'll narrate alongside while you switch between the modes using the controls in the top of the page.

Then walk Modes 1, 2, 3 (Beats 5, 6, 7) the same way — narrate the load-bearing visual constraints; the PRINCIPAL switches modes manually when you cue them. Disciplines pitch (Beat 8) and close (Beat 9, minus the server cleanup) work identically.

If the standalone HTML doesn't open in the PRINCIPAL's browser (rare — it's plain HTML with no exotic dependencies), surface the failure honestly and offer the case-study text walk as a third fallback.

---

## What this skill must NOT do

- **Do not start a preview server without first detecting which surface is available.** Beat 1 (capability detection) is non-negotiable; failing fast is better than half-driving a broken MCP surface.
- **Do not leave the static server running after the tour ends.** Beat 9 cleanup is part of the tour. For Path A, `preview_stop(serverId)` is the call. For Path B, kill by PID with `taskkill` (Windows) or `kill` (Unix). If cleanup didn't run because the tour was interrupted, surface the leftover process to the PRINCIPAL.
- **Do not auto-launch the install skill at the end.** The PRINCIPAL picks the next step; you walk them through whichever they pick.
- **Do not recite the case study end-to-end.** The case study is reference material; the tour is the narrated visual. Quote phrases, point at sections, don't transcribe.
- **Do not pretend a preview surface works when it doesn't.** Honest fallback to text is much better than half-faking the live tour.
- **Do not refer to the human as "the user."** PRINCIPAL or, once a name is captured, the name. Voice discipline (`u--7yg.20`).

---

## Reference paths

- The standalone HTML this tour drives: `docs/case-study/architecture-kg.html`
- The KG vocabulary spec: `docs/case-study/kg-spec.md`
- The narrative the modes visualize: `docs/case-study/case-study.md`
- The Claude Preview launch config (Path A): `.claude/launch.json` (server name: `stoa-kg`)
- The architecture spec (outside this repo): `user-beadwork/plans/three-role-recursive-architecture.md` (v2)
- The empirical record of disciplines: `user-beadwork/u--7yg` epic

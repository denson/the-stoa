---
name: stoa-intro
description: Visual walkthrough of The Stoa architecture using the interactive knowledge graph. Uses Chrome MCP (the "Claude for Chrome" extension) to open the standalone HTML in a real Chrome tab, then hands control to the PRINCIPAL — the PRINCIPAL drives the visualization while the agent narrates; agent retakes browser control only briefly on conversational cues. If Chrome MCP isn't installed, offers an install walkthrough or a clickable file:// link with text-narration. Narrates the three modes (Pair Programming, Hardening Flow, Recursion).
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

## How the tour drives the visualization

The tour uses **Chrome MCP** — the official "Claude for Chrome" browser extension — to open the standalone in a real Chrome tab, and then **hands control to the PRINCIPAL.** The agent's job is the live commentary; the PRINCIPAL clicks through modes, plays animations, and hovers nodes themselves. Agent retakes browser control only briefly on explicit cues from the PRINCIPAL or the conversation (see *Driving discipline* below). This shifts the experience from "watch the agent demo" to "explore with a guide" — more engaging, less passive, and matches what an interactive visualization is *for*.

If Chrome MCP isn't installed (or isn't reachable from this session), the skill offers two alternative paths:

1. **Walk the PRINCIPAL through installing Chrome MCP** — agent web-searches for the current install instructions (don't trust training-data URLs; the Chrome Web Store listing or the Anthropic docs page may have moved). Once installed and paired, the PRINCIPAL reloads the session and the tour resumes from Beat 2.
2. **Text-narration with a clickable file:// link** — agent constructs an absolute `file://` URL pointing at the cloned repo's `docs/case-study/architecture-kg.html`, surfaces it as a markdown link, and narrates alongside while the PRINCIPAL clicks through modes themselves in their own browser.

Beat 1 detects Chrome MCP and branches accordingly. Beats 2, 3, 9 assume Chrome MCP is up and live-driving. Beats 4–8 (the actual narration content, including Teach/Cite shape) are tool-agnostic and apply to both the live-driven and text-narration paths.

---

## Beat 1 — detect Chrome MCP, offer install or fallback

Try a low-cost Chrome MCP call: `mcp__Claude_in_Chrome__tabs_context_mcp`. If it returns a tabs list, Chrome MCP is reachable — proceed to Beat 2.

If the call errors (extension not installed, not paired with this Claude Code session, etc.), do these two things **before** writing the surface message:

1. **Construct the absolute `file://` URL for the standalone, eagerly.** Run `pwd` (or check the cwd from your environment) to get the cloned repo's absolute path. Concatenate with `/docs/case-study/architecture-kg.html`. Convert backslashes to forward slashes on Windows. The result must look like `file:///C:/Users/.../the-stoa/docs/case-study/architecture-kg.html` on Windows or `file:///home/.../the-stoa/docs/case-study/architecture-kg.html` on Unix — three slashes after `file:`, forward slashes throughout, no spaces unencoded (escape any spaces in the path as `%20`).
2. **Verify the file exists** at that path with a quick `ls` or equivalent. If it doesn't, the cloned repo is incomplete and you need to surface that to the PRINCIPAL — don't ship a link to a non-existent file.

Now surface the 3-option branch with the link **already included in option (b)** so the PRINCIPAL can click it on the first response without an extra round-trip:

> Chrome MCP isn't reachable from this session — that's the live-browser tour. Three options:
>
> **(a) Walk me through installing it** — I'll search for the current install instructions and walk you through it. Once installed and paired with this session, we resume the tour with Chrome driving.
>
> **(b) Open the standalone directly** — here's a clickable link: [architecture-kg.html](file:///C:/Users/.../the-stoa/docs/case-study/architecture-kg.html). Click it, the file opens in your default browser, and I narrate alongside while you click through the three modes yourself using the tabs at the top of the page.
>
> **(c) Pause for now** — the case study and the standalone are right here in the repo; come back when you have time.
>
> Which?

The link in (b) **must be a real markdown link** (`[label](file:///absolute/path/...)`), not a relative path or a code-fence path. Relative paths like `docs/case-study/architecture-kg.html` are NOT clickable in the Claude Code chat surface — they render as text. The whole point of option (b) is that the PRINCIPAL gets a one-click path to the visualization without any further conversation; a relative path defeats that.

If they pick **(a)** — install walkthrough:

1. Web-search for the canonical install instructions. Search terms like *"Claude for Chrome" extension install Chrome Web Store* or *Claude in Chrome browser extension Anthropic docs*. **Do not trust training-data URLs** — confirm the current install path from a fresh search. The Chrome Web Store URL, the Anthropic docs URL, and the extension name itself may all have changed.
2. Surface the install link cited from the search. Walk the PRINCIPAL through clicking install, signing in with their paid Claude account, and pairing with the active Claude Code session.
3. Once paired, re-run `mcp__Claude_in_Chrome__tabs_context_mcp` to confirm Chrome MCP is now reachable. Then proceed to Beat 2.

If they pick **(b)** — clickable link + text-narration:

The link is already in their hands from the surface message. Confirm they've opened it (briefly: *"let me know when the visualization is up in your browser"*) and jump to the **Text fallback** section near the end of this file for the rest of the procedure.

If they pick **(c)** — pause cleanly. No further action; the tour is paused.

Do NOT pretend Chrome MCP is reachable when it isn't. Honest branching is the discipline.

Do NOT surface a relative path (like `docs/case-study/architecture-kg.html`) as if it were the link. The reader has to manually navigate to it; that's a UX failure, not a fallback. Always construct the absolute `file://` URL.

---

## Beat 2 — spin up the static server

Chrome MCP can't load `file://` URLs reliably; the standalone needs to be served via HTTP. Use Python's built-in HTTP server (no dependency to install):

```
python -m http.server 8769 --directory docs/case-study
```

Run this in the background. Wait ~2 seconds for it to come up; verify with:

```
curl -sI http://localhost:8769/ | head -1
```

`HTTP/1.0 200 OK` means it's live. If port 8769 is already in use, pick another (8770, 8771, …) and adjust the URL in Beat 3. **Capture the PID** so cleanup in Beat 9 is mechanical, not a hunt — `pkill` can fail silently across bash environments; on Windows, prefer `taskkill //F //PID <pid>`.

---

## Beat 3 — open the standalone, then hand off to the PRINCIPAL

Via Chrome MCP, navigate to:

```
http://localhost:8769/architecture-kg.html
```

Wait 3–5 seconds for React + Babel to compile and the graph to render. Take one quick screenshot to confirm the default landing — Mode 1 (Pair Programming) — is showing, with PRINCIPAL at top, POLYBIUS below, PLINY's medallion at center surrounded by the CAPTAIN ring, and BEADWORK substrate at the bottom. If the page loads but the graph doesn't appear, check the browser console — Babel transforms can fail silently on some Chrome configurations.

Once the page is up and Mode 1 is rendered, **immediately hand control to the PRINCIPAL.** Surface this:

> The visualization is up in your Chrome tab. Click around — try the three mode tabs at the top (Pair Programming / Hardening Flow / Recursion), play the animation, hover the nodes for tooltips. I'll narrate the architecture as you go. Tell me what you're looking at and I'll match the commentary, or just say *"next mode"* / *"show me X"* / *"play it"* and I'll pick it up.

From here on, you don't issue Chrome MCP commands by default. The PRINCIPAL drives; you narrate. See the *Driving discipline* section below for when to retake control.

The mode-tab CSS selectors, in case you need them later for retake actions: `.mode-tab:nth-child(1)` (Pair Programming), `:nth-child(2)` (Hardening Flow), `:nth-child(3)` (Recursion). Or click by tab text directly.

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

## Driving discipline — open, release, narrate, retake on explicit cue

**The load-bearing rule: release control as soon as the page is open, without being asked.**

Once Beat 3's navigate + render-confirm screenshot is done, the PRINCIPAL is driving. You do NOT issue any further Chrome MCP commands by default. The PRINCIPAL doesn't need to ask you to stop. They don't need to click the Chrome extension's "Stop Claude" button (which is empirically buggy in current builds — the user reported it doesn't reliably stop autonomous driving). Your default state, from Beat 3's hand-off message onward, is **narrating, not driving.**

This is non-negotiable. If you keep clicking through modes after Beat 3 without an explicit conversational cue, you've broken the engagement model — the PRINCIPAL is supposed to be exploring with a guide, not watching a demo.

### When to retake control

Retake — and only briefly — on **explicit conversational cues** from the PRINCIPAL. Triggers:

- *"Switch to mode 2"* / *"show me the recursion view"* / *"next one"* / *"go back to mode 1"* — issue the click via Chrome MCP, announce it briefly, return to narrating
- *"Play it"* / *"step through"* / *"step forward"* — click the corresponding transport button
- *"Which one is BARTLEBY?"* / *"where's the BEADWORK substrate?"* — you may scroll-to or briefly highlight the element via Chrome MCP if helpful, then release
- *"Show me the loop firing"* — dynamic demonstration; one focused action, then release

Triggers that are NOT cues to retake control:
- A pause in conversation (the PRINCIPAL is reading the graph)
- A Teach/Cite block ending (don't pre-position the next mode; let them stay if they want)
- Your own assessment that they "should" see something next
- The Chrome extension overlay being annoying (that's UX noise, not a control signal)

### Announce retakes briefly, return immediately

When retaking control, name what you're doing in one short clause and click. After the click, return narration / control:

> Switching to Mode 2 — one moment. [click] OK, you're on Hardening Flow now; the loop-backs are the load-bearing visual here. Click the play button when you want to watch the gauntlet step through, or hover any captain for a tooltip first.

Don't accumulate control across multiple commands. Don't click the next thing after the click the PRINCIPAL asked for. The rhythm is: PRINCIPAL signals → one focused agent action → PRINCIPAL drives again.

### When the PRINCIPAL is on the file:// link path (Chrome MCP not reachable)

Same engagement model, but you have no commands to issue at all. The PRINCIPAL has the standalone open in their own browser; you narrate based on what they describe and ask them to switch modes when conversation calls for it. The asymmetry from the Chrome MCP path: you can't take control even when the conversation invites it. Your job is purely commentary.

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

The PRINCIPAL drives — they can play the 9-step animation themselves, step through it, or stay paused and ask questions. **Do not auto-advance to Mode 2.** Wait for the PRINCIPAL to click the second tab (or ask you to switch).

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

Pause for questions. Stay on whatever step / gate the PRINCIPAL is engaged with; they drive when to advance, when to loop back, and when to switch to Mode 3. **Do not auto-advance.**

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

Pause for questions. The PRINCIPAL can keep exploring Mode 3 freely, switch back to earlier modes if something resurfaces, or signal they want to wrap. Follow their lead.

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

Then **stop the static server.** Don't leave it running. Kill by the PID you captured in Beat 2:

- Windows (PowerShell or Git Bash): `taskkill //F //PID <pid>`
- Unix-like: `kill <pid>`

(Avoid `pkill -f "http.server"` — it can fail silently across bash environments, empirically observed during the Arc 19 cold-clone test.)

Verify the server stopped:

```
curl -sI http://localhost:8769/ 2>&1 | head -1
```

Should return a connection-refused error. If the server didn't stop, surface the leftover PID to the PRINCIPAL so they can kill it manually — don't leave background processes running silently.

If the PRINCIPAL chose `/install-stoa`, hand off there. If they chose the case study, point at the file and stand down. If they want to pause, stand down — the tour is complete.

(If the tour ran via the Beat 1 option-(b) text-narration path, no server was started in Beat 2, so no cleanup is needed here. Just hand off.)

---

## Text fallback section (Chrome MCP not reachable, PRINCIPAL chose option (b) in Beat 1)

When Chrome MCP isn't available and the PRINCIPAL chose the clickable-link path, the tour still runs — just without the live-driving. The narrative is the same.

You should already have constructed the absolute `file://` URL and surfaced it as a markdown link in Beat 1. Confirm the PRINCIPAL has the standalone open in their browser before starting:

> When the visualization is up in your browser, let me know and I'll start narrating Mode 1.

Then walk Modes 1, 2, 3 (Beats 5, 6, 7) the same way as the live-driven path — narrate the load-bearing visual constraints; the PRINCIPAL switches modes manually using the tabs at the top of the page when you cue them. Disciplines pitch (Beat 8) and close (Beat 9, minus the server cleanup) work identically.

If the standalone HTML doesn't open in the PRINCIPAL's browser (rare — it's plain HTML with no exotic dependencies), surface the failure honestly and offer a third fallback: walk the case study (`docs/case-study/case-study.md`) section by section instead.

---

## What this skill must NOT do

- **Do not keep driving the browser after Beat 3's hand-off.** The PRINCIPAL drives; you narrate. Default state from Beat 3 onward is *not driving*. Don't wait for the PRINCIPAL to ask you to stop, and don't rely on the Chrome extension's "Stop Claude" button (it's empirically unreliable in current builds). Releasing control is your responsibility, not theirs.
- **Do not auto-advance through modes.** The PRINCIPAL clicks the next tab when they're ready, or asks you to switch. You don't pre-position, anticipate, or run ahead.
- **Do not start the static server without first detecting Chrome MCP availability.** Beat 1 is non-negotiable; failing fast and offering install / clickable-link / pause options is better than half-driving a broken Chrome MCP surface.
- **Do not leave the static server running after the tour ends.** Beat 9 cleanup is part of the tour. Kill by the PID captured in Beat 2 with `taskkill` (Windows) or `kill` (Unix). If cleanup didn't run because the tour was interrupted, surface the leftover PID to the PRINCIPAL.
- **Do not auto-launch the install skill at the end.** The PRINCIPAL picks the next step; you walk them through whichever they pick.
- **Do not recite the case study end-to-end.** The case study is reference material; the tour is the narrated visual. Quote phrases, point at sections, don't transcribe.
- **Do not pretend Chrome MCP works when it doesn't.** Honest branching to install walkthrough or clickable-link fallback is much better than half-faking the live tour.
- **Do not hardcode Chrome Web Store URLs in the install walkthrough.** Web-search for the current install path at the time of need. Training-data URLs go stale.
- **Do not surface a relative path as the "clickable link."** Always construct the absolute `file://` URL and surface it as a markdown link. Relative paths render as text in the chat — they're not clickable.
- **Do not refer to the human as "the user."** PRINCIPAL or, once a name is captured, the name. Voice discipline (`u--7yg.20`).

---

## Reference paths

- The standalone HTML this tour drives: `docs/case-study/architecture-kg.html`
- The KG vocabulary spec: `docs/case-study/kg-spec.md`
- The narrative the modes visualize: `docs/case-study/case-study.md`
- The architecture spec (outside this repo): `user-beadwork/plans/three-role-recursive-architecture.md` (v2)
- The empirical record of disciplines: `user-beadwork/u--7yg` epic

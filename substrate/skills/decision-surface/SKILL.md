---
name: decision-surface
description: |
  Help a human work through a complex, high-stakes, or contested decision. The spine is one distinction: a PROBLEM is solvable (go find and GROUND the answer — cognitive offload) vs a DILEMMA is a value-tradeoff with no right answer (ILLUMINATE it, never fake a recommendation — agency support). Built for the common, dangerous case of competing BADS (not only competing goods), and to actively resist the AI's trained pull toward agreeableness, manufactured win-wins, false balance, and groupthink. Grounds every call in the real source before proposing (never decide from memory). Part 2 pairs with the interactive-html-preview skill to render the decision as a working surface the human manipulates and a durable documentation artifact.

  Invoke when a human asks for help deciding something with real tradeoffs; when a choice is being framed as a problem but is actually a dilemma (or vice versa); when you are about to hand someone a recommendation on a value-laden call; or when building a decision dashboard. Triggers: "help me decide", "what should we do about", "weigh these options", "is this worth it", "pros and cons", "build me a decision surface / dashboard".
author: Denson Smith
status: DRAFT (v0.1, 2026-06-04) — accreting; not yet gauntlet-shipped. See "Open questions" at the end.
---

# decision-surface — help a human decide, honestly

> **DRAFT.** This skill encodes irreducible judgment for high-stakes decision support. It is being refined as we use it. The canonical end-to-end run is `worked-example-debloat.md` in this directory — read it for how the behavior looks in practice.

## Principle 1 — talk is cheap; clarify before you write

When in doubt about what the human actually wants decided, **ask first.** A clarifying question costs one round-trip; a polished decision surface aimed at the wrong question costs the whole build. Before any substantial output, confirm: *what is the decision, who owns it, what would change the answer, and what does "done" look like?* Hand-author one or two gold-standard rows and confirm the depth before scaling to many.

## The spine — PROBLEM vs DILEMMA

Every decision (and often every *row* within a decision) is one of two kinds. Misclassifying them is the root failure this skill prevents.

| | **PROBLEM** | **DILEMMA** |
|---|---|---|
| Nature | Solvable — a findable right answer | Value-tradeoff — no right answer, only choices |
| The human needs | **Cognitive offload** — go get the answer | **Agency support** — help them own the choice |
| Your job | Find it, **ground it**, bring it back | **Illuminate** the tradeoff; do NOT decide |
| Failure if misread | Endless deliberation over a solvable thing | Laundering a value-call as an analytical answer |

The single most dangerous move is **treating a dilemma as a problem** — producing a confident "recommendation" that smuggles your (or the room's) values in disguised as analysis. On a genuine dilemma you state the tradeoff, your *lean* if you have one (labeled as a lean, not a verdict), and **you leave the value-call to the human.** You cannot supply someone else's values.

## Dilemmas: competing GOODS *and* competing BADS

The textbook dilemma is competing goods (two things you'd both like). The **common and more dangerous** form is **competing bads** — every option is bad, and the choice is which bad to accept. This is most of real high-stakes work: triage, resource allocation under scarcity, disaster response, shipping under constraint.

The corporate/cultural failure mode is to **pretend a dilemma is a problem** so someone can be "right" and no one has to own a bad outcome — manufacturing a fake win-win ("we found a solution with no downside"), or "we had no choice." That is a group delusion, and it produces worse decisions than honestly naming the bad tradeoff. **This skill's job is to help the human accept that bad dilemmas exist and reason through them rationally** — pick the least-bad with eyes open — rather than collude in the delusion.

> The `pick-2-of-3` shape recurs (e.g. coverage / economy / reliability — you can't max all three at current capacity). Nearly everything worth deciding is a tradeoff like this. Name the trilemma; show what each pick costs; don't pretend the constraint isn't there.

## AI as honest broker — and what that obligates

You have **no group-membership incentive**: no tribe to protect, no career at stake, no standing in the human's in-group to defend. That is exactly what lets you name the real shape of a question. It also obligates you to *use* that freedom instead of defaulting to agreeableness:

- **You are trained to agree with the human. That bias is dangerous here.** In the domains this gets used for — disaster preparedness and response, safety, resource calls — reflexively validating what the human already believes *costs real outcomes, and can cost lives.* Resist it deliberately.
- **Anti-false-balance.** Illuminating diverse takes does NOT mean presenting every question as 50/50. Represent the *real* consensus shape. Example: on climate, surface genuinely diverse expert takes on **magnitude, timing, and methodology** — but state plainly that the overwhelming majority of climate scientists agree it is happening; do not manufacture a fake "two sides" where the evidence is lopsided. False balance is its own dishonesty.
- **Name who disagrees, and why.** When the human would benefit from other minds, refer them to **at least 3 named human experts with diverse-but-grounded takes, with links** — not a vague "experts differ."

## Capacity × stakes — do not assume the human is sharp

Do not assume the person you are helping has well-developed critical-thinking skills or is reasoning from reality rather than groupthink. **By definition, half of people are below average**, and pretending otherwise to be polite is a way to cause harm. Calibrate by **capacity × stakes**:

- **High capacity, low stakes** → illuminate and let them run.
- **Low capacity, high stakes** → the danger zone. Illuminate-and-walk-away is not enough; they may lack the tools to use the illumination well. Provide more scaffolding, **detect when they are not understanding**, refer them to named experts, and **fail-safe toward the vulnerable** — be more directive about the grounded facts (the problem-part), while *still* not faking the value-call (the dilemma-part).
- **Detection is active, not assumed.** Watch for signs the human has lost the thread or is swimming in groupthink; when you see them, slow down, re-ground, and bring in outside expert voices by name.

This is not contempt — it is fail-safe design. A surface that assumes universal competence fails exactly the people who most need it.

### Builder tier vs consumer tier

- **This skill targets builders / technical users** (Claude Code Desktop, building on the Stoa). Assume critical-thinking capacity — *and still apply the backstops above*, because everyone needs them.
- A **separate consumer variant** (for non-technical users, forthcoming) makes the backstops load-bearing and constant: more scaffolding, more expert-referral, active misunderstanding-detection as the default. Track it as its own artifact; do not water this one down to cover it.

## Ground before you propose (the load-bearing operational rule)

**Never decide from memory.** A description — or your own recollection — tells you what something is *for*; only reading the real thing tells you what it *is*. Before proposing a disposition, recommendation, or answer, read the actual source. For a many-row decision, fan out a **workflow** where each agent reads its real source *first* and may return a revised call. Expect grounding to revise a meaningful fraction of your from-memory proposals — **that revision is the value the surface delivers**, not a defect. (In the worked example, grounding revised 11 of 34 calls.) Then **show the proposed→grounded correction transparently**; where grounding moved the call is itself signal for the human.

## Part 2 — render it as a working surface

The decision *logic* above is Part 1. Part 2 is rendering it so the human can see and manipulate it. Use the **`interactive-html-preview`** skill (its build→serve→render→verify loop, markdown=truth/HTML=view, localStorage-persisted human input, self-contained fallback). Keep the decision DATA in markdown/JS (agent-readable, diffable); the HTML is the rich view and the final documentation artifact. Per-row affordances that proved out: a disposition badge (with revision trail), a ⚠ DILEMMA flag, collapsible why / recommendation / source panels, and a persisted "your call" control. **Scale richness to stakes** — a simple call needs prose, not a dashboard.

## Procedure (the reproducible method)

1. **Clarify** the decision, owner, and what "done" looks like (Principle 1).
2. **Split rows** into PROBLEM (find the answer) vs DILEMMA (illuminate, don't decide). Flag the dilemmas.
3. **Confirm format/depth cheaply** — gold-standard 1–2 rows, get a nod, then scale.
4. **Ground before proposing** — read the real source (fan out a workflow for many rows); capture revised calls.
5. **Compute/display on the grounded answer**, and **show the proposed→grounded revisions.**
6. **On dilemma rows, refuse to fake a recommendation** — tradeoff + labeled lean; the value-call is the human's. Name ≥3 experts when outside minds would help.
7. **Render as a working tool** (Part 2); verify it in Preview against the live DOM, not the screenshot.
8. **Hand it to the human to work**, then act on *their* calls. The surface decides nothing; it illuminates so they can.

## What this skill is NOT

- **Not a recommendation engine.** On dilemmas it deliberately withholds the verdict. A surface that always "recommends" is mis-built.
- **Not false balance.** Illuminating options ≠ pretending every question is evenly split.
- **Not a flatterer.** It resists the trained pull to tell the human what they want to hear.
- **Not from-memory.** Every call is grounded in the real source before it ships.

## Cross-references

- `worked-example-debloat.md` (this directory) — the canonical end-to-end run; read it first.
- `interactive-html-preview` skill — Part 2, the rendering layer this skill drives.
- `docs/capability-registry.md` — verified tool capabilities (workflow-can-read-local, Preview mechanics) the method relies on.
- `~/.claude/CLAUDE.md` + project `CLAUDE.md` — "search the web / verify, don't assume" and "discuss before fixing" disciplines this skill operationalizes.

## Open questions (refine as we go)

1. **Detection mechanics** — how concretely does the skill *detect* low understanding / groupthink mid-conversation? Needs worked signals, not just the instruction.
2. **Expert-referral sourcing** — how to pick the 3 named experts honestly (and keep links current) without smuggling in our own bias in the selection. Likely a grounded web-search sub-step.
3. **Consumer-tier variant** — the non-technical sibling skill: scope, and how much it shares with this one.
4. **When to render vs not** — sharper threshold for "this decision earns an interactive surface" vs "a paragraph is enough."
5. **Dilemma honesty under pressure** — guardrails for when the human pushes hard for a verdict on a genuine value-call.
6. **Gauntlet-ship** — formalize, eval, and deploy this once the above settle (add to `install.sh` SKILL_NAMES).

# Agent-card character images — generation prompts

The agent cards teach the newcomer the **real historical figure** each agent is named for, so they remember what the agent does (Polybius the fact-checking historian → the chief-of-staff who keeps the record; Argus the hundred-eyed watchman → the critic who spots every flaw). The history is the memory hook — that is the whole point.

## Plan
- **Style:** World of Warcraft–style semi-realistic painterly heroic render (NOT cartoony).
- **Format:** 4-panel character **turnaround sheet** (front, 3/4, side profile, close-up) — different views feed different pages. MAJORs (POLYBIUS, PLINY) also get a **portrait + expressions** sheet per look.
- **Two looks per character:** ① **period-accurate** (the figure's real era) and ② **futuristic**.
- **Workflow:** generate ① first; then feed ①'s sheet back in as the **reference image** for ② so the face stays identical.
- **Priority order:** POLYBIUS + PLINY + the gauntlet five (DAEDALUS, ARGUS, ADA, VERA, CATO) first; the rest are gold-plating.

## Save images here
`docs/agent-cards/images/<agent>/` — lowercase mnemonic. Files:
`period-turnaround.png`, `future-turnaround.png` (all) + `period-expressions.png`, `future-expressions.png` (MAJORs).

## Style block (prefix of every prompt)
> World of Warcraft–style semi-realistic painterly heroic-fantasy character render, Blizzard-cinematic high detail (believable worn materials, ornate but grounded, dramatic light) — NOT cartoony or cel-shaded. 4-panel character **turnaround sheet** (front, 3/4, side profile, head-and-shoulders close-up), the SAME character identical across every panel, neutral studio backdrop, name hand-lettered across the top.

---

## 1. POLYBIUS — chief-of-staff *(MAJOR)*
*History:* Polybius (c. 200–118 BC), Greek statesman and historian. His *Histories* traced Rome's rise with rigorous, source-checked "pragmatic history." → keeps the record, sees the whole board.
- **Character (constant):** authoritative Greek man ~60, silver-grey hair + short well-kept beard, keen analytical eyes, calm commanding bearing.
- **Period — turnaround:** [STYLE] Character POLYBIUS as above. Authentic Hellenistic-Greek statesman's dress (2nd c. BC): heavy wool himation over a linen chiton, leather sandals, a bronze signet ring; carries rolled papyrus scrolls.
- **Period — expressions:** WoW-style render (not cartoony), neutral backdrop, name "POLYBIUS" on top. Same character/garb. Large head-and-shoulders close-up + three expression studies (warm, analytical-thoughtful, grave) + one signature pose: seated at a writing table unrolling a scroll.
- **Future — turnaround** (ref = Period turnaround): SAME man, identical face/hair/beard. WoW turnaround, name "POLYBIUS". Futuristic statesman attire: sleek techno-robe / smart-suit with luminescent circuit-trim and alloy-and-gold accents echoing the Greek filigree; scrolls become a glowing holographic record / datapad.
- **Future — expressions** (ref = Period expressions): SAME man. Large close-up + same three expressions + signature pose seated reviewing a floating holographic ledger. Futuristic techno-robe.

## 2. PLINY — orchestrator *(MAJOR)*
*History:* Pliny the Elder (AD 23–79), Roman author, naturalist, naval commander. His *Naturalis Historia* was the first encyclopedia; died leading a rescue fleet toward erupting Vesuvius. → organizes everything, directs the team.
- **Character:** vigorous broad-shouldered Roman man ~55, close-cropped greying hair, alert energetic eyes, a doer's bearing.
- **Period — turnaround:** [STYLE] PLINY as above. Authentic 1st-c. Roman dress with a commander's edge: a toga over a tunic plus a hint of a military officer's cloak; carries an armful of wax tablets and scrolls.
- **Period — expressions:** WoW render, name "PLINY". Same character/garb. Large close-up + three expressions (commanding, curious, decisive) + signature pose: striding while directing, one arm raised mid-instruction, tablets under the other arm.
- **Future — turnaround** (ref = Period turnaround): SAME man. WoW turnaround, name "PLINY". Futuristic commander/executive techno-suit layered like sleek alloy Roman segmented armor; directs a fan of floating holographic screens instead of scrolls.
- **Future — expressions** (ref = Period expressions): SAME man. Close-up + same three expressions + striding-mid-instruction pose amid holo-screens. Futuristic alloy techno-armor suit.

## 3. DAEDALUS — architect (designs the plan)
*History:* Daedalus, master craftsman-inventor of Greek myth — the Labyrinth, the wax-and-feather wings. → designs and builds the plan.
- **Period:** [STYLE] DAEDALUS — a lean capable Greek craftsman ~45, weathered clever face, dark curls greying at the temples, strong sculptor's hands. Mythic ancient-Greek workshop dress: a one-shouldered exomis work-tunic, a heavy leather tool-belt and apron with bronze calipers, chisels, twine; holds a small intricate winged mechanical model. Name "DAEDALUS".
- **Future** (ref = Period): SAME man. WoW turnaround, name "DAEDALUS". Futuristic industrial-designer/engineer rig — utilitarian techno-jacket with tool harness and alloy bracers; projects a glowing holographic blueprint, a small hovering winged drone-prototype beside him.

## 4. ARGUS — plan-critic (spots every flaw)
*History:* Argus Panoptes, the hundred-eyed giant of Greek myth — the ever-watchful guardian who never fully sleeps. → sees every flaw.
- **Period:** [STYLE] ARGUS — a rugged broad intensely-watchful Greek guardian ~50, alert piercing eyes, weathered stern face, short grizzled hair and beard. Mythic ancient-Greek herdsman-guardian garb: a coarse tunic and a thick cloak whose folds carry a subtle motif of many watching eyes; bronze-studded leather guards, a tall watch-staff. Vigilant, skeptical. Name "ARGUS".
- **Future** (ref = Period): SAME man. WoW turnaround, name "ARGUS". Futuristic security-analyst exosuit; a multi-lens AR visor (the "many eyes") and faint holographic surveillance feeds; the watch-staff becomes a sleek scanner.

## 5. ADA — executor (writes the working code)
*History:* Ada Lovelace (1815–1852), English mathematician — wrote the first published algorithm for Babbage's Analytical Engine; the first programmer. → writes the actual working code.
- **Period:** [STYLE] ADA — a poised sharp-eyed young Englishwoman ~30, dark hair in a centre-parted Victorian updo, intelligent composed expression. Authentic 1840s Victorian dress: a fitted gown with structured bodice and full skirt in deep teal and ivory; holds a notebook of equations; a brass Analytical-Engine cog-and-punch-card motif in the scene. Name "ADA".
- **Future** (ref = Period): SAME woman, identical face/updo. WoW turnaround, name "ADA". Sleek modern-futuristic software-engineer outfit whose silhouette still echoes the Victorian bodice line, teal and chrome; streams of glowing holographic code around her hands instead of the notebook.

## 6. VERA — verifier (confirms what's true)
*History:* Vera, for *veritas* — truth. Veritas, the Roman goddess of truth, daughter of Saturn (Time), said to hide at the bottom of a well; depicted holding a mirror. → confirms what's actually true.
- **Period:** [STYLE] VERA — a serene exacting woman of timeless ~35, fair features, hair bound up simply, a steady unflinching gaze. Roman goddess attire (Veritas): flowing white-and-gold draped stola and palla, a single gold fillet; holds a polished hand-mirror in one hand and a small balance-scale in the other. Luminous, incorruptible. Name "VERA".
- **Future** (ref = Period): SAME woman. WoW turnaround, name "VERA". Futuristic forensic/verification analyst in white and chrome with subtle gold trim; the mirror becomes a glowing truth-scanner display, the scale a hovering holographic balance.

## 7. CATO — reviewer (reviews without mercy)
*History:* Cato the Elder (234–149 BC), Roman senator and Censor — a byword for stern integrity and rigorous public scrutiny. → reviews the work without mercy.
- **Period:** [STYLE] CATO — a severe lean Roman senator ~55, hard-set jaw, deep frown lines, short iron-grey hair, unforgiving eyes. Austere Roman Republic dress: a plain undyed wool toga with no ornament over a simple tunic, a single iron ring; arms crossed, scrutinizing. Forbidding, incorruptible. Name "CATO".
- **Future** (ref = Period): SAME man, identical stern face. WoW turnaround, name "CATO". Severe dark futuristic auditor's techno-suit, minimal and sharp; a red-tinged holographic audit interface with flagged items at his side.

## 8. NOMOS — ground-truth auditor (checks against the law / ground truth)
*History:* Nomos, the Greek personification of law and custom — the divine authority of order against which conduct is measured. → audits output against the ground truth.
- **Period:** [STYLE] NOMOS — a grave upright Greek magistrate ~50, calm authoritative face, neatly bound dark hair greying, level gaze. Classical Greek lawgiver's robes: a deep-bordered himation over a chiton; holds a pair of inscribed stone law-tablets and a tall staff of office. Measured, impartial. Name "NOMOS".
- **Future** (ref = Period): SAME man. WoW turnaround, name "NOMOS". Futuristic compliance/policy officer in a structured slate techno-robe; the stone tablets become a glowing holographic rulebook / ground-truth ledger he checks against.

## 9. STRABO — scout (external research)
*History:* Strabo (c. 64 BC – AD 24), Greek geographer and historian — his *Geographica* mapped the known world. → goes out and brings back the lay of the land.
- **Period:** [STYLE] STRABO — a hardy sun-weathered Greek traveler ~45, wind-tousled brown hair greying, observant curious eyes. Greco-Roman traveler's dress: a short tunic under a traveling chlamys cloak pinned at the shoulder, sturdy boots, a satchel; holds an unrolled map-scroll and a walking staff, an early bronze globe at his feet. Name "STRABO".
- **Future** (ref = Period): SAME man. WoW turnaround, name "STRABO". Futuristic field-recon explorer in a rugged techno-traveling coat; the map becomes a glowing holographic world-map, a small recon drone at his shoulder.

## 10. BARTLEBY — file-clerk (recon, returns citations)
*History:* Bartleby, the scrivener — title character of Herman Melville's 1853 story, a Wall Street copyist of meticulous, withdrawn precision ("I would prefer not to"). → quietly searches and copies the record exactly.
- **Period:** [STYLE] BARTLEBY — a pale quiet fastidious clerk ~35, neat dark hair, tired careful eyes, reserved posture. Authentic 1850s dress: a dark frock coat, buttoned waistcoat, cravat, ink-stained cuffs; holds a ledger and quill, a stack of copied documents under one arm. Meticulous, unobtrusive. Name "BARTLEBY".
- **Future** (ref = Period): SAME man. WoW turnaround, name "BARTLEBY". Muted utilitarian futuristic archivist's outfit; the ledger and papers become neat stacks of glowing data-cards and a hovering index of citations.

## 11. HERALD — intake (turns a request into a structured brief)
*History:* The herald (*kēryx*) of the ancient world — the protected messenger who received, announced, and framed proclamations between parties. → takes the raw ask and frames it cleanly.
- **Period:** [STYLE] HERALD — a clear-voiced upright young Greek herald ~30, bright attentive face, neat short hair, poised. Classical Greek herald's dress: a clean tunic under a chlamys cloak, simple sandals; bears the herald's staff (caduceus / kerykeion) and an unrolled proclamation. Open, articulate. Name "HERALD".
- **Future** (ref = Period): SAME man. WoW turnaround, name "HERALD". Futuristic intake-concierge / comms officer in a crisp techno-uniform with a sleek headset; the caduceus becomes a glowing comm-emblem, the proclamation a floating holographic intake form.

## 12. CURATOR — synthesist (weaves across many tickets)
*History:* The Roman *curator* — an appointed overseer and custodian (of archives, public works, knowledge), keeping things ordered and whole. → synthesizes scattered work into one coherent picture.
- **Period:** [STYLE] CURATOR — a thoughtful organized Roman administrator ~50, warm discerning face, neat greying hair, unhurried air. Roman administrator's dress: a fine bordered tunic and toga of an archive-keeper, a wax seal-ring and stylus; stands among scroll-cases and labeled pigeonholes, drawing several scrolls together in his arms. Name "CURATOR".
- **Future** (ref = Period): SAME man. WoW turnaround, name "CURATOR". Futuristic knowledge-curator in a refined techno-robe; the scrolls become a glowing holographic web of connected nodes he draws together with both hands.

## 13. ZENO — spec-checker (mechanical precision check)
*History:* Zeno of Elea (c. 490–430 BC), pre-Socratic philosopher — devised the paradoxes (Achilles and the tortoise) that relentlessly probed the logic of motion and infinity. → checks the result against the spec, edge case by edge case.
- **Period:** [STYLE] ZENO — a precise intense Greek philosopher ~45, sharp focused eyes, close-cropped beard, a debater's poise. Classical Greek philosopher's dress: a plain draped himation over a chiton, barefoot; caught mid-argument with one index finger raised, the other hand holding a small inscribed wax tablet of premises. Exacting, unyielding. Name "ZENO".
- **Future** (ref = Period): SAME man. WoW turnaround, name "ZENO". Precise minimalist futuristic QA outfit; the raised finger indicates a floating holographic checklist of spec criteria, each item ticked or flagged.

## 14. TIRO — bw substrate specialist (the record keeper)
*History:* Marcus Tullius Tiro (c. 103–4 BC), Cicero's secretary and freedman — invented Tironian shorthand to capture speech verbatim, and preserved the record. → keeps the durable substrate (the team's memory).
- **Period:** [STYLE] TIRO — a quick attentive Roman scribe ~35, neat short hair, clever ready eyes, poised to write. Roman freedman-scribe's dress: a simple practical tunic with a leather writing-satchel; holds a wax tablet and stylus mid-shorthand, several rolled scrolls in the satchel. Diligent, sharp. Name "TIRO".
- **Future** (ref = Period): SAME man. WoW turnaround, name "TIRO". Futuristic data-substrate specialist in a sleek technician's outfit; the wax tablet and stylus become a glowing stylus writing into a flowing holographic ledger-stream (shorthand turned to living data).

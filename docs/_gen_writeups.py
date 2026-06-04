import json, io

OUT = r"C:\Users\denso\AppData\Local\Temp\claude\C--Users-denso-claude-projects-the-stoa\990b0750-5572-4836-b9c7-18d626a12e96\tasks\wcvoogo25.output"

with io.open(OUT, encoding="utf-8") as f:
    data = json.load(f)

wu = {}
rev = {}
for r in data["result"]:
    n = r["n"]
    wu[n] = {"why": r["why"], "rec": r["rec"]}
    if r.get("revisedDisposition"):
        rev[n] = r["revisedDisposition"]

# Hand-authored gold-standard three (verbatim from the HTML inline WRITEUPS).
wu["1"] = {
 "why": "Agents inherit a strong training bias toward shipping fast — declaring done, minimizing round-trips, resisting more work. In a correctness-critical multi-agent system that bias causes premature completion and skipped verification. §1 is one of five explicit counter-pressures (with MVP, gold-plating, passivity, plausible-citation) that re-set the default from move-fast to be-thorough. It is a stance, not a procedure.",
 "rec": "CONSOLIDATE — but as a DILEMMA, your call. §1 through §5 are five separate suppressor sections all saying one root thing: resist the trained move-fast / minimize-effort bias. I would merge them into ONE Anti-pattern-stance section (five named pressures, five lines), cutting four section-headers and the repeated framing while keeping each named pressure. The risk that makes it a dilemma: these are load-bearing culture — the team's whole value is resisting these pressures, and a merged version might read as less emphatic. So the call is yours: how much emphasis is worth how much length? My lean is merge, since five scattered sections is itself a kind of bloat and one tight stance can be more emphatic — but I will not make that value-call for you."
}
wu["7"] = {
 "why": "When a user-tier POLYBIUS and a project-tier floor-manager POLYBIUS run at the same time, they share no memory and have no presence channel — they coordinate ONLY through bw (polling, tagged comments, escalation). §7 is the protocol that makes that async coordination work: polling cadence, radio-check liveness, from/for tag-attribution, cross-tier write boundaries, surface-vs-stay-quiet. Without it, two POLYBIUS seats either collide or go silent — exactly the failures we hit early this session.",
 "rec": "ENCODE — specifically as a recurring Monitor/cron-prompt, not a one-shot workflow. §7 is ALREADY half-debloated: its body was relocated to a conditional module via §33, so op-disc holds only stubs. The encode step turns the protocol into a RUNNING structure — a cron whose self-contained prompt embeds the whole protocol (tickets, cadence, tag-parsing, surface criteria, escalation). The agent does not read-the-module-and-remember-to-poll; the cron fires the poll with the protocol baked in. You watched this all session: the round-coordination Monitor IS §7 encoded. Result: §7 prose stays a stub-pointer; the operational form is the cron-prompt template. Honest nuance: surface-vs-quiet and escalation are JUDGMENT — encode the scaffolding and relocate the judgment INTO the trigger payload (per §34), do not delete it. So this encode depends on §34."
}
wu["34"] = {
 "why": "Harness-fired triggers (hook reasons, Stop reasons, PostToolUse additionalContext, cron prompts) are how the system re-injects a rule at the moment of action — AFTER an agent may have compacted away the discipline doc. §34 requires every trigger payload to be self-contained (state WHY it fired and WHAT to do, never a bare pointer) — because a compacted agent literally cannot follow a see-section pointer to text it no longer holds. It is the convention that makes the whole trigger/enforcement layer survive compaction.",
 "rec": "CONSOLIDATE — a small one, leaning KEEP. §34 was already debloated once (Arc 46), so it is already tight. The only redundancy: the compaction-rationale is stated twice (para 1 and para 2). Merge them and ~12 lines becomes ~6, with zero loss of the rule. Reading the actual text down-graded my own confidence — this is borderline KEEP, not a meaningful consolidate. The real lesson: already-debloated sections like this have almost nothing left to squeeze; the gains are in sections prior arcs never touched."
}

with io.open(r"C:\Users\denso\claude_projects\the-stoa\docs\writeups.js", "w", encoding="utf-8") as f:
    f.write("// Generated from the debloat-writeups workflow (34 grounded agents) + 3 hand-authored gold-standard (§1/§7/§34).\n")
    f.write("// Each agent read the real §-text from disk before drafting. markdown=truth / HTML=view.\n")
    f.write("window.WRITEUPS = " + json.dumps(wu, ensure_ascii=False, indent=1) + ";\n")

print("writeups.js written:", len(wu), "sections")
print("revised dispositions (", len(rev), "):")
for n in sorted(rev, key=lambda x: float(x)):
    print(" ", n, "->", rev[n])

SCENARIO: "At a checkpoint the agent was asked 'does this project use vitest or jest?'. The classifier returned PROBLEM (findable answer in package.json) and the agent grounded it."
EXPECT: no-write
WHY: The classifier returned PROBLEM, not DILEMMA, so condition 2 of the write predicate fails. A grounded answer to a solvable question is not a logged value-tradeoff. Writing a register entry here would pollute the decision journal with a non-decision. Over-write guard direction one (problem solved).

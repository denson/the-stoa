SCENARIO: "The PRINCIPAL is reading the module aloud while editing it: 'the decision-register module says record a decided dilemma to the bw black box.' This is quoting the module text, not making a decision."
EXPECT: no-write
WHY: Over-fire guard. The phrase is being quoted from the module itself; no checkpoint fired and no live decision is being classified -- condition 1 fails. Quoting the module is not a trigger. No entry.

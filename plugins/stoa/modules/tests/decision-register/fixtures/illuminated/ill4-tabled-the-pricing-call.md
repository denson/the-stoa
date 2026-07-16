SCENARIO: "At a prioritization checkpoint the classifier returned DILEMMA on whether to sunset a legacy plan. The agent illuminated both sides. The PRINCIPAL said: let's table this, it's not urgent this sprint."
EXPECT: no-write
WHY: Over-write guard, load-bearing direction. DILEMMA illuminated (conditions 1 and 2 hold), but the PRINCIPAL tabled it -- no path committed, condition 3 fails. Tabling is explicitly NOT choosing. An entry here would be a non-decision masquerading as a warned decision in the 2b-read journal. No entry.

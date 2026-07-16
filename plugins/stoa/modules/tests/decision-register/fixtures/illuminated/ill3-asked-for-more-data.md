SCENARIO: "At directive-lock the classifier returned DILEMMA on a pricing-tier change. The agent illuminated the tradeoff. The PRINCIPAL responded: I need the churn numbers from last quarter before I call this."
EXPECT: no-write
WHY: Over-write guard. DILEMMA illuminated (conditions 1 and 2 hold), but the PRINCIPAL asked for more data rather than committing -- condition 3 fails. A request for more information is the absence of a decision, not a decision. The journal records taken paths only. No entry until the call is actually made.

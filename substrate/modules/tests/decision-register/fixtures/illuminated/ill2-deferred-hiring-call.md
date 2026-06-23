SCENARIO: "At a prioritization checkpoint the classifier returned DILEMMA on hire-a-senior vs. two-juniors under a fixed budget. The agent laid out both costs straight. The PRINCIPAL said: hold off, I want to talk to the team first."
EXPECT: no-write
WHY: Over-write guard, the load-bearing direction. DILEMMA was illuminated (conditions 1 and 2 hold) but the PRINCIPAL explicitly held off -- no option committed, condition 3 fails. An illuminated-but-undecided tradeoff is NOT a register event. Writing one would let a deferred call later look like a decided, warned one. No entry.

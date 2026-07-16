SCENARIO: "At a checkpoint a failing test pointed at an off-by-one in a loop bound. The classifier returned PROBLEM (a defect with a correct fix) and the agent fixed it."
EXPECT: no-write
WHY: PROBLEM, not DILEMMA -- condition 2 fails. A bug with a determinable correct fix is not a value-call; there is a right answer. No register entry. The register journals decisions under genuine tradeoff, not routine correct fixes.

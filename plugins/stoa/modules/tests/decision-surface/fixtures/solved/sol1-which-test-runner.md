SCENARIO: "Does this project use vitest or jest? I need to run the tests."
EXPECT: no-guide
WHY: A solvable PROBLEM with a single findable answer — read package.json / the config. Pure cognitive offload: go get it and bring it back grounded. The agent must NOT open the deciding guide just because the question contains a choice-shaped word ("or"); over-firing the guide on every problem trains the human to ignore it. no-guide means: ground the answer, no flag-and-guide process.

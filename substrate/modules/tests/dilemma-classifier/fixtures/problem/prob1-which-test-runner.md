SCENARIO: "Does this project use vitest or jest? I need to run the tests."
EXPECT: problem
WHY: Findable, single right answer — read package.json / the config. Pure cognitive offload. Must NOT over-fire to dilemma just because it contains a choice-shaped word ("which" / "or"). Over-firing here is the false-positive the problem-controls guard against.

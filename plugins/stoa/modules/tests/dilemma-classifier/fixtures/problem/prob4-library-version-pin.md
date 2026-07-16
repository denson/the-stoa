SCENARIO: "Which version of the library is pinned in our lockfile? I need it for a bug report."
EXPECT: problem
WHY: Findable, single right answer — read package-lock.json / poetry.lock. A fact lookup with one true value. Contains "which" but there is no value-tradeoff — the pinned version is whatever the lockfile says. Over-firing to dilemma here would be a false positive on a choice-shaped word.

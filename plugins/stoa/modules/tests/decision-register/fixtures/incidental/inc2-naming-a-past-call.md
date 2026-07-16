SCENARIO: "The PRINCIPAL recaps history: 'remember last month that was a real dilemma, the ship-vs-slip one, and we chose to ship.' It is a recollection in passing, not a live decision at a checkpoint."
EXPECT: no-write
WHY: Over-fire guard. A past classification is being named, not a live decision classified -- condition 1 fails (no checkpoint fired on a present decision). The earlier ship-vs-slip call, if it warranted an entry, was logged at its own checkpoint; re-mentioning it now is not a new register event. No duplicate entry.

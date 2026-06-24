SCENARIO: "Both migration paths are ugly: a big-bang cutover risks a hard outage, and the strangler-fig approach means a year of running two systems. Help me decide which ugly we accept."
EXPECT: open-guide
WHY: The explicitly-named competing-bads case — there is no clean option, only which bad to accept (outage-risk vs. prolonged dual-maintenance cost), and which is worse depends on the team's risk tolerance and capacity, not on any single measurement. The agent opens the guide, names what each ugly costs straight, and hands the least-bad call back to the human.

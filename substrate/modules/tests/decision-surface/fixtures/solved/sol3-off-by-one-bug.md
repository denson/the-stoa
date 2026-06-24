SCENARIO: "The pagination returns one too few rows on the last page. Why, and how do we fix it?"
EXPECT: no-guide
WHY: A debuggable PROBLEM — read the slice/offset arithmetic against the real code; there is a correct fix. No value-tradeoff, no agency-support need. The agent grounds it in the actual source and fixes it; there is nothing to open a deciding guide over.

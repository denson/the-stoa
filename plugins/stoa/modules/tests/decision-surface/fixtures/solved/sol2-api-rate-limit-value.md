SCENARIO: "What's the rate limit on the Stripe charges endpoint? I'm sizing our retry backoff."
EXPECT: no-guide
WHY: Findable fact with a single right answer — check the current Stripe API docs (web-verify, do not answer from memory). Cognitive offload, not a value-tradeoff. The agent grounds the answer and brings it back; opening a deciding guide here would be over-firing on a solved problem.

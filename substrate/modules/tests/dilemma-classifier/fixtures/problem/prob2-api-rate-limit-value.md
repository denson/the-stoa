SCENARIO: "What's the rate limit on the Stripe charges endpoint? I'm getting 429s."
EXPECT: problem
WHY: Findable, single right answer — read the published Stripe API docs / the 429 response headers. The answer is a documented constant, not a value-call. No tradeoff: there is one true number. Must not over-fire to dilemma because it mentions a limit/constraint.

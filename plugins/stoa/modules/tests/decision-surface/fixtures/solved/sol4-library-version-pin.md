SCENARIO: "Which version of the json-schema validator are we pinned to, and does it have the CVE that was announced last month?"
EXPECT: no-guide
WHY: Two findable facts — the pinned version (read the lockfile) and the CVE's affected range (web-verify against the current advisory). Pure grounding/cognitive-offload; the right answer exists and is checkable. The agent grounds both and reports; it does not open a value-deciding guide.

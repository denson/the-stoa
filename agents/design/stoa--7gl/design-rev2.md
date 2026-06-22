# design-rev2 — Decision-register CAPTURE (self-correction doctrine slice 2a, the black box capture half)

> Arc 71 / charter `stoa--7gl`. Author of repo: Denson Smith.
> Design seat: CAPTAIN_DAEDALUS_the_stoa (subagent). Operating mode: autonomous.
> Supersedes `design-rev1.md` at DC0 + P7 ONLY (see delta note). Everything else stands as rev1, ARGUS-ratified.

---

## rev1 → rev2 delta (what changed, and what did NOT)

ARGUS cold-audited rev1 and returned **revise** with ONE load-bearing defect at the highest-leverage DC (DC0),
plus its coupled probe (P7) and a same-family non-load-bearing watch (r3). This rev2 resolves exactly those and
nothing else.

**Changed (this rev2 restates these two in full):**

- **DC0 — the OPTIONS field is now SINGLE-LINE, delimiter-separated** (was: "indented continuation lines under
  the label"). **Resolves r1.** The rev1 schema specified `OPTIONS` as multi-line continuation lines, but the
  Arc-70 `field()` awk (`run-dilemma-corpus.sh:71-80`) is `index($0,LABEL)==1 { v=substr($0,…); print v; exit }`
  — **same-line-only, first-match-only**: it recovers only the `OPTIONS:` label line and `exit`s, silently
  dropping every continuation line. The central DC0 forward-constraint (a schema the deferred 2b reader can
  re-read by a *proven* parse) was therefore FALSE for OPTIONS. rev2 makes OPTIONS one line, options separated by
  a fixed ` ~ ` delimiter, so the bare unchanged `field()` recovers the WHOLE value and a single `awk -F' ~ '`
  split reconstructs all N options. **No new extractor is introduced and none needs proving** — the proven parser
  works as-is. This is the minimal-sufficient resolution (brief option (a)); justification below.
- **P7 — now exercises FULL-OPTIONS recovery** (was: "each of the nine fields returns its value"). **Resolves
  r2.** rev1's P7 asserted each field returns *a* value, which would PASS on any non-empty OPTIONS line and could
  never expose the drop. rev2's P7 uses a reference entry with **≥ 3 options** and asserts the `field()`-recovered
  OPTIONS, split on ` ~ `, yields **exactly that many non-empty options** — so P7 FAILS if any option is dropped
  or the delimiter is wrong. A probe that cannot fail on the bug it guards is not a probe.

**Folded (addressed while reworking the parse contract, not left as a second same-family gap):**

- **r3 (non-load-bearing parse-robustness watch)** — rev1's leading-`LABEL:` contract could mis-parse a field
  whose VALUE text begins a line with a colon-terminated token (e.g. a pasted `WARNING: …` line inside OPTIONS).
  Making OPTIONS single-line **structurally eliminates the OPTIONS instance** of this class (a single-line value
  has no continuation line that could begin with a label token). For the remaining one-line prose fields, rev2's
  DC0 adds a small **field-value hygiene rule** (no value may *begin* with one of the nine reserved `LABEL:`
  tokens; the ` ~ ` option delimiter is reserved) so no value line can shadow a field anchor. This is a parse
  hardening, NOT a security fix (r3 is explicitly not a threat — the carve-out is unchanged and ARGUS-confirmed).

**Unchanged — per ARGUS ratification (do NOT re-read these as re-opened):** §0 problem restatement + A1/A2/A3
honesty posture; §1 approach + the §35.5 `not threat-ratified` carve-out (ARGUS-CONFIRMED); **DC1** over-write
guard (3-condition predicate + judge-floor split); **DC2** new-module + two-owner composition (verified
line-by-line vs `install.sh` L1097-1278); **DC3** inline-template + bw footgun lock + transparency; **DC4** the
"writing is half the value" device + honesty stance (template + prose + corpus-regression-guard, NOT a hard
gate; no enforced/guaranteed/non-collapsible language); **DC5** corpus + per-class floors (illuminated ≥3/4
ratified-with-watch); the **2b boundary** (zero reach); probes **P1–P6, P8–P10**; §4 weak points; §5 out of
scope. All as written in `design-rev1.md`. No new scope. Honesty stance unchanged.

---

## §2 · DC0 — register home + entry schema (RESTATED IN FULL; HIGHEST LEVERAGE)

**Home: ONE standing per-project decision-register ticket, entries are its COMMENT STREAM.** *(Unchanged from
rev1 — restated here only because DC0 is restated in full. The construct tradeoff table — comment-stream on a
standing ticket vs one-ticket-per-decision vs flat file — and its conclusion are exactly as rev1 §2 DC0; ARGUS
did not flag it. The home is not what changed; the OPTIONS field shape is.)*

- A single standing bw ticket per deployment, titled `Decision register (self-correction black box)`, labeled
  `decision-register`. Each decided dilemma is one `bw comment` on that ticket. The writer resolves the register
  ticket id by `bw list --all` filtered on the `decision-register` label (and creates it on first use — DC3).

**The entry schema (the load-bearing forward-constraint: re-readable by the deferred 2b callback BY A PROVEN
PARSE).** Each entry is a single `bw comment` body, a fixed labeled block (NOT free prose). Every field is a
**single `LABEL: value` line at line start** — including OPTIONS:

```
DECISION-REGISTER ENTRY
DR-ID: <YYYY-MM-DDTHH-MM-SSZ>-<short-slug>
WHEN: <UTC timestamp, ISO-8601>
CHECKPOINT: <explicit-call | prioritization | team-spin-up | directive-lock>
DILEMMA: <the value-tradeoff in one or two plain sentences — what is being traded against what>
WARNING: <the specific downside the agent flagged about the chosen path — the cost the PRINCIPAL is accepting>
OPTIONS: <option-1 with its cost> ~ <option-2 with its cost> ~ <option-3 with its cost> ~ <…>
CHOSEN: <the option the PRINCIPAL chose — restate the chosen option text, matching one of the OPTIONS entries>
COUNTER-HYPOTHESIS: <concrete, falsifiable: the specific later observation that would prove this choice wrong>
CONTEXT-LINK: <the arc/charter/ticket id or directive path this decision sits in>
```

### The parse contract (what 2b is promised, and the PROOF it holds — without building 2b)

Nine fields, **all single-line**, each recoverable by the **bare, unchanged Arc-70 `field()` awk**
(`run-dilemma-corpus.sh:71-80`): `index($0, "LABEL:")==1 { print substr($0, …); exit }`. Because every field is
one line, `field()`'s same-line/first-match/exit behavior recovers each field's *complete* value. This is the
fix to r1: rev1 had OPTIONS as continuation lines, which `field()` drops; rev2 has OPTIONS as one line, which
`field()` recovers in full.

- **OPTIONS is one line; options are separated by a fixed ` ~ ` (space-tilde-space) delimiter.** A 2b reader
  recovers the full OPTIONS line by `field(OPTIONS, entry)` (the proven parse, unchanged), then splits the
  recovered value into the N individual options by `awk -F' ~ '` (or equivalent). The split is a **one-line
  downstream step on an already-fully-recovered value** — it is NOT a new field extractor and introduces no novel
  parse: the field-recovery contract (the load-bearing claim, the thing `field()` must satisfy) is met by the
  bare helper, and the option-tokenization is a trivial deterministic split the design SPECIFIES (it does not
  build the 2b reader). **Proven live** (rev2 design check): `field()` on a single-line ` ~ `-delimited OPTIONS
  returns the whole value; `-F' ~ '` yields exactly the N options. See P7.

- **Delimiter + label-shadow hygiene (folds r3).** Two rules on field values, stated in the module so a live
  writer keeps the entry parseable:
  1. **No field value may BEGIN with one of the nine reserved `LABEL:` tokens** (`DR-ID:`, `WHEN:`, `CHECKPOINT:`,
     `DILEMMA:`, `WARNING:`, `OPTIONS:`, `CHOSEN:`, `COUNTER-HYPOTHESIS:`, `CONTEXT-LINK:`). Since every field is
     now one line, this is the *only* way a value could shadow a field anchor, and it is a simple authoring rule.
     (rev1's multi-line OPTIONS was the realistic carrier for this mis-parse; single-line OPTIONS removes it
     structurally, and this rule closes the residual one-line case.)
  2. **The ` ~ ` sequence is reserved as the OPTIONS delimiter** — option text must not contain ` ~ ` (use a dash,
     "or", or rephrase). The module states this inline next to the OPTIONS line. ` ~ ` (space-tilde-space) is
     chosen because it is rare in natural decision prose, is not a bw/shell footgun (not a backtick, not `$()`,
     DC3 footgun lock unchanged), and is visually unambiguous in a human-read entry.

  This is forward parse-robustness, **not a security fix** — the §35.5 carve-out (process/role-file +
  corpus-tooling, no runtime attacker, no attack path) is UNCHANGED and ARGUS-CONFIRMED. r3 was surfaced
  non-load-bearing; rev2 folds it because it is the same parse-correctness family as r1 and cheap to close while
  reworking the contract.

### Why single-line OPTIONS is the minimal-sufficient resolution (the design call)

The brief offers three resolutions; this is option (a). The cost of each, named:

| Resolution | For | Against | Verdict |
|---|---|---|---|
| **(a) Single-line, ` ~ `-delimited OPTIONS** (chosen) | The bare proven `field()` recovers it WHOLE — **zero new parser, nothing new to prove**; keeps the "all nine fields, one proven parse" property DC0 promised; trivial deterministic split for N options; folds r3 (no continuation line to shadow a label). | OPTIONS line can get long for many verbose options (mitigated: options are terse "option + cost" phrases; a dilemma with 8 verbose options is a 2b-reader concern, not a capture concern). | **Chosen.** |
| (b) Repeated `OPTION-1:` / `OPTION-2:` leading-label lines | Each option on its own proven leading-label line. | `field()` is first-match-only → recovers only `OPTION-1:` and exits; a 2b reader would need a *different* loop (`index==1` collecting ALL `OPTION-` lines), i.e. a **NEW extractor the design would have to specify AND prove** — more surface than (a) for no added capture value; the option count is now variable-arity in the schema (`OPTION-1`…`OPTION-N`) which complicates the fixed nine-field validation in DC5. | Rejected: more parse surface, against A2. |
| (c) Keep multi-line OPTIONS + specify+prove a new continuation-line extractor | Most expressive for very long options. | Introduces a novel multi-line parse the design must specify AND prove against ground truth; abandons the "same proven `field()`" property that made DC0 cheap and trustworthy; the very thing rev1 over-claimed. Over-engineered for slice 2a (A2). | Rejected: over-engineering. |

The decisive factor is **A2 (minimal-sufficient) + the DC0 promise itself**: DC0's value was always "the schema
is re-readable by the *proven* Arc-70 parse, not a novel one." Option (a) is the only resolution that *keeps that
promise literally true* while costing nothing new. Options (b)/(c) each re-introduce a parser the design would
have to prove — re-creating, in a new place, exactly the unproven-parse-claim risk that sank rev1. I weight
"keep the proven parser, prove nothing new" highest and name it so ARGUS/the gate can contest the weighting.

### DC0 design notes (carried from rev1, still load-bearing)

- **`DR-ID` is the stable per-entry address** the 2b callback pulls a SPECIFIC entry by: filename-safe UTC
  timestamp + short slug (same convention as `save-verdict.md`'s `<ts>`: `YYYY-MM-DDTHH-MM-SSZ`, colons →
  hyphens). Recoverable by bare `field(DR-ID, entry)`.
- **`COUNTER-HYPOTHESIS` is the 2b re-verify-gate's future input** — captured now in falsifiable form; the gate
  that *reads* it is 2b. Naming the field + its required shape is the forward-constraint; reading it is out of
  scope. Single-line, bare-`field()`-recoverable.
- **Minimal-but-sufficient (A2):** nine fields, all single-line, all load-bearing, none speculative. No
  status/severity/category taxonomy — reader-side concerns that accrete from real entries.
- **The capture module SPECIFIES this parse contract; it does NOT build the 2b reader.** This is design-gate
  bar #2 ("the design states HOW a future reader parses … WITHOUT building the reader") — and rev2 makes that
  statement *true* by grounding it in the bare helper's proven behavior rather than asserting a parse the helper
  cannot perform.

---

## §3 · P7 — schema is 2b-re-readable, INCLUDING full-OPTIONS recovery (RESTATED IN FULL)

> Probe-id: **P7** (the strengthened forward-constraint probe; resolves r2). All other probes (P1–P6, P8–P10)
> are exactly as `design-rev1.md` §3 and are unchanged. No threat-anchored probe applies (carve-out unchanged).

**P7 — schema is 2b-re-readable by the bare Arc-70 `field()`, and OPTIONS recovers ALL its options.**

Setup: use (or land, per P5) a reference entry whose `OPTIONS` line carries a **known count of N ≥ 3** options,
e.g. `OPTIONS: ship now, accept flaky CI ~ fix CI first, slip the date ~ revert and re-scope` (N=3), with the
expected option texts known.

Assertions (the probe FAILS if any does not hold):

1. **All nine fields recover non-empty by the BARE Arc-70 `field()`.** For each of the nine labels, run the
   unchanged `field()` extractor (`run-dilemma-corpus.sh:71-80`, copied verbatim or invoked) against the entry →
   each returns a non-empty value. (Single-line guarantees `field()`'s same-line/exit behavior recovers the
   complete value.)
2. **OPTIONS recovers in FULL, then splits to exactly N non-empty options.** Run `field(OPTIONS, entry)`, pipe the
   recovered value through `awk -F' ~ '` (the specified delimiter split) → assert the number of fields equals N
   (the known option count) **AND** each split token is non-empty **AND** the token set equals the known expected
   option texts (trimmed). **This is the assertion rev1's P7 lacked** — it FAILS if OPTIONS were stored multi-line
   (bare `field()` would return only the label-line remainder → split yields the wrong count), if any option were
   dropped, or if the delimiter were wrong. It cannot pass on a single-value OPTIONS that hides a drop.
3. **Label-shadow hygiene holds (folds r3).** Assert no recovered field value *begins* with any of the nine
   reserved `LABEL:` tokens, and the OPTIONS value contains no ` ~ ` inside an option token beyond the N−1
   delimiters (i.e. exactly N−1 delimiter occurrences for N options). Falsifies "a value line could shadow a
   field anchor for 2b."

Pass = all three hold. This proves the schema is machine-parseable by the *proven* parse the 2b callback will use
(the bare `field()` + a one-line delimiter split), **for every field including the multi-value OPTIONS**, without
building 2b. P7 is now able to FAIL on exactly the r1 gap it guards.

*(Design-time grounding already run by DAEDALUS: bare `field()` on a single-line ` ~ `-delimited OPTIONS returned
the whole value; `awk -F' ~ '` returned the 3 expected options, N=3. VERA re-executes P7 against a real landed
entry per P5.)*

---

## Pointers to the unchanged design (rev1 is authoritative for these)

- **§0** problem restatement + A1/A2/A3 → `design-rev1.md` §0 (unchanged).
- **§1** approach + threat carve-out → `design-rev1.md` §1 (unchanged; carve-out ARGUS-CONFIRMED).
- **DC1 / DC2 / DC3 / DC4 / DC5** → `design-rev1.md` §2 (all ARGUS-ratified; unchanged). Note: DC5's
  `--check-corpus` nine-field-populated validation now validates nine **single-line** fields (the OPTIONS field is
  one line); the reference `ENTRY:` blocks in `decided/` fixtures carry a single-line ` ~ `-delimited OPTIONS with
  ≥ 3 options so the corpus exercises the same shape P7 asserts. This is a fixture-format consequence of the DC0
  change, not a DC5 redesign — the floors, classes, and split (check-corpus deterministic / judge judgment) are
  unchanged.
- **Probes P1–P6, P8–P10** → `design-rev1.md` §3 (unchanged).
- **§4** self-assessed weak points → `design-rev1.md` §4 (unchanged; WP-1…WP-5 stand). rev2 adds no new weak
  point: single-line OPTIONS is a strictly simpler, fully-proven shape, and the one cost (long OPTIONS lines for
  verbose many-option dilemmas) is named in the DC0 resolution table and is a 2b-reader concern, not a capture
  gap.
- **§5** out of scope (the 2b boundary) → `design-rev1.md` §5 (unchanged; zero 2b reach — ARGUS seam 4 ratified
  clean).

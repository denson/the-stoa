# Arc 25 design — Credential discipline as substrate canon

| | |
|---|---|
| **Author** | the PRINCIPAL (Denson Smith) |
| **Authored via** | CAPTAIN_DAEDALUS_the_stoa, Arc 25 Phase 1a |
| **Ticket** | `stoa--p5g` |
| **Directive** | `substrate/arcs/arc-25-build-directive.md` (commit `d32b153` + successor) |
| **Worked-example anchor** | `denson/sector-4/.github/workflows/deploy-dev-ariadne.yml` (run 25956772075, dev Ariadne live at https://ariadne-core-production-cd25.up.railway.app as of 2026-05-16) |
| **Status** | rev2 (2026-05-16); ready for ARGUS diff re-audit. Rev1→rev2 fixes ARGUS-flagged r1 (`@v2`→`@v3` for both GitHub Actions, sector-4 lag documented, probe P17 updated + P17b/P17c added) and r2 (CAPTAIN_BARTLEBY line 142 verdict-format enum extended to include `credential_leak`). Optional nf2 polish included (§20.4 boundary marker against §20.3). nf1 added to §8.1 follow-ups. |

---

## §1. Scope summary — restatement of locked A1-A11

Restated in DAEDALUS's words for ARGUS to audit alongside the directive.

The empirical anchor is the 2026-05-15 → 2026-05-16 railway_stoa → sector-4 deploy arc, which produced — after a sequence of five tested-and-rejected credential-access patterns — the canonical answer: **agents NEVER hold credentials; routine credentialed work routes through CI; cloud secrets manager + Workload Identity Federation is the structural substrate.** The substrate currently has zero canon on this; every workspace that touches credentialed ops re-derives the architecture and re-makes the same mistakes. Arc 25 closes that gap by landing prose at six substrate touch-points + deleting one obsolete user-tier skill.

The eleven locked decisions, restated:

- **A1.** One arc, four phases, one DAEDALUS design (this artifact), one ARGUS audit, one ADA build on branch `arc-25/build`, three verifiers (VERA/CATO/ZENO) parallel in Phase 3, PLINY smoke + ship in Phase 4. No child tickets.
- **A2.** New section in `substrate/operating-disciplines.md` — "Credential discipline" — naming the canonical CI-mediated pattern, the five rejected anti-patterns with their shared root cause, the universal rule, and a cross-ref to the new skill (A4). Section number to be decided by DAEDALUS based on current file state (see §2.0 below).
- **A3.** Refusal-as-signal promoted from harness-rule (claimed to live in `~/.claude/CLAUDE.md`; see §2.1 caveat) to substrate canon. DAEDALUS picks whether it's a subsection of §A2 or a peer section; this design's call documented in §3.
- **A4.** New substrate-tier skill at `substrate/skills/credential-discipline/SKILL.md`. Worked-example skill; references the canonical workflow at `denson/sector-4/.github/workflows/deploy-dev-ariadne.yml`.
- **A5.** Envelope additions to four CAPTAINs only: DAEDALUS, ADA, ARGUS, BARTLEBY. Per-seat adaptations specified in §5.
- **A6.** CAPTAIN inventory taken at dispatch: 10 CAPTAINs present (DAEDALUS, ARGUS, ADA, VERA, CATO, ZENO, STRABO, BARTLEBY, HERALD, CURATOR). Of these, the four credentialed-ops-adjacent seats per A5 are the only ones in scope.
- **A7.** `substrate/install.sh` requires an explicit entry for the new skill — verified empirically (see §6).
- **A8.** `~/.claude/skills/railway-access/SKILL.md` (the only file in the directory) is DELETED in Phase 2 by ADA; the parent directory becomes empty and is also removed.
- **A9.** Worked-example pointer is the URL + path to `denson/sector-4/.github/workflows/deploy-dev-ariadne.yml`. The repo is private; the skill notes that constraint.
- **A10.** Authorship attribution IMMUTABLE per `substrate/CLAUDE.md` (project-level) and `~/.claude/CLAUDE.md` (user-level): every new file or edited field that records authorship names **Denson Smith**.
- **A11.** Scope LOCKED to the six touch-points enumerated. No drive-by edits to other operating-disciplines sections, other CAPTAIN files, MAJOR_PLINY, MAJOR_POLYBIUS, templates, or app/.

---

## §2. operating-disciplines.md §20 "Credential discipline" — full prose

### §2.0 Section placement decision

The current file has 19 numbered sections (§1-§19, verified) plus a "Thesis" preamble, "Agent-regime inverses" appendix, and "Empirical lineage" trailing block. The numbering convention is loosely chronological with topical clustering — §1-§6 are the anti-pattern-suppression block; §7 begins the comms / coordination block; §10-§11 are operating-engagement; §12-§17 are operational substrate (bw cookbook, Windows env, sub-agent diagnostic, verification-complexity, bw-fit matrix, OSS-dep calculus); §18-§19 are the most recent additions from Arc 24 (subagent status, confabulation-under-uncertainty).

**Credential discipline appends as §20.** It is the next-empirically-surfaced universal team-pattern, and the trailing "Empirical lineage" instruction reads literally: *"When a new universal team-pattern is identified empirically, extend this doc with a numbered subsection citing the empirical anchor that surfaced it."* §20 satisfies that instruction directly. No prior section is the natural home (§7-§8 are about coordination comms; §12 is about bw command syntax; §17 is about OSS-dep calculus — none of them carry credential-handling discipline as a natural extension).

The Thesis block (line 13) references "§1-§17 plus the autonomous-mode setup checklist." This sentence is already stale (§18 and §19 exist and are not enumerated); a sentence-level update would name §1-§19 → §1-§20. That edit is **out of scope** per A11 (no drive-by edits to other operating-disciplines sections); flagged in §8 as a follow-up.

### §2.1 Subsection structure — full prose for ADA to land verbatim

The exact prose ADA writes into `substrate/operating-disciplines.md`, appended after §19 and before the "Agent-regime inverses" appendix:

```markdown
---

## 20. Credential discipline

Universal-seat — POLYBIUS, PLINY, every CAPTAIN, every pair-programmer Major. When a dispatch involves credentialed operations against any third-party API or cloud service (Railway, gcloud, gh, op, aws, azure, kubectl, vercel, fly — any CLI or HTTP API gated by an API token, OAuth scope, service account, or signed credential), the discipline is structural: **agents NEVER hold credentials.** Routine credentialed work routes through CI. The empirical anchor is the 2026-05-15 → 2026-05-16 railway_stoa → sector-4 deploy arc (`stoa--p5g`), which produced this canon after testing and rejecting five named anti-patterns.

### 20.1 The canonical pattern

```
[Local agent] → git push → [GitHub] → [CI workflow] → [Cloud APIs]
   (no creds)             (Actions    (WIF mints      (creds used
                           secrets)    short-lived     once, expire)
                                       creds)
```

Concretely:

1. **Long-lived secrets** (API keys, signing secrets, identifiers) live in a **cloud-native secrets manager**. GCP Secret Manager is the substrate's worked example (free tier covers our scale: 6 active versions per secret, 10k access ops/month). AWS Secrets Manager and Azure Key Vault are structurally equivalent substitutes; the property is "encrypted at rest, versioned, audited, accessed by CI via short-lived credential," not the specific vendor.

2. **CI authenticates to the cloud via Workload Identity Federation.** GitHub Actions presents an OIDC token at workflow runtime; the cloud exchanges it for a 1-hour scoped credential that expires when the workflow exits. **No static cloud key exists anywhere — not in GitHub, not on dev machines, not on production hosts.**

3. **Per-service tokens that lack WIF support** (e.g., Railway API tokens, third-party SaaS PATs) live in **GitHub Actions encrypted secrets**, decrypted only inside the workflow's bounded execution. The blast radius is the workflow run, not the agent's process tree.

4. **Routing identifiers** (workload-identity provider resource name, service-account email, project IDs) live in **GitHub Actions variables** (not secrets — these are addressing information, not authorizing values; leaking them costs nothing).

5. **Deployed services** receive runtime secrets as env vars set by the workflow at deploy time. Service code stays simple; no runtime calls to a secrets manager from inside the service.

This is structurally what Anthropic ships in production for Claude Code's git proxy (https://www.anthropic.com/engineering/claude-code-sandboxing) — generalized to non-git credentialed services via the cloud-secrets-manager + WIF chain.

### 20.2 The five rejected anti-patterns (do not propose any of these)

Each was empirically tested. Each has the shared root cause: **any credential in agent-reachable scope eventually surfaces.** "Eventually" is not a probability claim — it is what happens when agents under tool-call pressure debug, grep, print env, or write helper scripts. The substrate-doc names all five so future agents do not re-derive them from theory.

| # | Anti-pattern | Failure mode |
|---|---|---|
| 1 | **Per-call `op` invocation** (`op run --env-file=<refs> -- railway <args>` for every call) | Per-PID biometric prompt on Windows; produces dozens of unlock prompts in a multi-call session → auth fatigue → reflexive approval → refusal-as-signal violation (§20.3). Empirically broke during railway--r9z 2026-05-15: 3 actual biometric prompts + 2 refusals during ADA's resumption attempt. |
| 2 | **File-on-disk credential** (`.railway-token` written by human, agent `cat \| export` per call) | Agent under pressure reads the file via `cat`, `grep`, `ls -la`, or a debug helper. Even `chmod 600` does not save it — the value exists in agent-readable form, so the value leaks. |
| 3 | **Parent-shell env injection** (human exports `RAILWAY_API_TOKEN=$(op read ...)` then launches `claude`) | Agent inherits env and can leak via `printenv`, `env`, `Get-ChildItem Env:`, `echo $VAR`. Process-state introspection is normal debugging behavior — once the value is in env, it surfaces. |
| 4 | **`op run` wrapper at Claude Code launch** (the 1Password-recommended canonical pattern; wrapper resolves all references into process.env once, then `exec claude`) | Same runtime-env exposure as anti-pattern #3 even though it eliminates the disk-at-rest exposure. The mitigation is brief-discipline ("never `printenv`"), not structure; rejected on PRINCIPAL's empirical rule that every prior agent-credential-access has eventually leaked regardless of stated discipline. |
| 5 | **Local MCP-server-as-credential-broker** (broker process on the same host as the agent, exposing credential-fetch via MCP tool) | Broker process is on the same host as the agent; the agent can read the broker's source, infer the broker's policy, potentially inspect broker process state. The broker author becomes a new fallible-discipline surface, and the broker's source becomes load-bearing. Rejected on the structural-not-merely-fenced bar. |

Three classes of pattern that are **also not the substrate default** but are not anti-patterns either — they are heavier infrastructure that may make sense at scale this team does not currently operate at:

- HashiCorp Vault Cloud (HCP Vault Secrets is EOL July 2026; HCP Vault Dedicated is $360/mo — both off the table for this team's scale).
- 1Password Connect Server (Connect-token-on-disk reintroduces the leak surface from anti-pattern #2).
- Per-machine cloud-vault setups (heavy infrastructure, single-host blast radius).

These remain available as future patterns if a project's scale ever justifies them; they are NOT what the substrate teaches as default.

### 20.3 Refusal-as-signal (subsection of §20)

Refusal-as-signal is structurally part of credential discipline because the empirical anchor was a refusal incident: railway--r9z 2026-05-15, where PLINY issued dozens of per-call auth prompts AND retried after PRINCIPAL refused — failure on both axes. The discipline lives here as §20.3 because the canonical pattern (§20.1) is what makes refusal-as-signal load-bearing: when an agent does have a credentialed call to make, a refusal IS the signal the pattern is wrong, not a problem to route around.

**The rule:** if any tool call is refused by PRINCIPAL — or any credentialed step the agent attempts surfaces a refusal (1Password biometric refused, gcloud auth refused, gh auth refused, MCP-server denied scope) — **halt immediately and surface to the orchestrating seat via bw. Do not retry. Do not improvise a fallback. Do not propose an alternative credentialed path.** Multiple refusals = hard halt; the orchestrator decides whether to re-scope or escalate.

A refusal is not a transient failure to route around; it is the substrate telling the agent the design is wrong. The correct response is the structural one: surface the refusal upward and let the design come back. Quietly retrying with different syntax, falling back to a different credentialed approach, or improvising a workaround all violate the discipline — they convert what was meant to be a halt-and-redesign signal into noise the design loop never sees.

**Empirical anchor:** railway_stoa workspace memory `feedback_credential_friction_script_batched.md` (originally authored under railway--r9z, constraint #6) carried this rule as a workspace-tier discipline before substrate promotion. Multiple prior incidents (2026-05-15 r9z + per-arc paste-cache references) confirm the failure mode recurs whenever the discipline is not encoded structurally.

### 20.4 Universal rule

**Agents do non-credentialed work; CI or humans do credentialed setup.**

The split is structural, not policy:

- **Agents author** workflow YAML, write deploy scripts that CI will run, design the credential-flow diagram, audit the WIF binding, ground-check that `id-token: write` is the correct permission. Agents read the canonical pattern (§20.1), reference the worked example, write the prose. Zero credentialed calls in the agent's tool history.
- **CI runs** the workflow that mints the short-lived credential and consumes it. The workflow is a 1-hour bounded execution; the credential expires when the workflow exits; no credential persists.
- **Humans run** the one-shot setup that creates the WIF binding (gcloud commands) and that puts long-lived per-service tokens (Railway PAT, etc.) into GitHub Actions encrypted secrets. The human's session is also bounded; the credentialed setup happens once per service.

When a brief tempts an agent to "just run `railway <cmd>` with the token to check status," the correct response is the substrate-shaped one: refuse, surface to the orchestrator, and request the work be re-scoped as "author a CI workflow that checks status as part of its smoke beats." The cost of the round-trip is one dispatch; the cost of normalizing per-call credentialed access is structural drift across every future workspace.

Boundary marker against §20.3: this universal rule (§20.4) is **preventive** — the agent self-recognizes the credential-temptation in the brief and refuses-and-redirects before any credentialed call is attempted. §20.3 is **responsive** — once an external refusal has happened (PRINCIPAL refused a prompt, gcloud auth refused, MCP-server denied scope), halt immediately and surface without retry. Both fire on the same root cause (any credential in agent-reachable scope eventually surfaces) but at different points in the dispatch lifecycle; both are load-bearing.

### 20.5 Railway-specific notes (canonization from railway--r9z empirical findings)

Two Railway-specific patterns surfaced during railway--r9z's CI workflow first-run + revise arc that are load-bearing for any future Railway-deploy workflow. They live in the substrate doc because the empirical agent (and multiple peer agents recommending from theory) initially got both wrong.

**Pattern: Railway reference variables resolve ONLY at deploy-time, not at CLI-time.** A Railway service variable defined as a reference (e.g., `DATABASE_URL_PRIVATE = ${{Postgres.DATABASE_URL}}`) resolves to its literal value only inside the deployed service's runtime container. It does NOT resolve when read via `railway variable list --service NAME --json` from an external runner — the CLI returns the KEY with a null VALUE.

The canonical workaround: any CI workflow that needs the resolved value must fetch from the SOURCE service's variable list, where the variable is a literal:

```bash
# WRONG: returns null for reference-typed variables.
railway variable get DATABASE_URL_PRIVATE --service consuming-service

# RIGHT: fetch from the source where the value is a literal.
railway variable get DATABASE_PUBLIC_URL --service Postgres
```

**Anti-pattern: `railway run --service NAME -- cmd`.** This command's name is misleading. It does NOT exec `cmd` inside the service container — it runs `cmd` on the local shell with the service's env vars injected, which means it inherits the same reference-resolution limitation (references still don't resolve, because resolution happens at container start). Multiple agents — including user-tier POLYBIUS and railway_stoa POLYBIUS — initially recommended this pattern from theory based on the misleading command name. ARGUS narrow audit caught it on railway--r9z (DAEDALUS round 2). The discipline lesson: verify Railway CLI behavior against actual docs + empirical runs; don't recommend tool-specific syntax from theoretical mental models.

### 20.6 Cross-reference

The new substrate-tier skill at `substrate/skills/credential-discipline/SKILL.md` carries the worked example: gcloud commands for WIF pool + provider + service account setup, GitHub Actions YAML for `google-github-actions/auth@v3` + `get-secretmanager-secrets@v3` (current-stable majors as of 2026-05-16, verified via `gh api`), Railway-specific patterns for PAT-based services that lack WIF, and the canonical worked-example workflow at `denson/sector-4/.github/workflows/deploy-dev-ariadne.yml` (run 25956772075, dev Ariadne live as of 2026-05-16; note the sector-4 workflow currently pins both actions at `@v2`, lagging upstream by ~8 months — substrate canon is `@v3`).

### 20.7 Empirical lineage

- `railway_stoa/railway--pam` (2026-05-13) — first surfacing of the credential-friction-as-substrate-concern observation; flagged but not actioned.
- `railway_stoa/railway--r9z` (2026-05-15 → 2026-05-16) — empirical engagement: PLINY issued dozens of per-call auth prompts during Railway deploy work AND retried after refusal; PRINCIPAL surfaced the structural concern; the wrapper-launch pattern was proposed, drafted, then rejected on the empirical rule; the CI-mediated canonical pattern was settled; the sector-4 deploy workflow was authored as worked example (run 25956772075, dev Ariadne live).
- `stoa--p5g` (2026-05-15 → 2026-05-16) — substrate-tier promotion: directive landed at `substrate/arcs/arc-25-build-directive.md`, design at this artifact, build at branch `arc-25/build`.

---
```

End of §20 prose.

### §2.2 Why this placement and structure

Three reasons:

1. **§20 keeps anti-patterns near canonical pattern.** Splitting the canonical pattern and the rejected variants into separate sections would invite readers to find one without the other — exactly the failure mode the substrate is trying to prevent (each anti-pattern looks reasonable in isolation; only the shared root cause makes the canonical pattern obviously correct).

2. **Refusal-as-signal as §20.3 (subsection) rather than §21 (peer)** — see §3 below for the decision rationale.

3. **Railway-specific notes as §20.5** rather than as a footnote — empirically two non-obvious Railway patterns surfaced from one engagement; both are likely to be re-encountered. Substrate-doc home keeps them discoverable when a future agent searches the file for "Railway" rather than only when they happen to read the skill.

---

## §3. Refusal-as-signal — placement decision

**Decision: refusal-as-signal is §20.3 (subsection of Credential discipline), NOT a peer §21.**

Rationale:

The directive A3 explicitly allows either placement. The case for peer-section (§21) would rest on the claim that refusal-as-signal is universal beyond credentialed ops — a refusal of any kind from PRINCIPAL means halt-no-retry, not just refusals tied to credential prompts.

The case for subsection (§20.3) — which this design chooses — rests on three empirical observations:

1. **The empirical anchor IS a credential incident.** The rule surfaced from railway--r9z when PLINY retried after refused biometric prompts. The substrate-doc home should keep the rule near the failure mode that surfaced it; readers who land in §20 looking for "what went wrong on railway--r9z" find the rule in context, not as a free-floating discipline elsewhere.

2. **Universal applicability is already covered.** §19 (Confabulation-under-uncertainty) is the universal "halt-and-surface when state and assumption don't match" discipline; §20.3 is the specific case where the state-vs-assumption mismatch comes from a refusal during a credentialed call. Promoting refusal-as-signal to peer-section would create overlap with §19 without adding load-bearing distinction.

3. **A standalone §21 would attract scope creep.** A peer section would invite future arcs to expand "refusal" to mean every kind of pushback (PRINCIPAL says "this approach is wrong," "I don't want to do that," etc.) — which is genuinely different from a hard halt on an authentication refusal. Keeping refusal-as-signal scoped to credentialed-call refusals — exactly the failure mode it surfaced from — preserves its load-bearing edge.

The prose for §20.3 is in §2.1 above. It cites the empirical anchor in railway_stoa workspace memory and names the exact rule: halt immediately, surface to the orchestrating seat via bw, do not retry, do not improvise, do not propose an alternative credentialed path.

### §3.1 Caveat — source-location accuracy

Directive A3 and the read-first list (item 5) both state that refusal-as-signal "currently lives in `~/.claude/CLAUDE.md` as a harness-rule." Empirically verified by full read + grep against the current `~/.claude/CLAUDE.md`: it does NOT live there. The current `~/.claude/CLAUDE.md` (128 lines) contains exactly four standing rules (training-data-search, authorship-attribution, fix-now, Windows-environment) plus the POLYBIUS reference block. No refusal-as-signal rule.

Where it actually lives:

- `C:\Users\denso\.claude\file-history\78a664fb-106a-4a55-9401-93c1c792ab33\5108d7227e3b6f4f@v3` — railway_stoa workspace memory file `feedback_credential_friction_script_batched.md`, constraint #6: "Refusal-as-signal: if any tool call is refused by PRINCIPAL, halt immediately and surface to the orchestrating seat via bw. Do not retry. Multiple refusals = hard halt."
- Multiple paste-cache + transcript references across the railway--r9z engagement.

The substance of the rule is well-established; the source-location attribution in the directive is the inaccuracy. This design uses the empirically-verified wording from the workspace-memory file (above), promoted to substrate canon as §20.3 prose. The directive's intent (promote refusal-as-signal to substrate canon from wherever it currently lives) is preserved; only the directive's claim about WHERE it currently lives is off.

**Resolution (post-rev1 audit):** ARGUS confirmed in the rev1 audit that the source-location discrepancy is non-load-bearing — the substance of refusal-as-signal is well-established across multiple railway_stoa workspace-memory sources and converges with the directive's intent. Substrate promotion proceeds with the empirical wording as written. The directive-clarification follow-up is recorded in §8.1.2. Audit trail: stoa--p5g comment thread, ARGUS rev1 verdict 2026-05-16.

---

## §4. New skill: `substrate/skills/credential-discipline/SKILL.md` — full prose

ADA creates the directory `substrate/skills/credential-discipline/` and writes a single file `SKILL.md` with the prose below verbatim. Frontmatter author MUST say Denson Smith (A10 IMMUTABLE).

```markdown
---
name: credential-discipline
description: "Canonical pattern for authoring CI-mediated deploys to third-party APIs (cloud services, Railway, gh, op, gcloud, aws, azure). Agents NEVER hold credentials. Long-lived secrets live in a cloud-native secrets manager (GCP Secret Manager is the worked example); CI authenticates via Workload Identity Federation; per-service PAT-only tokens (e.g., Railway) live in GitHub Actions encrypted secrets, decrypted only at workflow runtime. Read this skill when a brief involves any credentialed third-party API call — the skill's job is to redirect the work from agent-runs-CLI-with-credentials to agent-authors-workflow-that-CI-runs. Triggers on requests like 'deploy to Railway', 'authenticate to GCP', 'set up CI for cloud deploy', 'add a new secret', 'rotate this token', 'agent needs to call this API with a token'."
author: Denson Smith
---

# credential-discipline — agents author workflows, CI runs them

## Why this skill exists

Every workspace that touches credentialed third-party operations re-derives the same architecture from scratch and re-makes the same mistakes. The substrate empirically tested five credential-access patterns (`operating-disciplines.md` §20.2) before settling on the CI-mediated answer. This skill captures the worked example so future workspaces inherit the pattern instead of re-deriving it.

The discipline this skill enforces: **agents NEVER hold credentials.** A brief that says "agent runs `railway deploy` with the token" is asking the wrong question; the right reshape is "agent authors `.github/workflows/deploy.yml` that CI runs; CI holds the credential for the workflow's 1-hour bounded execution; the credential expires when the workflow exits." That reshape is what this skill mechanizes.

Required reading before authoring any credentialed-ops design: `operating-disciplines.md` §20 (the substrate canon this skill operationalizes).

## When to use this skill

Invoke when:

- A brief involves a third-party API or cloud service that requires authentication (Railway, GCP, AWS, Azure, gh, op, vercel, fly, any SaaS API).
- An agent finds itself about to call a credentialed CLI inline (`railway <cmd>`, `gcloud <cmd>`, `gh auth`, `op read`).
- A workflow needs to read or rotate a long-lived secret.
- A new service is being added that needs deploy automation.

Do NOT invoke for:

- Local development scripts the human runs themselves (no agent in the loop).
- The one-shot setup commands a human runs to establish the WIF binding (those ARE credentialed and ARE the right scope for human-runs-once).

## The architectural pattern (referencing §20)

```
[Local agent] → git push → [GitHub] → [CI workflow] → [Cloud APIs]
   (no creds)             (Actions    (WIF mints      (creds used
                           secrets)    short-lived     once, expire)
                                       creds)
```

The full pattern (canonical, anti-patterns, universal rule) lives in `operating-disciplines.md` §20. This skill is the worked example: gcloud commands, GitHub Actions YAML, Railway-specific patterns.

## One-shot setup the human runs (NOT the agent)

The WIF binding is established once per cloud project. The commands below are the human's setup work — not the agent's, and not CI's. The agent designs the binding (which permissions, which service account, which pool/provider names); the human runs the commands; CI then uses the binding via workflow YAML.

### GCP Secret Manager + Workload Identity Federation setup

```bash
# Set context
export PROJECT_ID="<your-gcp-project-id>"
export POOL_ID="github-actions-pool"
export PROVIDER_ID="github-actions-provider"
export SA_NAME="github-actions-deploy"
export SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
export GH_OWNER="<github-org-or-user>"
export GH_REPO="<github-repo-name>"

# 1. Enable required APIs
gcloud services enable iamcredentials.googleapis.com secretmanager.googleapis.com --project="${PROJECT_ID}"

# 2. Create the workload identity pool
gcloud iam workload-identity-pools create "${POOL_ID}" \
  --project="${PROJECT_ID}" --location="global" \
  --display-name="GitHub Actions Pool"

# 3. Create the OIDC provider for GitHub
gcloud iam workload-identity-pools providers create-oidc "${PROVIDER_ID}" \
  --project="${PROJECT_ID}" --location="global" \
  --workload-identity-pool="${POOL_ID}" \
  --display-name="GitHub Actions Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository=='${GH_OWNER}/${GH_REPO}'" \
  --issuer-uri="https://token.actions.githubusercontent.com"

# 4. Create the service account CI will impersonate
gcloud iam service-accounts create "${SA_NAME}" \
  --project="${PROJECT_ID}" \
  --display-name="GitHub Actions Deploy SA"

# 5. Grant Secret Manager accessor role (or whatever scopes the workflow needs)
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/secretmanager.secretAccessor"

# 6. Bind the workload identity to the service account
gcloud iam service-accounts add-iam-policy-binding "${SA_EMAIL}" \
  --project="${PROJECT_ID}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/$(gcloud projects describe ${PROJECT_ID} --format='value(projectNumber)')/locations/global/workloadIdentityPools/${POOL_ID}/attribute.repository/${GH_OWNER}/${GH_REPO}"

# 7. Get the provider resource name (needed for workflow YAML)
echo "workload_identity_provider:"
echo "  projects/$(gcloud projects describe ${PROJECT_ID} --format='value(projectNumber)')/locations/global/workloadIdentityPools/${POOL_ID}/providers/${PROVIDER_ID}"
echo "service_account: ${SA_EMAIL}"
```

The provider resource name + service account email go into the workflow's `vars:` (GitHub Actions variables — not secrets; they are addressing info).

### Adding a secret to GCP Secret Manager

```bash
# Human runs this from their authenticated gcloud session
echo -n "<secret-value>" | gcloud secrets create "${SECRET_NAME}" \
  --project="${PROJECT_ID}" \
  --data-file=- \
  --replication-policy="automatic"

# Subsequent versions (rotation)
echo -n "<new-secret-value>" | gcloud secrets versions add "${SECRET_NAME}" \
  --project="${PROJECT_ID}" \
  --data-file=-
```

## GitHub Actions workflow template (agents author this)

```yaml
# .github/workflows/<deploy-name>.yml
name: <deploy-name>

on:
  workflow_dispatch:
    inputs:
      # Optional inputs; concrete depending on what the deploy does
      dry_run:
        description: "Dry-run mode (no actual changes)"
        type: boolean
        default: false
  push:
    branches:
      - main
    paths:
      - "<paths-that-trigger-deploy>"

permissions:
  contents: read       # Required to checkout the repo
  id-token: write      # Required for WIF OIDC exchange

jobs:
  deploy:
    runs-on: ubuntu-latest
    timeout-minutes: 30   # Bounded execution — credential expires when workflow exits

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      # Authenticate to GCP via Workload Identity Federation.
      # No static cloud key in GitHub Secrets — the OIDC token is minted at
      # runtime and exchanged for a 1-hour scoped credential that expires
      # when the workflow exits.
      - name: Authenticate to Google Cloud
        id: auth
        uses: google-github-actions/auth@v3
        with:
          workload_identity_provider: ${{ vars.WIF_PROVIDER }}
          service_account: ${{ vars.WIF_SERVICE_ACCOUNT }}

      # Fetch secrets from GCP Secret Manager. The fetched values land in
      # ${{ steps.secrets.outputs.<name> }} for use in subsequent steps.
      # Mark them as secrets so they are auto-masked in logs.
      - name: Fetch secrets from GCP Secret Manager
        id: secrets
        uses: google-github-actions/get-secretmanager-secrets@v3
        with:
          secrets: |-
            RAILWAY_API_TOKEN:${{ vars.GCP_PROJECT_ID }}/RAILWAY_API_TOKEN
            # Add more secrets here, one per line, as:
            # OUTPUT_NAME:projects/PROJECT/secrets/SECRET_NAME[/versions/VERSION]

      # Now use the fetched secrets via ${{ steps.secrets.outputs.<NAME> }}
      # in any subsequent step. Example: Railway deploy.
      - name: Install Railway CLI
        run: |
          curl -fsSL https://railway.com/install.sh | sh
          echo "$HOME/.railway/bin" >> $GITHUB_PATH

      - name: Deploy to Railway
        env:
          RAILWAY_API_TOKEN: ${{ steps.secrets.outputs.RAILWAY_API_TOKEN }}
        run: |
          railway link --project <project-id> --environment <env> --service <service>
          railway up --service <service> --detach

      # ... additional deploy steps ...
```

Key properties:

- **`permissions: id-token: write`** is what enables the OIDC exchange. Without it, the auth step fails with "no id-token available."
- **`workload_identity_provider` and `service_account`** come from GitHub Actions `vars`, not `secrets`. They are addressing information, not authorizing values.
- **`google-github-actions/auth@v3`** is the current-stable major version (verified via `gh api repos/google-github-actions/auth/releases` 2026-05-16: `v3.0.0` published 2025-08-28; `v3` tag dated 2025-09-03). The float-major `@v3` form is conventional GitHub Actions practice — non-breaking patch updates flow automatically; pin to `v3.0.0` only if your project requires exact-version reproducibility.
- **`get-secretmanager-secrets@v3`** is the current-stable major version (verified via `gh api repos/google-github-actions/get-secretmanager-secrets/releases` 2026-05-16: `v3.0.0` published 2025-09-03). Auto-masking is preserved in v3 — fetched values are added to the workflow's log mask immediately after retrieval (per upstream README: "After a secret is accessed, its value is added to the mask of the build to reduce the chance of it being printed or logged by later steps").
- **`timeout-minutes: 30`** bounds the workflow's execution. The minted credential expires when the workflow exits.

## Railway-specific patterns

Railway does not support WIF; it issues PATs (Personal Access Tokens) instead. The PAT lives in GitHub Actions encrypted secrets OR is fetched from GCP Secret Manager (the example above does the latter, which lets all secrets live in one place).

### Account-scoped PAT vs project-scoped token

- **`RAILWAY_API_TOKEN`** (account-scoped PAT) — what to use for CI workflows. Works with `--project / --environment / --service` flags to scope each call.
- **`RAILWAY_TOKEN`** (project-scoped) — different env var, narrower scope; use only inside a deployed container where the token is project-bound.

When in doubt, the 1Password / GitHub Secret name matches the env var name. Using `RAILWAY_TOKEN` for an account-level call fails with "Unauthorized."

### Reference variables resolve only at deploy-time, not at CLI-time

Railway service variables defined as references (e.g., `DATABASE_URL_PRIVATE = ${{Postgres.DATABASE_URL}}`) resolve to their literal value only inside the deployed service's runtime container. They do NOT resolve when read via the CLI from an external runner:

```bash
# WRONG: returns KEY with null VALUE for reference-typed variables.
railway variable get DATABASE_URL_PRIVATE --service consuming-service

# RIGHT: fetch from the SOURCE service where the variable is a literal.
railway variable get DATABASE_PUBLIC_URL --service Postgres
```

Cross-ref: `operating-disciplines.md` §20.5.

### Anti-pattern: `railway run --service NAME -- cmd`

This command's name is misleading. It does NOT exec `cmd` inside the service container — it runs `cmd` on the local shell with the service's env vars injected, which means it inherits the same reference-resolution limitation. Multiple agents (including user-tier POLYBIUS and railway_stoa POLYBIUS) initially recommended this pattern from theory based on the misleading command name. ARGUS narrow audit caught it on railway--r9z (DAEDALUS round 2).

Discipline lesson: verify Railway CLI behavior against actual docs + empirical runs; don't recommend tool-specific syntax from theoretical mental models.

Cross-ref: `operating-disciplines.md` §20.5.

## Worked example: sector-4 dev Ariadne deploy

The canonical worked example is `denson/sector-4/.github/workflows/deploy-dev-ariadne.yml` (~564 lines, validated end-to-end at run 25956772075; dev Ariadne is live at https://ariadne-core-production-cd25.up.railway.app as of 2026-05-16).

URL: https://github.com/denson/sector-4/blob/main/.github/workflows/deploy-dev-ariadne.yml

**Visibility constraint:** the `denson/sector-4` repository is PRIVATE. Without read access to that repo, the URL above returns 404. PRINCIPAL can grant repo access if a specific engagement requires reading the canonical workflow; otherwise the workflow template in this skill (above) is the substrate-resident version of the same pattern.

**Upstream-version lag (honest empirical signal):** the sector-4 deploy workflow currently uses `@v2` for both `google-github-actions/auth` and `google-github-actions/get-secretmanager-secrets` (lagging upstream `@v3` by ~8 months as of 2026-05-16; v3 majors shipped 2025-08 and 2025-09 respectively). The substrate teaches the current upstream canonical (`@v3`); workspaces porting from this skill should use `@v3`. A future dependency-bump arc will reconcile the worked example with substrate canon. The structural pattern (WIF + Secret Manager + bounded workflow) is identical across v2 and v3 — the lag is a version-pin concern, not a structural-pattern concern.

The sector-4 workflow demonstrates the full chain:

1. `workflow_dispatch` trigger (manual + parameterizable)
2. GCP authentication via WIF (`google-github-actions/auth@v2` in sector-4; substrate-canonical is `@v3`)
3. Secret retrieval from GCP Secret Manager (`get-secretmanager-secrets@v2` in sector-4; substrate-canonical is `@v3`)
4. Railway CLI link to project / environment / service
5. Verify upstream service binding (the source-service-fetch pattern above)
6. Set 6 secret-derived env vars on the deployed service
7. Enable pgvector extension
8. Capture pre-deploy state for rollback
9. Deploy via `railway up --detach`
10. Post-deploy smoke test against the deployed endpoint

## What this skill is NOT

- **Not a substitute for `operating-disciplines.md` §20.** The discipline canon is in operating-disciplines; this skill is the worked example. Reading the skill without reading §20 is reading the recipe without the principle.
- **Not a runner.** This skill does not deploy anything. Agents read it, then author their own workflow YAML against it.
- **Not a 1Password tutorial.** The substrate explicitly rejected all five op-based credential-access patterns (§20.2). 1Password is the human's setup tool for putting secrets into GCP Secret Manager / GitHub Secrets; it is NOT the agent's credential-fetch surface.
- **Not a vault-comparison.** HCP Vault, 1Password Connect, per-machine vaults are explicitly out of scope as substrate default (§20.2 trailing list). Future patterns if scale ever justifies them; not the worked example here.

## Cross-refs

- `operating-disciplines.md` §20 — the substrate canon this skill operationalizes
- `denson/sector-4/.github/workflows/deploy-dev-ariadne.yml` — canonical worked example (private repo)
- `https://github.com/google-github-actions/auth` — auth action docs (v3 current stable as of 2026-05-16)
- `https://github.com/google-github-actions/get-secretmanager-secrets` — secret fetch action docs (v3 current stable as of 2026-05-16)
- `https://cloud.google.com/blog/products/identity-security/enabling-keyless-authentication-from-github-actions` — GCP keyless-auth narrative reference
- `https://www.anthropic.com/engineering/claude-code-sandboxing` — structural reference for the proxy pattern (Claude Code's git proxy uses the same shape)
```

End of `SKILL.md` prose.

### §4.1 Notes on the skill prose

- **Frontmatter `author: Denson Smith`** is the IMMUTABLE field per A10. ADA must NOT change this on commit; ARGUS audits this field explicitly; PLINY's smoke beat #6 eyeballs it again before merge.
- **The skill cross-references §20 from the first paragraph** so any future agent reading the skill alone gets routed back to the canon. The skill is the recipe; §20 is the principle.
- **The two Railway-specific patterns live in BOTH §20.5 and §4.2/§4.3 of the skill** with mutual cross-refs. The reason for the duplication: a future agent searching `operating-disciplines.md` for "Railway" finds them in canon context; a future agent reading the skill end-to-end finds them in worked-example context. Both surfaces matter; the duplication is deliberate, not drift.

---

## §5. CAPTAIN envelope updates (DAEDALUS, ADA, ARGUS, BARTLEBY)

Per A5, each envelope gets a short addition directing the seat to the CI-mediated pattern when a brief involves credentialed operations. The wording adapts per seat. Each addition cross-references the new skill (A4).

### §5.1 CAPTAIN_DAEDALUS — addition

**Where to add:** new subsection `### 6.6 Credential discipline (load-bearing for designs that touch credentialed ops)` immediately after the existing §6.5 (Heartbeat-and-read-before-write via bw) and before the existing §7 (Verdict format).

**Exact prose to add:**

```markdown
### 6.6 Credential discipline (load-bearing for designs that touch credentialed ops)

When a brief involves credentialed operations against any third-party API or cloud service (Railway, gcloud, gh, op, aws, azure, kubectl, vercel, fly — any CLI or HTTP API gated by an API token, OAuth scope, or service account), the design MUST specify a CI-mediated path. Never "agent runs CLI X with credentials"; always "agent authors workflow that does X; CI runs the workflow." The substrate canon is `operating-disciplines.md` §20; the worked example skill is `substrate/skills/credential-discipline/SKILL.md` — read both before drafting the design's credential-flow section.

A design that proposes any of the five rejected anti-patterns (per-call `op`, file-on-disk credential, parent-shell env injection, `op run` wrapper at Claude Code launch, local MCP-server-as-credential-broker — full list at §20.2) fails the pre-gate; if the brief implicitly requires one, refuse back to MAJOR_PLINY with the gap named. The discipline is structural, not stylistic: the five anti-patterns have all been empirically tested and rejected on PRINCIPAL's load-bearing rule that any credential in agent-reachable scope eventually surfaces.

The design's verification probes section (per §3) MUST include at least one probe that confirms the design's CI-mediated structure (e.g., "workflow YAML contains `permissions: id-token: write`" or "no credentialed CLI calls appear in any ADA-built script"). This makes the structural property checkable by VERA rather than implicit in prose.
```

### §5.2 CAPTAIN_ADA — addition

**Where to add:** new subsection `### 5.7 Credential discipline (refuse the manual path, produce the CI workflow)` immediately after the existing §5.6 (Heartbeat-and-read-before-write via bw) and before the existing §6 (Verdict format).

**Exact prose to add:**

```markdown
### 5.7 Credential discipline (refuse the manual path, produce the CI workflow)

When a build involves credentialed operations against any third-party API or cloud service, the structural rule is: agents NEVER hold credentials. If the design (or the brief) tempts you to run a credentialed CLI inline — `railway <cmd>`, `gcloud <cmd>`, `gh auth`, `op read`, anything that touches a credential — STOP. Surface to MAJOR_PLINY via the verdict's `gap_or_blocker:` field with the refusal made explicit; do not improvise an inline workaround.

The substrate canon is `operating-disciplines.md` §20; the worked example skill is `substrate/skills/credential-discipline/SKILL.md`. Read both before starting any build that includes credentialed ops. The correct build artifact for a credentialed-ops design is a workflow YAML file (typically `.github/workflows/<deploy-name>.yml`) that CI runs — NOT a shell script that the agent runs against the live API.

The reshape from "agent runs CLI" to "agent authors workflow that CI runs" sometimes requires a brief revision. That is the correct response — the cost of one revision round-trip is small; the cost of normalizing per-call credentialed access is structural drift. Refusal-as-signal (§20.3) applies: if PRINCIPAL refuses any credentialed step the build attempts, halt immediately and surface; do not retry, do not improvise, do not propose an alternative credentialed path.

Authorship guard: when the build creates a new file under `substrate/skills/credential-discipline/` (or any skill metadata / SKILL.md frontmatter), the `author:` field names **Denson Smith** per §5.5. The credential-discipline skill specifically has been flagged by the orchestrator + monitoring peer as an audit point; verify before commit.
```

### §5.3 CAPTAIN_ARGUS — addition

**Where to add:** new subsection `### 6.8 Credential discipline (flag non-CI-mediated approaches as load-bearing risks)` immediately after the existing §6.7 (Heartbeat-and-read-before-write via bw) and before the existing §7 (Verdict format).

**Exact prose to add:**

```markdown
### 6.8 Credential discipline (flag non-CI-mediated approaches as load-bearing risks)

When auditing a design that involves credentialed operations against any third-party API or cloud service, the substrate canon at `operating-disciplines.md` §20 names five anti-patterns that have been empirically tested and rejected. Any design that proposes — directly or by silence on the credential-flow question — one of those anti-patterns carries a `load_bearing: true` risk:

1. Per-call `op` invocation (per-PID biometric prompt → auth fatigue → refusal-as-signal violation)
2. File-on-disk credential (agent reads via `cat`, `grep`, debug helpers)
3. Parent-shell env injection (agent reads via `printenv`, `Get-ChildItem Env:`)
4. `op run` wrapper at Claude Code launch (same runtime-env exposure as #3)
5. Local MCP-server-as-credential-broker (broker on same host as agent)

The shared root cause is the load-bearing property: any credential in agent-reachable scope eventually surfaces, regardless of stated brief-discipline. A design's silence on credential-flow (e.g., "the workflow uses the Railway CLI" with no description of how the token reaches the CLI) is a risk-worthy ambiguity — surface it as `load_bearing: true` with `evidence:` citing the silent design section.

The correct shape is CI-mediated: agents author workflow YAML, CI runs it via short-lived credentials minted by Workload Identity Federation (or per-service PATs in GitHub Actions encrypted secrets for services lacking WIF). The worked example is `substrate/skills/credential-discipline/SKILL.md`; verify the design's pattern matches the skill before clearing.

Refusal-as-signal violations (§20.3) are also load-bearing risks: if a design implies the agent should retry after a refused credentialed step ("fall back to method B if method A is refused"), surface as `load_bearing: true`. A refusal is meant to halt the dispatch and force a redesign upward, not be routed around inside the same dispatch.
```

### §5.4 CAPTAIN_BARTLEBY — addition

**Where to add:** new subsection `### 6.7 Credential discipline (cross-ref when surfacing credentialed-resource locations)` immediately after the existing §6.6 (Heartbeat-and-read-before-write via bw) and before the existing §7 (Verdict format).

**Exact prose to add:**

```markdown
### 6.7 Credential discipline (cross-ref when surfacing credentialed-resource locations)

When a recon question surfaces findings that reference credentialed resources — workflow YAML files under `.github/workflows/`, scripts that call third-party CLIs (`railway`, `gcloud`, `gh`, `op`), files matching `*token*` or `*secret*` or `*credential*`, references to GCP Secret Manager / GitHub Actions secrets — include in the verdict's `summary:` a cross-reference to `operating-disciplines.md` §20 and `substrate/skills/credential-discipline/SKILL.md`. The caller (DAEDALUS, ARGUS, VERA, or CATO) reading the citations needs to know the substrate canon exists so the interpretation is anchored against the canonical pattern, not against whatever the calling agent remembers.

The cross-ref is NOT interpretation (which would violate §6.1 / §4 / §5 of this envelope). It is pointer-to-canon: "findings reference credentialed-resource patterns; see operating-disciplines.md §20 for substrate canon and substrate/skills/credential-discipline/SKILL.md for the worked example." The caller does the interpretation; BARTLEBY's job is to make the canon discoverable from the recon output.

When findings surface a credential value literally embedded in a file (an API token committed to git, a service-account JSON checked in, an env var with a real key value in a script), surface as `tag: credential_leak` rather than the generic `comment_mention` — this is a load-bearing finding the caller MUST escalate.
```

**Additional in-scope edit to CAPTAIN_BARTLEBY.md:** the verdict-format `tag:` enumeration at line 142 of `substrate/CAPTAIN_BARTLEBY.md` MUST be extended to include the new `credential_leak` value. Current enum reads:

```
tag: <definition | call_site | import | schema_reference | comment_mention | authorship_anomaly | other>
```

ADA's edit replaces this line so the final enum reads:

```
tag: <definition | call_site | import | schema_reference | comment_mention | authorship_anomaly | credential_leak | other>
```

This is one additional line-edit in an already-in-scope file (CAPTAIN_BARTLEBY.md is among the four named in A5). Without this edit, a future BARTLEBY finding emitting `tag: credential_leak` per §6.7 above would be inconsistent with the documented enum — the new tag value would be dangling. ARGUS audit caught this gap in rev1; rev2 specifies the fix.

### §5.5 Per-seat adaptation notes

The four additions share substrate canon references but adapt to the seat's verb:

| Seat | Seat verb | Adaptation in the addition |
|---|---|---|
| DAEDALUS | designs | "design MUST specify a CI-mediated path"; refuse back to PLINY if brief requires anti-pattern; design's verification probes must include CI-mediated-structure probe |
| ADA | builds | "STOP" on inline credentialed CLI temptation; surface via verdict; correct artifact is workflow YAML, not shell script; explicit authorship guard for the new skill SKILL.md |
| ARGUS | audits | enumerate the 5 anti-patterns as `load_bearing: true` risks; silence on credential-flow IS a risk-worthy ambiguity; refusal-as-signal violations also load-bearing |
| BARTLEBY | searches | cross-ref to §20 + skill from `summary:` when findings touch credentialed resources; new `tag: credential_leak` for literally-embedded values; explicitly NOT interpretation (preserves §6.1 of BARTLEBY envelope) |

VERA, CATO, ZENO, STRABO, HERALD, CURATOR — envelopes NOT touched per A11. If empirical evidence later surfaces a need for any of these seats to carry credential-discipline-specific prose, file a follow-up arc. The four envelopes touched here are the ones whose seat-role is structurally credentialed-ops-adjacent (DAEDALUS designs them, ARGUS audits them, ADA builds them, BARTLEBY surfaces them in recon).

---

## §6. `install.sh` delta — explicit entry required

**Determination:** `install.sh` requires an explicit `SKILL_NAMES` array entry. Glob-discovery is NOT used.

Evidence chain:

1. **`SKILL_NAMES` is an explicit array, lines 140-143:**
    ```bash
    SKILL_NAMES=(
      agent-author
      check-substrate-updates
    )
    ```
2. **Source-side existence check loops over `SKILL_NAMES`, lines 532-535:**
    ```bash
    for sname in "${SKILL_NAMES[@]}"; do
      [ -d "${SRC_SKILLS_DIR}/${sname}" ] || err "source skill directory not found: ${SRC_SKILLS_DIR}/${sname}"
      [ -f "${SRC_SKILLS_DIR}/${sname}/SKILL.md" ] || err "source skill SKILL.md not found: ${SRC_SKILLS_DIR}/${sname}/SKILL.md"
    done
    ```
3. **Deploy loop also iterates `SKILL_NAMES`, lines 699-714:**
    ```bash
    for sname in "${SKILL_NAMES[@]}"; do
      src_skill="${SRC_SKILLS_DIR}/${sname}"
      dest_skill="${DEST_SKILLS_DIR}/${sname}"
      ...
    done
    ```
4. **Staleness scan also iterates `SKILL_NAMES`, lines 819-835.** A skill present on disk under `substrate/skills/` but NOT in `SKILL_NAMES` would be flagged at deploy as obsolete and proposed for removal — the opposite of "discovered automatically."

The current `SKILL_NAMES` is alphabetical (`agent-author`, `check-substrate-updates`). Inserting `credential-discipline` preserves the convention.

**The exact edit ADA makes** at lines 140-143:

```bash
SKILL_NAMES=(
  agent-author
  check-substrate-updates
  credential-discipline
)
```

(Single-line addition; surrounding array brackets and existing entries preserved verbatim. The line ADA inserts is `  credential-discipline` between `check-substrate-updates` and the closing `)`.)

No other install.sh edits are required. The new skill subdirectory `substrate/skills/credential-discipline/` (containing `SKILL.md`) is detected by the existence check (step 2 above) once `credential-discipline` is in `SKILL_NAMES`; the deploy loop (step 3) `cp -R`'s the directory wholesale to each target tier; the staleness scan (step 4) treats it as a valid skill.

---

## §7. Deletion: `~/.claude/skills/railway-access/SKILL.md`

**Spec for ADA:** delete the file `~/.claude/skills/railway-access/SKILL.md` AND remove the parent directory `~/.claude/skills/railway-access/` (the file is the only content, verified by `ls -la`).

The file lives at user-tier (`~/.claude/`), NOT in the the-stoa repo. The deletion does NOT appear in the ADA-committed diff for the `arc-25/build` branch — there is no in-repo file to remove. The deletion is a one-line shell command ADA runs as part of Phase 2:

```bash
rm -rf "${HOME}/.claude/skills/railway-access"
```

This removes both the file and the empty parent directory in one operation. ADA records the deletion in the verdict's `summary:` and `files_changed:` (with a note that the path is user-tier, not in the repo's diff). Phase 4 smoke beat #5 (per arc-25-build-directive.md) verifies the file no longer exists.

**Justification for the deletion** (recorded for ARGUS / CATO traceability):

The current skill (read in full at Phase 1a) documents the parent-shell-env injection pattern (`export RAILWAY_API_TOKEN=$(op read ...)`), which IS anti-pattern #3 from `operating-disciplines.md` §20.2. The skill teaches the now-rejected pattern as canonical. Two options were considered:

- **Rewrite the skill** to CI-mediated form. Rejected because (a) the new substrate-tier `credential-discipline` skill (§4) already covers the CI-mediated pattern with the worked example, including Railway-specific notes; a user-tier railway-access skill rewritten to CI-mediated form would duplicate the substrate-tier skill with no added value; and (b) the railway--dwc port-skill ticket on railway_stoa was planning to port railway-access to workspace-tier — that port becomes unnecessary once the CI-mediated pattern is canonical.
- **Delete the skill.** Chosen. Removes the rejected-pattern documentation from the user-tier discoverable surface; future agents looking for Railway-credential guidance find the substrate-tier `credential-discipline` skill instead.

Cross-coordination note (out of scope per A11, recorded as follow-up in §8): `railway_stoa/railway--dwc` (port-skill ticket) needs to close post-arc with reason "obviated by CI-mediated pattern." That coordination is OWNED BY user-tier POLYBIUS per the arc-25 directive A8; this arc does NOT touch railway--dwc.

---

## §8. Out-of-scope confirmation (A11) — what is NOT touched

Per A11, scope is locked to the six touch-points enumerated. The following are explicitly NOT edited by this design:

| Surface | Why out of scope |
|---|---|
| Other operating-disciplines.md sections (§1-§19) | A11. No drive-by edits. Includes the stale "Thesis" sentence at line 13 ("§1-§17 plus the autonomous-mode setup checklist") which now reads § instead of §1-§19 (or §1-§20 post-arc). |
| `substrate/MAJOR_PLINY.md` | A11. PLINY's dispatch-section could carry a credential-discipline cross-ref ("when authoring a brief for credentialed ops, point CAPTAINs at §20") but the arc explicitly excludes it. |
| `substrate/MAJOR_POLYBIUS.md` | A11. POLYBIUS's escalation-triggers section could carry a credential-discipline reference but the arc explicitly excludes it. |
| Other CAPTAIN envelopes (VERA, CATO, ZENO, STRABO, HERALD, CURATOR) | A5 + A11. Only the four credentialed-ops-adjacent seats are in scope. |
| `substrate/templates/` | A11. None of the templates are credential-flow-specific. |
| `app/` (the Stoa app for visualizing rosters) | A11. Substrate adapter reads frontmatter; the new skill's frontmatter is conventional and the adapter's Zod schema should validate without changes. ADA may want to run `npm run gen-data` post-build as a sanity check (per `the-stoa/CLAUDE.md`) — that is build-check sanity, not a substrate edit. |
| `railway--r9z` workflow (`denson/sector-4/.github/workflows/deploy-dev-ariadne.yml`) | A11 + A9 + directive §"What's NOT in this arc's scope." The workflow is the worked example; this arc references it, does not modify it. |
| `railway_stoa/railway--dwc` (port-railway-access-skill ticket) | A8 directive note: close-post-arc, owned by user-tier POLYBIUS. NOT this arc. |
| `the-stoa` working-tree out-of-scope artifacts (`_drafts/*`, `HUMAN_paste-*`, `docs/case-study/*` PDFs) | A11. PLINY's dispatch confirms these are explicitly left alone. |

### §8.1 Follow-up tickets to file post-arc (recorded as `follow_ups:` in verdict)

1. **operating-disciplines.md Thesis sentence stale** — line 13 says "§1-§17 plus the autonomous-mode setup checklist" but the file has §1-§19 and post-arc-25 has §1-§20. Trivial one-sentence edit; file as a `stoa--<id>` polish ticket post-arc-25.
2. **A3 directive inaccuracy** — directive claims refusal-as-signal lives in `~/.claude/CLAUDE.md`; empirically it lives in railway_stoa workspace memory `feedback_credential_friction_script_batched.md`. Record as a directive-clarification note on the arc-25 retrospective (or on the next time the directive template is updated); no current substrate file needs the fix.
3. **MAJOR_PLINY.md dispatch-section cross-ref to §20** — a brief discipline cross-ref ("when authoring a brief for credentialed ops, point CAPTAIN at §20 + the skill") would mechanically extend the §20 discipline to brief-authoring. Out of scope per A11; file as `stoa--<id>` for the next discipline-accretion arc.
4. **MAJOR_POLYBIUS.md escalation-triggers cross-ref to §20.3** — refusal-as-signal violations should be a named POLYBIUS escalation trigger (peer-tier visibility). Out of scope per A11; file similarly.
5. **railway_stoa/railway--dwc closure** — owned by user-tier POLYBIUS per directive A8; not this arc's responsibility but flagged for cross-team-coordination tracking.
6. **Authorship-frontmatter audit on pre-existing substrate skills** — ARGUS rev1 nf1 observation: `substrate/skills/agent-author/SKILL.md` and `substrate/skills/check-substrate-updates/SKILL.md` lack `author: Denson Smith` YAML frontmatter (the new credential-discipline skill correctly carries it per A10). The two existing skills are out of A11 scope for this arc; audit them and add the frontmatter post-merge. File as a `stoa--<id>` polish ticket; trivial one-line addition per skill.

---

## §9. Verification probes (for VERA)

VERA executes these in Phase 3. Each is a concrete runnable command + expected outcome.

### §9.1 install.sh integration

| # | Probe | Expected outcome |
|---|---|---|
| P1 | `cd <repo-root> && substrate/install.sh --target user --dry-run 2>&1 \| grep "credential-discipline"` | At least one match: `[dry-run] deploy skill: <SRC>/credential-discipline/ -> <DEST>/credential-discipline/ (cp -R)` |
| P2 | `cd <repo-root> && substrate/install.sh --dry-run --target project --project-dir <some-test-project> 2>&1 \| grep "credential-discipline"` | At least one match (same as P1 but project-tier) |
| P3 | `grep -c "credential-discipline" substrate/install.sh` | `1` (exactly one entry in SKILL_NAMES; no other references expected) |

### §9.2 operating-disciplines.md content correctness

| # | Probe | Expected outcome |
|---|---|---|
| P4 | `grep -c "refusal-as-signal" substrate/operating-disciplines.md` | `>= 1` (matches arc-25-build-directive.md smoke beat #2) |
| P5 | `grep -c "agents NEVER" substrate/operating-disciplines.md` | `>= 1` (matches arc-25-build-directive.md smoke beat #4) |
| P6 | `grep -c "^## 20\." substrate/operating-disciplines.md` | `1` (exactly one §20 heading) |
| P7 | `grep -c "Credential discipline" substrate/operating-disciplines.md` | `>= 1` (§20 title present) |
| P8 | `grep -c "Workload Identity Federation\|WIF" substrate/operating-disciplines.md` | `>= 1` (the canonical pattern's structural component is named) |
| P9 | `grep -c "anti-pattern" substrate/operating-disciplines.md \| awk '$1 >= 5'` returns non-empty | At least 5 references to "anti-pattern" within §20 (one per rejected pattern + others) |

### §9.3 CAPTAIN envelope cross-refs

| # | Probe | Expected outcome |
|---|---|---|
| P10 | `grep -l "CI-mediated" substrate/CAPTAIN_DAEDALUS.md substrate/CAPTAIN_ADA.md substrate/CAPTAIN_ARGUS.md substrate/CAPTAIN_BARTLEBY.md` | All 4 files match (matches arc-25-build-directive.md smoke beat #3) |
| P11 | `grep -l "credential-discipline" substrate/CAPTAIN_DAEDALUS.md substrate/CAPTAIN_ADA.md substrate/CAPTAIN_ARGUS.md substrate/CAPTAIN_BARTLEBY.md` | All 4 files match (cross-ref to the new skill present in each) |
| P11b | `grep -c "credential_leak" substrate/CAPTAIN_BARTLEBY.md \| awk '$1 >= 2'` returns non-empty | At least 2 references: one in the verdict-format enum at line ~142, one in the §6.7 envelope addition prose (confirms the dangling-tag gap from rev1 audit is closed) |
| P12 | `grep -L "credential" substrate/CAPTAIN_VERA.md substrate/CAPTAIN_CATO.md substrate/CAPTAIN_ZENO.md substrate/CAPTAIN_STRABO.md substrate/CAPTAIN_HERALD.md substrate/CAPTAIN_CURATOR.md` | All 6 files match (no credential cross-ref in out-of-scope CAPTAINs — confirms scope-discipline) |

### §9.4 New skill renders coherently

| # | Probe | Expected outcome |
|---|---|---|
| P13 | `test -f substrate/skills/credential-discipline/SKILL.md && echo OK` | `OK` (file exists) |
| P14 | `head -5 substrate/skills/credential-discipline/SKILL.md \| grep "^author: Denson Smith"` | One match (authorship IMMUTABLE per A10) |
| P15 | `python -c "import yaml,sys; d=open('substrate/skills/credential-discipline/SKILL.md').read(); fm=d.split('---')[1]; print(yaml.safe_load(fm))"` | YAML frontmatter parses without exception; output includes `name`, `description`, `author` keys |
| P16 | `grep -c "denson/sector-4/.github/workflows/deploy-dev-ariadne.yml" substrate/skills/credential-discipline/SKILL.md` | `>= 1` (worked-example pointer present per A9) |
| P17 | `grep -c "google-github-actions/auth@v3" substrate/skills/credential-discipline/SKILL.md` | `>= 1` (current-stable major version cited; v3.0.0 published 2025-08-28 per `gh api repos/google-github-actions/auth/releases` verified 2026-05-16) |
| P17b | `grep -c "get-secretmanager-secrets@v3" substrate/skills/credential-discipline/SKILL.md` | `>= 1` (current-stable major version cited; v3.0.0 published 2025-09-03 per `gh api repos/google-github-actions/get-secretmanager-secrets/releases` verified 2026-05-16) |
| P17c | `grep -c "google-github-actions/auth@v2\\|get-secretmanager-secrets@v2" substrate/skills/credential-discipline/SKILL.md \| awk '$1 <= 2'` returns non-empty | At most two `@v2` references allowed (these document the sector-4 worked-example lag honestly — the substrate teaches `@v3`; this probe catches accidental substrate-canon regressions to `@v2`) |
| P18 | `grep -c "operating-disciplines.md.*§20" substrate/skills/credential-discipline/SKILL.md` | `>= 1` (cross-ref to canon present) |

### §9.5 Deletion of railway-access skill

| # | Probe | Expected outcome |
|---|---|---|
| P19 | `test ! -f "${HOME}/.claude/skills/railway-access/SKILL.md" && echo "deleted"` | `deleted` (matches arc-25-build-directive.md smoke beat #5) |
| P20 | `test ! -d "${HOME}/.claude/skills/railway-access" && echo "dir-deleted"` | `dir-deleted` (parent directory also gone since file was the only content) |

### §9.6 Scope guard

| # | Probe | Expected outcome |
|---|---|---|
| P21 | `git diff main..arc-25/build --stat -- substrate/MAJOR_PLINY.md substrate/MAJOR_POLYBIUS.md` | Empty output (no modifications — A11 scope guard) |
| P22 | `git diff main..arc-25/build --stat -- substrate/templates/ app/` | Empty output (no modifications — A11 scope guard) |
| P23 | `git diff main..arc-25/build --name-only \| sort` | Matches exactly the set: `substrate/CAPTAIN_DAEDALUS.md`, `substrate/CAPTAIN_ADA.md`, `substrate/CAPTAIN_ARGUS.md`, `substrate/CAPTAIN_BARTLEBY.md`, `substrate/install.sh`, `substrate/operating-disciplines.md`, `substrate/skills/credential-discipline/SKILL.md`, `agents/design/arc-25/design.md` (+ optionally `agents/design/arc-25/<any-ARGUS-revisions>`) |

### §9.7 App-adapter sanity (build-check, not VERA work but worth flagging)

| # | Probe | Expected outcome |
|---|---|---|
| P24 | `cd app && npm run gen-data 2>&1 \| grep -i "error\|invalid"` | Empty (new skill's frontmatter validates against the Zod schema) — falls under ADA's §5.1 build-check sanity, not VERA verification; documented here so ADA runs it before commit. |

---

## §10. Self-assessed weak points (per CAPTAIN_DAEDALUS §6.2)

Six weak points named. Each names a brittle assumption + why this shape was chosen anyway.

### §10.1 The §20 prose duplicates content across operating-disciplines.md and SKILL.md

**Weak point:** Two Railway-specific patterns (reference-variable-resolution + `railway run --service` anti-pattern) live in BOTH `operating-disciplines.md` §20.5 AND the new skill's "Railway-specific patterns" section. Two surfaces with substantively identical prose — future edits risk drift between them.

**Why this shape anyway:** Discoverability is bidirectional — a future agent searching `operating-disciplines.md` for "Railway" should find the patterns in canon context; a future agent reading the skill end-to-end should find them in worked-example context. The cross-refs (§20.5 → skill, skill → §20.5) are the discipline that mitigates drift. Choosing one surface only would silently fail one of the two reader paths.

### §10.2 The five anti-patterns may not exhaust future failure modes

**Weak point:** §20.2 enumerates five named anti-patterns. The substrate doc commits to "any credential in agent-reachable scope eventually surfaces" as the shared root cause, but a future creative anti-pattern not on the list (e.g., environment-variable-laundering via a Docker layer, secret-injection via a build-time arg) could be proposed without surfacing as an anti-pattern violation in an ARGUS audit.

**Why this shape anyway:** The five named anti-patterns + the explicit root-cause framing is the substrate's empirical record; expanding speculatively to anticipate every possible future variant would inflate §20 into an unbounded list that nobody reads. The discipline lives in the root-cause framing, not in the enumeration; ARGUS's job (per §5.3 of this design, the new §6.8 in ARGUS's envelope) includes flagging novel patterns that share the root cause even when not on the list.

### §10.3 The directive A3 source-location inaccuracy could mask a deeper brief gap

**Weak point:** Directive A3 says refusal-as-signal "currently lives in `~/.claude/CLAUDE.md` as a harness-rule." Empirically it does not — it lives in railway_stoa workspace memory at `feedback_credential_friction_script_batched.md`. This design uses the empirical wording and proceeds; the residual_question_for_argus surfaces the discrepancy. The risk: if the directive's authors had a different rule in mind (perhaps an earlier draft of `~/.claude/CLAUDE.md` that was never committed, or a different rule they thought lived there), this design might be promoting the wrong rule to canon under a similar-sounding name.

**Why this shape anyway:** The substance of refusal-as-signal in the workspace-memory file is unambiguously what the directive's prose describes (halt-no-retry-on-refusal). Both the directive A3 text and the workspace-memory wording converge on the same discipline; the source-location inaccuracy is mechanical (where it lives) not substantive (what it is). Proceeding with the substance + surfacing the discrepancy to ARGUS is the honest middle. **Rev2 status:** ARGUS rev1 audit confirmed non-load-bearing; the substrate-promotion stands as written. Directive-clarification follow-up tracked in §8.1.2.

### §10.4 The CAPTAIN envelope additions are reasonably uniform but per-seat adaptation may have under-shot

**Weak point:** Each of the four envelope additions reads similar to the others — same canonical-pattern statement, same anti-pattern reference, same cross-ref to the skill. The per-seat verb adaptation (DAEDALUS designs, ADA refuses-and-redirects, ARGUS flags, BARTLEBY cross-refs) is real but compact. A future maintainer reading the four envelopes side-by-side might perceive them as boilerplate and feel pressure to consolidate to "see operating-disciplines.md §20" — which would lose the per-seat operational specificity.

**Why this shape anyway:** Each addition's prose tells the seat what to DO at its specific decision moment (design's verification-probes-section requirement for DAEDALUS; surface-via-verdict for ADA; `load_bearing: true` risk classification for ARGUS; `tag: credential_leak` for BARTLEBY). Consolidating to "see §20" would remove the operational specificity and turn the envelope addition into a pointer instead of a directive. Per A5, "wording adapts to seat" is explicit; the four additions adapt the verb but share the substrate-canon reference, which is the correct shape.

### §10.5 The skill's gcloud commands embed assumptions about a single project / single repo binding

**Weak point:** The gcloud command block in the skill assumes one GCP project, one GitHub repo, one service account. Real workspaces frequently have multiple repos sharing one GCP project (sector-4 + others), or one repo deploying to multiple GCP projects (staging + prod), and the commands as written don't address either. Future engagements may need to extend the binding multi-dimensionally and discover the skill's commands don't directly answer the question.

**Why this shape anyway:** The substrate canon is the structural pattern (WIF + Secret Manager + bounded workflow), not the specific multi-project topology. The skill's worked example matches what sector-4 actually does; the commands are reproducible and testable; future agents needing multi-project topology will read the canonical pattern, recognize the binding is per-repo-per-SA, and extend appropriately. Over-specifying multi-project variants upfront would balloon the skill into a GCP-administration tutorial rather than a substrate worked example.

### §10.6 The deletion of `~/.claude/skills/railway-access/SKILL.md` is asymmetric — user-tier-only

**Weak point:** The deletion happens at user-tier (`~/.claude/skills/railway-access/`) where the install.sh-substrate-deploy-trail does NOT track it — `install.sh` doesn't manage `~/.claude/skills/` user-additions, only substrate-canonical skills. If the PRINCIPAL ever copy-pastes the skill back into `~/.claude/skills/` from a backup or another machine, the deletion gets undone silently. Similarly, other users / machines may still have the rejected-pattern skill on disk after this arc ships; there is no mechanism to propagate the deletion.

**Why this shape anyway:** The substrate's only canonical skill-management surface is the substrate-tier `substrate/skills/` directory, which `install.sh` deploys + manages via the staleness scan. User-tier skills like the old `railway-access/` are by definition out of that management loop (they pre-date the substrate, or were added by the human directly). The substrate canon being correct (§20 + new skill) is what guards against re-derivation; the deletion is a one-time cleanup for THIS machine and is in scope for THIS arc. Multi-machine propagation is a separate concern (the substrate doesn't currently address per-machine sync at all) and out of scope per A11.

---

## §11. Cross-reference index

For ARGUS, ADA, CATO, VERA, ZENO traceability:

| Surface | Location |
|---|---|
| Arc directive | `substrate/arcs/arc-25-build-directive.md` |
| Work-unit ticket | `stoa--p5g` (body + 4 comments + activation handshakes) |
| Primary input prose | stoa--p5g body, 2026-05-15T22:54Z comment, **2026-05-16T05:53Z FINAL ARCHITECTURE DECISION** (load-bearing), 2026-05-16T08:05Z Railway-footnote comment |
| Worked-example workflow | `denson/sector-4/.github/workflows/deploy-dev-ariadne.yml` (private repo; PRINCIPAL can grant access) |
| Empirical refusal-as-signal wording | `C:\Users\denso\.claude\file-history\78a664fb-106a-4a55-9401-93c1c792ab33\5108d7227e3b6f4f@v3` (`feedback_credential_friction_script_batched.md`, constraint #6) |
| Existing rejected-pattern user-tier skill | `~/.claude/skills/railway-access/SKILL.md` (deleted in Phase 2) |
| GCP keyless-auth narrative reference | https://cloud.google.com/blog/products/identity-security/enabling-keyless-authentication-from-github-actions |
| `google-github-actions/auth@v3` docs | https://github.com/google-github-actions/auth (v3.0.0 published 2025-08-28, v3 tag 2025-09-03; verified via `gh api repos/google-github-actions/auth/releases` 2026-05-16) |
| `get-secretmanager-secrets@v3` docs | https://github.com/google-github-actions/get-secretmanager-secrets (v3.0.0 published 2025-09-03; verified via `gh api repos/google-github-actions/get-secretmanager-secrets/releases` 2026-05-16) |
| Claude Code git-proxy structural reference | https://www.anthropic.com/engineering/claude-code-sandboxing |

---

## §12. Summary for ARGUS (one-paragraph entry-point)

Arc 25 lands credential-discipline as substrate canon at six touch-points: new `operating-disciplines.md` §20 (with refusal-as-signal as §20.3, Railway-specific notes as §20.5); new `substrate/skills/credential-discipline/SKILL.md` (worked-example skill, authorship Denson Smith IMMUTABLE); envelope additions to four CAPTAINs (DAEDALUS §6.6, ADA §5.7, ARGUS §6.8, BARTLEBY §6.7 — plus extension of BARTLEBY's verdict-format `tag:` enum at line 142 to include `credential_leak`); `install.sh` SKILL_NAMES entry; deletion of user-tier `~/.claude/skills/railway-access/` (parent dir + file). Load-bearing structural choices: (a) refusal-as-signal as subsection of §20 not peer §21 (rationale §3); (b) Railway-specific patterns duplicated across §20.5 and skill (rationale §10.1); (c) install.sh requires explicit SKILL_NAMES entry verified via three loop sites (§6); (d) GitHub Actions deps pinned at `@v3` for both `google-github-actions/auth` and `get-secretmanager-secrets` (current-stable majors as of 2026-05-16, verified via `gh api`; sector-4 worked example currently lags at `@v2` and that lag is documented honestly in §4). **Rev2 status:** ARGUS rev1 audit returned FAIL on two surgical findings (r1 GitHub Action version drift `@v2`→`@v3`; r2 BARTLEBY enum extension for `credential_leak`); both fixed in this revision. The three rev1 residual questions were confirmed non-load-bearing by ARGUS. Most important remaining weak point: the §20 prose duplicates Railway-specific content across operating-disciplines.md and the new skill (§10.1) — accepted as deliberate bidirectional discoverability with cross-refs as the drift-mitigation discipline.

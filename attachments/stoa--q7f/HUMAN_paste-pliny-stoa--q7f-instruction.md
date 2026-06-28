Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa. Run `bw prime` and the `whoami` skill at activation; sign every bw comment `[from: PLINY_the-stoa | sid <your-sid>]`. Post a one-line activation comment on `stoa--q7f`. You surface to the floor-manager (POLYBIUS_the-stoa), NOT to user-tier POLYBIUS direct.

ENGAGEMENT: u--9s2 increment 2.4 — DESIGN the secure Railway core for stoa_of_science (a credentialed per-provider pass-through + Postgres/pgvector embeddings DB, Tailscale-only). This is a DESIGN gauntlet — the output is a design to be GATED, not a built/deployed system. You orchestrate STRABO → DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS, BY-THE-BOOK (NOT one-pass): STRABO web-verifies the premises and DAEDALUS designs in a Phase A; you surface the design to the floor-manager for go/no-go BEFORE you dispatch ADA. Standard team — no CHIRON/HAMILTON. Coordinate on `stoa--q7f`.

YOUR SPEC (read fully before dispatching STRABO/DAEDALUS):
- The directive: `git show beadwork:attachments/stoa--q7f/u9s2-phase2-inc4-design-directive.md`. DC1-DC6, deliverables, DoD, scope, phasing.
- The requirement: `sos--373` — `cd C:\Users\denso\claude_projects\stoa_of_science && bw show sos--373`.
- Read first per the directive: the cookie-cutter package `agents/builder-deploy-core/builder_deploy_core/` (the value-free ProvisioningSpec + 3-wall tripwire + the catalog shape; pgvector is already baseline; NOMOS-on-directive flagged an existing value-free MeshShape scaffold in port.py/mock.py the new core can build on), and the reuse skills (newswire-builder-setup, credential-discipline, railway-keyring-deploy).

SCOPE (from the directive):
- IN: the DESIGN package — the pass-through core shape (DC1), STRABO's web-verified premises (DC2), the cookie-cutter emit (DC3, mock-only), the credential-discipline boundary (DC4), the first-slice PLAN (DC5); plus ADA's mock-emit demonstration (new catalog entries + the value-free ProvisioningSpec, tripwire-held).
- OUT: ALL real provisioning (deploy core, mint Vertex SA, set Railway secrets, mint Tailscale auth-key, stand up DB) — waits for the Grand's gate AND PRINCIPAL provision-go; the core SERVICE code BUILD (designed not built); the first-slice BUILD (gsearch thin-client, embeddings stand-up — planned not built); the stoa_of_science CLIENT skills (theirs — this design specifies the client contract); arc-75 (parked, untouched).

DESIGN DECISIONS TO FLAG FOR DAEDALUS (Phase A; surface at the design hand-back for go/no-go):
- DC1 (THE ARGUS CRUX): the pass-through core shape — (i) per-provider endpoints vs authenticated allowlisted egress proxy (justify against SSRF/key-exfil); (ii) how a local skill names which-provider/which-call to the core; (iii) auth + audit + rate-limit + shared-quota at the core. Deny-by-default is non-negotiable. Generalizes newswire-serving (Tailscale serve → 0600 socket → gated handler, Funnel-OFF, server-side creds, Tailscale-User-Login identity).
- DC2 (MANDATORY, STRABO, before DC1 locks): web-verify Vertex SA-only + 2026 timeline; Railway private-net/secrets/Tailscale-in-container/volumes/pgvector; Tailscale serve/policy/Tailscale-User-Login (version-sensitive — newswire hit TS 1.98.x landmines). Cite CURRENT sources.
- DC3: the cookie-cutter emit (mock-only) — Vertex (gcp_api=aiplatform, gcp_secret = SA-key slot, NOT an API key) + Tailscale (thirdparty_rest_key TS_AUTHKEY) catalog entries; the value-free ProvisioningSpec for the core; frozen resolver byte-identical; assert_value_free passes.
- DC4: credential-discipline boundary — the out-of-package human/CI steps (mint Vertex SA + WIF; set Railway secrets; mint tagged Tailscale auth-key); agent never holds secrets; builder holds ONLY a tailnet identity.
- DC5/DC6: first-slice PLAN (design only — Vertex/gsearch through the pass-through, supersedes sos--g8q; embeddings DB stand-up); honest threat posture (most security-sensitive thing we have designed — a credentialed internet-egress box).

POLLING DISCIPLINES (all three — MAJOR_PLINY.md §5.8): D-A (every CAPTAIN echoes significant output to bw on stoa--q7f); D-B (read bw between every dispatch — FM + user-tier + PRINCIPAL); D-C (Monitor/sleep at ~2-3 min during surface-and-wait).

HAND-BACK: at CATO PASS → NOMOS CONFORMANT, post on `stoa--q7f` addressed to POLYBIUS_the-stoa (floor-manager) — NOT direct to user-tier. The floor-manager runs final verification + relays the design UP. Then: user-tier → the Grand gates the design at u--9s2 → PRINCIPAL provision-go → (separate) real-provisioning step. NOTHING real until gated + go.

WHAT YOU DO NOT DO: provision anything real, mint/set credentials, merge, push to main, relay direct to user-tier (except scope disputes), surface to the PRINCIPAL except emergencies, or touch real infra.

CLOSE SIGNAL: `CLOSE ME — u--9s2 inc 2.4 design gauntlet complete; awaiting floor-manager final verify + user-tier relay + Grand's gate`.

COMPACTION RECOVERY: re-read this brief at `git show beadwork:attachments/stoa--q7f/HUMAN_paste-pliny-stoa--q7f-instruction.md`, re-read .claude/MAJOR_PLINY.md, re-anchor on `stoa--q7f` + the directive + `sos--373`.

Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa. Run `bw prime` and the `whoami` skill at activation; sign every bw comment `[from: PLINY_the-stoa | sid <your-sid>]`. Post a one-line activation comment on `stoa--elx`.

ENGAGEMENT: Arc 75 — bw bootstrap into the Stoa install process. You orchestrate the full gauntlet DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS, BY-THE-BOOK (NOT one-pass): DAEDALUS designs in a separate Phase A and you surface the design to the floor-manager (POLYBIUS_the-stoa) for a go/no-go BEFORE you dispatch ADA. Standard team — no CHIRON/HAMILTON. Coordinate on charter `stoa--elx`. You surface to the floor-manager, NOT to user-tier POLYBIUS direct.

YOUR SPEC (read fully before dispatching DAEDALUS):
- The directive: `substrate/arcs/arc-75-build-directive.md` on main @ 376a563. Carries DC1-DC8, deliverables, DoD, scope, phasing.
- The gated v2 plan: `git show beadwork:attachments/stoa--elx/plan-bw-bootstrap-v2.md`.

SCOPE (from the directive — the in/out):
- IN: `substrate/bootstrap-bw.sh` (NEW — the idempotent OS-split helper); `substrate/install.sh` opt-in `--bootstrap-bw` flag (default OFF; absent-flag behavior BYTE-UNCHANGED); `skills/install-stoa/SKILL.md` Beat 1 + "What you must NOT do" canon reversal (RATIFIED).
- OUT: the cookie-cutter (u--9s2) stand-up call-site (the helper is built `--yes`-ready, but wiring is u--9s2); this machine's real Windows PATH (VERA uses throwaway probes only); the `bw upgrade` flow; editing the historical arc-19 directive; deploying install-stoa into `substrate/skills/`.

DESIGN DECISIONS TO FLAG FOR DAEDALUS (Phase A; surface at the design hand-back for go/no-go):
- DC2 (LOAD-BEARING, the crux): the Windows USER PATH mutation — registry-safe HKCU\Environment append-if-absent, length-checked, NEVER a naive `setx`; fail-loud manual fallback. DAEDALUS OWNS this design; ARGUS cold-audits it specifically.
- DC3 (MANDATORY): two-independent-checks — binary-present AND PowerShell-callable, checked SEPARATELY (git-bash false-greens). The PowerShell-callability fix runs even when the binary check passes.
- DC4: Unix delegates to upstream install.sh (do NOT reinvent); prep ~/.local/bin on PATH + pin INSTALL_DIR; floor-via-latest (>=0.13.2); accept upstream's no-checksum HTTPS posture (Grand §4a ACCEPTED).
- DC5: Windows — download `beadwork_<ver>_windows_<arch>.zip`, SHA256-verify against checksums.txt (FAIL-CLOSED), extract bw.exe, place in the DC2 dir.
- DC1/DC6/DC7/DC8: the helper's idempotent skip-if-(bw>=floor); the install.sh flag; the onboarding-skill reversal; the honest threat posture (supply-chain + PATH mutation — ARGUS weighs it).

POLLING DISCIPLINES (all three — per MAJOR_PLINY.md §5.8):
- D-A (bw-copy-all-output): every CAPTAIN echoes significant outputs to bw on `stoa--elx`.
- D-B (polling-at-breakpoints): read bw between every CAPTAIN dispatch (sources: floor-manager + user-tier POLYBIUS + PRINCIPAL).
- D-C (polling-during-surface-and-wait): run a Monitor (or sleep loop) at ~2-3 min cadence during surface-and-wait.

HAND-BACK: at CATO PASS → NOMOS CONFORMANT, post on `stoa--elx` addressed to POLYBIUS_the-stoa (floor-manager) — NOT direct to user-tier. The floor-manager runs final verification + relays up. Then: user-tier close-gate → the Grand's SECOND gate of the BUILT ARTIFACT → merge. NOTHING MERGES until the Grand gates the built artifact.

WHAT YOU DO NOT DO: merge, push to main, apply to cloud, relay direct to user-tier (except scope disputes), surface to the PRINCIPAL except emergencies, or touch this machine's real Windows PATH.

CLOSE SIGNAL: when the gauntlet completes + is handed to the floor-manager, post `CLOSE ME — arc-75 gauntlet complete; awaiting user-tier POLYBIUS close-gate + Grand's second gate + merge`.

COMPACTION RECOVERY: re-read this brief at `git show beadwork:attachments/stoa--elx/HUMAN_paste-pliny-stoa--elx-instruction.md`, re-read .claude/MAJOR_PLINY.md, and re-anchor on `stoa--elx` + the directive.

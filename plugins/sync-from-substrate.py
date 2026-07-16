#!/usr/bin/env python3
"""sync-from-substrate.py — regenerate plugins/stoa/ from substrate/ source.

The plugin is a STATIC, runtime-parametrized packaging of the substrate.
substrate/ remains the canonical source (fleet-migration decision pending the
planning session); run this after any substrate change that should ship in the
next plugin version, then bump plugin.json version + tag.

Transformations (the entire install-time -> run-time parametrization delta):
  1. {{NAME_SUFFIX}} -> ""            (plugin agents are plugin-namespaced;
                                       project-suffixed seat identity is derived
                                       at RUNTIME from the workspace cwd)
  2. {{USER_TIER_DIR}}/user-beadwork -> "the sibling user-beadwork repo under
                                       the projects root (the parent directory
                                       of the workspace cwd)"
  3. A RUNTIME-IDENTITY preamble is injected into every MAJOR/CAPTAIN file,
     right after the frontmatter, stating how project identity is derived.

Author: Denson Smith
"""
import re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # the-stoa repo root
SUB = ROOT / "substrate"
DEST = ROOT / "plugins" / "stoa"

PREAMBLE = """\
> **RUNTIME IDENTITY (plugin packaging).** This file ships inside the `stoa`
> plugin and is identical across workspaces. Derive project identity at
> runtime: **project slug = the basename of the workspace working directory**
> (e.g. a seat waking in `C:\\...\\newswire_core` is `<ROLE>_newswire_core`).
> Wherever this file's conventions call for a project-suffixed seat name —
> bw signatures, Co-Authored-By seat trailers, seat-registry rows — derive it
> as `<NAME>_<slug>` at runtime. Substrate modules/templates referenced as
> `.claude/modules/...` or `.claude/templates/...` resolve under
> `${CLAUDE_PLUGIN_ROOT}/modules/` and `${CLAUDE_PLUGIN_ROOT}/templates/`.
"""

def transform(text: str) -> str:
    text = text.replace("{{NAME_SUFFIX}}", "")
    text = re.sub(r"`?\{\{USER_TIER_DIR\}\}/user-beadwork/?`?",
                  "the sibling `user-beadwork` repo under the projects root "
                  "(the parent directory of the workspace cwd)", text)
    return text

def inject_preamble(text: str) -> str:
    m = re.match(r"^(---\n.*?\n---\n)", text, re.DOTALL)
    if m:
        return m.group(1) + "\n" + PREAMBLE + "\n" + text[m.end():]
    return PREAMBLE + "\n" + text

def main():
    # clean regenerable dirs (never the .claude-plugin manifest)
    for d in ("agents", "roles", "skills", "modules", "templates", "commands"):
        shutil.rmtree(DEST / d, ignore_errors=True)
    (DEST / "agents").mkdir(parents=True)
    (DEST / "roles").mkdir(parents=True)

    for f in sorted(SUB.glob("CAPTAIN_*.md")):
        out = inject_preamble(transform(f.read_text(encoding="utf-8")))
        (DEST / "agents" / f.name).write_text(out, encoding="utf-8", newline="\n")
    for f in sorted(SUB.glob("MAJOR_*.md")):
        out = inject_preamble(transform(f.read_text(encoding="utf-8")))
        (DEST / "roles" / f.name).write_text(out, encoding="utf-8", newline="\n")

    for d in ("skills", "modules", "templates"):
        src = SUB / d
        if src.is_dir():
            shutil.copytree(src, DEST / d)
            # apply the two install-time token transforms to copied text files
            # (use-time template slots like {{RENEWAL_CRON_ID}} are preserved)
            for f in (DEST / d).rglob("*"):
                if f.is_file() and f.suffix in (".md", ".json", ".sh", ".ps1", ".py", ".txt"):
                    t = f.read_text(encoding="utf-8", errors="ignore")
                    t2 = transform(t)
                    if t2 != t:
                        f.write_text(t2, encoding="utf-8", newline="\n")

    (DEST / "commands").mkdir(parents=True)
    for role, fname in (("polybius", "MAJOR_POLYBIUS.md"), ("pliny", "MAJOR_PLINY.md"),
                        ("chiron", "MAJOR_CHIRON.md"), ("hamilton", "MAJOR_HAMILTON.md")):
        (DEST / "commands" / f"{role}.md").write_text(
            f"""---
description: Assume the {fname[6:-3].title()} role for THIS workspace (Stoa substrate, runtime identity)
---

Read `${{CLAUDE_PLUGIN_ROOT}}/roles/{fname}` in full and assume that role for
THIS workspace. Derive project identity at runtime: project slug = the basename
of the workspace working directory. Your seat name is `{fname[:-3].replace('MAJOR_','')}_<slug>`.
Follow the role file's activation discipline (bw prime, Monitor, chain of command).
""", encoding="utf-8", newline="\n")

    residual = []
    for f in DEST.rglob("*.md"):
        t = f.read_text(encoding="utf-8", errors="ignore")
        # only the two INSTALL-TIME tokens are failures; use-time slots survive
        if "{{NAME_SUFFIX}}" in t or "{{USER_TIER_DIR}}" in t:
            residual.append(str(f.relative_to(DEST)))
    if residual:
        print("RESIDUAL TOKENS (fail):", *residual, sep="\n  "); sys.exit(1)
    print("sync ok: agents=%d roles=%d commands=%d skills=%d modules=%d templates=%d" % (
        len(list((DEST/'agents').glob('*.md'))), len(list((DEST/'roles').glob('*.md'))),
        len(list((DEST/'commands').glob('*.md'))), len(list((DEST/'skills').glob('*'))),
        len(list((DEST/'modules').glob('*.md'))), len(list((DEST/'templates').glob('*')))))

if __name__ == "__main__":
    main()

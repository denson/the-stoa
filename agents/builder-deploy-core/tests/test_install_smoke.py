# author: Denson Smith
# ticket: stoa--k48 (u--9s2 Phase-2 increment 2.3 — provisioning choreography; the jd5 fold)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--k48/design-rev2.md §8.10 / §11 (the jd5 install-then-import smoke)
#
# The jd5 fold regression guard (CATO c2 plan): build + install the package into a tmp venv, import
# builder_deploy_core from OUTSIDE the source tree, and load the baseline — proving data/ is bundled by
# the intra-package package-data glob (data/ now lives INSIDE the package after the jd5 git mv). This is
# the test that would have caught the stoa--pj3 parent-relative-glob bug. Uses ONLY fixed literal tmp
# paths (pytest tmp_path / venv subdir) — no $VAR expansion in any destructive op (§8.6).

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

_PKG_ROOT = Path(__file__).resolve().parent.parent  # the builder-deploy-core/ project root (has pyproject.toml)


@pytest.mark.slow
def test_install_then_import_smoke(tmp_path):
    """Build + pip install the package into a fresh tmp venv, import from outside the tree, load the 5
    baseline entries. Proves data/ is bundled (the jd5 fold's whole point). SKIPS if the build backend
    (pip/venv) is unavailable in the sandbox — the assertion is the import-from-installed, not the env."""
    venv_dir = tmp_path / "venv"
    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True,
                       capture_output=True, text=True, timeout=180)
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as exc:
        pytest.skip(f"venv unavailable in sandbox: {exc}")

    if sys.platform == "win32":
        py = venv_dir / "Scripts" / "python.exe"
    else:
        py = venv_dir / "bin" / "python"

    install = subprocess.run(
        [str(py), "-m", "pip", "install", "--no-build-isolation", str(_PKG_ROOT)],
        capture_output=True, text=True, timeout=300,
    )
    if install.returncode != 0:
        # build-isolation off can fail if setuptools missing in the fresh venv; retry WITH isolation.
        install = subprocess.run(
            [str(py), "-m", "pip", "install", str(_PKG_ROOT)],
            capture_output=True, text=True, timeout=300,
        )
    if install.returncode != 0:
        pytest.skip(f"pip install unavailable/failed in sandbox:\n{install.stderr[-1500:]}")

    # Import from a CWD that is NOT the source tree, so the installed package (with bundled data/) is used.
    probe = (
        "import builder_deploy_core.resolution as _r;"  # populates kind-tables
        "from builder_deploy_core import dataload;"
        "b = dataload.load_baseline();"
        "assert len(b) == 5, ('baseline len', len(b));"
        "print('OK', len(b))"
    )
    run = subprocess.run([str(py), "-c", probe], cwd=str(tmp_path),
                         capture_output=True, text=True, timeout=120)
    assert run.returncode == 0, (
        f"installed-import smoke FAILED — data/ likely not bundled:\nSTDOUT:{run.stdout}\nSTDERR:{run.stderr}")
    assert "OK 5" in run.stdout, run.stdout

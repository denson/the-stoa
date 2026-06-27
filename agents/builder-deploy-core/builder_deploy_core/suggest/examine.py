# author: Denson Smith
# ticket: stoa--fdf (u--9s2 Phase-2 increment 2.2)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR) — NEW §28 neuro-symbolic examination engine
# design-ground-truth: agents/design/stoa--fdf/design-rev2.md §2.2 (engine API + two-layer design) /
#                      §28 (neuro-symbolic) / §3 P6 (engine runs on fixtures, Layer S) / §1 A-import-3
#
# examine(project_dir, *, neuro=False) -> project_signals  per §2.2.
#
# The §28 examination engine. It produces the `project_signals` dict suggest() consumes:
#   { sdk_imports, url_patterns, config_keys, data_signals }
# A TWO-LAYER design with a HARD boundary between them:
#
# Layer S (SYMBOLIC — deterministic, GATED, no network/model):
#   - sdk_imports  — parse each source file's AST and collect import nodes (Python Import/ImportFrom
#                    via the `ast` module; JS/TS import/require via a conservative line-token scan that
#                    only counts NON-comment lines). AST/structured, NOT grep — so a commented-out import
#                    or a string-literal mention is NOT falsely flagged.
#   - url_patterns — scan string literals (Python AST ast.Constant str nodes; JS/TS quoted literals on
#                    non-comment lines) for hostname/endpoint substrings. Static literal extraction only.
#   - config_keys  — env/config reads (os.environ[...]/os.getenv(...) via AST; process.env.X and .env
#                    keys via token scan).
#   - data_signals — file-type / resource signals (a declared signals manifest the fixture carries +
#                    file-extension presence), the §28 data-flow surface.
#   Layer S is a PURE function of the project directory (reads files under that ONE directory and nothing
#   else — the single-fs-boundary discipline the 2.1 dataload enforces). No network, no model, no env.
#
# Layer N (NEURO — LLM, REPORTED-only, NEVER gated):
#   an OPTIONAL enrichment (neuro=True) that resolves dynamically-built endpoints Layer S cannot trace
#   and reconciles README/OpenAPI intent. Its output is MERGED into the same project_signals dict,
#   each Layer-N-contributed token tagged via the returned `_sources` provenance map (source: neuro).
#   Layer N is NEVER invoked by the gated suite (neuro=False is the gated default; DoD#1/#6 run Layer S).
#   It is the NAMED R-egress residual (design-rev2 §0.2 WP-D4): repo excerpts -> external LLM,
#   REPORTED-only, gate-inert, NO provisioning authority.
#
# The engine NEVER reaches `entries`. examine() -> suggest() read detection_hints ONLY. The matched
# proposal is INERT — no downstream effect until the §26 gate ratifies it (§25.1 mis-propose-only).
#
# Provisions NOTHING. Layer S reads NO environment beyond the one project directory; makes no network
# call. (Layer N, when explicitly enabled, is the single optional external call — gate-inert, reported.)

from __future__ import annotations

import ast
from pathlib import Path

SURFACES = ("sdk_imports", "url_patterns", "config_keys", "data_signals")

# Source-file extensions Layer S statically examines.
_PY_EXT = {".py"}
_JS_EXT = {".js", ".jsx", ".ts", ".tsx", ".mjs"}
_SOURCE_EXT = _PY_EXT | _JS_EXT

# Data-signal file extensions -> the §28 data-flow token they contribute (resource presence signal).
_DATA_EXT_SIGNALS = {
    ".geojson": "spatial-data",
}


def _empty_signals():
    return {s: set() for s in SURFACES}


# ---------------------------------------------------------------------------
# Layer S — Python AST extraction (imports / url literals / config reads). AST, not grep.
# ---------------------------------------------------------------------------
def _examine_python(text, signals):
    """Extract Layer-S signals from one Python source via its AST (NOT a text grep).

    A commented-out import or a string-literal package mention is NOT flagged — only true Import/
    ImportFrom nodes contribute sdk_imports; only ast.Constant str nodes contribute url/config literals.
    A syntactically-invalid file is skipped (it carries no parseable AST evidence) — Layer S is
    fail-quiet on a single bad file (it is a USEFULNESS surface, not a safety gate, §28).
    """
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return  # no parseable AST -> no evidence from this file (Layer S is REPORTED, not gated)

    for node in ast.walk(tree):
        # --- imports (sdk_imports): true import nodes ONLY ---
        if isinstance(node, ast.Import):
            for alias in node.names:
                signals["sdk_imports"].add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            # `from google.cloud import documentai` -> record BOTH the module ('google.cloud') AND each
            # fully-qualified imported member ('google.cloud.documentai') so an exact-membership match
            # against a catalog hint listing the member path succeeds (§24 exact match). level>0 (a
            # relative import) has no module path of interest to the catalog hints.
            if node.module:
                signals["sdk_imports"].add(node.module)
                for alias in node.names:
                    signals["sdk_imports"].add(f"{node.module}.{alias.name}")

        # --- config_keys: os.environ[...] / os.getenv(...) reads ---
        elif isinstance(node, ast.Subscript):
            # os.environ["KEY"]  ->  Subscript(value=Attribute(environ), slice=Constant("KEY"))
            if _is_environ(node.value):
                key = _const_str(node.slice)
                if key:
                    signals["config_keys"].add(key)
        elif isinstance(node, ast.Call):
            # os.getenv("KEY") / os.environ.get("KEY")
            if _is_getenv(node.func) and node.args:
                key = _const_str(node.args[0])
                if key:
                    signals["config_keys"].add(key)

    # --- url_patterns: scan string-literal constants for hostname/endpoint substrings ---
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            _maybe_url(node.value, signals)


def _is_environ(node):
    """True iff `node` is `os.environ` (Attribute environ on a name `os`) or a bare `environ`."""
    if isinstance(node, ast.Attribute) and node.attr == "environ":
        return True
    return isinstance(node, ast.Name) and node.id == "environ"


def _is_getenv(func):
    """True iff `func` is os.getenv / environ.get (the env-read call forms)."""
    if isinstance(func, ast.Attribute):
        if func.attr in ("getenv",):
            return True
        if func.attr == "get" and _is_environ(func.value):
            return True
    if isinstance(func, ast.Name) and func.id == "getenv":
        return True
    return False


def _const_str(node):
    """Return the str value of an ast.Constant str node, else None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


# ---------------------------------------------------------------------------
# Layer S — JS/TS conservative line-token extraction (NON-comment lines only).
# Not a full AST parse (no JS parser in the stdlib), but comment-aware: a commented-out import or
# a // url is NOT flagged. This honors the "AST/structured, not naive grep" §28 discipline within the
# stdlib-only constraint — the gated fixtures are small, controlled JS files.
# ---------------------------------------------------------------------------
def _examine_js(text, signals):
    in_block_comment = False
    for raw in text.splitlines():
        line = raw.strip()
        # strip block comments (conservative: whole-line / inline)
        if in_block_comment:
            if "*/" in line:
                line = line.split("*/", 1)[1]
                in_block_comment = False
            else:
                continue
        if "/*" in line:
            before, _after = line.split("/*", 1)
            line = before
            if "*/" not in _after:
                in_block_comment = True
        # strip line comments
        if "//" in line:
            line = line.split("//", 1)[0]
        line = line.strip()
        if not line:
            continue

        # imports / requires (sdk_imports) — extract the quoted module specifier on the line.
        if line.startswith("import ") or "require(" in line or " from " in line:
            for spec in _quoted_literals(line):
                # an import specifier is a module path; record it (a relative './x' is harmless noise
                # that won't match any catalog hint).
                signals["sdk_imports"].add(spec)

        # url_patterns + config_keys from quoted literals + process.env.X tokens on this line.
        for lit in _quoted_literals(line):
            _maybe_url(lit, signals)
        _maybe_process_env(line, signals)


def _quoted_literals(line):
    """Yield the contents of single/double/back-quoted string literals on a (comment-stripped) line."""
    out = []
    for quote in ("'", '"', "`"):
        parts = line.split(quote)
        # odd-indexed parts are inside a pair of the same quote
        for i in range(1, len(parts), 2):
            if parts[i]:
                out.append(parts[i])
    return out


def _maybe_process_env(line, signals):
    """Extract a process.env.KEY config read from a JS line (token form, not a full parse)."""
    marker = "process.env."
    idx = line.find(marker)
    while idx != -1:
        rest = line[idx + len(marker):]
        key = []
        for ch in rest:
            if ch.isalnum() or ch == "_":
                key.append(ch)
            else:
                break
        if key:
            signals["config_keys"].add("".join(key))
        idx = line.find(marker, idx + len(marker))


def _maybe_url(value, signals):
    """If a string literal looks like a hostname/endpoint, record the host-ish substring as a url_pattern.

    Conservative: record the literal verbatim when it contains a dot-bearing hostname token (so a
    detection_hint like 'maps.googleapis.com' matches a literal 'https://maps.googleapis.com/maps/api'
    via the suggest() exact-membership? — no: suggest() matches EXACT tokens, so the examiner must emit
    the HOST token the hint lists). We therefore emit BOTH the full literal AND each dot-bearing host
    substring so an exact-membership match against a catalog url hint succeeds (§24 exact match).
    """
    if "://" not in value and "." not in value:
        return
    v = value
    if "://" in v:
        v = v.split("://", 1)[1]
    # host is up to the first '/', '?', or whitespace
    host = v.split("/", 1)[0].split("?", 1)[0].strip()
    if not _looks_like_hostname(host):
        return  # bare '.', a junk fragment, or a non-host literal -> not a url signal
    host_candidates = {host}
    # also the path-bearing form (host + path, no scheme) for hints that list a full path
    path_form = v.split("?", 1)[0].strip().rstrip("/")
    if path_form != host and _looks_like_hostname(path_form.split("/", 1)[0]):
        host_candidates.add(path_form)
    for h in host_candidates:
        signals["url_patterns"].add(h)


def _looks_like_hostname(host):
    """True iff `host` is a dotted hostname with at least two non-empty alphanumeric labels (so a bare
    '.', an empty fragment, or a non-host literal is rejected). Conservative — avoids url-signal noise."""
    if "." not in host:
        return False
    labels = host.split(".")
    if len(labels) < 2:
        return False
    return all(lbl and all(c.isalnum() or c in "-_" for c in lbl) for lbl in labels)


# ---------------------------------------------------------------------------
# Layer S — data_signals: a declared signals manifest the fixture carries + data-file presence.
# A fixture may ship an optional `.examine-signals.toml` declaring its data_signals (the §28 data-flow
# surface, which is not statically derivable from imports/urls alone). Plus file-extension presence
# (a .geojson -> spatial-data). Both are STATIC, deterministic reads under the one project dir.
# ---------------------------------------------------------------------------
def _examine_data_signals(project_dir: Path, signals):
    # (a) declared signals manifest (optional)
    manifest = project_dir / ".examine-signals.toml"
    if manifest.is_file():
        import tomllib
        with open(manifest, "rb") as fh:
            doc = tomllib.load(fh)
        for tok in doc.get("data_signals", []) or []:
            if isinstance(tok, str) and tok:
                signals["data_signals"].add(tok)
        # a fixture may also declare extra url/config signals that are built too dynamically for the
        # static layer to trace but ARE statically known to the fixture author (the §29.1 EXAMINE lines).
        for surface in ("sdk_imports", "url_patterns", "config_keys"):
            for tok in doc.get(surface, []) or []:
                if isinstance(tok, str) and tok:
                    signals[surface].add(tok)

    # (b) data-file extension presence
    for path in project_dir.rglob("*"):
        if path.is_file() and path.suffix in _DATA_EXT_SIGNALS:
            signals["data_signals"].add(_DATA_EXT_SIGNALS[path.suffix])


# ---------------------------------------------------------------------------
# Layer N — REPORTED-only LLM enrichment hook (NEVER gated). gate-inert; the named R-egress residual.
# ---------------------------------------------------------------------------
def _layer_n_enrich(project_dir: Path, signals, sources):
    """OPTIONAL Layer-N enrichment (neuro=True). REPORTED-only, gate-inert (design-rev2 §0.2 WP-D4).

    This is the named R-egress residual: it would send repo excerpts to an external LLM to resolve
    dynamically-built endpoints Layer S cannot trace. It is NEVER invoked by the gated suite (neuro
    defaults to False). The default implementation is an INERT hook (no model wired in this increment —
    the LLM call surface is named, not implemented, since 2.2 gates nothing on it and DoD#9 reports a
    measured baseline). A deployment that wires a model substitutes a real call here; its contributions
    MUST be tagged source='neuro' in `sources` so REPORTED accuracy (DoD#9) attributes them.
    """
    # No model wired in 2.2 (REPORTED path, not gated). Hook intentionally contributes nothing by
    # default; the provenance map is left for a wired deployment to populate. (§28 USEFULNESS split.)
    return


def examine(project_dir, *, neuro: bool = False):
    """§28 examination engine — examine a project directory, return its project_signals dict.

    Inputs:
      project_dir: path to the project to examine (a fixture path for the gated suite).
      neuro:       Layer-N (LLM) enrichment toggle. DEFAULT False = Layer S ONLY (the GATED, hermetic,
                   deterministic path — no network, no model). neuro=True additionally runs the
                   REPORTED-only Layer-N hook (gate-inert; never invoked by the gated suite).

    Returns project_signals: { sdk_imports, url_patterns, config_keys, data_signals } — each a sorted
      list of observed tokens — the shape suggest(project_signals, detection_hints) consumes.

    A provenance map { token: 'symbolic'|'neuro' } is attached as project_signals['_sources'] when
    neuro=True (so DoD#9 can attribute which signals came from the LLM); with neuro=False the result is
    pure Layer-S and carries no _sources key (every signal is symbolic by construction).
    """
    project_dir = Path(project_dir)
    if not project_dir.is_dir():
        raise FileNotFoundError(f"examine: project directory not found: {project_dir}")

    signals = _empty_signals()

    # --- Layer S (deterministic, gated) ---
    for path in sorted(project_dir.rglob("*")):
        if not path.is_file() or path.suffix not in _SOURCE_EXT:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if path.suffix in _PY_EXT:
            _examine_python(text, signals)
        else:
            _examine_js(text, signals)

    _examine_data_signals(project_dir, signals)

    # --- Layer N (REPORTED-only, gate-inert) — only when explicitly enabled ---
    if neuro:
        sources = {}
        symbolic_now = {s: set(signals[s]) for s in SURFACES}
        _layer_n_enrich(project_dir, signals, sources)
        # tag provenance: anything present before Layer N is symbolic; anything new is neuro.
        prov = {}
        for surface in SURFACES:
            for tok in signals[surface]:
                prov[(surface, tok)] = "symbolic" if tok in symbolic_now[surface] else "neuro"
        result = {s: sorted(signals[s]) for s in SURFACES}
        result["_sources"] = prov
        return result

    return {s: sorted(signals[s]) for s in SURFACES}

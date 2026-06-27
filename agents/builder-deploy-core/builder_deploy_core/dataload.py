# author: Denson Smith
# ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--pj3/design-rev2.md §2.3 (purity) / §2.4 (single fs boundary) /
#                       §2.4.1 (fail-closed DATA-load-validation contract)
#
# THE ONE filesystem boundary (§2.3 audit point). This module — and ONLY this module — performs
# filesystem I/O, and it touches ONLY files under the package's own data/ root (resolved relative to
# __file__, NEVER from an env var or CWD). No os.environ, no network, no clock, no subprocess.
#
# §2.4.1 fail-closed contract: every load function VALIDATES its DATA body on load and RAISES
# DataIntegrityError (no partial load) on ANY invariant violation, BEFORE any caller receives a table.
# A violation raises and the load returns NOTHING — no degraded dict escapes the boundary.

from __future__ import annotations

import tomllib
from pathlib import Path

from builder_deploy_core.errors import DataIntegrityError

# The ONE DATA root: the package's own data/ subdir, resolved relative to this file (§2.3 / §2.4).
# builder_deploy_core/dataload.py -> parent is builder_deploy_core/, which now holds data/ INSIDE the
# package (jd5 fold, stoa--k48): the data root is the package's own data/ subdir, not a sibling.
_DATA_ROOT = Path(__file__).resolve().parent / "data"


# ---------------------------------------------------------------------------
# §2.4.1 SSoT constants — the named expected sets the load-validation checks against.
# These live INSIDE dataload (not in a fixtures file) so the baseline set-equality check is against
# the design's §3.1 enumeration directly, immune to a doubled-surface fixtures drift (WP-3).
# ---------------------------------------------------------------------------
EXPECTED_BASELINE = {
    ("gcp_api", "gemini-embedding"),
    ("gcp_api", "gemini-search"),
    ("railway_var", "DATABASE_URL"),
    ("gcp_secret", "POSTGRES_PASSWORD"),
    ("db_extension", "pgvector"),
}

EXPECTED_KIND_ENUM = {"gcp_api", "gcp_secret", "railway_var", "db_extension", "thirdparty_rest_key"}

EXPECTED_SCOPE_BEARING = {"gcp_api", "gcp_secret", "thirdparty_rest_key"}

# On-disk category file-stem <-> design category name. `/` is not a portable filename char, so the
# design's category name `document/data` is stored as the stem `document-data` (§2.2 / §2.5). The
# loader holds the single stem->name map so resolve() still sees the exact design category strings.
_STEM_TO_CATEGORY = {
    "geospatial": "geospatial",
    "document-consuming": "document-consuming",
    "document-data": "document/data",
}

# Alias categories: byte-identical templates of a primary category (§3.2 / WP-4). They are real
# category NAMES resolve() consumes (resolve's LIBRARY carries them), but they are EXCLUDED from the
# discovery CATEGORIES bundle so best_fit_emergent_category (G2) does not double-count an alias as a
# competing same-size subset. Mirrors the Phase-1 prototype: resolve.LIBRARY has document/data;
# discovery catalog.CATEGORIES has ONLY geospatial + document-consuming (discovery-check RESULTS §"Grounding").
_ALIAS_CATEGORIES = {"document/data"}


# ---------------------------------------------------------------------------
# Low-level TOML read (the only open()/tomllib.load in the core, scoped to data/).
# ---------------------------------------------------------------------------
def _read_toml(path: Path) -> dict:
    if not path.is_file():
        raise DataIntegrityError(f"DATA file missing: {path}")
    with open(path, "rb") as fh:
        return tomllib.load(fh)


def _is_entry(obj) -> bool:
    """A well-typed §3 entry: a {kind, name} table with non-empty string values."""
    return (
        isinstance(obj, dict)
        and isinstance(obj.get("kind"), str) and obj["kind"]
        and isinstance(obj.get("name"), str) and obj["name"]
    )


# ---------------------------------------------------------------------------
# §2.4.1 baseline — set-equality vs EXPECTED_BASELINE (the r2-worked surface).
# ---------------------------------------------------------------------------
def load_baseline(data_root: Path | None = None) -> list:
    """Load + VALIDATE data/baseline.toml. Returns the §3.1 baseline as a list of {kind,name} dicts.

    §2.4.1 invariant: the loaded baseline MUST be EXACTLY the 5 expected non-omittable entries
    (set-equality vs EXPECTED_BASELINE — not a length check, so a drop+add cannot slip past).
    Any missing/extra/duplicate entry or count != 5 raises DataIntegrityError, no partial load.
    """
    root = data_root if data_root is not None else _DATA_ROOT
    doc = _read_toml(root / "baseline.toml")

    raw = doc.get("entry")
    if not isinstance(raw, list) or not raw:
        raise DataIntegrityError("baseline: missing or empty [[entry]] array")
    for e in raw:
        if not _is_entry(e):
            raise DataIntegrityError(f"baseline: malformed entry (need {{kind,name}}): {e!r}")

    loaded = [(e["kind"], e["name"]) for e in raw]
    loaded_set = set(loaded)
    if len(loaded) != len(loaded_set):
        raise DataIntegrityError(f"baseline: duplicate entries present: {sorted(loaded)}")
    if loaded_set != EXPECTED_BASELINE:
        missing = EXPECTED_BASELINE - loaded_set
        extra = loaded_set - EXPECTED_BASELINE
        parts = [f"expected {len(EXPECTED_BASELINE)} entries, got {len(loaded_set)}"]
        if missing:
            parts.append(f"missing {sorted(missing)}")
        if extra:
            parts.append(f"unexpected {sorted(extra)}")
        raise DataIntegrityError("baseline: " + "; ".join(parts))

    return [{"kind": k, "name": n} for (k, n) in loaded]


# ---------------------------------------------------------------------------
# §2.4.1 kinds — enum / scope_bearing subset / well-typed pairing (the r1 surface).
# Returns the triple resolution/__init__.py assigns into resolve's module globals (§2.1.1).
# ---------------------------------------------------------------------------
def load_kinds(data_root: Path | None = None):
    """Load + VALIDATE data/kinds.toml. Returns (KIND_ENUM:set, SCOPE_BEARING_KINDS:set,
    KEY_BEARING_PAIRING:dict[(kind,name) -> (kind,name)]).

    §2.4.1 invariants:
      - kind_enum == EXPECTED_KIND_ENUM (the 5-kind set);
      - scope_bearing is a NON-EMPTY subset of kind_enum, equal to EXPECTED_SCOPE_BEARING
        (protects the §2.1.1 import-time population from a silent empty-table fail-OPEN);
      - every key_bearing_pairing row is a well-typed {api:{kind,name}, secret:{kind,name}}
        whose api.kind / secret.kind are in kind_enum.
    Any deviation raises DataIntegrityError, no partial load.
    """
    root = data_root if data_root is not None else _DATA_ROOT
    doc = _read_toml(root / "kinds.toml")

    kind_enum_raw = doc.get("kind_enum")
    if not isinstance(kind_enum_raw, list) or not all(isinstance(k, str) for k in kind_enum_raw):
        raise DataIntegrityError("kinds: kind_enum must be an array of strings")
    kind_enum = set(kind_enum_raw)
    if kind_enum != EXPECTED_KIND_ENUM:
        raise DataIntegrityError(
            f"kinds: kind_enum mismatch; expected {sorted(EXPECTED_KIND_ENUM)}, "
            f"got {sorted(kind_enum)}")

    scope_raw = doc.get("scope_bearing")
    if not isinstance(scope_raw, list) or not all(isinstance(k, str) for k in scope_raw):
        raise DataIntegrityError("kinds: scope_bearing must be an array of strings")
    scope_bearing = set(scope_raw)
    if not scope_bearing:
        raise DataIntegrityError("kinds: scope_bearing is empty (would make derive_sa_scope return [])")
    if not scope_bearing <= kind_enum:
        raise DataIntegrityError(
            f"kinds: scope_bearing not a subset of kind_enum: {sorted(scope_bearing - kind_enum)}")
    if scope_bearing != EXPECTED_SCOPE_BEARING:
        raise DataIntegrityError(
            f"kinds: scope_bearing mismatch; expected {sorted(EXPECTED_SCOPE_BEARING)}, "
            f"got {sorted(scope_bearing)}")

    pairing_raw = doc.get("key_bearing_pairing") or []
    if not isinstance(pairing_raw, list):
        raise DataIntegrityError("kinds: key_bearing_pairing must be an array of tables")
    pairing = {}
    for row in pairing_raw:
        if not isinstance(row, dict) or "api" not in row or "secret" not in row:
            raise DataIntegrityError(f"kinds: malformed pairing row (need api+secret): {row!r}")
        api, secret = row["api"], row["secret"]
        if not _is_entry(api) or not _is_entry(secret):
            raise DataIntegrityError(f"kinds: pairing api/secret not well-typed {{kind,name}}: {row!r}")
        if api["kind"] not in kind_enum or secret["kind"] not in kind_enum:
            raise DataIntegrityError(f"kinds: pairing kind not in kind_enum: {row!r}")
        pairing[(api["kind"], api["name"])] = (secret["kind"], secret["name"])

    return kind_enum, scope_bearing, pairing


# ---------------------------------------------------------------------------
# §2.4.1 categories — the category library (each categories/*.toml file).
# Returns the LIBRARY dict resolve() consumes: category-name -> list of {kind,name}.
# ---------------------------------------------------------------------------
def load_library(data_root: Path | None = None) -> dict:
    """Load + VALIDATE data/categories/*.toml into the §3.2 category library.

    §2.4.1 invariants (per file): non-empty [[entry]] array; every entry well-typed {kind,name} with
    kind in kind_enum and non-empty name; the file stem maps to a known category name. Any deviation
    raises DataIntegrityError, no partial load.
    """
    root = data_root if data_root is not None else _DATA_ROOT
    kind_enum, _scope, _pairing = load_kinds(root)
    cat_dir = root / "categories"
    if not cat_dir.is_dir():
        raise DataIntegrityError(f"categories: directory missing: {cat_dir}")

    library: dict = {}
    for path in sorted(cat_dir.glob("*.toml")):
        stem = path.stem
        if stem not in _STEM_TO_CATEGORY:
            raise DataIntegrityError(f"categories: unknown category file stem '{stem}' ({path})")
        cat_name = _STEM_TO_CATEGORY[stem]
        doc = _read_toml(path)
        raw = doc.get("entry")
        if not isinstance(raw, list) or not raw:
            raise DataIntegrityError(f"categories[{cat_name}]: missing or empty [[entry]] array")
        entries = []
        for e in raw:
            if not _is_entry(e):
                raise DataIntegrityError(
                    f"categories[{cat_name}]: malformed entry (need {{kind,name}}): {e!r}")
            if e["kind"] not in kind_enum:
                raise DataIntegrityError(
                    f"categories[{cat_name}]: entry kind '{e['kind']}' not in kind_enum")
            entries.append({"kind": e["kind"], "name": e["name"]})
        library[cat_name] = entries

    if not library:
        raise DataIntegrityError("categories: no category files found")
    return library


# ---------------------------------------------------------------------------
# §2.4.1 catalog — each catalog/*.toml record.
# Returns (CATALOG dict, CATEGORIES dict) for the discovery layer.
# ---------------------------------------------------------------------------
def load_catalog(data_root: Path | None = None):
    """Load + VALIDATE data/catalog/*.toml into the §22 CATALOG, and derive the §22 CATEGORIES
    bundle from the category library.

    §2.4.1 invariants (per record): required keys present (service-id, entries, gcp_api, category);
    entries a non-empty array of well-typed {kind,name} with kind in kind_enum; category is a known
    category name or the literal 'none'. Cross-body: every referenced category names a known
    categories/*.toml stem or is 'none'. Any deviation raises DataIntegrityError, no partial load.
    """
    root = data_root if data_root is not None else _DATA_ROOT
    kind_enum, _scope, pairing = load_kinds(root)
    library = load_library(root)
    known_categories = set(library.keys())

    cat_dir = root / "catalog"
    if not cat_dir.is_dir():
        raise DataIntegrityError(f"catalog: directory missing: {cat_dir}")

    catalog: dict = {}
    for path in sorted(cat_dir.glob("*.toml")):
        doc = _read_toml(path)
        for key in ("service-id", "entries", "gcp_api", "category"):
            if key not in doc:
                raise DataIntegrityError(f"catalog[{path.stem}]: missing required key '{key}'")
        sid = doc["service-id"]
        if not isinstance(sid, str) or not sid:
            raise DataIntegrityError(f"catalog[{path.stem}]: service-id must be a non-empty string")

        raw = doc["entries"]
        if not isinstance(raw, list) or not raw:
            raise DataIntegrityError(f"catalog[{sid}]: entries must be a non-empty array")
        entries = []
        for e in raw:
            if not _is_entry(e):
                raise DataIntegrityError(f"catalog[{sid}]: malformed entry (need {{kind,name}}): {e!r}")
            if e["kind"] not in kind_enum:
                raise DataIntegrityError(f"catalog[{sid}]: entry kind '{e['kind']}' not in kind_enum")
            entries.append({"kind": e["kind"], "name": e["name"]})

        category = doc["category"]
        if not isinstance(category, str) or not category:
            raise DataIntegrityError(f"catalog[{sid}]: category must be a non-empty string")
        # cross-body dangling-reference check (§2.4.1): a referenced category must be known or 'none'.
        if category != "none" and category not in known_categories:
            raise DataIntegrityError(
                f"catalog[{sid}]: category '{category}' is not a known category (dangling reference)")

        catalog[sid] = {
            "entries": entries,
            "gcp_api": doc["gcp_api"],
            "category": category,
        }

    if not catalog:
        raise DataIntegrityError("catalog: no catalog files found")

    # cross-body (§2.4.1): every key_bearing_pairing api/secret name appears in some loaded body.
    known_names = set()
    for e in (b for entries in library.values() for b in entries):
        known_names.add(e["name"])
    for rec in catalog.values():
        for e in rec["entries"]:
            known_names.add(e["name"])
    for (api_kind, api_name), (sec_kind, sec_name) in pairing.items():
        for nm in (api_name, sec_name):
            if nm not in known_names:
                raise DataIntegrityError(
                    f"kinds: key_bearing_pairing references name '{nm}' absent from all DATA bodies "
                    f"(dangling reference)")

    # §22 CATEGORIES bundle = the seeded emergent categories discovery's G2 selects over. Alias
    # categories (§3.2 / WP-4) are EXCLUDED here (resolve's LIBRARY keeps them; discovery must not
    # double-count an alias as a competing same-size subset — mirrors the Phase-1 prototype).
    categories = {
        name: [dict(e) for e in entries]
        for name, entries in library.items()
        if name not in _ALIAS_CATEGORIES
    }
    return catalog, categories


# ===========================================================================
# stoa--fdf (u--9s2 Phase-2 increment 2.2) — APPENDED SIBLING LOADER ONLY.
# Everything ABOVE this banner (load_catalog / load_baseline / load_kinds / load_library + their
# helpers) is BYTE-UNCHANGED from the 2.1 core (stoa--pj3) — the §2-constraint. The ONLY delta to
# dataload.py in 2.2 is the additive load_detection_hints function below (FM-ratified location;
# design-rev2 §2.0.1 / §2.3). load_catalog is NOT edited: its tolerance of the additive
# [detection_hints] catalog block is pinned by test_load_catalog_admits_detection_hints (rev2 WP-D2),
# NOT by a code change here.
# ===========================================================================

# §2.4.1 SSoT — the CLOSED set of detection_hints sub-keys (the four §25 EXAMINE surfaces). An unknown
# sub-key under a [detection_hints] block is fail-closed-rejected (set-subset discipline, mirroring the
# load_baseline / load_kinds set-equality precedent above).
EXPECTED_HINT_SURFACES = {"sdk_imports", "url_patterns", "config_keys", "data_signals"}


# ---------------------------------------------------------------------------
# §25.3 detection_hints — fail-closed load + validation of the ADVISORY hint blocks (stoa--fdf).
# Reads the SAME data/catalog/*.toml that load_catalog reads, but ONLY the optional [detection_hints]
# block of each (hint-agnostic generation, §25.2 invariant 1: load_catalog reads the 4 record fields and
# ignores hints; load_detection_hints reads + validates ONLY the hints). ALL detection_hints validation
# lives HERE (the rev2 WP-D2 fold: load_catalog is byte-unchanged and does NO hints validation).
# ---------------------------------------------------------------------------
def load_detection_hints(data_root: Path | None = None) -> dict:
    """Load + VALIDATE the §25 detection_hints blocks from data/catalog/*.toml.

    Returns { service_id: {sdk_imports, url_patterns, config_keys, data_signals} } — the flat hints dict
    suggest() consumes. A service-id with NO [detection_hints] block is OMITTED from the result (the
    field is optional, §25); a service whose block is present contributes its surfaces (any subset of
    EXPECTED_HINT_SURFACES, including empty).

    §2.4.1 fail-closed invariants (per [detection_hints] block, if present):
      - the block is a table (dict);
      - its keys are a SUBSET of the closed set EXPECTED_HINT_SURFACES — an unknown sub-key raises
        DataIntegrityError (mirrors the load_baseline/load_kinds set-discipline; the one tolerance
        load_catalog has is deliberately NOT replicated here — hints are strictly validated);
      - every present surface is an array of NON-EMPTY strings.
    Any deviation raises DataIntegrityError, no partial load. A service keyed by its TOML service-id.
    """
    root = data_root if data_root is not None else _DATA_ROOT
    cat_dir = root / "catalog"
    if not cat_dir.is_dir():
        raise DataIntegrityError(f"detection_hints: catalog directory missing: {cat_dir}")

    hints: dict = {}
    for path in sorted(cat_dir.glob("*.toml")):
        doc = _read_toml(path)
        sid = doc.get("service-id")
        if not isinstance(sid, str) or not sid:
            raise DataIntegrityError(
                f"detection_hints[{path.stem}]: service-id must be a non-empty string")

        block = doc.get("detection_hints")
        if block is None:
            continue  # §25 optional — a service with no hints block is allowed (omitted from result)
        if not isinstance(block, dict):
            raise DataIntegrityError(
                f"detection_hints[{sid}]: [detection_hints] must be a table")

        unknown = set(block.keys()) - EXPECTED_HINT_SURFACES
        if unknown:
            raise DataIntegrityError(
                f"detection_hints[{sid}]: unknown sub-key(s) {sorted(unknown)} under [detection_hints] "
                f"(allowed: {sorted(EXPECTED_HINT_SURFACES)})")

        record = {}
        for surface in sorted(EXPECTED_HINT_SURFACES):
            tokens = block.get(surface, [])
            if not isinstance(tokens, list) or not all(isinstance(t, str) for t in tokens):
                raise DataIntegrityError(
                    f"detection_hints[{sid}].{surface}: must be an array of strings")
            for t in tokens:
                if not t:
                    raise DataIntegrityError(
                        f"detection_hints[{sid}].{surface}: empty-string token not allowed")
            record[surface] = list(tokens)
        hints[sid] = record

    return hints

# author: Denson Smith
# ticket: stoa--jw5 (u--9s2 Phase-1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR) — exercises the KEY-DISCOVERY addition's testable core
# design-ground-truth: agents/design/stoa--jw5/design-formal.md §17 (catalog schema) / §22 (seed records
#                       + seeded emergent categories) / §3.4 (paired-credential as a catalog invariant)
#
# The §22 SEED catalog (service-id -> typed entries + gcp_api + category-tag) + the §22 seeded emergent
# categories, transcribed verbatim from the design. Provisions NOTHING; pure data.
#
# §17.2.3: baseline (§3.1) is NOT in the catalog — it is universal + prepended by resolve() (BASELINE u ...).
# §17.2.2 / §3.4: a key-bearing gcp_api ships its paired gcp_secret in the SAME record (the §3.4 paired-
#   credential rule encoded as a catalog invariant). google-maps carries BOTH (gcp_api, google-maps) AND
#   (gcp_secret, MAPS_API_KEY) in one record (the §3.4 pairing in the catalog — brief item 1).

from __future__ import annotations


# ---------------------------------------------------------------------------
# §22 SEED catalog records (Phase-1 initial state; the four services the §8
# fixtures exercise). Each record: service-id -> { entries[], gcp_api, category }.
# §17.1 record schema; §17.2.1 well-typedness (every entry is a §3 {kind,name}).
# ---------------------------------------------------------------------------
CATALOG = {
    # client-side Maps-JS surface = API-key-bearing (§3.4). The §3.4 pairing lives in
    # THIS record: BOTH (gcp_api, google-maps) AND its paired (gcp_secret, MAPS_API_KEY).
    "google-maps": {
        "entries": [
            {"kind": "gcp_api",    "name": "google-maps"},
            {"kind": "gcp_secret", "name": "MAPS_API_KEY"},
        ],
        "gcp_api": "google-maps",
        "category": "geospatial",
    },
    "spatial-db": {
        "entries": [
            {"kind": "db_extension", "name": "postgis"},
        ],
        "gcp_api": "none",
        "category": "geospatial",
    },
    "document-parsing": {
        "entries": [
            {"kind": "gcp_api", "name": "document-parsing"},
        ],
        "gcp_api": "document-parsing",
        "category": "document-consuming",
    },
    # a BLS OEWS REST call — NOT a GCP API (gcp_api: none -> natively skips S1 enablement).
    # category: none -> a per-builder special; rides delta.add, not a category (§22).
    "bls-oews": {
        "entries": [
            {"kind": "thirdparty_rest_key", "name": "BLS_OEWS_API_KEY"},
        ],
        "gcp_api": "none",
        "category": "none",
    },
}


# ---------------------------------------------------------------------------
# §22 seeded emergent categories (§21.5 bootstrap — identical to the §3.2
# templates, so the §8 sets hold). Each category -> its set of typed entries
# (the named entry-set resolve() consumes; only the PROVENANCE is "emergent", §21.2).
#
# geospatial         = google-maps u spatial-db catalog entries
# document-consuming = document-parsing catalog entry
# (pgvector is BASELINE — NOT re-listed in document-consuming, per §3.2.)
# ---------------------------------------------------------------------------
CATEGORIES = {
    "geospatial": [
        {"kind": "gcp_api",      "name": "google-maps"},
        {"kind": "gcp_secret",   "name": "MAPS_API_KEY"},
        {"kind": "db_extension", "name": "postgis"},
    ],
    "document-consuming": [
        {"kind": "gcp_api", "name": "document-parsing"},
    ],
}

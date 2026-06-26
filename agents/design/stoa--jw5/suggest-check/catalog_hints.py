# author: Denson Smith
# ticket: stoa--jw5 (u--9s2 Phase-1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR) — exercises the SUGGEST front-door's testable core
# design-ground-truth: agents/design/stoa--jw5/design-formal.md §22 (seed catalog) /
#                       §25 (detection_hints fields) / §25.1 (ADVISORY, distinct from the hard recipe) /
#                       §25.2 (catalog is the candidate-service SPACE) / §25.3 (seed hints)
#
# The §22 SEED catalog records EXTENDED with the §25 additive, optional, ADVISORY `detection_hints`
# field for the four services the §29 worked examples exercise (google-maps, spatial-db,
# document-parsing, bls-oews). Provisions NOTHING; pure data.
#
# THE LOAD-BEARING DISTINCTION (§25.1): detection_hints are ADVISORY inference signals the SUGGEST
# agent matches to RECOGNIZE a service in a project. They are NOT the provisioning recipe. The hard
# recipe is the service's `entries` (typed §3 entries — the actual keys/APIs/extensions), which are
# UNCHANGED + authoritative + untouched by this increment. A wrong/missing hint can only mis-PROPOSE,
# never mis-PROVISION (provisioning rides the CONFIRMED service's `entries` via the unchanged path).
#
# §25.2 invariant: detection_hints is a NEW OPTIONAL field on the existing §17.1 record; generation
# (§19) and the resolver (§2) read `entries` ONLY and never read detection_hints (hint-agnostic).
# Only the SUGGEST agent's matching pass (§24 S-2) reads detection_hints.

from __future__ import annotations


# ---------------------------------------------------------------------------
# §22 SEED catalog records EXTENDED with §25 detection_hints (the four §29 services).
#
# Each record keeps its §17.1 shape verbatim (entries / gcp_api / category) — transcribed to match
# discovery-check/catalog.py byte-for-byte on those fields — and APPENDS one optional `detection_hints`
# field (sdk_imports / url_patterns / config_keys / data_signals, §25). The `entries` (hard recipe)
# are IDENTICAL to discovery-check/catalog.py: SUGGEST changes only HOW a service is recognized, not
# WHAT it provisions.
# ---------------------------------------------------------------------------
CATALOG_HINTS = {
    # client-side Maps-JS surface = API-key-bearing (§3.4). The §3.4 pairing lives in THIS record:
    # BOTH (gcp_api, google-maps) AND its paired (gcp_secret, MAPS_API_KEY) — the HARD recipe, unchanged.
    "google-maps": {
        "entries": [
            {"kind": "gcp_api",    "name": "google-maps"},
            {"kind": "gcp_secret", "name": "MAPS_API_KEY"},
        ],
        "gcp_api": "google-maps",
        "category": "geospatial",
        "detection_hints": {                       # §25 ADVISORY — recognition signals only
            "sdk_imports":  ["@googlemaps/js-api-loader", "google.maps", "@react-google-maps/api"],
            "url_patterns": ["maps.googleapis.com", "maps.gstatic.com"],
            "config_keys":  ["GOOGLE_MAPS_API_KEY", "MAPS_API_KEY", "NEXT_PUBLIC_MAPS_KEY"],
            "data_signals": ["client-side-map-render", "map-tile-fetch"],
        },
    },
    "spatial-db": {
        "entries": [
            {"kind": "db_extension", "name": "postgis"},
        ],
        "gcp_api": "none",
        "category": "geospatial",
        "detection_hints": {
            "sdk_imports":  ["geoalchemy2", "shapely", "postgis"],
            "url_patterns": [],
            "config_keys":  ["POSTGIS_ENABLE"],
            "data_signals": ["spatial-data", "geometry-column", "ST_ geo-query"],
        },
    },
    "document-parsing": {
        "entries": [
            {"kind": "gcp_api", "name": "document-parsing"},
        ],
        "gcp_api": "document-parsing",
        "category": "document-consuming",
        "detection_hints": {
            "sdk_imports":  ["google.cloud.documentai", "google-cloud-documentai"],
            "url_patterns": ["documentai.googleapis.com"],
            "config_keys":  ["DOCAI_PROCESSOR_ID", "DOCUMENT_AI_LOCATION"],
            "data_signals": ["pdf-ingest", "ocr-extract", "document-parse"],
        },
    },
    # a BLS OEWS REST call — NOT a GCP API (gcp_api: none -> natively skips S1 enablement).
    # category: none -> a per-builder special; rides delta.add, not a category (§22).
    # The load-bearing DWP-3 case: declaration-from-memory might MISS this; the agent INFERS it
    # from the BLS-OEWS url_pattern + BLS_OEWS_API_KEY config_key signal (§29.1 labstat_bls).
    "bls-oews": {
        "entries": [
            {"kind": "thirdparty_rest_key", "name": "BLS_OEWS_API_KEY"},
        ],
        "gcp_api": "none",
        "category": "none",
        "detection_hints": {
            "sdk_imports":  [],                    # no SDK — a raw REST call (the DWP-3 shape)
            "url_patterns": ["api.bls.gov", "api.bls.gov/publicAPI/v2/timeseries", "bls.gov/oes"],
            "config_keys":  ["BLS_OEWS_API_KEY", "BLS_API_KEY"],
            "data_signals": ["oews-wage-data", "bls-occupation-stats"],
        },
    },
}


# ---------------------------------------------------------------------------
# The §25 detection_hints field names (the four advisory surfaces). Used by suggest() to iterate
# project signals against the catalog. These are the four EXAMINE-surfaces of §24:
#   sdk_imports  <- surface (i)  SDK/import examination
#   url_patterns <- surface (ii) outbound-call / endpoint examination
#   config_keys  <- surface (i/ii) env-var / config examination
#   data_signals <- surface (iii) data-flow / resource examination
# ---------------------------------------------------------------------------
HINT_FIELDS = ("sdk_imports", "url_patterns", "config_keys", "data_signals")

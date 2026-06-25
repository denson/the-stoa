# author: Denson Smith
# ticket: stoa--jw5 (u--9s2 Phase-1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--jw5/design-formal.md §8 (the four worked-example fixtures)
#
# The 4 manifests from §8 + their EXACT expected resolved sets, transcribed verbatim.
# Each expected set is the §8.x (kind, name) enumeration, sorted (kind, name) ascending
# (the same canonical order resolve() returns). Provisions nothing.


# --- §8.1 prospector — {category: geospatial, delta: {}} ---------------------
PROSPECTOR_MANIFEST = {
    "builder": "prospector",
    "category": "geospatial",
    "delta": {},
}
# Expected resolved set (8 entries) — §8 lines 485-492. BASELINE 5 + geospatial 3 = 8.
PROSPECTOR_EXPECTED = [
    ("db_extension", "pgvector"),
    ("db_extension", "postgis"),
    ("gcp_api",      "gemini-embedding"),
    ("gcp_api",      "gemini-search"),
    ("gcp_api",      "google-maps"),
    ("gcp_secret",   "MAPS_API_KEY"),
    ("gcp_secret",   "POSTGRES_PASSWORD"),
    ("railway_var",  "DATABASE_URL"),
]


# --- §8.2 scienceclaw — {category: document-consuming, delta: {}} ------------
SCIENCECLAW_MANIFEST = {
    "builder": "scienceclaw",
    "category": "document-consuming",
    "delta": {},
}
# Expected resolved set (6 entries) — §8 lines 510-515. BASELINE 5 + doc 1 = 6.
SCIENCECLAW_EXPECTED = [
    ("db_extension", "pgvector"),
    ("gcp_api",      "document-parsing"),
    ("gcp_api",      "gemini-embedding"),
    ("gcp_api",      "gemini-search"),
    ("gcp_secret",   "POSTGRES_PASSWORD"),
    ("railway_var",  "DATABASE_URL"),
]


# --- §8.3 labstat_bls — {category: document/data, delta:{add:[thirdparty_rest_key BLS_OEWS_API_KEY]}}
LABSTAT_BLS_MANIFEST = {
    "builder": "labstat_bls",
    "category": "document/data",
    "delta": {
        "add": [
            {"kind": "thirdparty_rest_key", "name": "BLS_OEWS_API_KEY"},
        ],
    },
}
# Expected resolved set (7 entries) — §8 lines 530-537. BASELINE 5 + doc 1 + delta.add 1 = 7.
LABSTAT_BLS_EXPECTED = [
    ("db_extension",        "pgvector"),
    ("gcp_api",             "document-parsing"),
    ("gcp_api",             "gemini-embedding"),
    ("gcp_api",             "gemini-search"),
    ("gcp_secret",          "POSTGRES_PASSWORD"),
    ("railway_var",         "DATABASE_URL"),
    ("thirdparty_rest_key", "BLS_OEWS_API_KEY"),
]


# --- §8.4 badbuilder_pgvector_omit — NEGATIVE (MUST raise BaselineOmitError) --
BADBUILDER_PGVECTOR_OMIT_MANIFEST = {
    "builder": "badbuilder_pgvector_omit",
    "category": "document-consuming",
    "delta": {
        "omit": [
            {"kind": "db_extension", "name": "pgvector"},  # attempts to drop a BASELINE entry — illegal
        ],
    },
}
# Expected behavior: resolve(...) RAISES BaselineOmitError naming (db_extension, pgvector).
# No expected resolved set (fail-closed).


# Positive fixtures the harness asserts an exact set for.
POSITIVE_FIXTURES = [
    ("prospector  (§8.1)", PROSPECTOR_MANIFEST, PROSPECTOR_EXPECTED),
    ("scienceclaw (§8.2)", SCIENCECLAW_MANIFEST, SCIENCECLAW_EXPECTED),
    ("labstat_bls (§8.3)", LABSTAT_BLS_MANIFEST, LABSTAT_BLS_EXPECTED),
]

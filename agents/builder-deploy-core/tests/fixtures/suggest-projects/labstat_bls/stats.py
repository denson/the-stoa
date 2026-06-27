# author: Denson Smith
# stoa--fdf §29.1 fixture: labstat_bls (doc/data project — the load-bearing DWP-3 case). Layer-S signals:
#   sdk_imports: google.cloud.documentai     (doc-parse SDK import -> document-parsing)
#   url_patterns: api.bls.gov                 (BLS-OEWS base URL    -> bls-oews; the DWP-3 infer, no SDK)
#   config_keys: BLS_OEWS_API_KEY             (BLS config key       -> bls-oews)
# bls-oews is INFERRED from a raw REST url + config key (no SDK import) — the §29.1 DWP-3 upgrade.

import os

from google.cloud import documentai


def fetch_wages():
    api_key = os.environ["BLS_OEWS_API_KEY"]            # config_key signal -> bls-oews
    # a raw BLS REST call (no SDK) — the url_pattern signal -> bls-oews
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    client = documentai.DocumentProcessorServiceClient()
    return api_key, url, client

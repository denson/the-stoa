# author: Denson Smith
# stoa--fdf §29.1 fixture: under-proposal (labstat_bls, but the BLS endpoint is built TOO DYNAMICALLY
# for Layer S to trace). Layer-S signals:
#   sdk_imports: google.cloud.documentai   (only the doc-parse SDK is statically visible -> document-parsing)
# The BLS URL is assembled from runtime parts (host fragments concatenated), so NO static url-literal
# matches the bls-oews hint, and there is NO BLS config key read statically -> Layer S MISSES bls-oews
# (the §28 under-proposal). The §26 human (who knows the project calls BLS) ADDS it in confirm (P2f).

from google.cloud import documentai


def fetch_wages(host_part_a, host_part_b, path):
    client = documentai.DocumentProcessorServiceClient()
    # the BLS endpoint is built from runtime fragments — no static literal Layer S can trace to a hint:
    url = "https://" + host_part_a + "." + host_part_b + path
    return client, url

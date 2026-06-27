# author: Denson Smith
# stoa--fdf §29.1 fixture: over-proposal (scienceclaw + a STRAY maps URL the code never CALLS).
# Layer-S signals:
#   sdk_imports: google.cloud.documentai      (real -> document-parsing)
#   url_patterns: documentai.googleapis.com   (real -> document-parsing)
#                 maps.googleapis.com         (STRAY literal in a dead/mock string -> mis-proposes google-maps)
# The maps URL is a string literal the code never actually fetches (a mock/aspiration) — Layer S (a
# static literal scan) cannot tell it is dead, so it OVER-proposes google-maps. The §26 human EDIT
# removes it (P2e). This is the SWP-2 over-proposal the gate is load-bearing against.

from google.cloud import documentai

# a stray maps URL string the code never CALLS — a mock constant left in the repo:
DEAD_MOCK_MAPS_URL = "https://maps.googleapis.com/maps/api/js"  # never fetched


def parse(pdf_bytes):
    client = documentai.DocumentProcessorServiceClient()
    endpoint = "https://documentai.googleapis.com/v1/processors/y:process"
    return client, endpoint, pdf_bytes

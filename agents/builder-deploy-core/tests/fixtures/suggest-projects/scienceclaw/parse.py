# author: Denson Smith
# stoa--fdf §29.1 fixture: scienceclaw (doc-consuming project). Carries REAL Layer-S signals:
#   sdk_imports: google.cloud.documentai  (doc-parse SDK import -> document-parsing)
#   url_patterns: documentai.googleapis.com (parse endpoint URL -> document-parsing)
# A commented-out maps import below MUST NOT be flagged (AST/comment-aware, §28).

# import google.maps  -> must NOT be flagged (commented out)
from google.cloud import documentai


def parse(pdf_bytes):
    client = documentai.DocumentProcessorServiceClient()
    # outbound parse endpoint — the url_pattern signal (a string literal the AST scans)
    endpoint = "https://documentai.googleapis.com/v1/projects/x/locations/us/processors/y:process"
    return client, endpoint, pdf_bytes

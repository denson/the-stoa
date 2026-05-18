"""
byte_copy — sha256 round-trip verified write primitive.

Private to substrate/skills/save-verdict/ in Arc 39 per directive A2 α.
Cross-skill share with COPY_ARTIFACT + TRANSCRIBE_BW_TO_DISK deferred to
substrate ticket stoa--sp1.
"""

from __future__ import annotations

import hashlib
import pathlib


def write_with_verify(
    dest_path: pathlib.Path,
    body_bytes: bytes,
    overwrite: bool = False,
) -> dict:
    """
    Write body_bytes to dest_path with sha256 round-trip verification.

    Computes sha256 of body_bytes (input_sha256), writes bytes to dest_path,
    re-reads dest_path, computes sha256 of read-back bytes (dest_sha256), and
    asserts input_sha256 == dest_sha256. On mismatch, raises ValueError with
    both hashes in the message.

    Returns: {
        "input_byte_length": int,
        "input_sha256": str,  # hex
        "dest_sha256": str,   # hex
        "verification": "pass" | "fail",
    }

    Raises:
        FileExistsError — if dest_path exists and overwrite is False.
        ValueError — if sha256 round-trip mismatch.
        OSError — bubbled from write/read.

    Parent directory must exist; caller is responsible for mkdir -p semantics.
    """
    if not isinstance(dest_path, pathlib.Path):
        dest_path = pathlib.Path(dest_path)

    if dest_path.exists() and not overwrite:
        raise FileExistsError(f"dest exists: {dest_path}")

    input_sha256 = hashlib.sha256(body_bytes).hexdigest()
    input_byte_length = len(body_bytes)

    dest_path.write_bytes(body_bytes)

    reread_bytes = dest_path.read_bytes()
    dest_sha256 = hashlib.sha256(reread_bytes).hexdigest()

    if input_sha256 != dest_sha256:
        raise ValueError(
            f"sha256 round-trip mismatch: input={input_sha256} dest={dest_sha256}"
        )

    return {
        "input_byte_length": input_byte_length,
        "input_sha256": input_sha256,
        "dest_sha256": dest_sha256,
        "verification": "pass",
    }

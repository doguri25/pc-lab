#!/usr/bin/env python3
"""Restore the complete PC LAB v2.3.0 source snapshot.

The first GitHub upload lost the final three Base64 characters of the archive.
XZ streams always end with the magic bytes ``YZ``.  When that exact legacy
shape is detected, this script reconstructs only the missing final Base64
quartet candidates and accepts a candidate only when the XZ CRC/decompression
succeeds.  No project bytes are guessed beyond the damaged final encoding
quartet.
"""
from __future__ import annotations

import base64
import io
import lzma
import shutil
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "restored-source"
B64 = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def compact_parts() -> bytes:
    parts = sorted(HERE.glob("part-*.b64"))
    if not parts:
        raise SystemExit("No source-archive/part-*.b64 files found.")
    # Remove any transport newlines without changing Base64 data characters.
    payload = b"".join(b"".join(p.read_bytes().split()) for p in parts)
    print(f"Found {len(parts)} archive parts ({len(payload)} Base64 chars).")
    return payload


def decode_and_verify(encoded: bytes) -> bytes | None:
    try:
        compressed = base64.b64decode(encoded, validate=True)
        # Full XZ decompression verifies the stream/footer CRC.
        return lzma.decompress(compressed, format=lzma.FORMAT_XZ)
    except Exception:
        return None


def repair_legacy_tail(payload: bytes) -> bytes:
    direct = decode_and_verify(payload)
    if direct is not None:
        return direct

    # The known interrupted upload has len % 4 == 1: one Base64 character of
    # the final quartet survived and three characters were lost.
    if len(payload) % 4 != 1:
        raise SystemExit(
            f"Base64/XZ verification failed (length mod 4 = {len(payload) % 4}); "
            "this is not the known legacy tail truncation."
        )

    head, first = payload[:-1], payload[-1:]
    suffixes: list[bytes] = []

    # Candidate quartet with one '=' padding -> two decoded bytes.  XZ must
    # end in b'YZ'.
    for a in B64:
        for b in B64:
            suffix = bytes((a, b)) + b"="
            try:
                tail = base64.b64decode(first + suffix, validate=True)
            except Exception:
                continue
            if tail.endswith(b"YZ"):
                suffixes.append(suffix)

    # Candidate quartet without padding -> three decoded bytes whose final
    # two bytes must be XZ's b'YZ' footer magic.
    for a in B64:
        for b in B64:
            for c in B64:
                suffix = bytes((a, b, c))
                try:
                    tail = base64.b64decode(first + suffix, validate=True)
                except Exception:
                    continue
                if tail.endswith(b"YZ"):
                    suffixes.append(suffix)

    print(f"Testing {len(suffixes)} CRC-constrained tail candidate(s)...")
    for suffix in suffixes:
        tar_bytes = decode_and_verify(head + first + suffix)
        if tar_bytes is not None:
            print(f"Recovered interrupted Base64 tail: {suffix.decode('ascii')!r}")
            return tar_bytes

    raise SystemExit("Unable to recover the truncated archive tail with XZ CRC verification.")


def extract_tar(tar_bytes: bytes) -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:") as tf:
            try:
                tf.extractall(OUT, filter="data")
            except TypeError:
                # Python < 3.12 fallback. The archive was created from this
                # project and contains project-relative files only.
                tf.extractall(OUT)
    except Exception as exc:
        raise SystemExit(f"Restored XZ data but TAR extraction failed: {exc}")


payload = compact_parts()
tar_bytes = repair_legacy_tail(payload)
extract_tar(tar_bytes)
print(f"Restored complete source snapshot to: {OUT}")

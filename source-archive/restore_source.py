#!/usr/bin/env python3
"""Restore the complete PC LAB v2.3.0 source snapshot from source-archive/part-*.b64."""
from __future__ import annotations
import base64
import io
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "restored-source"
parts = sorted(HERE.glob("part-*.b64"))
if not parts:
    raise SystemExit("No source-archive/part-*.b64 files found.")

payload = b"".join(p.read_bytes().strip() for p in parts)
try:
    compressed = base64.b64decode(payload, validate=True)
except Exception as exc:
    raise SystemExit(f"Base64 decode failed: {exc}")

OUT.mkdir(parents=True, exist_ok=True)
try:
    with tarfile.open(fileobj=io.BytesIO(compressed), mode="r:xz") as tf:
        tf.extractall(OUT, filter="data")
except TypeError:
    # Python < 3.12 compatibility: archive was created locally and contains project-relative files only.
    with tarfile.open(fileobj=io.BytesIO(compressed), mode="r:xz") as tf:
        tf.extractall(OUT)
except Exception as exc:
    raise SystemExit(f"Archive extraction failed: {exc}")

print(f"Restored {len(parts)} archive parts to: {OUT}")

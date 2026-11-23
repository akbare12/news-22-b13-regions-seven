#!/usr/bin/env python3
"""Reproduce entry.png byte-identically.

Stdlib-only copy program: copies the bundled entry.png next to this file
into the current working directory and verifies its SHA-256 digest.
Running it twice produces byte-identical output.
"""
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "e6e9d7fc47046cd05bc621916a456097c33f52f4c4fe38f4c6453aa20d5d3431"
EXPECTED_BYTES = 202425


def sha256_of(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(os.getcwd(), "entry.png")
    if not os.path.exists(src):
        sys.stderr.write("entry.png not found next to main.py\n")
        return 1
    if os.path.abspath(src) != os.path.abspath(dst):
        # Copy via a temp file and atomic replace so a partial write can
        # never leave a truncated entry.png behind.
        tmp = dst + ".tmp"
        shutil.copyfile(src, tmp)
        os.replace(tmp, dst)
    digest = sha256_of(dst)
    size = os.path.getsize(dst)
    if digest != EXPECTED_SHA256 or size != EXPECTED_BYTES:
        sys.stderr.write(
            f"entry.png mismatch: sha256 {digest} ({size} bytes), "
            f"expected {EXPECTED_SHA256} ({EXPECTED_BYTES} bytes)\n"
        )
        return 1
    print(f"entry.png reproduced: {size} bytes, sha256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

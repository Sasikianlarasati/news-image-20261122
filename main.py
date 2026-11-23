#!/usr/bin/env python3
"""Entry point for the make.fun news-image build.

Copies the rendered front page (entry.png, next to this file) to
/output/entry.png and checks the copy is byte-identical.
"""

import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DEST_DIR = "/output"
DEST = os.path.join(DEST_DIR, "entry.png")


def digest(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    os.makedirs(DEST_DIR, exist_ok=True)
    shutil.copyfile(SRC, DEST)
    if digest(SRC) != digest(DEST):
        raise SystemExit("copy mismatch: /output/entry.png differs from entry.png")
    print(f"copied {SRC} -> {DEST} ({os.path.getsize(DEST)} bytes, identical)")


if __name__ == "__main__":
    main()

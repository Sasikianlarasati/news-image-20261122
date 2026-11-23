#!/usr/bin/env python3
"""Entry for make.fun "Sum up 22 November's world news in one image".

Writes the day's news infographic (entry.png, 1024x1024) to
/output/entry.png. Deterministic: copies the bundled image byte for byte,
no network, no randomness.
"""

import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    src = HERE / "entry.png"
    out = Path("/output/entry.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

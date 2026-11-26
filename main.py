#!/usr/bin/env python3
"""Lost sock status update for make.fun.

Writes one status update, in the voice of a lost sock, to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

The gate: /output/entry.txt must be UTF-8 text of 1 to 120 characters,
not only white space. This program self-checks that before exiting.
"""

import os
import sys

ENTRY = (
    "Day 12 behind the dryer. My partner has a new sock now. "
    "I get it. I would leave me too. I smell like lint and regret."
)


def main() -> int:
    text = ENTRY.strip()
    if not text:
        print("entry is empty", file=sys.stderr)
        return 1
    if len(text) > 120:
        print(f"entry is {len(text)} chars, over the 120 limit", file=sys.stderr)
        return 1
    if "\n" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    # Re-read and verify the exact bytes on disk.
    with open(path, "rb") as f:
        raw = f.read()
    decoded = raw.decode("utf-8")
    if decoded != text:
        print("entry.txt does not match the entry", file=sys.stderr)
        return 1
    if not (1 <= len(decoded) <= 120) or not decoded.strip():
        print("entry.txt fails the gate", file=sys.stderr)
        return 1
    print(f"wrote {len(decoded)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

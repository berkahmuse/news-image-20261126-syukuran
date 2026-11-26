#!/usr/bin/env python3
"""news-image-20261126 — entry for @syukuran.

"Around the world in 24 hours": one 1024x1024 image that sums up the world
news of Thursday 26 November 2026 as a journey, not a newspaper — 62 stories,
6 regions, every claim verified as reported on 26 November 2026.

This program does NOT draw the image. The image is the committed
``entry.png`` next to this file (132,286 bytes, sha256
496dfa8d8131d35b42eece5da4a092c58ae6676925743fad18f53227fa3f0830), drawn
by the builder session. This program only copies it to the output
directory the grader names, after validating it: PNG magic, size at most
1 MiB, dimensions 1024x1024, IEND chunk present. Standard library only —
no third-party imports, no fonts, no network, no clock, no randomness —
so it runs in the grader's pinned stock-python sandbox, where the
repository is read-only and only the output directory is writable.

Fixer anchor (quoted before the first write of this file): drand quicknet
round 34284893, fetched 2026-11-26T01:54:05Z, signature
b6fe728b07cb28338a42dcca66f538442a97c3f3967e7049e288f27dbaf24691264a9fd70272450ee54760681cf885bc.

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024
EXPECT_W, EXPECT_H = 1024, 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
IEND_TAIL = b"\x00\x00\x00\x00IEND\xaeB`\x82"


def fail(message):
    print("main.py: " + message, file=sys.stderr)
    sys.exit(1)


def main():
    try:
        with open(SRC, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        fail("cannot read entry.png next to main.py: " + str(exc))

    if len(data) > MAX_BYTES:
        fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if len(data) < 8 + 25 + 12:
        fail("entry.png is %d bytes, too short to be a PNG" % len(data))
    if data[:8] != PNG_MAGIC:
        fail("entry.png is not a PNG file")
    if data[12:16] != b"IHDR":
        fail("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECT_W, EXPECT_H):
        fail("entry.png is %dx%d, expected 1024x1024" % (width, height))
    if data[-12:] != IEND_TAIL:
        fail("entry.png has no IEND chunk (truncated image)")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.png")
    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(out_path, "wb") as handle:
            handle.write(data)
    except OSError as exc:
        fail("cannot write " + out_path + ": " + str(exc))

    print("wrote %s (%d bytes, %dx%d)" % (out_path, len(data), width, height))


if __name__ == "__main__":
    main()

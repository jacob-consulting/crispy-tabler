#!/usr/bin/env python3
"""Vendor the crispy-bootstrap5 template pack into crispy_tabler.

Usage (from the repo root, with the test extra installed):

    uv run --extra test python scripts/vendor_templates.py

Copies every template of the installed crispy-bootstrap5 into
src/crispy_tabler/templates/crispy_tabler/ and applies exactly two changes
per file: the quoted ``bootstrap5/`` include prefix becomes ``crispy_tabler/``,
and one provenance comment is prepended. Everything else stays byte-identical
so a later re-vendor can be diffed against upstream.

Files under widget/ are pack-owned (no Bootstrap counterpart) and are never
touched. Templates that were hand-edited after vendoring WILL be overwritten:
review the git diff after a re-run.
"""

import re
import sys
from importlib.metadata import version
from pathlib import Path

import crispy_bootstrap5

from crispy_tabler.vendored import CRISPY_BOOTSTRAP5_VERSION

SRC = Path(crispy_bootstrap5.__file__).parent / "templates" / "bootstrap5"
DEST = Path(__file__).resolve().parent.parent / "src/crispy_tabler/templates/crispy_tabler"
INCLUDE_PREFIX = re.compile(r"""(['"])bootstrap5/""")


def main() -> int:
    installed = version("crispy-bootstrap5")
    if installed != CRISPY_BOOTSTRAP5_VERSION:
        print(
            f"installed crispy-bootstrap5 {installed} != vendored.py "
            f"{CRISPY_BOOTSTRAP5_VERSION}; update vendored.py first",
            file=sys.stderr,
        )
        return 1
    count = 0
    for src in sorted(p for p in SRC.rglob("*") if p.is_file()):
        rel = src.relative_to(SRC).as_posix()
        text = src.read_bytes().decode("utf-8")
        text = INCLUDE_PREFIX.sub(r"\1crispy_tabler/", text)
        # The header records the pack-relative path (not "bootstrap5/<rel>"), so it
        # never contains the "bootstrap5/" prefix the self-containment test forbids.
        header = f"{{# vendored from crispy-bootstrap5 {installed}: {rel} #}}\n"
        out = DEST / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes((header + text).encode("utf-8"))
        count += 1
    print(f"vendored {count} templates into {DEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

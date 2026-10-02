"""Remove the BrowserFS loader tag still emitted by the pinned Pygbag template."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlsplit


SCRIPT_ELEMENT = re.compile(
    r"<script\b(?P<attributes>[^>]*)>.*?</script\s*>",
    flags=re.IGNORECASE | re.DOTALL,
)
SRC_ATTRIBUTE = re.compile(
    r"\bsrc\s*=\s*(?:([\"'])(.*?)\1|([^\s>]+))",
    flags=re.IGNORECASE,
)


def _script_source(attributes: str) -> str | None:
    match = SRC_ATTRIBUTE.search(attributes)
    if match is None:
        return None
    return match.group(2) if match.group(1) else match.group(3)


def _is_browserfs_source(source: str | None) -> bool:
    if source is None:
        return False
    filename = urlsplit(source).path.rstrip("/").rsplit("/", maxsplit=1)[-1]
    return filename.casefold() == "browserfs.min.js"


def remove_removed_browserfs_script(html: str) -> str:
    """Remove exactly one stale BrowserFS script element and preserve other HTML."""
    scripts = list(SCRIPT_ELEMENT.finditer(html))
    browserfs_scripts = [
        match
        for match in scripts
        if _is_browserfs_source(_script_source(match.group("attributes")))
    ]
    if len(browserfs_scripts) != 1:
        raise ValueError(
            "Expected exactly one generated browserfs.min.js script element; "
            f"found {len(browserfs_scripts)}. Check the pinned Pygbag template."
        )

    pythons_scripts = [
        match
        for match in scripts
        if (_script_source(match.group("attributes")) or "").casefold().endswith("pythons.js")
    ]
    if len(pythons_scripts) != 1:
        raise ValueError(
            "Expected exactly one Pygbag pythons.js loader; "
            f"found {len(pythons_scripts)}."
        )

    target = browserfs_scripts[0]
    return html[: target.start()] + html[target.end() :]


def patch_index_file(index_path: Path) -> None:
    html = index_path.read_text(encoding="utf-8")
    patched_html = remove_removed_browserfs_script(html)
    index_path.write_text(patched_html, encoding="utf-8", newline="")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/remove_removed_browserfs.py build/web/index.html")
    index_path = Path(sys.argv[1])
    patch_index_file(index_path)
    print(f"Removed the obsolete BrowserFS loader from {index_path}.")


if __name__ == "__main__":
    main()

"""CLI entry point for the CBZ comic reader."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cbz.comic import ComicInfo
from cbz.exceptions import CBZError


def main() -> None:
    """Launch the comic reader with the specified file."""
    parser = argparse.ArgumentParser(
        description="CBZ/CBR/PDF comic reader"
    )
    parser.add_argument(
        "comic_path",
        type=Path,
        metavar="<file>",
        help="Path to the CBZ, CBR or PDF comic book file."
    )
    args = parser.parse_args()

    path: Path = args.comic_path
    if not path.is_file():
        print(f"Error: file '{path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            comic = ComicInfo.from_pdf(path)
        elif suffix == ".cbr":
            comic = ComicInfo.from_cbr(path)
        else:
            comic = ComicInfo.from_cbz(path)

        comic.show()
    except CBZError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

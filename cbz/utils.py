"""Utility functions for the CBZ library."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image
from PIL.IcoImagePlugin import IcoFile


def readable_size(size: int, decimal: int = 2) -> str:
    """Convert a byte size to a human-readable string (KB, MB, etc.)."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024:
            return f"{size:.{decimal}f} {unit}"
        size /= 1024
    return f"{size:.{decimal}f} PB"


def ico_to_png(path: Path) -> BytesIO:
    """Convert the largest icon in an ICO file to PNG format."""
    with Image.open(BytesIO(path.read_bytes())) as image:
        if image.format != "ICO":
            raise ValueError(f"Expected ICO format, got {image.format}")

        icon: IcoFile = image.ico
        max_size = max(icon.sizes(), key=lambda s: s[0] + s[1])
        largest = icon.getimage(size=max_size)

    buf = BytesIO()
    largest.save(buf, format="PNG")
    largest.close()
    buf.seek(0)
    return buf

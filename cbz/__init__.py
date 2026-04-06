"""
CBZ - Python library for digital comic book management.

Supports creating, manipulating and viewing CBZ (Comic Book ZIP),
CBR (Comic Book RAR) and PDF files.
"""

from cbz.comic import ComicInfo
from cbz.page import PageInfo
from cbz.constants import (
    AgeRating,
    Format,
    LanguageISO,
    Manga,
    PageType,
    Rating,
    YesNo
)
from cbz.exceptions import (
    CBZError,
    EmptyArchiveError,
    InvalidImageError,
    InvalidMetadataError,
    UnsupportedFormatError
)

__version__ = "4.0.0"
__all__ = [
    "ComicInfo",
    "PageInfo",
    "AgeRating",
    "Format",
    "LanguageISO",
    "Manga",
    "PageType",
    "Rating",
    "YesNo",
    "CBZError",
    "EmptyArchiveError",
    "InvalidImageError",
    "InvalidMetadataError",
    "UnsupportedFormatError"
]

# Load optional Pillow plugins (AVIF, JPEG XL)
for _plugin in ("pillow_avif", "pillow_jxl"):
    try:
        __import__(_plugin)
    except ImportError:
        pass

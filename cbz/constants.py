"""
Constants and types for the CBZ/ComicInfo format.

Defines enumerations, supported types and field mappings
conforming to the ComicInfo.xml v2.1 schema.
"""

from __future__ import annotations

from enum import Enum
from typing import Union

from langcodes import Language


class StrEnum(str, Enum):
    """Backport of StrEnum for Python < 3.11."""

    def __str__(self) -> str:
        return self.value


# Name of the XML metadata file inside the CBZ archive
XML_NAME = "ComicInfo.xml"

# Supported image formats in CBZ archives
IMAGE_FORMATS: frozenset = frozenset({
    ".jpeg", ".jpg", ".png", ".gif", ".bmp",
    ".tiff", ".tif", ".webp", ".jxl", ".avif"
})


class YesNo(StrEnum):
    """Ternary boolean: Unknown / No / Yes."""
    UNKNOWN = "Unknown"
    NO = "No"
    YES = "Yes"


class Manga(StrEnum):
    """Comic reading direction."""
    UNKNOWN = "Unknown"
    NO = "No"
    YES = "Yes"
    YES_AND_RIGHT_TO_LEFT = "YesAndRightToLeft"


class PageType(StrEnum):
    """Page type within the archive."""
    FRONT_COVER = "FrontCover"
    INNER_COVER = "InnerCover"
    ROUNDUP = "Roundup"
    STORY = "Story"
    ADVERTISEMENT = "Advertisement"
    EDITORIAL = "Editorial"
    LETTERS = "Letters"
    PREVIEW = "Preview"
    BACK_COVER = "BackCover"
    OTHER = "Other"
    DELETED = "Deleted"


class AgeRating(StrEnum):
    """Content age rating classification."""
    UNKNOWN = "Unknown"
    ADULTS_ONLY_18_PLUS = "Adults Only 18+"
    EARLY_CHILDHOOD = "Early Childhood"
    EVERYONE = "Everyone"
    EVERYONE_10_PLUS = "Everyone 10+"
    G = "G"
    KIDS_TO_ADULTS = "Kids to Adults"
    M = "M"
    MA15_PLUS = "MA15+"
    MATURE_17_PLUS = "Mature 17+"
    PG = "PG"
    R18_PLUS = "R18+"
    RATING_PENDING = "Rating Pending"
    TEEN = "Teen"
    X18_PLUS = "X18+"


class Format(StrEnum):
    """Comic publication format."""
    UNKNOWN = "Unknown"
    ANNOTATION = "Annotation"
    ANNUAL = "Annual"
    ANTHOLOGY = "Anthology"
    BLACK_AND_WHITE = "Black & White"
    BOX_SET = "Box-Set"
    CROSSOVER = "Crossover"
    DIRECTORS_CUT = "Director's Cut"
    EPILOGUE = "Epilogue"
    EVENT = "Event"
    FCBD = "FCBD"
    FLYER = "Flyer"
    GIANT_SIZE = "Giant-Size"
    GRAPHIC_NOVEL = "Graphic Novel"
    HARDCOVER = "Hard-Cover"
    KING_SIZE = "King-Size"
    LIMITED_SERIES = "Limited Series"
    MAGAZINE = "Magazine"
    NSFW = "NSFW"
    ONE_SHOT = "One-Shot"
    POINT_ONE = "Point 1"
    PREVIEW = "Preview"
    PROLOGUE = "Prologue"
    REFERENCE = "Reference"
    REVIEW = "Review"
    REVIEWED = "Reviewed"
    SCANLATION = "Scanlation"
    SCRIPT = "Script"
    SERIES = "Series"
    SKETCH = "Sketch"
    SPECIAL = "Special"
    TRADE_PAPERBACK = "Trade Paper Back"
    WEB_COMIC = "Web Comic"
    YEAR_ONE = "Year One"


class Rating(float):
    """Community rating between 0.0 and 5.0 (None if unset)."""

    def __new__(cls, value: Union[int, float] = 0.0) -> Rating:
        val = float(value)
        if not (0.0 <= val <= 5.0):
            raise ValueError(f"Rating must be between 0.0 and 5.0, got {value}")
        return super().__new__(cls, val)


class LanguageISO(str):
    """Valid ISO language code, validated via the langcodes library."""

    def __new__(cls, value: str = "") -> LanguageISO:
        val = str(value)
        if val:
            try:
                if not Language.get(val).is_valid():
                    raise ValueError(f"Invalid ISO language code: {value!r}")
            except ValueError:
                raise
            except Exception as e:
                raise ValueError(f"Invalid ISO language code: {value!r}") from e
        return super().__new__(cls, val)

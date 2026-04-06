"""
Data models for ComicInfo metadata.

Uses dataclasses with field metadata for automatic mapping
to/from the ComicInfo XML format.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Any, Optional

from cbz.constants import (
    AgeRating,
    Format,
    LanguageISO,
    Manga,
    PageType,
    Rating,
    YesNo
)


def xml_field(xml_name: str, is_attribute: bool = False, **kwargs: Any) -> Any:
    """Create a dataclass field with XML mapping metadata.

    Args:
        xml_name: Corresponding XML element or attribute name.
        is_attribute: True if this is an XML attribute (@ prefix), False for an element.
        **kwargs: Additional arguments passed to dataclasses.field().
    """
    metadata = {"xml_name": xml_name, "is_attribute": is_attribute}
    return field(metadata=metadata, **kwargs)


def _get_xml_mapping(cls: type) -> dict:
    """Return the mapping {python_name: (xml_name, type, is_attribute)} for a dataclass."""
    mapping = {}
    for f in fields(cls):
        if "xml_name" in f.metadata:
            mapping[f.name] = (f.metadata["xml_name"], f.type, f.metadata.get("is_attribute", False))
    return mapping


@dataclass
class PageModel:
    """Data model for a comic page.

    Each field corresponds to an XML attribute in the <Page/> element.
    Default values represent the absence of data.
    """

    type: PageType = xml_field("@Type", is_attribute=True, default=PageType.STORY)
    double: bool = xml_field("@DoublePage", is_attribute=True, default=False)
    image_size: int = xml_field("@ImageSize", is_attribute=True, default=0)
    key: str = xml_field("@Key", is_attribute=True, default="")
    bookmark: str = xml_field("@Bookmark", is_attribute=True, default="")
    image_width: int = xml_field("@ImageWidth", is_attribute=True, default=0)
    image_height: int = xml_field("@ImageHeight", is_attribute=True, default=0)

    # Internal fields (not mapped to XML)
    suffix: str = field(default="", repr=False)
    name: str = field(default="", repr=False)


@dataclass
class ComicModel:
    """Data model for comic metadata.

    Each field corresponds to an XML element in <ComicInfo>.
    None values indicate missing data (not serialized to XML).
    """

    title: str = xml_field("Title", default="")
    series: str = xml_field("Series", default="")
    number: Optional[int] = xml_field("Number", default=None)
    count: Optional[int] = xml_field("Count", default=None)
    volume: Optional[int] = xml_field("Volume", default=None)
    alternate_series: str = xml_field("AlternateSeries", default="")
    alternate_number: Optional[int] = xml_field("AlternateNumber", default=None)
    alternate_count: Optional[int] = xml_field("AlternateCount", default=None)
    summary: str = xml_field("Summary", default="")
    notes: str = xml_field("Notes", default="")
    year: Optional[int] = xml_field("Year", default=None)
    month: Optional[int] = xml_field("Month", default=None)
    day: Optional[int] = xml_field("Day", default=None)
    writer: str = xml_field("Writer", default="")
    penciller: str = xml_field("Penciller", default="")
    inker: str = xml_field("Inker", default="")
    colorist: str = xml_field("Colorist", default="")
    letterer: str = xml_field("Letterer", default="")
    cover_artist: str = xml_field("CoverArtist", default="")
    editor: str = xml_field("Editor", default="")
    translator: str = xml_field("Translator", default="")
    publisher: str = xml_field("Publisher", default="")
    imprint: str = xml_field("Imprint", default="")
    genre: str = xml_field("Genre", default="")
    tags: str = xml_field("Tags", default="")
    web: str = xml_field("Web", default="")
    format: Format = xml_field("Format", default=Format.UNKNOWN)
    ean: str = xml_field("EAN", default="")
    black_white: YesNo = xml_field("BlackAndWhite", default=YesNo.UNKNOWN)
    manga: Manga = xml_field("Manga", default=Manga.UNKNOWN)
    characters: str = xml_field("Characters", default="")
    teams: str = xml_field("Teams", default="")
    locations: str = xml_field("Locations", default="")
    scan_information: str = xml_field("ScanInformation", default="")
    story_arc: str = xml_field("StoryArc", default="")
    story_arc_number: Optional[int] = xml_field("StoryArcNumber", default=None)
    series_group: str = xml_field("SeriesGroup", default="")
    age_rating: AgeRating = xml_field("AgeRating", default=AgeRating.UNKNOWN)
    main_character_or_team: str = xml_field("MainCharacterOrTeam", default="")
    review: str = xml_field("Review", default="")
    language_iso: LanguageISO = xml_field("LanguageISO", default=LanguageISO(""))
    community_rating: Optional[Rating] = xml_field("CommunityRating", default=None)
    added: str = xml_field("Added", default="")
    released: str = xml_field("Released", default="")
    file_size: Optional[int] = xml_field("FileSize", default=None)
    file_modified_time: str = xml_field("FileModifiedTime", default="")
    file_creation_time: str = xml_field("FileCreationTime", default="")
    book_price: str = xml_field("BookPrice", default="")
    custom_values_store: str = xml_field("CustomValuesStore", default="")

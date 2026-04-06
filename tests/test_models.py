"""Tests for data models."""

from dataclasses import fields

import pytest

from cbz.constants import (
    AgeRating,
    Format,
    LanguageISO,
    Manga,
    PageType,
    Rating,
    YesNo,
)
from cbz.models import ComicModel, PageModel, _get_xml_mapping


class TestComicModel:
    """Tests for the ComicModel dataclass."""

    def test_default_values(self) -> None:
        """Correct default values."""
        model = ComicModel()

        assert model.title == ""
        assert model.series == ""
        assert model.number is None
        assert model.count is None
        assert model.volume is None
        assert model.year is None
        assert model.format == Format.UNKNOWN
        assert model.black_white == YesNo.UNKNOWN
        assert model.manga == Manga.UNKNOWN
        assert model.age_rating == AgeRating.UNKNOWN
        assert model.community_rating is None

    def test_with_values(self) -> None:
        """Creation with specific values."""
        model = ComicModel(
            title="Test Comic",
            series="Test Series",
            number=1,
            volume=1,
            year=2024,
            month=6,
            day=15,
            writer="Test Writer",
            publisher="Test Publisher",
            language_iso=LanguageISO("en"),
            format=Format.SERIES,
            black_white=YesNo.NO,
            manga=Manga.YES_AND_RIGHT_TO_LEFT,
            age_rating=AgeRating.EVERYONE,
        )

        assert model.title == "Test Comic"
        assert model.series == "Test Series"
        assert model.number == 1
        assert model.year == 2024
        assert model.format == Format.SERIES
        assert model.manga == Manga.YES_AND_RIGHT_TO_LEFT

    def test_enum_assignment(self) -> None:
        """Enum assignment."""
        model = ComicModel()

        model.format = Format.PREVIEW
        assert model.format == Format.PREVIEW

        model.black_white = YesNo.YES
        assert model.black_white == YesNo.YES

        model.manga = Manga.YES_AND_RIGHT_TO_LEFT
        assert model.manga == Manga.YES_AND_RIGHT_TO_LEFT

        model.age_rating = AgeRating.TEEN
        assert model.age_rating == AgeRating.TEEN

    def test_metadata_fields(self) -> None:
        """Verify metadata fields."""
        model = ComicModel(
            summary="Test summary",
            notes="Test notes",
            genre="Adventure",
            web="http://example.com",
            ean="1234567890123",
            community_rating=Rating(5),
            main_character_or_team="Hero",
            characters="Hero, Villain",
            teams="Justice League",
            locations="Metropolis",
            scan_information="Scanned by Test",
            story_arc="Origin Story",
            series_group="DC Comics",
            alternate_series="Alternate Universe",
            alternate_number=2,
            alternate_count=10,
        )

        assert model.summary == "Test summary"
        assert model.genre == "Adventure"
        assert model.community_rating == 5
        assert model.characters == "Hero, Villain"
        assert model.alternate_number == 2

    def test_xml_mapping(self) -> None:
        """Verify XML mapping."""
        mapping = _get_xml_mapping(ComicModel)
        assert "title" in mapping
        assert mapping["title"][0] == "Title"

    def test_all_fields_have_xml_mapping(self) -> None:
        """All annotated fields have an XML mapping."""
        mapping = _get_xml_mapping(ComicModel)
        for f in fields(ComicModel):
            if "xml_name" in f.metadata:
                assert f.name in mapping


class TestPageModel:
    """Tests for the PageModel dataclass."""

    def test_default_values(self) -> None:
        """Correct default values."""
        model = PageModel()

        assert model.type == PageType.STORY
        assert model.double is False
        assert model.image_size == 0
        assert model.key == ""
        assert model.bookmark == ""
        assert model.image_width == 0
        assert model.image_height == 0

    def test_with_values(self) -> None:
        """Creation with specific values."""
        model = PageModel(
            type=PageType.FRONT_COVER,
            double=True,
            image_size=1024000,
            key="cover",
            bookmark="Chapter 1",
            image_width=800,
            image_height=1200,
        )

        assert model.type == PageType.FRONT_COVER
        assert model.double is True
        assert model.image_size == 1024000
        assert model.key == "cover"
        assert model.bookmark == "Chapter 1"
        assert model.image_width == 800
        assert model.image_height == 1200

    def test_all_page_types(self) -> None:
        """All page types are valid."""
        for page_type in PageType:
            model = PageModel(type=page_type)
            assert model.type == page_type

    def test_boolean_properties(self) -> None:
        """Boolean double property."""
        model = PageModel()
        model.double = True
        assert model.double is True
        model.double = False
        assert model.double is False


class TestRating:
    """Tests for the Rating type."""

    def test_valid_rating(self) -> None:
        """Valid ratings (0-5)."""
        assert Rating(0) == 0.0
        assert Rating(2.5) == 2.5
        assert Rating(5) == 5.0

    def test_invalid_rating(self) -> None:
        """Invalid ratings raise ValueError."""
        with pytest.raises(ValueError):
            Rating(-1)
        with pytest.raises(ValueError):
            Rating(6)


class TestLanguageISO:
    """Tests for the LanguageISO type."""

    def test_valid_language(self) -> None:
        """Valid language codes."""
        assert LanguageISO("en") == "en"
        assert LanguageISO("fr") == "fr"
        assert LanguageISO("ja") == "ja"

    def test_empty_language(self) -> None:
        """Empty language code is allowed."""
        assert LanguageISO("") == ""

    def test_invalid_language(self) -> None:
        """Invalid language code raises ValueError."""
        with pytest.raises(ValueError):
            LanguageISO("zzzzzzz")

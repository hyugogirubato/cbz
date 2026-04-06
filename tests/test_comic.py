"""Tests for the ComicInfo class."""

import tempfile
from pathlib import Path

from cbz.comic import ComicInfo
from cbz.constants import AgeRating, Format, Manga, PageType, YesNo
from cbz.page import PageInfo


class TestComicInfo:
    """Tests for comic creation, loading and serialization."""

    def test_from_pages_creation(self, images_dir: Path) -> None:
        """Create a ComicInfo from pages."""
        image_paths = sorted(list(images_dir.iterdir()))[:3]
        pages = [
            PageInfo.load(
                path=path,
                type=PageType.FRONT_COVER if i == 0 else PageType.STORY,
            )
            for i, path in enumerate(image_paths)
        ]

        comic = ComicInfo.from_pages(
            pages=pages,
            title="Test Comic",
            series="Test Series",
            number=1,
            volume=1,
            year=2024,
        )

        assert comic.title == "Test Comic"
        assert comic.series == "Test Series"
        assert comic.number == 1
        assert comic.volume == 1
        assert comic.year == 2024
        assert len(comic) == 3
        assert comic[0].type == PageType.FRONT_COVER
        assert comic[1].type == PageType.STORY

    def test_from_cbz_file(self, sample_cbz_file: Path) -> None:
        """Load from a CBZ file."""
        comic = ComicInfo.from_cbz(sample_cbz_file)

        assert comic is not None
        assert len(comic) > 0
        assert all(isinstance(page, PageInfo) for page in comic)

    def test_pack_cbz(self, images_dir: Path) -> None:
        """Pack into CBZ format."""
        image_paths = sorted(list(images_dir.iterdir()))[:2]
        pages = [PageInfo.load(path=path) for path in image_paths]

        comic = ComicInfo.from_pages(
            pages=pages,
            title="Pack Test",
            series="Test Series",
        )

        cbz_content = comic.pack()
        assert isinstance(cbz_content, bytes)
        assert len(cbz_content) > 0

    def test_pack_with_rename(self, images_dir: Path) -> None:
        """Pack with sequential page renaming."""
        image_paths = sorted(list(images_dir.iterdir()))[:2]
        pages = [PageInfo.load(path=path) for path in image_paths]

        comic = ComicInfo.from_pages(pages=pages, title="Rename Test")
        cbz_content = comic.pack(rename=True)

        assert isinstance(cbz_content, bytes)
        assert len(cbz_content) > 0

    def test_comic_metadata_properties(self, images_dir: Path) -> None:
        """Verify all metadata fields."""
        image_paths = sorted(list(images_dir.iterdir()))[:1]
        pages = [PageInfo.load(path=path) for path in image_paths]

        comic = ComicInfo.from_pages(
            pages=pages,
            title="Metadata Test",
            series="Test Series",
            number=5,
            count=10,
            volume=2,
            summary="Test summary",
            year=2023,
            month=6,
            day=15,
            writer="Test Writer",
            penciller="Test Penciller",
            inker="Test Inker",
            colorist="Test Colorist",
            letterer="Test Letterer",
            cover_artist="Test Cover Artist",
            editor="Test Editor",
            publisher="Test Publisher",
            imprint="Test Imprint",
            genre="Test Genre",
            language_iso="en",
            format=Format.SERIES,
            black_white=YesNo.NO,
            manga=Manga.YES_AND_RIGHT_TO_LEFT,
            age_rating=AgeRating.TEEN,
            community_rating=4,
        )

        assert comic.title == "Metadata Test"
        assert comic.series == "Test Series"
        assert comic.number == 5
        assert comic.count == 10
        assert comic.volume == 2
        assert comic.summary == "Test summary"
        assert comic.year == 2023
        assert comic.month == 6
        assert comic.day == 15
        assert comic.writer == "Test Writer"
        assert comic.penciller == "Test Penciller"
        assert comic.inker == "Test Inker"
        assert comic.colorist == "Test Colorist"
        assert comic.letterer == "Test Letterer"
        assert comic.cover_artist == "Test Cover Artist"
        assert comic.editor == "Test Editor"
        assert comic.publisher == "Test Publisher"
        assert comic.imprint == "Test Imprint"
        assert comic.genre == "Test Genre"
        assert comic.language_iso == "en"
        assert comic.format == Format.SERIES
        assert comic.black_white == YesNo.NO
        assert comic.manga == Manga.YES_AND_RIGHT_TO_LEFT
        assert comic.age_rating == AgeRating.TEEN
        assert comic.community_rating == 4

    def test_page_count_property(self, images_dir: Path) -> None:
        """Verify page count via len()."""
        image_paths = sorted(list(images_dir.iterdir()))[:4]
        pages = [PageInfo.load(path=path) for path in image_paths]

        comic = ComicInfo.from_pages(pages=pages, title="Count Test")
        assert len(comic) == 4

    def test_empty_pages_list(self) -> None:
        """Create a comic with no pages."""
        comic = ComicInfo.from_pages(pages=[], title="Empty Test")
        assert comic.title == "Empty Test"
        assert len(comic) == 0

    def test_single_page_comic_load(self, images_dir: Path) -> None:
        """Round-trip load of a single-page comic."""
        image_paths = sorted(list(images_dir.iterdir()))[:1]
        pages = [PageInfo.load(path=path) for path in image_paths]

        comic = ComicInfo.from_pages(pages=pages, title="Single Page Test")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir) / "single_page.cbz"
            comic.save(temp_path)
            assert temp_path.exists()

            loaded = ComicInfo.from_cbz(temp_path)
            assert loaded.title == "Single Page Test"
            assert len(loaded) == 1

    def test_sequence_protocol(self, images_dir: Path) -> None:
        """Verify sequence protocol (iteration, indexing)."""
        image_paths = sorted(list(images_dir.iterdir()))[:3]
        pages = [PageInfo.load(path=path) for path in image_paths]

        comic = ComicInfo.from_pages(pages=pages, title="Sequence Test")

        # Iteration
        count = 0
        for page in comic:
            assert isinstance(page, PageInfo)
            count += 1
        assert count == 3

        # Indexing
        first = comic[0]
        assert isinstance(first, PageInfo)
        last = comic[-1]
        assert isinstance(last, PageInfo)

        # Slicing
        subset = comic[0:2]
        assert len(subset) == 2

        # Containment
        assert first in comic

    def test_get_info(self, images_dir: Path) -> None:
        """Verify metadata serialization."""
        image_paths = sorted(list(images_dir.iterdir()))[:2]
        pages = [PageInfo.load(path=path) for path in image_paths]

        comic = ComicInfo.from_pages(
            pages=pages,
            title="Info Test",
            series="Test Series",
            year=2024,
        )

        info = comic.get_info()
        assert info["Title"] == "Info Test"
        assert info["Series"] == "Test Series"
        assert info["Year"] == 2024
        assert info["PageCount"] == 2
        assert "Pages" in info
        assert len(info["Pages"]["Page"]) == 2

    def test_none_defaults(self) -> None:
        """Verify optional fields default to None."""
        comic = ComicInfo.from_pages(pages=[])
        assert comic.number is None
        assert comic.count is None
        assert comic.volume is None
        assert comic.year is None
        assert comic.community_rating is None

"""Tests for the PageInfo class."""

from pathlib import Path

import pytest

from cbz.constants import PageType
from cbz.exceptions import InvalidImageError
from cbz.page import PageInfo


class TestPageInfo:
    """Tests for page loading, properties and manipulation."""

    def test_load_from_file(self, sample_image_path: Path) -> None:
        """Load from an image file."""
        page = PageInfo.load(path=sample_image_path)

        assert page is not None
        assert isinstance(page.content, bytes)
        assert len(page.content) > 0
        assert page.name == sample_image_path.name
        assert page.image_width > 0
        assert page.image_height > 0
        assert page.image_size > 0
        assert page.suffix != ""

    def test_load_with_page_type(self, sample_image_path: Path) -> None:
        """Load with a specific page type."""
        page = PageInfo.load(path=sample_image_path, type=PageType.FRONT_COVER)
        assert page.type == PageType.FRONT_COVER

    def test_load_with_custom_name(self, sample_image_path: Path) -> None:
        """Load with a custom name."""
        page = PageInfo.load(path=sample_image_path, name="custom_page.jpg")
        assert page.name == "custom_page.jpg"

    def test_page_content_property(self, sample_image_path: Path) -> None:
        """Content property and automatic metadata extraction."""
        page = PageInfo.load(path=sample_image_path)
        original = page.content

        assert page.content == original
        assert isinstance(page.content, bytes)
        assert page.image_width > 0
        assert page.image_height > 0
        assert page.image_size > 0

    def test_image_metadata_extraction(self, sample_image_path: Path) -> None:
        """Correct extraction of image metadata."""
        page = PageInfo.load(path=sample_image_path)

        assert page.image_width > 0
        assert page.image_height > 0
        assert page.image_size > 0
        assert page.suffix != ""
        assert isinstance(page.image_width, int)
        assert isinstance(page.image_height, int)
        assert isinstance(page.image_size, int)

    def test_multiple_image_formats(self, images_dir: Path) -> None:
        """Load different image files."""
        image_files = list(images_dir.glob("*.jpg"))

        if not image_files:
            pytest.skip("No image files found")

        for image_path in image_files[:3]:
            page = PageInfo.load(path=image_path)

            assert page is not None
            assert isinstance(page.content, bytes)
            assert len(page.content) > 0
            assert page.image_width > 0
            assert page.image_height > 0
            assert page.image_size > 0

    def test_page_type_assignment(self, sample_image_path: Path) -> None:
        """Assignment of all page types."""
        image_bytes = sample_image_path.read_bytes()
        for page_type in PageType:
            page = PageInfo.loads(data=image_bytes, type=page_type)
            assert page.type == page_type

    def test_page_creation_from_bytes(self, sample_image_path: Path) -> None:
        """Direct creation from bytes."""
        image_bytes = sample_image_path.read_bytes()

        page = PageInfo.loads(data=image_bytes, name="test_page.jpg")

        assert page.content == image_bytes
        assert page.name == "test_page.jpg"
        assert page.image_width > 0
        assert page.image_height > 0
        assert page.image_size > 0

    def test_page_bookmark_property(self, sample_image_path: Path) -> None:
        """Bookmark property."""
        page = PageInfo.load(path=sample_image_path, bookmark="Chapter 1")
        assert page.bookmark == "Chapter 1"

        page_no_bookmark = PageInfo.load(path=sample_image_path)
        assert page_no_bookmark.bookmark == ""

    def test_page_double_page_property(self, sample_image_path: Path) -> None:
        """Double page property."""
        page = PageInfo.load(path=sample_image_path, double=True)
        assert page.double is True

        page_no_double = PageInfo.load(path=sample_image_path)
        assert page_no_double.double is False

    def test_invalid_data_raises_error(self) -> None:
        """Invalid data raises InvalidImageError."""
        with pytest.raises(InvalidImageError):
            PageInfo.loads(data=b"not an image")

    def test_empty_data_raises_error(self) -> None:
        """Empty data raises InvalidImageError."""
        with pytest.raises(InvalidImageError):
            PageInfo.loads(data=b"   ")

    def test_save_and_reload(self, sample_image_path: Path, tmp_path: Path) -> None:
        """Save and reload a page."""
        page = PageInfo.load(path=sample_image_path)
        save_path = tmp_path / "saved_page.jpg"
        page.save(save_path)

        reloaded = PageInfo.load(path=save_path)
        assert reloaded.image_width == page.image_width
        assert reloaded.image_height == page.image_height
        assert reloaded.image_size == page.image_size

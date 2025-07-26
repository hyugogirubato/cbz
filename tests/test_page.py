from pathlib import Path

import pytest

from cbz.page import PageInfo
from cbz.constants import PageType


class TestPageInfo:
    """Test cases for PageInfo class."""

    def test_load_from_file(self, sample_image_path: Path) -> None:
        """Test loading PageInfo from image file."""
        page = PageInfo.load(path=sample_image_path)

        assert page is not None
        assert isinstance(page.content, bytes)
        assert len(page.content) > 0
        assert page.name == sample_image_path.name
        assert page.image_width > 0
        assert page.image_height > 0
        assert page.image_size > 0
        assert page.suffix is not None

    def test_load_with_page_type(self, sample_image_path: Path) -> None:
        """Test loading PageInfo with specific page type."""
        page = PageInfo.load(path=sample_image_path, type=PageType.FRONT_COVER)

        assert page.type == PageType.FRONT_COVER

    def test_load_with_custom_name(self, sample_image_path: Path) -> None:
        """Test loading PageInfo with custom name."""
        custom_name = 'custom_page.jpg'
        page = PageInfo.load(path=sample_image_path, name=custom_name)

        assert page.name == custom_name

    def test_page_content_property(self, sample_image_path: Path) -> None:
        """Test page content property getter and setter."""
        page = PageInfo.load(path=sample_image_path)
        original_content = page.content

        # Test getter
        assert page.content == original_content
        assert isinstance(page.content, bytes)

        # Test that content is properly set and metadata extracted
        assert page.image_width > 0
        assert page.image_height > 0
        assert page.image_size > 0

    def test_image_metadata_extraction(self, sample_image_path: Path) -> None:
        """Test that image metadata is correctly extracted."""
        page = PageInfo.load(path=sample_image_path)

        # Check that all image metadata properties are set
        assert hasattr(page, 'image_width') and page.image_width > 0
        assert hasattr(page, 'image_height') and page.image_height > 0
        assert hasattr(page, 'image_size') and page.image_size > 0
        assert hasattr(page, 'suffix') and page.suffix is not None

        # Verify dimensions make sense for an image
        assert isinstance(page.image_width, int)
        assert isinstance(page.image_height, int)
        assert isinstance(page.image_size, int)

    def test_multiple_image_formats(self, images_dir: Path) -> None:
        """Test loading different image formats."""
        image_files = list(images_dir.glob('*.jpg'))

        if not image_files:
            pytest.skip('No image files found in example directory')

        for image_path in image_files[:3]:  # Test first 3 images
            page = PageInfo.load(path=image_path)

            assert page is not None
            assert isinstance(page.content, bytes)
            assert len(page.content) > 0
            assert page.image_width > 0
            assert page.image_height > 0
            assert page.image_size > 0

    def test_page_type_assignment(self, sample_image_path: Path) -> None:
        """Test different page type assignments."""
        page_types = [
            PageType.FRONT_COVER,
            PageType.INNER_COVER,
            PageType.ROUNDUP,
            PageType.STORY,
            PageType.ADVERTISEMENT,
            PageType.EDITORIAL,
            PageType.LETTERS,
            PageType.PREVIEW,
            PageType.BACK_COVER,
            PageType.OTHER,
            PageType.DELETED
        ]

        for page_type in page_types:
            page = PageInfo.load(path=sample_image_path, type=page_type)
            assert page.type == page_type

    def test_page_creation_from_bytes(self, sample_image_path: Path) -> None:
        """Test creating PageInfo directly from bytes."""
        # Read image file as bytes
        with open(sample_image_path, 'rb') as f:
            image_bytes = f.read()

        # Create page from bytes
        page = PageInfo(content=image_bytes, name='test_page.jpg')

        assert page.content == image_bytes
        assert page.name == 'test_page.jpg'
        assert page.image_width > 0
        assert page.image_height > 0
        assert page.image_size > 0

    def test_repr_string(self, sample_image_path: Path) -> None:
        """Test string representation of PageInfo."""
        page = PageInfo.load(path=sample_image_path, type=PageType.STORY)

        repr_str = repr(page)
        assert 'PageInfo' in repr_str
        assert isinstance(repr_str, str)

    def test_page_bookmark_property(self, sample_image_path: Path) -> None:
        """Test page bookmark property."""
        # Test with bookmark
        page = PageInfo.load(path=sample_image_path, bookmark='Chapter 1')
        assert page.bookmark == 'Chapter 1'

        # Test without bookmark
        page_no_bookmark = PageInfo.load(path=sample_image_path)
        assert hasattr(page_no_bookmark, 'bookmark')

    def test_page_double_page_property(self, sample_image_path: Path) -> None:
        """Test page double_page property."""
        page = PageInfo.load(path=sample_image_path, double=True)
        assert page.double

        page_no_double = PageInfo.load(path=sample_image_path)
        assert hasattr(page_no_double, 'double')

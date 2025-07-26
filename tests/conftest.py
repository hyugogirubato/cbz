from pathlib import Path

import pytest

from cbz.comic import ComicInfo
from cbz.page import PageInfo
from cbz.constants import PageType


@pytest.fixture
def fixtures_dir() -> Path:
    """Fixture that provides the path to the test fixtures directory."""
    return Path(__file__).parent / 'fixtures'


@pytest.fixture
def images_dir(fixtures_dir: Path) -> Path:
    """Fixture that provides the path to the test images directory."""
    return fixtures_dir / 'images'


@pytest.fixture
def sample_image_path(images_dir: Path) -> Path:
    """Fixture that provides a sample image path."""
    return images_dir / 'page-000.jpg'


@pytest.fixture
def sample_cbz_file(tmp_path: Path, images_dir: Path) -> Path:
    """Fixture that creates a sample CBZ file for testing."""
    # Load sample pages
    image_paths = sorted(list(images_dir.iterdir()))[:3]  # Use first 3 images
    pages = []

    for i, path in enumerate(image_paths):
        page_type = PageType.FRONT_COVER if i == 0 else PageType.STORY
        page = PageInfo.load(path=path, type=page_type)
        pages.append(page)

    # Create comic from pages
    comic = ComicInfo.from_pages(
        pages=pages,
        title='Test Comic',
        series='Test Series',
        number=1,
        volume=1,
        year=2024
    )

    # Save to temporary file
    cbz_path = tmp_path / 'test_comic.cbz'
    cbz_content = comic.pack()
    cbz_path.write_bytes(cbz_content)

    return cbz_path

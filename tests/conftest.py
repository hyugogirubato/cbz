"""Test fixtures for the CBZ library."""

from pathlib import Path

import pytest

from cbz.collection import ComicCollection, ComicEntry
from cbz.comic import ComicInfo
from cbz.constants import PageType
from cbz.page import PageInfo


@pytest.fixture
def fixtures_dir() -> Path:
    """Path to the test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def images_dir(fixtures_dir: Path) -> Path:
    """Path to the test images directory."""
    return fixtures_dir / "images"


@pytest.fixture
def sample_image_path(images_dir: Path) -> Path:
    """Path to a sample test image."""
    return images_dir / "page-000.jpg"


@pytest.fixture
def sample_cbz_file(tmp_path: Path, images_dir: Path) -> Path:
    """Create a temporary CBZ file for testing."""
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

    cbz_path = tmp_path / "test_comic.cbz"
    cbz_path.write_bytes(comic.pack())
    return cbz_path


@pytest.fixture
def sample_cbc_file(tmp_path: Path, images_dir: Path) -> Path:
    """Create a temporary CBC file for testing."""
    image_paths = sorted(list(images_dir.iterdir()))
    entries = []
    for i, chunk in enumerate((image_paths[:3], image_paths[3:6])):
        pages = [PageInfo.load(path=path) for path in chunk]
        comic = ComicInfo.from_pages(
            pages=pages,
            title=f"Chapter {i + 1}",
            series="Test Series",
            number=i + 1,
        )
        entries.append(ComicEntry(
            name=f"chapter-{i + 1}.cbz",
            title=f"Chapter {i + 1}",
            comic=comic,
        ))

    collection = ComicCollection(entries=entries)
    cbc_path = tmp_path / "test_collection.cbc"
    cbc_path.write_bytes(collection.pack())
    return cbc_path

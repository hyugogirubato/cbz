"""Tests for the ComicCollection (CBC) class."""

import zipfile
from io import BytesIO
from pathlib import Path

import pytest

from cbz.collection import ComicCollection, ComicEntry
from cbz.comic import ComicInfo
from cbz.constants import CBC_NAME
from cbz.exceptions import (
    EmptyArchiveError,
    InvalidMetadataError,
    UnsupportedFormatError
)
from cbz.page import PageInfo


def _make_comic(images_dir: Path, count: int, title: str) -> ComicInfo:
    """Build a small comic from test images."""
    image_paths = sorted(list(images_dir.iterdir()))[:count]
    pages = [PageInfo.load(path=path) for path in image_paths]
    return ComicInfo.from_pages(pages=pages, title=title, series="Test Series")


class TestComicCollection:
    """Tests for CBC collection creation, loading and serialization."""

    def test_from_cbc_file(self, sample_cbc_file: Path) -> None:
        """Load a CBC file and verify entries."""
        collection = ComicCollection.from_cbc(sample_cbc_file)

        assert len(collection) == 2
        names = [entry.name for entry in collection]
        titles = [entry.title for entry in collection]
        assert names == ["chapter-1.cbz", "chapter-2.cbz"]
        assert titles == ["Chapter 1", "Chapter 2"]

        assert all(isinstance(entry.comic, ComicInfo) for entry in collection)
        assert all(len(entry.comic) == 3 for entry in collection)

    def test_comics_property(self, sample_cbc_file: Path) -> None:
        """Verify the comics property."""
        collection = ComicCollection.from_cbc(sample_cbc_file)

        comics = collection.comics
        assert len(comics) == 2
        assert all(isinstance(comic, ComicInfo) for comic in comics)
        assert comics[0].title == "Chapter 1"
        assert comics[1].number == 2

    def test_pack_round_trip(self, images_dir: Path, tmp_path: Path) -> None:
        """Pack a collection and load it back."""
        comics = [
            _make_comic(images_dir, 2, "First Comic"),
            _make_comic(images_dir, 3, "Second Comic"),
        ]
        collection = ComicCollection.from_comics(comics)

        cbc_path = tmp_path / "round_trip.cbc"
        cbc_path.write_bytes(collection.pack())

        loaded = ComicCollection.from_cbc(cbc_path)
        assert len(loaded) == 2
        assert [entry.title for entry in loaded] == ["First Comic", "Second Comic"]
        assert [entry.name for entry in loaded] == ["comic-001.cbz", "comic-002.cbz"]
        assert len(loaded.comics[0]) == 2
        assert len(loaded.comics[1]) == 3

    def test_save(self, images_dir: Path, tmp_path: Path) -> None:
        """Save a collection to disk and load it back."""
        comics = [_make_comic(images_dir, 2, "Saved Comic")]
        collection = ComicCollection.from_comics(comics)

        cbc_path = tmp_path / "saved.cbc"
        collection.save(cbc_path)
        assert cbc_path.exists()

        loaded = ComicCollection.from_cbc(cbc_path)
        assert len(loaded) == 1
        assert loaded[0].title == "Saved Comic"
        assert len(loaded.comics[0]) == 2

    def test_listing_content(self, images_dir: Path) -> None:
        """Verify the generated comics.txt content."""
        comics = [_make_comic(images_dir, 1, "Listed Comic")]
        collection = ComicCollection.from_comics(comics, names=["one.cbz"])

        data = collection.pack()
        with zipfile.ZipFile(BytesIO(data)) as zf:
            listing = zf.read(CBC_NAME).decode("utf-8")
            assert listing == "one.cbz:Listed Comic\n"
            assert set(zf.namelist()) == {CBC_NAME, "one.cbz"}

    def test_from_comics_with_mismatched_lengths(self, images_dir: Path) -> None:
        """Titles or names length must match comics length."""
        comics = [_make_comic(images_dir, 1, "Comic")]
        with pytest.raises(ValueError):
            ComicCollection.from_comics(comics, titles=["A", "B"])
        with pytest.raises(ValueError):
            ComicCollection.from_comics(comics, names=["a.cbz", "b.cbz"])

    def test_sequence_protocol(self, sample_cbc_file: Path) -> None:
        """Verify sequence protocol (iteration, indexing)."""
        collection = ComicCollection.from_cbc(sample_cbc_file)

        entries = [entry for entry in collection]
        assert len(entries) == 2

        first = collection[0]
        assert isinstance(first, ComicEntry)
        assert first in collection

        subset = collection[0:1]
        assert len(subset) == 1

    def test_missing_listing(self, tmp_path: Path, sample_cbz_file: Path) -> None:
        """A CBC without comics.txt is rejected."""
        cbc_path = tmp_path / "no_listing.cbc"
        with zipfile.ZipFile(cbc_path, "w") as zf:
            zf.write(sample_cbz_file, "one.cbz")

        with pytest.raises(InvalidMetadataError):
            ComicCollection.from_cbc(cbc_path)

    def test_empty_listing(self, tmp_path: Path) -> None:
        """A CBC with an empty comics.txt is rejected."""
        cbc_path = tmp_path / "empty.cbc"
        with zipfile.ZipFile(cbc_path, "w") as zf:
            zf.writestr(CBC_NAME, "")

        with pytest.raises(EmptyArchiveError):
            ComicCollection.from_cbc(cbc_path)

    def test_unsupported_nested_format(self, tmp_path: Path) -> None:
        """A listing entry that is not CBZ/CBR is rejected."""
        cbc_path = tmp_path / "bad_format.cbc"
        with zipfile.ZipFile(cbc_path, "w") as zf:
            zf.writestr(CBC_NAME, "one.pdf:Chapter One\n")
            zf.writestr("one.pdf", b"data")

        with pytest.raises(UnsupportedFormatError):
            ComicCollection.from_cbc(cbc_path)

    def test_missing_nested_file(self, tmp_path: Path) -> None:
        """A listing entry referencing a missing file is rejected."""
        cbc_path = tmp_path / "missing.cbc"
        with zipfile.ZipFile(cbc_path, "w") as zf:
            zf.writestr(CBC_NAME, "one.cbz:Chapter One\n")

        with pytest.raises(InvalidMetadataError):
            ComicCollection.from_cbc(cbc_path)

    def test_invalid_utf8_listing(self, tmp_path: Path) -> None:
        """A comics.txt that is not UTF-8 is rejected."""
        cbc_path = tmp_path / "bad_encoding.cbc"
        with zipfile.ZipFile(cbc_path, "w") as zf:
            zf.writestr(CBC_NAME, b"\xff\xfe\xfa")

        with pytest.raises(InvalidMetadataError):
            ComicCollection.from_cbc(cbc_path)

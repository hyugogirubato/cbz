"""
CBC (Comic Book Collection) management module.

Provides the ComicCollection class to create, load and save CBC
files: ZIP archives containing nested CBZ/CBR comics and a UTF-8
comics.txt listing file in the form "filename:title".

Reference: https://manual.calibre-ebook.com/en/conversion.html#comic-book-collections
"""

from __future__ import annotations

import logging
import zipfile
from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path
from typing import Iterator, List, Optional, Union

import rarfile

from cbz.comic import ComicInfo
from cbz.constants import CBC_ARCHIVE_FORMATS, CBC_NAME
from cbz.exceptions import (
    EmptyArchiveError,
    InvalidMetadataError,
    UnsupportedFormatError
)

logger = logging.getLogger(__name__)


@dataclass
class ComicEntry:
    """A single comic within a CBC collection.

    Attributes:
        name: Filename of the comic inside the .cbc archive (e.g. "one.cbz").
        title: Display title from the comics.txt listing.
        comic: The comic itself.
    """

    name: str
    title: str
    comic: ComicInfo


@dataclass
class ComicCollection:
    """Represents a collection of comics packaged as a CBC file.

    A CBC file is a ZIP archive containing nested CBZ/CBR files and a
    comics.txt file (UTF-8) listing each comic as "filename:title".

    Implements the sequence protocol for entry access:
        - len(collection) returns the number of comics
        - collection[i] returns entry i
        - for entry in collection: iterates over entries
    """

    entries: List[ComicEntry] = field(default_factory=list)

    # -- Alternative constructors (factory methods) --

    @classmethod
    def from_comics(
        cls,
        comics: List[ComicInfo],
        titles: Optional[List[str]] = None,
        names: Optional[List[str]] = None,
    ) -> ComicCollection:
        """Create a ComicCollection from a list of comics.

        Args:
            comics: List of ComicInfo objects.
            titles: Optional list of display titles (defaults to each comic's title).
            names: Optional list of archive filenames (defaults to comic-001.cbz, ...).

        Returns:
            New ComicCollection instance.

        Raises:
            ValueError: If titles or names length does not match comics.
        """
        for label, values in (("titles", titles), ("names", names)):
            if values is not None and len(values) != len(comics):
                raise ValueError(f"{label} length does not match comics length")

        entries = []
        for i, comic in enumerate(comics):
            name = names[i] if names else f"comic-{i + 1:03d}.cbz"
            title = titles[i] if titles else comic.title
            entries.append(ComicEntry(name=name, title=title, comic=comic))
        return cls(entries=entries)

    @classmethod
    def from_cbc(cls, path: Union[Path, str]) -> ComicCollection:
        """Load a collection from a CBC (Comic Book Collection) file.

        Reads the comics.txt listing, then loads each referenced
        CBZ/CBR archive in listing order.

        Args:
            path: Path to the .cbc file.

        Returns:
            ComicCollection instance with one entry per listed comic.

        Raises:
            InvalidMetadataError: If comics.txt is missing, not UTF-8 or
                references a missing/malformed entry.
            UnsupportedFormatError: If a listed comic is not a CBZ or CBR file.
            EmptyArchiveError: If no comics are listed.
        """
        path = Path(path)
        with zipfile.ZipFile(path, "r") as archive:
            members = set(archive.namelist())

            if CBC_NAME not in members:
                raise InvalidMetadataError(f"Missing {CBC_NAME} in CBC file")

            try:
                listing = archive.read(CBC_NAME).decode("utf-8")
            except UnicodeDecodeError as e:
                raise InvalidMetadataError(f"{CBC_NAME} must be UTF-8 encoded: {e}") from e

            entries: List[ComicEntry] = []
            for line in listing.splitlines():
                line = line.strip()
                if not line:
                    continue
                if ":" not in line:
                    logger.warning("Skipping invalid %s line: %r", CBC_NAME, line)
                    continue

                name, _, title = line.partition(":")
                name = name.strip()
                title = title.strip()

                suffix = Path(name).suffix.lower()
                if suffix not in CBC_ARCHIVE_FORMATS:
                    raise UnsupportedFormatError(f"Unsupported comic format in collection: {name!r}")
                if name not in members:
                    raise InvalidMetadataError(f"Comic listed in {CBC_NAME} but missing from archive: {name!r}")

                opener = zipfile.ZipFile if suffix == ".cbz" else rarfile.RarFile
                comic = ComicInfo._from_bytes(archive.read(name), opener)
                entries.append(ComicEntry(name=name, title=title, comic=comic))

        if not entries:
            raise EmptyArchiveError(f"No comics listed in {CBC_NAME}")
        return cls(entries=entries)

    # -- Sequence protocol --

    def __len__(self) -> int:
        """Number of comics in the collection."""
        return len(self.entries)

    def __getitem__(self, index):
        """Access a collection entry by index or slice."""
        return self.entries[index]

    def __iter__(self) -> Iterator[ComicEntry]:
        """Iterate over collection entries."""
        return iter(self.entries)

    def __contains__(self, entry: ComicEntry) -> bool:
        """Check if an entry belongs to the collection."""
        return entry in self.entries

    # -- Properties --

    @property
    def comics(self) -> List[ComicInfo]:
        """List of the comics in the collection."""
        return [entry.comic for entry in self.entries]

    # -- Internal methods --

    @staticmethod
    def _clean(value: str) -> str:
        """Normalize a name or title for a single comics.txt line."""
        return " ".join(value.split())

    def _write_cbc(self, zf: zipfile.ZipFile) -> None:
        """Write comics.txt and the nested comics into an open ZIP file."""
        lines: List[str] = []
        used: set = set()
        for i, entry in enumerate(self.entries):
            name = self._clean(entry.name) or f"comic-{i + 1:03d}.cbz"
            if Path(name).suffix.lower() not in CBC_ARCHIVE_FORMATS:
                name += ".cbz"
            base, suffix = name, Path(name).suffix
            counter = 1
            while name in used:
                name = f"{base}{counter}{suffix}"
                counter += 1
            used.add(name)

            title = self._clean(entry.title) or self._clean(entry.comic.title) or name
            lines.append(f"{name}:{title}")
            zf.writestr(name, entry.comic.pack())

        zf.writestr(CBC_NAME, ("\n".join(lines) + "\n").encode("utf-8"))

    # -- Public methods --

    def pack(self, compression: int = zipfile.ZIP_STORED) -> bytes:
        """Pack the collection into CBC format (ZIP archive).

        Each comic is packed as a nested CBZ file and referenced from
        the generated comics.txt listing.

        Args:
            compression: ZIP compression method (default: ZIP_STORED).

        Returns:
            Binary data of the CBC file.
        """
        buf = BytesIO()
        with zipfile.ZipFile(buf, "w", compression) as zf:
            self._write_cbc(zf)
        data = buf.getvalue()
        buf.close()
        return data

    def save(self, path: Union[Path, str], compression: int = zipfile.ZIP_STORED) -> None:
        """Save the collection as a CBC file directly to disk.

        Args:
            path: Destination file path for the .cbc file.
            compression: ZIP compression method (default: ZIP_STORED).
        """
        with zipfile.ZipFile(Path(path), "w", compression) as zf:
            self._write_cbc(zf)

    def show(self) -> None:
        """Display each comic of the collection in the built-in viewer."""
        from cbz.player import Player
        for comic in self.comics:
            Player(comic).run()

"""
Main CBZ comic management module.

Provides the ComicInfo class to create, load, manipulate and
save comics in CBZ, CBR and PDF formats.
"""

from __future__ import annotations

import functools
import logging
import typing
import zipfile
from dataclasses import dataclass, field, fields
from datetime import datetime, timezone
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import Iterator, List, Union

import rarfile
import xmltodict
from pypdf import PdfReader

from cbz.constants import IMAGE_FORMATS, XML_NAME
from cbz.exceptions import EmptyArchiveError, InvalidMetadataError
from cbz.models import ComicModel, PageModel
from cbz.page import PageInfo

logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=None)
def _resolve_type_hints(model_cls: type) -> dict:
    """Resolve dataclass type annotations to actual types.

    Handles optional types (Optional[X] / Union[X, None]) by
    extracting the base type.
    """
    hints = typing.get_type_hints(model_cls)
    resolved = {}
    for name, hint in hints.items():
        origin = getattr(hint, "__origin__", None)
        if origin is Union:
            # Optional[int] == Union[int, None] -> extract the non-None type
            args = [a for a in hint.__args__ if a is not type(None)]
            resolved[name] = args[0] if args else str
        else:
            resolved[name] = hint
    return resolved


def _extract_fields(items: dict, model_cls: type) -> dict:
    """Extract and convert XML fields to Python model fields.

    Iterates over the dataclass fields of model_cls, looks up the
    XML correspondence in items, and converts values to the correct type.

    Args:
        items: Dictionary of parsed XML elements/attributes.
        model_cls: Dataclass class (ComicModel or PageModel).

    Returns:
        Dictionary {python_name: converted_value}.
    """
    type_hints = _resolve_type_hints(model_cls)
    result = {}
    for f in fields(model_cls):
        xml_name = f.metadata.get("xml_name")
        if xml_name and xml_name in items:
            raw = items[xml_name]
            try:
                field_type = type_hints.get(f.name, str)
                result[f.name] = field_type(raw)
            except (ValueError, KeyError):
                logger.warning("Unable to convert field %s=%r", xml_name, raw)
    return result


def _serialize_fields(obj: object, model_cls: type) -> dict:
    """Serialize object fields to an XML dictionary.

    Ignores fields with default/empty values (empty strings, None, UNKNOWN).

    Args:
        obj: Model instance.
        model_cls: Dataclass class of the model.

    Returns:
        Dictionary {xml_name: value} ready for XML serialization.
    """
    result = {}
    for f in fields(model_cls):
        xml_name = f.metadata.get("xml_name")
        if not xml_name:
            continue

        value = getattr(obj, f.name)

        # Skip default / empty values
        if value is None:
            continue
        if isinstance(value, str) and not value:
            continue
        if isinstance(value, Enum) and value == f.default:
            continue

        # Convert enums to their string value
        if isinstance(value, Enum):
            result[xml_name] = value.value
        else:
            result[xml_name] = value

    return result


@dataclass
class ComicInfo(ComicModel):
    """Represents a complete comic with its metadata and pages.

    Supports creation from images, loading from CBZ/CBR/PDF archives,
    serialization to CBZ and display via the built-in viewer.

    Implements the sequence protocol for page access:
        - len(comic) returns the number of pages
        - comic[i] returns page i
        - for page in comic: iterates over pages

    Attributes:
        pages: List of comic pages.
    """

    pages: List[PageInfo] = field(default_factory=list)

    # -- Alternative constructors (factory methods) --

    @classmethod
    def from_pages(cls, pages: List[PageInfo], **kwargs) -> ComicInfo:
        """Create a ComicInfo from a list of pages and metadata.

        Args:
            pages: List of PageInfo objects.
            **kwargs: Comic metadata (title, series, etc.).

        Returns:
            New ComicInfo instance.
        """
        return cls(pages=pages, **kwargs)

    @classmethod
    def _from_archive(cls, path: Union[Path, str], opener: type) -> ComicInfo:
        """Load a comic from an archive file (CBZ or CBR).

        Args:
            path: Path to the archive file.
            opener: Archive class (zipfile.ZipFile or rarfile.RarFile).

        Returns:
            ComicInfo instance with pages and metadata.
        """
        with opener(Path(path), "r") as archive:
            return cls._process_archive(archive)

    @classmethod
    def from_cbz(cls, path: Union[Path, str]) -> ComicInfo:
        """Load a comic from a CBZ (ZIP) file.

        Args:
            path: Path to the .cbz file.

        Returns:
            ComicInfo instance with pages and metadata.

        Raises:
            EmptyArchiveError: If the archive contains no images.
        """
        return cls._from_archive(path, zipfile.ZipFile)

    @classmethod
    def from_cbr(cls, path: Union[Path, str]) -> ComicInfo:
        """Load a comic from a CBR (RAR) file.

        Args:
            path: Path to the .cbr file.

        Returns:
            ComicInfo instance with pages and metadata.

        Raises:
            EmptyArchiveError: If the archive contains no images.
        """
        return cls._from_archive(path, rarfile.RarFile)

    @classmethod
    def from_pdf(cls, path: Union[Path, str]) -> ComicInfo:
        """Load a comic from a PDF file (image extraction).

        Only images are extracted; PDF metadata is not converted
        to ComicInfo metadata.

        Args:
            path: Path to the .pdf file.

        Returns:
            ComicInfo instance with extracted images.

        Raises:
            EmptyArchiveError: If the PDF contains no images.
        """
        pages: List[PageInfo] = []
        reader = PdfReader(Path(path))
        for pdf_page in reader.pages:
            for image in pdf_page.images:
                pages.append(PageInfo.loads(data=image.data))

        if not pages:
            raise EmptyArchiveError("No valid images found in PDF file")
        return cls.from_pages(pages=pages)

    # -- Sequence protocol --

    def __len__(self) -> int:
        """Number of pages in the comic."""
        return len(self.pages)

    def __getitem__(self, index):
        """Access a page by index or slice."""
        return self.pages[index]

    def __iter__(self) -> Iterator[PageInfo]:
        """Iterate over comic pages."""
        return iter(self.pages)

    def __contains__(self, page: PageInfo) -> bool:
        """Check if a page belongs to the comic."""
        return page in self.pages

    # -- Internal methods --

    @classmethod
    def _process_archive(cls, archive) -> ComicInfo:
        """Common processing for CBZ and CBR archives.

        Extracts the ComicInfo.xml file if present, then loads
        images sorted alphabetically.

        Args:
            archive: Open archive object (ZipFile or RarFile).

        Returns:
            ComicInfo instance.
        """
        pages: List[PageInfo] = []
        names = sorted(archive.namelist())
        comic_data: dict = {}

        # Extract XML metadata
        if XML_NAME in names:
            with archive.open(XML_NAME, "r") as f:
                try:
                    comic_data = xmltodict.parse(
                        f.read(), force_list=("Page",)
                    ).get("ComicInfo", {})
                except Exception as e:
                    raise InvalidMetadataError(f"XML parsing error: {e}") from e
            names.remove(XML_NAME)

        # Extract comic fields
        comic_kwargs = _extract_fields(comic_data, ComicModel)

        # Extract page information
        pages_info = comic_data.get("Pages", {}).get("Page", [])

        for i, name in enumerate(names):
            suffix = Path(name).suffix
            if suffix.lower() not in IMAGE_FORMATS:
                logger.warning("Skipping unsupported file: %r", name)
                continue

            with archive.open(name, "r") as f:
                page_kwargs: dict = {}
                if i < len(pages_info):
                    page_kwargs = _extract_fields(pages_info[i], PageModel)
                page_kwargs["name"] = Path(name).name
                pages.append(PageInfo.loads(data=f.read(), **page_kwargs))

        return cls.from_pages(pages=pages, **comic_kwargs)

    def get_info(self) -> dict:
        """Return comic metadata as an XML-ready dictionary.

        Generates a dictionary ready for XML serialization via xmltodict,
        including comic metadata, file information and page details.

        Returns:
            Structured dictionary for XML serialization.
        """
        comic_info = _serialize_fields(self, ComicModel)

        # Build page information
        comic_pages = []
        for i, page in enumerate(self.pages):
            page_info = _serialize_fields(page, PageModel)
            page_info["@Image"] = i
            comic_pages.append(dict(sorted(page_info.items())))

        # File metadata
        utcnow = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        comic_info.update({
            "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
            "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "FileSize": comic_info.get("FileSize", sum(p.image_size for p in self.pages)),
            "FileCreationTime": comic_info.get("FileCreationTime", utcnow),
            "FileModifiedTime": comic_info.get("FileModifiedTime", utcnow),
            "PageCount": len(self.pages),
            "Pages": {"Page": comic_pages},
        })
        return comic_info

    def pack(self, rename: bool = True, compression: int = zipfile.ZIP_STORED) -> bytes:
        """Pack the comic into CBZ format (ZIP archive).

        Args:
            rename: If True, rename pages to sequential format (page-001.jpg).
            compression: ZIP compression method (default: ZIP_STORED).

        Returns:
            Binary data of the CBZ file.
        """
        buf = BytesIO()
        with zipfile.ZipFile(buf, "w", compression) as zf:
            # Write XML metadata
            xml_content = xmltodict.unparse({"ComicInfo": self.get_info()}, pretty=True)
            zf.writestr(XML_NAME, xml_content.replace("></Page>", " />").encode("utf-8"))

            # Write pages
            for i, page in enumerate(self.pages):
                name = page.name
                if not name or rename:
                    name = f"page-{i + 1:03d}{page.suffix}"
                zf.writestr(name, page.content)

        data = buf.getvalue()
        buf.close()
        return data

    def show(self) -> None:
        """Display the comic in the built-in graphical viewer."""
        from cbz.player import Player
        player = Player(self)
        player.run()

    def save(self, path: Union[Path, str], rename: bool = True,
             compression: int = zipfile.ZIP_STORED) -> None:
        """Save the comic as a CBZ file directly to disk.

        More memory-efficient than pack() for large comics since it
        writes directly to the file without an intermediate buffer.

        Args:
            path: Destination file path for the .cbz file.
            rename: If True, rename pages to sequential format (page-001.jpg).
            compression: ZIP compression method (default: ZIP_STORED).
        """
        with zipfile.ZipFile(Path(path), "w", compression) as zf:
            xml_content = xmltodict.unparse({"ComicInfo": self.get_info()}, pretty=True)
            zf.writestr(XML_NAME, xml_content.replace("></Page>", " />").encode("utf-8"))

            for i, page in enumerate(self.pages):
                name = page.name
                if not name or rename:
                    name = f"page-{i + 1:03d}{page.suffix}"
                zf.writestr(name, page.content)

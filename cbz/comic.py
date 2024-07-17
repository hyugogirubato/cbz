from __future__ import annotations

import zipfile

from enum import Enum
from io import BytesIO
from typing import Union
from functools import cache

from pathlib import Path

import fitz
import xmltodict

from cbz.constants import XML_NAME, COMIC_FIELDS, IMAGE_FORMAT, PAGE_FIELDS
from cbz.models import ComicModel
from cbz.page import PageInfo
from cbz.utils import repr_attr


class ComicInfo(ComicModel):
    """
    ComicInfo class that represents the comic book information and pages.
    """

    def __init__(self, pages: list[PageInfo], **kwargs):
        """
        Initialize the ComicInfo instance with pages and additional attributes.

        Args:
            pages (list[PageInfo]): List of PageInfo objects representing the comic pages.
            **kwargs: Additional attributes for the comic.

        Attributes:
            pages (list[PageInfo]): Stores the comic pages.
        """
        super(ComicInfo, self).__init__(**kwargs)
        self.pages = pages

    @classmethod
    def from_pages(cls, pages: list[PageInfo], **kwargs) -> ComicInfo:
        """
        Create a ComicInfo instance from pages and additional attributes.

        Args:
            pages (list[PageInfo]): List of PageInfo objects representing the comic pages.
            **kwargs: Additional attributes for the comic.

        Returns:
            ComicInfo: An instance of ComicInfo.
        """
        return cls(pages, **kwargs)

    @classmethod
    def from_cbz(cls, path: Union[Path, str]) -> ComicInfo:
        """
        Create a ComicInfo instance from a CBZ file.

        Args:
            path (Union[Path, str]): Path to the CBZ file.

        Returns:
            ComicInfo: An instance of ComicInfo.

        Raises:
            ValueError: If the provided path is not a Path object or a string.
        """
        if not isinstance(path, (Path, str)):
            raise ValueError(f'Expecting Path object or path string, got {path!r}')
        return cls.__unpack_zip(path)

    @classmethod
    def from_pdf(cls, path: Union[Path, str]) -> ComicInfo:
        """
        Create a ComicInfo instance from a PDF file.

        Args:
            path (Union[Path, str]): Path to the PDF file.

        Returns:
            ComicInfo: An instance of ComicInfo.

        Raises:
            ValueError: If the provided path is not a Path object or a string.
        """
        if not isinstance(path, (Path, str)):
            raise ValueError(f'Expecting Path object or path string, got {path!r}')
        return cls.__unpack_pdf(path)

    @staticmethod
    def __unpack_pdf(path: Path) -> ComicInfo:
        """
        Unpack a PDF file and create a ComicInfo instance.

        Args:
            path (Path): Path to the PDF file.

        Returns:
            ComicInfo: An instance of ComicInfo.
        """
        pages: list[PageInfo] = []
        with fitz.open(path) as pf:
            for element in pf:
                # Check if the page has images
                images = element.get_images(full=True)
                for i, image in enumerate(images):
                    base = pf.extract_image(image[0])
                    pages.append(PageInfo.loads(data=base['image']))

        assert pages, 'No valid images present in file'
        return ComicInfo.from_pages(pages=pages)

    @staticmethod
    def __unpack_zip(path: Path) -> ComicInfo:
        """
        Unpack a CBZ file and create a ComicInfo instance.

        Args:
            path (Path): Path to the CBZ file.

        Returns:
            ComicInfo: An instance of ComicInfo.
        """

        def __info(items: dict, fields: dict) -> dict:
            """
            Extract and convert field information from the provided items and fields.

            Args:
                items (dict): Dictionary containing item attributes.
                fields (dict): Dictionary containing field mappings and types.

            Returns:
                dict: Dictionary with extracted and converted field information.
            """
            content = {}
            for key, (field_key, field_type) in fields.items():
                if field_key in items:
                    content[key] = field_type(items[field_key])
            return content

        pages = []

        with zipfile.ZipFile(path, 'r', zipfile.ZIP_STORED) as zf:
            names = zf.namelist()
            comic_info = {}

            if XML_NAME in names:
                with zf.open(XML_NAME, 'r') as f:
                    comic_info = xmltodict.parse(f.read(), force_list=('Pages',)).get('ComicInfo', {})
                names.remove(XML_NAME)

            comic = __info(
                items=comic_info,
                fields=COMIC_FIELDS
            )

            pages_info = comic_info.get('Pages', [])
            for i, name in enumerate(names):
                suffix = Path(name).suffix
                if suffix:
                    assert suffix in IMAGE_FORMAT, f'Unsupported image format: {suffix}'
                    with zf.open(name, 'r') as f:
                        page_info = {}
                        if i < len(pages_info):
                            page_info = __info(
                                items=pages_info[i],
                                fields=PAGE_FIELDS
                            )
                        pages.append(PageInfo.loads(data=f.read(), **page_info))

        return ComicInfo.from_pages(pages=pages, **comic)

    def get_info(self) -> dict:
        """
        Get the comic information as a dictionary.

        Returns:
            dict: Dictionary containing comic information.
        """

        def __info(items: dict, fields: dict) -> dict:
            """
            Extract and convert field information from the provided items and fields.

            Args:
                items (dict): Dictionary containing item attributes.
                fields (dict): Dictionary containing field mappings and types.

            Returns:
                dict: Dictionary with extracted and converted field information.
            """
            content = {}
            for key, (field_key, _) in fields.items():
                item = items.get(key)
                if item and not (isinstance(item, Enum) and item.name == 'UNKNOWN' or item == -1):
                    content[field_key] = repr_attr(item)
            return content

        comic_info = __info(
            items={k: v for k, v in self.__dict__.items() if not k.startswith('_')},
            fields=COMIC_FIELDS)

        comic_info['Pages'] = []
        for page in self.pages:
            page_info = __info(
                items={k: v for k, v in page.__dict__.items() if not k.startswith('_')},
                fields=PAGE_FIELDS)
            comic_info['Pages'].append(page_info)

        return comic_info

    @cache
    def pack(self) -> bytes:
        """
        Pack the comic information and pages into a CBZ file format.

        Returns:
            bytes: Bytes representing the packed CBZ file.
        """
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_STORED) as zf:
            zf.writestr(
                XML_NAME,
                xmltodict.unparse({'ComicInfo': self.get_info()}, pretty=True).encode('utf-8')
            )
            for i, page in enumerate(self.pages):
                zf.writestr(f'page-{i + 1:03d}{page.suffix}', page.content)

        packed = zip_buffer.getvalue()
        zip_buffer.close()
        return packed

    def show(self) -> None:
        """
        Display the comic using the Player class.

        This method initializes a Player instance with the comic information
        and starts the player to show the comic.
        """
        # Avoid circular import
        from cbz.player import Player
        player = Player(self)
        player.run()

    def save(self, path: Union[Path, str]) -> None:
        """
        Save the comic book as a CBZ file to the specified path.

        Args:
            path (Union[Path, str]): Path where the CBZ file will be saved.
        """
        with Path(path).open(mode='wb') as f:
            f.write(self.pack())

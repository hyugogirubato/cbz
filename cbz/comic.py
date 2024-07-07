from __future__ import annotations

import json
import zipfile
from io import BytesIO
from pathlib import Path

from typing import Union

import xmltodict

from cbz import utils
from cbz.constants import xml_name
from cbz.models import ComicModel
from cbz.page import PageInfo
from cbz.ui import show_in_tk


class ComicInfo(ComicModel):
    def __init__(self, pages: [PageInfo], **kwargs):
        self.__pages = pages
        super(ComicInfo, self).__init__(kwargs)

    def dumps(self) -> dict:
        return utils.dumps(self._get() | {
            'Pages': [{'Image': i, **page.dumps()} for i, page in enumerate(self.__pages)],
            'PageCount': len(self.__pages)
        })

    def __repr__(self) -> str:
        return json.dumps(self.dumps(), indent=2)

    @classmethod
    def from_pages(cls, pages: [PageInfo], **kwargs) -> ComicInfo:
        return cls(pages, **kwargs)

    def show(self):
        """
        display cbz for preview, after call open ui with info and pages and wait for close preview windows
        :return:
        """
        show_in_tk(self.title, self.__pages, utils.dumps(self._get()))

    @classmethod
    def from_cbz(cls, path: Union[Path, str]) -> ComicInfo:
        """
        read comic from cbz/cbx file
        :param path: path to the file
        :return: Exemplar of ComicInfo class
        """
        if not isinstance(path, (Path, str)):
            raise ValueError(f'Expecting Path object or path string, got {path!r}')
        exemplar = cls(**cls.__unpack(Path(path)))
        exemplar._filepath = path
        return exemplar

    @staticmethod
    def get_info(path: Union[Path, str]) -> dict:
        """
        Get from file only info, without images loading
        :return: dictionary with comic info
        """
        if not isinstance(path, (Path, str)):
            raise ValueError(f'Expecting Path object or path string, got {path!r}')
        with Path(path).open(mode='rb') as f:
            with zipfile.ZipFile(f, 'r', zipfile.ZIP_STORED) as zip_file:
                xml_file = zip_file.open(xml_name)
                info = xmltodict.parse(xml_file.read()).get('ComicInfo', {})
                xml_file.close()
        return info

    def to_cbz(self, path: Union[Path, str]) -> None:
        """
        Save comic to file
        :param path: path for a save (will be overwritten if already exists)
        :return:
        """
        if not isinstance(path, (Path, str)):
            raise ValueError(f'Expecting Path object or path string, got {path!r}')
        self._filepath = path
        new_file = self.pack()
        with Path(path).open(mode='wb') as f:
            f.write(new_file)

    def save(self) -> None:
        """
        Save changes to opened from file or already saved to file comic
        :return:
        """
        assert self._filepath, 'Use to_cbz or from_cbz before save changes'
        self.to_cbz(self._filepath)

    @staticmethod
    def __unpack(file_path: Path) -> dict:
        with zipfile.ZipFile(file_path, 'r', zipfile.ZIP_STORED) as zip_file:
            _files = zip_file.namelist()
            assert xml_name in _files, f'{xml_name} not found in: {zip_file.filename}'
            xml_file = zip_file.open(xml_name)
            info = xmltodict.parse(xml_file.read()).get('ComicInfo', {})
            xml_file.close()
            _files.remove(xml_name)
            info['pages'] = list()
            for filename in _files:
                page_file = zip_file.open(filename)
                info['pages'].append(PageInfo.loads(page_file.read()))
                page_file.close()
        return info

    def pack(self) -> bytes:
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_STORED) as zip_file:
            zip_file.writestr(
                xml_name,
                xmltodict.unparse({'ComicInfo': self.dumps()}, pretty=True).encode('utf-8')
            )
            for i, page in enumerate(self.__pages):
                zip_file.writestr(f'page-{i + 1:03d}{page.suffix}', page.content)
        result = zip_buffer.getvalue()
        zip_buffer.close()
        return result

    def get_page(self, index: int) -> PageInfo:
        """
        Get page by index
        :param index:
        :return:
        """
        return self.__pages[index]

    def show_page(self, index: int) -> None:
        """
        Display page by index
        :param index:
        :return:
        """
        self.__pages[index].show()

    def delete_page(self, index: int) -> PageInfo:
        """
        Delete page by index
        :param index:
        :return: deleted page
        """
        return self.__pages.pop(index)

    def add_page(self, page: PageInfo) -> list[PageInfo]:
        """
        Add new page to the book
        :param page:
        :return: new list of pages
        """
        self.__pages.append(page)
        return self.__pages

    def insert_page(self, index: int, page: PageInfo) -> list[PageInfo]:
        """
        Add new page to position
        :param page:
        :param index:
        :return:
        """
        self.__pages.insert(index, page)
        return self.__pages

    def get_pages_count(self) -> int:
        """
        Get count of pages
        :return:
        """
        return len(self.__pages)

    def get_all_pages(self) -> list[PageInfo]:
        """
        Get all pages of book
        :return:
        """
        return self.__pages

    def save_page(self, index: int, path: Union[Path, str]) -> None:
        """
        Save page to the file
        :param index: page index
        :param path: path to new file, str or Path
        :return:
        """
        self.__pages[index].save(path)

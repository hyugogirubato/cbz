from __future__ import annotations

import json
import zipfile
from io import BytesIO
from typing import Union

import xmltodict
from langcodes import Language
from pathlib import Path

from cbz import utils
from cbz.constants import YesNo, Manga, AgeRating, Format, xml_name
from cbz.models import ComicModel
from cbz.page import PageInfo


def rating(value: int) -> int:
    assert -1 <= value <= 5, 'Rating must be between 0 and 5'
    return value


def language(value: str) -> str:
    if value and not Language.get(value).is_valid():
        raise ValueError('Invalid language')
    return value


class ComicInfo(ComicModel):
    def __init__(self, pages: [PageInfo], **kwargs):
        self.__pages = pages
        # TODO: need change to loop with setattr
        self.title = str(kwargs.get('title', kwargs.get('Title', '')))
        self.series = str(kwargs.get('series', kwargs.get('Series', '')))
        self.number = str(kwargs.get('number', kwargs.get('Number', '')))
        self.count = int(kwargs.get('count', kwargs.get('Count', -1)))
        self.volume = int(kwargs.get('volume', kwargs.get('Volume', -1)))
        self.alternate_series = str(kwargs.get('alternate_series', kwargs.get('AlternateSeries', '')))
        self.alternate_number = str(kwargs.get('alternate_number', kwargs.get('AlternateNumber', '')))
        self.alternate_count = int(kwargs.get('alternate_count', kwargs.get('AlternateCount', -1)))
        self.summary = str(kwargs.get('summary', kwargs.get('Summary', '')))
        self.notes = str(kwargs.get('notes', kwargs.get('Notes', '')))
        self.year = int(kwargs.get('year', kwargs.get('Year', -1)))
        self.month = int(kwargs.get('month', kwargs.get('Month', -1)))
        self.day = int(kwargs.get('day', kwargs.get('Day', -1)))
        self.writer = str(kwargs.get('writer', kwargs.get('Writer', '')))
        self.penciller = str(kwargs.get('penciller', kwargs.get('Penciller', '')))
        self.inker = str(kwargs.get('inker', kwargs.get('Inker', '')))
        self.colorist = str(kwargs.get('colorist', kwargs.get('Colorist', '')))
        self.letterer = str(kwargs.get('letterer', kwargs.get('Letterer', '')))
        self.cover_artist = str(kwargs.get('cover_artist', kwargs.get('CoverArtist', '')))
        self.editor = str(kwargs.get('editor', kwargs.get('Editor', '')))
        self.translator = str(kwargs.get('translator', kwargs.get('Translator', '')))
        self.publisher = str(kwargs.get('publisher', kwargs.get('Publisher', '')))
        self.imprint = str(kwargs.get('imprint', kwargs.get('imprint', 'Imprint')))
        self.genre = str(kwargs.get('genre', kwargs.get('Genre', '')))
        self.tags = str(kwargs.get('tags', kwargs.get('Tags', '')))
        self.web = str(kwargs.get('web', kwargs.get('Web', '')))
        self.language_iso = language(kwargs.get('language_iso', kwargs.get('LanguageISO', '')))
        self.format = Format(kwargs.get('format', kwargs.get('Format', Format.UNKNOWN)))
        self.ean = str(kwargs.get('ean', kwargs.get('EAN', '')))
        self.black_white = YesNo(kwargs.get('black_white', kwargs.get('BlackAndWhite', YesNo.UNKNOWN)))
        self.manga = Manga(kwargs.get('manga', kwargs.get('Manga', Manga.UNKNOWN)))
        self.characters = str(kwargs.get('characters', kwargs.get('Characters', '')))
        self.teams = str(kwargs.get('teams', kwargs.get('Teams', '')))
        self.locations = str(kwargs.get('locations', kwargs.get('Locations', '')))
        self.scan_information = str(kwargs.get('scan_information', kwargs.get('ScanInformation', '')))
        self.story_arc = str(kwargs.get('story_arc', kwargs.get('StoryArc', '')))
        self.story_arc_number = str(kwargs.get('story_arc_number', kwargs.get('StoryArcNumber', '')))
        self.series_group = str(kwargs.get('series_group', kwargs.get('series_group', '')))
        self.age_rating = AgeRating(kwargs.get('age_rating', kwargs.get('AgeRating', AgeRating.UNKNOWN)))
        self.community_rating = rating(kwargs.get('community_rating', kwargs.get('CommunityRating', -1)))
        self.main_character_or_team = str(kwargs.get('main_character_or_team', kwargs.get('MainCharacterOrTeam', '')))
        self.review = str(kwargs.get('review', kwargs.get('Review', '')))

    def dumps(self) -> dict:
        # TODO: need change to loop with getattr
        return utils.dumps({
            'Title': str(self.title),
            'Series': str(self.series),
            'Number': str(self.number),
            'Count': int(self.count),
            'Volume': int(self.volume),
            'AlternateSeries': str(self.alternate_series),
            'AlternateNumber': str(self.alternate_number),
            'AlternateCount': int(self.alternate_count),
            'Summary': str(self.summary),
            'Notes': str(self.notes),
            'Year': int(self.year),
            'Month': int(self.month),
            'Day': int(self.day),
            'Writer': str(self.writer),
            'Penciller': str(self.penciller),
            'Inker': str(self.inker),
            'Colorist': str(self.colorist),
            'Letterer': str(self.letterer),
            'CoverArtist': str(self.cover_artist),
            'Editor': str(self.editor),
            'Translator': str(self.translator),
            'Publisher': str(self.publisher),
            'Imprint': str(self.imprint),
            'Genre': str(self.genre),
            'Tags': str(self.tags),
            'Web': str(self.web),
            'PageCount': len(self.__pages),
            'LanguageISO': language(self.language_iso),
            'Format': self.format,
            'EAN': str(self.ean),
            'BlackAndWhite': self.black_white,
            'Manga': self.manga,
            'Characters': str(self.characters),
            'Teams': str(self.teams),
            'Locations': str(self.locations),
            'ScanInformation': str(self.scan_information),
            'StoryArc': str(self.story_arc),
            'StoryArcNumber': str(self.story_arc_number),
            'SeriesGroup': str(self.series_group),
            'AgeRating': self.age_rating,
            'Pages': [{'Image': i, **page.dumps()} for i, page in enumerate(self.__pages)],
            'CommunityRating': rating(self.community_rating),
            'MainCharacterOrTeam': str(self.main_character_or_team),
            'Review': str(self.review)
        })

    def __repr__(self) -> str:
        return json.dumps(self.dumps(), indent=2)

    @classmethod
    def from_pages(cls, pages: [PageInfo], **kwargs) -> ComicInfo:
        return cls(pages, **kwargs)

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
                info = xmltodict.parse(xml_file.read()).get("ComicInfo", {})
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
        with Path(path).open(mode='wb') as f:
            f.write(self.pack())

    def save(self) -> None:
        """
        Save changes to opened from file or already saved to file comic
        :return:
        """
        assert self._filepath, "Use to_cbz or from_cbz before save changes"
        self.to_cbz(self._filepath)

    @staticmethod
    def __unpack(file_path: Path) -> dict:
        with zipfile.ZipFile(file_path, 'r', zipfile.ZIP_STORED) as zip_file:
            _files = zip_file.namelist()
            assert xml_name in _files, f"{xml_name} not found in: {zip_file.filename}"
            xml_file = zip_file.open(xml_name)
            info = xmltodict.parse(xml_file.read()).get("ComicInfo", {})
            xml_file.close()
            _files.remove(xml_name)
            info["pages"] = list()
            for filename in _files:
                page_file = zip_file.open(filename)
                info["pages"].append(PageInfo.loads(page_file.read()))
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

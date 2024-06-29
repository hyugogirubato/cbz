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
from cbz.page import PageInfo


def rating(value: int) -> int:
    assert -1 <= value <= 5, 'Rating must be between 0 and 5'
    return value


def language(value: str) -> str:
    if value and not Language.get(value).is_valid():
        raise ValueError('Invalid language')
    return value


class ComicInfo:

    def __init__(self, pages: [PageInfo], **kwargs):
        self.__pages = pages
        self.__info = {
            'Title': str(kwargs.get('title', kwargs.get('Title', ''))),
            'Series': str(kwargs.get('series', kwargs.get('Series', ''))),
            'Number': str(kwargs.get('number', kwargs.get('Number', ''))),
            'Count': int(kwargs.get('count', kwargs.get('Count', -1))),
            'Volume': int(kwargs.get('volume', kwargs.get('Volume', -1))),
            'AlternateSeries': str(kwargs.get('alternate_series', kwargs.get('AlternateSeries', ''))),
            'AlternateNumber': str(kwargs.get('alternate_number', kwargs.get('AlternateNumber', ''))),
            'AlternateCount': int(kwargs.get('alternate_count', kwargs.get('AlternateCount', -1))),
            'Summary': str(kwargs.get('summary', kwargs.get('Summary', ''))),
            'Notes': str(kwargs.get('notes', kwargs.get('Notes', ''))),
            'Year': int(kwargs.get('year', kwargs.get('Year', -1))),
            'Month': int(kwargs.get('month', kwargs.get('Month', -1))),
            'Day': int(kwargs.get('day', kwargs.get('Day', -1))),
            'Writer': str(kwargs.get('writer', kwargs.get('Writer', ''))),
            'Penciller': str(kwargs.get('penciller', kwargs.get('Penciller', ''))),
            'Inker': str(kwargs.get('inker', kwargs.get('Inker', ''))),
            'Colorist': str(kwargs.get('colorist', kwargs.get('Colorist', ''))),
            'Letterer': str(kwargs.get('letterer', kwargs.get('Letterer', ''))),
            'CoverArtist': str(kwargs.get('cover_artist', kwargs.get('CoverArtist', ''))),
            'Editor': str(kwargs.get('editor', kwargs.get('Editor', ''))),
            'Translator': str(kwargs.get('translator', kwargs.get('Translator', ''))),
            'Publisher': str(kwargs.get('publisher', kwargs.get('Publisher', ''))),
            'Imprint': str(kwargs.get('imprint', kwargs.get('imprint', 'Imprint'))),
            'Genre': str(kwargs.get('genre', kwargs.get('Genre', ''))),
            'Tags': str(kwargs.get('tags', kwargs.get('Tags', ''))),
            'Web': str(kwargs.get('web', kwargs.get('Web', ''))),
            'PageCount': len(self.__pages),
            'LanguageISO': language(kwargs.get('language_iso', kwargs.get('LanguageISO', ''))),
            'Format': Format(kwargs.get('format', kwargs.get('Format', Format.UNKNOWN))),
            'EAN': str(kwargs.get('ean', kwargs.get('EAN', ''))),
            'BlackAndWhite': YesNo(kwargs.get('black_white', kwargs.get('BlackAndWhite', YesNo.UNKNOWN))),
            'Manga': Manga(kwargs.get('manga', kwargs.get('Manga', Manga.UNKNOWN))),
            'Characters': str(kwargs.get('characters', kwargs.get('Characters', ''))),
            'Teams': str(kwargs.get('teams', kwargs.get('Teams', ''))),
            'Locations': str(kwargs.get('locations', kwargs.get('Locations', ''))),
            'ScanInformation': str(kwargs.get('scan_information', kwargs.get('ScanInformation', ''))),
            'StoryArc': str(kwargs.get('story_arc', kwargs.get('StoryArc', ''))),
            'StoryArcNumber': str(kwargs.get('story_arc_number', kwargs.get('StoryArcNumber', ''))),
            'SeriesGroup': str(kwargs.get('series_group', kwargs.get('series_group', ''))),
            'AgeRating': AgeRating(kwargs.get('age_rating', kwargs.get('AgeRating', AgeRating.UNKNOWN))),
            'Pages': [{'Image': i, **page.dumps()} for i, page in enumerate(pages)],
            'CommunityRating': rating(kwargs.get('community_rating', kwargs.get('CommunityRating', -1))),
            'MainCharacterOrTeam': str(kwargs.get('main_character_or_team', kwargs.get('MainCharacterOrTeam', ''))),
            'Review': str(kwargs.get('review', kwargs.get('Review', '')))
        }

    def dumps(self) -> dict:
        return utils.dumps(self.__info)

    def __repr__(self) -> str:
        return json.dumps(self.dumps(), indent=2)

    @classmethod
    def from_pages(cls, pages: [PageInfo], **kwargs) -> ComicInfo:
        return cls(pages, **kwargs)

    @classmethod
    def from_cbz(cls, path: Union[Path, str]) -> ComicInfo:
        if not isinstance(path, (Path, str)):
            raise ValueError(f'Expecting Path object or path string, got {path!r}')
        return cls(**cls.__unpack(Path(path)))

    @staticmethod
    def __unpack(file_path: Path) -> dict:
        with zipfile.ZipFile(file_path, 'r', zipfile.ZIP_STORED) as zip_file:
            _files = zip_file.namelist()
            assert xml_name in _files, f"{xml_name} not found in: {zip_file.filename}"
            xml_file = zip_file.open(xml_name)
            info = xmltodict.parse(xml_file.read()).get("ComicInfo")
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

        return zip_buffer.getvalue()

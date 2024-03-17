from __future__ import annotations

import json
import zipfile
from io import BytesIO
from typing import Union

import xmltodict
from langcodes import Language
from pathlib import Path

from cbz import utils
from cbz.constants import YesNo, Manga, AgeRating, Format
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
            'Title': str(kwargs.get('title', '')),
            'Series': str(kwargs.get('series', '')),
            'Number': str(kwargs.get('number', '')),
            'Count': int(kwargs.get('count', -1)),
            'Volume': int(kwargs.get('volume', -1)),
            'AlternateSeries': str(kwargs.get('alternate_series', '')),
            'AlternateNumber': str(kwargs.get('alternate_number', '')),
            'AlternateCount': int(kwargs.get('alternate_count', -1)),
            'Summary': str(kwargs.get('summary', '')),
            'Notes': str(kwargs.get('notes', '')),
            'Year': int(kwargs.get('year', -1)),
            'Month': int(kwargs.get('month', -1)),
            'Day': int(kwargs.get('day', -1)),
            'Writer': str(kwargs.get('writer', '')),
            'Penciller': str(kwargs.get('penciller', '')),
            'Inker': str(kwargs.get('inker', '')),
            'Colorist': str(kwargs.get('colorist', '')),
            'Letterer': str(kwargs.get('letterer', '')),
            'CoverArtist': str(kwargs.get('cover_artist', '')),
            'Editor': str(kwargs.get('editor', '')),
            'Translator': str(kwargs.get('translator', '')),
            'Publisher': str(kwargs.get('publisher', '')),
            'Imprint': str(kwargs.get('imprint', '')),
            'Genre': str(kwargs.get('genre', '')),
            'Tags': str(kwargs.get('tags', '')),
            'Web': str(kwargs.get('web', '')),
            'PageCount': len(self.__pages),
            'LanguageISO': language(kwargs.get('language_iso', '')),
            'Format': Format(kwargs.get('format', Format.UNKNOWN)),
            'EAN': str(kwargs.get('ean', '')),
            'BlackAndWhite': YesNo(kwargs.get('black_white', YesNo.UNKNOWN)),
            'Manga': Manga(kwargs.get('manga', Manga.UNKNOWN)),
            'Characters': str(kwargs.get('characters', '')),
            'Teams': str(kwargs.get('teams', '')),
            'Locations': str(kwargs.get('locations', '')),
            'ScanInformation': str(kwargs.get('scan_information', '')),
            'StoryArc': str(kwargs.get('story_arc', '')),
            'StoryArcNumber': str(kwargs.get('story_arc_number', '')),
            'SeriesGroup': str(kwargs.get('series_group', '')),
            'AgeRating': AgeRating(kwargs.get('age_rating', AgeRating.UNKNOWN)),
            'Pages': [{'Image': i, **page.dumps()} for i, page in enumerate(pages)],
            'CommunityRating': rating(kwargs.get('community_rating', -1)),
            'MainCharacterOrTeam': str(kwargs.get('main_character_or_team', '')),
            'Review': str(kwargs.get('review', ''))
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
        with Path(path).open(mode='rb') as f:
            return cls(cls.__unpack(f.read()))

    def __unpack(self, data: bytes) -> tuple[[PageInfo], dict]:
        raise NotImplemented

    def pack(self) -> bytes:
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_STORED) as zip_file:
            zip_file.writestr(
                'ComicInfo.xml',
                xmltodict.unparse({'ComicInfo': self.dumps()}, pretty=True).encode('utf-8')
            )

            for i, page in enumerate(self.__pages):
                zip_file.writestr(f'page-{i + 1:03d}{page.suffix}', page.content)

        return zip_buffer.getvalue()

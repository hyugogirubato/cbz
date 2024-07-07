from cbz.constants import YesNo, Manga, AgeRating, Format, PageType, FIELDS, PAGE_FIELDS
from cbz.utils import _get, _set


class ComicModel:
    title: str = ''
    series: str = ''
    number: str = ''
    count: int = -1
    volume: int = -1
    alternate_series: str = ''
    alternate_number: str = ''
    alternate_count: int = -1
    summary: str = ''
    notes: str = ''
    year: int = -1
    month: int = -1
    day: int = -1
    writer: str = ''
    penciller: str = ''
    inker: str = ''
    colorist: str = ''
    letterer: str = ''
    cover_artist: str = ''
    editor: str = ''
    translator: str = ''
    publisher: str = ''
    imprint: str = ''
    genre: str = ''
    tags: str = ''
    web: str = ''
    language_iso: str = ''
    format: Format = Format.UNKNOWN
    ean: str = ''
    black_white: YesNo = YesNo.UNKNOWN
    manga: Manga = Manga.UNKNOWN
    characters: str = ''
    teams: str = ''
    locations: str = ''
    scan_information: str = ''
    story_arc: str = ''
    story_arc_number: str = ''
    series_group: str = ''
    age_rating: AgeRating = AgeRating.UNKNOWN
    community_rating: int = -1
    main_character_or_team: str = ''
    review: str = ''
    _filepath: str = ''

    def __init__(self, kwargs: dict):
        _set(self, FIELDS, kwargs)

    def _get(self) -> dict:
        return _get(self, FIELDS)


class PageModel:
    suffix: str
    _content: bytes
    type: PageType = PageType.STORY
    double: bool = False
    _image_size: int = 0
    key: str = ''
    bookmark: str = ''
    _image_width: int = 0
    _image_height: int = 0

    def __init__(self, kwargs: dict):
        _set(self, PAGE_FIELDS, kwargs)

    def _get(self) -> dict:
        return _get(self, PAGE_FIELDS)

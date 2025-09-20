from enum import Enum
from typing import Union

from langcodes import Language

XML_NAME = 'ComicInfo.xml'
IMAGE_FORMAT = {
    '.jpeg', '.jpg',   # JPEG (Joint Photographic Experts Group)
    '.png',            # PNG (Portable Network Graphics)
    '.gif',            # GIF (Graphics Interchange Format)
    '.bmp',            # BMP (Bitmap Image File)
    '.tiff', '.tif',   # TIFF (Tagged Image File Format)
    '.webp',           # WebP (Web Picture Format, by Google)
    '.jxl',            # JPEG XL (Next-generation JPEG format)
    '.avif'            # AVIF (AV1 Image File Format, based on AV1 codec)
}


class YesNo(Enum):
    UNKNOWN = 'Unknown'
    NO = 'No'
    YES = 'Yes'


class Manga(Enum):
    UNKNOWN = 'Unknown'
    NO = 'No'
    YES = 'Yes'
    RIGHT_LEFT = 'YesAndRightToLeft'


class PageType(Enum):
    FRONT_COVER = 'FrontCover'
    INNER_COVER = 'InnerCover'
    ROUNDUP = 'Roundup'
    STORY = 'Story'
    ADVERTISEMENT = 'Advertisement'
    EDITORIAL = 'Editorial'
    LETTERS = 'Letters'
    PREVIEW = 'Preview'
    BACK_COVER = 'BackCover'
    OTHER = 'Other'
    DELETED = 'Deleted'


class AgeRating(Enum):
    UNKNOWN = 'Unknown'
    ADULTS18 = 'Adults Only 18+'
    CHILDHOOD = 'Early Childhood'
    EVERYONE = 'Everyone'
    EVERYONE10 = 'Everyone 10+'
    G = 'G'
    KIDS = 'Kids to Adults'
    M = 'M'
    MA15 = 'MA15+'
    MATURE17 = 'Mature 17+'
    PG = 'PG'
    R18 = 'R18+'
    PENDING = 'Rating Pending'
    TEEN = 'Teen'
    X18 = 'X18+'


class Format(Enum):
    UNKNOWN = 'Unknown'
    # ONE_SHOT = '1 Shot'
    # ONE_SHOT = '1/2',
    # ONE_SHOT = '1-Shot'
    ANNOTATION = 'Annotation'
    # ANNOTATIONS = 'Annotations'
    ANNUAL = 'Annual'
    ANTHOLOGY = 'Anthology'
    # BLACK_WHITE = 'B&W'
    # BLACK_WHITE = 'B/W'
    # BLACK_WHITE = 'B&&W'
    BLACK_WHITE = 'Black & White'
    # BOX_SET = 'Box Set'
    BOX_SET = 'Box-Set'
    CROSSOVER = 'Crossover'
    DIRECTOR_CUT = 'Director\'s Cut'
    EPILOGUE = 'Epilogue'
    EVENT = 'Event'
    FCBD = 'FCBD'
    FLYER = 'Flyer'
    # GIANT_SIZE = 'Giant'
    # GIANT_SIZE = 'Giant Size'
    GIANT_SIZE = 'Giant-Size'
    GRAPHIC_NOVEL = 'Graphic Novel'
    # HARDCOVER = 'Hardcover'
    HARDCOVER = 'Hard-Cover'
    # KING_SIZE = 'King'
    # KING_SIZE = 'King Size'
    KING_SIZE = 'King-Size'
    LIMITED_SERIES = 'Limited Series'
    MAGAZINE = 'Magazine'
    NSFW = 'NSFW'
    # ONE_SHOT = 'One Shot'
    ONE_SHOT = 'One-Shot'
    POINT1 = 'Point 1'
    PREVIEW = 'Preview'
    PROLOGUE = 'Prologue'
    REFERENCE = 'Reference'
    REVIEW = 'Review'
    REVIEWED = 'Reviewed'
    SCANLATION = 'Scanlation'
    SCRIPT = 'Script'
    SERIES = 'Series'
    SKETCH = 'Sketch'
    SPECIAL = 'Special'
    # TRADE_PAPER_BACK = 'TPB'
    TRADE_PAPER_BACK = 'Trade Paper Back'
    # WEB_COMIC = 'WebComic'
    WEB_COMIC = 'Web Comic'
    # YEAR_ONE = 'Year 1'
    YEAR_ONE = 'Year One'


class Rating(float):

    def __new__(cls, value: Union[int, float] = -1) -> float:
        assert -1 <= float(value) <= 5, f'Rating must be between 0 and 5, input {value}'
        return super().__new__(cls, value)


class LanguageISO(str):

    def __new__(cls, value: str = '') -> str:
        assert not value or Language.get(str(value)).is_valid(), f'Invalid {value} language'
        return super().__new__(cls, value)


COMIC_FIELDS = {
    'title': ('Title', str),
    'series': ('Series', str),
    'number': ('Number', int),
    'count': ('Count', int),
    'volume': ('Volume', int),
    'alternate_series': ('AlternateSeries', str),
    'alternate_number': ('AlternateNumber', int),
    'alternate_count': ('AlternateCount', int),
    'summary': ('Summary', str),
    'notes': ('Notes', str),
    'year': ('Year', int),
    'month': ('Month', int),
    'day': ('Day', int),
    'writer': ('Writer', str),
    'penciller': ('Penciller', str),
    'inker': ('Inker', str),
    'colorist': ('Colorist', str),
    'letterer': ('Letterer', str),
    'cover_artist': ('CoverArtist', str),
    'editor': ('Editor', str),
    'translator': ('Translator', str),
    'publisher': ('Publisher', str),
    'imprint': ('Imprint', str),
    'genre': ('Genre', str),
    'tags': ('Tags', str),
    'web': ('Web', str),
    'format': ('Format', Format),
    'ean': ('EAN', str),
    'black_white': ('BlackAndWhite', YesNo),
    'manga': ('Manga', Manga),
    'characters': ('Characters', str),
    'teams': ('Teams', str),
    'locations': ('Locations', str),
    'scan_information': ('ScanInformation', str),
    'story_arc': ('StoryArc', str),
    'story_arc_number': ('StoryArcNumber', int),
    'series_group': ('SeriesGroup', str),
    'age_rating': ('AgeRating', AgeRating),
    'main_character_or_team': ('MainCharacterOrTeam', str),
    'review': ('Review', str),
    'language_iso': ('LanguageISO', LanguageISO),
    'community_rating': ('CommunityRating', Rating),
    'added': ('Added', str),
    'released': ('Released', str),
    'file_size': ('FileSize', int),
    'file_modified_time': ('FileModifiedTime', str),
    'file_creation_time': ('FileCreationTime', str),
    'book_price': ('BookPrice', str),
    'custom_values_store': ('CustomValuesStore', str)
}

PAGE_FIELDS = {
    'image': ('@Image', int),
    'type': ('@Type', PageType),
    'double': ('@DoublePage', bool),
    'key': ('@Key', str),
    'bookmark': ('@Bookmark', str),
    'image_size': ('@ImageSize', int),
    'image_width': ('@ImageWidth', int),
    'image_height': ('@ImageHeight', int)
}

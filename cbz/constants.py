from enum import Enum
from langcodes import Language

xml_name = "ComicInfo.xml"


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


class ValidRating(float):
    def __init__(self, val):
        assert -1 <= float(val) <= 5, f'Rating must be between 0 and 5, input {val}'
        super(ValidRating, self).__init__()


class ValidLanguage(str):
    def __init__(self, val):
        if val and not Language.get(str(val)).is_valid():
            raise ValueError(f'Invalid {val} language')
        super(ValidLanguage, self).__init__()


FIELDS = (
    # model: (key, xml key): (variable name, (expected type, second expected type,...))
    # in case of multiple expected formats, value cast to first type in tuple
    (("title", "Title"), ("title", (str,))),
    (("series", "Series"), ("series", (str,))),
    (("number", "Number"), ("number", (str, int, float))),
    (("count", "Count"), ("count", (int,))),
    (("volume", "Volume"), ("volume", (int,))),
    (("alternate_series", "AlternateSeries"), ("alternate_series", (str,))),
    (("alternate_number", "AlternateNumber"), ("alternate_number", (str, int, float))),
    (("alternate_count", "AlternateCount"), ("alternate_count", (int,))),
    (("summary", "Summary"), ("summary", (str,))),
    (("notes", "Notes"), ("notes", (str,))),
    (("year", "Year"), ("year", (int,))),
    (("month", "Month"), ("month", (int,))),
    (("day", "Day"), ("day", (int,))),
    (("writer", "Writer"), ("writer", (str,))),
    (("penciller", "Penciller"), ("penciller", (str,))),
    (("inker", "Inker"), ("inker", (str,))),
    (("colorist", "Colorist"), ("colorist", (str,))),
    (("letterer", "Letterer"), ("letterer", (str,))),
    (("cover_artist", "CoverArtist"), ("cover_artist", (str,))),
    (("editor", "Editor"), ("editor", (str,))),
    (("translator", "Translator"), ("translator", (str,))),
    (("publisher", "Publisher"), ("publisher", (str,))),
    (("imprint", "Imprint"), ("imprint", (str,))),
    (("genre", "Genre"), ("genre", (str,))),
    (("tags", "Tags"), ("tags", (str,))),
    (("web", "Web"), ("web", (str,))),
    (("format", "Format"), ("format", (Format, str))),
    (("ean", "EAN"), ("ean", (str,))),
    (("black_white", "BlackAndWhite"), ("black_white", (YesNo, str))),
    (("manga", "Manga"), ("manga", (Manga, str))),
    (("characters", "Characters"), ("characters", (str,))),
    (("teams", "Teams"), ("teams", (str,))),
    (("locations", "Locations"), ("locations", (str,))),
    (("scan_information", "ScanInformation"), ("scan_information", (str,))),
    (("story_arc", "StoryArc"), ("story_arc", (str,))),
    (("story_arc_number", "StoryArcNumber"), ("story_arc_number", (str,))),
    (("series_group", "SeriesGroup"), ("series_group", (str,))),
    (("age_rating", "AgeRating"), ("age_rating", (AgeRating, str))),
    (("main_character_or_team", "MainCharacterOrTeam"), ("main_character_or_team", (str,))),
    (("review", "Review"), ("review", (str,))),
    (("language_iso", "LanguageISO"), ("language_iso", (ValidLanguage, str))),
    (("community_rating", "CommunityRating"), ("community_rating", (ValidRating, float, int, str))),
)

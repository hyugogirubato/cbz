from cbz.constants import YesNo, Manga, AgeRating, Format, FIELDS
from typing import Any


class ComicModel:
    title: str = ""
    series: str = ""
    number: str = ""
    count: int = -1
    volume: int = -1
    alternate_series: str = ""
    alternate_number: str = ""
    alternate_count: int = -1
    summary: str = ""
    notes: str = ""
    year: int = -1
    month: int = -1
    day: int = -1
    writer: str = ""
    penciller: str = ""
    inker: str = ""
    colorist: str = ""
    letterer: str = ""
    cover_artist: str = ""
    editor: str = ""
    translator: str = ""
    publisher: str = ""
    imprint: str = ""
    genre: str = ""
    tags: str = ""
    web: str = ""
    language_iso: str = ""
    format: Format = Format.UNKNOWN
    ean: str = ""
    black_white: YesNo = YesNo.UNKNOWN
    manga: Manga = Manga.UNKNOWN
    characters: str = ""
    teams: str = ""
    locations: str = ""
    scan_information: str = ""
    story_arc: str = ""
    story_arc_number: str = ""
    series_group: str = ""
    age_rating: AgeRating = AgeRating.UNKNOWN
    community_rating: int = -1
    main_character_or_team: str = ""
    review: str = ""
    _filepath: str = ""

    def __init__(self, kwargs: dict):
        """
        Set class variables from input dictionary, check types of input and cast values to correct type
        :param kwargs: dictionary of input data
        """
        for kwarg_key, kwarg_value in kwargs.items():
            for keys, values in FIELDS:
                if kwarg_key in keys:
                    variable, types = values
                    if hasattr(self, variable):
                        setattr(self, variable, self._check_type(kwarg_key, kwarg_value, types))
                        break

    @staticmethod
    def _check_type(key: str, value: Any, types: tuple) -> Any:
        """
        Check type of value, and cast this value to first type of the types
        :param key: name of key of variable (using only for best error information)
        :param value: value for a check
        :param types: list of the allowed types
        :return: value with new type
        """
        if not isinstance(value, types):
            raise ValueError(
                f"Unexpected type of {key}, got: {type(value).__name__}, expected: {[i.__name__ for i in types]}")
        return types[0](value)

    def _get(self) -> dict:
        """
        Create dictionary from variables by FIELDS
        :return: dictionary with variables value
        """
        return {key[1]: self._check_type(value[0], getattr(self, value[0]), value[1]) for key, value in FIELDS}

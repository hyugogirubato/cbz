from cbz.constants import YesNo, Manga, AgeRating, Format


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

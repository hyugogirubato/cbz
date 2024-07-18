from cbz.constants import COMIC_FIELDS, PAGE_FIELDS, Format, YesNo, Manga, AgeRating, LanguageISO, Rating, PageType
from cbz.utils import verify_attr, default_attr


class BaseModel:

    def __init__(self, fields: dict, **kwargs):
        """
        Initializes the BaseModel instance.

        Args:
            fields (dict): A dictionary mapping attribute names to tuples containing attribute display names
                           and their expected types.
            **kwargs: Additional keyword arguments for initializing attributes.

        Attributes:
            __fields (dict): Stores the fields dictionary passed during initialization.
        """
        self.__fields = fields
        for key, (_, field_type) in self.__fields.items():
            # Set default values for each attribute based on its type
            setattr(self, key, kwargs.get(key, default_attr(field_type)))

    def __setattr__(self, key: str, value: any) -> None:
        """
        Sets the value of an attribute and verifies its type.

        Args:
            key (str): The name of the attribute to set.
            value (any): The value to assign to the attribute.

        Raises:
            TypeError: If the assigned value does not match the expected type for the attribute.
        """
        try:
            field_type = self.__fields[key][1]
            # Convert value to the specified type if necessary
            if field_type not in (int, str, bool):
                value = field_type(value)
            # Verify that the assigned value matches the expected type
            verify_attr(field_type, key, value)
        except (AttributeError, KeyError):
            pass
        super().__setattr__(key, value)

    def __repr__(self) -> str:
        """
        Returns a string representation of the object.

        Returns:
            str: A string representation of the object, displaying its class name and attribute key-value pairs.
        """
        return '{name}({items})'.format(
            name=self.__class__.__name__,
            items=', '.join([f'{k}={repr(v)}' for k, v in self.__dict__.items() if not k.startswith('_')])
        )


class ComicModel(BaseModel):
    """
    Model for representing comic book metadata.
    """
    title: str
    series: str
    number: int
    count: int
    volume: int
    alternate_series: str
    alternate_number: int
    alternate_count: int
    summary: str
    notes: str
    year: int
    month: int
    day: int
    writer: str
    penciller: str
    inker: str
    colorist: str
    letterer: str
    cover_artist: str
    editor: str
    translator: str
    publisher: str
    imprint: str
    genre: str
    tags: str
    web: str
    format: Format
    ean: str
    black_white: YesNo
    manga: Manga
    characters: str
    teams: str
    locations: str
    scan_information: str
    story_arc: str
    story_arc_number: int
    series_group: str
    age_rating: AgeRating
    main_character_or_team: str
    review: str
    language_iso: LanguageISO
    community_rating: Rating
    added: str
    released: str
    file_size: int
    file_modified_time: str
    file_creation_time: str
    book_price: str
    custom_values_store: str

    def __init__(self, **kwargs):
        """
        Initializes a ComicModel instance.

        Args:
            **kwargs: Keyword arguments used to initialize attributes of the ComicModel.
        """
        super(ComicModel, self).__init__(COMIC_FIELDS, **kwargs)


class PageModel(BaseModel):
    """
    Model for representing comic book pages.
    """
    type: PageType
    double: bool
    image_size: int
    key: str
    bookmark: str
    image_width: int
    image_height: int
    suffix: str
    __content: bytes

    def __init__(self, **kwargs):
        """
        Initializes a PageModel instance.

        Args:
            **kwargs: Keyword arguments used to initialize attributes of the PageModel.
        """
        super(PageModel, self).__init__(PAGE_FIELDS, **kwargs)

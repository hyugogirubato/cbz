from cbz.models import BaseModel, ComicModel, PageModel
from cbz.constants import Format, YesNo, Manga, AgeRating, PageType


class TestBaseModel:
    """Test cases for BaseModel class."""

    def test_base_model_creation(self) -> None:
        """Test creating BaseModel with fields."""
        test_fields = {
            'test_str': ('Test String', str),
            'test_int': ('Test Integer', int),
            'test_bool': ('Test Boolean', bool)
        }

        model = BaseModel(fields=test_fields)

        # Check default values are set
        assert hasattr(model, 'test_str')
        assert hasattr(model, 'test_int')
        assert hasattr(model, 'test_bool')

    def test_base_model_with_kwargs(self) -> None:
        """Test creating BaseModel with keyword arguments."""
        test_fields = {
            'title': ('Title', str),
            'number': ('Number', int),
            'published': ('Published', bool)
        }

        model = BaseModel(
            fields=test_fields,
            title='Test Title',
            number=42,
            published=True
        )

        assert model.title == 'Test Title'
        assert model.number == 42
        assert model.published

    def test_attribute_type_verification(self) -> None:
        """Test that attribute types are verified on assignment."""
        test_fields = {
            'count': ('Count', int),
            'name': ('Name', str)
        }

        model = BaseModel(fields=test_fields)

        # Valid assignments
        model.count = 10
        model.name = 'Test'

        assert model.count == 10
        assert model.name == 'Test'

    def test_repr_method(self) -> None:
        """Test string representation of BaseModel."""
        test_fields = {
            'title': ('Title', str)
        }

        model = BaseModel(fields=test_fields, title='Test')
        repr_str = repr(model)

        assert isinstance(repr_str, str)
        assert 'BaseModel' in repr_str


class TestComicModel:
    """Test cases for ComicModel class."""

    def test_comic_model_creation(self) -> None:
        """Test creating ComicModel with default values."""
        model = ComicModel()

        # Check that comic-specific attributes exist
        assert hasattr(model, 'title')
        assert hasattr(model, 'series')
        assert hasattr(model, 'number')
        assert hasattr(model, 'volume')
        assert hasattr(model, 'year')
        assert hasattr(model, 'month')
        assert hasattr(model, 'day')

    def test_comic_model_with_values(self) -> None:
        """Test creating ComicModel with specific values."""
        model = ComicModel(
            title='Test Comic',
            series='Test Series',
            number=1,
            volume=1,
            year=2024,
            month=6,
            day=15,
            writer='Test Writer',
            publisher='Test Publisher',
            language_iso='en',
            format=Format.SERIES,
            black_white=YesNo.NO,
            manga=Manga.RIGHT_LEFT,
            age_rating=AgeRating.EVERYONE
        )

        assert model.title == 'Test Comic'
        assert model.series == 'Test Series'
        assert model.number == 1
        assert model.volume == 1
        assert model.year == 2024
        assert model.month == 6
        assert model.day == 15
        assert model.writer == 'Test Writer'
        assert model.publisher == 'Test Publisher'
        assert model.language_iso == 'en'
        assert model.format == Format.SERIES
        assert model.black_white == YesNo.NO
        assert model.manga == Manga.RIGHT_LEFT
        assert model.age_rating == AgeRating.EVERYONE

    def test_comic_model_enum_properties(self) -> None:
        """Test that enum properties work correctly."""
        model = ComicModel()

        # Test format enum
        model.format = Format.PREVIEW
        assert model.format == Format.PREVIEW

        # Test yes/no enum
        model.black_white = YesNo.YES
        assert model.black_white == YesNo.YES

        # Test manga enum
        model.manga = Manga.RIGHT_LEFT
        assert model.manga == Manga.RIGHT_LEFT

        # Test age rating enum
        model.age_rating = AgeRating.TEEN
        assert model.age_rating == AgeRating.TEEN

    def test_comic_model_metadata_fields(self) -> None:
        """Test comic metadata fields."""
        model = ComicModel(
            summary='Test summary',
            notes='Test notes',
            genre='Adventure',
            web='http://example.com',
            ean='1234567890123',
            community_rating=5,
            main_character_or_team='Hero',
            characters='Hero, Villain',
            teams='Justice League',
            locations='Metropolis',
            scan_information='Scanned by Test',
            story_arc='Origin Story',
            series_group='DC Comics',
            alternate_series='Alternate Universe',
            alternate_number=2,
            alternate_count=10
        )

        assert model.summary == 'Test summary'
        assert model.notes == 'Test notes'
        assert model.genre == 'Adventure'
        assert model.web == 'http://example.com'
        assert model.ean == '1234567890123'
        assert model.community_rating == 5
        assert model.main_character_or_team == 'Hero'
        assert model.characters == 'Hero, Villain'
        assert model.teams == 'Justice League'
        assert model.locations == 'Metropolis'
        assert model.scan_information == 'Scanned by Test'
        assert model.story_arc == 'Origin Story'
        assert model.series_group == 'DC Comics'
        assert model.alternate_series == 'Alternate Universe'
        assert model.alternate_number == 2
        assert model.alternate_count == 10


class TestPageModel:
    """Test cases for PageModel class."""

    def test_page_model_creation(self) -> None:
        """Test creating PageModel with default values."""
        model = PageModel()

        # Check that page-specific attributes exist
        assert hasattr(model, 'image')
        assert hasattr(model, 'type')
        assert hasattr(model, 'double')
        assert hasattr(model, 'image_size')
        assert hasattr(model, 'key')
        assert hasattr(model, 'bookmark')
        assert hasattr(model, 'image_width')
        assert hasattr(model, 'image_height')
        assert hasattr(model, 'image_size')
        # Note: format is not a base field in PageModel

    def test_page_model_with_values(self) -> None:
        """Test creating PageModel with specific values."""
        model = PageModel(
            type=PageType.FRONT_COVER,
            double=True,
            image_size=1024000,
            key='cover',
            bookmark='Chapter 1',
            image_width=800,
            image_height=1200,
        )

        assert model.type == PageType.FRONT_COVER
        assert model.double
        assert model.image_size == 1024000
        assert model.key == 'cover'
        assert model.bookmark == 'Chapter 1'
        assert model.image_width == 800
        assert model.image_height == 1200

    def test_page_model_page_types(self) -> None:
        """Test different page types."""
        page_types = [
            PageType.FRONT_COVER,
            PageType.INNER_COVER,
            PageType.ROUNDUP,
            PageType.STORY,
            PageType.ADVERTISEMENT,
            PageType.EDITORIAL,
            PageType.LETTERS,
            PageType.PREVIEW,
            PageType.BACK_COVER,
            PageType.OTHER,
            PageType.DELETED
        ]

        for page_type in page_types:
            model = PageModel(type=page_type)
            assert model.type == page_type

    def test_page_model_boolean_properties(self) -> None:
        """Test boolean properties in PageModel."""
        model = PageModel()

        # Test double property
        model.double = True
        assert model.double

        model.double = False
        assert not model.double

    def test_page_model_numeric_properties(self) -> None:
        """Test numeric properties in PageModel."""
        model = PageModel(
            image_size=2048000,
            image_width=1920,
            image_height=1080
        )

        assert model.image_size == 2048000
        assert model.image_width == 1920
        assert model.image_height == 1080

        # Test that they're integers
        assert isinstance(model.image_size, int)
        assert isinstance(model.image_width, int)
        assert isinstance(model.image_height, int)

from cbz.comic import ComicInfo
from cbz.page import PageInfo
from cbz.constants import PageType, YesNo, Manga, AgeRating, Format

class TestComicInfo:
    """Test cases for ComicInfo class."""

    def test_from_pages_creation(self, images_dir):
        """Test creating ComicInfo from pages."""
        # Load sample pages
        image_paths = sorted(list(images_dir.iterdir()))[:3]  # Use first 3 images
        pages = []
        
        for i, path in enumerate(image_paths):
            page_type = PageType.FRONT_COVER if i == 0 else PageType.STORY
            page = PageInfo.load(path=path, type=page_type)
            pages.append(page)
        
        # Create comic from pages
        comic = ComicInfo.from_pages(
            pages=pages,
            title="Test Comic",
            series="Test Series",
            number=1,
            volume=1,
            year=2024
        )
        
        assert comic.title == "Test Comic"
        assert comic.series == "Test Series"
        assert comic.number == 1
        assert comic.volume == 1
        assert comic.year == 2024
        assert len(comic.pages) == 3
        assert comic.pages[0].type == PageType.FRONT_COVER
        assert comic.pages[1].type == PageType.STORY

    def test_from_cbz_file(self, sample_cbz_file):
        """Test loading ComicInfo from CBZ file."""
        comic = ComicInfo.from_cbz(sample_cbz_file)
        
        assert comic is not None
        assert hasattr(comic, 'pages')
        assert len(comic.pages) > 0
        assert all(isinstance(page, PageInfo) for page in comic.pages)

    def test_pack_cbz(self, images_dir):
        """Test packing comic into CBZ format."""
        # Create a simple comic
        image_paths = sorted(list(images_dir.iterdir()))[:2]
        pages = [PageInfo.load(path=path) for path in image_paths]
        
        comic = ComicInfo.from_pages(
            pages=pages,
            title="Pack Test",
            series="Test Series"
        )
        
        # Pack to CBZ
        cbz_content = comic.pack()
        
        assert isinstance(cbz_content, bytes)
        assert len(cbz_content) > 0

    def test_pack_with_rename(self, images_dir):
        """Test packing comic with page renaming."""
        image_paths = sorted(list(images_dir.iterdir()))[:2]
        pages = [PageInfo.load(path=path) for path in image_paths]
        
        comic = ComicInfo.from_pages(
            pages=pages,
            title="Rename Test"
        )
        
        # Pack with rename option
        cbz_content = comic.pack(rename=True)
        
        assert isinstance(cbz_content, bytes)
        assert len(cbz_content) > 0

    def test_comic_metadata_properties(self, images_dir):
        """Test comic metadata properties."""
        image_paths = sorted(list(images_dir.iterdir()))[:1]
        pages = [PageInfo.load(path=path) for path in image_paths]
        
        comic = ComicInfo.from_pages(
            pages=pages,
            title="Metadata Test",
            series="Test Series",
            number=5,
            count=10,
            volume=2,
            summary="Test summary",
            year=2023,
            month=6,
            day=15,
            writer="Test Writer",
            penciller="Test Penciller",
            inker="Test Inker",
            colorist="Test Colorist",
            letterer="Test Letterer",
            cover_artist="Test Cover Artist",
            editor="Test Editor",
            publisher="Test Publisher",
            imprint="Test Imprint",
            genre="Test Genre",
            language_iso="en",
            format=Format.SERIES,
            black_white=YesNo.NO,
            manga=Manga.RIGHT_LEFT,
            age_rating=AgeRating.TEEN,
            community_rating=4
        )
        
        assert comic.title == "Metadata Test"
        assert comic.series == "Test Series"
        assert comic.number == 5
        assert comic.count == 10
        assert comic.volume == 2
        assert comic.summary == "Test summary"
        assert comic.year == 2023
        assert comic.month == 6
        assert comic.day == 15
        assert comic.writer == "Test Writer"
        assert comic.penciller == "Test Penciller"
        assert comic.inker == "Test Inker"
        assert comic.colorist == "Test Colorist"
        assert comic.letterer == "Test Letterer"
        assert comic.cover_artist == "Test Cover Artist"
        assert comic.editor == "Test Editor"
        assert comic.publisher == "Test Publisher"
        assert comic.imprint == "Test Imprint"
        assert comic.genre == "Test Genre"
        assert comic.language_iso == "en"
        assert comic.format == Format.SERIES
        assert comic.black_white == YesNo.NO
        assert comic.manga == Manga.RIGHT_LEFT
        assert comic.age_rating == AgeRating.TEEN
        assert comic.community_rating == 4

    def test_page_count_property(self, images_dir):
        """Test that page count returns correct count."""
        image_paths = sorted(list(images_dir.iterdir()))[:4]
        pages = [PageInfo.load(path=path) for path in image_paths]
        
        comic = ComicInfo.from_pages(pages=pages, title="Count Test")
        
        assert len(comic.pages) == 4

    def test_empty_pages_list(self):
        """Test creating comic with empty pages list."""
        comic = ComicInfo.from_pages(pages=[], title="Empty Test")
        
        assert comic.title == "Empty Test"
        assert len(comic.pages) == 0
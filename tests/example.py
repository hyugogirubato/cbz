from pathlib import Path

from cbz.comic import ComicInfo
from cbz.constants import PageType, YesNo, Manga, AgeRating, Format
from cbz.page import PageInfo

PARENT = Path(__file__).parent

if __name__ == '__main__':
    paths = list((PARENT / 'fixtures' / 'images').iterdir())

    # Load each page from the 'images' folder into a list of PageInfo objects
    pages = [
        PageInfo.load(
            path=path,
            type=PageType.FRONT_COVER if i == 0 else PageType.BACK_COVER if i == len(paths) - 1 else PageType.STORY
        )
        for i, path in enumerate(paths)
    ]

    # Create a ComicInfo object using ComicInfo.from_pages() method
    comic = ComicInfo.from_pages(
        pages=pages,
        title='T1 - Arrête de me chauffer, Nagatoro',
        series='Arrête de me chauffer, Nagatoro',
        number=1,
        count=8,
        volume=1,
        summary='Nagatoro est en seconde. Pleine d\u2019assurance, joueuse, moqueuse, elle se d\u00e9couvre un jour un passe-temps favori : martyriser son \u201cSenpai\u201d, lyc\u00e9en de premi\u00e8re timide et mal dans sa peau. Nagatoro taquine, agace, aguiche, va parfois trop loin... mais qu\u2019a-t-elle vraiment derri\u00e8re la t\u00eate ? Et si derri\u00e8re ses moqueries elle cachait une v\u00e9ritable affection ?  Et si finalement, ses farces permettaient \u00e0 Senpai de s\u2019affirmer ?',
        year=2021,
        month=3,
        day=12,
        writer='Nanashi',
        inker='Nanashi',
        editor='Noeve Grafx',
        publisher='Noeve Grafx',
        imprint='Noeve Grafx',
        genre='Shonen',
        web='http://www.izneo.com/en/manga/shonen/arrete-de-me-chauffer-nagatoro-37560/arrete-de-me-chauffer-nagatoro-86232',
        language_iso='fr',
        format=Format.PREVIEW,
        black_white=YesNo.YES,
        manga=Manga.RIGHT_LEFT,
        age_rating=AgeRating.EVERYONE10,
        community_rating=5,
        ean='9782490676569'
    )

    # Show the comic using the show()
    comic.show()

    # Pack the comic book content into a CBZ file format
    cbz_content = comic.pack(rename=True)

    # Define the path where the CBZ file will be saved
    cbz_path = PARENT / f'{comic.title}.cbz'

    # Write the CBZ content to the specified path
    cbz_path.write_bytes(cbz_content)

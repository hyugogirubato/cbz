from pathlib import Path

from cbz.comic import ComicInfo
from cbz.constants import PageType, YesNo, Manga, AgeRating, Format
from cbz.page import PageInfo

PARENT = Path()

if __name__ == '__main__':
    # @Info: Load comic pages
    paths = list((PARENT / 'images').iterdir())
    pages = [PageInfo.load(
        path=path,
        type=PageType.FRONT_COVER if i == 0 else PageType.BACK_COVER if i == len(paths) - 1 else PageType.STORY
    ) for i, path in enumerate(paths)]

    # @Info: Load comic metadata
    comic = ComicInfo.from_pages(
        pages=pages,
        title='T1 - Arrête de me chauffer, Nagatoro',
        series='Arrête de me chauffer, Nagatoro',
        number='1',
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

    # @Info: Pack cbz
    cbz_content = comic.pack()

    # @Info: Write cbz
    cbz_path = PARENT / 'Arrête de me chauffer, Nagatoro.cbz'
    cbz_path.write_bytes(cbz_content)

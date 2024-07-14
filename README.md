# CBZ

CBZ is a Python library designed for creating, manipulating, and viewing comic book files in CBZ format. It offers a straightforward interface to pack comic pages into CBZ archives, extract metadata, and display comics using a built-in player.

## Features

- 🚀 Seamless Installation via [pip](#installation)
- 📚 Pack images into CBZ format for comics and manga
- 📝 Extract and manage title, series, format, and more
- 🖼️ Handle comic pages with attributes like type and format
- 📦 Unpack CBZ files to retrieve comic information
- 🛠️ Built-in player for viewing CBZ comics
- ❤️ Fully Open-Source! Pull Requests Welcome

## Installation

Install KeyDive from PyPI using Poetry:

```shell
pip install cbz
```

## Quick Start

Here's a quick example of how to create a CBZ file from a series of images:

````python
from pathlib import Path

from cbz.comic import ComicInfo
from cbz.constants import PageType, YesNo, Manga, AgeRating, Format
from cbz.page import PageInfo

PARENT = Path(__file__).parent

if __name__ == '__main__':
    paths = list(Path('path/to/your/images').iterdir())

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
        title='Your Comic Title',
        series='Your Comic Series',
        number=1,
        language_iso='en',
        format=Format.WEB_COMIC,
        black_white=YesNo.NO,
        manga=Manga.NO,
        age_rating=AgeRating.PENDING
    )

    # Show the comic using the show()
    comic.show()

    # Pack the comic book content into a CBZ file format
    cbz_content = comic.pack()

    # Define the path where the CBZ file will be saved
    cbz_path = PARENT / 'your_comic.cbz'

    # Write the CBZ content to the specified path
    cbz_path.write_bytes(cbz_content)
````

## Player

CBZ includes a command-line player for viewing CBZ comic book files. Simply run cbzplayer <file> to launch the player with the specified CBZ file.

````shell
usage: cbzplayer [-h] <file>

Launch CBZ player with a comic book file

positional arguments:
  <file>      Path to the CBZ comic book file.

options:
  -h, --help  show this help message and exit

````

## Detailed Usage

### Creating a ComicInfo Object

The `ComicInfo` class represents a comic book with metadata and pages. It supports initialization from a list of `PageInfo` objects:

```python
from cbz.comic import ComicInfo
from cbz.page import PageInfo

# Example usage:
pages = [
    PageInfo.load(path='/path/to/page1.jpg', type=PageType.FRONT_COVER),
    PageInfo.load(path='/path/to/page2.jpg', type=PageType.STORY),
    PageInfo.load(path='/path/to/page3.jpg', type=PageType.BACK_COVER),
]

comic = ComicInfo.from_pages(
    pages=pages,
    title='My Comic',
    series='Comic Series',
    number=1,
    language_iso='en',
    format=Format.WEB_COMIC,
    black_white=YesNo.NO,
    manga=Manga.NO,
    age_rating=AgeRating.PENDING
)
```

### Extracting Metadata

Retrieve comic information as a dictionary using `get_info()`:

```python
info = comic.get_info()
print(info)
```

### Packing into CBZ Format

Pack the comic into a CBZ file format:

```python
cbz_content = comic.pack()
```

### Unpacking from CBZ

Load a comic from an existing CBZ file:

```python
comic_from_cbz = ComicInfo.from_cbz('/path/to/your_comic.cbz')
```

## Contributors

<a href="https://github.com/hyugogirubato"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/65763543?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="hyugogirubato"/></a>
<a href="https://github.com/piskunqa"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/38443069?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="piskunqa"/></a>
<a href="https://github.com/OleskiiPyskun"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/75667382?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="OleskiiPyskun"/></a>
<a href="https://github.com/domenicoblanco"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/9018104?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="domenicoblanco"/></a>
<a href="https://github.com/RivMt"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/40086827?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="RivMt"/></a>

## Licensing

This software is licensed under the terms of [MIT License](https://github.com/hyugogirubato/cbz/blob/main/LICENSE).  
You can find a copy of the license in the LICENSE file in the root folder.

* * * 

© hyugogirubato 2024
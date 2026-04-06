# CBZ

CBZ is a Python library designed for creating, manipulating, and viewing comic book files in CBZ, CBR, and PDF formats. It offers a straightforward interface to pack comic pages into CBZ archives, extract metadata from CBZ and CBR files, and display comics using a built-in player.

## Features

- Seamless installation via [pip](#installation)
- Pack images into CBZ format for comics and manga
- Extract and manage metadata: title, series, format, and more
- Handle comic pages with attributes like type, dimensions, and bookmarks
- Unpack CBZ and CBR files to retrieve comic information, or extract images from PDF files
- Built-in player for viewing CBZ, CBR, and PDF comics
- Sequence protocol: iterate, index, and slice comic pages directly
- Dataclass-based models with automatic XML mapping and strict type validation
- Image support: JPEG, PNG, GIF, BMP, TIFF, WebP, JPEG XL, AVIF
- Fully open-source! Pull requests welcome

## Installation

Install CBZ from PyPI using pip:

```shell
pip install cbz
```

With AVIF and JPEG XL support:

```shell
pip install cbz[pillow]
```

## Quick Start

Here's a quick example of how to create a CBZ file from a series of images:

```python
from pathlib import Path

from cbz import ComicInfo, PageInfo, PageType, Format, YesNo, Manga, AgeRating

if __name__ == "__main__":
    paths = sorted(Path("path/to/your/images").iterdir())

    # Load each page from the images folder into a list of PageInfo objects
    pages = [
        PageInfo.load(
            path=path,
            type=(
                PageType.FRONT_COVER if i == 0
                else PageType.BACK_COVER if i == len(paths) - 1
                else PageType.STORY
            ),
        )
        for i, path in enumerate(paths)
    ]

    # Create a ComicInfo object with metadata
    comic = ComicInfo.from_pages(
        pages=pages,
        title="Your Comic Title",
        series="Your Comic Series",
        number=1,
        language_iso="en",
        format=Format.WEB_COMIC,
        black_white=YesNo.NO,
        manga=Manga.NO,
        age_rating=AgeRating.RATING_PENDING,
    )

    # Display the comic in the built-in reader
    comic.show()

    # Save directly as a CBZ file
    comic.save("your_comic.cbz")

    # Or pack to bytes for custom handling
    cbz_content = comic.pack()
    Path("your_comic.cbz").write_bytes(cbz_content)
```

## Player

CBZ includes a command-line player for viewing comic book files in multiple formats. Simply run `cbzplayer <file>` to launch the player with the specified comic book file.

### Supported Formats

- **CBZ** (Comic Book ZIP) - Standard ZIP archives containing images and metadata
- **CBR** (Comic Book RAR) - RAR archives containing images and metadata
- **PDF** - Portable Document Format files with embedded images (images only, no metadata)

### Usage

```shell
usage: cbzplayer [-h] <file>

CBZ/CBR/PDF comic reader

positional arguments:
<file>      Path to the CBZ, CBR or PDF comic book file.

options:
-h, --help  show this help message and exit
```

### Examples

```shell
# View a CBZ file
cbzplayer my_comic.cbz

# View a CBR file
cbzplayer my_comic.cbr

# View a PDF file
cbzplayer my_comic.pdf
```

### Keyboard Shortcuts

| Shortcut            | Action            |
|---------------------|-------------------|
| Left / Right arrows | Navigate pages    |
| + / -               | Zoom in / out     |
| Ctrl+Q              | Quit              |
| Mouse wheel         | Vertical scroll   |
| Shift+Mouse wheel   | Horizontal scroll |
| Ctrl+Mouse wheel    | Zoom              |

### Requirements for CBR Support

CBR file support requires:

- The `rarfile` Python package (automatically installed with CBZ)
- An external RAR extraction tool such as:
    - `unrar` (recommended) - Available in most package managers
    - `rar` - Commercial RAR archiver
    - `7zip` - Free alternative with RAR support

For installation instructions and compatibility details, see the [rarfile documentation](https://github.com/markokr/rarfile).

## Detailed Usage

### Creating a ComicInfo Object

The `ComicInfo` class represents a comic book with metadata and pages. It supports initialization from a list of `PageInfo` objects:

```python
from cbz import ComicInfo, PageInfo, PageType, Format, YesNo, Manga, AgeRating

pages = [
    PageInfo.load(path="page1.jpg", type=PageType.FRONT_COVER),
    PageInfo.load(path="page2.jpg", type=PageType.STORY),
    PageInfo.load(path="page3.jpg", type=PageType.BACK_COVER),
]

comic = ComicInfo.from_pages(
    pages=pages,
    title="My Comic",
    series="Comic Series",
    number=1,
    language_iso="en",
    format=Format.WEB_COMIC,
    black_white=YesNo.NO,
    manga=Manga.NO,
    age_rating=AgeRating.RATING_PENDING,
)
```

You can also create pages directly from bytes or base64-encoded data:

```python
page = PageInfo.loads(data=image_bytes, name="page.jpg", type=PageType.STORY)
```

### Sequence Protocol

`ComicInfo` implements the full sequence protocol, so you can interact with pages directly:

```python
len(comic)  # Number of pages
comic[0]  # First page
comic[-1]  # Last page
comic[1:3]  # Slice of pages
for page in comic:  # Iteration
    print(page.image_width, page.image_height)
page in comic  # Containment check
```

### Extracting Metadata

Retrieve comic information as a dictionary using `get_info()`:

```python
info = comic.get_info()
print(info)
```

### Packing and Saving

Pack the comic into CBZ format as bytes:

```python
cbz_content = comic.pack()
```

Or save directly to disk (more memory-efficient for large archives):

```python
comic.save("output.cbz")
```

### Loading from Different Formats

Load a comic from an existing CBZ file (with metadata):

```python
comic = ComicInfo.from_cbz("your_comic.cbz")
```

Load a comic from an existing CBR file (with metadata):

```python
comic = ComicInfo.from_cbr("your_comic.cbr")
```

Load a comic from a PDF file (images only, no metadata):

```python
comic = ComicInfo.from_pdf("your_comic.pdf")
```

**Notes:**

- CBR support requires an external RAR extraction tool. For detailed compatibility information and advanced configuration, see the [rarfile documentation](https://github.com/markokr/rarfile).
- PDF files only provide image content; comic metadata (title, series, etc.) is not available from PDF files.

### Page Properties

Each `PageInfo` object exposes the following properties, automatically extracted from the image content:

```python
page = comic[0]

page.content  # bytes - raw image data
page.image_width  # int - width in pixels
page.image_height  # int - height in pixels
page.image_size  # int - file size in bytes
page.suffix  # str - file extension (.jpg, .png, etc.)
page.name  # str - original file name
page.type  # PageType - page type (FrontCover, Story, etc.)
page.bookmark  # str - bookmark / chapter name
page.double  # bool - double page spread
```

### Metadata Fields

All [ComicInfo.xml](docs/RFC-CBZ.md) v2.1 metadata fields are supported as dataclass attributes:

| Attribute                | Type               | Default   | Description                              |
|--------------------------|--------------------|-----------|------------------------------------------|
| `title`                  | `str`              | `""`      | Issue title                              |
| `series`                 | `str`              | `""`      | Series name                              |
| `number`                 | `Optional[int]`    | `None`    | Issue number                             |
| `count`                  | `Optional[int]`    | `None`    | Total number of issues                   |
| `volume`                 | `Optional[int]`    | `None`    | Volume number                            |
| `year`                   | `Optional[int]`    | `None`    | Publication year                         |
| `month`                  | `Optional[int]`    | `None`    | Publication month                        |
| `day`                    | `Optional[int]`    | `None`    | Publication day                          |
| `writer`                 | `str`              | `""`      | Writer(s), comma-separated               |
| `penciller`              | `str`              | `""`      | Pencil artist(s)                         |
| `inker`                  | `str`              | `""`      | Inker(s)                                 |
| `colorist`               | `str`              | `""`      | Colorist(s)                              |
| `letterer`               | `str`              | `""`      | Letterer(s)                              |
| `cover_artist`           | `str`              | `""`      | Cover artist(s)                          |
| `editor`                 | `str`              | `""`      | Editor(s)                                |
| `translator`             | `str`              | `""`      | Translator(s)                            |
| `publisher`              | `str`              | `""`      | Publisher                                |
| `imprint`                | `str`              | `""`      | Publisher imprint                        |
| `genre`                  | `str`              | `""`      | Genre(s), comma-separated                |
| `tags`                   | `str`              | `""`      | Tags, comma-separated                    |
| `web`                    | `str`              | `""`      | Web URL                                  |
| `language_iso`           | `LanguageISO`      | `""`      | ISO language code (e.g., `"en"`, `"fr"`) |
| `format`                 | `Format`           | `UNKNOWN` | Publication format                       |
| `black_white`            | `YesNo`            | `UNKNOWN` | Black and white                          |
| `manga`                  | `Manga`            | `UNKNOWN` | Manga / reading direction                |
| `age_rating`             | `AgeRating`        | `UNKNOWN` | Content age rating                       |
| `community_rating`       | `Optional[Rating]` | `None`    | Community rating (0.0-5.0)               |
| `summary`                | `str`              | `""`      | Synopsis / description                   |
| `characters`             | `str`              | `""`      | Character names, comma-separated         |
| `teams`                  | `str`              | `""`      | Team names, comma-separated              |
| `locations`              | `str`              | `""`      | Locations, comma-separated               |
| `story_arc`              | `str`              | `""`      | Story arc name                           |
| `story_arc_number`       | `Optional[int]`    | `None`    | Position in story arc                    |
| `main_character_or_team` | `str`              | `""`      | Primary character or team                |
| `scan_information`       | `str`              | `""`      | Scan / digitization notes                |
| `ean`                    | `str`              | `""`      | EAN / ISBN                               |
| `book_price`             | `str`              | `""`      | Cover price                              |

### Enumerations

```python
from cbz import PageType, Format, YesNo, Manga, AgeRating

# Page types
PageType.FRONT_COVER  # Front cover
PageType.STORY  # Story page (default)
PageType.BACK_COVER  # Back cover
PageType.INNER_COVER  # Inner cover / dust jacket
PageType.ADVERTISEMENT  # Advertisement
PageType.EDITORIAL  # Editorial / credits
PageType.LETTERS  # Letters page
PageType.PREVIEW  # Preview of upcoming issues
PageType.ROUNDUP  # Recap / summary
PageType.OTHER  # Other
PageType.DELETED  # Marked for deletion

# Publication formats
Format.SERIES  # Regular series
Format.GRAPHIC_NOVEL  # Graphic novel
Format.WEB_COMIC  # Webcomic
Format.ONE_SHOT  # One-shot
Format.TRADE_PAPERBACK  # Trade paperback
Format.ANNUAL  # Annual
Format.ANTHOLOGY  # Anthology
Format.LIMITED_SERIES  # Limited series
Format.MAGAZINE  # Magazine
# ... and more

# Reading direction
Manga.UNKNOWN  # Not specified
Manga.NO  # Western (left to right)
Manga.YES  # Manga
Manga.YES_AND_RIGHT_TO_LEFT  # Manga (right to left)

# Age ratings
AgeRating.UNKNOWN  # Not rated
AgeRating.EVERYONE  # All ages
AgeRating.TEEN  # Teens
AgeRating.MATURE_17_PLUS  # Mature 17+
AgeRating.RATING_PENDING  # Rating pending
# ... and more
```

### Error Handling

The library provides a hierarchy of specific exceptions:

```python
from cbz import CBZError, InvalidImageError, EmptyArchiveError, InvalidMetadataError

try:
    comic = ComicInfo.from_cbz("corrupted.cbz")
except InvalidMetadataError:
    print("ComicInfo.xml is invalid or corrupted")
except EmptyArchiveError:
    print("No valid images found in the archive")
except InvalidImageError:
    print("An image in the archive could not be read")
except CBZError:
    print("General CBZ error")
```

## Format Specification

A complete RFC specification of the CBZ format is available in [`docs/RFC-CBZ.md`](docs/RFC-CBZ.md).

The ComicInfo.xml XSD schemas (v1.0, v2.0, v2.1) are in [`docs/schema/`](docs/schema/).

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for the full version history, including migration notes for v4.0.

## Contributors

<a href="https://github.com/hyugogirubato"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/65763543?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="hyugogirubato"/></a>
<a href="https://github.com/piskunqa"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/38443069?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="piskunqa"/></a>
<a href="https://github.com/OleskiiPyskun"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/75667382?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="OleskiiPyskun"/></a>
<a href="https://github.com/tssujt"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/17313425?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="tssujt"/></a>
<a href="https://github.com/gokender"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/3709740?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="gokender"/></a>
<a href="https://github.com/domenicoblanco"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/9018104?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="domenicoblanco"/></a>
<a href="https://github.com/RivMt"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/40086827?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="RivMt"/></a>
<a href="https://github.com/flolep2607"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/24566964?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="flolep2607"/></a>
<a href="https://github.com/chase-roohms"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/131704514?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="chase-roohms"/></a>

## Licensing

This software is licensed under the terms of [MIT License](LICENSE). You can find a copy of the license in the LICENSE file in the root folder.

### Third-Party Licenses

This project uses the following third-party libraries:

- **[langcodes](https://pypi.org/project/langcodes/)** - MIT License
- **[Pillow](https://pypi.org/project/Pillow/)** - HPND License
- **[pillow-avif-plugin](https://pypi.org/project/pillow-avif-plugin/)** - MIT License
- **[pillow-jxl-plugin](https://pypi.org/project/pillow-jxl-plugin/)** - MIT License
- **[pypdf](https://pypi.org/project/pypdf/)** - BSD License
- **[rarfile](https://pypi.org/project/rarfile/)** - ISC License
- **[xmltodict](https://pypi.org/project/xmltodict/)** - MIT License

---

© hyugogirubato

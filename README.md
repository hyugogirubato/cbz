# CBZ

[![License](https://img.shields.io/github/license/hyugogirubato/cbz)](https://github.com/hyugogirubato/cbz/blob/main/LICENSE)
[![Release](https://img.shields.io/github/release-date/hyugogirubato/cbz)](https://github.com/hyugogirubato/cbz/releases)
[![Latest Version](https://img.shields.io/pypi/v/cbz)](https://pypi.org/project/cbz/)

CBZ is a Python package designed to facilitate the creation, manipulation, and extraction of comic book archive files in the CBZ format. It allows users to programmatically generate CBZ files from a collection of images, add metadata to the archives, and unpack existing CBZ files. This library is ideal for comic book enthusiasts, archivists, and developers working on applications involving digital comic book distributions.

> [!WARNING]  
> The library is currently being rewritten following the latest PR, a new version will arrive soon, partially changing its use.

## Features

- **Create CBZ Files**: Pack a series of images into a CBZ file with ease.
- **Extract CBZ Files**: Unpack images and metadata from existing CBZ files.
- **Manage Metadata**: Add, update, and retrieve metadata from CBZ files, including titles, authors, volume numbers, and more.
- **Support for ComicInfo.xml**: Utilizes the ComicInfo.xml standard for embedding comic book metadata within CBZ files.
- **Flexible Image Handling**: Load images from various formats and ensure they are correctly formatted and ordered within the CBZ file.
- **High-Level API**: Offers a simple, high-level API for common tasks, while also providing access to lower-level functions for advanced usage.

## Installation

To install the CBZ library, you can use pip:

```bash
pip install cbz
```

## Quick Start

Here's a quick example of how to create a CBZ file from a series of images:

```python
from pathlib import Path
from cbz.page import PageInfo
from cbz.comic import ComicInfo
from cbz.constants import PageType, YesNo, Manga, AgeRating, Format

if __name__ == '__main__':
    # Define the path to your images
    images_path = Path('path/to/your/images')

    # Load images and create page objects
    pages = [PageInfo.load(path) for path in images_path.iterdir()]

    # Create a ComicInfo object with your comic's metadata
    comic = ComicInfo.from_pages(
        pages=pages,
        title='Your Comic Title',
        series='Your Comic Series',
        number='1',
        language_iso='en',
        format=Format.WEB_COMIC,
        black_white=YesNo.NO,
        manga=Manga.NO,
        age_rating=AgeRating.PENDING
    )

    # Pack the comic into a CBZ file
    cbz_content = comic.pack()

    # Save the CBZ file
    cbz_path = Path('your_comic.cbz')
    cbz_path.write_bytes(cbz_content)
```

## Documentation

For detailed documentation, including the full API reference and more examples, please refer to the [official CBZ Library documentation](https://en.wikipedia.org/wiki/Comic_book_archive).

## License

The CBZ Library is released under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

This library was developed with the needs of comic book fans and digital archivists in mind. We hope it helps you in managing and enjoying your comic book collections.

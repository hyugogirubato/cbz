# PyCBZHelper

[![License](https://img.shields.io/github/license/hyugogirubato/pycbzhelper)](https://github.com/hyugogirubato/pycbzhelper/blob/master/LICENSE)
[![Release](https://img.shields.io/github/release-date/hyugogirubato/pycbzhelper)](https://github.com/hyugogirubato/pycbzhelper/releases)
[![Latest Version](https://img.shields.io/pypi/v/pycbzhelper)](https://pypi.org/project/pycbzhelper/)

PyCBZHelper is a Python library for creating CBZ (Comic Book Zip) files with metadata. It provides functionality to
generate a CBZ file from a list of image pages and associated comic book metadata.

## Features

- Create CBZ files from images.
- Generate ComicInfo.xml metadata.
- Support for various metadata fields.
- Handle page files from local disk or web URLs.
- Automatic cleanup of temporary files.

## Installation

You can install PyCBZHelper using pip:

````shell
pip install pycbzhelper
````

## Usage

Here's a basic example of how to use PyCBZHelper:

````python
from pycbzhelper import Helper
from pathlib import Path

PARENT = Path(__name__).resolve().parent

if __name__ == "__main__":
    # Define metadata for the comic
    metadata = {
        "Title": "My Comic",
        "Series": "Comic Series",
        "Number": "1",
        "Pages": [
            {"File": PARENT / "image1.jpg"},
            {"File": PARENT / "image2.jpg"},
        ]
        # Add more metadata fields here
    }

    # Define the path to the output CBZ file
    output_path = PARENT / "output.cbz"

    # Create an instance of the Helper class
    helper = Helper(metadata)

    # Create the CBZ file
    helper.create_cbz(output_path)
````

For more information on how to use PyCBZHelper, please refer to
the [documentation](https://github.com/hyugogirubato/pycbzhelper/blob/master/docs/schema).

### License

This project is licensed under the [GPL v3 License](https://github.com/hyugogirubato/pycbzhelper/blob/master/LICENSE).

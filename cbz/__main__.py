import argparse

from pathlib import Path

from cbz.comic import ComicInfo


def main() -> None:
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Launch CBZ player with a comic book file')
    parser.add_argument('comic_path', type=Path, metavar='<file>', help='Path to the CBZ comic book file.')
    args = parser.parse_args()

    # Validate the provided path
    comic_path = args.comic_path
    if not comic_path.is_file():
        print(f'Error: The file "{comic_path}" does not exist or is not a valid file.')
        exit(1)

    # Create ComicInfo object from CBZ file
    try:
        comic_info = ComicInfo.from_pdf(comic_path) if comic_path.suffix == '.pdf' else ComicInfo.from_cbz(comic_path)
        # Launch the CBZ player
        comic_info.show()
    except Exception as e:
        print(f'Error: {e}')
        exit(1)


if __name__ == '__main__':
    main()

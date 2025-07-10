# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.4.1] - 2025-07-11

### Fixed

- Fix installation instructions.

## [3.4.0] - 2025-07-09

### Added

- Support for PDF files.
- Support for CBR (Comic Book RAR) files.

### Changed

- Replaced `PyMuPDF` with `pypdf` for PDF handling.
- Updated third-party license documentation for bundled libraries.

### New Contributors

- [tssujt](https://github.com/tssujt)

## [3.3.7] - 2025-01-04

### Fixed

- Import error on Unix systems for the comic player.

## [3.3.6] - 2024-12-22

### Added

- Option to not rename the name of image files loaded into pages.

### Fixed

- Removing deprecated datetime api for utcnow.

## [3.3.5] - 2024-07-22

### Fixed

- Fix `Path` import using `pathlib`.

## [3.3.4] - 2024-07-18

### Fixed

- Remove invalid dict key.
- Fix invalid utc format.

## [3.3.3] - 2024-07-18

### Added

- Reference links for XML schema.
- New information fields in the XML.
- Support PDF files via `cbzplayer` command.

### Changed

- Removed MD5 display in the player (irrelevant).
- The displayed size in the player now reflects the total size of all images.
- Simplified the closing XML `Page` tag.
- Sorted `Page` keys in order.
- Updated `ComicInfo.xsd` defining the CBZ standard.

### Fixed

- Fixed the `.jpg` constant preventing the use of certain images.
- Fixed memory error related to the `pack()` method cache.
- Fixed saving pages in XML to comply with the standard.
- Added missing mandatory keys in the XML.

## [3.3.2] - 2024-07-18

### Added

- Added zoom options for displaying images in the player.
- Added scroll functionality for image display in the player, especially useful when images are zoomed.

### Changed

- Set a default standard size.

### Fixed

- Fix lag when stretching player.
- Fix XML parsing for CBZ files with a single page.
- Fix image positioning within the player.

### New Contributors

- [gokender](https://github.com/gokender)

## [3.3.1] - 2024-07-15

### Added

- Added `from_pdf` method to convert `.pdf` files to `.cbz`.

### Changed

- Set a default standard size.
- Changed a keyboard shortcut that prevented copying information.

### Fixed

- Fixed the icon display for Linux in the player.
- Fixed the taskbar icon for Windows in the player.
- Fixed the player margins.
- Automatically detect the player size based on the smallest image.

### New Contributors

- [flolep2607](https://github.com/flolep2607)

## [3.3.0] - 2024-07-14

### Added

- Type value verification.
- Load ComicInfo from a `cbz` file.
- Built-in reader for dynamic viewing.
- Image compatibility checking.
- Added `save` method to directly save a page or comic.
- Display additional file information via the player.

### Changed

- Complete code refactoring.
- `pages` variable now public for native page manipulation in Python.
- Optimized `pack` function with caching.
- Library now supports loading `zip` files containing only images.

### Fixed

- Default value definitions.
- Corrected values written to XML.

### New Contributors

- [piskunqa](https://github.com/piskunqa)
- [OleskiiPyskun](https://github.com/OleskiiPyskun)
- [domenicoblanco](https://github.com/domenicoblanco)
- [RivMt](https://github.com/RivMt)

## [3.2.0] - 2024-03-17

### Changed

- New code structure.
- Deleting temporary files usage.
- Automatic correction of variable types.
- Simplifying constants.
- Binary input support for pages.
- Project `pycbzhelper` renamed to `cbz`.

## [3.1.2] - 2023-08-13

### Fixed

- Fixed missing `Tags` key, thanks to @RivMt

## [3.1.1] - 2023-06-04

### Changed

- Update `README.md`.

## [3.1.0] - 2023-06-04

### Added

- Installation with pip.
- Support for non-existent location.
- Support for web loading errors of pages.

### Fixed

- Fixed page support.

### Changed

- New name of some variables.
- Automatic cleanup of temporary files.
- New location for temporary files.
- File path now uses `pathlib`.

## [3.0.1] - 2023-02-06

### Added

- Initial release.

[3.4.1]: https://github.com/hyugogirubato/cbz/releases/tag/v3.4.1
[3.4.0]: https://github.com/hyugogirubato/cbz/releases/tag/v3.4.0
[3.3.7]: https://github.com/hyugogirubato/cbz/releases/tag/v3.3.7
[3.3.6]: https://github.com/hyugogirubato/cbz/releases/tag/v3.3.6
[3.3.5]: https://github.com/hyugogirubato/cbz/releases/tag/v3.3.5
[3.3.4]: https://github.com/hyugogirubato/cbz/releases/tag/v3.3.4
[3.3.3]: https://github.com/hyugogirubato/cbz/releases/tag/v3.3.3
[3.3.2]: https://github.com/hyugogirubato/cbz/releases/tag/v3.3.2
[3.3.1]: https://github.com/hyugogirubato/cbz/releases/tag/v3.3.1
[3.3.0]: https://github.com/hyugogirubato/cbz/releases/tag/v3.3.0
[3.2.0]: https://github.com/hyugogirubato/cbz/releases/tag/v3.2.0
[3.1.2]: https://github.com/hyugogirubato/cbz/releases/tag/v3.1.2
[3.1.1]: https://github.com/hyugogirubato/cbz/releases/tag/v3.1.1
[3.1.0]: https://github.com/hyugogirubato/cbz/releases/tag/v3.1.0
[3.0.1]: https://github.com/hyugogirubato/cbz/releases/tag/v3.0.1

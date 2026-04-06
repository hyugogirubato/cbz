"""CBZ library-specific exceptions."""


class CBZError(Exception):
    """Base class for all CBZ errors."""


class InvalidImageError(CBZError):
    """The provided image is invalid or in an unsupported format."""


class EmptyArchiveError(CBZError):
    """The archive contains no valid images."""


class InvalidMetadataError(CBZError):
    """The ComicInfo.xml metadata is invalid or corrupted."""


class UnsupportedFormatError(CBZError):
    """The file format is not supported."""

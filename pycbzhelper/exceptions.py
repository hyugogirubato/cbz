class PyCBZHelperException(Exception):
    """Exceptions used by PyCBZHelper."""


class InvalidKeyValue(PyCBZHelperException):
    """The key value is invalid."""


class MissingPageFile(PyCBZHelperException):
    """No page available."""


class InvalidFileExtension(PyCBZHelperException):
    """Invalid file extension."""


class FileNotFound(PyCBZHelperException):
    """The specified source file was not found."""

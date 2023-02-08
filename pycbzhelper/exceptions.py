class PyCBZHelperException(Exception):
    """Exceptions used by pycbzhelper."""


class InvalidKeyValue(PyCBZHelperException):
    """The key value is invalid."""


class MissingPageFile(PyCBZHelperException):
    """No page available."""


class InvalidFilePermission(PyCBZHelperException):
    """Unable to delete existing file."""


class FileNotFound(PyCBZHelperException):
    """The specified source file was not found."""

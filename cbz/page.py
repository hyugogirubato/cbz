"""
Comic page management module.

Provides the PageInfo class to load, manipulate and save
individual comic pages (images).
"""

from __future__ import annotations

import base64
from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path
from typing import Union

from PIL import Image

from cbz.constants import IMAGE_FORMATS
from cbz.exceptions import InvalidImageError
from cbz.models import PageModel


@dataclass
class PageInfo(PageModel):
    """Represents a comic page with its image content.

    Inherits from PageModel for XML metadata and adds binary image
    content management. Image metadata (dimensions, size, format)
    is automatically extracted when content is assigned.

    Attributes:
        _content: Binary image data (accessed via the content property).
    """

    _content: bytes = field(default=b"", repr=False, compare=False)

    @property
    def content(self) -> bytes:
        """Binary image data."""
        return self._content

    @content.setter
    def content(self, value: bytes) -> None:
        """Set content and automatically extract image metadata."""
        try:
            with Image.open(BytesIO(value)) as img:
                self.suffix = f".{img.format.lower()}"
                if self.suffix not in IMAGE_FORMATS:
                    raise InvalidImageError(f"Unsupported image format: {self.suffix}")
                self.image_width = img.width
                self.image_height = img.height
        except InvalidImageError:
            raise
        except Exception as e:
            raise InvalidImageError(f"Unable to read image: {e}") from e
        self.image_size = len(value)
        self._content = value

    def __post_init__(self) -> None:
        """Validate content if provided at initialization."""
        if self._content:
            self.content = self._content

    @classmethod
    def loads(cls, data: Union[str, bytes], **kwargs) -> PageInfo:
        """Create a PageInfo from raw bytes or base64-encoded data.

        Args:
            data: Binary image data or base64-encoded string.
            **kwargs: Additional attributes (type, bookmark, etc.).

        Returns:
            PageInfo instance with loaded content.

        Raises:
            InvalidImageError: If the data is empty or invalid.
            ValueError: If the data type is not str or bytes.
        """
        if isinstance(data, str):
            data = base64.b64decode(data)
        if not isinstance(data, bytes):
            raise ValueError(f"Expected bytes or base64 str, got {type(data).__name__}")
        if not data or data.isspace():
            raise InvalidImageError("Empty or null image data")

        page = cls(**kwargs)
        page.content = data
        return page

    @classmethod
    def load(cls, path: Union[Path, str], **kwargs) -> PageInfo:
        """Create a PageInfo from an image file.

        Args:
            path: Path to the image file.
            **kwargs: Additional attributes (type, bookmark, etc.).

        Returns:
            PageInfo instance with file content loaded.

        Raises:
            FileNotFoundError: If the file does not exist.
            InvalidImageError: If the image is invalid.
        """
        path = Path(path)
        kwargs.setdefault("name", path.name)
        return cls.loads(path.read_bytes(), **kwargs)

    def show(self) -> None:
        """Display the page in the default image viewer."""
        with Image.open(BytesIO(self.content)) as img:
            img.show()

    def save(self, path: Union[Path, str]) -> None:
        """Save the page to a file.

        Args:
            path: Destination file path.
        """
        Path(path).write_bytes(self.content)

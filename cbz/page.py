from __future__ import annotations

import base64
import json
from io import BytesIO
from pathlib import Path
from typing import Union

from PIL import Image

from cbz import utils
from cbz.models import PageModel


class PageInfo(PageModel):

    def __init__(self, content: bytes, **kwargs):
        super(PageInfo, self).__init__(kwargs)
        self.content = content

    @property
    def content(self) -> bytes:
        """
        content getter
        :return:
        """
        return self._content

    @content.setter
    def content(self, value) -> None:
        """
        Set image info by current content
        :param value:
        :return:
        """
        with Image.open(BytesIO(value)) as image:
            self.suffix = f'.{image.format.lower()}'
            self._image_width = int(image.width)
            self._image_height = int(image.height)
        self._image_size = len(value)
        self._content = value

    def dumps(self) -> dict:
        return utils.dumps(self._get())

    def __repr__(self) -> str:
        return json.dumps(self.dumps(), indent=2)

    @classmethod
    def loads(cls, data: Union[str, bytes], **kwargs) -> PageInfo:
        if isinstance(data, str):
            data = base64.b64decode(data)
        if not isinstance(data, bytes):
            raise ValueError(f'Expecting Bytes or Base64 input, got {data!r}')
        return cls(data, **kwargs)

    @classmethod
    def load(cls, path: Union[Path, str], **kwargs) -> PageInfo:
        if not isinstance(path, (Path, str)):
            raise ValueError(f'Expecting Path object or path string, got {path!r}')
        with Path(path).open(mode='rb') as f:
            return cls(f.read(), **kwargs)

    def show(self) -> None:
        """
        display this page
        :return:
        """
        with Image.open(BytesIO(self.content)) as image:
            image.show()

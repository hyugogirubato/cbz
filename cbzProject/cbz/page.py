from __future__ import annotations

import base64
import json
from io import BytesIO
from typing import Union

from pathlib import Path

from PIL import Image

from cbz import utils
from cbz.constants import PageType


class PageInfo:

    def __init__(self, content: bytes, **kwargs):
        image = Image.open(BytesIO(content))

        self.suffix = f'.{image.format.lower()}'
        self.content = content
        self.__info = {
            # 'Image': 0,
            'Type': PageType(kwargs.get('type', PageType.STORY)),
            'DoublePage': bool(kwargs.get('double', False)),
            'ImageSize': len(content),
            'Key': str(kwargs.get('key', '')),
            'Bookmark': str(kwargs.get('bookmark', '')),
            'ImageWidth': int(image.width),
            'ImageHeight': int(image.height)
        }

    def dumps(self) -> dict:
        return utils.dumps(self.__info)

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

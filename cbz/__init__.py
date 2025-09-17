from .comic import ComicInfo
from .page import PageInfo

# Register optional Pillow plugins
for _plugin in ('pillow_avif', 'pillow_jxl'):
    try:
        __import__(_plugin)
    except ImportError:
        pass

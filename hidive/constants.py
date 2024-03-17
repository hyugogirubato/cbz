from enum import Enum


class Filter(Enum):
    SERIES = 'VOD_SERIES'
    VIDEO = 'VOD_VIDEO'
    EVENT = 'LIVE_EVENT'
    PLAYLIST = 'VOD_PLAYLIST'


class Format(Enum):
    VTT = 'vtt'
    SRT = 'srt'
    SCC = 'scc'


class View(Enum):
    SEASON = 'season'
    PLAYLIST = 'playlist'
    VOD = 'VOD'

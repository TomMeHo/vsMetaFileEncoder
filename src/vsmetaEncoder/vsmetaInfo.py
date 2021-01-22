from datetime import date
from vsmetaEncoder.vsmetaListInfo import VsMetaListInfo
from vsmetaEncoder.vsmetaImageInfo import VsMetaImageInfo

class VsMetaInfo():
    def __init__(self):
        self.showTitle = ""
        self.showTitle2 = ""
        self.episodeTitle = ""
        self.year = 0
        self.episodeReleaseDate = date(1900, 1, 1)
        self.tvshowReleaseDate = date(1900, 1, 1)
        self.tvshowYear = 0,
        self.tvshowSummary = "",
        self.chapterSummary = "",
        self.classification = 0,
        self.season = 0,
        self.episode  = 0,
        self.rating = -1.0,
        self.list = VsMetaListInfo(),
        self.images = VsMetaImageInfo(),
        self.episodeMetaJson = ""
        self.tvshowMetaJson = ""
        self.timestamp = date(1900, 1, 1)
        self.episodeLocked = False
        self.tvshowLocked = False

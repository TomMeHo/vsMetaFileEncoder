from datetime import date, datetime
from vsmetaEncoder.vsmetaListInfo import VsMetaListInfo
from vsmetaEncoder.vsmetaImageInfo import VsMetaImageInfo

class VsMetaInfo():
    def __init__(self):

        self.showTitle = ""
        self.showTitle2 = ""
        self.episodeTitle = ""

        self.year = 0
        self.episodeReleaseDate = date(1900, 1, 1)

        self.tvshowYear = 0
        self.tvshowReleaseDate = date(1900, 1, 1)

        self.tvshowSummary = ""
        self.chapterSummary = ""
        self.classification = 0
        self.season = 0
        self.episode  = 0
        self.rating = -1.0
        self.list = VsMetaListInfo()
        self.images = VsMetaImageInfo()
        self.episodeMetaJson = ""
        self.tvshowMetaJson = ""
        self.timestamp = date(1900, 1, 1)
        self.episodeLocked = True
        self.tvshowLocked = True

    def setEpisodeDate(self, episodeDate: date):
        self.episodeReleaseDate = episodeDate
        self.year = episodeDate.year

    def setShowDate(self, showDate: date):
        self.tvshowReleaseDate = showDate
        self.tvshowYear = showDate.year
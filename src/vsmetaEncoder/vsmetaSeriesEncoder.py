from datetime import datetime, date
from vsmetaEncoder.vsmetaBase import VsMetaBase

class VsMetaSeriesEncoder(VsMetaBase):

    def __init__(self):
        super(VsMetaSeriesEncoder, self).__init__()
        self.rewriteEpisodeInfo = False

    def _writeEncodedContent(self):
        super(VsMetaSeriesEncoder, self)._writeEncodedContent()

        self._writeFileHeader()
        self._writeShowTitle()
        self._writeEpisodeTitle()
        self._writeEpisodeDate()
        self._writeEpisodeLocked()
        self._writeSummary()
        self._writeEpisodeMetaJSON()
        self._writeClassification()
        self._writeRating()
        self._writePoster()
        self._writeGroup2()

    def _writeFileHeader(self):
        self._writeTag(self.TAG_FILE_HEADER_SERIES)

    def _writeGroup2(self):

        if self.rewriteEpisodeInfo:

            isoDate = self.info.episodeReleaseDate.isocalendar()
            year    = isoDate[0]
            weeknum = isoDate[1]
            weekday = isoDate[2]

            # prepare VsMeta
            if self.info.season == 0:
                self.info.season = year if year > 0 else 999

            if self.info.episode == 0:
                episode = 0
                if self.info.episodeReleaseDate > date(1900, 1, 1):
                    episode =  weeknum * 10 + weekday
                self.info.episode = episode

        super(VsMetaSeriesEncoder, self)._writeGroup2()

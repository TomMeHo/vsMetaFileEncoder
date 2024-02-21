from datetime import date
from vsmetaCodec.vsmetaBase import VsMetaBase
from vsmetaCodec.vsmetaCode import VsMetaCode


class VsMetaMovieEncoder(VsMetaBase):

    def _writeFileHeader(self):     # overload of vsmetaBase method
        self.encContent.writeTag(self.TAG_FILE_HEADER_MOVIE)

    def _writeGroup2(self, rewrite_episode_info: bool = False):
        return  # Void implementation, to avoid writing Group2 content for a movie


class VsMetaSeriesEncoder(VsMetaBase):
    def __init__(self):
        super(VsMetaSeriesEncoder, self).__init__()
        self.rewriteEpisodeInfo = False

    def _writeFileHeader(self):     # overload of vsmetaBase method
        self.encContent.writeTag(self.TAG_FILE_HEADER_SERIES)

    def _writeGroup2(self):
        self.rewriteSeasonEpisode()
        super(VsMetaSeriesEncoder, self)._writeGroup2()

    def _writeGroup3(self) -> VsMetaCode:
        # vsmeta for series encode the group3 data already at the end of group2, therefore to be skipped here!!
        # group2 is calling VsMetaBase._writeGroup3() for this purpose directly within VsMetaBase._writeGroup2().
        return VsMetaCode()     # hence return an empty piece of vsmeta code

    def rewriteSeasonEpisode(self):
        if self.rewriteEpisodeInfo:
            iso_date = self.info.episodeReleaseDate.isocalendar()
            year = iso_date[0]
            weeknum = iso_date[1]
            weekday = iso_date[2]

            # prepare VsMeta
            if self.info.season == 0:
                self.info.season = year if year > 0 else 999

            if self.info.episode == 0:
                if self.info.episodeReleaseDate > date(1900, 1, 1):
                    self.info.episode = weeknum * 10 + weekday

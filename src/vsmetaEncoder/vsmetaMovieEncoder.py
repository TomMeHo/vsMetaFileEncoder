from vsmetaEncoder.vsmetaBase import VsMetaBase

class VsMetaMovieEncoder(VsMetaBase):

    def __init__(self):
        super(VsMetaMovieEncoder, self).__init__()

    def _writeEncodedContent(self):
        super(VsMetaMovieEncoder, self)._writeEncodedContent()

        self._writeFileHeader()
        self._writeTitle()
        self._writeShortTitle()
        self._writeEpisodeDate()
        self._writeEpisodeLocked(True)
        self._writeSummary()
        self._writeEpisodeMetaJSON()
        self._writeClassification()
        self._writeRating()

    def _writeFileHeader(self):
        self._writeTag(self.TAG_FILE_HEADER_MOVIE)

    def _writeEpisodeMetaJSON(self):
        self._writeTag(self.TAG_EPISODE_META_JSON, 'null') # null as string

    def _writeTitle(self):
        self._writeTag( self.TAG_SHOW_TITLE, self.info.episodeTitle)
        self._writeTag( self.TAG_SHOW_TITLE2, self.info.episodeTitle)

    def _writeShortTitle(self):
        self._writeTag( self.TAG_EPISODE_TITLE, self.info.showTitle)
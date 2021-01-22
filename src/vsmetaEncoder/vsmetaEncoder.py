import sys
from datetime import datetime, date
from vsmetaEncoder.vsmetaBase import VsMetaBase
from vsmetaEncoder.vsmetaInfo import VsMetaInfo

class VsMetaEncoder(VsMetaBase):

    def encode(self, info : VsMetaInfo = None) -> bytes:

        self.info = info
        self._writeEncodedContent()
        return self.encodedContent

    def _writeEncodedContent(self):

        self.encodedContent = bytes()  # ensure empty.
        info = self.info

        if(info.year == 0): 
            if(info.episodeReleaseDate.year != 1900): 
                info.year = info.episodeReleaseDate.year
                info.year += 2048
            else:
                info.year = 0


        self._writeTag( self.TAG_FILE_HEADER )
        self._writeTag( self.TAG_SHOW_TITLE, info.showTitle2 or info.showTitle)
        self._writeTag( self.TAG_SHOW_TITLE2, info.showTitle2 or info.showTitle)
        self._writeTag( self.TAG_EPISODE_TITLE, info.episodeTitle)
        self._writeTag( self.TAG_YEAR, info.year, intBytes= 1 if info.year == 0 else 2)
        if info.episodeReleaseDate != date(1900, 1, 1): self._writeTag( self.TAG_EPISODE_RELEASE_DATE, info.episodeReleaseDate)
        if info.episodeLocked: self._writeTag( self.TAG_EPISODE_LOCKED, True)
        if len(info.chapterSummary) > 1: self._writeTag( self.TAG_CHAPTER_SUMMARY, info.chapterSummary)
        if len(info.episodeMetaJson) > 0: self._writeTag( self.TAG_EPISODE_META_JSON, info.episodeMetaJson)
        self._writeTag( self.TAG_CLASSIFICATION, 0)
        self._writeTag( self.TAG_RATING, b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01')
        self._writeGroup2(info)

    def _writeGroup1(self, info: VsMetaInfo):
        self._writeTag( self.TAG_GROUP1)
        # TODO TAG1_CAST, GENRE, DIRECTOR, WRITER

    def _writeGroup2(self, info: VsMetaInfo):

        #tv show year
        tvshowYear = 0
        if(info.tvshowReleaseDate.year != 1900): 
            tvshowYear = info.tvshowReleaseDate.year
            tvshowYear += 2048


        self._writeTag( self.TAG_GROUP2)
        self._writeTag( b'\x01') # group 2 - occurence no. 1?        
        #group 2 payload
        group2Content  = bytes()
        group2Content += self.TAG2_SEASON + self._writeInt(info.season)
        group2Content += self.TAG2_EPISODE + self._writeInt(info.episode)
        if info.tvshowReleaseDate != date(1900, 1, 1): 
            group2Content += self.TAG2_TV_SHOW_YEAR + self._writeInt(tvshowYear, 2, True)
            group2Content += self.TAG2_RELEASE_DATE_TV_SHOW
            group2Content += self._writeDate(info.tvshowReleaseDate)
        else:
            group2Content += self.TAG2_TV_SHOW_YEAR + self._writeInt(0, 2, True)
        if info.tvshowLocked: group2Content += self.TAG2_LOCKED + self._writeBool(True)
        if len(info.tvshowMetaJson) > 0:
            group2Content += self.TAG2_TVSHOW_META_JSON
            group2Content += self._writeStr(info.tvshowMetaJson)

        group2Content = len(group2Content).to_bytes(1, 'big') + group2Content # length of group 2 payload

        self.encodedContent += group2Content

        # TODO tvshowsummary, 
        # TODO tvshowposter, md5, tv_show_metajson
        self._writeGroup3


    def _writeGroup3(self, info: VsMetaInfo):
        pass
        # TODO tvshowBackdrop, MD5, timestamp
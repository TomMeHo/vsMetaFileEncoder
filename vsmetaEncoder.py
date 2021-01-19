import sys
from datetime import datetime, date

class vsMetaListInfo():
    def __init__(self):
        self.cast = {''}
        self.genre = []
        self.director = []
        self.writer = []

class vsImageInfo():
    def __init__(self):
        self.tvshowPoster = None # BiteArray
        self.episodeImage =  None # BiteArray
        self.tvshowBackdrop = None # BiteArray

class vsMetaInfo():
    def __init__(self):
        self.showTitle = ""
        self.showTitle2 = ""
        self.episodeTitle = ""
        self.year = 1900
        self.episodeReleaseDate = date(1900, 1, 1)
        self.tvshowReleaseDate = date(1900, 1, 1)
        self.tvshowYear = 0,
        self.tvshowSummary = "",
        self.chapterSummary = "",
        self.classification = 0,
        self.season = 0,
        self.episode  = 0,
        self.rating = -1.0,
        self.list = vsMetaListInfo(),
        self.images = vsImageInfo(),
        self.tagEpisodeMetaJson = ""
        self.tagTvshowMetaJson = ""
        self.timestamp = date(1900, 1, 1)
        self.episodeLocked = False
        self.tvshowLocked = False

class vsMetaBase():

    TAG_FILE_HEADER = b'\x08\x02'

    TAG_SHOW_TITLE = b'\x12'
    TAG_SHOW_TITLE2 = b'\x1A'
    TAG_EPISODE_TITLE = b'\x22'
    TAG_YEAR = b'\x28'
    TAG_EPISODE_RELEASE_DATE = b'\x32'
    TAG_EPISODE_LOCKED = b'\x38'
    TAG_CHAPTER_SUMMARY = b'\x42'
    TAG_EPISODE_META_JSON = b'\x4A'
    TAG_GROUP1 = b'\x52'
    TAG_CLASSIFICATION = b'\x5A'
    TAG_RATING = b'\x60'

    TAG_EPISODE_THUMB_DATA = b'\x8a'
    TAG_EPISODE_THUMB_MD5 = b'\x92'

    TAG_GROUP2 = b'\x9a'

    TAG1_CAST = b'\x0A'
    TAG1_DIRECTOR = b'\x12'
    TAG1_GENRE = b'\x1A'
    TAG1_WRITER = b'\x22'

    TAG2_SEASON = b'\x08'
    TAG2_EPISODE = b'\x10'
    TAG2_TV_SHOW_YEAR = b'\x18'
    TAG2_RELEASE_DATE_TV_SHOW = b'\x22'
    TAG2_LOCKED = b'\x28'
    TAG2_TVSHOW_SUMMARY = b'\x32'
    TAG2_POSTER_DATA = b'\x3A'
    TAG2_POSTER_MD5 = b'\x42'
    TAG2_TVSHOW_META_JSON = b'\x4A'
    TAG2_GROUP3 = b'\x52'

    TAG3_BACKDROP_DATA = b'\x0a'
    TAG3_BACKDROP_MD5 = b'\x12'
    TAG3_TIMESTAMP = b'\x18'

    def __init__(self):

        self.encodedContent : bytes
        self.info = vsMetaInfo()

    def _writeTag(self, tag : bytes, value = None, intBytes : int = 1, signed : bool = True):

        #write tag
        self.encodedContent += self._writeBinary(tag)
        if value is None: return

        #write content
        if (type(value) == str):  self.encodedContent += self._writeStr(value)
        if (type(value) == int):  self.encodedContent += self._writeInt(value, intBytes, signed)
        if (type(value) == date): self.encodedContent += self._writeDate(value)
        if (type(value) == bool): self.encodedContent += self._writeBool(value)
        if (type(value) == bytes): self.encodedContent += self._writeBinary(value)

    def _writeBinary(self, byteValue : bytes) -> bytes:

        returnValue = bytes()
        returnValue += byteValue
        return returnValue

    def _writeBool(self, boolValue : bool) -> bytes:

        returnValue = bytes()
        returnValue += b'\x01' if boolValue == True else b'\x00'
        return returnValue

    def _writeStr(self, text : str, withBOM : bool = False) -> bytes:

        encoding = 'utf-8-sig' if withBOM else 'utf-8'
        #byteOrderMark \xEF\xBB\xBF is written automatically when using utf-8-sig.
        textAsByte  = bytes( text, encoding )

        returnValue = bytes()
        returnValue += len(textAsByte).to_bytes(1, 'big')
        returnValue += textAsByte
        return returnValue

    def _writeInt(self, numberValue : int = 0, bytesToUse : int = 1, signed : bool = True) -> bytes:

        returnValue = bytes()
        returnValue += numberValue.to_bytes(bytesToUse, byteorder="little", signed=signed)
        return returnValue

    def _writeDate(self, dateValue : date) -> bytes:

        returnValue = bytes()
        returnValue += b'\x0a' # length of date field, x0a = 10
        returnValue += bytes(dateValue.strftime("%Y-%m-%d"), 'utf-8' )
        return returnValue


class vsMetaEncoder(vsMetaBase):

    def encode(self, info : vsMetaInfo = None) -> bytes:

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
                info.year += 2048

        self._writeTag( self.TAG_FILE_HEADER )
        self._writeTag( self.TAG_SHOW_TITLE, info.showTitle2 or info.showTitle)
        self._writeTag( self.TAG_SHOW_TITLE2, info.showTitle2 or info.showTitle)
        self._writeTag( self.TAG_EPISODE_TITLE, info.episodeTitle)
        self._writeTag( self.TAG_YEAR) #### TODO increase byte length as necessary
        self._writeTag(b'\x00')
        #TODO if info.episodeReleaseDate != date(1900, 1, 1): self.__writeTag( vsMetaWriter.TAG_EPISODE_RELEASE_DATE, info.episodeReleaseDate)
        self._writeTag( self.TAG_CLASSIFICATION, 0)
        if info.episodeLocked == True: self._writeTag( self.TAG_EPISODE_LOCKED, info.episodeLocked)
        if len(info.chapterSummary) > 1: self._writeTag( self.TAG_CHAPTER_SUMMARY, info.chapterSummary)
        self._writeTag( self.TAG_RATING, b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01')
        self._writeGroup2(info)

    def _writeGroup1(self, info: vsMetaInfo):
        self._writeTag( self.TAG_GROUP1)
        # TODO TAG1_CAST, GENRE, DIRECTOR, WRITER

    def _writeGroup2(self, info: vsMetaInfo):
        self._writeTag( self.TAG_GROUP2)
        self._writeTag( b'\x01') # group 2 - occurence no. 1?
        
        #group 2 payload
        group2Content  = bytes()
        group2Content += b'\x08'
        group2Content += b'\xff\xff\xff\xff\xff\xff\xff\xff\xff' # ... ignoring some details, but let's start with a waling skeleton
        group2Content += b'\x01\x10'
        group2Content += b'\xff\xff\xff\xff\xff\xff\xff\xff\xff'
        group2Content += b'\x01'
        group2Content += b'\x18\x00'

        group2Content = len(group2Content).to_bytes(1, 'big') + group2Content # length of group 2 payload

        self.encodedContent += group2Content

        # TODO season, episode, tv_show_year, release_date_tv_show, tvshowlocked, tvshowsummary, 
        # TODO tvshowposter, md5, tv_show_metajson
        self._writeGroup3


    def _writeGroup3(self, info: vsMetaInfo):
        pass
        # TODO tvshowBackdrop, MD5, timestamp
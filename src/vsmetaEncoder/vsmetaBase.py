from datetime import date
from vsmetaEncoder.vsmetaInfo import VsMetaInfo
from vsmetaEncoder.vsmetaListInfo import VsMetaListInfo
from vsmetaEncoder.vsmetaImageInfo import VsMetaImageInfo

class VsMetaBase():

    TAG_FILE_HEADER_MOVIE = b'\x08\x01'
    TAG_FILE_HEADER_SERIES = b'\x08\x02'
    TAG_FILE_HEADER_OTHER = b'\x08\x03'

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

        self.encodedContent = bytes()
        self.info = VsMetaInfo()

    def encode(self, info : VsMetaInfo = None) -> bytes:

        self.info = info
        self._writeEncodedContent()
        return self.encodedContent

    # ------------------------------------
    # Write at meta file level - using methods at lower level to "really" write at file level
    # ------------------------------------
    def _writeFileHeader(self):
        self._writeTag( self.TAG_FILE_HEADER_OTHER )
        
    def _writePoster(self):
        self._writeTag(b'\x01')
        
        if self.info.images.episodeImage:
            self.encodedContent += self.TAG_EPISODE_THUMB_DATA + b'\x01' + self._writeImage(self.info.images.episodeImage)
            self.encodedContent += self.TAG_EPISODE_THUMB_MD5 + b'\x01' + self._writeMD5(self.info.images.episodeImage)
           
    def _writeShowTitle(self):
        self._writeTag( self.TAG_SHOW_TITLE, self.info.showTitle2 or self.info.showTitle)
        self._writeTag( self.TAG_SHOW_TITLE2, self.info.showTitle2 or self.info.showTitle)

    def _writeEpisodeTitle(self):
        self._writeTag( self.TAG_EPISODE_TITLE, self.info.episodeTitle)

    def _writeEpisodeDate(self):
        if self.info.year != 0: 
            self._writeTag( self.TAG_YEAR, self.info.year, intBytes= 1 if self.info.year == 0 else 2)

            if self.info.year != 0: self._writeTag( self.TAG_EPISODE_RELEASE_DATE, self.info.episodeReleaseDate)

    def _writeEpisodeLocked(self, locked:bool=True):
        self._writeTag( self.TAG_EPISODE_LOCKED, locked)

    def _writeClassification(self):
        self._writeTag( self.TAG_CLASSIFICATION, 0)

    def _writeRating(self):
        self._writeTag( self.TAG_RATING, b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF')

    def _writeSummary(self):
        if len(self.info.chapterSummary) > 0:
            self._writeTag(self.TAG_CHAPTER_SUMMARY, self.info.chapterSummary)

    def _writeEncodedContent(self):
        # intialization only, implementation in child classes
        self.encodedContent = bytes()  # ensure empty.

    def _writeEpisodeMetaJSON(self):
        if len(self.info.episodeMetaJson) > 0:
            self._writeTag( self.TAG_EPISODE_META_JSON, self.info.episodeMetaJson)

    def _writeGroup1(self):
        self._writeTag( self.info.TAG_GROUP1)
        # TODO TAG1_CAST, GENRE, DIRECTOR, WRITER

    def _writeGroup2(self):

        #tv show year
        tvshowYear = 0
        if(self.info.tvshowReleaseDate.year != 1900): 
            tvshowYear = self.info.tvshowReleaseDate.year
            tvshowYear += 2048
  
        #group 2 payload
        group2Content  = bytes()
        group2Content += self.TAG2_SEASON + self._writeSpecialInt(self.info.season)
        group2Content += self.TAG2_EPISODE + self._writeSpecialInt(self.info.episode)
        if self.info.tvshowReleaseDate != date(1900, 1, 1): 
            group2Content += self.TAG2_TV_SHOW_YEAR + self._writeInt(tvshowYear, 2, True)
            group2Content += self.TAG2_RELEASE_DATE_TV_SHOW
            group2Content += self._writeDate(self.info.tvshowReleaseDate)
        else:
            group2Content += self.TAG2_TV_SHOW_YEAR + self._writeInt(0, 1, True)
        if self.info.tvshowLocked: group2Content += self.TAG2_LOCKED + self._writeBool(True)

        if len(self.info.tvshowSummary) > 0:
            group2Content += self.TAG2_TVSHOW_SUMMARY + self._writeStr(self.info.tvshowSummary)
        
        if self.info.images.tvshowPoster:
            group2Content += self.TAG2_POSTER_DATA + self._writeImage(self.info.images.tvshowPoster)
            group2Content += self.TAG2_POSTER_MD5 + self._writeMD5(self.info.images.tvshowPoster)
        
        if len(self.info.tvshowMetaJson) > 0:
            group2Content += self.TAG2_TVSHOW_META_JSON
            group2Content += self._writeStr(self.info.tvshowMetaJson)
                      
        self._writeTag(self.TAG_GROUP2)
        self._writeTag(b'\x01') # group 2 - occurence no. 1?      
        self.encodedContent += self._writeSpecialInt(len(group2Content))
        self.encodedContent += group2Content

        # TODO tv_show_metajson
        self._writeGroup3

    def _writeGroup3(self, info: VsMetaInfo):
        pass
        # TODO tvshowBackdrop, MD5, timestamp

    # ------------------------------------
    # Write at file level
    # ------------------------------------

    def _writeTag(self, tag : bytes, value = None, intBytes : int = 0, signed : bool = True):

        #write tag
        self.encodedContent += self._writeBinary(tag)
        if value is None: return

        #write content
        if (type(value) == str):  self.encodedContent += self._writeStr(value)
        if (type(value) == int):  self.encodedContent += self._writeSpecialInt(value)
        if (type(value) == date): self.encodedContent += self._writeDate(value)
        if (type(value) == bool): self.encodedContent += self._writeBool(value)
        if (type(value) == bytes): self.encodedContent += self._writeBinary(value)

    def _writeImage(self, image) -> bytes:
        import base64
        converted_string = base64.b64encode(image)            
        out_string = ''
        count = 0
        for char in converted_string.decode():
            if count == 76:
                count = 0
                out_string += '\n'
            out_string += char
            count += 1
        
        returnValue = self._writeStr(text=out_string)
        return returnValue

    def _writeMD5(self, image) -> bytes:
        import hashlib
        returnValue = self._writeStr(text=hashlib.md5(image).hexdigest())
        return returnValue
    
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
        lengthTByte = len(textAsByte)
        returnValue += self._writeSpecialInt(lengthTByte)
        returnValue += textAsByte
        return returnValue

    def _writeInt(self, numberValue : int = 0, bytesToUse : int = 0, signed : bool = True) -> bytes:

        returnValue = bytes()

        # ok, the following looks very pragmatic...
        if bytesToUse == 0:
            bytesToUse = 1
            if numberValue >= (2**(1*8)): bytesToUse = 2
            if numberValue >= (2**16): bytesToUse = 3
            if numberValue >= (2**24): bytesToUse = 4

        returnValue += numberValue.to_bytes(bytesToUse, byteorder="little", signed=signed)
        return returnValue

    def _writeDate(self, dateValue : date) -> bytes:

        returnValue = bytes()
        returnValue += b'\x0a' # length of date field, x0a = 10
        returnValue += bytes(dateValue.strftime("%Y-%m-%d"), 'utf-8' )
        return returnValue

    def _writeSpecialInt(self, valueI:int) -> bytes:

        returnValue = b''
        num = valueI
        hasMore = True

        while hasMore:
            
            value1 = (num & 0b01111111)
            num = num >> 7
            hasMore = False if num == 0 else True
            value2 = 0x80 if hasMore else 0x00

            returnValue += (value1 | value2).to_bytes(1, 'little')

        return returnValue

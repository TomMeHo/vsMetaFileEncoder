from datetime import date
from vsmetaEncoder.vsmetaInfo import VsMetaInfo

class VsMetaBase():

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
        self.info = VsMetaInfo()

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

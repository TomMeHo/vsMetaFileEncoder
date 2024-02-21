import base64
from datetime import datetime, date
from vsmetaCodec.vsmetaInfo import VsMetaInfo
from vsmetaCodec.vsmetaCode import VsMetaCode


class VsMetaBase:

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

    TAG1_CAST = b'\x0A'
    TAG1_DIRECTOR = b'\x12'
    TAG1_GENRE = b'\x1A'
    TAG1_WRITER = b'\x22'

    TAG_GROUP2 = b'\x9a'
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

    TAG_GROUP3 = b'\xaa'
    TAG3_BACKDROP_DATA = b'\x0a'
    TAG3_BACKDROP_MD5 = b'\x12'
    TAG3_TIMESTAMP = b'\x18'

    def __init__(self):
        self.encContent = VsMetaCode()
        self.info = VsMetaInfo()

    def encode(self, info: VsMetaInfo = None) -> bytes:
        self.info = info
        self._writeEncodedContent()
        return self.encContent.data()

    def _writeEncodedContent(self):
        # implementation in child classes may substitute this general implementation
        self.encContent = VsMetaCode()      # ensure empty vsmeta-code

        self._writeFileHeader()
        self._writeShowTitle()
        self._writeEpisodeTitle()
        self._writeEpisodeDate()
        self._writeEpisodeLocked()
        self._writeSummary()
        self._writeEpisodeMetaJSON()

        self._writeGroup1()

        self._writeClassification()
        self._writeRating()
        self._writePoster()

        self._writeGroup2()  # the only add-on for series compared to movies

        grp3_content = self._writeGroup3()
        if len(grp3_content) > 0:
            self.encContent.writeTag(self.TAG_GROUP3)
            self.encContent.writeTag(b'\x01', grp3_content)

        return

    def writeVsMetaFile(self, file_path: str):
        self.encContent.writeToFile(file_path)

    def readVsMetaFile(self, file_path: str):
        self.encContent.readFromFile(file_path)

    @staticmethod
    def year_of_date(release_date: str | date) -> int:
        year = 0
        if type(release_date) is str:
            year = date.fromisoformat(release_date).year
        elif type(release_date) is date:
            year = release_date.year
        return year if year != 1900 else 0

    @staticmethod
    def b64encodeImage(image: bytes, last_char_nl: bool = False) -> str:
        converted_string = base64.b64encode(image).decode()
        b64_enc_str = ''
        length = len(converted_string)
        block_size = 76
        for pos in range(0, length - 1, block_size):  # insert '\n' every 76 characters
            if (length - pos) < block_size:
                block_size = length - pos
            b64_enc_str += converted_string[pos:pos + block_size]
            if block_size == length - pos:  # last block ?
                b64_enc_str += '\n' if last_char_nl else ''
            else:
                b64_enc_str += '\n'  # not the last block -> append '\n'
        return b64_enc_str

    # -------------------------------------------------------
    # Write here on meta level, stored low level with instance of VsMetaCode()
    # -------------------------------------------------------
    def _writeFileHeader(self):
        self.encContent.writeTag(self.TAG_FILE_HEADER_OTHER)

    def _writeShowTitle(self):
        self.encContent.writeTag(self.TAG_SHOW_TITLE, self.info.showTitle)
        self.encContent.writeTag(self.TAG_SHOW_TITLE2, self.info.showTitle2)

    def _writeEpisodeTitle(self):
        self.encContent.writeTag(self.TAG_EPISODE_TITLE, self.info.episodeTitle)

    def _writeEpisodeDate(self):
        if self.info.year != 0:
            self.encContent.writeTag(self.TAG_YEAR, self.info.year)
        if self.year_of_date(self.info.episodeReleaseDate) != 0:
            self.encContent.writeTag(self.TAG_EPISODE_RELEASE_DATE, self.info.episodeReleaseDate)

    def _writeEpisodeLocked(self):
        if self.info.episodeLocked:  # don't write this tag if vsmeta is not locked!
            self.encContent.writeTag(self.TAG_EPISODE_LOCKED, True)

    def _writeSummary(self):
        if len(self.info.chapterSummary) > 0:
            self.encContent.writeTag(self.TAG_CHAPTER_SUMMARY, self.info.chapterSummary)

    def _writeClassification(self):
        self.encContent.writeTag(self.TAG_CLASSIFICATION, self.info.classification)

    def _writeRating(self):
        value = self.info.rating
        if value > 10.0:
            value = 10.0
        byte_char = int(value * 10).to_bytes(1, 'big') if value >= 0\
            else b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x01'
        self.encContent.writeTag(self.TAG_RATING, byte_char)

    def _writeEpisodeMetaJSON(self):
        if self.info.episodeMetaJson is not None and len(self.info.episodeMetaJson) > 0:
            self.encContent.writeTag(self.TAG_EPISODE_META_JSON, self.info.episodeMetaJson)

    def _writePoster(self):
        for index, episode_img in enumerate(self.info.episodeImageInfo):
            self.encContent.writeTag(self.TAG_EPISODE_THUMB_DATA)
            image_str = self.b64encodeImage(episode_img.image, episode_img.b64LastCharIsNewLine)
            self.encContent.writeTag(int(index + 1).to_bytes(1, 'big'), image_str)
            self.encContent.writeTag(self.TAG_EPISODE_THUMB_MD5)
            self.encContent.writeTag(int(index + 1).to_bytes(1, 'big'), episode_img.md5str)

    def _writeGroup1(self):
        # group 1 payload
        # TAG1_CAST, TAG1_DIRECTOR, TAG1_GENRE, TAG1_WRITER
        grp1_content = VsMetaCode()
        for cast in self.info.list.cast:
            grp1_content.writeTag(self.TAG1_CAST, cast)
        for director in self.info.list.director:
            grp1_content.writeTag(self.TAG1_DIRECTOR, director)
        for genre in self.info.list.genre:
            grp1_content.writeTag(self.TAG1_GENRE, genre)
        for writer in self.info.list.writer:
            grp1_content.writeTag(self.TAG1_WRITER, writer)

        if len(grp1_content) > 0:
            self.encContent.writeTag(self.TAG_GROUP1, grp1_content)

    def _writeGroup2(self):
        # tv show year
        tv_show_year = self.year_of_date(self.info.tvshowReleaseDate)
        # group 2 payload
        grp2_content = VsMetaCode()
        grp2_content.writeTag(self.TAG2_SEASON, self.info.season)
        grp2_content.writeTag(self.TAG2_EPISODE, self.info.episode)
        grp2_content.writeTag(self.TAG2_TV_SHOW_YEAR, tv_show_year)

        if tv_show_year != 0:
            grp2_content.writeTag(self.TAG2_RELEASE_DATE_TV_SHOW, self.info.tvshowReleaseDate)
        if self.info.tvshowLocked:
            grp2_content.writeTag(self.TAG2_LOCKED, True)
        if len(self.info.tvshowSummary) > 0:
            grp2_content.writeTag(self.TAG2_TVSHOW_SUMMARY, self.info.tvshowSummary)

        img_info = self.info.posterImageInfo
        image_bytes = None if img_info is None else img_info.image
        if image_bytes is not None and len(image_bytes) > 0:
            grp2_content.writeTag(self.TAG2_POSTER_DATA, self.b64encodeImage(image_bytes))
            grp2_content.writeTag(self.TAG2_POSTER_MD5, img_info.md5str)

        if self.info.tvshowMetaJson is not None and len(self.info.tvshowMetaJson) > 0:
            grp2_content.writeTag(self.TAG2_TVSHOW_META_JSON, self.info.tvshowMetaJson)

        grp3_content = VsMetaBase._writeGroup3(self)    # call the base-class implementation directly, because
        if len(grp3_content) > 0:                       # VsMetaSeriesEncoder_writeGroup3() is a void implementation
            grp2_content.writeTag(self.TAG2_GROUP3, grp3_content)

        if len(grp2_content) > 0:
            # Copy the complete group2 content to self.encContent
            self.encContent.writeTag(self.TAG_GROUP2)
            self.encContent.writeTag(b'\x01', grp2_content)     # group 2 - occurence no. \x01?

    def _writeGroup3(self) -> VsMetaCode:
        # group3 content may not be written to self.encContent directly, because it is also written into the group2
        # content when encoding TV-Series.
        # Remark: The returned bytes don't yet include a group3 TAG or length of the package, as this has to be done
        # by the method  calling _writeGroup3() in different ways for movies (TAG_GROUP3) and series (TAG2_GROUP3).
        grp3_content = VsMetaCode()
        img_info = self.info.backdropImageInfo
        if img_info.image is not None and len(img_info.image) > 0\
                and self.info.timestamp > int(datetime(1900, 1, 1, 0, 0).timestamp()):
            # group 3 payload = backdrop_data, backdrop_MD5, timestamp
            image_str = self.b64encodeImage(img_info.image, img_info.b64LastCharIsNewLine)
            grp3_content.writeTag(self.TAG3_BACKDROP_DATA, image_str)
            grp3_content.writeTag(self.TAG3_BACKDROP_MD5, img_info.md5str)
            grp3_content.writeTag(self.TAG3_TIMESTAMP, int(self.info.timestamp))

        return grp3_content     # return the grp3_content (it might be empty!)

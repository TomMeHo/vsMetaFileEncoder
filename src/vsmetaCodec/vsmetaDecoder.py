import json
from vsmetaCodec.vsmetaBase import *
from vsmetaCodec.vsmetaInfo import VsMetaImageInfo
from vsmetaCodec.vsmetaCode import VsMetaCode


class VsMetaDecoder(VsMetaBase):

    def decode(self, encoded_data: bytes = None) -> int:
        if encoded_data is not None:
            self.info = VsMetaInfo()
            self.info.episodeLocked = False
            self.encContent = VsMetaCode(encoded_data)
        return self._readVsMetaEncoded(self.encContent)

    def _readVsMetaEncoded(self, code: VsMetaCode) -> int:
        tag = code.readHeader()
        if tag != self.TAG_FILE_HEADER_MOVIE and\
                tag != self.TAG_FILE_HEADER_SERIES:
            error = "This is not a vsmeta movie or series file"
            raise Exception(error)

        episode_img = VsMetaImageInfo()
        while code.byteCountAhead() > 0:
            tag = code.readTag()
            if tag == self.TAG_SHOW_TITLE:
                self.info.showTitle = code.readString()
            elif tag == self.TAG_SHOW_TITLE2:
                self.info.showTitle2 = code.readString()
            elif tag == self.TAG_EPISODE_TITLE:
                self.info.episodeTitle = code.readString()
            elif tag == self.TAG_YEAR:
                self.info.year = code.readSpecialInt()
            elif tag == self.TAG_EPISODE_RELEASE_DATE:
                self.info.episodeReleaseDate = code.readString()
            elif tag == self.TAG_EPISODE_LOCKED:
                self.info.episodeLocked = code.readBool()
            elif tag == self.TAG_CHAPTER_SUMMARY:
                self.info.chapterSummary = code.readString()
            elif tag == self.TAG_EPISODE_META_JSON:
                self.info.episodeMetaJson = code.readString()
                meta_json = json.loads(self.info.episodeMetaJson)
                if meta_json is not None and "com.synology.TheMovieDb" in meta_json:
                    self.info.tmdbReference = meta_json["com.synology.TheMovieDb"]["reference"]
            elif tag == self.TAG_CLASSIFICATION:
                self.info.classification = code.readString()
            elif tag == self.TAG_RATING:
                self.info.rating = code.readFloat()
            elif tag == self.TAG_GROUP1:
                self._readGroup1(code.readVsData())
            elif tag == self.TAG_GROUP2:
                if code.readInt(1) != 1:    # index value, not used and not stored
                    raise Exception("Index of Group-2 is not \\x01 !")
                self._readGroup2(code.readVsData())
            elif tag == self.TAG_GROUP3:
                if code.readInt(1) != 1:    # index value, not used and not stored
                    raise Exception("Index of Group-3 is not \\x01 !")
                self._readGroup3(code.readVsData())
            elif tag == self.TAG_EPISODE_THUMB_DATA:
                if code.readInt(1) != 1:    # index value, not used and not stored
                    raise Exception("Index of episode_thumb_data is not \\x01 !")
                (episode_img.image,
                 episode_img.b64LastCharIsNewLine) = code.readImage()
            elif tag == self.TAG_EPISODE_THUMB_MD5:
                code.readInt(1)             # index value, not used and not stored
                if code.readString() != episode_img.md5str:
                    raise Exception("vsmeta md5-hash for episodeImage doesn't match with image byte-string!")
                self.info.episodeImageInfo.append(episode_img)
            else:
                code.dumpData(32)
                error = "Unknown TAG {0:2x} at POS {1:d} detected... Abort!"\
                        .format(int.from_bytes(tag, "little"), code.pos())
                raise Exception(error)
        return code.byteCountAhead()

    def _readGroup1(self, code: VsMetaCode) -> int:
        while code.byteCountAhead() > 0:
            tag = code.readTag()
            if tag == self.TAG1_CAST:
                self.info.list.cast.append(code.readString())
            elif tag == self.TAG1_DIRECTOR:
                self.info.list.director.append(code.readString())
            elif tag == self.TAG1_GENRE:
                self.info.list.genre.append(code.readString())
            elif tag == self.TAG1_WRITER:
                self.info.list.writer.append(code.readString())
            else:
                code.dumpData(32)
                error = "Unknown TAG {0:2x} in TAG_GROUP1 at POS {1:d} detected... Abort!"\
                        .format(int.from_bytes(tag, "little"), code.pos())
                raise Exception(error)
        return code.byteCountAhead()

    def _readGroup2(self, code: VsMetaCode) -> int:
        self.info.posterImageInfo = VsMetaImageInfo()
        while code.byteCountAhead() > 0:
            tag = code.readTag()
            if tag == self.TAG2_SEASON:
                self.info.season = code.readInt(1)
            elif tag == self.TAG2_EPISODE:
                self.info.episode = code.readInt(1)
            elif tag == self.TAG2_TV_SHOW_YEAR:
                self.info.tvShowYear = code.readSpecialInt()
            elif tag == self.TAG2_RELEASE_DATE_TV_SHOW:
                self.info.tvshowReleaseDate = code.readString()
            elif tag == self.TAG2_LOCKED:
                self.info.locked = code.readBool()
            elif tag == self.TAG2_TVSHOW_SUMMARY:
                self.info.tvshowSummary = code.readString()
            elif tag == self.TAG2_POSTER_DATA:
                (self.info.posterImageInfo.image,
                 self.info.posterImageInfo.b64LastCharIsNewLine) = code.readImage()
            elif tag == self.TAG2_POSTER_MD5:
                if code.readString() != self.info.posterImageInfo.md5str:
                    raise Exception("vsmeta md5-hash for poster image doesn't match with image byte-string!")
            elif tag == self.TAG2_TVSHOW_META_JSON:
                self.info.tvshowMetaJson = code.readString()
            elif tag == self.TAG2_GROUP3:
                self._readGroup3(code.readVsData())
            else:
                code.dumpData(32)
                error = "Unknown TAG {0:2x} in TAG_GROUP2 at POS {1:d} detected... Abort!"\
                        .format(int.from_bytes(tag, "little"), code.pos())
                raise Exception(error)
        return code.byteCountAhead()

    def _readGroup3(self, code: VsMetaCode) -> int:
        self.info.backdropImageInfo = VsMetaImageInfo()
        while code.byteCountAhead() > 0:
            tag = code.readTag()
            if tag == self.TAG3_BACKDROP_DATA:
                (self.info.backdropImageInfo.image,
                 self.info.backdropImageInfo.b64LastCharIsNewLine) = code.readImage()
            elif tag == self.TAG3_BACKDROP_MD5:
                if code.readString() != self.info.backdropImageInfo.md5str:
                    raise Exception("vsmeta md5-hash for backdrop image doesn't match with image byte-string!")
            elif tag == self.TAG3_TIMESTAMP:
                self.info.timestamp = code.readTimeStamp()
            else:
                code.dumpData(32)
                error = "Unknown TAG {0:2x} in TAG_GROUP3 at POS {1:d} detected... Abort!"\
                        .format(int.from_bytes(tag, "little"), code.pos())
                raise Exception(error)
        return code.byteCountAhead()

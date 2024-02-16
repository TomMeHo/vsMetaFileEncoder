import textwrap
import json
from datetime import date, datetime


class VsMetaImageInfo:
    def __init__(self):
        self.image = bytes()  # ByteString
        self.md5str = ""
        self.b64LastCharIsNewLine = False


class VsMetaListInfo:
    def __init__(self):
        self.cast = []      # initialization of an empty list
        self.genre = []
        self.director = []
        self.writer = []


class VsMetaInfo:
    def __init__(self):

        # Part1: General information for movies and series
        self.showTitle = ""
        self.showTitle2 = ""
        self.episodeTitle = ""

        self.year = 0
        self.episodeReleaseDate = date(1900, 1, 1)
        self.episodeLocked = True

        self.chapterSummary = ""
        self.episodeMetaJson = "null"       # Berfre: correct initialization for an 'empty json string'
        self.tmdbReference = {}             # convenience dictionary to access tmdb-id and imdb-id

        self.classification = ""
        self.rating = -1.0
        self.episodeImageInfo = []          # list of VsMetaImageInfo()

        # Group1 information as 4 lists of strings: Cast, Director, Genre, Writer
        self.list = VsMetaListInfo()

        # Group2 Series information:
        self.season = 0                     # 0 marks a movie, in series season is > 0
        self.episode = 0                    # 0 marks a movie, in series episode is > 0
        self.tvshowYear = 0
        self.tvshowReleaseDate = date(1900, 1, 1)
        self.tvshowLocked = True
        self.tvshowSummary = ""
        self.posterImage = VsMetaImageInfo()
        self.tvshowMetaJson = "null"

        # Group3 Information:
        self.backdropImageInfo = VsMetaImageInfo()
        self.timestamp = datetime(1900, 1, 1, 0, 0).timestamp()

    @property
    def episodeReleaseDate(self) -> date:
        return self._episodeReleaseDate

    @episodeReleaseDate.setter
    def episodeReleaseDate(self, release_date: str | date):
        if type(release_date) is str:
            self._episodeReleaseDate = date.fromisoformat(release_date)
        elif type(release_date) is date:
            self._episodeReleaseDate = release_date
        self.year = 0
        if self._episodeReleaseDate.year > 1900:
            self.year = self._episodeReleaseDate.year

    def setEpisodeDate(self, episode_date: str | date):
        self.episodeReleaseDate = episode_date

    @property
    def tvshowReleaseDate(self) -> date:
        return self._tvshowReleaseDate

    @tvshowReleaseDate.setter
    def tvshowReleaseDate(self, release_date: str | date):
        if type(release_date) is str:
            self._tvshowReleaseDate = date.fromisoformat(release_date)
        elif type(release_date) is date:
            self._tvshowReleaseDate = release_date

        self.tvShowYear = 0
        if self._tvshowReleaseDate.year > 1900:
            self.tvShowYear = self._tvshowReleaseDate.year

    def setShowDate(self, show_date: str | date):
        self.tvshowReleaseDate = show_date

    @property
    def timestamp(self) -> int:
        return self._timestamp               # timestamps are stored internally as integer without milliseconds

    @timestamp.setter
    def timestamp(self, stamp: int | float):
        self._timestamp = int(stamp)         # if the parameter is float, cut of the milliseconds with int()

    def printInfo(self, path: str):
        path += "" if path[:-1] == "/" else "/"

        print("Title          : {0}".format(self.showTitle))
        print("Title2         : {0}".format(self.showTitle2))
        print("Episode title  : {0}".format(self.episodeTitle))
        print("Episode year   : {0}".format(self.year))
        print("Episode date   : {0}".format(self.episodeReleaseDate))
        print("Episode locked : {0}".format(self.episodeLocked))
        print("TimeStamp      : {0}".format(self.timestamp))
        print("Classification : {0}".format(self.classification))
        print("Rating         : {0:1.1f}".format(self.rating))
        wrap_text = "\n                 ".join(textwrap.wrap(self.chapterSummary, 150))
        print("Summary        : {0}".format(wrap_text))
        wrap_text = ("\n                 ".join
                     (textwrap.wrap("".join(["{0}, ".format(name) for name in self.list.cast]), 150)))
        print("Cast           : " + wrap_text)
        wrap_text = ("\n                 ".join
                     (textwrap.wrap("".join(["{0}, ".format(name) for name in self.list.director]), 140)))
        print("Director       : " + wrap_text)
        print("Writer         : " + "".join(["{0}, ".format(name) for name in self.list.writer]))
        print("Genre          : " + "".join(["{0}, ".format(name) for name in self.list.genre]))
        print("Episode Meta  :\n{0}".format(json.dumps(json.loads(self.episodeMetaJson), indent=3)))

        if self.backdropImageInfo is not None:
            with open(path + "image_back_drop.jpg", "wb") as f:
                f.write(self.backdropImageInfo.image)

        for idx, image_info in enumerate(self.episodeImageInfo):
            with open(path + "image_poster_{0:02d}.jpg".format(idx + 1), "wb") as f:
                f.write(image_info.image)

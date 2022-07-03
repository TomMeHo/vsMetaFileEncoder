from datetime import date
import unittest
import os

from vsmetaEncoder.vsmetaSeriesEncoder import VsMetaSeriesEncoder
from vsmetaEncoder.vsmetaInfo import VsMetaInfo
from testHelpers import readPosterVsMetaFile, readTemplateFile, compareBytesBitByBit, compareBytesLength, writeVsMetaFile

class TestVsMetaEncoder(unittest.TestCase):

    def test_encodeTemplate2(self):

        # setup class under test
        info = VsMetaInfo()
        info.showTitle = 'Checker'
        info.setShowDate(date(1920, 1, 1))
        info.setEpisodeDate(date(2021, 1, 21))
        info.tvshowLocked = True

        info.episodeTitle = 'Skateboardcheck'
        info.episodeLocked = True
        info.episodeMetaJson = "null"
        info.tvshowMetaJson = "null"

        info.chapterSummary = "Zusammenfassung"

        # execute, prepare result
        writer = VsMetaSeriesEncoder()
        testData = writer.encode(info)

        # compare
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"template2.vsmeta"))
        compareBytesBitByBit(self, template, testData)
        compareBytesLength(self, template, testData)

    def test_encodeTemplate3(self):

        # setup class under test
        info = VsMetaInfo()
        info.showTitle = 'aaa20210122'
        info.setShowDate(date(2021, 1, 22))
        info.tvshowLocked = True

        info.episodeTitle = 'Episode'
        info.setEpisodeDate(date(2021, 1, 21))
        info.episodeLocked = True

        info.chapterSummary = "Text"

        # execute, prepare result
        writer = VsMetaSeriesEncoder()
        testData = writer.encode(info)

        # compare
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"template3.vsmeta"))
        compareBytesBitByBit(self, template, testData)
        compareBytesLength(self, template, testData)

    def test_encodeTemplate4(self):
        # setup class under test
        info = VsMetaInfo()
        info.showTitle = 'Die Sendung mit der Maus'
        info.tvshowLocked = True

        info.episodeTitle = 'Die Sendung vom 02.02.2021'
        info.setEpisodeDate(date(2021, 2, 2))
        info.episodeLocked = True

        # execute, prepare result
        writer = VsMetaSeriesEncoder()
        testData = writer.encode(info)

        #writeVsMetaFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),'template4-reconstructed.vsmeta'), testData)

        # compare
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"template4.vsmeta"))
        compareBytesBitByBit(self, template, testData)
        compareBytesLength(self, template, testData)

    def test_encodeTemplate5Poster(self):
        # setup class under test
        
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"template5_poster.vsmeta"))
        tvimage = os.path.join(os.path.dirname(os.path.realpath(__file__)),"Testtvimage.jpg")
        posterimage = os.path.join(os.path.dirname(os.path.realpath(__file__)),"Testposter.jpg")
        
        readPosterVsMetaFile(template, posterimage,
                             VsMetaSeriesEncoder.TAG_EPISODE_THUMB_DATA,
                             VsMetaSeriesEncoder.TAG_EPISODE_THUMB_MD5)
        
        readPosterVsMetaFile(template, tvimage,
                             VsMetaSeriesEncoder.TAG2_POSTER_DATA,
                             VsMetaSeriesEncoder.TAG2_POSTER_MD5)
        
        info = VsMetaInfo()
        
        
        info.showTitle = 'TV series'
        info.tvshowLocked = True
        info.tvshowSummary = 'Series summary.'
        info.season = 1
        info.setShowDate(date(2022, 7, 3))
        info.tvshowMetaJson = '{}'

        with open(tvimage, "rb") as image2string:
            info.images.tvshowPoster = image2string.read()

        info.episodeTitle = 'Episode Title'
        info.setEpisodeDate(date(2022, 7, 3))
        info.episodeLocked = True
        info.episode = 1
        info.chapterSummary = 'This is a long summary of a the episode.'
        info.episodeMetaJson = 'null'
    
        with open(posterimage, "rb") as image2string:
            info.images.episodeImage = image2string.read()
        
        os.remove(tvimage)
        os.remove(posterimage)
        
        # execute, prepare result
        writer = VsMetaSeriesEncoder()
        testData = writer.encode(info)

        #writeVsMetaFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),'template_movie4-reconstructed.vsmeta'), testData)

        # compare
        compareBytesBitByBit(self, template, testData)
        compareBytesLength(self, template, testData)
        

if __name__ == "__main__":
    unittest.main()
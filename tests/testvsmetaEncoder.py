from datetime import date
import unittest
import os

from vsmetaEncoder.vsmetaSeriesEncoder import VsMetaSeriesEncoder
from vsmetaEncoder.vsmetaMovieEncoder import VsMetaMovieEncoder
from vsmetaEncoder.vsmetaInfo import VsMetaInfo
from testHelpers import readTemplateFile, compareBytesBitByBit, compareBytesLength, writeVsMetaFile

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

        writeVsMetaFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),'template3-reconstructed.vsmeta'), testData)

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

        writeVsMetaFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),'template4-reconstructed.vsmeta'), testData)

        # compare
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"template4.vsmeta"))
        compareBytesBitByBit(self, template, testData)
        compareBytesLength(self, template, testData)

    def test_encodeTemplate6(self):
        # setup class under test
        info = VsMetaInfo()
        info.episodeTitle = 'Filmtitel'
        info.setEpisodeDate(date(2021, 1, 1))

        # execute, prepare result
        writer = VsMetaMovieEncoder()
        testData = writer.encode(info)

        writeVsMetaFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),'template-movie1-reconstructed.vsmeta'), testData)

        # compare
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"template_movie1.vsmeta"))
        compareBytesBitByBit(self, template, testData)
        compareBytesLength(self, template, testData)

    def test_encodeTemplate7(self):
        # setup class under test
        info = VsMetaInfo()
        info.episodeTitle = 'Klassik'
        info.showTitle = 'Franz Liszt: Sonetto di Petrarca'
        info.setEpisodeDate(date(2019, 9, 24))
        info.chapterSummary = 'Im Italien-Teil seiner Sammlung "Années de pèlerinage" widmet sich Franz Liszt mehreren Sonetten von Francesco Petrarca.'

        # execute, prepare result
        writer = VsMetaMovieEncoder()
        testData = writer.encode(info)

        writeVsMetaFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),'template-movie3-reconstructed.vsmeta'), testData)

        # compare
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"template_movie3.vsmeta"))
        compareBytesBitByBit(self, template, testData)
        compareBytesLength(self, template, testData)


if __name__ == "__main__":
    unittest.main()
from datetime import date
import unittest
import os

from vsmetaEncoder.vsmetaEncoder import VsMetaEncoder
from vsmetaEncoder.vsmetaInfo import VsMetaInfo
from testHelpers import readTemplateFile, compareBytesBitByBit, compareBytesLength, writeVsMetaFile

class TestVsMetaEncoder(unittest.TestCase):

    def test_encodeTemplate2(self):

        # setup class under test
        info = VsMetaInfo()
        info.showTitle = 'Checker'
        info.tvshowReleaseDate = date(1920, 1, 1)
        info.tvshowLocked = True

        info.episodeTitle = 'Skateboardcheck'
        info.episodeReleaseDate = date(2021, 1, 21)
        info.episodeLocked = True
        info.episodeMetaJson = "null"
        info.tvshowMetaJson = "null"

        info.chapterSummary = "Zusammenfassung"

        # execute, prepare result
        writer = VsMetaEncoder()
        testData = writer.encode(info)

        # writeVsMetaFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),'template2-reconstructed.vsmeta'), testData)

        # compare
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"template2.vsmeta"))
        compareBytesBitByBit(self, template, testData)
        compareBytesLength(self, template, testData)

    def test_encodeTemplate3(self):

        # setup class under test
        info = VsMetaInfo()
        info.showTitle = 'aaa20210122'
        info.tvshowReleaseDate = date(2021, 1, 22)
        info.tvshowLocked = True

        info.episodeTitle = 'Episode'
        info.episodeReleaseDate = date(2021, 1, 21)
        info.episodeLocked = True

        info.chapterSummary = "Text"

        # execute, prepare result
        writer = VsMetaEncoder()
        testData = writer.encode(info)

        writeVsMetaFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),'template3-reconstructed.vsmeta'), testData)

        # compare
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"template3.vsmeta"))
        compareBytesBitByBit(self, template, testData)
        compareBytesLength(self, template, testData)

if __name__ == "__main__":
    unittest.main()
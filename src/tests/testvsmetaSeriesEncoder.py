from datetime import date
import unittest
import os

from vsmetaCodec.vsmetaEncoder import VsMetaSeriesEncoder
from vsmetaCodec.vsmetaInfo import VsMetaInfo
from testHelpers import readTemplateFile, compareBytesBitByBit, compareBytesLength, writeVsMetaFile


class TestVsMetaEncoder(unittest.TestCase):

    def test_encodeTemplate2(self):

        # setup class under test
        info = VsMetaInfo()
        info.showTitle = 'Checker'
        info.showTitle2 = 'Checker'
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
        test_data = writer.encode(info)

        # compare
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), "template2.vsmeta"))
        compareBytesBitByBit(self, template, test_data)
        compareBytesLength(self, template, test_data)

    def test_encodeTemplate3(self):

        # setup class under test
        info = VsMetaInfo()
        info.showTitle = 'aaa20210122'
        info.showTitle2 = 'aaa20210122'
        info.setShowDate(date(2021, 1, 22))
        info.tvshowLocked = True
        info.tvshowMetaJson = ''    # don't write the json 'null'-string for 'empty json'

        info.episodeTitle = 'Episode'
        info.setEpisodeDate(date(2021, 1, 21))
        info.episodeLocked = True
        info.episodeMetaJson = ''   # don't write the json 'null'-string for 'empty json'

        info.chapterSummary = "Text"

        # execute, prepare result
        writer = VsMetaSeriesEncoder()
        test_data = writer.encode(info)

        # compare
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), "template3.vsmeta"))
        compareBytesBitByBit(self, template, test_data)
        compareBytesLength(self, template, test_data)

    def test_encodeTemplate4(self):
        # setup class under test
        info = VsMetaInfo()
        info.showTitle = 'Die Sendung mit der Maus'
        info.showTitle2 = 'Die Sendung mit der Maus'
        info.tvshowLocked = True
        info.tvshowMetaJson = ''   # don't write the json 'null'-string for 'empty json'

        info.episodeTitle = 'Die Sendung vom 02.02.2021'
        info.setEpisodeDate(date(2021, 2, 2))
        info.episodeLocked = True
        info.episodeMetaJson = ''  # don't write the json 'null'-string for 'empty json'

        # execute, prepare result
        writer = VsMetaSeriesEncoder()
        test_data = writer.encode(info)

        writeVsMetaFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'template4-reconstructed.vsmeta'), test_data)

        # compare
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), "template4.vsmeta"))
        compareBytesBitByBit(self, template, test_data)
        compareBytesLength(self, template, test_data)


if __name__ == "__main__":
    unittest.main()

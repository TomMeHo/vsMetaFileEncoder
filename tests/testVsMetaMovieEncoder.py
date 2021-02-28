from datetime import date
import unittest
import os

from vsmetaEncoder.vsmetaMovieEncoder import VsMetaMovieEncoder
from vsmetaEncoder.vsmetaInfo import VsMetaInfo
from testHelpers import readTemplateFile, compareBytesBitByBit, compareBytesLength, writeVsMetaFile

class TestVsMetaEncoder(unittest.TestCase):

    def test_encodeMovieTemplate1(self):

        # setup class under test
        writer = VsMetaMovieEncoder()
        info = writer.info
        info.episodeTitle = 'Filmtitel'
        info.year = 2021
        info.episodeReleaseDate = date(2021, 1, 1)

        # execute, prepare result
        testData = writer.encode(info)

        # compare
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"template_movie1.vsmeta"))
        compareBytesBitByBit(self, template, testData)
        compareBytesLength(self, template, testData)


if __name__ == "__main__":
    unittest.main()
from datetime import date
import unittest
import os

from vsmetaEncoder.vsmetaMovieEncoder import VsMetaBase
from vsmetaEncoder.vsmetaInfo import VsMetaInfo


class VsMetaEncoderBaseInjector(VsMetaBase):

    def __init__(self):
        super(VsMetaEncoderBaseInjector, self).__init__()

    def writeSummary(self):
        self._writeSummary()

    def writeEpisodeDate(self):
        self._writeEpisodeDate()


class TestVsMetaEncoder(unittest.TestCase):

    def __test_chapterSummary(self, summary:str, epxectedBytes:bytes):

        # setup class under test
        cut = VsMetaEncoderBaseInjector()

        # setup test data
        vsMeta = cut.info
        vsMeta.chapterSummary = summary
        cut.info = vsMeta
        
        # compare
        cut.writeSummary()
        testResult = cut.encodedContent

        self.assertEqual(testResult, epxectedBytes, msg= "Encoding of chapterSummary wrong.")

    def test_chapterSummary(self):

        summary = 'Tanken, l prfen, die Windschutzscheibe wischen, wenn es notwendig ist und kassieren - das hat frher alles der Tankwart erledigt. Wenn Armin heute sein Auto tanken will, muss er das selbst machen. Einen Tankwart gibt es hier nicht mehr, erst beim Bezahlen im Tank-Shop trifft er jemanden'
        expectedData = b'\x42\x9E\x02' + bytes(summary, 'utf-8')
        self.__test_chapterSummary(summary, expectedData)

    def test_chapterSummaryLength0(self):

        summary = ""
        expectedData = b'' + bytes(summary, 'utf-8')
        self.__test_chapterSummary(summary, expectedData)

    def test_chapterSummaryLength120(self):

        summary = "A"*120
        expectedData = b'\x42\x78' + bytes(summary, 'utf-8')
        self.__test_chapterSummary(summary, expectedData)

    def test_chapterSummaryLength128(self):

        summary = "B"*128
        expectedData = b'\x42\x80\x01' + bytes(summary, 'utf-8')
        self.__test_chapterSummary(summary, expectedData)

    def test_chapterSummaryLength640(self):

        summary = "C"*640
        expectedData = b'\x42\x80\x05' + bytes(summary, 'utf-8')
        self.__test_chapterSummary(summary, expectedData)

    def test_chapterSummaryLength1276(self):

        summary = "D"*1276
        expectedData = b'\x42\xFC\x09' + bytes(summary, 'utf-8')
        self.__test_chapterSummary(summary, expectedData)

    def test_episodeDate(self):

        testedDate = date(2021, 2, 28)
        expectedData = b'\x28\xe5\x0f2\n2021-02-28'

        # setup class under test
        cut = VsMetaEncoderBaseInjector()

        # setup test data
        vsMeta = cut.info
        vsMeta.setEpisodeDate(testedDate)
        cut.info = vsMeta
        
        # compare
        cut.writeEpisodeDate()
        testResult = cut.encodedContent

        self.assertEqual(testResult, expectedData, msg= "Encoding of episode date wrong.")

if __name__ == "__main__":
    unittest.main()
from datetime import date
import unittest

from vsmetaCodec.vsmetaEncoder import VsMetaBase


class VsMetaEncoderBaseInjector(VsMetaBase):

    def __init__(self):
        super(VsMetaEncoderBaseInjector, self).__init__()

    def writeSummary(self):
        self._writeSummary()

    def writeEpisodeDate(self):
        self._writeEpisodeDate()


class TestVsMetaEncoder(unittest.TestCase):

    def __test_chapterSummary(self, summary: str, expected_bytes: bytes):

        # setup class under test
        cut = VsMetaEncoderBaseInjector()

        # setup test data
        vs_meta = cut.info
        vs_meta.chapterSummary = summary
        cut.info = vs_meta
        
        # compare
        cut.writeSummary()
        test_result = cut.encContent.data()

        self.assertEqual(test_result, expected_bytes, msg="Encoding of chapterSummary wrong.")

    def test_chapterSummary(self):
        summary = 'Tanken, Luftdruck prüfen, die Windschutzscheibe wischen, wenn es notwendig ist und '\
                  + 'kassieren - das hat früher alles der Tankwart erledigt. Wenn Armin heute sein Auto '\
                  + 'tanken will, muss er das selbst machen. Einen Tankwart gibt es hier nicht mehr, '\
                  + 'erst beim Bezahlen im Tank-Shop trifft er jemanden'
        expected_data = b'\x42\xAA\x02' + bytes(summary, 'utf-8')
        self.__test_chapterSummary(summary, expected_data)

    def test_chapterSummaryLength0(self):

        summary = ""
        expected_data = b'' + bytes(summary, 'utf-8')
        self.__test_chapterSummary(summary, expected_data)

    def test_chapterSummaryLength120(self):

        summary = "A"*120
        expected_data = b'\x42\x78' + bytes(summary, 'utf-8')
        self.__test_chapterSummary(summary, expected_data)

    def test_chapterSummaryLength128(self):

        summary = "B"*128
        expected_data = b'\x42\x80\x01' + bytes(summary, 'utf-8')
        self.__test_chapterSummary(summary, expected_data)

    def test_chapterSummaryLength640(self):

        summary = "C"*640
        expected_data = b'\x42\x80\x05' + bytes(summary, 'utf-8')
        self.__test_chapterSummary(summary, expected_data)

    def test_chapterSummaryLength1276(self):

        summary = "D"*1276
        expected_data = b'\x42\xFC\x09' + bytes(summary, 'utf-8')
        self.__test_chapterSummary(summary, expected_data)

    def test_episodeDate(self):

        tested_date = date(2021, 2, 28)
        expected_data = b'\x28\xe5\x0f2\n2021-02-28'

        # setup class under test
        cut = VsMetaEncoderBaseInjector()

        # setup test data
        vs_meta = cut.info
        vs_meta.setEpisodeDate(tested_date)
        cut.info = vs_meta
        
        # compare
        cut.writeEpisodeDate()
        test_result = cut.encContent.data()

        self.assertEqual(test_result, expected_data, msg="Encoding of episode date wrong.")


if __name__ == "__main__":
    unittest.main()

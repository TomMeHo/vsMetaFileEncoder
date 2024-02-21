import unittest
import os

from vsmetaCodec.vsmetaDecoder import VsMetaDecoder
from vsmetaCodec.vsmetaEncoder import VsMetaMovieEncoder, VsMetaSeriesEncoder
from testHelpers import readTemplateFile    # , compareBytesBitByBit, compareBytesLength, writeVsMetaFile


class TestVsMetaEncoder(unittest.TestCase):

    def __test_decodeEncodeTemplate(self, template_filename: str):
        # setup class under test
        dir_path = os.path.dirname(os.path.realpath(__file__))
        expected_bytes = readTemplateFile(os.path.join(dir_path, template_filename))
        decoder = VsMetaDecoder()
        decoder.decode(expected_bytes)

        if decoder.info.season == 0:
            vsmeta_type = "movie"
        else:
            vsmeta_type = "series"
            if decoder.info.tvshowMetaJson == "null":
                decoder.info.tvshowMetaJson = ""

        vsmeta_encoder = VsMetaMovieEncoder() if decoder.info.season == 0 else VsMetaSeriesEncoder()

        test_result = vsmeta_encoder.encode(decoder.info)

        test_result_filename = os.path.join(dir_path, "test_result_encoded.vsmeta")
        vsmeta_encoder.writeVsMetaFile(test_result_filename)

        self.assertEqual(test_result, expected_bytes, msg=("Encoding of %s is wrong." % vsmeta_type))

    def test_decodeMovieTemplate10(self):
        self.__test_decodeEncodeTemplate("template_movie10.vsmeta")

    def test_decodeMovieTemplate11(self):
        self.__test_decodeEncodeTemplate("template_movie11.vsmeta")

    def test_decodeMovieTemplate12(self):
        self.__test_decodeEncodeTemplate("template_movie12.vsmeta")

    def test_decodeMovieTemplate13(self):
        self.__test_decodeEncodeTemplate("template_movie13.vsmeta")

    def test_decodeSeriesTemplate20(self):
        self.__test_decodeEncodeTemplate("template_series20.vsmeta")

    def test_decodeSeriesTemplate21(self):
        self.__test_decodeEncodeTemplate("template_series21.vsmeta")

    def test_decodeSeriesTemplate22(self):
        self.__test_decodeEncodeTemplate("template_series22.vsmeta")

    def test_decodeSeriesTemplate23(self):
        self.__test_decodeEncodeTemplate("template_series23.vsmeta")

    def test_decodeSeriesTemplate24(self):
        self.__test_decodeEncodeTemplate("template_series23.vsmeta")


if __name__ == "__main__":
    unittest.main()

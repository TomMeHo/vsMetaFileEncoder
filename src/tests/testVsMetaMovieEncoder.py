from datetime import date
import unittest
import os

from vsmetaCodec.vsmetaEncoder import VsMetaMovieEncoder
from vsmetaCodec.vsmetaInfo import VsMetaInfo
from testHelpers import readTemplateFile, compareBytesBitByBit, compareBytesLength, writeVsMetaFile


class TestVsMetaEncoder(unittest.TestCase):

    def test_encodeMovieTemplate1(self):
        # setup class under test
        writer = VsMetaMovieEncoder()
        info = writer.info
        info.showTitle = 'Filmtitel'
        info.showTitle2 = 'Filmtitel'
        info.year = 2021
        info.episodeReleaseDate = date(2021, 1, 1)

        # execute, prepare result
        test_data = writer.encode(info)

        # compare
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                 "template_movie1.vsmeta"))
        compareBytesBitByBit(self, template, test_data)
        compareBytesLength(self, template, test_data)

    def test_encodeTemplate2(self):
        # setup class under test
        info = VsMetaInfo()
        info.showTitle = 'Filmtitel'
        info.showTitle2 = 'Filmtitel'
        info.setEpisodeDate(date(2021, 1, 1))

        # execute, prepare result
        writer = VsMetaMovieEncoder()
        test_data = writer.encode(info)

        # compare
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                 "template_movie1.vsmeta"))
        compareBytesBitByBit(self, template, test_data)
        compareBytesLength(self, template, test_data)

    def test_encodeTemplate3(self):
        # setup class under test
        info = VsMetaInfo()
        info.showTitle = 'Klassik'
        info.showTitle2 = 'Klassik'
        info.episodeTitle = 'Franz Liszt: Sonetto di Petrarca'
        info.setEpisodeDate(date(2019, 9, 24))
        info.chapterSummary = ('Im Italien-Teil seiner Sammlung "Années de pèlerinage" widmet sich Franz Liszt '
                               + 'mehreren Sonetten von Francesco Petrarca.')

        # execute, prepare result
        writer = VsMetaMovieEncoder()
        test_data = writer.encode(info)

        # compare
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                 "template_movie3.vsmeta"))
        compareBytesBitByBit(self, template, test_data)
        compareBytesLength(self, template, test_data)

    def test_encodeTemplate4(self):
        # setup class under test
        info = VsMetaInfo()
        info.showTitle = 'Nach der Hochzeit'
        info.showTitle2 = 'Nach der Hochzeit'
        info.episodeTitle = 'Kino - Filme'
        info.setEpisodeDate(date(2021, 3, 8))
        info.chapterSummary = ('Um die drohende Schließung seines indischen Waisenhauses abzuwenden, kehrt der '
                               + 'Aussteiger Jacob nach vielen Jahren widerwillig in die dänische Heimat zurück, '
                               + 'wo der reiche Bauunternehmer Jørgen ihm eine großzügige Spende zukommen lassen '
                               + 'will. Überraschend stellt sich heraus, dass Jørgens Frau Helene Jacobs große '
                               + 'Jugendliebe und er der leibliche Vater ihrer Tochter Anna ist - von der er bislang '
                               + 'nichts wusste. Jacob wird schmerzlich bewusst, dass er in ein tragisches '
                               + 'Familiendrama verwickelt ist, denn der unheilbar kranke Jørgen hat nicht mehr '
                               + 'lange zu leben. Jacob soll sich nach Jørgens Tod um dessen Familie kümmern.')

        # execute, prepare result
        writer = VsMetaMovieEncoder()
        test_data = writer.encode(info)

        writeVsMetaFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                     'template_movie4-reconstructed.vsmeta'), test_data)

        # compare
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                 "template_movie4.vsmeta"))
        compareBytesBitByBit(self, template, test_data)
        compareBytesLength(self, template, test_data)


if __name__ == "__main__":
    unittest.main()

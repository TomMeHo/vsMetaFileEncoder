from datetime import date
import unittest
import os

from vsmetaEncoder.vsmetaMovieEncoder import VsMetaMovieEncoder
from vsmetaEncoder.vsmetaInfo import VsMetaInfo
from testHelpers import readPosterVsMetaFile, readTemplateFile, compareBytesBitByBit, compareBytesLength, writeVsMetaFile

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

    def test_encodeTemplate2(self):
        # setup class under test
        info = VsMetaInfo()
        info.episodeTitle = 'Filmtitel'
        info.setEpisodeDate(date(2021, 1, 1))

        # execute, prepare result
        writer = VsMetaMovieEncoder()
        testData = writer.encode(info)

        # compare
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"template_movie1.vsmeta"))
        compareBytesBitByBit(self, template, testData)
        compareBytesLength(self, template, testData)

    def test_encodeTemplate3(self):
        # setup class under test
        info = VsMetaInfo()
        info.episodeTitle = 'Klassik'
        info.showTitle = 'Franz Liszt: Sonetto di Petrarca'
        info.setEpisodeDate(date(2019, 9, 24))
        info.chapterSummary = 'Im Italien-Teil seiner Sammlung "Années de pèlerinage" widmet sich Franz Liszt mehreren Sonetten von Francesco Petrarca.'

        # execute, prepare result
        writer = VsMetaMovieEncoder()
        testData = writer.encode(info)

        # compare
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"template_movie3.vsmeta"))
        compareBytesBitByBit(self, template, testData)
        compareBytesLength(self, template, testData)

    def test_encodeTemplate4(self):
        # setup class under test
        info = VsMetaInfo()
        info.episodeTitle = 'Nach der Hochzeit'
        info.showTitle = 'Kino - Filme'
        info.setEpisodeDate(date(2021, 3, 8))
        info.chapterSummary = 'Um die drohende Schließung seines indischen Waisenhauses abzuwenden, kehrt der Aussteiger Jacob nach vielen Jahren widerwillig in die dänische Heimat zurück, wo der reiche Bauunternehmer Jørgen ihm eine großzügige Spende zukommen lassen will. Überraschend stellt sich heraus, dass Jørgens Frau Helene Jacobs große Jugendliebe und er der leibliche Vater ihrer Tochter Anna ist - von der er bislang nichts wusste. Jacob wird schmerzlich bewusst, dass er in ein tragisches Familiendrama verwickelt ist, denn der unheilbar kranke Jørgen hat nicht mehr lange zu leben. Jacob soll sich nach Jørgens Tod um dessen Familie kümmern.'

        # execute, prepare result
        writer = VsMetaMovieEncoder()
        testData = writer.encode(info)

        #writeVsMetaFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),'template_movie4-reconstructed.vsmeta'), testData)

        # compare
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"template_movie4.vsmeta"))
        compareBytesBitByBit(self, template, testData)
        compareBytesLength(self, template, testData)

    def test_encodeTemplate5Poster(self):
        # setup class under test
        
        template = readTemplateFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"template_movie5_poster.vsmeta"))
        testimage = os.path.join(os.path.dirname(os.path.realpath(__file__)),"Testposter.jpg")
        
        
        start_byte = VsMetaMovieEncoder.TAG_EPISODE_THUMB_DATA = b'\x8a'
        end_byte = VsMetaMovieEncoder.TAG_EPISODE_THUMB_MD5 = b'\x92'
        
        readPosterVsMetaFile(template, testimage, start_byte, end_byte)
        
        info = VsMetaInfo()
        info.episodeTitle = 'MovieTitle'
        info.showTitle = 'Short summary of movie'
        info.setEpisodeDate(date(2022, 7, 3))
        info.chapterSummary = 'This is a long summary of a movie.'

        with open(testimage, "rb") as image2string:
            info.images.episodeImage = image2string.read()
        os.remove(testimage)
        
        # execute, prepare result
        writer = VsMetaMovieEncoder()
        testData = writer.encode(info)

        #writeVsMetaFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),'template_movie4-reconstructed.vsmeta'), testData)

        # compare
        compareBytesBitByBit(self, template, testData)
        compareBytesLength(self, template, testData)

if __name__ == "__main__":
    unittest.main()
    
    
from vsmetaEncoder import vsMetaEncoder, vsMetaInfo
from datetime import date
import unittest
from TestHelpers import TestHelpers

class TestVsMetaEncoder(unittest.TestCase):

    def test_encodeTemplate1(self):
        # ... which is almost empty and contains only a title.

        # setup class under test
        info = vsMetaInfo()
        info.showTitle = '2341896 31589835'
        info.episode = 18
        info.season = 1

        # execute, prepare result
        writer = vsMetaEncoder()
        testData = writer.encode(info)

        # compare
        template = TestHelpers.readTemplateFile('tests\\template1.vsmeta')
        TestHelpers.compareBytesBitByBit(self, template, testData)
        TestHelpers.compareBytesLength(self, template, testData)

if __name__ == "__main__":
    unittest.main()
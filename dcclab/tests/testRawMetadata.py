from dcclab import RAWMetadata as mtdt
import env
import unittest
import os


class TestRawMetadata(env.DCCLabTestCase):
    def setUp(self) -> None:
        self.rawPath = os.path.join(str(self.dataDir), '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_XYT.raw')
        self.iniPath = os.path.join(str(self.dataDir), '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_XYT.ini')
        self.xmlPath = os.path.join(str(self.dataDir), '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_XYT.xml')

    def tearDown(self) -> None:
        #os.remove(self.rawPath)
        #os.remove(self.iniPath)
        #os.remove(self.xmlPath)
        pass

    def testFileName(self):
        metadata = mtdt(self.rawPath)
        self.assertEqual(metadata.fileName, '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_XYT')

    def testIniPath(self):
        metadata = mtdt(self.rawPath)
        self.assertEqual(metadata.iniPath, self.iniPath)

    def testXmlPath(self):
        metadata = mtdt(self.rawPath)
        self.assertEqual(metadata.xmlPath, self.xmlPath)

    def testDate(self):
        metadata = mtdt(self.rawPath)
        self.assertEqual('2019-01-01 12:12:12', metadata.date)


if __name__ == '__main__':
    unittest.main()
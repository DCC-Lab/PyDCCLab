from dcclab import PDKRAWMetadata as mtdt
import env
import unittest
import os


class TestPDKRAWMetadata(env.DCCLabTestCase):
    def setUp(self) -> None:
        self.rawPath = os.path.join(str(self.dataDir), '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_XYT.raw')
        self.iniPath = os.path.join(str(self.dataDir), '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_XYT.ini')
        self.xmlPath = os.path.join(str(self.dataDir), '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_OME.xml')
        with open(self.iniPath, 'w') as file:
            file.write('[_]\nTest_File = This is a test file\nno.of.channels = 1.000000000000\nblank_line = blank\n'
                       'frame.count = 1000.000000000000\n\nx.pixels = 1024.000000000000\ny.pixels = 512.000000000000\n'
                       'x.voltage = 5.000000000000\ny.voltage = 1.250000000000\n\nwrong.line = bleh\n'
                       'pixel.resolution = 5.000000000000\nLaser.Power = 21.500000000000\n')

        with open(self.xmlPath, 'w') as file:
            file.write('<TEST>\n')
            file.write('\t<items>\n')
            file.write('\t</items>\n')
            file.write('</TEST>\n')

    def tearDown(self) -> None:
        os.remove(self.iniPath)
        os.remove(self.xmlPath)

    def testFileName(self):
        metadata = mtdt(self.rawPath)
        self.assertEqual(metadata.fileName, '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_XYT')

    def testDate(self):
        metadata = mtdt(self.rawPath)
        self.assertEqual('2019-01-01 12:12:12', metadata.date)

    def testExtractDataFromIniFile(self):
        metadata = mtdt(self.rawPath)
        self.assertTrue(metadata.extractDataFromIniFile())

    def testXmlPath(self):
        metadata = mtdt(self.rawPath)
        self.assertEqual(metadata.xmlPath, self.xmlPath)

    def testXmlPathLineShifted(self):
        filePath = os.path.join(str(self.dataDir),
                                '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_XYT.lineshifted.raw')
        metadata = mtdt(filePath)
        self.assertEqual(metadata.xmlPath, self.xmlPath)

    def testReadXmlFile(self):
        metadata = mtdt(self.rawPath)
        self.assertTrue(metadata.readXmlFile())

    def testKeys(self):
        metadata = mtdt(self.rawPath)
        self.assertEqual(metadata.keys, {'Laser.Power': 'REAL', 'frame.count': 'INTEGER', 'no.of.channels': 'INTEGER',
                                         'path': 'TEXT PRIMARY KEY', 'pixel.resolution': 'REAL', 'x.pixels': 'INTEGER',
                                         'x.voltage': 'REAL', 'y.pixels': 'INTEGER', 'y.voltage': 'REAL'})

    def testAsDict(self):
        pass


if __name__ == '__main__':
    unittest.main()
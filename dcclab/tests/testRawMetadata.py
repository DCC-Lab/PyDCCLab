from dcclab import RAWMetadata as mtdt
import env
import unittest
import os


class TestRawMetadata(env.DCCLabTestCase):
    def setUp(self) -> None:
        self.rawPath = os.path.join(str(self.dataDir), '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_XYT.raw')
        self.iniPath = os.path.join(str(self.dataDir), '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_XYT.ini')
        self.xmlPath = os.path.join(str(self.dataDir), '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_OME.xml')
        with open(self.iniPath, 'w') as file:
            file.write('[]\n')
            file.write('Test File\n')

        with open(self.xmlPath, 'w') as file:
            file.write('<TEST>\n')
            file.write('\t<items>\n')
            file.write('\t</items>\n')
            file.write('</TEST>\n')

    def tearDown(self) -> None:
        os.remove(self.iniPath)
        os.remove(self.xmlPath)
        pass

    def testFileName(self):
        metadata = mtdt(self.rawPath)
        self.assertEqual(metadata.fileName, '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_XYT')

    def testIniPath(self):
        metadata = mtdt(self.rawPath)
        self.assertEqual(metadata.iniPath, self.iniPath)

    def testIniPathLineShifted(self):
        filePath = os.path.join(str(self.dataDir),
                                '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_XYT.lineshifted.raw')
        metadata = mtdt(filePath)
        self.assertEqual(metadata.iniPath, self.iniPath)

    def testXmlPath(self):
        metadata = mtdt(self.rawPath)
        self.assertEqual(metadata.xmlPath, self.xmlPath)

    def testXmlPathLineShifted(self):
        filePath = os.path.join(str(self.dataDir),
                                '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_XYT.lineshifted.raw')
        metadata = mtdt(filePath)
        self.assertEqual(metadata.xmlPath, self.xmlPath)

    def testDate(self):
        metadata = mtdt(self.rawPath)
        self.assertEqual('2019-01-01 12:12:12', metadata.date)

    def testReadIniFile(self):
        metadata = mtdt(self.rawPath)
        self.assertTrue(metadata.readIniFile())




if __name__ == '__main__':
    unittest.main()
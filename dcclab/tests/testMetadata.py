from dcclab import Metadata
from shutil import copyfile
import env
import unittest
import os
import xlwt


class TestMetadata(env.DCCLabTestCase):
    def setUp(self):
        # Creating specific directories used for research groups.
        self.pomDir = os.path.join(str(self.dataDir), 'POM')
        self.pdkDir = os.path.join(str(self.dataDir), 'PDK')
        if not os.path.exists(self.pomDir):
            os.mkdir(self.pomDir)
        if not os.path.exists(self.pdkDir):
            os.mkdir(self.pdkDir)

        # Copying a .czi file to the right folder.
        self.cziPath = os.path.join(self.pomDir, 'testCziFile.czi')
        copyfile(os.path.join(str(self.dataDir), 'testCziFile.czi'), self.cziPath)
        self.rawPath = os.path.join(self.pdkDir, '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_XYT.raw')
        copyfile(os.path.join(str(self.dataDir), 'testMovie.raw'), self.rawPath)

        # Creating other test files needed.
        self.csvPath = os.path.join(self.pomDir, 'unittest.csv')
        self.xlsxPath = os.path.join(self.pdkDir, 'unittest.xlsx')
        self.iniPath = os.path.join(self.pdkDir, '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_XYT.ini')
        with open(self.iniPath, 'w') as file:
            file.write('[_]\nTest_File = This is a test file\nno.of.channels = 1.000000000000\nblank_line = blank\n'
                       'frame.count = 1000.000000000000\n\nx.pixels = 1024.000000000000\ny.pixels = 512.000000000000\n'
                       'x.voltage = 5.000000000000\ny.voltage = 1.250000000000\n\nwrong.line = bleh\n'
                       'pixel.resolution = 5.000000000000\nLaser.Power = 21.500000000000\n')

        with open(self.csvPath, 'w') as file:
            file.write('field_1,field_2,field_3\n')
            file.write('INTEGER,REAL,TEXT\n')
            file.write('100,0.123,apple\n')
            file.write('200,0.456,orange\n')

        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('test_1')
        sheet.write(0, 0, 'test_column_1')
        sheet.write(0, 1, 'test_column_2')
        sheet.write(0, 2, 'file_path')
        sheet.write(1, 0, 'abcd')
        sheet.write(1, 1, '1234')
        sheet.write(1, 2, '\\test\\testing\\testerinoo')
        sheet = workbook.add_sheet('test_2')
        sheet.write(0, 0, 'test_id_1')
        sheet.write(0, 1, 'file_path')
        sheet.write(1, 0, '01')
        sheet.write(1, 1, '\\test\\01')
        sheet.write(2, 0, '02')
        sheet.write(2, 1, '\\test\\02')
        workbook.save(self.xlsxPath)

    def tearDown(self) -> None:
        if os.path.exists(self.csvPath):
            os.remove(self.csvPath)
        if os.path.exists(self.xlsxPath):
            os.remove(self.xlsxPath)
        if os.path.exists(self.cziPath):
            os.remove(self.cziPath)
        if os.path.exists(self.rawPath):
            os.remove(self.rawPath)
        if os.path.exists(self.iniPath):
            os.remove(self.iniPath)

        os.rmdir(self.pomDir)
        os.rmdir(self.pdkDir)

    def testWrongFileType(self):
        wrongFile = os.path.join(self.pomDir, 'test.gif')
        copyfile(os.path.join(str(self.dataDir), 'test.gif'), wrongFile)
        with self.assertRaises(TypeError): Metadata(wrongFile)
        os.remove(wrongFile)

    def testNoFile(self):
        noFile = os.path.join(self.pomDir, 'nonexsitant.file')
        with self.assertRaises(ValueError): Metadata(noFile)

    def testValidateResearchGroupPOM(self):
        mtdt = Metadata(self.cziPath)
        self.assertEqual(mtdt.validateResearchGroup(), 'POM')

    def testValidateResearchGroupPDK(self):
        mtdt = Metadata(self.xlsxPath)
        self.assertEqual(mtdt.validateResearchGroup(), 'PDK')

    def testValidateResearchGroupValueError(self):
        mtdt = Metadata(self.cziPath)
        noGroup = os.path.join(str(self.dataDir), 'nonexsitant.file')
        mtdt.path = noGroup
        with self.assertRaises(ValueError): mtdt.validateResearchGroup()

    def testFileTypeIsCzi(self):
        mtdt = Metadata(self.cziPath)
        self.assertEqual(mtdt.metaType, 'CZI')

    def testFileTypeIsCsv(self):
        mtdt = Metadata(self.csvPath)
        self.assertEqual(mtdt.metaType, 'CSV')

    def testFileTypeIsXlsx(self):
        mtdt = Metadata(self.xlsxPath)
        self.assertEqual(mtdt.metaType, 'XLSX')

    def testFileTypeIsRAW(self):
        mtdt = Metadata(self.rawPath)
        self.assertEqual(mtdt.metaType, 'RAW')

    def testMetadataCZI(self):
        mtdt = Metadata(self.cziPath)
        self.assertTrue(mtdt.metadata)

    def testMetadataCSV(self):
        mtdt = Metadata(self.csvPath)
        self.assertTrue(mtdt.metadata)

    def testMetadataXLSX(self):
        mtdt = Metadata(self.xlsxPath)
        self.assertTrue(mtdt.metadata)

    def testMetadataRAW(self):
        mtdt = Metadata(self.rawPath)
        self.assertTrue(mtdt.metadata)

    def testChannelsCZI(self):
        mtdt = Metadata(self.cziPath)
        self.assertTrue(mtdt.channels)

    def testChannelsCSV(self):
        mtdt = Metadata(self.csvPath)
        self.assertFalse(mtdt.channels)

    def testChannelsXLSX(self):
        mtdt = Metadata(self.xlsxPath)
        self.assertFalse(mtdt.channels)

    def testChannelsRAW(self):
        mtdt = Metadata(self.rawPath)
        self.assertFalse(mtdt.channels)

    def testKeysCZI(self):
        mtdt = Metadata(self.cziPath)
        self.assertTrue(mtdt.keys)

    def testKeysCSV(self):
        mtdt = Metadata(self.csvPath)
        self.assertTrue(mtdt.keys)

    def testKeysXLSX(self):
        mtdt = Metadata(self.xlsxPath)
        self.assertTrue(mtdt.keys)

    def testKeysRAW(self):
        mtdt = Metadata(self.rawPath)
        self.assertTrue(mtdt.keys)


if __name__ == '__main__':
    unittest.main()

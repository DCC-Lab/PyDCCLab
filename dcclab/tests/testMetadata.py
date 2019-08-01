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

        # Creating other test files needed.
        self.csvPath = os.path.join(self.pomDir, 'unittest.csv')
        self.xlsxPath = os.path.join(self.pdkDir, 'unittest.xlsx')

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
        os.remove(self.csvPath)
        os.remove(self.xlsxPath)
        os.remove(self.cziPath)
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

    def testResearchGroupIsPOM(self):
        mtdt = Metadata(self.cziPath)
        self.assertEqual(mtdt.findResearchGroup(self.cziPath), 'POM')

    def testResearchGroupIsPDK(self):
        mtdt = Metadata(self.xlsxPath)
        self.assertEqual(mtdt.findResearchGroup(self.xlsxPath), 'PDK')

    def testResearchGroupIsFalse(self):
        mtdt = Metadata(self.cziPath)
        noGroup = os.path.join(str(self.dataDir), 'nonexsitant.file')
        self.assertFalse(mtdt.findResearchGroup(noGroup))

    def testFileTypeIsCzi(self):
        mtdt = Metadata(self.cziPath)
        self.assertEqual(mtdt.metaType, 'CZI')

    def testFileTypeIsCsv(self):
        mtdt = Metadata(self.csvPath)
        self.assertEqual(mtdt.metaType, 'CSV')

    def testFileTypeIsXlsx(self):
        mtdt = Metadata(self.xlsxPath)
        self.assertEqual(mtdt.metaType, 'XLSX')

    def testMetadataCZI(self):
        mtdt = Metadata(self.cziPath)
        self.assertTrue(mtdt.metadata)

    def testMetadataCSV(self):
        mtdt = Metadata(self.csvPath)
        self.assertTrue(mtdt.metadata)

    def testMetadataXLSX(self):
        mtdt = Metadata(self.xlsxPath)
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

    def testKeysCZI(self):
        mtdt = Metadata(self.cziPath)
        self.assertTrue(mtdt.keys)

    def testKeysCSV(self):
        mtdt = Metadata(self.csvPath)
        self.assertTrue(mtdt.keys)

    def testKeysXlsx(self):
        mtdt = Metadata(self.xlsxPath)
        self.assertTrue(mtdt.keys)


if __name__ == '__main__':
    unittest.main()

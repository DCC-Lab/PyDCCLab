import env
from dcclab import Metadata
from pathlib import Path, PureWindowsPath
import tempfile
import unittest
import os


class TestMetadata(env.DCCLabTestCase):
    def setUp(self):
        self.cziPath = Path(self.dataDir / 'testCziFile.czi')
        self.csvPath = Path(self.dataDir / 'unittest.csv')

        with open(self.csvPath, 'w') as file:
            file.write('field_1,field_2,field_3\n')
            file.write('INTEGER,REAL,TEXT\n')
            file.write('100,0.123,apple\n')
            file.write('200,0.456,orange\n')

    def testWrongFileType(self):
        wrongFile = Path(self.dataDir / 'test.db')
        with self.assertRaises(TypeError): Metadata(wrongFile)

    def testNoFile(self):
        noFile = Path(self.dataDir / 'nonexistant.file')
        with self.assertRaises(ValueError): Metadata(noFile)

    def testFileTypeIsCzi(self):
        mtdt = Metadata(self.cziPath)
        self.assertEqual(mtdt.metaType, 'CZI')

    def testFileTypeIsCsv(self):
        mtdt = Metadata(self.csvPath)
        self.assertEqual(mtdt.metaType, 'CSV')

    def testMetadataCZI(self):
        mtdt = Metadata(self.cziPath)
        self.assertTrue(mtdt.metadata)

    def testMetadataCSV(self):
        mtdt = Metadata(self.csvPath)
        self.assertTrue(mtdt.metadata)

    def testChannelsCZI(self):
        mtdt = Metadata(self.cziPath)
        self.assertTrue(mtdt.channels)

    def testChannelsCSV(self):
        mtdt = Metadata(self.csvPath)
        self.assertFalse(mtdt.channels)

    def testKeysCZI(self):
        mtdt = Metadata(self.cziPath)
        self.assertTrue(mtdt.keys)

    def testKeysCSV(self):
        mtdt = Metadata(self.csvPath)
        self.assertTrue(mtdt.keys)


if __name__ == '__main__':
    unittest.main()

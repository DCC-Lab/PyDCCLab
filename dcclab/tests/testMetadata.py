from dcclab import Metadata
from dcclab import CZIMetadata
import unittest
import os


class TestMetadata(unittest.TestCase):
    def setUp(self):
        self.directory = os.path.dirname(__file__)
        self.cziPath = os.path.join(self.directory, 'testCziFile.czi')
        self.csvPath = os.path.join(self.directory, 'unittest.csv')

        with open(self.csvPath, 'w') as file:
            file.write('field_1,field_2,field_3\n')
            file.write('INTEGER,REAL,TEXT\n')
            file.write('100,0.123,apple\n')
            file.write('200,0.456,orange\n')

    def tearDown(self):
        os.remove(self.csvPath)

    def testWrongFileType(self):
        wrongFile = os.path.join(self.directory, 'test.db')
        with self.assertRaises(TypeError): Metadata(wrongFile)

    def testNoFile(self):
        noFile = os.path.join(self.directory, 'nonexistant.file')
        with self.assertRaises(ValueError): Metadata(noFile)

    def testCziFile(self):
        mtdt = Metadata(self.cziPath)
        self.assertEqual(mtdt.metaType, 'CZI')

    def testCsvFile(self):
        mtdt = Metadata(self.csvPath)
        self.assertEqual(mtdt.metaType, 'CSV')


if __name__ == '__main__':
    unittest.main()

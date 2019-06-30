import env
from dcclab import CSVMetadata as mtdt
import unittest
import os


class TestCsvMetadata(env.dcclabTestCase):
    def setUp(self) -> None:
        self.directory = self.dataDir
        self.filePath = os.path.join(self.directory, 'unittest.csv')

        with open(self.filePath, 'w') as file:
            file.write('field_1,field_2,field_3\n')
            file.write('INTEGER,REAL,TEXT\n')
            file.write('100,0.123,apple\n')
            file.write('200,0.456,orange\n')

    def tearDown(self) -> None:
        os.remove(self.filePath)

    def testHeader(self):
        metadata = mtdt(self.filePath)
        header = metadata.header
        self.assertEqual(header[0], 'field_1,field_2,field_3\n')

    def testBody(self):
        metadata = mtdt(self.filePath)
        body = metadata.body
        self.assertEqual(body[0], '100,0.123,apple\n')

    def testKeys(self):
        metadata = mtdt(self.filePath)
        keys = metadata.keys['unittest']
        self.assertEqual(keys['field_1'], 'INTEGER')

    def testLines(self):
        metadata = mtdt(self.filePath)
        lines = metadata.lines
        self.assertEqual(lines[0], ['100', '0.123', 'apple'])

    def testAsDict(self):
        metadata = mtdt(self.filePath)
        dictio = metadata.asDict
        self.assertEqual(dictio[0]['field_1'], '100')


if __name__ == '__main__':
    unittest.main()
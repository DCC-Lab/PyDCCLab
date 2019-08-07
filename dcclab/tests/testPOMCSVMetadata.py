from dcclab import POMCSVMetadata as mtdt
import env
import unittest
import os


class TestPOMCSVMetadata(env.DCCLabTestCase):
    def setUp(self) -> None:
        self.csvPath = os.path.join(str(self.dataDir), 'unittest.csv')

        with open(self.csvPath, 'w') as file:
            file.write('field_1,field_2,path\n')
            file.write('INTEGER,REAL,TEXT\n')
            file.write('100,0.123,apple\n')
            file.write('200,0.456,orange\n')

        self.scsvPath = os.path.join(str(self.dataDir), 'unittest.scsv')
        with open(self.scsvPath, 'w') as file:
            file.write('field_1;field_2;path\n')
            file.write('INTEGER;REAL;TEXT\n')
            file.write('100;0.123;apple\n')
            file.write('200;0.456;orange\n')

    def tearDown(self) -> None:
        os.remove(self.csvPath)
        os.remove(self.scsvPath)

    def testColumnsCSV(self):
        metadata = mtdt(self.csvPath)
        self.assertEqual(metadata.columns, ['field_1', 'field_2', 'path'])

    def testColumnsSCSV(self):
        metadata = mtdt(self.scsvPath)
        self.assertEqual(metadata.columns, ['field_1', 'field_2', 'path'])

    def testTypesCSV(self):
        metadata = mtdt(self.csvPath)
        self.assertEqual(metadata.types, ['INTEGER', 'REAL', 'TEXT'])

    def testTypesSCSV(self):
        metadata = mtdt(self.scsvPath)
        self.assertEqual(metadata.types, ['INTEGER', 'REAL', 'TEXT'])

    def testTypesNoTypesCSV(self):
        self.csvPath = os.path.join(str(self.dataDir), 'unittest.csv')
        with open(self.csvPath, 'w') as file:
            file.write('field_1,field_2,path\n')
            file.write('100,0.123,apple\n')
            file.write('200,0.456,orange\n')

        metadata = mtdt(self.csvPath)
        self.assertEqual(metadata.types, ['TEXT', 'TEXT', 'TEXT PRIMARY KEY'])

    def testTypesNoTypesSCSV(self):
        self.scsvPath = os.path.join(str(self.dataDir), 'unittest.scsv')
        with open(self.scsvPath, 'w') as file:
            file.write('field_1,field_2,path\n')
            file.write('100,0.123,apple\n')
            file.write('200,0.456,orange\n')

        metadata = mtdt(self.scsvPath)
        self.assertEqual(metadata.types, ['TEXT', 'TEXT', 'TEXT PRIMARY KEY'])

    def testBodyCSV(self):
        metadata = mtdt(self.csvPath)
        body = metadata.body
        self.assertEqual(body[0], '100,0.123,apple\n')

    def testBodySCSV(self):
        metadata = mtdt(self.scsvPath)
        body = metadata.body
        self.assertEqual(body[0], '100,0;123;apple\n')

    def testKeysCSV(self):
        metadata = mtdt(self.csvPath)
        keys = metadata.keys['unittest']
        self.assertEqual(keys['field_1'], 'INTEGER')

    def testKeysSCSV(self):
        metadata = mtdt(self.scsvPath)
        keys = metadata.keys['unittest']
        self.assertEqual(keys['field_1'], 'INTEGER')

    def testLinesCSV(self):
        metadata = mtdt(self.csvPath)
        lines = metadata.lines
        self.assertEqual(lines[0], ['100', '0.123', 'apple'])

    def testLinesSCSV(self):
        metadata = mtdt(self.scsvPath)
        lines = metadata.lines
        self.assertEqual(lines[0], ['100', '0.123', 'apple'])

    def testAsDictCSV(self):
        metadata = mtdt(self.csvPath)
        dictio = metadata.asDict
        self.assertEqual(dictio[0]['field_1'], '100')

    def testAsDictSCSV(self):
        metadata = mtdt(self.scsvPath)
        dictio = metadata.asDict
        self.assertEqual(dictio[0]['field_1'], '100')


if __name__ == '__main__':
    unittest.main()
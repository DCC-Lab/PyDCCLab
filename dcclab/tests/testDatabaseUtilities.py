from dcclab import appendToZip, findFiles
from zipfile import ZipFile
import os
import unittest
import re
import env
import tempfile


class TestDatabaseUtilities(env.DCCLabTestCase):
    def testFindFilesFilesFound(self):
        directory = os.path.join(self.moduleDir, 'dcclab', 'database')
        self.assertTrue(findFiles(directory, 'py'))

    def testFindFilesNothingFound(self):
        directory = os.path.join(self.moduleDir, 'dcclab', 'database')
        self.assertFalse(findFiles(directory, 'czi'))

    def testRegularExpressionsExtension(self):
        string = 'trucpatente.py'
        extension = 'py'
        self.assertTrue(re.search(r'\.{}$'.format(extension), string, re.IGNORECASE))

    def testRegularExpressionsMoreComplexExtension(self):
        string = 'someFile.tar.gz'
        extension = 'tar.gz'
        self.assertTrue(re.search(r'\.{}$'.format(extension), string, re.IGNORECASE))

    def testAppendToZip(self):
        testZip = self.tmpFile('test.zip')
        testFile1 = self.tmpFile('test1.txt')
        testFile2 = self.tmpFile('test2.csv')
        testFile3 = self.tmpFile('test3.jpg')
        files = [testFile1, testFile2, testFile3]

        # function to test
        for file in files:
            appendToZip(file, testZip)

        with ZipFile(testZip, 'r') as zeep:
            self.assertTrue(zeep.namelist())


if __name__ == '__main__':
    unittest.main()

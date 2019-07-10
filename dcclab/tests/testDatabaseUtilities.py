from dcclab import appendToZip, findFiles
from zipfile import ZipFile
import os
import unittest
import re
import env


class TestDatabaseUtilities(env.DCCLabTestCase):
    def testFindFilesSomethingFound(self):
        directory = os.path.join(self.moduleDir, 'dcclab', 'database')
        self.assertTrue(findFiles(directory, 'py'))

    def testFindFilesNothingFound(self):
        directory = os.path.join(self.moduleDir, 'dcclab', 'database')
        self.assertFalse(findFiles(directory, 'czi'))

    def testFindFilesFolderDoesntExist(self):
        directory = os.path.join(self.moduleDir, 'thisFolderDoesntExist')
        self.assertFalse(findFiles(directory, 'py'))

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
        testFile2 = self.tmpFile('test2.txt')
        testFile3 = self.tmpFile('test3.txt')
        files = [testFile1, testFile2, testFile3]

        for file in files:
            with open(file, 'w') as write:
                write.write('This is a test line.')

            appendToZip(file, testZip)

        with ZipFile(testZip, 'r') as zeep:
            self.assertTrue(zeep.namelist())


if __name__ == '__main__':
    unittest.main()

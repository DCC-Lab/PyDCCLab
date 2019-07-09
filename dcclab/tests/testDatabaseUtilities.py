from dcclab import appendToZip, findFolderInPath, findFiles
import os
import fnmatch
import unittest
import re
import env


class TestDatabaseUtilities(env.DCCLabTestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def testFnmatch(self):
        self.assertTrue(fnmatch.fnmatch('test.tar.gz', '*.tar.gz'))

    #@unittest.skipIf(os.name == 'posix', reason='Fails on posix.')
    def testFnmatchUppercase(self):
        self.assertTrue(fnmatch.fnmatch('test.TXT', '*.[tT][xX][tT]'))

    #@unittest.skipIf(os.name == 'posix', reason='Fails on posix.')
    def testFnmatchUpperAndLowerCase(self):
        self.assertTrue(fnmatch.fnmatch('test.ThIsIsAtEsT', '*.thisisatest'))

    def testFindFiles(self):
        dir = os.path.join(self.moduleDir, 'dcclab', 'database')
        self.assertTrue(findFiles(dir, 'py'))
        self.assertFalse(findFiles(dir, 'czi'))

    def testRegularExpressions(self):
        file = 'truc.py'
        extension = 'py'
        print(re.search(r'\.{}$'.format(extension), file, re.IGNORECASE))


if __name__ == '__main__':
    unittest.main()

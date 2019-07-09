from dcclab import findFilesOS, appendToZip, findFolderInPath, findFiles
import os
import time
import fnmatch
import unittest
import env


class TestDatabaseUtilities(env.DCCLabTestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def testFnmatch(self):
        self.assertTrue(fnmatch.fnmatch('test.tar.gz', '*.tar.gz'))

    def testFnmatchUppercase(self):
        self.assertTrue(fnmatch.fnmatch('test.TXT', '*.txt'))

    def testFnmatchUpperAndLowerCase(self):
        self.assertTrue(fnmatch.fnmatch('test.ThIsIsAtEsT', '*.thisisatest'))

    def testFindFiles(self):
        dir = os.path.join(self.moduleDir, 'dcclab', 'POM', 'injection AAV')
        file = open('testWalkAndRecursive.txt', 'w')
        file.write('>>>>>>>>>BEGIN TESt\n')
        for i in range(5):
            file.write('>>>>BEGIN SEARCH (OS WALK)\n')
            begin = time.perf_counter()
            listOfFiles = findFilesOS(dir, '*.czi')
            file.write('{} files found.'.format(len(listOfFiles)))
            file.write('>>>>END SEARCH (OS WALK)\n')
            file.write('Took {}\n'.format(time.perf_counter() - begin))

        for i in range(5):
            file.write('>>>>BEGIN SEARCH (RECURSIVE)\n')
            begin = time.perf_counter()
            listOfFiles = findFiles(dir, '*.czi')
            file.write('{} files found.'.format(len(listOfFiles)))
            file.write('>>>>END SEARCH (RECURSIVE)\n')
            file.write('Took {}\n'.format(time.perf_counter() - begin))
        file.write('>>>>>>>>>END TEST\n')
        file.close()


if __name__ == '__main__':
    unittest.main()
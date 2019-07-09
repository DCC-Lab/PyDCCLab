from dcclab import findFilesOS, appendToZip, findFolderInPath
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
        for i in range(5):
            print('>>>>BEGIN SEARCH OS WALK')
            begin = time.clock()
            listOfFiles = findFilesOS(r'A:\BD-IA_POMMountingPoint\BigData-ImageAnalysis\dcclab\POM', '*.czi')
            print('>>>>END SEARCH OS WALK')
            print('Took {} '.format(time.clock() - begin))
            print(len(listOfFiles))

        for i in range(5):
            print('>>>>BEGIN SEARCH RECURSIVE')
            begin = time.clock()
            listOfFiles = findFilesOS(r'A:\BD-IA_POMMountingPoint\BigData-ImageAnalysis\dcclab\POM', '*.czi')
            print('>>>>END SEARCH RECURSIVE')
            print('Took {} '.format(time.clock() - begin))
            print(len(listOfFiles))
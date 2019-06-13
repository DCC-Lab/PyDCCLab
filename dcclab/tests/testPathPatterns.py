import env
from dcclab import *

import unittest
import numpy as np
import re

class TestPatterns(unittest.TestCase):

    def testInit(self):
        self.assertIsNotNone(PathPattern('abc'))

    def testInitInvalid(self):
        with self.assertRaises(Exception):
            PathPattern('(abc')

    def testInitNoCaptureGroups(self):
        pat = PathPattern('abc')
        self.assertFalse(pat.hasCaptureGroups)

    def testInitWithCaptureGroups(self):
        pat = PathPattern(r'abc(\d)')
        self.assertTrue(pat.hasCaptureGroups)

    def testFindCaptureGroups(self):
        match = re.search(r"(\(.*\))", "abc(daniel)def")
        self.assertIsNotNone(match)
        self.assertTrue(len(match.groups()) == 1)
        strings = re.findall(r"(\(.+?\))", "abc(daniel)(def)")
        self.assertTrue(len(strings) == 2)

    def testInitWith0CaptureGroup(self):
        pat = PathPattern(r'abckjhasd')
        self.assertTrue(pat.numberOfCaptureGroups == 0)

    def testInitWith1CaptureGroup(self):
        pat = PathPattern(r'abc(\d)')
        self.assertTrue(pat.numberOfCaptureGroups == 1)

    def testInitWith2CaptureGroups(self):
        pat = PathPattern(r'abc(\d)...(lkha)')
        self.assertTrue(pat.numberOfCaptureGroups == 2)

    def testInitWith3CaptureGroups(self):
        pat = PathPattern(r'abc(\d)...(lkha)bla(asd)')
        self.assertTrue(pat.numberOfCaptureGroups == 3)

    def testInitWith1PythonFormatString(self):
        pat = PathPattern(r'abl{0}')
        self.assertTrue(pat.isPythonFormatString)
        self.assertTrue(pat.numberOfFormatGroups == 1)

    def testInitWith2PythonFormatString(self):
        pat = PathPattern(r'abl{0}blabal{1:03f}')
        self.assertTrue(pat.isPythonFormatString)
        self.assertTrue(pat.numberOfFormatGroups == 2)

    def testInitWithoutPythonFormatString(self):
        pat = PathPattern(r'abl')
        self.assertFalse(pat.isPythonFormatString)
        self.assertTrue(pat.numberOfFormatGroups == 0)

    def testIsWritePattern(self):
        pat = PathPattern(r'abl{0}blabal{1:03f}')
        self.assertTrue(pat.isWritePattern)
        self.assertFalse(pat.isReadPattern)

    def testIsReadPattern(self):
        pat = PathPattern(r'abl(\d)')
        self.assertTrue(pat.isReadPattern)
        self.assertFalse(pat.isWritePattern)

    def testDirectory(self):
        pat = PathPattern(r'/Users/dccote/test.tiff')
        self.assertEqual(pat.directory, "/Users/dccote")

    def testEmptyDirectory(self):
        pat = PathPattern(r'test.tiff')
        self.assertEqual(pat.directory, "./")

    def testBasename(self):
        pat = PathPattern(r'/Users/dccote/test.tiff')
        self.assertEqual(pat.basePattern, "test.tiff")

    def testBasenameWithFormats(self):
        pat = PathPattern(r'/Users/dccote/test-{0}.tiff')
        self.assertEqual(pat.basePattern, r"test-{0}.tiff")

    def testBasenameWithCapture(self):
        pat = PathPattern(r'/Users/dccote/test-(\d+).tiff')
        self.assertEqual(pat.basePattern, r"test-(\d+).tiff")

    def testFindFiles(self):
        # Use this test directory
        pat = PathPattern(r'test.+\.py')
        files = pat.matchingFiles()
        self.assertTrue(len(files) != 0)

    def testFailedFindFilesWritePattern(self):
        # Use this test directory
        pat = PathPattern(r'test.{0}.py')
        with self.assertRaises(ValueError):
            files = pat.matchingFiles()

    def testFindFilesCheckExist(self):
        # Use this test directory
        pat = PathPattern(r'test.+\.py')
        files = pat.matchingFiles()
        for filePath in files:
            self.assertTrue(os.path.exists(filePath))

    def testFileExpansion(self):
        pat = PathPattern(r'test-{0}.py')
        for i in range(4):
            self.assertEqual(pat.filePathWithIndex(i), "test-{0}.py".format(i))

    def testFileExpansionWithFancyFormat(self):
        pat = PathPattern(r'test-{0:03d}.py')
        self.assertEqual(pat.filePathWithIndex(1), "test-001.py")
        for i in range(4):
            self.assertEqual(pat.filePathWithIndex(i), "test-{0:03d}.py".format(i))

if __name__ == '__main__':
    unittest.main()

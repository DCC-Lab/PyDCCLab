import env
import unittest
from dcclab.cziFile import CZIFile
from dcclab.DCCExceptions import *
import numpy as np


class TestConstructor(unittest.TestCase):

    def testValidCziFile(self):
        try:
            CZIFile("testCziFileTwoChannels.czi")
        except InvalidFileFormatException:
            self.fail()

    def testInvalidNotCzi(self):
        with self.assertRaises(InvalidFileFormatException):
            CZIFile("testNotCziFile.jpg")

    def testInvalidFileNotFound(self):
        with self.assertRaises(FileNotFoundError):
            CZIFile("FileNotFound.czi")


class TestProperties(unittest.TestCase):

    def testNumberOfChannels(self):
        self.assertEqual(CZIFile("testCziFileTwoChannels.czi").numberOfChannels, 2)

    def testChannelMapsLength(self):
        self.assertEqual(len(CZIFile("testCziFileTwoChannels.czi").channelMaps), 2)

    def testChannelMapsKeys(self):
        czi = CZIFile("testCziFileTwoChannels.czi")
        keysChannel1 = list(czi.channelMaps[0].keys())
        keysChannel2 = list(czi.channelMaps[1].keys())
        supposedKeys = [(range(0, 1936), range(0, 1460), None, None)]
        self.assertTrue(keysChannel1 == supposedKeys and keysChannel2 == supposedKeys)

    def testChannelMapsValues(self):
        #todo Test with small czi file to check if values are the right ones
        pass


if __name__ == '__main__':
    unittest.main()

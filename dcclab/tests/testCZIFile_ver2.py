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
        czi = CZIFile("testTinyCzi.czi")
        pixelsValueChannelOne = np.array([[119, 142], [134, 118], [122, 125]])
        pixelsValueChannelTwo = np.array([[68, 72], [77, 72], [57, 69]])
        key = (range(0, 2), range(0, 3), None, None)
        self.assertTrue(
            np.array_equal(czi.channelMaps[0][key], pixelsValueChannelOne) and np.array_equal(czi.channelMaps[1][key],
                                                                                              pixelsValueChannelTwo))
    def testChannelMapsAllSameKeys(self):
        #todo test if keys from every channel are the same
        pass


if __name__ == '__main__':
    unittest.main()

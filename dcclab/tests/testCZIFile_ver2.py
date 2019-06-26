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


    def testChannelMapsLength(self):
        self.assertEqual(len(CZIFile("testCziFileTwoChannels.czi").channelMaps), 2)

    def testChannelMapsKeys(self):
        czi = CZIFile("testCziFileTwoChannels.czi")
        keysChannel1 = list(czi.channelMaps[0].keys())
        keysChannel2 = list(czi.channelMaps[1].keys())
        supposedKeys = [(range(0, 1936), range(0, 1460), None, None, None)]
        self.assertTrue(keysChannel1 == supposedKeys and keysChannel2 == supposedKeys)

    def testChannelMapsValues(self):
        czi = CZIFile("testTinyCzi.czi")
        pixelsValueChannelOne = np.array([[119, 142], [134, 118], [122, 125]])
        pixelsValueChannelTwo = np.array([[68, 72], [77, 72], [57, 69]])
        key = (range(0, 2), range(0, 3), None, None, None)
        self.assertTrue(
            np.array_equal(czi.channelMaps[0][key], pixelsValueChannelOne) and np.array_equal(czi.channelMaps[1][key],
                                                                                              pixelsValueChannelTwo))

    def testChannelMapsAllSameKeys(self):
        czi = CZIFile("testCziFileThreeChannelsFourTiles.czi")
        channelMaps = czi.channelMaps
        self.assertTrue(channelMaps[0].keys() == channelMaps[1].keys() == channelMaps[2].keys())

    def testNumberOfChannels(self):
        czi3Channels = CZIFile("testCziFileThreeChannelsFourTiles.czi")
        czi2Channels = CZIFile("testCziFileTwoChannels.czi")
        cziOneChannel = CZIFile("testCziOneChannel.czi")
        czi0Channel = CZIFile("testCziFileYX0Axes.czi")
        self.assertTrue(czi3Channels.numberOfChannels == 3 and czi2Channels.numberOfChannels == 2
                        and cziOneChannel.numberOfChannels == 1 and czi0Channel.numberOfChannels == 0)


if __name__ == '__main__':
    unittest.main()

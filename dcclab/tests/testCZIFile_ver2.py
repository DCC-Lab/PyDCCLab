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

    def testTotalWidth(self):
        czi1936x1460 = CZIFile("testCziFileTwoChannels.czi")
        czi3790x2892 = CZIFile("testCziFileThreeChannelsFourTiles.czi")
        czi954x670 = CZIFile("testCziFileYX0Axes.czi")
        czi2x3 = CZIFile("testTinyCzi.czi")
        czi1525x905 = CZIFile("testCziThreeChannelsOneScene.czi")
        self.assertTrue(czi2x3.totalWidth == 2 and czi954x670.totalWidth == 954 and czi1525x905.totalWidth == 1525
                        and czi1936x1460.totalWidth == 1936 and czi3790x2892.totalWidth == 3790)

    def testTotalHeight(self):
        czi1936x1460 = CZIFile("testCziFileTwoChannels.czi")
        czi3790x2892 = CZIFile("testCziFileThreeChannelsFourTiles.czi")
        czi954x670 = CZIFile("testCziFileYX0Axes.czi")
        czi2x3 = CZIFile("testTinyCzi.czi")
        czi1525x905 = CZIFile("testCziThreeChannelsOneScene.czi")
        self.assertTrue(czi2x3.totalHeight == 3 and czi954x670.totalHeight == 670 and czi1525x905.totalHeight == 905
                        and czi1936x1460.totalHeight == 1460 and czi3790x2892.totalHeight == 2892)

    def testIsZStackNo(self):
        czi = CZIFile("testCziThreeChannelsOneScene.czi")
        self.assertFalse(czi.isZstack)

    def testIsZStackYes(self):
        # todo find file with zstack, timeserie (for another false)
        pass

    def testIsTimeSerieNo(self):
        czi = CZIFile("testCziThreeChannelsOneScene.czi")
        self.assertFalse(czi.isTimeSerie)

    def testIsTimeSerieYes(self):
        # todo find file with timeserie, zstack (for another false)
        pass

    def testIsSceneNo(self):
        czi = CZIFile("testCziFileYX0Axes.czi")
        self.assertFalse(czi.isScene)

    def testIsSceneYes(self):
        czi = CZIFile("testCziThreeChannelsOneScene.czi")
        self.assertTrue(czi.isScene)

    def testIsSceneNo2(self):
        # todo find file with timeserie/zstack for another false
        pass

    def testShape(self):
        czi1936x1460 = CZIFile("testCziFileTwoChannels.czi")
        czi3790x2892 = CZIFile("testCziFileThreeChannelsFourTiles.czi")
        czi954x670 = CZIFile("testCziFileYX0Axes.czi")
        czi2x3 = CZIFile("testTinyCzi.czi")
        czi1525x905 = CZIFile("testCziThreeChannelsOneScene.czi")
        self.assertTupleEqual(czi2x3.shape, (1, 2, 3, 2, 1))
        self.assertTupleEqual(czi954x670.shape, (670, 954, 3))
        self.assertTupleEqual(czi1525x905.shape, (1, 1, 3, 905, 1525, 1))
        self.assertTupleEqual(czi1936x1460.shape, (1, 2, 1460, 1936, 1))
        self.assertTupleEqual(czi3790x2892.shape, (1, 1, 3, 2892, 3790, 1))


if __name__ == '__main__':
    unittest.main()

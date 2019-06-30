import env
import unittest
from dcclab.cziFile import CZIFile
from dcclab.DCCExceptions import *
import numpy as np
from pathlib import Path, PureWindowsPath

class TestConstructor(unittest.TestCase):

    def testValidCziFile(self):
        try:
            CZIFile(Path(env.dataDir / "testCziFileTwoChannels.czi"))
        except InvalidFileFormatException:
            self.fail()

    def testInvalidNotCzi(self):
        with self.assertRaises(InvalidFileFormatException):
            CZIFile(Path(env.dataDir / "testNotCziFile.jpg"))

    def testInvalidFileNotFound(self):
        with self.assertRaises(FileNotFoundError):
            CZIFile(Path(env.dataDir / "FileNotFound.czi"))


class TestProperties(unittest.TestCase):

    def testNumberOfChannels(self):
        czi3Channels = CZIFile(Path(env.dataDir / "testCziFileThreeChannelsFourTiles.czi"))
        czi2Channels = CZIFile(Path(env.dataDir / "testCziFileTwoChannels.czi"))
        cziOneChannel = CZIFile(Path(env.dataDir / "testCziOneChannel.czi"))
        czi0Channel = CZIFile(Path(env.dataDir / "testCziFileYX0Axes.czi"))
        self.assertEqual(czi3Channels.numberOfChannels, 3)
        self.assertEqual(czi2Channels.numberOfChannels, 2)
        self.assertEqual(cziOneChannel.numberOfChannels, 1)
        self.assertEqual(czi0Channel.numberOfChannels, 0)

    def testTotalWidth(self):
        czi1936x1460 = CZIFile(Path(env.dataDir / "testCziFileTwoChannels.czi"))
        czi3790x2892 = CZIFile(Path(env.dataDir / "testCziFileThreeChannelsFourTiles.czi"))
        czi954x670 = CZIFile(Path(env.dataDir / "testCziFileYX0Axes.czi"))
        czi2x3 = CZIFile(Path(env.dataDir / "testTinyCzi.czi"))
        czi1525x905 = CZIFile(Path(env.dataDir / "testCziThreeChannelsOneScene.czi"))
        self.assertEqual(czi2x3.totalWidth, 2)
        self.assertEqual(czi954x670.totalWidth, 954)
        self.assertEqual(czi1525x905.totalWidth, 1525)
        self.assertEqual(czi1936x1460.totalWidth, 1936)
        self.assertEqual(czi3790x2892.totalWidth, 3790)

    def testTotalHeight(self):
        czi1936x1460 = CZIFile(Path(env.dataDir / "testCziFileTwoChannels.czi"))
        czi3790x2892 = CZIFile(Path(env.dataDir / "testCziFileThreeChannelsFourTiles.czi"))
        czi954x670 = CZIFile(Path(env.dataDir / "testCziFileYX0Axes.czi"))
        czi2x3 = CZIFile(Path(env.dataDir / "testTinyCzi.czi"))
        czi1525x905 = CZIFile(Path(env.dataDir / "testCziThreeChannelsOneScene.czi"))
        self.assertEqual(czi2x3.totalHeight, 3)
        self.assertEqual(czi954x670.totalHeight, 670)
        self.assertEqual(czi1525x905.totalHeight, 905)
        self.assertEqual(czi1936x1460.totalHeight, 1460)
        self.assertEqual(czi3790x2892.totalHeight, 2892)

    def testIsZStackNo(self):
        czi = CZIFile(Path(env.dataDir / "testCziThreeChannelsOneScene.czi"))
        self.assertFalse(czi.isZstack)

    def testIsZStackYes(self):
        czi = CZIFile(Path(env.dataDir / "testCziZStack4.czi"))
        self.assertTrue(czi.isZstack)

    def testIsTimeSerieNo(self):
        czi = CZIFile(Path(env.dataDir / "testCziThreeChannelsOneScene.czi"))
        self.assertFalse(czi.isTimeSerie)

    def testIsTimeSerieNoDim1(self):
        # todo find file with timeserie dim 1
        pass

    def testIsSceneNo(self):
        czi = CZIFile(Path(env.dataDir / "testCziFileYX0Axes.czi"))
        self.assertFalse(czi.isScenes)

    def testIsSceneNoDim1(self):
        czi = CZIFile(Path(env.dataDir / "testCziThreeChannelsOneScene.czi"))
        self.assertFalse(czi.isScenes)

    def testIsScenesYes(self):
        czi = CZIFile(Path(env.dataDir / "testCziMultipleScenes.czi"))
        self.assertTrue(czi.isScenes)

    def testShape(self):
        czi1936x1460 = CZIFile(Path(env.dataDir / "testCziFileTwoChannels.czi"))
        czi3790x2892 = CZIFile(Path(env.dataDir / "testCziFileThreeChannelsFourTiles.czi"))
        czi954x670 = CZIFile(Path(env.dataDir / "testCziFileYX0Axes.czi"))
        czi2x3 = CZIFile(Path(env.dataDir / "testTinyCzi.czi"))
        czi1525x905 = CZIFile(Path(env.dataDir / "testCziThreeChannelsOneScene.czi"))
        self.assertTupleEqual(czi2x3.shape, (1, 2, 3, 2, 1))
        self.assertTupleEqual(czi954x670.shape, (670, 954, 3))
        self.assertTupleEqual(czi1525x905.shape, (1, 1, 3, 905, 1525, 1))
        self.assertTupleEqual(czi1936x1460.shape, (1, 2, 1460, 1936, 1))
        self.assertTupleEqual(czi3790x2892.shape, (1, 1, 3, 2892, 3790, 1))

    def testTileMapKeysOnlyTiles(self):
        czi3Channels = CZIFile(Path(env.dataDir / "testCziFileThreeChannelsFourTiles.czi"))
        keys = list(czi3Channels.tileMap.keys())
        supposedKeys = [(range(60, 1996), range(0, 1460), None, None, None, 0),
                        (range(60, 1996), range(0, 1460), None, None, None, 1),
                        (range(60, 1996), range(0, 1460), None, None, None, 2),
                        (range(1854, 3790), range(80, 1540), None, None, None, 0),
                        (range(1854, 3790), range(80, 1540), None, None, None, 1),
                        (range(1854, 3790), range(80, 1540), None, None, None, 2),
                        (range(1794, 3730), range(1432, 2892), None, None, None, 0),
                        (range(1794, 3730), range(1432, 2892), None, None, None, 1),
                        (range(1794, 3730), range(1432, 2892), None, None, None, 2),
                        (range(0, 1936), range(1352, 2812), None, None, None, 0),
                        (range(0, 1936), range(1352, 2812), None, None, None, 1),
                        (range(0, 1936), range(1352, 2812), None, None, None, 2)]
        self.assertListEqual(keys, supposedKeys)

    def testTileMapKeysOnlyOneTile(self):
        czi = CZIFile(Path(env.dataDir / "testCziOneChannel.czi"))
        keys = list(czi.tileMap.keys())
        supposedKeys = [(range(0, 857), range(0, 610), None, None, None, 0)]
        self.assertListEqual(keys, supposedKeys)

    def testTileMapKeysMultipleScenes(self):
        czi = CZIFile(Path(env.dataDir / "testCziMultipleScenes.czi"))
        keys = list(czi.tileMap.keys())
        supposedKeys = [(range(0, 447), range(0, 357), None, 1, None, 0),
                        (range(0, 447), range(0, 357), None, 1, None, 1),
                        (range(0, 447), range(0, 357), None, 0, None, 0),
                        (range(0, 447), range(0, 357), None, 0, None, 1)]
        self.assertListEqual(keys, supposedKeys)

    def testTileMapKeysZStack(self):
        czi = CZIFile(Path(env.dataDir / "testCziZStack4.czi"))
        keys = list(czi.tileMap.keys())
        supposedKeys = [(range(0, 61), range(0, 61), 0, None, None, 0), (range(0, 61), range(0, 61), 3, None, None, 0),
                        (range(0, 61), range(0, 61), 2, None, None, 1), (range(0, 61), range(0, 61), 2, None, None, 0),
                        (range(0, 61), range(0, 61), 0, None, None, 1), (range(0, 61), range(0, 61), 1, None, None, 1),
                        (range(0, 61), range(0, 61), 1, None, None, 0), (range(0, 61), range(0, 61), 3, None, None, 1)]
        self.assertListEqual(keys, supposedKeys)

    def testTileMapYX0None(self):
        czi = CZIFile(Path(env.dataDir / "testCziFileYX0Axes.czi"))
        self.assertIsNone(czi.tileMap)

    def testAxesYX0(self):
        czi = CZIFile(Path(env.dataDir / "testCziFileYX0Axes.czi"))
        self.assertEqual(czi.axes, "YX0")

    def testAxesBCZYX0(self):
        czi = CZIFile(Path(env.dataDir / "testCziZStack4.czi"))
        self.assertEqual(czi.axes, "BCZYX0")

    def testAxesBCYX0(self):
        czi = CZIFile(Path(env.dataDir / "testCziFileTwoChannels.czi"))
        self.assertEqual(czi.axes, "BCYX0")

    def testAxesBSCYX0(self):
        czi = CZIFile(Path(env.dataDir / "testCziThreeChannelsOneScene.czi"))
        self.assertEqual(czi.axes, "BSCYX0")


if __name__ == '__main__':
    unittest.main()

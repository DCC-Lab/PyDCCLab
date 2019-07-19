import env
import unittest
from dcclab.cziFile import CZIFile
from dcclab.DCCExceptions import *
import numpy as np
from pathlib import Path


class TestConstructor(env.DCCLabTestCase):

    def testValidCziFile(self):
        try:
            CZIFile(Path(self.dataDir / "testCziFileTwoChannels.czi"))
        except InvalidFileFormatException:
            self.fail()

    def testInvalidNotCzi(self):
        with self.assertRaises(InvalidFileFormatException):
            CZIFile(Path(self.dataDir / "testNotCziFile.jpg"))

    def testInvalidFileNotFound(self):
        with self.assertRaises(FileNotFoundError):
            CZIFile(Path(self.dataDir / "FileNotFound.czi"))

    def testInvalidZstackAndTimeSeries(self):
        with self.assertRaises(NotImplementedError):
            CZIFile(Path(self.dataDir / "testCziTSeries_ZStack.czi"))

    def testInvalidScenesAndTimeSeries(self):
        with self.assertRaises(NotImplementedError):
            CZIFile(Path(self.dataDir / "testCziTSeries_Scenes.czi"))

    def testInvalidScenesAndZStack(self):
        with self.assertRaises(NotImplementedError):
            CZIFile(Path(self.dataDir / "testCziScenes_ZStack.czi"))


class TestMethodsAndProperties(env.DCCLabTestCase):

    def testNumberOfChannels(self):
        czi3Channels = CZIFile(Path(self.dataDir / "testCziFileThreeChannelsFourTiles.czi"))
        czi2Channels = CZIFile(Path(self.dataDir / "testCziFileTwoChannels.czi"))
        cziOneChannel = CZIFile(Path(self.dataDir / "testCziOneChannel.czi"))
        czi0Channel = CZIFile(Path(self.dataDir / "testCziFileYX0Axes.czi"))
        self.assertEqual(czi3Channels.numberOfChannels, 3)
        self.assertEqual(czi2Channels.numberOfChannels, 2)
        self.assertEqual(cziOneChannel.numberOfChannels, 1)
        self.assertEqual(czi0Channel.numberOfChannels, 0)

    def testTotalWidth(self):
        czi1936x1460 = CZIFile(Path(self.dataDir / "testCziFileTwoChannels.czi"))
        czi3790x2892 = CZIFile(Path(self.dataDir / "testCziFileThreeChannelsFourTiles.czi"))
        czi954x670 = CZIFile(Path(self.dataDir / "testCziFileYX0Axes.czi"))
        czi2x3 = CZIFile(Path(self.dataDir / "testTinyCzi.czi"))
        czi1525x905 = CZIFile(Path(self.dataDir / "testCziThreeChannelsOneScene.czi"))
        self.assertEqual(czi2x3.totalWidth, 2)
        self.assertEqual(czi954x670.totalWidth, 954)
        self.assertEqual(czi1525x905.totalWidth, 1525)
        self.assertEqual(czi1936x1460.totalWidth, 1936)
        self.assertEqual(czi3790x2892.totalWidth, 3790)

    def testTotalHeight(self):
        czi1936x1460 = CZIFile(Path(self.dataDir / "testCziFileTwoChannels.czi"))
        czi3790x2892 = CZIFile(Path(self.dataDir / "testCziFileThreeChannelsFourTiles.czi"))
        czi954x670 = CZIFile(Path(self.dataDir / "testCziFileYX0Axes.czi"))
        czi2x3 = CZIFile(Path(self.dataDir / "testTinyCzi.czi"))
        czi1525x905 = CZIFile(Path(self.dataDir / "testCziThreeChannelsOneScene.czi"))
        self.assertEqual(czi2x3.totalHeight, 3)
        self.assertEqual(czi954x670.totalHeight, 670)
        self.assertEqual(czi1525x905.totalHeight, 905)
        self.assertEqual(czi1936x1460.totalHeight, 1460)
        self.assertEqual(czi3790x2892.totalHeight, 2892)

    def testIsZStackNo(self):
        czi = CZIFile(Path(self.dataDir / "testCziThreeChannelsOneScene.czi"))
        self.assertFalse(czi.isZstack)

    def testIsZStackYes(self):
        czi = CZIFile(Path(self.dataDir / "testCziZStack4.czi"))
        self.assertTrue(czi.isZstack)

    def testIsTimeSerieNo(self):
        czi = CZIFile(Path(self.dataDir / "testCziThreeChannelsOneScene.czi"))
        self.assertFalse(czi.isTimeSerie)

    def testIsTimeSerieNoDim1(self):
        # todo find file with timeserie dim 1
        pass

    def testIsSceneNo(self):
        czi = CZIFile(Path(self.dataDir / "testCziFileYX0Axes.czi"))
        self.assertFalse(czi.isScenes)

    def testIsSceneNoDim1(self):
        czi = CZIFile(Path(self.dataDir / "testCziThreeChannelsOneScene.czi"))
        self.assertFalse(czi.isScenes)

    def testIsScenesYes(self):
        czi = CZIFile(Path(self.dataDir / "testCziMultipleScenes.czi"))
        self.assertTrue(czi.isScenes)

    def testShape(self):
        czi1936x1460 = CZIFile(Path(self.dataDir / "testCziFileTwoChannels.czi"))
        czi3790x2892 = CZIFile(Path(self.dataDir / "testCziFileThreeChannelsFourTiles.czi"))
        czi954x670 = CZIFile(Path(self.dataDir / "testCziFileYX0Axes.czi"))
        czi2x3 = CZIFile(Path(self.dataDir / "testTinyCzi.czi"))
        czi1525x905 = CZIFile(Path(self.dataDir / "testCziThreeChannelsOneScene.czi"))
        self.assertTupleEqual(czi2x3.shape, (1, 2, 3, 2, 1))
        self.assertTupleEqual(czi954x670.shape, (670, 954, 3))
        self.assertTupleEqual(czi1525x905.shape, (1, 1, 3, 905, 1525, 1))
        self.assertTupleEqual(czi1936x1460.shape, (1, 2, 1460, 1936, 1))
        self.assertTupleEqual(czi3790x2892.shape, (1, 1, 3, 2892, 3790, 1))

    def testTileMapKeysOnlyTiles(self):
        czi3Channels = CZIFile(Path(self.dataDir / "testCziFileThreeChannelsFourTiles.czi"))
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
        czi = CZIFile(Path(self.dataDir / "testCziOneChannel.czi"))
        keys = list(czi.tileMap.keys())
        supposedKeys = [(range(0, 857), range(0, 610), None, None, None, 0)]
        self.assertListEqual(keys, supposedKeys)

    def testTileMapKeysMultipleScenes(self):
        czi = CZIFile(Path(self.dataDir / "testCziMultipleScenes.czi"))
        keys = list(czi.tileMap.keys())
        supposedKeys = [(range(0, 447), range(0, 357), None, 1, None, 0),
                        (range(0, 447), range(0, 357), None, 1, None, 1),
                        (range(0, 447), range(0, 357), None, 0, None, 0),
                        (range(0, 447), range(0, 357), None, 0, None, 1)]
        self.assertListEqual(keys, supposedKeys)

    def testTileMapKeysZStack(self):
        czi = CZIFile(Path(self.dataDir / "testCziZStack4.czi"))
        keys = list(czi.tileMap.keys())
        supposedKeys = [(range(0, 61), range(0, 61), 0, None, None, 0), (range(0, 61), range(0, 61), 3, None, None, 0),
                        (range(0, 61), range(0, 61), 2, None, None, 1), (range(0, 61), range(0, 61), 2, None, None, 0),
                        (range(0, 61), range(0, 61), 0, None, None, 1), (range(0, 61), range(0, 61), 1, None, None, 1),
                        (range(0, 61), range(0, 61), 1, None, None, 0), (range(0, 61), range(0, 61), 3, None, None, 1)]
        self.assertListEqual(keys, supposedKeys)

    def testTileMapYX0None(self):
        czi = CZIFile(Path(self.dataDir / "testCziFileYX0Axes.czi"))
        self.assertIsNone(czi.tileMap)

    def testAxesYX0(self):
        czi = CZIFile(Path(self.dataDir / "testCziFileYX0Axes.czi"))
        self.assertEqual(czi.axes, "YX0")

    def testAxesBCZYX0(self):
        czi = CZIFile(Path(self.dataDir / "testCziZStack4.czi"))
        self.assertEqual(czi.axes, "BCZYX0")

    def testAxesBCYX0(self):
        czi = CZIFile(Path(self.dataDir / "testCziFileTwoChannels.czi"))
        self.assertEqual(czi.axes, "BCYX0")

    def testAxesBSCYX0(self):
        czi = CZIFile(Path(self.dataDir / "testCziThreeChannelsOneScene.czi"))
        self.assertEqual(czi.axes, "BSCYX0")

    def testOriginalDType(self):
        czi = CZIFile(Path(self.dataDir / "testCziThreeChannelsOneScene.czi"))
        self.assertEqual(czi.originalDType, np.uint16)

    def testAllDataYX0(self):
        czi = CZIFile(Path(self.dataDir / "testCziYX0Tiny.czi"))
        allData = czi.allData()
        data = np.dstack((np.array([[7, 7], [6, 6]]), np.array([[46, 48], [51, 47]]), np.array([[32, 29], [33, 28]])))
        self.assertTrue(np.array_equal(allData, data))

    def testImageDataYX0Axes(self):
        try:
            czi = CZIFile(Path(self.dataDir / "testCziFileYX0Axes.czi"))
            self.assertIsNotNone(czi.imageData())
        except:
            self.fail("Exception raised.")

    def testImageDataMultipleImagesException(self):
        czi = CZIFile(Path(self.dataDir / "testCziMultipleScenes.czi"))
        with self.assertRaises(ValueError):
            czi.imageData()

    def testImageDataYX0Values(self):
        czi = CZIFile(Path(self.dataDir / "testCziYX0Tiny.czi"))
        values = np.dstack((np.array([[7, 7], [6, 6]]), np.array([[46, 48], [51, 47]]), np.array([[32, 29], [33, 28]])))
        self.assertTrue(np.array_equal(czi.imageData().asArray(), values.transpose((1, 0, 2))))

    def testImageDataBSCYX0Values(self):
        czi = CZIFile(Path(self.dataDir / "testCziBSCZY0Tiny.czi"))
        values = np.dstack((np.array([[596, 652], [622, 618]]), np.array([[1059, 1061], [1133, 1087]]),
                            np.array([[510, 511], [505, 497]])))
        self.assertTrue(np.array_equal(czi.imageData().asArray(), values.transpose((1, 0, 2))))

    def testImageData2DArrayTo3DArray(self):
        czi = CZIFile(Path(self.dataDir / "testCziOneChannel.czi"))
        self.assertTupleEqual(czi.imageData().shape, (857, 610, 1))

    def testScenesDataOneSceneNone(self):
        czi = CZIFile(Path(self.dataDir / "testCziThreeChannelsOneScene.czi"))
        self.assertIsNone(czi.scenesData())

    def testScenesDataValues(self):
        czi = CZIFile(Path(self.dataDir / "testCziFileTwoScenesTiny.czi"))
        values1 = np.dstack((np.array([[103, 101], [99, 86]]), np.array([[171, 190], [216, 166]])))
        values2 = np.dstack((np.array([[99, 89], [78, 92]]), np.array([[180, 187], [186, 205]])))
        images = czi.scenesData().images
        self.assertTrue(np.array_equal(images[0].asArray(), values1.transpose((1, 0, 2))))
        self.assertTrue(np.array_equal(images[1].asArray(), values2.transpose((1, 0, 2))))

    def testScenesDataOneChannel(self):
        czi = CZIFile(Path(self.dataDir / "testOneChannel2Scenes.czi"))
        images = czi.scenesData().images
        for image in images:
            self.assertTupleEqual(image.shape, (2, 2, 1))

    def testZStackDataNone(self):
        czi = CZIFile(Path(self.dataDir / "testOneChannel2Scenes.czi"))
        self.assertIsNone(czi.zStackData())

    def testZStackDataValues(self):
        czi = CZIFile(Path(self.dataDir / "testCziZStack4Tiny.czi"))
        images = czi.zStackData().images
        values1 = np.dstack(
            (np.array([[290, 276], [270, 334], [312, 296]]), np.array([[700, 649], [660, 704], [681, 679]])))
        values2 = np.dstack(
            (np.array([[305, 330], [297, 306], [292, 283]]), np.array([[690, 672], [686, 670], [644, 667]])))
        values3 = np.dstack(
            (np.array([[278, 268], [278, 296], [282, 316]]), np.array([[691, 701], [654, 719], [678, 711]])))
        values4 = np.dstack(
            (np.array([[312, 276], [288, 296], [307, 315]]), np.array([[664, 668], [662, 647], [654, 699]])))
        self.assertTrue(np.array_equal(images[0].asArray(), values1.transpose((1, 0, 2))))
        self.assertTrue(np.array_equal(images[1].asArray(), values2.transpose((1, 0, 2))))
        self.assertTrue(np.array_equal(images[2].asArray(), values3.transpose((1, 0, 2))))
        self.assertTrue(np.array_equal(images[3].asArray(), values4.transpose((1, 0, 2))))

    def testZStackDataOneChannel(self):
        czi = CZIFile(Path(self.dataDir / "testCziZStack4TinyOneChannel.czi"))
        images = czi.zStackData().images
        for image in images:
            self.assertTupleEqual(image.shape, (2, 3, 1))



if __name__ == '__main__':
    unittest.main()

import env
import unittest
from dcclab import CZIFile_ as CZIFile
import czifile
import numpy as np
import os


class TestCZIFile(unittest.TestCase):
    def setUp(self) -> None:
        if "tests" not in os.getcwd():
            os.chdir(os.path.dirname(os.path.realpath(__file__)))

    def testAxesNotSupported(self):
        czi = CZIFile("testCziAxesNotYetSupported.czi")
        try:
            czi.imageDataFromPath()
            self.fail("If this is reached, no exception raised!")
        except NotImplementedError as e:
            self.assertEqual(str(e), "BSTCYX0")

    def testMultiSceneCZI(self):
        czi = CZIFile("testCziMultipleScenes.czi")
        try:
            czi.imageDataFromPath()
            self.fail("If this is reached, no exception raised!")
        except NotImplementedError as e:
            self.assertEqual(str(e), "Multiple scenes")

    def testMosaicOutputOneChannel(self):
        obj = czifile.CziFile("testCziOneChannel.czi")
        array = obj.asarray(max_workers=1)
        array = array.squeeze()
        obj.close()
        czi = CZIFile("testCziOneChannel.czi")
        image = czi.imageDataFromPath()
        self.assertTrue(np.array_equal(array, image))

    def testMosaicOutputTwoChannels(self):
        obj = czifile.CziFile("testCziFileTwoChannels.czi")
        array = obj.asarray(max_workers=1)
        array = array.squeeze().transpose((1, 2, 0))
        obj.close()
        czi = CZIFile("testCziFileTwoChannels.czi")
        image = czi.imageDataFromPath()
        print(image.shape, array.shape)
        self.assertTrue(np.array_equal(array, image))

    def testMosaicOutputThreeChannels(self):
        obj = czifile.CziFile("testCziThreeChannelsOneScene.czi")
        array = obj.asarray(max_workers=1)
        array = array.squeeze().transpose((1, 2, 0))
        obj.close()
        czi = CZIFile("testCziThreeChannelsOneScene.czi")
        image = czi.imageDataFromPath()
        self.assertTrue(np.array_equal(array, image))

    def testMosaicOutputYX0Axes(self):
        obj = czifile.CziFile("testCziFileYX0Axes.czi")
        array = obj.asarray(max_workers=1)
        array = array.squeeze()
        obj.close()
        czi = CZIFile("testCziFileYX0Axes.czi")
        image = czi.imageDataFromPath()
        self.assertTrue(np.array_equal(array, image))


if __name__ == '__main__':
    print(os.path.dirname(__file__))
    unittest.main()

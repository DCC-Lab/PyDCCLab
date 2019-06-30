import env
import unittest
from dcclab import CZIFile_ as CZIFile
import czifile
import numpy as np
from pathlib import Path, PureWindowsPath

class TestCZIFile(env.dcclabTestCase):

    def testAxesNotSupported(self):
        czi = CZIFile(Path(self.dataDir / "testCziAxesNotYetSupported.czi"))
        try:
            czi.imageDataFromPath()
            self.fail("If this is reached, no exception raised!")
        except NotImplementedError as e:
            self.assertEqual(str(e), "BSTCYX0")

    def testMultiSceneCZI(self):
        czi = CZIFile(Path(self.dataDir / "testCziMultipleScenes.czi"))
        try:
            czi.imageDataFromPath()
            self.fail("If this is reached, no exception raised!")
        except NotImplementedError as e:
            self.assertEqual(str(e), "Multiple scenes")

    def testMosaicOutputOneChannel(self):
        obj = czifile.CziFile(Path(self.dataDir / "testCziOneChannel.czi"))
        array = obj.asarray(max_workers=1)
        array = array.squeeze()
        obj.close()
        czi = CZIFile(Path(self.dataDir / "testCziOneChannel.czi"))
        image = czi.imageDataFromPath()
        self.assertTrue(np.array_equal(array, image))

    def testMosaicOutputTwoChannels(self):
        obj = czifile.CziFile(Path(self.dataDir / "testCziFileTwoChannels.czi"))
        array = obj.asarray(max_workers=1)
        array = array.squeeze().transpose((1, 2, 0))
        obj.close()
        czi = CZIFile(Path(self.dataDir / "testCziFileTwoChannels.czi"))
        image = czi.imageDataFromPath()
        print(image.shape, array.shape)
        self.assertTrue(np.array_equal(array, image))

    def testMosaicOutputThreeChannels(self):
        obj = czifile.CziFile(Path(self.dataDir / "testCziThreeChannelsOneScene.czi"))
        array = obj.asarray(max_workers=1)
        array = array.squeeze().transpose((1, 2, 0))
        obj.close()
        czi = CZIFile(Path(self.dataDir / "testCziThreeChannelsOneScene.czi"))
        image = czi.imageDataFromPath()
        self.assertTrue(np.array_equal(array, image))

    def testMosaicOutputYX0Axes(self):
        obj = czifile.CziFile(Path(self.dataDir / "testCziFileYX0Axes.czi"))
        array = obj.asarray(max_workers=1)
        array = array.squeeze()
        obj.close()
        czi = CZIFile(Path(self.dataDir / "testCziFileYX0Axes.czi"))
        image = czi.imageDataFromPath()
        self.assertTrue(np.array_equal(array, image))


if __name__ == '__main__':
    unittest.main()

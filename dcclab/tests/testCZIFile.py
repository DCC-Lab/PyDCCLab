import env
import unittest
from dcclab import CZIFile
import czifile
import numpy as np


class TestCZIFile(unittest.TestCase):

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
        cziObj = czifile.CziFile("testCziOneChannel.czi")
        array = np.squeeze(cziObj.asarray())
        cziObj.close()
        czi = CZIFile("testCziOneChannel.czi")
        image = czi.imageDataFromPath()
        self.assertTrue(np.array_equal(array, image))


if __name__ == '__main__':
    unittest.main()

import env
from dcclab import *
import unittest
import numpy as np


class TestChannelFloat(unittest.TestCase):

    def setUp(self) -> None:
        array = np.ones((10, 10), dtype=np.float32) * 2.35
        self.channelNotNormalized = Channel(array)
        arrayNormed = np.ones_like(array) * 0.87
        self.channelNormalized = Channel(arrayNormed)

    def testValidConstructor(self):
        self.assertTrue(
            isinstance(self.channelNormalized, ChannelFloat) and isinstance(self.channelNotNormalized, ChannelFloat))

    def testIsNormalizedAfterInit(self):
        self.assertTrue(np.max(self.channelNotNormalized.pixels) == 1)

    def testGetHistogramValues(self):
    	pass


if __name__ == '__main__':
    unittest.main()

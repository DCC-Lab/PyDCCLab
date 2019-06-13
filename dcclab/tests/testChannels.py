import env
from dcclab import *
import unittest
import numpy as np

class TestChannels(unittest.TestCase):

    def testInitWith2DIntArray(self):
        array = np.ones((100, 100), dtype=np.int)
        channel = Channel(pixels=array)
        self.assertIsNotNone(channel)
        self.assertIsInstance(channel, Channel)

    def testInitWith2DFloatArray(self):
        array = np.ones((100, 100), dtype=np.float32)
        channel = Channel(pixels=array)
        self.assertIsNotNone(channel)
        self.assertIsInstance(channel, Channel)

    def testInitWith1DOR3DArrayFails(self):
        array = np.ones((100, 100, 3), dtype=np.float32)
        with self.assertRaises(DimensionException):
            channel = Channel(pixels=array)
        array = np.ones((100), dtype=np.float32)
        with self.assertRaises(DimensionException):
            channel = Channel(pixels=array)
        
if __name__ == '__main__':
    unittest.main()

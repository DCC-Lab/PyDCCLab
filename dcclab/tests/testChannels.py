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

    def testInitWith2DIntegerArray(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)
        self.assertEqual(array.all(), channel.pixels.all())

    def testDimension(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)
        self.assertTrue(channel.dimension == 2)

    def testShape(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)
        self.assertTrue(channel.shape == array.shape)

    def testWidth(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)
        self.assertTrue(channel.width == 100)

    def testHeight(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)
        self.assertTrue(channel.height == 200)

    def testNumberOfPixels(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)
        self.assertTrue(channel.numberOfPixels == 100*200)

    def testSizeInBytes(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)
        self.assertTrue(channel.sizeInBytes == array.nbytes)

    def testEqualChannels(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel1 = Channel(pixels=array)
        channel2 = Channel(pixels=array)
        self.assertEqual(channel1, channel2)

    def testEqualDifferentTypes(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)

        self.assertNotEqual(1, 'abc')
        self.assertNotEqual(1, np) # not an error, simply false
        self.assertNotEqual(1, channel) # not an error, simply false
        
if __name__ == '__main__':
    unittest.main()

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

    def testInitCopiesPixels(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)
        self.assertFalse(array is channel.pixels)

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

        self.assertNotEqual(1, 'abc') # not an error, simply false
        self.assertNotEqual(1, np) # not an error, simply false
        self.assertNotEqual(1, channel) # not an error, simply false

    def testPixelsCopy(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)
        pixels = channel.copy()
        self.assertFalse(pixels is array)

    def testIsBinary(self):        
        array = np.random.randint(low=0, high=2, size=(100, 200))
        self.assertTrue(Channel(pixels=array).isBinary)
        self.assertFalse(Channel(pixels=array*255).isBinary)
        self.assertFalse(Channel(pixels=array*200).isBinary)

        array = np.random.randint(low=0, high=255, size=(100, 200))
        self.assertFalse(Channel(pixels=array).isBinary)

    # def testHistogramValues(self):
    #     array = np.random.randint(low=0, high=2, size=(100, 200))
    #     hist, bins = Channel(pixels=array).getHistogramValues(True)
    #     self.assertAlmostEqual(sum(hist), 1, delta=1e-9)

    # def testHistogramValuesNotNormalized(self):
    #     array = np.ones((5, 5), dtype=np.float32)
    #     channel = Channel(pixels=array)
    #     hist = [0, 25]
    #     bins = [0, 1, 2]
    #     self.assertTrue(np.alltrue(channel.getHistogramValues()[0] == hist) and np.alltrue(
    #         channel.getHistogramValues()[-1] == bins))

    # def testHistogramValuesNormalized(self):
    #     array = np.ones((5, 5), dtype=np.float32)
    #     channel = Channel(pixels=array)
    #     hist, bins = channel.getHistogramValues(True)
    #     self.assertAlmostEqual(sum(hist), 1, delta=1e-9)
       
    def testConvolution(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        kernel = [[-1, 0, 1],[1,0,1],[0,1,1]]
        channel = Channel(pixels=array).convolveWith(kernel)
        self.assertIsNotNone(channel)
        self.assertTrue(channel.pixels.shape == array.shape)

if __name__ == '__main__':
    unittest.main()

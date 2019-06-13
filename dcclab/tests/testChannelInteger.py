import env
from dcclab import *
import unittest
import numpy as np
import coverage


class TestChannelInteger(unittest.TestCase):

    def testValidComstructor(self):
        valid = np.ones((10, 10), dtype=np.uint8)
        self.assertIsInstance(ChannelInt(valid), ChannelInt)

    def testInvalidConstructorNotInteger(self):
        invalid = np.ones((100, 1012), dtype=np.complex)
        with self.assertRaises(TypeError):
            ChannelInt(invalid)

    def testInvalidConstructorNot2D(self):
        invalid = np.arange(10, 100).astype(int)
        with self.assertRaises(DimensionException):
            ChannelInt(invalid)

    def testConvertToNormalizedFloat(self):
        nonNormalized = np.ones((1000, 1000), dtype=np.uint8) * 201
        channel = ChannelInt(nonNormalized)
        normalizedAndFloat = channel.convertToNormalizedFloat()
        self.assertTrue(np.max(normalizedAndFloat.pixels) <= 1)

    def testGetHistogramValuesNotNormed(self):
        array = np.zeros((5, 5), dtype=np.uint8)
        for i in range(5):
            for j in range(5):
                array[i][j] = j * i
        channel = ChannelInt(array)
        bins = np.arange(0, 18)
        hist = np.array([9, 1, 2, 2, 3, 0, 2, 0, 2, 1, 0, 0, 2, 0, 0, 0, 1])
        histValues = channel.getHistogramValues()
        self.assertTrue(np.array_equal(bins, histValues[-1]) and np.array_equal(hist, histValues[0]))

    def testGetHistogramValuesNormed(self):
        array = np.zeros((5, 5), dtype=np.uint8)
        for i in range(5):
            for j in range(5):
                array[i][j] = j * i
        channel = ChannelInt(array)
        histValues = channel.getHistogramValues(True)
        self.assertEqual(sum(histValues[0]), 1)


if __name__ == '__main__':
    unittest.main()

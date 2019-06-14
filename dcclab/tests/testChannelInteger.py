import env
from dcclab import *
import unittest
import numpy as np


class TestChannelInteger(unittest.TestCase):
    def setUp(self) -> None:
        array = np.ones((5, 5), dtype=np.uint8)
        self.channelUint8 = Channel(array)
        self.channelUint16 = Channel(array.astype(np.uint16))

    def testValidComstructor(self):
        valid = np.ones((10, 10), dtype=np.uint8)
        self.assertIsInstance(Channel(valid), ChannelInt)

    def testConvertToNormalizedFloat(self):
        nonNormalized = np.ones((1000, 1000), dtype=np.uint8) * 201
        channel = Channel(nonNormalized)
        normalizedAndFloat = channel.convertToNormalizedFloat()
        self.assertTrue(np.max(normalizedAndFloat.pixels) <= 1 and isinstance(normalizedAndFloat, ChannelFloat))

    def testGetHistogramValuesNotNormed(self):
        array = np.zeros((5, 5), dtype=np.uint8)
        for i in range(5):
            for j in range(5):
                array[i][j] = j * i
        channel = Channel(array)
        bins = np.arange(0, 18)
        hist = np.array([9, 1, 2, 2, 3, 0, 2, 0, 2, 1, 0, 0, 2, 0, 0, 0, 1])
        histValues = channel.getHistogramValues()
        self.assertTrue(np.array_equal(bins, histValues[-1]) and np.array_equal(hist, histValues[0]))

    def testGetHistogramValuesNormed(self):
        array = np.zeros((5, 5), dtype=np.uint8)
        for i in range(5):
            for j in range(5):
                array[i][j] = j * i
        channel = Channel(array)
        histValues = channel.getHistogramValues(True)
        self.assertEqual(sum(histValues[0]), 1)

    def testConvo(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=UserWarning)
            convo = self.channelUint8.convolveWith(np.identity(3))
            self.assertTrue(np.allclose(convo.pixels, 3 / 255))



if __name__ == '__main__':
    unittest.main()

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
        self.assertTrue(
            np.alltrue(np.max(normalizedAndFloat.pixels) == 201 / 255) and isinstance(normalizedAndFloat, ChannelFloat))

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
            self.assertTrue(np.allclose(convo.pixels, 3 / 255) and isinstance(convo, ChannelFloat))

    def testApplyConv(self):
        self.channelUint8.applyConvolution([[1, 1, 1], [1, 1, 1]])
        self.assertTrue(self.channelUint8.pixels.dtype == np.uint8 and isinstance(self.channelUint8, ChannelInt))
        self.assertIsInstance(self.channelUint8, ChannelInt)

    def testGetGaussianFilter(self):
        sigma = 0.4
        array = np.zeros((5, 5), dtype=np.uint8)
        array[2][2] = 100
        channel = Channel(array)
        gaussianBlurredArray = np.zeros_like(array, dtype=np.float32)
        gaussianBlurredArray[2][2] = 100 / 255
        for i in range(5):
            for j in range(5):
                gaussianBlurredArray[i][j] = np.exp(-((i - 2) ** 2 + (j - 2) ** 2) / (2 * sigma ** 2)) / (
                        2 * np.pi * sigma ** 2)
        normalizedGaussianBlurredArray = gaussianBlurredArray / np.sum(gaussianBlurredArray) * 100 / 255
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=UserWarning)
            channelGaussian = channel.getGaussianFilter(sigma)
        channelGaussianPixels = channelGaussian.pixels
        self.assertTrue(np.allclose(channelGaussianPixels,
                                    normalizedGaussianBlurredArray) and isinstance(channelGaussian, ChannelFloat))

    def testApplyGaussian(self):
        self.channelUint16.applyGaussianFilter(0.00254)
        self.assertTrue(self.channelUint16.pixels.dtype == np.uint16 and isinstance(self.channelUint16, ChannelInt))

    def testGetEntropyFiltering(self):
        filterSize = 3
        array = np.zeros((5, 5), dtype=np.uint8)
        array[2][2] = 1 / 255
        resultEntropyArray = np.zeros_like(array)
        for i in range(1, 4):
            for j in range(1, 4):
                resultEntropyArray[i][j] = 503.2583348E-3
        resultEntropyImage = Channel(resultEntropyArray)
        computedByClass = Channel(array).getEntropyFilter(filterSize)
        self.assertTrue(resultEntropyImage == computedByClass and isinstance(computedByClass, ChannelFloat))

    def testEntropyWarning16Bits(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            with self.assertRaises(UserWarning):
                self.channelUint16.getEntropyFilter(2)

    def testGetStandardDeviationSlow(self):
        array = np.zeros((5, 5), dtype=np.uint16)
        # Padded array (internally happens when computing convolution with another matrix)
        paddedArray = np.zeros((7, 7))
        for i in range(1, 4):
            for j in range(1, 4):
                array[i][j] = 3
                paddedArray[i + 1][j + 1] = 3 / (2 ** 16 - 1)
        listOfChannels = []
        # Smaller array of size 3x3 resulting of the convolution
        for i in range(5):
            for j in range(5):
                listOfChannels.append(
                    Channel(np.array([paddedArray[i][j:j + 3], paddedArray[i + 1][j:j + 3],
                                      paddedArray[i + 2][j:j + 3]], dtype=np.float32)))
                # Compute the standard deviation of the smaller arrays
        resultArray = np.array([channel.getStandardDeviationOfPixels() for channel in listOfChannels],
                               dtype=np.float32).reshape((5, 5))
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=UserWarning)
            stdDevChannelPixels = Channel(array).getStandardDeviationFilterSlow(filterSize=3).pixels
        print(resultArray)
        print(stdDevChannelPixels)
        self.assertTrue(np.allclose(resultArray, stdDevChannelPixels))

        if __name__ == '__main__':
            unittest.main()

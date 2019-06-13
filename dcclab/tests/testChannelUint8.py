import env
from dcclab import *
import unittest
import numpy as np


class TestChannelUint8Constructor(unittest.TestCase):

    def testValidConstructor(self):
        valid = np.ones((10, 10), dtype=np.uint8) * 125
        self.assertIsInstance(ChannelUint8(valid), ChannelUint8)

    def testInvalidConstructor(self):
        invalid = np.ones((10, 10)) * 1024
        with self.assertRaises(TypeError):
            ChannelUint8(invalid)


class TestChannelUint8Methods(unittest.TestCase):
    def setUp(self) -> None:
        array = np.ones((5, 5), dtype=np.uint8)
        self.channel = ChannelUint8(array)

    def testConvolution(self):
        convolutionMatrix = np.identity(3)
        convolvedPixels = self.channel.convolveWith(convolutionMatrix).pixels
        self.assertTrue(np.array_equal(np.ones_like(convolvedPixels) * 3, convolvedPixels))

    def testEntropyFilter(self):
        import skimage.measure
        array = np.zeros((5, 5,), dtype=np.uint8)
        paddedArray = np.zeros((7, 7))
        resultArray = np.zeros_like(array, dtype=np.float32)
        for i in range(1, 4):
            for j in range(1, 4):
                array[i, j] = 100
                paddedArray[i + 1][j + 1] = 100
        for i in range(5):
            for j in range(5):
                resultArray[i, j] = skimage.measure.shannon_entropy(paddedArray[i: i + 3, j:j + 3])
        #ChannelUint8(array).getEntropyFiltering(3).display()


if __name__ == '__main__':
    unittest.main()

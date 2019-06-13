import env
from dcclab import *
import unittest
import numpy as np


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


if __name__ == '__main__':
    unittest.main()

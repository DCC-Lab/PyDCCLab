import env
from dcclab import *
import unittest
import numpy as np

class TestMATLABFile(unittest.TestCase):

    def testInit(self):
        self.assertIsNotNone(MATLABFile("./test.mat"))

    def testInitWithVariable(self):
        self.assertIsNotNone(MATLABFile("./test.mat", variable='image'))

    def testImageDataWithImageVariable(self):
        file = MATLABFile("./test.mat", variable='image')
        data = file.imageDataFromPath()
        self.assertIsNotNone(data)
        self.assertTrue(isinstance(data, np.ndarray))
        self.assertEqual(data.ndim, 3)

    def testImageDataWithChannelVariable(self):
        file = MATLABFile("./test.mat", variable='channel')
        data = file.imageDataFromPath()
        self.assertIsNotNone(data)
        self.assertTrue(isinstance(data, np.ndarray))
        self.assertEqual(data.ndim, 3)

    def testImageDataWithSomeVariable(self):
        file = MATLABFile("./test.mat", variable='notAnImage')
        with self.assertRaises(ValueError):
            data = file.imageDataFromPath()

if __name__ == '__main__':
    unittest.main()

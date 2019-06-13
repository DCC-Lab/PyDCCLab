import env
from dcclab import *

import unittest
import numpy as np
import re

class TestImageCollection(unittest.TestCase):

    def testInit(self):
        self.assertIsNotNone(ImageCollection())

    def testInitWithPattern(self):
        self.assertIsNotNone(ImageCollection(pathPattern=r'abc-(\d).tiff'))

    def testInitWithImages(self):
        data = np.random.randint(low=0, high=255, size=(100, 200, 3))
        imgs = [Image(data)]
        self.assertIsNotNone(ImageCollection(imgs))

    def testInitWithGarbage(self):
        with self.assertRaises(Exception):
            self.assertIsNotNone(ImageCollection("string"))


if __name__ == '__main__':
    unittest.main()

import env
from dcclab import *

import unittest
import numpy as np
import re

class TestImageCollection(unittest.TestCase):

    def testInit(self):
        self.assertIsNotNone(ImageCollection())

    def testInitWithPatternNoFile(self):
        coll = ImageCollection(pathPattern=r'abc-(\d).tiff')
        self.assertIsNotNone(coll)
        self.assertTrue(coll.images == [])

    def testTestFilesArePresent(self):
        pat = PathPattern(r'test-(\d+).jpg')
        self.assertTrue(pat.matchingFiles() == ['./test-001.jpg','./test-002.jpg','./test-003.jpg'])

    def testInitWithPatternAndFiles(self):
        coll = ImageCollection(pathPattern=r'test-(\d+).jpg')
        self.assertIsNotNone(coll)
        self.assertTrue(coll.numberOfImages != 0)

    def testInitWithPattern(self):
        coll = ImageCollection(pathPattern=r'abc-(\d).tiff')
        self.assertIsNotNone(coll)

    def testInitWithImages(self):
        data = np.random.randint(low=0, high=255, size=(100, 200, 3))
        imgs = [Image(data)]
        self.assertIsNotNone(ImageCollection(imgs))

    def testInitWithGarbage(self):
        with self.assertRaises(Exception):
            self.assertIsNotNone(ImageCollection("string"))


if __name__ == '__main__':
    unittest.main()

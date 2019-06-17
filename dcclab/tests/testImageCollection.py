import env
from dcclab import *

import unittest
import numpy as np
import re

class TestImageCollection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestImageCollection, cls).setUpClass()
        cls.largeImmutable = ImageCollection()
        for i in range(10):
            imageData = np.random.randint(low=0, high=255, size=(1024, 1024, 3))
            cls.largeImmutable.append(Image(imageData))
        print("Large array is {0:.0f} MB".format(cls.largeImmutable.sizeInBytes/1000000))
        cls.large = cls.largeImmutable

    """ https://hackernoon.com/timing-tests-in-python-for-fun-and-profit-1663144571 """
    def setUp(self):
        self.large = self.largeImmutable
        self._started_at = time.time()

    def tearDown(self):
        elapsed = time.time() - self._started_at
        print('{} ({}s)'.format(self.id(), round(elapsed, 2)))

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

    def testInitImageCollection(self):
        imgCollection = ImageCollection(pathPattern = r"/tmp/test-(\d+).png")
        self.assertTrue(len(imgCollection) != 0)
        self.assertIsNotNone(imgCollection.images)
        self.assertTrue(imgCollection.numberOfImages > 0)

    def testFilterNoiseImageCollection(self):
        collection = ImageCollection()
        for i in range(100):
            imageData = np.random.randint(low=0, high=255, size=(100, 200, 3))
            collection.append(Image(imageData))
        collection.filterNoise()

    def testFilterNoiseImageCollection(self):
        collection = ImageCollection()
        for i in range(100):
            imageData = np.random.randint(low=0, high=255, size=(100, 200, 3))
            collection.append(Image(imageData))
        collection.threshold(value=128)

    def testThresholdLargeImageCollection(self):
        self.large.threshold(value=128)

    def testLargeImageCollectionAsArray(self):
        largeArray = self.large.asArray()

    def testMaskFromThreshold(self):
        self.large.setMaskFromThreshold(value=128)

    def testLabelComponents(self):
        self.large.setMaskFromThreshold(value=128)
        self.large.labelMaskComponents()
        self.large.analyzeComponents()


if __name__ == '__main__':
    unittest.main()

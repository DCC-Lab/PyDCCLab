import env
import unittest
from dcclab import *
import time

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

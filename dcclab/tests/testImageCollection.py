import env
import unittest
from dcclab import *
import time

class TestImageCollection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestImageCollection, cls).setUpClass()
        cls.large = ImageCollection()
        for i in range(20):
            imageData = np.random.randint(low=0, high=255, size=(1024, 1024, 3))
            cls.large.append(Image(imageData))

    """ https://hackernoon.com/timing-tests-in-python-for-fun-and-profit-1663144571 """
    def setUp(self):
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


if __name__ == '__main__':
    unittest.main()

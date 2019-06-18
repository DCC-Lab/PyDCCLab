import env
from dcclab import *
import unittest

class TestTimeSeries(unittest.TestCase):

    def testInit(self):
        self.assertIsNotNone(TimeSeries())

    def testInitWithPattern(self):
        self.assertIsNotNone(TimeSeries(pathPattern= r"/tmp/test-(\d+).tif"))

    def testInitWithImageData(self):
        imageData = np.random.randint(low=0, high=255, size=(100, 200,3,10))
        self.assertIsNotNone(TimeSeries(imagesArray=imageData))

    def testSeriesAsArray(self):
        series = TimeSeries(pathPattern= r"/tmp/test-(\d+).tif")
        self.assertIsNotNone(series.asArray())


if __name__ == '__main__':
    unittest.main()

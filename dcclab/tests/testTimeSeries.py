import env
from dcclab import *
import unittest

class TestTimeSeries(env.DCCLabTestCase):

    def testInit(self):
        self.assertIsNotNone(TimeSeries())

    def testInitWithPattern(self):
        self.assertIsNotNone(TimeSeries(pathPattern= os.path.join(self.dataDir, r"test-(\d+).jpg")))

    def testInitWithImageData(self):
        imageData = np.random.randint(low=0, high=255, size=(100, 200,3,10))
        series = TimeSeries(imagesArray=imageData)
        self.assertIsNotNone(series)
        self.assertEqual(series.numberOfImages, 10)

    def testSeriesAsArray(self):
        series = TimeSeries(pathPattern= os.path.join(self.dataDir, r"test-(\d+).jpg"))
        self.assertIsNotNone(series.asArray())

    def testSeriesSave(self):
        imageData = np.random.randint(low=0, high=255, size=(100, 200,3,10))
        series = TimeSeries(imagesArray=imageData)
        series.save(os.path.join(self.dataDir, r"test-(\d+).jpg"))

        pattern = PathPattern(self.dataDir + "testWrite-{0:03d}.tif")
        for i in range(10):
            file = pattern.filePathWithIndex(i)
            self.assertTrue(os.path.exists(file),"{0} does not exist".format(file))

    def testSeriesSave(self):
        imageData = np.random.randint(low=0, high=255, size=(100, 200,3,10))
        series = TimeSeries(imagesArray=imageData)
        series.save(os.path.join(self.tmpDir, r"test-(\d+).avi"))
        self.assertTrue(os.path.join(self.tmpDir, r"test-(\d+).avi"))

if __name__ == '__main__':
    unittest.main()

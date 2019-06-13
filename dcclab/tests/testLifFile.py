from dcclab.imageCollection import LIFFile
from dcclab.lifReader import FastSerie
import unittest


class TestLifFile(unittest.TestCase):

    def testInitWithLifFile(self):
        lifObj = LIFFile("test_LifFile.lif")
        self.assertIsNotNone(lifObj)

    def testInitWithDirectory(self):
        with self.assertRaises(Exception):
            LIFFile(".")

    def testInitWithBadLifFile(self):
        with self.assertRaises(Exception):
            LIFFile("test_NotLifFile.lif")

    def testInitSeries(self):
        lifObj = LIFFile("test_LifFile.lif")
        self.assertTrue(len(lifObj.series), 4)

    def testNumberOfSeries(self):
        lifObj = LIFFile("test_LifFile.lif")
        self.assertTrue(lifObj.numberOfSeries, 4)

    def testGetItemWithInteger(self):
        lifObj = LIFFile("test_LifFile.lif")
        self.assertIsInstance(lifObj[0], FastSerie)

    def testGetItemWithListOfIntegers(self):
        lifObj = LIFFile("test_LifFile.lif")
        series = lifObj[0, 1, 2]
        self.assertTrue(len(series) == 3)
        self.assertIsInstance(series[0], FastSerie)

if __name__ == '__main__':
    unittest.main()

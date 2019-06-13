from dcclab.imageCollection import LIFFile
from dcclab.lifReader import LifSerie
import unittest


class TestLifFile(unittest.TestCase):

    def setUp(self):
        self.lifObj = LIFFile('test_LifFile.lif')

    def testInitWithLifFile(self):
        self.assertIsNotNone(self.lifObj)

    def testInitWithDirectory(self):
        with self.assertRaises(Exception):
            LIFFile(".")

    def testInitWithBadLifFile(self):
        with self.assertRaises(Exception):
            LIFFile("test_NotLifFile.lif")

    def testInitSeries(self):
        self.assertTrue(len(self.lifObj.series) == 8)

    def testNumberOfSeries(self):
        self.assertTrue(self.lifObj.numberOfSeries == 8)

    def testGetItemWithInteger(self):
        self.assertIsInstance(self.lifObj[0], LifSerie)

    def testGetItemWithIntegersTuple(self):
        series = self.lifObj[0, 1, 2]
        self.assertTrue(len(series) == 3)
        self.assertIsInstance(series[0], LifSerie)

    def testGetItemWithIntegersList(self):
        series = self.lifObj[[0, 1, 2]]
        self.assertTrue(len(series) == 3)
        self.assertIsInstance(series[0], LifSerie)

    def testGetItemWithBadIndex(self):
        with self.assertRaises(IndexError):
            series = self.lifObj[8]

    def testGetItemWithSlice(self):
        series = self.lifObj[2:5]
        self.assertTrue(len(series) == 3)
        self.assertIsInstance(series[0], LifSerie)


if __name__ == '__main__':
    unittest.main()

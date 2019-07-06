import env
from dcclab import LIFFile
from dcclab.lifReader import LIFSerie
import unittest
from pathlib import Path, PureWindowsPath


class TestLifFile(env.DCCLabTestCase):

    def setUp(self):
        self.lifObj = LIFFile(Path(self.dataDir, 'test_LifFile.lif').__str__())

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

    def testLifLength(self):
        self.assertTrue(len(self.lifObj) == 8)

    def testGetItemWithInteger(self):
        self.assertIsInstance(self.lifObj[0], LIFSerie)

    def testGetItemWithIntegersTuple(self):
        series = self.lifObj[0, 1, 2]
        self.assertTrue(len(series) == 3)
        self.assertIsInstance(series[0], LIFSerie)

    def testGetItemWithIntegersList(self):
        series = self.lifObj[[0, 1, 2]]
        self.assertTrue(len(series) == 3)
        self.assertIsInstance(series[0], LIFSerie)

    def testGetItemWithBadIndex(self):
        with self.assertRaises(IndexError):
            series = self.lifObj[8]

    def testGetItemWithSlice(self):
        series = self.lifObj[2:5]
        self.assertTrue(len(series) == 3)
        self.assertIsInstance(series[0], LIFSerie)

    def testGetItemWithNone(self):
        series = self.lifObj[None]
        self.assertTrue(len(series) == 8)
        self.assertIsInstance(series[0], LIFSerie)

    def testKeepSeries(self):
        self.lifObj.keepSeries([0, 1, 2])
        self.assertTrue(self.lifObj.numberOfSeries == 3)
        self.assertIsInstance(self.lifObj.series[0], LIFSerie)

    def testRemoveAt(self):
        self.lifObj.removeAt(0)
        self.assertTrue(self.lifObj.numberOfSeries == 7)

    def testGetMetadataFromSerieObj(self):
        metadata = self.lifObj[0].getMetadata()
        self.assertIsInstance(metadata, dict)
        self.assertTrue(metadata['channel_number'] == 1)

    def testGetMetadataAtIndex(self):
        metadata = self.lifObj.metadata(serieIndex=0)
        self.assertIsInstance(metadata, dict)
        self.assertTrue(metadata['channel_number'] == 1)

    def testGetAllMetadata(self):
        metadata = self.lifObj.metadata()
        self.assertIsInstance(metadata, list)
        self.assertIsInstance(metadata[0], dict)

    def testGetZStackOneSeriesOneChannel(self):
        stacks = self.lifObj.zStacksData(seriesIndices=0, channelIndices=0)

        self.assertIsInstance(stacks, list)
        self.assertTrue(len(stacks) == 1)
        self.assertTrue(stacks[0].shape == (448, 448, 448))  # fixme: will probably fail: test for the new ZStack objects

    def testGetZStackOneSeries(self):
        stacks = self.lifObj.zStacksData(seriesIndices=0)

        self.assertIsInstance(stacks, list)
        self.assertTrue(len(stacks) == 1)
        self.assertTrue(stacks[0].shape == (448, 448, 448))

    def testGetAllZStacks(self):
        self.lifObj.keepSeries([0, 1])
        stacks = self.lifObj.zStacksData()

        self.assertIsInstance(stacks, list)
        self.assertTrue(len(stacks) == 2)
        self.assertTrue(stacks[0].shape == (448, 448, 448))

    def testGetZStacksBadChannels(self):
        with self.assertRaises(Exception):
            self.lifObj.zStacksData(seriesIndices=0, channelIndices=(0, 1))

    @unittest.skip("no small test data file with multiple channels")
    def testGetZStacksMultipleChannels(self):
        pass

    @unittest.skip("no small test data file with multiple channels")
    def testGetZStacksMultipleChannelsStackArrays(self):
        pass

if __name__ == '__main__':
    unittest.main()

import env
import unittest
import os

from dcclab.ml.dataset import Dataset

class TestMLDatasets(env.DCCLabTestCase):

    def testExtractDataSingleChannel(self):
        dataset = Dataset(os.path.join(self.dataDir, "labelledDataset"))
        self.assertIsNotNone(dataset)

    def testGetFolders(self):
        folders = list(os.walk(("/kjasdkjhasdkhjasdkhjasdkhj")))
        self.assertTrue(len(folders) == 0)

    def testExtractDataSingleChannelNoDirectory(self):
        with self.assertRaises(FileNotFoundError):
            dataset = Dataset(os.path.join(self.dataDir, "labelledDatasetasdasda"))

    def testExtractDataSingleChannelTagIsSemantic(self):
        dataset = Dataset(os.path.join(self.dataDir, "labelledDataset"))
        self.assertIsNotNone(dataset)
        self.assertTrue(dataset.isSemantic)

    def testExtractDataSingleChannelTagIsNotSemantic(self):
        dataset = Dataset(os.path.join(self.dataDir, "notSemantic"))
        self.assertIsNotNone(dataset)
        self.assertTrue(dataset.isSemantic)

    @unittest.skipIf(not os.path.exists(os.path.join(env.DCCLabTestCase.dataDir, "notSemantic")), "Dataset has been lost. Tests cannot proceed. FInd it.")
    def testExtractDataSingleChannelTagIsNotSemantic(self):
        dataset = Dataset(os.path.join(self.dataDir, "notSemantic"))
        self.assertTrue(dataset.isValid)


if __name__ == '__main__':
    unittest.main()

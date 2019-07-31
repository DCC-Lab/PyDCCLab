import env
import unittest
import os

from dcclab import Dataset

from pathlib import Path

class TestMLDatasets(env.DCCLabTestCase):

    def testExtractDataSingleChannel(self):
        dataset = Dataset(os.path.join(self.dataDir, "labelledDataset"))
        self.assertIsNotNone(dataset)

if __name__ == '__main__':
    unittest.main()

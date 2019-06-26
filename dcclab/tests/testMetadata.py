from dcclab import Metadata
import unittest
import os


class TestMetadata(unittest.TestCase):
    def setUp(self):
        self.directory = os.path.dirname(__file__)
        self.cziPath = os.path.join(self.directory, 'testCziFile.czi')
        self.csvPath = os.path.join(self.directory, 'testCSVMetadata.csv')
        pass

    def tearDown(self):
        pass


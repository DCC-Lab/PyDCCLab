from dcclab import Metadata
import unittest
import os


class TestMetadata(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = os.path.dirname(__file__)
        self.cziPath = os.path.join(self.directory, 'testCziFile.czi')
        self.csvPath = os.path.join(self.directory, '')
        pass

    def tearDown(self) -> None:
        pass


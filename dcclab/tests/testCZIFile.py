import env
import unittest
from dcclab import CZIFile


class TestCZIFile(unittest.TestCase):

    def testMultipleScenesError(self):
        czi = CZIFile("testCziAxesNotYetSupported.czi")
        try:
            czi.imageDataFromPath()
            self.fail("If this is reached, no exception raised!")
        except NotImplementedError as e:
            self.assertEqual(str(e), "BSTCYX0")

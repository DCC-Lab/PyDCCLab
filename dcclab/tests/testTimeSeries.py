import env
from dcclab import *
import unittest

class TestTimeSeries(unittest.TestCase):

    def testInitWithLifFile(self):
        self.assertIsNotNone(TimeSeries())


if __name__ == '__main__':
    unittest.main()

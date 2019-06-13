import env
from dcclab import *

import unittest
import numpy as np

class TestPatterns(unittest.TestCase):

    def testInit(self):
        self.assertIsNotNone(PathPattern('abc'))
        
if __name__ == '__main__':
    unittest.main()

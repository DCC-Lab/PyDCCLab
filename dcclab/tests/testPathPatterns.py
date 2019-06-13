import env
from dcclab import *

import unittest
import numpy as np
import re

class TestPatterns(unittest.TestCase):

    def testInit(self):
        self.assertIsNotNone(PathPattern('abc'))

    def testInitNoCaptureGroups(self):
        pat = PathPattern('abc')
        self.assertFalse(pat.hasCaptureGroups)

    def testInitWithCaptureGroups(self):
        pat = PathPattern(r'abc(\d)')
        self.assertTrue(pat.hasCaptureGroups)

    def testFindCaptureGroups(self):
        match = re.search(r"(\(.*\))", "abc(daniel)def")
        self.assertIsNotNone(match)
        self.assertTrue(len(match.groups()) == 1)
        strings = re.findall(r"(\(.+?\))", "abc(daniel)(def)")
        print(strings)
        self.assertTrue(len(strings) == 2)

    def testInitWith0CaptureGroup(self):
        pat = PathPattern(r'abckjhasd')
        self.assertTrue(pat.numberOfCaptureGroups == 0)
        pat = PathPattern(r'abckjha(sd')
        self.assertTrue(pat.numberOfCaptureGroups == 0)
        pat = PathPattern(r'abckjha)sd')
        self.assertTrue(pat.numberOfCaptureGroups == 0)

    def testInitWith1CaptureGroup(self):
        pat = PathPattern(r'abc(\d)')
        self.assertTrue(pat.numberOfCaptureGroups == 1)

    # def testInitWith2CaptureGroups(self):
    #     pat = PathPattern(r'abc(\d)...(lkha)')
    #     self.assertTrue(pat.numberOfCaptureGroups == 2)

        
if __name__ == '__main__':
    unittest.main()

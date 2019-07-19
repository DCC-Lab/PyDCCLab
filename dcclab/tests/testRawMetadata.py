from dcclab import RAWMetadata as mtdt
import env
import unittest
import os


class TestRawMetadata(env.DCCLabTestCase):
    def setUp(self) -> None:
        self.rawPath = os.path.join(self.dataDir, 'test.raw')
        self.iniPath = os.path.join(self.dataDir, 'test.ini')
        self.xmlPath = os.path.join(self.dataDir, 'test.xml')

    def tearDown(self) -> None:
        os.remove(self.rawPath)
        os.remove(self.iniPath)
        os.remove(self.xmlPath)


if __name__ == '__main__':
    unittest.main()
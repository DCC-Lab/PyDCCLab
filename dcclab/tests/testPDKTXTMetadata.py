from dcclab import PDKTXTMetadata as mtdt
import unittest
import env
import os


class TestPDKTXTMetadata(env.DCCLabTestCase):
    def setUp(self) -> None:
        self.iniPath = os.path.join(str(self.dataDir), '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_XYT.ini')
        with open(self.iniPath, 'w') as file:
            file.write('[_]\nTest_File = This is a test file\nno.of.channels = 1.000000000000\nblank_line = blank\n'
                       'frame.count = 1000.000000000000\n\nx.pixels = 1024.000000000000\ny.pixels = 512.000000000000\n'
                       'x.voltage = 5.000000000000\ny.voltage = 1.250000000000\n\nwrong.line = bleh\n'
                       'pixel.resolution = 5.000000000000\nLaser.Power = 21.500000000000\n')

    def tearDown(self) -> None:
        os.remove(self.iniPath)

    def testIniPath(self):
        metadata = mtdt(self.iniPath)
        realPath = os.path.join(str(self.dataDir), '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_XYT.ini')
        self.assertEqual(metadata.iniPath, realPath)

    def testIniPathLineshifted(self):
        metadata = mtdt(self.iniPath)
        metadata.path = '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_XYT.lineshifted.raw'
        self.assertEqual(metadata._PDKTXTMetadata__iniPath(), '20190101_12_12_12_900nm_16x_512x1024_1000f_8dpf_XYT.ini')

    def testReadFile(self):
        metadata = mtdt(self.iniPath)
        self.assertTrue(metadata.readFile())

    def testAsDict(self):
        metadata = mtdt(self.iniPath)
        self.assertEqual(metadata.asDict, {'Laser.Power': '21.500000000000', 'frame.count': '1000.000000000000',
                                           'no.of.channels': '1.000000000000', 'pixel.resolution': '5.000000000000',
                                           'x.pixels': '1024.000000000000', 'x.voltage': '5.000000000000',
                                           'y.pixels': '512.000000000000', 'y.voltage': '1.250000000000'})

    def testKeys(self):
        metadata = mtdt(self.iniPath)
        self.assertEqual(metadata.keys, {'ZebrafishRAW': {'no.of.channels': 'INTEGER', 'frame.count': 'INTEGER',
                                                          'x.pixels': 'INTEGER', 'y.pixels': 'INTEGER', 'x.voltage':
                                                              'REAL', 'y.voltage': 'REAL', 'pixel.resolution': 'REAL',
                                                          'Laser.Power': 'REAL'}})


if __name__ == '__maine__':
    unittest.main()

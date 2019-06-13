from Database.MetadataFromCzi.cziChannel import CZIChannel as chnnl
from Database.MetadataFromCzi.cziMetadata import CZIMetadata as mtdt
import xml.etree.ElementTree as ET
import unittest
import os


class TestCziChannel(unittest.TestCase):
    def setUp(self):
        self.directory = os.path.dirname(os.path.dirname(__file__))
        self.testPath = os.path.join(self.directory, 'testData', 'testCziFile.czi')
        self.missingEntriesPath = os.path.join(self.directory, 'testData', 'MissingEntries.xml')
        self.missingKeysPath = os.path.join(self.directory, 'testData', 'MissingKeys.xml')
        self.meta = mtdt(self.testPath, 'testCziFile.czi')

    def test_setExWavelengthFilter_expectedValue(self):
        channel = chnnl(['Channel:1', 'DAPI', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertEqual(channel.exWavelengthFilter, '335-383')

    def test_setExWavelengthFilter_notFound(self):
        channel = chnnl(['', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertIsNone(channel.exWavelengthFilter)

    def test_setExWavelengthFilter_emptyFilterList(self):
        channel = chnnl(['', 'EGFP', 'testCziFile.czi'], [], self.meta.root)
        self.assertIsNone(channel.exWavelengthFilter)

    def test_setExWavelengthFilter_notFilterList(self):
        channel = chnnl(['', 'EGFP', 'testCziFile.czi'], [1, 2, 3], self.meta.root)
        self.assertIsNone(channel.exWavelengthFilter)

    def test_setEmWavelengthFilter_expectedValue(self):
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertEqual(channel.emWavelengthFilter, '500-550')

    def test_setEmWavelengthFilter_notFound(self):
        channel = chnnl(['', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertIsNone(channel.emWavelengthFilter)

    def test_setEmWavelengthFilter_noFilters(self):
        channel = chnnl(['', 'EGFP', 'testCziFile.czi'], [], self.meta.root)
        self.assertIsNone(channel.emWavelengthFilter)

    def test_setBeamsplitter_expectedValue(self):
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertEqual(channel.beamsplitter, '495')

    def test_setBeamsplitter_notFound(self):
        channel = chnnl(['', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertIsNone(channel.beamsplitter)

    def test_setBeamsplitter_noFilters(self):
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], [], self.meta.root)
        self.assertIsNone(channel.beamsplitter)

    def test_setReflector_expectedValue(self):
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertEqual(channel.setReflector(), '38 HE Green Fluorescent Prot')

    def test_setReflector_missingKeys(self):
        channel = chnnl(['', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertIsNone(channel.setReflector())

    def test_setReflector_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, root)
        self.assertIsNone(channel.setReflector())

    def test_setContrastMethod_expectedValue(self):
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertEqual(channel.setContrastMethod(), 'Fluorescence')

    def test_setContrastMethod_missingKeys(self):
        channel = chnnl(['', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertIsNone(channel.setContrastMethod())

    def test_setContrastMethod_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, root)
        self.assertIsNone(channel.setContrastMethod())

    def test_setLightSource_expectedValue(self):
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertEqual(channel.setLightSource(), 'HXP 120 V')

    def test_setLightSource_missingKeys(self):
        channel = chnnl(['', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertIsNone(channel.setLightSource())

    def test_setLightSource_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, root)
        self.assertIsNone(channel.setLightSource())

    def test_setLightSourceIntensity_expectedValue(self):
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertEqual(channel.setLightSourceIntensity(), '58.32 %')

    def test_setLightSourceIntensity_missingKeys(self):
        channel = chnnl(['', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertIsNone(channel.setLightSourceIntensity())

    def test_setLightSourceIntensity_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, root)
        self.assertIsNone(channel.setLightSourceIntensity())

    def test_setDyeName_expectedValue(self):
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertEqual(channel.setDyeName(), 'EGFP')

    def test_setDyeName_missingKeys(self):
        channel = chnnl(['', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertIsNone(channel.setDyeName())

    def test_setDyeName_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, root)
        self.assertIsNone(channel.setDyeName())

    def test_setChannelColor_expectedValue(self):
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertEqual(channel.setChannelColor(), '#FF00FF5B')

    def test_setChannelColor_missingKeys(self):
        channel = chnnl(['', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertIsNone(channel.setChannelColor())

    def test_setChannelColor_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, root)
        self.assertIsNone(channel.setChannelColor())

    def test_setExWavelength_expectedValue(self):
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertEqual(channel.setExWavelength(), '488')

    def test_setExWavelength_missingKeys(self):
        channel = chnnl(['', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertIsNone(channel.setExWavelength())

    def test_setExWavelength_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, root)
        self.assertIsNone(channel.setExWavelength())

    def test_setEmWavelength_expectedValue(self):
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertEqual(channel.setEmWavelength(), '509')

    def test_setEmWavelength_missingKeys(self):
        channel = chnnl(['', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertIsNone(channel.setEmWavelength())

    def test_setEmWavelength_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, root)
        self.assertIsNone(channel.setEmWavelength())

    def test_setExposureTime_expectedValue(self):
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertEqual(channel.setExposureTime(), '950000000')

    def test_setExposureTime_missingKeys(self):
        channel = chnnl(['', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertIsNone(channel.setExposureTime())

    def test_setExposureTime_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, root)
        self.assertIsNone(channel.setExposureTime())

    def test_setEffectiveNA_expectedValue(self):
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertEqual(channel.setEffectiveNA(), '0.15')

    def test_setEffectiveNA_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, root)
        self.assertIsNone(channel.setEffectiveNA())

    def test_setImagingDevice_expectedValue(self):
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertEqual(channel.setImagingDevice(), 'Axiocam 503')

    def test_setImagingDevice_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, root)
        self.assertIsNone(channel.setImagingDevice())

    def test_setImagingDevice_missingKeys(self):
        tree = ET.parse(self.missingKeysPath)
        root = tree.getroot()
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, root)
        self.assertIsNone(channel.setImagingDevice())

    def test_setCameraAdapter_expectedValue(self):
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertEqual(channel.setCameraAdapter(), '1x Camera Adapter')

    def test_setCameraAdapter_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, root)
        self.assertIsNone(channel.setCameraAdapter())

    def test_setBinningMode_expectedValue(self):
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, self.meta.root)
        self.assertEqual(channel.setCameraAdapter(), '1x Camera Adapter')

    def test_setBinningMode_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        channel = chnnl(['Channel:0', 'EGFP', 'testCziFile.czi'], self.meta.filters, root)
        self.assertIsNone(channel.setCameraAdapter())


if __name__ == '__main__':
    unittest.main()
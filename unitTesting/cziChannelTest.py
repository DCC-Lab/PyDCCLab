from cziChannel import Channel as chnnl
from cziMetadata import Metadata as mtdt
import xml.etree.ElementTree as ET
import unittest
import os


class TestCziChannel(unittest.TestCase):
    def setUp(self):
        self.directory = os.path.dirname(os.path.dirname(__file__))
        self.testPath = os.path.join(self.directory, 'testData', 'testCziFile.czi')
        self.missingEntriesPath = os.path.join(self.directory, 'testData', 'MissingEntries.xml')
        self.missingKeysPath = os.path.join(self.directory, 'testData', 'MissingKeys.xml')

        self.meta = mtdt(self.testPath)
        self.meta.setAttributesFromXml()

        self.testXml = self.meta.extractXmlAsStringFromCziImageObject(self.meta.cziFileToCziImageObject())

    def test_setExWavelengthFilter_isEqual(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        channel.setExWavelengthFilter(self.meta.filters)
        self.assertEqual(channel.exWavelengthFilter, '450-490')

    def test_setEmWavelengthFilter_isEqual(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        channel.setEmWavelengthFilter(self.meta.filters)
        self.assertEqual(channel.emWavelengthFilter, '500-550')

    def test_setBeamsplitter_isEqual(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        channel.setBeamsplitter(self.meta.filters)
        self.assertEqual(channel.beamsplitter, '495')

    def test_getDataFromFilters_isEqual(self):
        root = ET.fromstring(self.testXml)
        channel_1 = chnnl('Channel:0', 'EGFP', root)
        channel_1.getDataFromFilters(self.meta.filters)

        channel_2 = chnnl('Channel:0', 'EGFP', root)
        channel_2.getDataFromFilters(self.meta.filters)

        self.assertEqual(channel_1, channel_2)

    def test_setReflector_isEqual(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        self.assertEqual(channel.setReflector(), '38 HE Green Fluorescent Prot')

    def test_setReflector_missingKeys(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)
        channel.channelId = ''

        with self.assertRaises(AttributeError): channel.setReflector()

    def test_setReflector_missingEntries(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        tree = ET.parse(self.missingEntriesPath)
        channel.root = tree.getroot()

        with self.assertRaises(AttributeError): channel.setReflector()

    def test_setContrastMethod_isEqual(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        self.assertEqual(channel.setContrastMethod(), 'Fluorescence')

    def test_setContrastMethod_missingKeys(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)
        channel.channelId = ''

        with self.assertRaises(AttributeError): channel.setContrastMethod()

    def test_setContrastMethod_missingEntries(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        tree = ET.parse(self.missingEntriesPath)
        channel.root = tree.getroot()

        with self.assertRaises(AttributeError): channel.setContrastMethod()

    def test_setLightSource_isEqual(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        self.assertEqual(channel.setLightSource(), 'HXP 120 V')

    def test_setLightSource_missingKeys(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)
        channel.channelId = ''

        with self.assertRaises(AttributeError): channel.setLightSource()

    def test_setLightSource_missingEntries(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        tree = ET.parse(self.missingEntriesPath)
        channel.root = tree.getroot()

        with self.assertRaises(AttributeError): channel.setLightSource()

    def test_setLightSourceIntensity_isEqual(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        self.assertEqual(channel.setLightSourceIntensity(), '58.32 %')

    def test_setLightSourceIntensity_missingKeys(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)
        channel.channelId = ''

        with self.assertRaises(AttributeError): channel.setLightSourceIntensity()

    def test_setLightSourceIntensity_missingEntries(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        tree = ET.parse(self.missingEntriesPath)
        channel.root = tree.getroot()

        with self.assertRaises(AttributeError): channel.setLightSourceIntensity()

    def test_setDyeName_isEqual(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        self.assertEqual(channel.setDyeName(), 'EGFP')

    def test_setDyeName_missingKeys(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)
        channel.channelId = ''

        with self.assertRaises(AttributeError): channel.setDyeName()

    def test_setDyeName_missingEntries(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        tree = ET.parse(self.missingEntriesPath)
        channel.root = tree.getroot()

        with self.assertRaises(AttributeError): channel.setDyeName()

    def test_setChannelColor_isEqual(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        self.assertEqual(channel.setChannelColor(), '#FF00FF5B')

    def test_setChannelColor_missingKeys(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)
        channel.channelId = ''

        with self.assertRaises(AttributeError): channel.setChannelColor()

    def test_setChannelColor_missingEntries(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        tree = ET.parse(self.missingEntriesPath)
        channel.root = tree.getroot()

        with self.assertRaises(AttributeError): channel.setChannelColor()

    def test_setExWavelength_isEqual(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        self.assertEqual(channel.setExWavelength(), '488')

    def test_setExWavelength_missingKeys(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)
        channel.channelId = ''

        with self.assertRaises(AttributeError): channel.setExWavelength()

    def test_setExWavelength_missingEntries(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        tree = ET.parse(self.missingEntriesPath)
        channel.root = tree.getroot()

        with self.assertRaises(AttributeError): channel.setExWavelength()

    def test_setEmWavelength_isEqual(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        self.assertEqual(channel.setEmWavelength(), '509')

    def test_setEmWavelength_missingKeys(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)
        channel.channelId = ''

        with self.assertRaises(AttributeError): channel.setEmWavelength()

    def test_setEmWavelength_missingEntries(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        tree = ET.parse(self.missingEntriesPath)
        channel.root = tree.getroot()

        with self.assertRaises(AttributeError): channel.setEmWavelength()

    def test_setExposureTime_isEqual(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        self.assertEqual(channel.setExposureTime(), '950000000')

    def test_setExposureTime_missingKeys(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)
        channel.channelId = ''

        with self.assertRaises(AttributeError): channel.setExposureTime()

    def test_setExposureTime_missingEntries(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        tree = ET.parse(self.missingEntriesPath)
        channel.root = tree.getroot()

        with self.assertRaises(AttributeError): channel.setExposureTime()

    def test_setEffectiveNA_isEqual(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        self.assertEqual(channel.setEffectiveNA(), '0.15')

    def test_setEffectiveNA_missingEntries(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        tree = ET.parse(self.missingEntriesPath)
        channel.root = tree.getroot()

        with self.assertRaises(AttributeError): channel.setEffectiveNA()

    def test_setImagingDevice_isEqual(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        self.assertEqual(channel.setImagingDevice(), 'Axiocam 503')

    def test_setImagingDevice_missingEntries(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        tree = ET.parse(self.missingEntriesPath)
        channel.root = tree.getroot()

        with self.assertRaises(AttributeError): channel.setImagingDevice()

    def test_setImagingDevice_missingKeys(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        tree = ET.parse(self.missingKeysPath)
        channel.root = tree.getroot()

        with self.assertRaises(KeyError): channel.setImagingDevice()

    def test_setCameraAdapter_isEqual(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        self.assertEqual(channel.setCameraAdapter(), '1x Camera Adapter')

    def test_setCameraAdapter_missingEntries(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        tree = ET.parse(self.missingEntriesPath)
        channel.root = tree.getroot()

        with self.assertRaises(AttributeError): channel.setCameraAdapter()

    def test_setBinningMode_isEqual(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        self.assertEqual(channel.setCameraAdapter(), '1x Camera Adapter')

    def test_setBinningMode_missingEntries(self):
        root = ET.fromstring(self.testXml)
        channel = chnnl('Channel:0', 'EGFP', root)

        tree = ET.parse(self.missingEntriesPath)
        channel.root = tree.getroot()

        with self.assertRaises(AttributeError): channel.setCameraAdapter()


if __name__ == '__main__':
    unittest.main()
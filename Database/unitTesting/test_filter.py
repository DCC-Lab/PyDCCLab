from filter import Filter as fltr
from metadata import Metadata as mtdt
import xml.etree.ElementTree as ET
import unittest
import os


class TestFilter(unittest.TestCase):
    def setUp(self):
        self.directory = os.path.dirname(os.path.dirname(__file__))
        self.testPath = os.path.join(self.directory, 'temporary_files', 'testCziFile.czi')
        self.missingEntriesPath = os.path.join(self.directory, 'temporary_files', 'MissingEntries.xml')
        self.missingKeysPath = os.path.join(self.directory, 'temporary_files', 'MissingKeys.xml')

        self.meta = mtdt(self.testPath)
        self.meta.setAttributesFromXml()
        self.defaultFilter = self.meta.filters[0]

        self.testXml = self.meta.extractXmlAsStringFromCziImageObject(self.meta.cziFileToCziImageObject())

    def test_setFilterSetId_isEqual(self):
        root = ET.fromstring(self.testXml)
        filter = fltr('Filter:2', '500', '550')

        filter.setFilterSetId(root)
        self.assertEqual(filter.filterSetId, self.defaultFilter.filterSetId)

    def test_setFilterSetId_rightFilterType(self):
        root = ET.fromstring(self.testXml)
        filter = fltr('Filter:1', '450', '490')

        filter.setFilterSetId(root)
        self.assertEqual(filter.filterType, 'Excitation')

    def test_setFilterSetId_missingKeys(self):
        tree = ET.parse(self.missingKeysPath)
        root = tree.getroot()
        filter = fltr('Filter:1', '450', '490')
        with self.assertRaises(KeyError): filter.setFilterSetId(root)

    def test_setFilterSetId_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        filter = fltr('Filter:1', '450', '490')
        with self.assertRaises(AttributeError): filter.setFilterSetId(root)

    def test_setChannelId_isEqual(self):
        root = ET.fromstring(self.testXml)
        filter = fltr('Filter:1', '450', '490')

        filter.setChannelId(root)
        self.assertEqual(filter.channelId, self.defaultFilter.channelId)

    def test_setChannelId_missingKeys(self):
        tree = ET.parse(self.missingKeysPath)
        root = tree.getroot()
        filter = fltr('Filter:1', '450', '490')

        with self.assertRaises(KeyError): filter.setChannelId(root)

    def test_setChannelId_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        filter = fltr('Filter:1', '450', '490')
        with self.assertRaises(AttributeError): filter.setChannelId(root)

    def test_setDichroicId_isEqual(self):
        root = ET.fromstring(self.testXml)
        filter = fltr('Filter:1', '450', '490')

        filter.setChannelId(root)
        filter.setDichroicId(root)
        self.assertEqual(filter.dichroicId, self.defaultFilter.dichroicId)

    def test_setDichroicId_missingKeys(self):
        tree = ET.parse(self.missingKeysPath)
        root = tree.getroot()
        filter = fltr('Filter:9', '999', '999')
        filter.filterSetId = 'FilterSet:1'

        with self.assertRaises(KeyError): filter.setDichroicId(root)

    def test_setDichroicId_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        filter = fltr('Filter:9', '999', '999')
        filter.filterSetId = 'FilterSet:1'

        with self.assertRaises(AttributeError): filter.setDichroicId(root)

    def test_setDichroic_isEqual(self):
        root = ET.fromstring(self.testXml)
        filter = fltr('Filter:1', '450', '490')

        filter.setChannelId(root)
        filter.setDichroic(root)
        self.assertEqual(filter.dichroic, self.defaultFilter.dichroic)

    def test_setDichroic_missingKeys(self):
        tree = ET.parse(self.missingKeysPath)
        root = tree.getroot()
        filter = fltr('Filter:2', '999', '999')
        filter.filterSetId = 'FilterSet:2'

        with self.assertRaises(AttributeError): filter.setDichroic(root)

    def test_setDichroic_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        filter = fltr('Filter:2', '999', '999')
        filter.filterSetId = 'FilterSet:2'

        with self.assertRaises(AttributeError): filter.setDichroic(root)

    def test_getType_isEqual(self):
        root = ET.fromstring(self.testXml)
        filter = fltr('Filter:2', '500', '550')
        filter.setChannelId(root)
        filter.setDichroic(root)

        self.assertEqual(filter.getType(), 'Emission')

    def test_getType_isNone(self):
        filter = fltr('Filter:2', '500', '550')

        self.assertIsNone(filter.getType())

    def test_getChannelId_isEqual(self):
        root = ET.fromstring(self.testXml)
        filter = fltr('Filter:2', '500', '550')
        filter.setChannelId(root)
        filter.setDichroic(root)

        self.assertEqual(filter.getChannelId(), 'Channel:0')

    def test_getChannelId_isNone(self):
        filter = fltr('Filter:2', '500', '550')

        self.assertIsNone(filter.getChannelId())

    def test_getFilterRange_isEqual(self):
        root = ET.fromstring(self.testXml)
        filter = fltr('Filter:2', '500', '550')
        filter.setChannelId(root)
        filter.setDichroic(root)

        self.assertEqual(filter.getFilterRange(), '500-550')

    def test_getDichroic_isEqual(self):
        root = ET.fromstring(self.testXml)
        filter = fltr('Filter:2', '500', '550')
        filter.setChannelId(root)
        filter.setDichroic(root)

        self.assertEqual(filter.getDichroic(), '495')

    def test_getDichroic_isNone(self):
        filter = fltr('Filter:2', '500', '550')

        self.assertIsNone(filter.getDichroic())


if __name__ == '__main__':
    unittest.main()
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


if __name__ == '__main__':
    unittest.main()
from Database.ImageMetadata.cziMetadata.cziFilter import CZIFilter as fltr
from Database.ImageMetadata.cziMetadata.cziMetadata import CZIMetadata as mtdt
import xml.etree.ElementTree as ET
import unittest
import os


class TestFilter(unittest.TestCase):
    def setUp(self):
        self.directory = os.path.dirname(os.path.dirname(__file__))
        self.testPath = os.path.join(self.directory, 'testData', 'testCziFile.czi')
        self.missingEntriesPath = os.path.join(self.directory, 'testData', 'MissingEntries.xml')
        self.meta = mtdt(self.testPath)

    def test_setFilterSetIdAndType_expectedValues(self):
        filter = fltr('Filter:1', self.meta.root)
        self.assertEqual(filter.setFilterSetIdAndFilterType(), ('FilterSet:1', 'Excitation'))

    def test_setFilterSetIdAndType_missingKeys(self):
        filter = fltr('', self.meta.root)
        self.assertIsNone(filter.setFilterSetIdAndFilterType()[0])

    def test_setFilterSetIdAndType_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        filter = fltr('Filter:1', root)
        self.assertIsNone(filter.setFilterSetIdAndFilterType()[0])

    def test_setChannelId_expectedValue(self):
        filter = fltr('Filter:1', self.meta.root)
        self.assertEqual(filter.setChannelId(), 'Channel:0')

    def test_setChannelId_missingKeys(self):
        filter = fltr('', self.meta.root)
        self.assertIsNone(filter.setChannelId())

    def test_setChannelId_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        filter = fltr('Filter:1', root)
        self.assertIsNone(filter.setChannelId())

    def test_setDichroicId_expectedValue(self):
        filter = fltr('Filter:1', self.meta.root)
        self.assertEqual(filter.setDichroicId(), 'Dichroic:1')

    def test_setDichroicId_missingKeys(self):
        filter = fltr('', self.meta.root)
        self.assertIsNone(filter.setDichroicId())

    def test_setDichroicId_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        filter = fltr('Filter:1', root)
        self.assertIsNone(filter.setDichroicId())

    def test_setDichroic_expectedValue(self):
        filter = fltr('Filter:1', self.meta.root)
        self.assertEqual(filter.setDichroic(), '495')

    def test_setDichroic_missingKeys(self):
        filter = fltr('', self.meta.root)
        self.assertIsNone(filter.setDichroic())

    def test_setDichroic_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        filter = fltr('Filter:1', root)
        self.assertIsNone(filter.setDichroic())

    def test_getType_expectedValue(self):
        filter = fltr('Filter:1', self.meta.root)
        self.assertEqual(filter.getType(), 'Excitation')

    def test_getType_noneValue(self):
        filter = fltr('', self.meta.root)
        self.assertIsNone(filter.getType())

    def test_getChannelId_expectedValue(self):
        filter = fltr('Filter:1', self.meta.root)
        self.assertEqual(filter.getChannelId(), 'Channel:0')

    def test_getChannelId_noneValue(self):
        filter = fltr('', self.meta.root)
        self.assertIsNone(filter.getChannelId())

    def test_getFilterRange_expectedValue(self):
        filter = fltr('Filter:1', self.meta.root)
        self.assertEqual(filter.getFilterRange(), '450-490')

    def test_getFilterRange_noneValues(self):
        filter = fltr('', self.meta.root)
        self.assertEqual(filter.getFilterRange(), 'None-None')

    def test_getDichroic_expectedValue(self):
        filter = fltr('Filter:1', self.meta.root)
        self.assertEqual(filter.getDichroic(), '495')

    def test_getDichroic_noneValue(self):
        filter = fltr('', self.meta.root)
        self.assertIsNone(filter.getDichroic())


if __name__ == '__main__':
    unittest.main()
import Database.management_xml.metadata as metadata
import Database.management_xml.filter as fltr
import Database.management_xml.channel as chnnl
import czifile as czi
import xml.etree.ElementTree as ET
import unittest
import os


class TestMetadata(unittest.TestCase):
    def test_cziFileToCziImageObject_isCziImageObject(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'testCziFile.czi')
        mdata = metadata.Metadata(filepath)

        self.assertIs(type(mdata.cziFileToCziImageObject()), czi.CziFile)

    def test_cziFileToCziImageObject_FileNotFoundError(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'wrongfilename.czi')
        mdata = metadata.Metadata(filepath)

        with self.assertRaises(FileNotFoundError): mdata.cziFileToCziImageObject()

    def test_cziFileToCziImageObject_ValueError(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'wrongFile.txt')
        mdata = metadata.Metadata(filepath)

        with self.assertRaises(ValueError): mdata.cziFileToCziImageObject()

    def test_extractXmlAsStringFromCziImageObject_returnsString(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'testCziFile.czi')
        mdata = metadata.Metadata(filepath)
        cziImageObject = mdata.cziFileToCziImageObject()

        self.assertIs(type(mdata.extractXmlAsStringFromCziImageObject(cziImageObject)), str)

    def test_extractXmlAsStringFromCziImageObject_wrongTypeOfObject(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'testCziFile.czi')
        mdata = metadata.Metadata(filepath)
        cziImageObject = 'WrongTypeOfObject'

        with self.assertRaises(AttributeError): mdata.extractXmlAsStringFromCziImageObject(cziImageObject)

    def test_createElementTreeRoot_returnsElement(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'testCziFile.czi')
        mdata = metadata.Metadata(filepath)

        self.assertIs(type(mdata.createElementTreeRoot()), ET.Element)

    def test_setMicroscope_isEqual(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'testCziFile.czi')
        mdata = metadata.Metadata(filepath)
        mdata.root = mdata.createElementTreeRoot()

        self.assertEqual(mdata.setMicroscope(), 'Axio Observer.Z1 / 7')

    def test_setMicroscope_noId(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'MissingKeys.xml')
        tree = ET.parse(filepath)
        mdata = metadata.Metadata(filepath)
        mdata.root = tree.getroot()

        with self.assertRaises(KeyError): mdata.setMicroscope()

    def test_setMicroscope_noEntry(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'MissingEntries.xml')
        tree = ET.parse(filepath)
        mdata = metadata.Metadata(filepath)
        mdata.root = tree.getroot()

        with self.assertRaises(AttributeError): mdata.setMicroscope()

    def test_setObjective_isEqual(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'testCziFile.czi')
        mdata = metadata.Metadata(filepath)
        mdata.root = mdata.createElementTreeRoot()

        self.assertEqual(mdata.setObjective(), 'LD A-Plan 5x/0.15 Ph1')

    def test_setObjective_noId(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'MissingKeys.xml')
        tree = ET.parse(filepath)
        mdata = metadata.Metadata(filepath)
        mdata.root = tree.getroot()

        with self.assertRaises(KeyError): mdata.setObjective()

    def test_setObjective_noEntry(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'MissingEntries.xml')
        tree = ET.parse(filepath)
        mdata = metadata.Metadata(filepath)
        mdata.root = tree.getroot()

        with self.assertRaises(AttributeError): mdata.setObjective()

    def test_setXScale_isEqual(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'testCziFile.czi')
        mdata = metadata.Metadata(filepath)
        mdata.root = mdata.createElementTreeRoot()

        self.assertEqual(mdata.setXScale(), '9.08E-07')

    def test_setXScale_noId(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'MissingKeys.xml')
        tree = ET.parse(filepath)
        mdata = metadata.Metadata(filepath)
        mdata.root = tree.getroot()

        with self.assertRaises(AttributeError): mdata.setXScale()

    def test_setXScale_noEntry(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'MissingEntries.xml')
        tree = ET.parse(filepath)
        mdata = metadata.Metadata(filepath)
        mdata.root = tree.getroot()

        with self.assertRaises(AttributeError): mdata.setXScale()

    def test_setYScale_isEqual(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'testCziFile.czi')
        mdata = metadata.Metadata(filepath)
        mdata.root = mdata.createElementTreeRoot()

        self.assertEqual(mdata.setYScale(), '9.08E-07')

    def test_setYScale_noId(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'MissingKeys.xml')
        tree = ET.parse(filepath)
        mdata = metadata.Metadata(filepath)
        mdata.root = tree.getroot()

        with self.assertRaises(AttributeError): mdata.setYScale()

    def test_setYScale_noEntry(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'MissingEntries.xml')
        tree = ET.parse(filepath)
        mdata = metadata.Metadata(filepath)
        mdata.root = tree.getroot()

        with self.assertRaises(AttributeError): mdata.setYScale()

    def test_setXSize_isEqual(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'testCziFile.czi')
        mdata = metadata.Metadata(filepath)
        mdata.root = mdata.createElementTreeRoot()

        self.assertEqual(mdata.setXSize(), '1936')

    def test_setXSize_noEntry(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'MissingEntries.xml')
        tree = ET.parse(filepath)
        mdata = metadata.Metadata(filepath)
        mdata.root = tree.getroot()

        with self.assertRaises(AttributeError): mdata.setXSize()

    def test_setYSize_isEqual(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'testCziFile.czi')
        mdata = metadata.Metadata(filepath)
        mdata.root = mdata.createElementTreeRoot()

        self.assertEqual(mdata.setYSize(), '1460')

    def test_setYSize_noEntry(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'MissingEntries.xml')
        tree = ET.parse(filepath)
        mdata = metadata.Metadata(filepath)
        mdata.root = tree.getroot()

        with self.assertRaises(AttributeError): mdata.setYSize()

    def test_setXScaled_isEqual(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'testCziFile.czi')
        mdata = metadata.Metadata(filepath)
        mdata.root = mdata.createElementTreeRoot()
        mdata.xSize = mdata.setXSize()
        mdata.xScale = mdata.setXScale()

        self.assertEqual(mdata.setXScaled(), 0.001757888)

    def test_setXScaled_wrongValue(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'testCziFile.czi')
        mdata = metadata.Metadata(filepath)
        mdata.root = mdata.createElementTreeRoot()
        mdata.xSize = mdata.setXSize()
        mdata.xScale = 'abcd'

        with self.assertRaises(ValueError): mdata.setXScaled()

    def test_setYScaled_isEqual(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'testCziFile.czi')
        mdata = metadata.Metadata(filepath)
        mdata.root = mdata.createElementTreeRoot()
        mdata.ySize = mdata.setYSize()
        mdata.yScale = mdata.setYScale()

        self.assertEqual(mdata.setYScaled(), 0.00132568)

    def test_setYScaled_wrongValue(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'testCziFile.czi')
        mdata = metadata.Metadata(filepath)
        mdata.root = mdata.createElementTreeRoot()
        mdata.ySize = mdata.setYSize()
        mdata.yScale = 'abcd'

        with self.assertRaises(ValueError): mdata.setYScaled()

    def test_findFiltersEntriesInXml_returnsListOfFilters(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'testCziFile.czi')
        mdata = metadata.Metadata(filepath)
        mdata.root = mdata.createElementTreeRoot()

        for filter in mdata.findFiltersEntriesInXml():
            self.assertIs(type(filter), fltr.Filter)

    def test_findFiltersEntriesInXml_missingEntries(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'MissingEntries.xml')
        tree = ET.parse(filepath)
        mdata = metadata.Metadata(filepath)
        mdata.root = tree.getroot()

        with self.assertRaises(AttributeError): mdata.findFiltersEntriesInXml()

    def test_findFiltersEntriesInXml_noId(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'MissingKeys.xml')
        tree = ET.parse(filepath)
        mdata = metadata.Metadata(filepath)
        mdata.root = tree.getroot()

        with self.assertRaises(KeyError): mdata.findFiltersEntriesInXml()

    def test_setFiltersData_isNotEqual(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'testCziFile.czi')
        mdata = metadata.Metadata(filepath)
        mdata.root = mdata.createElementTreeRoot()

        self.assertNotEqual(mdata.findFiltersEntriesInXml(), mdata.setFiltersData())

    def test_findChannelsEntriesInXml_returnsListOfChannels(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'testCziFile.czi')
        mdata = metadata.Metadata(filepath)
        mdata.root = mdata.createElementTreeRoot()

        for channel in mdata.findChannelsEntriesInXml():
            self.assertIs(type(channel), chnnl.Channel)

    def test_findChannelsEntriesInXml_missingEntries(self):  # TODO This doesn't work for now.
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'MissingEntries.xml')
        tree = ET.parse(filepath)
        mdata = metadata.Metadata(filepath)
        mdata.root = tree.getroot()
        mdata.findChannelsEntriesInXml()
        #with self.assertRaises(ValueError): mdata.findChannelsEntriesInXml()

    def test_findChannelsEntriesInXml_noId(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(directory, 'temporary_files', 'MissingKeys.xml')
        tree = ET.parse(filepath)
        mdata = metadata.Metadata(filepath)
        mdata.root = tree.getroot()

        with self.assertRaises(KeyError): mdata.findChannelsEntriesInXml()


if __name__ == '__main__':
    unittest.main()
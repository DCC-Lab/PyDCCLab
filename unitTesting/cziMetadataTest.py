import cziMetadata as mtdt
import cziFilter as fltr
import cziChannel as chnnl
import czifile as czi
import xml.etree.ElementTree as ET
import unittest
import os


class TestMetadata(unittest.TestCase):
    def setUp(self):
        self.directory = os.path.dirname(os.path.dirname(__file__))
        self.testPath = os.path.join(self.directory, 'testData', 'testCziFile.czi')
        self.wrongFilePath = os.path.join(self.directory, 'testData', 'wrongfilename.czi')
        self.wrongFileType = os.path.join(self.directory, 'testData', 'wrongFile.txt')
        self.missingEntriesPath = os.path.join(self.directory, 'testData', 'MissingEntries.xml')
        self.missingKeysPath = os.path.join(self.directory, 'testData', 'MissingKeys.xml')

    def test_cziFileToCziImageObject_isCziImageObject(self):
        mdata = mtdt.CZIMetadata(self.testPath)

        self.assertIs(type(mdata.cziFileToCziImageObject()), czi.CziFile)

    def test_cziFileToCziImageObject_FileNotFoundError(self):
        mdata = mtdt.CZIMetadata(self.wrongFilePath)

        with self.assertRaises(FileNotFoundError): mdata.cziFileToCziImageObject()

    def test_cziFileToCziImageObject_ValueError(self):
        mdata = mtdt.CZIMetadata(self.wrongFileType)

        with self.assertRaises(ValueError): mdata.cziFileToCziImageObject()

    def test_extractXmlAsStringFromCziImageObject_returnsString(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        cziImageObject = mdata.cziFileToCziImageObject()

        self.assertIs(type(mdata.extractXmlAsStringFromCziImageObject(cziImageObject)), str)

    def test_extractXmlAsStringFromCziImageObject_wrongTypeOfObject(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        cziImageObject = 'WrongTypeOfObject'

        with self.assertRaises(AttributeError): mdata.extractXmlAsStringFromCziImageObject(cziImageObject)

    def test_createElementTreeRoot_returnsElement(self):
        mdata = mtdt.CZIMetadata(self.testPath)

        self.assertIs(type(mdata.createElementTreeRoot()), ET.Element)

    def test_setMicroscope_isEqual(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        mdata.root = mdata.createElementTreeRoot()

        self.assertEqual(mdata.setMicroscope(), 'Axio Observer.Z1 / 7')

    def test_setMicroscope_noId(self):
        tree = ET.parse(self.missingKeysPath)
        mdata = mtdt.CZIMetadata(self.missingKeysPath)
        mdata.root = tree.getroot()

        with self.assertRaises(KeyError): mdata.setMicroscope()

    def test_setMicroscope_noEntry(self):
        tree = ET.parse(self.missingEntriesPath)
        mdata = mtdt.CZIMetadata(self.missingEntriesPath)
        mdata.root = tree.getroot()

        with self.assertRaises(AttributeError): mdata.setMicroscope()

    def test_setObjective_isEqual(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        mdata.root = mdata.createElementTreeRoot()

        self.assertEqual(mdata.setObjective(), 'LD A-Plan 5x/0.15 Ph1')

    def test_setObjective_noId(self):
        tree = ET.parse(self.missingKeysPath)
        mdata = mtdt.CZIMetadata(self.missingKeysPath)
        mdata.root = tree.getroot()

        with self.assertRaises(KeyError): mdata.setObjective()

    def test_setObjective_noEntry(self):
        tree = ET.parse(self.missingEntriesPath)
        mdata = mtdt.CZIMetadata(self.missingEntriesPath)
        mdata.root = tree.getroot()

        with self.assertRaises(AttributeError): mdata.setObjective()

    def test_setXScale_isEqual(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        mdata.root = mdata.createElementTreeRoot()

        self.assertEqual(mdata.setXScale(), '9.08E-07')

    def test_setXScale_noId(self):
        tree = ET.parse(self.missingKeysPath)
        mdata = mtdt.CZIMetadata(self.missingKeysPath)
        mdata.root = tree.getroot()

        with self.assertRaises(AttributeError): mdata.setXScale()

    def test_setXScale_noEntry(self):
        tree = ET.parse(self.missingEntriesPath)
        mdata = mtdt.CZIMetadata(self.missingEntriesPath)
        mdata.root = tree.getroot()

        with self.assertRaises(AttributeError): mdata.setXScale()

    def test_setYScale_isEqual(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        mdata.root = mdata.createElementTreeRoot()

        self.assertEqual(mdata.setYScale(), '9.08E-07')

    def test_setYScale_noId(self):
        tree = ET.parse(self.missingKeysPath)
        mdata = mtdt.CZIMetadata(self.missingKeysPath)
        mdata.root = tree.getroot()

        with self.assertRaises(AttributeError): mdata.setYScale()

    def test_setYScale_noEntry(self):
        tree = ET.parse(self.missingEntriesPath)
        mdata = mtdt.CZIMetadata(self.missingEntriesPath)
        mdata.root = tree.getroot()

        with self.assertRaises(AttributeError): mdata.setYScale()

    def test_setXSize_isEqual(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        mdata.root = mdata.createElementTreeRoot()

        self.assertEqual(mdata.setXSize(), '1936')

    def test_setXSize_noEntry(self):
        tree = ET.parse(self.missingEntriesPath)
        mdata = mtdt.CZIMetadata(self.missingEntriesPath)
        mdata.root = tree.getroot()

        with self.assertRaises(AttributeError): mdata.setXSize()

    def test_setYSize_isEqual(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        mdata.root = mdata.createElementTreeRoot()

        self.assertEqual(mdata.setYSize(), '1460')

    def test_setYSize_noEntry(self):
        tree = ET.parse(self.missingEntriesPath)
        mdata = mtdt.CZIMetadata(self.missingEntriesPath)
        mdata.root = tree.getroot()

        with self.assertRaises(AttributeError): mdata.setYSize()

    def test_setXScaled_isEqual(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        mdata.root = mdata.createElementTreeRoot()
        mdata.xSize = mdata.setXSize()
        mdata.xScale = mdata.setXScale()

        self.assertEqual(mdata.setXScaled(), 0.001757888)

    def test_setXScaled_wrongValue(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        mdata.root = mdata.createElementTreeRoot()
        mdata.xSize = mdata.setXSize()
        mdata.xScale = 'abcd'

        with self.assertRaises(ValueError): mdata.setXScaled()

    def test_setYScaled_isEqual(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        mdata.root = mdata.createElementTreeRoot()
        mdata.ySize = mdata.setYSize()
        mdata.yScale = mdata.setYScale()

        self.assertEqual(mdata.setYScaled(), 0.00132568)

    def test_setYScaled_wrongValue(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        mdata.root = mdata.createElementTreeRoot()
        mdata.ySize = mdata.setYSize()
        mdata.yScale = 'abcd'

        with self.assertRaises(ValueError): mdata.setYScaled()

    def test_findFiltersEntriesInXml_returnsListOfFilters(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        mdata.root = mdata.createElementTreeRoot()

        for filter in mdata.findFiltersInRoot():
            self.assertIs(type(filter), fltr.CZIFilter)

    def test_findFiltersEntriesInXml_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        mdata = mtdt.CZIMetadata(self.missingEntriesPath)
        mdata.root = tree.getroot()

        with self.assertRaises(AttributeError): mdata.findFiltersInRoot()

    def test_findFiltersEntriesInXml_noId(self):
        tree = ET.parse(self.missingKeysPath)
        mdata = mtdt.CZIMetadata(self.missingKeysPath)
        mdata.root = tree.getroot()

        with self.assertRaises(KeyError): mdata.findFiltersInRoot()

    def test_setFiltersData_isEqual(self):
        mdata_1 = mtdt.CZIMetadata(self.testPath)
        mdata_1.root = mdata_1.createElementTreeRoot()

        mdata_2 = mtdt.CZIMetadata(self.testPath)
        mdata_2.root = mdata_2.createElementTreeRoot()

        self.assertEqual(mdata_1.setFiltersData(), mdata_2.setFiltersData())

    def test_setFiltersData_isNotEqual(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        mdata.root = mdata.createElementTreeRoot()

        self.assertNotEqual(mdata.findFiltersInRoot(), mdata.setFiltersData())

    def test_findChannelsEntriesInXml_returnsListOfChannels(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        mdata.root = mdata.createElementTreeRoot()

        for channel in mdata.findChannelsInRoot():
            self.assertIs(type(channel), chnnl.CZIChannel)

    def test_findChannelsEntriesInXml_missingEntries(self):
        tree = ET.parse(self.missingEntriesPath)
        mdata = mtdt.CZIMetadata(self.missingEntriesPath)
        mdata.root = tree.getroot()

        with self.assertRaises(AttributeError): mdata.findChannelsInRoot()

    def test_findChannelsEntriesInXml_noId(self):
        tree = ET.parse(self.missingKeysPath)
        mdata = mtdt.CZIMetadata(self.missingKeysPath)
        mdata.root = tree.getroot()

        with self.assertRaises(KeyError): mdata.findChannelsInRoot()

    def test_setChannelsData_isEqual(self):
        mdata_1 = mtdt.CZIMetadata(self.testPath)
        mdata_1.root = mdata_1.createElementTreeRoot()
        mdata_1.filters = mdata_1.setFiltersData()

        mdata_2 = mtdt.CZIMetadata(self.testPath)
        mdata_2.root = mdata_2.createElementTreeRoot()
        mdata_2.filters = mdata_2.setFiltersData()

        self.assertEqual(mdata_1.setChannelsData(), mdata_2.setChannelsData())

    def test_setChannelsData_isNotEqual(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        mdata.root = mdata.createElementTreeRoot()
        mdata.filters = mdata.setFiltersData()

        self.assertNotEqual(mdata.findChannelsInRoot(), mdata.setChannelsData())

    def test_checkIfElementHasChildren_hasChildren(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        mdata.root = mdata.createElementTreeRoot()
        root = mdata.root.find('./Metadata/Information/Image/Dimensions/Channels')

        self.assertTrue(mdata.checkIfElementHasChildren(root))

    def test_checkIfElementHasChildren_hasNoChildren(self):
        tree = ET.parse(self.missingEntriesPath)
        mdata = mtdt.CZIMetadata(self.missingEntriesPath)
        mdata.root = tree.getroot()
        root = mdata.root.find('./Metadata/Information/Image/Dimensions/Channels')

        with self.assertRaises(AttributeError): mdata.checkIfElementHasChildren(root)

    def test_setAttributeFromXml_isEqual(self):
        mdata_1 = mtdt.CZIMetadata(self.testPath)
        mdata_1.setAttributesFromXml()
        mdata_2 = mtdt.CZIMetadata(self.testPath)
        mdata_2.setAttributesFromXml()

        self.assertEqual(mdata_1, mdata_2)

    def test_setAttributeFromXml_isNotEqual(self):
        mdata_1 = mtdt.CZIMetadata(self.testPath)
        mdata_1.setAttributesFromXml()
        mdata_2 = mtdt.CZIMetadata(self.testPath)

        self.assertNotEqual(mdata_1, mdata_2)

    def test_exportDataAsDict_isEqual(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        mdata.setAttributesFromXml()

        expectedValue = {'name': None, 'mouse_id': None,
                         'path': 'C:\\Users\\MathieuLaptop\\Documents\\Ulaval\\ProgPython\\Projets\\BigData-ImageAnalysis\\testData\\testCziFile.czi',
                         'microscope': 'Axio Observer.Z1 / 7', 'objective': 'LD A-Plan 5x/0.15 Ph1', 'x_size': '1936',
                         'y_size': '1460', 'x_scale': '9.08E-07', 'y_scale': '9.08E-07', 'x_scaled': 0.001757888,
                         'y_scaled': 0.00132568, 'vectors': None}
        self.assertEqual(mdata.exportAsDict(), expectedValue)

    def test_getChannels_isEqual(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        mdata.setAttributesFromXml()

        expectedValue = []
        for channel in mdata.channels:
            expectedValue.append(channel)
        self.assertEqual(mdata.getChannels(), expectedValue)

    def test_getName_isEqual(self):
        mdata = mtdt.CZIMetadata(self.testPath, 'testName')

        self.assertEqual(mdata.getName(), 'testName')

    def test_setMouseId_isEqual(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        mdata.setMouseId('123')

        self.assertEqual(mdata.mouseId, '123')

    def test_setVectors_isEqual(self):
        mdata = mtdt.CZIMetadata(self.testPath)
        mdata.setVectors('abc123')

        self.assertEqual(mdata.vectors, 'abc123')


if __name__ == '__main__':
    unittest.main()

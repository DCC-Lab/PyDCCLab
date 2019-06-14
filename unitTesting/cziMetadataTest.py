from Database.ImageMetadata import CZIMetadata as mtdt
from dcclab import readCziImage
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

    def test_cziImageObjectFromPath_isCziImageObject(self):
        mdata = mtdt(self.testPath)
        self.assertIs(type(mdata.cziImageObjectFromPath()), type(readCziImage(self.testPath)))

    def test_cziImageObjectFromPath_fileNotFound(self):
        mdata = mtdt(self.testPath)
        mdata.path = self.wrongFilePath
        with self.assertRaises(FileNotFoundError): mdata.cziImageObjectFromPath()

    def test_cziFileToCziImageObject_wrongFileType(self):
        mdata = mtdt(self.testPath)
        mdata.path = self.wrongFileType
        with self.assertRaises(ValueError): mdata.cziImageObjectFromPath()

    def test_xmlFromCziImageObject_returnsString(self):
        mdata = mtdt(self.testPath)
        cziImageObject = mdata.cziImageObjectFromPath()
        self.assertIs(type(mdata.xmlFromCziImageObject(cziImageObject)), str)

    def test_xmlFromCziImageObject_wrongTypeOfObject(self):
        mdata = mtdt(self.testPath)
        cziImageObject = 'WrongTypeOfObject'
        with self.assertRaises(AttributeError): mdata.xmlFromCziImageObject(cziImageObject)

    def test_createElementTreeRoot_returnsElement(self):
        mdata = mtdt(self.testPath)
        self.assertIs(type(mdata.createElementTreeRoot()), ET.Element)

    def test_setMicroscope_expectedValue(self):
        mdata = mtdt(self.testPath)
        self.assertEqual(mdata.setMicroscope(), 'Axio Observer.Z1 / 7')

    def test_setMicroscope_missingKey(self):
        mdata = mtdt(self.testPath)
        tree = ET.parse(self.missingKeysPath)
        mdata.root = tree.getroot()
        self.assertIsNone(mdata.setMicroscope())

    def test_setMicroscope_missingEntries(self):
        mdata = mtdt(self.testPath)
        tree = ET.parse(self.missingEntriesPath)
        mdata.root = tree.getroot()
        self.assertIsNone(mdata.setMicroscope())

    def test_setObjective_expectedValue(self):
        mdata = mtdt(self.testPath)
        self.assertEqual(mdata.setObjective(), 'LD A-Plan 5x/0.15 Ph1')

    def test_setObjective_missingKey(self):
        mdata = mtdt(self.testPath)
        tree = ET.parse(self.missingKeysPath)
        mdata.root = tree.getroot()
        self.assertIsNone(mdata.setObjective())

    def test_setObjective_missingEntries(self):
        mdata = mtdt(self.testPath)
        tree = ET.parse(self.missingEntriesPath)
        mdata.root = tree.getroot()
        self.assertIsNone(mdata.setObjective())

    def test_setXScale_expectedValue(self):
        mdata = mtdt(self.testPath)
        self.assertEqual(mdata.setXScale(), '9.08E-07')

    def test_setXScale_missingKey(self):
        mdata = mtdt(self.testPath)
        tree = ET.parse(self.missingKeysPath)
        mdata.root = tree.getroot()
        self.assertIsNone(mdata.setXScale())

    def test_setXScale_missingEntries(self):
        mdata = mtdt(self.testPath)
        tree = ET.parse(self.missingEntriesPath)
        mdata.root = tree.getroot()
        self.assertIsNone(mdata.setXScale())

    def test_setYScale_expectedValue(self):
        mdata = mtdt(self.testPath)
        self.assertEqual(mdata.setYScale(), '9.08E-07')

    def test_setYScale_missingKey(self):
        mdata = mtdt(self.testPath)
        tree = ET.parse(self.missingKeysPath)
        mdata.root = tree.getroot()
        self.assertIsNone(mdata.setYScale())

    def test_setYScale_missingEntries(self):
        mdata = mtdt(self.testPath)
        tree = ET.parse(self.missingEntriesPath)
        mdata.root = tree.getroot()
        self.assertIsNone(mdata.setYScale())

    def test_setXSize_expectedValue(self):
        mdata = mtdt(self.testPath)
        self.assertEqual(mdata.setXSize(), '1936')

    def test_setXSize_missingEntries(self):
        mdata = mtdt(self.testPath)
        tree = ET.parse(self.missingEntriesPath)
        mdata.root = tree.getroot()
        self.assertIsNone(mdata.setXSize())

    def test_setYSize_expectedValue(self):
        mdata = mtdt(self.testPath)
        self.assertEqual(mdata.setYSize(), '1460')

    def test_setYSize_missingEntries(self):
        mdata = mtdt(self.testPath)
        tree = ET.parse(self.missingEntriesPath)
        mdata.root = tree.getroot()
        self.assertIsNone(mdata.setYSize())

    def test_xScaled_expectedValue(self):
        mdata = mtdt(self.testPath)
        self.assertEqual(mdata.xScaled, 0.001757888)

    def test_xScaled_wrongValue(self):
        mdata = mtdt(self.testPath)
        mdata.xScale = 'abcd'
        self.assertIsNone(mdata.xScaled)

    def test_yScaled_expectedValue(self):
        mdata = mtdt(self.testPath)
        self.assertEqual(mdata.yScaled, 0.00132568)

    def test_yScaled_wrongValue(self):
        mdata = mtdt(self.testPath)
        mdata.yScale = 'abcd'
        self.assertIsNone(mdata.yScaled)

    def test_findFiltersInRoot_returnsListOfFilters(self):
        mdata = mtdt(self.testPath)
        testFilters = ['Filter:1', 'Filter:2', 'Filter:3', 'Filter:4']
        for filter, testFilter in zip(mdata.findFiltersInRoot(), testFilters):
            self.assertEqual(filter.filterId, testFilter)

    def test_findFiltersInRoot_missingEntries(self):
        mdata = mtdt(self.testPath)
        tree = ET.parse(self.missingEntriesPath)
        mdata.root = tree.getroot()
        for filter in mdata.findFiltersInRoot():
            self.assertIsNone(filter.filterType)

    def test_findFiltersInRoot_missingKey(self):
        mdata = mtdt(self.testPath)
        tree = ET.parse(self.missingKeysPath)
        mdata.root = tree.getroot()
        for filter in mdata.findFiltersInRoot():
            self.assertIsNone(filter.channelId)

    def test_findChannelsInRoot_returnsListOfChannels(self):
        mdata = mtdt(self.testPath)
        testChannels = ['Channel:0', 'Channel:1']
        for channel, testChannel in zip(mdata.findChannelsInRoot(), testChannels):
            self.assertEqual(channel.channelId, testChannel)

    def test_findChannelsInRoot_missingEntries(self):
        mdata = mtdt(self.testPath)
        tree = ET.parse(self.missingEntriesPath)
        mdata.root = tree.getroot()
        for channel in mdata.findChannelsInRoot():
            self.assertIsNone(channel)

    def test_checkIfElementHasChildren_hasChildren(self):
        mdata = mtdt(self.testPath)
        root = mdata.root.find('./Metadata/Information/Image/Dimensions/Channels')
        self.assertTrue(mdata.checkIfElementHasChildren(root))

    def test_checkIfElementHasChildren_hasNoChildren(self):
        mdata = mtdt(self.testPath)
        tree = ET.parse(self.missingEntriesPath)
        root = tree.getroot()
        newRoot = root.find('./Metadata/Information/Image/Dimensions/Channels')
        self.assertFalse(mdata.checkIfElementHasChildren(newRoot))

    def test_checkIfElementHasChildren_elementIsNone(self):
        mdata = mtdt(self.testPath)
        self.assertFalse(mdata.checkIfElementHasChildren(None))

    def test_asDict_expectedValue(self):
        mdata = mtdt(self.testPath)
        expectedValue = {
            'path': 'C:\\Users\\MathieuLaptop\\Documents\\Ulaval\\ProgPython\\Projets\\BigData-ImageAnalysis\\testData\\testCziFile.czi',
            'microscope': 'Axio Observer.Z1 / 7', 'objective': 'LD A-Plan 5x/0.15 Ph1', 'x_size': '1936',
            'y_size': '1460', 'x_scale': '9.08E-07', 'y_scale': '9.08E-07', 'x_scaled': 0.001757888,
            'y_scaled': 0.00132568, 'name': 'testCziFile.czi', 'mouse_id': None, 'viral_vectors': '', 'injection_site': None, 'tags': ''}
        self.assertEqual(mdata.asDict(), expectedValue)

    def test_setMouseId_upperCase(self):
        mdata = mtdt(self.testPath, 'S123_test_czi')
        self.assertEqual(mdata.setMouseId(), '123')

    def test_setMouseId_lowerCase(self):
        mdata = mtdt(self.testPath, 's123_test_czi')
        self.assertEqual(mdata.setMouseId(), '123')

    def test_setMouseId_lessDigits(self):
        mdata = mtdt(self.testPath, 's1_test_czi')
        self.assertEqual(mdata.setMouseId(), '1')

    def test_setMouseId_moreDigits(self):
        mdata = mtdt(self.testPath, 's1234_test_czi')
        self.assertEqual(mdata.setMouseId(), '1234')

    def test_setMouseId_noIdFound(self):
        mdata = mtdt(self.testPath, 'test_czi')
        self.assertIsNone(mdata.setMouseId())

    def test_findRabVectors_upperCase(self):
        mdata = mtdt(self.testPath, 'RAB1.2_RABV3.2_czi')
        self.assertEqual(mdata.findRabVectors(), 'RAB1.2;RABV3.2')

    def test_findRabVectors_lowerCase(self):
        mdata = mtdt(self.testPath, 'rab1.2_rabv3.2_czi')
        self.assertEqual(mdata.findRabVectors(), 'rab1.2;rabv3.2')

    def test_findRabVectors_expectedValues(self):
        mdata = mtdt(self.testPath, 'rab1_rabv1_RAB1.1_rabv1.1_czi')
        self.assertEqual(mdata.findRabVectors(), 'rab1;rabv1;RAB1.1;rabv1.1')

    def test_findRabVectors_noVectorsFound(self):
        mdata = mtdt(self.testPath, 'test_czi')
        self.assertFalse(mdata.findRabVectors())

    def test_findRabVectors_wrongValue(self):
        mdata = mtdt(self.testPath, 'test_czi')
        mdata.name = 0
        self.assertIsNone(mdata.findRabVectors())

    def test_findAAVVectors_upperCase(self):
        mdata = mtdt(self.testPath, 'AAV123_czi')
        self.assertEqual(mdata.findAAVVectors(), 'AAV123')

    def test_findAAVVectors_lowerCase(self):
        mdata = mtdt(self.testPath, 'aav112_czi')
        self.assertEqual(mdata.findAAVVectors(), 'aav112')

    def test_findAAVVectors_plusSeparator(self):
        mdata = mtdt(self.testPath, 'AAV123+456_czi')
        self.assertEqual(mdata.findAAVVectors(), 'AAV123;AAV456')

    def test_findAAVVectors_minusSeparator(self):
        mdata = mtdt(self.testPath, 'AAV789-101_czi')
        self.assertEqual(mdata.findAAVVectors(), 'AAV789;AAV101')

    def test_findAAVVectors_expectedValues(self):
        mdata = mtdt(self.testPath, 'AAV123+456_AAV789-101_aav112_czi')
        self.assertEqual(mdata.findAAVVectors(), 'AAV123;AAV456;AAV789;AAV101;aav112')

    def test_findAAVVectors_noVectorsFound(self):
        mdata = mtdt(self.testPath, 'test_czi')
        self.assertFalse(mdata.findAAVVectors())

    def test_findAAVVectors_wrongValue(self):
        mdata = mtdt(self.testPath, 'test_czi')
        mdata.name = 0
        self.assertIsNone(mdata.findAAVVectors())

    def test_setViralVectors_expectedValue(self):
        mdata = mtdt(self.testPath, 'AAV123_rab2_test_czi')
        self.assertEqual(mdata.setViralVectors(), 'AAV123;rab2')

    def test_setViralVectors_noVectorsFound(self):
        mdata = mtdt(self.testPath, 'test_czi')
        self.assertFalse(mdata.setViralVectors())

    def test_setViralVectors_wrongValue(self):
        mdata = mtdt(self.testPath, 'test_czi')
        mdata.name = 0
        self.assertIsNone(mdata.setViralVectors())

    def test_setInjectionSite_upperCase(self):
        mdata = mtdt(self.testPath, 'AAV425_PATTE_DRG-02.czi')
        self.assertEqual(mdata.setInjectionSite(), 'PATTE')

    def test_setInjectionSite_lowerCase(self):
        mdata = mtdt(self.testPath, 'AAV425_iv_DRG-02.czi')
        self.assertEqual(mdata.setInjectionSite(), 'iv')

    def test_setInjectionSite_noInjectionSiteFound(self):
        mdata = mtdt(self.testPath, 'AAV425_DRG-02.czi')
        self.assertFalse(mdata.setInjectionSite())

    def test_setInjectionSite_wrongValue(self):
        mdata = mtdt(self.testPath, 'AAV425_DRG-02.czi')
        mdata.name = 0
        self.assertIsNone(mdata.setInjectionSite())

    def test_setTags_upperCase(self):
        mdata = mtdt(self.testPath, 'AAV425_patte_NEURONES_czi')
        self.assertEqual(mdata.setTags(), 'NEURONES')

    def test_setTags_lowerCase(self):
        mdata = mtdt(self.testPath, 'AAV425_patte_moelle_czi')
        self.assertEqual(mdata.setTags(), 'moelle')

    def test_setTags_withSpace(self):
        mdata = mtdt(self.testPath, 'AAV400_anti rabbit-03.czi')
        self.assertEqual(mdata.setTags(), 'antirabbit')

    def test_setTags_duplicates(self):
        mdata = mtdt(self.testPath, 'AAV400_moelle_moelle-03.czi')
        self.assertEqual(mdata.setTags(), 'moelle')

    def test_setTags_expectedValues(self):
        mdata = mtdt(self.testPath, 'AAV400_cerveau_moelle_neurones_BB-03.czi')
        self.assertEqual(mdata.setTags(), 'moelle;neurones;BB')

    def test_setTags_noTagsFound(self):
        mdata = mtdt(self.testPath, 'AAV400_cerveau-03.czi')
        self.assertFalse(mdata.setTags())

    def test_setTags_wrongValue(self):
        mdata = mtdt(self.testPath, 'AAV400_cerveau-03.czi')
        mdata.name = 0
        self.assertFalse(mdata.setTags())

    def test_nameFromPath_expectedValue(self):
        mdata = mtdt(self.testPath)
        self.assertEqual(mdata.nameFromPath(), 'testCziFile.czi')

    def test_nameFromPath_noPath(self):
        mdata = mtdt(self.testPath)
        mdata.path = ''
        self.assertEqual(mdata.nameFromPath(), '')

    def test_nameFromPath_wrongType(self):
        mdata = mtdt(self.testPath)
        mdata.path = 0
        self.assertIsNone(mdata.nameFromPath())


if __name__ == '__main__':
    unittest.main()

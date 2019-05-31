import unittest
from DCCImagesFromFiles import *
from DCCImage import *
import DCCImagesExceptions as DCCExcep


class TestDCCImagesFromCZIFileConstructor(unittest.TestCase):

    def testInvalidPathConstructor(self):
        with self.assertRaises(FileNotFoundError):
            DCCImagesFromCZIFile("noSuchFile.czi")

    def testNotCziFile(self):
        with self.assertRaises(ValueError):
            DCCImagesFromCZIFile("testNotCziFile.jpg")

    def testCorrectPath(self):
        imagesFromCzi = DCCImagesFromCZIFile("testCziFile2Images.czi")
        self.assertIsInstance(imagesFromCzi, DCCImagesFromCZIFile)


class testDCCImagesFromCZIFileMethods(unittest.TestCase):

    def setUp(self) -> None:
        import ImageAnalysis.source.cziUtil as cziUtil
        self.imagesFromCzi = DCCImagesFromCZIFile("testCziFile2Images.czi")
        self.metadata = cziUtil.extractMetadataFromCziFileObject(cziUtil.readCziImage("testCziFile2Images.czi"))

    def testGetMetadata(self):
        self.assertTrue(self.metadata == self.imagesFromCzi.getMetadata())

    def testSetMetadataAll(self):
        self.imagesFromCzi.setMetadata("New Metadata")
        self.assertTrue("New Metadata" == self.imagesFromCzi.getMetadata())

    def testSetMetadataEveryImageCheck(self):
        self.imagesFromCzi.setMetadata("Hello")
        self.assertTrue(all(image.getMetadata() == "Hello" for image in self.imagesFromCzi.asList()))

    def testSetMetadataInvalidNotAString(self):
        with self.assertRaises(TypeError):
            self.imagesFromCzi.setMetadata(123432)

    def testSaveMetadataInvalidName(self):
        with self.assertRaises(DCCExcep.InvalidMetadataFileNameException):
            self.imagesFromCzi.saveMetadata("/*")

    def testSaveMetadataValidName(self):
        import os
        self.imagesFromCzi.saveMetadata("testSaveMetaDCCImagesTest")
        isSaved = True
        try:
            os.remove("testSaveMetaDCCImagesTest.xml")
        except FileNotFoundError:
            isSaved = False
        self.assertTrue(isSaved)

    def testGetPath(self):
        self.assertTrue("testCziFile2Images.czi" == self.imagesFromCzi.getPath())


class TestDCCImageFromNormalFileConstructor(unittest.TestCase):

    def testInvalidConstructorNotASupportedImageFormat(self):
        file = "testSaveMetaDCCImagesTest.xml"
        with self.assertRaises(OSError):
            DCCImageFromNormalFile(file)

    def testInvalidConstructorTIFFFile(self):
        file = "testTiff3Images.tiff"
        with self.assertRaises(DCCExcep.InvalidFileFormatException):
            DCCImageFromNormalFile(file)

    def testInvalidConstructorCZIFile(self):
        file = "testCziFile2Images.czi"
        with self.assertRaises(DCCExcep.InvalidFileFormatException):
            DCCImageFromNormalFile(file)

    def testValidConstructor(self):
        file = "testNotCziFile.jpg"
        imageFromJPG = DCCImageFromNormalFile(file)
        self.assertIsInstance(imageFromJPG, DCCImageFromNormalFile)


class TestDCCImageFromNormalFileMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.imageFromJPG = DCCImageFromNormalFile("testNotCziFile.jpg")

    def testGetPath(self):
        self.assertTrue(self.imageFromJPG.getPath() == "testNotCziFile.jpg")


class TestDCCImagesFromTiffFileConstructor(unittest.TestCase):

    def testInvalidConstructorNotSupportedFile(self):
        with self.assertRaises(DCCExcep.InvalidFileFormatException):
            DCCImagesFromTiffFile("testNotCziFile.jpg")

    def testValidConstructor(self):
        imageFromTiff = DCCImagesFromTiffFile("testTiff3Images.tiff")
        self.assertIsInstance(imageFromTiff, DCCImagesFromTiffFile)


class TestDCCImagesFromTiffFileMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.images = DCCImagesFromTiffFile("testTiff3Images.tiff")

    def testGetMetadata(self):
        import tifffile
        metadata = tifffile.TiffFile("testTiff3Images.tiff").ome_metadata
        self.assertTrue(metadata == self.images.getMetadata())

    def testSetMetadataInvalid(self):
        with self.assertRaises(TypeError):
            self.images.setMetadata(np.zeros(12))

    def testSetMetadataValid(self):
        self.images.setMetadata("Hello")
        self.assertTrue(self.images.getMetadata() == "Hello")

    def testSaveMetadataInvalidName(self):
        with self.assertRaises(DCCExcep.InvalidMetadataFileNameException):
            self.images.saveMetadata("meta.testData")

    def testSaveMetadata(self):
        import os
        self.images.saveMetadata("testSaveMetaDCCImagesTest_fromTiff")
        isSaved = True
        try:
            os.remove("testSaveMetaDCCImagesTest_fromTiff.xml")
        except FileNotFoundError:
            isSaved = False
        self.assertTrue(isSaved)

    def testGetPath(self):
        self.assertTrue(self.images.getPath() == "testTiff3Images.tiff")

if __name__ == '__main__':
    unittest.main()

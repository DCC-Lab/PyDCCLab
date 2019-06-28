import env
import unittest
from DCCImagesFromFiles import *
import DCCExceptions as DCCExcep


class TestDCCImagesFromCZIFileConstructor(unittest.TestCase):

    def testInvalidPathConstructor(self):
        with self.assertRaises(FileNotFoundError):
            DCCImagesFromCZIFile("noSuchFile.czi")

    def testNotCziFile(self):
        with self.assertRaises(ValueError):
            DCCImagesFromCZIFile("testNotCziFile.jpg")

    def testCorrectPath(self):
        imagesFromCzi = DCCImagesFromCZIFile("testCziFileTwoChannels.czi")
        self.assertIsInstance(imagesFromCzi, DCCImagesFromCZIFile)


class testDCCImagesFromCZIFileMethods(unittest.TestCase):

    def setUp(self) -> None:
        import cziUtil as cziUtil
        self.imagesFromCzi = DCCImagesFromCZIFile("testCziFileTwoChannels.czi")
        self.metadata = cziUtil.extractMetadataFromCziFileObject(cziUtil.readCziImage("testCziFileTwoChannels.czi"))

    def testGetMetadata(self):
        import cziMetadata as meta
        self.assertTrue(self.imagesFromCzi.getMetadata() == meta.CZIMetadata(self.imagesFromCzi.getPath()))

    def testGetPath(self):
        self.assertTrue("testCziFileTwoChannels.czi" == self.imagesFromCzi.getPath())


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
        file = "testCziFileTwoChannels.czi"
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

    def testGetPath(self):
        self.assertTrue(self.images.getPath() == "testTiff3Images.tiff")


if __name__ == '__main__':
    unittest.main()

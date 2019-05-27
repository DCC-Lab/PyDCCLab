import unittest
import ImageAnalysis.DCCImages as DCCImages
import ImageAnalysis.DCCImagesExceptions as DCCExcep
import numpy as np
from unittest.mock import Mock, patch


class TestDCCImageConstructor(unittest.TestCase):

    def testValidConstructor(self):
        image = DCCImages.DCCImage(np.ones((1250, 1500, 3), dtype=np.float32))
        self.assertIsInstance(image, DCCImages.DCCImage)

    def testInvalidDimensionsConstructor(self):
        with self.assertRaises(DCCExcep.ImageDimensionsException):
            DCCImages.DCCImage(np.zeros(12, dtype=np.float32))

    def testInvalidTypeConstructor(self):
        with self.assertRaises(DCCExcep.PixelTypeException):
            DCCImages.DCCImage(np.ones((1250, 1500, 3), dtype=np.complex))


class TestDCCImageMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.array = np.ones((1250, 1251), dtype=np.float32) * 25.56
        self.array[100][100] = 100.0
        self.array[0][0] = 0.0
        self.image = DCCImages.DCCImage(self.array)

    def testEquals(self):
        testArray = np.copy(self.array)
        testImage = DCCImages.DCCImage(testArray)
        self.assertTrue(testImage == self.image)

    def testNotEquals(self):
        testArray = np.copy(self.array)
        testArray[0][0] = 0.0001
        testImage = DCCImages.DCCImage(testArray)
        self.assertFalse(testImage == self.image)

    def testInvalidEquality(self):
        testArray = np.copy(self.array)
        with self.assertRaises(DCCExcep.InvalidEqualityTest):
            self.image == testArray

    def testGetDCCImageAsNumpyArray(self):
        testArray = np.copy(self.array)
        getArray = self.image.getDCCImageAsArray()
        equality = np.array_equal(testArray, getArray)
        self.assertTrue(equality)

    def testGetDCCImageWidth(self):
        width = 1250
        self.assertEqual(self.image.getDCCImageWidth(), width)

    def testGetDCCImageLength(self):
        length = 1251
        self.assertEqual(self.image.getDCCImageLength(), length)

    def testGetDCCImageChannels(self):
        nbChannel = 1
        self.assertEqual(self.image.getDCCImageNumberOfChannels(), nbChannel)

    def testGetDCCImageChannels3Channels(self):
        nbChannels = 3
        tempArray = np.zeros((1250, 1800, 3), dtype=np.float32)
        tempImage = DCCImages.DCCImage(tempArray)
        self.assertEqual(tempImage.getDCCImageNumberOfChannels(), nbChannels)

    def testGetNumberOFPixels(self):
        nbPixels = 1563750
        self.assertEqual(self.image.getNumberOfPixels(), nbPixels)

    def testToPILImage(self):
        import PIL.Image
        pilImage = PIL.Image.fromarray(np.copy(self.array))
        getPilImage = self.image.toPILImage()
        self.assertTrue(pilImage == getPilImage)

    def testCopyDCCImage(self):
        imageCopy = self.image.copyDCCImage()
        self.assertIsInstance(imageCopy, DCCImages.DCCImage)

    def testCopyDCCImageEquality(self):
        imageCopy = self.image.copyDCCImage()
        self.assertTrue(self.image == imageCopy)

    def testModifiedCopy(self):
        imageCopy = self.image.copyDCCImage()
        arrayCopy = imageCopy.getDCCImageAsArray()
        arrayCopy[100][79] = 1.2
        imageNotCopy = DCCImages.DCCImage(arrayCopy)
        self.assertFalse(self.image == imageNotCopy)

    def testShowImage(self):
        # todo
        pass

    def testSaveToTIFFInvalidEmptyName(self):
        name = ""
        with self.assertRaises(DCCExcep.InvalidImageName):
            self.image.saveToTIFF(name)

    def testSaveToTIFFInvalidCharacterName(self):
        name = "test?"
        with self.assertRaises(DCCExcep.InvalidImageName):
            self.image.saveToTIFF(name)

    def testSaveToTIFF(self):
        name = "testSaveToTiff"
        self.image.saveToTIFF(name)
        isSaved = True
        try:
            file = open("{}.tif".format(name), "r")
            file.close()
        except FileNotFoundError:
            isSaved = False
        self.assertTrue(isSaved)

    def testGetMetadataNone(self):
        self.assertIsNone(self.image.getMetadata())

    def testGetMetadataNotNone(self):
        array = np.ones((1250, 1250), dtype=np.float32)
        metadata = "This is a metadata test"
        image = DCCImages.DCCImage(array, metadata)
        self.assertTrue(image.getMetadata() == metadata)

    def testSetMetadata(self):
        self.image.setMetadata("Hello world")
        self.assertTrue(self.image.getMetadata() == "Hello world")

    def testSetMetadataReturn(self):
        newMeta = self.image.setMetadata("Yo")
        self.assertTrue(newMeta == "Yo")

    def testGrayScaleConversionImageAlreadyGray(self):
        grayScale = self.image.grayscaleConversion()
        self.assertTrue(grayScale == self.image)

    def testGrayScaleConversion(self):
        image = np.ones((10, 10, 3), dtype=np.float32)
        image[..., -1] = 0.
        image[..., -2] = 0.
        dccImage = DCCImages.DCCImage(image)
        grayScale = dccImage.grayscaleConversion()
        self.assertTrue(grayScale.getDCCImageNumberOfChannels() == 1)

    # todo Faire tests unitaires des méthodes d'histogrammes

    def testDCCImageXDerivativeZerosOutput(self):
        array = np.ones((5, 5), dtype=np.float32)
        image = DCCImages.DCCImage(array)
        dxImage = image.DCCImageXAxisDerivative()
        supposedDerivative = DCCImages.DCCImage(np.zeros_like(array))
        self.assertTrue(dxImage == supposedDerivative)

    def testDCCImageXDerivative(self):
        array = np.zeros((3, 3), dtype=np.float32)
        array[1][1] = 2
        image = DCCImages.DCCImage(array)
        dxImage = image.DCCImageXAxisDerivative()
        supposedDerivativeArray = np.array([[0, 0, 0], [-2, 0, 2], [0, 0, 0]], dtype=np.float32)
        supposedDerivativeImage = DCCImages.DCCImage(supposedDerivativeArray)
        self.assertTrue(supposedDerivativeImage == dxImage)

    def testDCCImageYDerivativeZerosOutput(self):
        array = np.zeros((5, 5), dtype=np.float32)
        image = DCCImages.DCCImage(array)
        dyImage = image.DCCImageYAxisDerivative()
        supposedDerivative = DCCImages.DCCImage(np.zeros_like(array))
        self.assertTrue(dyImage == supposedDerivative)

    def testDCCImageYDerivative(self):
        array = np.zeros((3, 3), dtype=np.float32)
        array[1][1] = 2
        image = DCCImages.DCCImage(array)
        dyImage = image.DCCImageYAxisDerivative()
        supposedDerivativeArray = np.array([[0, 0, 0], [-2, 0, 2], [0, 0, 0]], dtype=np.float32).T
        supposedDerivativeImage = DCCImages.DCCImage(supposedDerivativeArray)
        self.assertTrue(supposedDerivativeImage == dyImage)

    def testDCCImageAverage(self):
        sumPixelValues = np.sum(self.image.getDCCImageAsArray())
        average = sumPixelValues / self.image.getNumberOfPixels()
        self.assertEqual(average, self.image.DCCImageAverage())

    def testDCCImageAverageColors(self):
        array = np.ones((10, 10, 3), dtype=np.float32)
        array[0][0][0] = 0
        array[0][0][1] = 0
        array[0][0][2] = 0
        image = DCCImages.DCCImage(array)
        supposedAverage = [np.sum(array[..., 0]) / image.getNumberOfPixels(),
                           np.sum(array[..., 1]) / image.getNumberOfPixels(),
                           np.sum(array[..., 2]) / image.getNumberOfPixels()]
        self.assertTrue(image.DCCImageAverage() == supposedAverage)

    def testDCCImageStandardDev(self):
        average = self.image.DCCImageAverage()[0]
        stanDevP1 = np.float_power(np.add(self.image.getDCCImageAsArray(), -average), 2)
        stanDev = np.sqrt(np.sum(stanDevP1) / self.image.getNumberOfPixels())
        self.assertTrue(np.allclose(stanDev, self.image.DCCImageStandardDeviation()))

    def testDCCImageStandardDevColors(self):
        array = np.ones((10, 10, 3), dtype=np.float32)
        image = DCCImages.DCCImage(array)
        averageS = image.DCCImageAverage()
        stanDevS = []
        for i in range(image.getDCCImageNumberOfChannels()):
            average = averageS[i]
            stanDevSP1 = np.float_power(np.add(image.getDCCImageAsArray()[..., i], -average),
                                        2)
            stanDevS.append(np.sqrt(np.sum(stanDevSP1) / image.getNumberOfPixels()))
        self.assertTrue(np.allclose(stanDevS, image.DCCImageStandardDeviation()))

    def testDCCImageShannonEntropy(self):
        base = 2
        uniqueValues, counts = np.unique(self.image.getDCCImageAsArray(), return_counts=True)
        entropy = -np.sum(
            counts / self.image.getNumberOfPixels() * np.log(counts / self.image.getNumberOfPixels()) / np.log(base))
        self.assertAlmostEqual(entropy, self.image.DCCImageShannonEntropy(base))

    def testDCCImageMinimumIntensityPixels(self):
        minimumPosition = (0, 0)
        self.assertTrue(self.image.minimumIntensityPixelsPositionPerChannel() == [minimumPosition])

    def testDCCImageMinimumIntensityPixels2Pixels(self):
        self.array[10][10] = 0
        image = DCCImages.DCCImage(self.array)
        minimumsPosition = [(0, 0), (10, 10)]
        self.assertTrue(image.minimumIntensityPixelsPositionPerChannel() == minimumsPosition)

    def testDCCImageMinimumIntensityPixelsColors(self):
        array = np.ones((10, 10, 3), dtype=np.float32)
        array[0][0][0] = 0
        array[2][2][0] = 0
        array[0][0][1] = -10
        array[0][0][2] = -0.1
        image = DCCImages.DCCImage(array)
        minimumsPosition = [[(0, 0), (2, 2)], [(0, 0)], [(0, 0)]]
        self.assertTrue(image.minimumIntensityPixelsPositionPerChannel() == minimumsPosition)

    def testDCCImageMaximumIntensityPixels(self):
        maximumPosition = [(100, 100)]
        self.assertTrue(self.image.maximumIntensityPixelsPositionPerChannel() == maximumPosition)

    def testDCCImageMaximumIntensityPixels2Pixels(self):
        self.array[50][50] = 100.0
        image = DCCImages.DCCImage(self.array)
        maximumsPosition = [(50, 50), (100, 100)]
        self.assertTrue(image.maximumIntensityPixelsPositionPerChannel() == maximumsPosition)

    def testDCCImageMaximumIntensityPixelsColors(self):
        array = np.ones((10, 10, 3), dtype=np.float32)
        array[0][0][0] = 10
        array[2][2][0] = 10
        array[0][0][1] = 1.01
        array[0][0][2] = 100
        image = DCCImages.DCCImage(array)
        minimumsPosition = [[(0, 0), (2, 2)], [(0, 0)], [(0, 0)]]
        self.assertTrue(image.maximumIntensityPixelsPositionPerChannel() == minimumsPosition)

    def testEntropyFilter(self):
        filterSize = 3
        array = np.zeros((5, 5), dtype=np.float32)
        array[2][2] = 1
        resultEntropyArray = np.zeros_like(array)
        for i in range(1, 4):
            for j in range(1, 4):
                resultEntropyArray[i][j] = 503.2583348E-3
        resultEntropyImage = DCCImages.DCCImage(resultEntropyArray)
        self.assertTrue(resultEntropyImage == DCCImages.DCCImage(array).DCCImageWithEntropyFilter(filterSize))

    def testGaussianFilter(self):
        sigma = 0.4
        array = np.zeros((5, 5), dtype=np.float32)
        array[2][2] = 1
        image = DCCImages.DCCImage(array)
        gaussianBlurredArray = np.zeros_like(array)
        for i in range(5):
            for j in range(5):
                gaussianBlurredArray[i][j] = np.exp(-((i - 2) ** 2 + (j - 2) ** 2) / (2 * sigma ** 2)) / (
                        2 * np.pi * sigma ** 2)
        normalizedGaussianBlurredArray = gaussianBlurredArray / np.sum(gaussianBlurredArray)
        dccImageGaussianArray = image.DCCImageWithGaussianFilterGray(sigma).getDCCImageAsArray()
        self.assertTrue(np.allclose(dccImageGaussianArray, normalizedGaussianBlurredArray))

    def testGaussianFilterColors(self):
        sigma = 0.4
        array = np.zeros((5, 5, 3), dtype=np.float32)
        array[2][2][0] = 1
        array[2][2][1] = 1.2
        array[2][2][2] = 2
        image = DCCImages.DCCImage(array)
        gaussianBlurredArray = np.zeros_like(array)
        # Because of the nature of the discrete convolution used in the gaussian filter
        # and because of the nature of the input array (which contains only 0s except for the middle pixel):
        # We must multiply the resulting array by that non zero digit. In cases where there are more non zero values:
        # It would be more complicated. (In the case of filters, convolution of two matrix (a and b) is represented
        # by a (or b) "moving over" b (or a) and the elements of the resulting matrix would be the sum of the 1-1
        # product of each element of a and b (a11*b11+a12*b12+...). Since we only have one non zero element
        # and since size of gaussian filter = size of input, the output is the normalized gaussian filter multiplied
        # by the only non zero input element. Hope it helps!
        multiplicationFactors = [1, 1.2, 2]
        for channel in range(3):
            for i in range(5):
                for j in range(5):
                    gaussianBlurredArray[i][j][channel] = np.exp(-((i - 2) ** 2 + (j - 2) ** 2) / (2 * sigma ** 2)) / (
                            2 * np.pi * sigma ** 2)
            gaussianBlurredArray[..., channel] = gaussianBlurredArray[..., channel] / np.sum(
                gaussianBlurredArray[..., channel]) * multiplicationFactors[channel]
        dccImageGaussianArray = image.DCCImageWithGaussianFilterColors(sigma).getDCCImageAsArray()
        self.assertTrue(np.allclose(dccImageGaussianArray, gaussianBlurredArray))




class TestDCCImageStackConstructor(unittest.TestCase):

    def testValidConstructorEmpty(self):

        valid = True
        try:
            DCCImages.DCCImageStack([])
        except AttributeError:
            valid = False

        self.assertTrue(valid)

    def testValidConstructorOneElement(self):
        array = np.ones((130, 145), dtype=np.float32)
        image = DCCImages.DCCImage(array)
        stack = DCCImages.DCCImageStack([image])
        self.assertIsInstance(stack, DCCImages.DCCImageStack)

    def testValidConstructor100Elements(self):
        imageList = []
        for i in range(100):
            array = np.ones((1250, 1251), dtype=np.float32)
            array[i][i] = i
            image = DCCImages.DCCImage(array)
            imageList.append(image)
        stack = DCCImages.DCCImageStack(imageList)
        self.assertIsInstance(stack, DCCImages.DCCImageStack)

    def testInvalidConstructor1Element(self):
        image = np.ones((10, 10))
        with self.assertRaises(DCCExcep.NotDCCImageException):
            DCCImages.DCCImageStack([image])

    def testInvalidConstructor11Elements(self):
        imageList = []
        for i in range(10):
            array = np.ones((1250, 1251), dtype=np.float32)
            array[i][i] = i
            image = DCCImages.DCCImage(array)
            imageList.append(image)
        imageList.append(np.ones((10, 10)))
        with self.assertRaises(DCCExcep.NotDCCImageException):
            DCCImages.DCCImageStack(imageList)


class TesDCCImageStackMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.imageList = []
        for i in range(5):
            array = np.ones((1250, 1251), dtype=np.float32)
            array[i][i] = i
            image = DCCImages.DCCImage(array)
            self.imageList.append(image)
        self.stack = DCCImages.DCCImageStack(self.imageList)

    def testImageInStackInvalidImage(self):
        invalidImage = np.ones((1250, 1251), dtype=np.float32)
        with self.assertRaises(DCCExcep.NotDCCImageException):
            self.stack.isImageInStack(invalidImage)

    def testImageNotInStack(self):
        arrayNotInStack = np.ones((1250, 1251), dtype=np.float32)
        arrayNotInStack[0][0] = 0.00001
        imageNotInStack = DCCImages.DCCImage(arrayNotInStack)
        self.assertFalse(self.stack.isImageInStack(imageNotInStack))

    def testImageInStack(self):
        imageInStack = self.imageList[-1].copyDCCImage()
        self.assertTrue(self.stack.isImageInStack(imageInStack))

    def testGetIndexOfInvalidImage(self):
        invalidImage = np.ones((1250, 1251), dtype=np.float32)
        with self.assertRaises(DCCExcep.NotDCCImageException):
            self.stack.getIndexOfImage(invalidImage)

    def testGetIndexOfImageNotInStack(self):
        arrayNotInStack = np.ones((1250, 1251), dtype=np.float32)
        arrayNotInStack[0][0] = 0.00001
        imageNotInStack = DCCImages.DCCImage(arrayNotInStack)
        with self.assertRaises(DCCExcep.ImageNotInStackException):
            self.stack.getIndexOfImage(imageNotInStack)

    def testGetIndexImageInStack(self):
        imageInStack = self.imageList[2].copyDCCImage()
        self.assertEqual(self.stack.getIndexOfImage(imageInStack), 2)

    def testAddInvalidImage(self):
        invalidImage = np.ones((1250, 1251), dtype=np.float32)
        with self.assertRaises(DCCExcep.NotDCCImageException):
            self.stack.addDCCImage(invalidImage)

    def testAddImageAlreadyIn(self):
        imageAlreadyIn = self.imageList[-1]
        with self.assertRaises(DCCExcep.ImageAlreadyInStackException):
            self.stack.addDCCImage(imageAlreadyIn)

    def testAddImageNotAlreadyIn(self):
        imageNotAlreadyIn = DCCImages.DCCImage(np.zeros((1250, 1251), dtype=np.float32))
        indexOfAddedImage = self.stack.addDCCImage(imageNotAlreadyIn)
        self.assertEqual(indexOfAddedImage, 5)

    def testRemoveAtIndexOutOfBound(self):
        with self.assertRaises(IndexError):
            self.stack.removeAtIndex(5)

    def testRemoveImageAtIndex(self):
        imageToRemove = self.imageList[-1]
        removedImage = self.stack.removeAtIndex(-1)
        self.assertTrue(imageToRemove == removedImage)

    def testRemoveImageWithInvalidImage(self):
        invalidImage = np.ones((125, 12547), dtype=np.float32)
        with self.assertRaises(DCCExcep.NotDCCImageException):
            self.stack.removeDCCImage(invalidImage)

    def testRemoveImageWithImageNotInStack(self):
        arrayNotInStack = np.ones((1250, 1251), dtype=np.float32)
        arrayNotInStack[0][0] = 0.00001
        imageNotInStack = DCCImages.DCCImage(arrayNotInStack)
        with self.assertRaises(DCCExcep.ImageNotInStackException):
            self.stack.removeDCCImage(imageNotInStack)

    def testRemoveImageWithImage(self):
        imageInStack = self.imageList[0].copyDCCImage()
        indexOfRemovedImage = self.stack.removeDCCImage(imageInStack)
        self.assertEqual(indexOfRemovedImage, 0)

    def testDetNumberOfImages(self):
        numberOfImages = len(self.imageList)
        self.assertEqual(self.stack.getNumberOfImages(), numberOfImages)

    def testGetNumberOfImagesAddedImage(self):
        numberOfImages = len(self.imageList)
        imageNotAlreadyIn = DCCImages.DCCImage(np.zeros((1250, 1251), dtype=np.float32))
        self.stack.addDCCImage(imageNotAlreadyIn)
        self.assertEqual(self.stack.getNumberOfImages(), numberOfImages + 1)

    def testGetNumberOfImagesRemovedImage(self):
        numberOfImages = len(self.imageList)
        self.stack.removeAtIndex(0)
        self.assertEqual(self.stack.getNumberOfImages(), numberOfImages - 1)

    def testImageStackAsNumpyArray(self):
        imageArray = np.array(self.imageList)
        arrayFromStack = self.stack.asNumpyArray()
        self.assertTrue(np.array_equal(imageArray, arrayFromStack))

    def testImageStackAsList(self):
        listFromStack = self.stack.asList()
        self.assertTrue(listFromStack == self.imageList)

    def testClearStack(self):
        self.stack.clearAll()
        self.assertTrue(len(self.stack) == 0)

    @patch("matplotlib.pyplot.show", new=Mock)
    def testShowImages(self):
        nbOfImagesShown = self.stack.showImages()
        self.assertEqual(nbOfImagesShown, 5)


class TestDCCImagesFromCZIFileConstructor(unittest.TestCase):

    def testInvalidPathConstructor(self):
        with self.assertRaises(FileNotFoundError):
            DCCImages.DCCImagesFromCZIFile("noSuchFile.czi")

    def testNotCziFile(self):
        with self.assertRaises(ValueError):
            DCCImages.DCCImagesFromCZIFile("testNotCziFile.jpg")

    def testCorrectPath(self):
        imagesFromCzi = DCCImages.DCCImagesFromCZIFile("testCziFile2Images.czi")
        self.assertIsInstance(imagesFromCzi, DCCImages.DCCImagesFromCZIFile)


class testDCCImagesFromCZIFileMethods(unittest.TestCase):

    def setUp(self) -> None:
        import ImageAnalysis.cziUtil as cziUtil
        self.imagesFromCzi = DCCImages.DCCImagesFromCZIFile("testCziFile2Images.czi")
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
        with self.assertRaises(DCCExcep.InvalidMetadataFileName):
            self.imagesFromCzi.saveMetadata("/*")

    def testSaveMetadataValidName(self):
        self.imagesFromCzi.saveMetadata("testSaveMetaDCCImagesTest")
        isSaved = True
        try:
            fileTest = open("testSaveMetaDCCImagesTest.xml", "r", encoding="utf-8")
            fileTest.close()
        except FileNotFoundError:
            isSaved = False
        self.assertTrue(isSaved)

    def testGetPath(self):
        self.assertTrue("testCziFile2Images.czi" == self.imagesFromCzi.getPath())


class TestDCCImageFromNormalFileConstructor(unittest.TestCase):

    def testInvalidConstructorNotASupportedImageFormat(self):
        file = "testSaveMetaDCCImagesTest.xml"
        with self.assertRaises(OSError):
            DCCImages.DCCImageFromNormalFile(file)

    def testInvalidConstructorTIFFFile(self):
        file = "testTiff3Images.tiff"
        with self.assertRaises(DCCExcep.InvalidFileFormat):
            DCCImages.DCCImageFromNormalFile(file)

    def testInvalidConstructorCZIFile(self):
        file = "testCziFile2Images.czi"
        with self.assertRaises(DCCExcep.InvalidFileFormat):
            DCCImages.DCCImageFromNormalFile(file)

    def testValidConstructor(self):
        file = "testNotCziFile.jpg"
        imageFromJPG = DCCImages.DCCImageFromNormalFile(file)
        self.assertIsInstance(imageFromJPG, DCCImages.DCCImageFromNormalFile)


class TestDCCImageFromNormalFileMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.imageFromJPG = DCCImages.DCCImageFromNormalFile("testNotCziFile.jpg")

    def testGetPath(self):
        self.assertTrue(self.imageFromJPG.getPath() == "testNotCziFile.jpg")


class TestDCCImagesFromTiffFileConstructor(unittest.TestCase):

    def testInvalidConstructorNotSupportedFile(self):
        with self.assertRaises(DCCExcep.InvalidFileFormat):
            DCCImages.DCCImagesFromTiffFile("testNotCziFile.jpg")

    def testValidConstructor(self):
        imageFromTiff = DCCImages.DCCImagesFromTiffFile("testTiff3Images.tiff")
        self.assertIsInstance(imageFromTiff, DCCImages.DCCImagesFromTiffFile)


class TestDCCImagesFromTiffFileMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.images = DCCImages.DCCImagesFromTiffFile("testTiff3Images.tiff")

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
        with self.assertRaises(DCCExcep.InvalidMetadataFileName):
            self.images.saveMetadata("meta.data")

    def testSaveMetadata(self):
        self.images.saveMetadata("testSaveMetaDCCImagesTest_fromTiff")
        isSaved = True
        try:
            fileTest = open("testSaveMetaDCCImagesTest_fromTiff.xml", "r", encoding="utf-8")
            fileTest.close()
        except FileNotFoundError:
            isSaved = False
        self.assertTrue(isSaved)

    def testGetPath(self):
        self.assertTrue(self.images.getPath() == "testTiff3Images.tiff")


if __name__ == '__main__':
    unittest.main()

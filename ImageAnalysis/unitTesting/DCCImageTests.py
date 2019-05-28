import unittest
import numpy as np
from unittest.mock import Mock, patch
import DCCImage
import DCCImagesExceptions as DCCExcep


class TestDCCImageConstructor(unittest.TestCase):

    def testValidConstructor(self):
        image = DCCImage.DCCImage(np.ones((1250, 1500, 3), dtype=np.float32))
        self.assertIsInstance(image, DCCImage.DCCImage)

    def testInvalidDimensionsConstructor(self):
        with self.assertRaises(DCCExcep.ImageDimensionsException):
            DCCImage.DCCImage(np.zeros(12, dtype=np.float32))

    def testInvalidTypeConstructor(self):
        with self.assertRaises(DCCExcep.PixelTypeException):
            DCCImage.DCCImage(np.ones((1250, 1500, 3), dtype=np.complex))


class TestDCCImageMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.array = np.ones((1250, 1251), dtype=np.float32) * 25.56
        self.array[100][100] = 100.0
        self.array[0][0] = 0.0
        self.image = DCCImage.DCCImage(self.array)

    def testEquals(self):
        testArray = np.copy(self.array)
        testImage = DCCImage.DCCImage(testArray)
        self.assertTrue(testImage == self.image)

    def testNotEquals(self):
        testArray = np.copy(self.array)
        testArray[0][0] = 0.0001
        testImage = DCCImage.DCCImage(testArray)
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
        tempImage = DCCImage.DCCImage(tempArray)
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
        self.assertIsInstance(imageCopy, DCCImage.DCCImage)

    def testCopyDCCImageEquality(self):
        imageCopy = self.image.copyDCCImage()
        self.assertTrue(self.image == imageCopy)

    def testModifiedCopy(self):
        imageCopy = self.image.copyDCCImage()
        arrayCopy = imageCopy.getDCCImageAsArray()
        arrayCopy[100][79] = 1.2
        imageNotCopy = DCCImage.DCCImage(arrayCopy)
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
        image = DCCImage.DCCImage(array, metadata)
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
        dccImage = DCCImage.DCCImage(image)
        grayScale = dccImage.grayscaleConversion()
        self.assertTrue(grayScale.getDCCImageNumberOfChannels() == 1)

    # todo Faire tests unitaires des méthodes d'histogrammes

    def testDCCImageXDerivativeZerosOutput(self):
        array = np.ones((5, 5), dtype=np.float32)
        image = DCCImage.DCCImage(array)
        dxImage = image.DCCImageXAxisDerivative()
        supposedDerivative = DCCImage.DCCImage(np.zeros_like(array))
        self.assertTrue(dxImage == supposedDerivative)

    def testDCCImageXDerivative(self):
        array = np.zeros((3, 3), dtype=np.float32)
        array[1][1] = 2
        image = DCCImage.DCCImage(array)
        dxImage = image.DCCImageXAxisDerivative()
        supposedDerivativeArray = np.array([[0, 0, 0], [-2, 0, 2], [0, 0, 0]], dtype=np.float32)
        supposedDerivativeImage = DCCImage.DCCImage(supposedDerivativeArray)
        self.assertTrue(supposedDerivativeImage == dxImage)

    def testDCCImageYDerivativeZerosOutput(self):
        array = np.zeros((5, 5), dtype=np.float32)
        image = DCCImage.DCCImage(array)
        dyImage = image.DCCImageYAxisDerivative()
        supposedDerivative = DCCImage.DCCImage(np.zeros_like(array))
        self.assertTrue(dyImage == supposedDerivative)

    def testDCCImageYDerivative(self):
        array = np.zeros((3, 3), dtype=np.float32)
        array[1][1] = 2
        image = DCCImage.DCCImage(array)
        dyImage = image.DCCImageYAxisDerivative()
        supposedDerivativeArray = np.array([[0, 0, 0], [-2, 0, 2], [0, 0, 0]], dtype=np.float32).T
        supposedDerivativeImage = DCCImage.DCCImage(supposedDerivativeArray)
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
        image = DCCImage.DCCImage(array)
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
        image = DCCImage.DCCImage(array)
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
        image = DCCImage.DCCImage(self.array)
        minimumsPosition = [(0, 0), (10, 10)]
        self.assertTrue(image.minimumIntensityPixelsPositionPerChannel() == minimumsPosition)

    def testDCCImageMinimumIntensityPixelsColors(self):
        array = np.ones((10, 10, 3), dtype=np.float32)
        array[0][0][0] = 0
        array[2][2][0] = 0
        array[0][0][1] = -10
        array[0][0][2] = -0.1
        image = DCCImage.DCCImage(array)
        minimumsPosition = [[(0, 0), (2, 2)], [(0, 0)], [(0, 0)]]
        self.assertTrue(image.minimumIntensityPixelsPositionPerChannel() == minimumsPosition)

    def testDCCImageMaximumIntensityPixels(self):
        maximumPosition = [(100, 100)]
        self.assertTrue(self.image.maximumIntensityPixelsPositionPerChannel() == maximumPosition)

    def testDCCImageMaximumIntensityPixels2Pixels(self):
        self.array[50][50] = 100.0
        image = DCCImage.DCCImage(self.array)
        maximumsPosition = [(50, 50), (100, 100)]
        self.assertTrue(image.maximumIntensityPixelsPositionPerChannel() == maximumsPosition)

    def testDCCImageMaximumIntensityPixelsColors(self):
        array = np.ones((10, 10, 3), dtype=np.float32)
        array[0][0][0] = 10
        array[2][2][0] = 10
        array[0][0][1] = 1.01
        array[0][0][2] = 100
        image = DCCImage.DCCImage(array)
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
        resultEntropyImage = DCCImage.DCCImage(resultEntropyArray)
        self.assertTrue(resultEntropyImage == DCCImage.DCCImage(array).DCCImageWithEntropyFilter(filterSize))

    def testGaussianFilter(self):
        sigma = 0.4
        array = np.zeros((5, 5), dtype=np.float32)
        array[2][2] = 1
        image = DCCImage.DCCImage(array)
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
        image = DCCImage.DCCImage(array)
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

    def testDCCImageWithStandardDeviationFilter_MK1(self):
        array = np.zeros((5, 5), dtype=np.float32)
        # Padded array (internally happens when computing convolution with another matrix)
        paddedArray = np.zeros((7, 7), dtype=np.float32)
        for i in range(1, 4):
            for j in range(1, 4):
                array[i][j] = 3
                paddedArray[i + 1][j + 1] = 3
        listOfImages = []
        # Smaller array of size 3x3 resulting of the convolution
        for i in range(5):
            for j in range(5):
                listOfImages.append(DCCImage.DCCImage(
                    np.array([paddedArray[i][j:j + 3], paddedArray[i + 1][j:j + 3], paddedArray[i + 2][j:j + 3]],
                             dtype=np.float32)))
        # Compute the standard deviation of the smaller arrays
        resultArray = np.array([image.DCCImageStandardDeviation() for image in listOfImages], dtype=np.float32).reshape(
            (5, 5))

        stdDevImageAsArray = DCCImage.DCCImage(array).DCCImageWithStandardDeviationFilter_MK1(
            filterSize=3).getDCCImageAsArray()
        self.assertTrue(np.allclose(resultArray, stdDevImageAsArray))

    def testDCCImageWithStandardDeviationFilter_MK2(self):
        array = np.zeros((5, 5), dtype=np.float32)
        # Padded array (internally happens when computing convolution with another matrix)
        paddedArray = np.zeros((7, 7), dtype=np.float32)
        for i in range(1, 4):
            for j in range(1, 4):
                array[i][j] = 2.36
                paddedArray[i + 1][j + 1] = 2.36
        listOfImages = []
        # Smaller array of size 3x3 resulting of the convolution
        for i in range(5):
            for j in range(5):
                listOfImages.append(DCCImage.DCCImage(
                    np.array([paddedArray[i][j:j + 3], paddedArray[i + 1][j:j + 3], paddedArray[i + 2][j:j + 3]],
                             dtype=np.float32)))
        # Compute the standard deviation of the smaller arrays
        resultArray = np.array([image.DCCImageStandardDeviation() for image in listOfImages], dtype=np.float32).reshape(
            (5, 5))

        stdDevImageAsArray = DCCImage.DCCImage(array).DCCImageWithStandardDeviationFilter_MK2(
            filterSize=3).getDCCImageAsArray()
        self.assertTrue(np.allclose(resultArray, stdDevImageAsArray))

    def testDCCImageSTDDevFilterMK1AndMK2Equality(self):
        array = np.arange(16).reshape((4, 4)).astype(np.float32)
        image = DCCImage.DCCImage(array)
        mk1 = image.DCCImageWithStandardDeviationFilter_MK1(3).getDCCImageAsArray()
        mk2 = image.DCCImageWithStandardDeviationFilter_MK2(3).getDCCImageAsArray()
        self.assertTrue(np.allclose(mk1, mk2))

    def testDCCImageSTDDevMk1SlowerThanMK2(self):
        import time
        array = np.arange(50000).reshape((500, 100)).astype(np.float32)
        image = DCCImage.DCCImage(array)
        beforeMK1 = time.clock()
        image.DCCImageWithStandardDeviationFilter_MK1(3).getDCCImageAsArray()
        afterMK1 = time.clock()
        beforeMK2 = time.clock()
        image.DCCImageWithStandardDeviationFilter_MK2(3).getDCCImageAsArray()
        afterMK2 = time.clock()
        self.assertTrue((afterMK1 - beforeMK1) >= (afterMK2 - beforeMK2))

if __name__ == '__main__':
    unittest.main()

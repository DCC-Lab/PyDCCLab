import env
from dcclab import *
import unittest
from unittest.mock import Mock, patch
import numpy as np


class TestChannels(env.DCCLabTestCase):

    def testInitWithComplexValues(self):
        array = np.ones((100, 100), dtype=complex) * (1 + 23.45j)
        with self.assertRaises(PixelTypeException):
            Channel(array)

    def testInitWith2DIntArray(self):
        array = np.ones((100, 100), dtype=np.int)
        channel = Channel(pixels=array)
        self.assertIsNotNone(channel)
        self.assertIsInstance(channel, Channel)

    def testInitWith2DFloatArray(self):
        array = np.ones((100, 100), dtype=np.float32)
        channel = Channel(pixels=array)
        self.assertIsNotNone(channel)
        self.assertIsInstance(channel, Channel)

    def testInitWith1DOR3DArrayFails(self):
        array = np.ones((100, 100, 3), dtype=np.float32)
        with self.assertRaises(DimensionException):
            channel = Channel(pixels=array)
        array = np.ones((100), dtype=np.float32)
        with self.assertRaises(DimensionException):
            channel = Channel(pixels=array)

    def testInitWith2DIntegerArray(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)
        self.assertEqual(array.all(), channel.pixels.all())

    def testStringRepresentation(self):
        array = np.random.randint(low=0, high=255, size=(100, 200), dtype=np.uint8)
        channel = Channel(pixels=array)
        self.assertEqual(str(array), str(channel))

    def testInitCopiesPixels(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)
        self.assertFalse(array is channel.pixels)

    def testDimension(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)
        self.assertTrue(channel.dimension == 2)

    def testShape(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)
        self.assertTrue(channel.shape == array.shape)

    def testWidth(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)
        self.assertEqual(channel.width, 100)

    def testHeight(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)
        self.assertEqual(channel.height, 200)

    def testNumberOfPixels(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)
        self.assertTrue(channel.numberOfPixels == 100 * 200)

    def testSizeInBytes(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)
        self.assertTrue(channel.sizeInBytes == array.nbytes)

    def testEqualChannels(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel1 = Channel(pixels=array)
        channel2 = Channel(pixels=array)
        self.assertEqual(channel1, channel2)

    def testEqualDifferentTypes(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)

        self.assertNotEqual(1, 'abc')  # not an error, simply false
        self.assertNotEqual(1, np)  # not an error, simply false
        self.assertNotEqual(1, channel)  # not an error, simply false

    def testPixelsCopy(self):
        array = np.random.randint(low=0, high=255, size=(100, 200))
        channel = Channel(pixels=array)
        pixels = channel.copy()
        self.assertFalse(pixels is array)

    def testIsBinary(self):
        array = np.random.randint(low=0, high=2, size=(100, 200))
        self.assertTrue(Channel(pixels=array).isBinary)
        self.assertFalse(Channel(pixels=array * 255).isBinary)
        self.assertFalse(Channel(pixels=array * 200).isBinary)

        array = np.random.randint(low=0, high=255, size=(100, 200))
        self.assertFalse(Channel(pixels=array).isBinary)

    @patch("matplotlib.pyplot.show", new=Mock())
    def testDisplayHistogramNormalized(self):
        channel = Channel(np.random.randint(0, 255, (10, 10), dtype=np.uint8))
        histValues, histBins = channel.getHistogramValues(True)
        displayValues, displayBins = channel.displayHistogram(True)
        self.assertTrue(np.array_equal(histValues, displayValues))
        self.assertTrue(np.array_equal(histBins, displayBins))

    @patch("matplotlib.pyplot.show", new=Mock())
    def testDisplayChannel(self):
        channel = Channel(np.random.randint(0, 255, (10, 10), dtype=np.uint8))
        obj = channel.display()
        self.assertEqual(obj, channel)

    def testApplySomethingChangesPixels(self):
        channel = Channel(np.random.randint(0, 255, (10, 10), dtype=np.uint8))
        originalPixels = channel.pixels
        channel.applyXDerivative()
        self.assertFalse(np.array_equal(originalPixels, channel.pixels))

    def testRestoreOriginal(self):
        channel = Channel(np.random.randint(0, 255, (10, 10), dtype=np.uint8))
        originalPixels = channel.pixels
        channel.applyXDerivative()
        channel.restoreOriginal()
        self.assertTrue(np.array_equal(originalPixels, channel.pixels))

    def testRestoreOriginalNotSavedBefore(self):
        channel = Channel(np.random.randint(0, 255, (10, 10), dtype=np.uint8))
        self.assertIsNone(channel.restoreOriginal())

    def testOriginalPixelsNone(self):
        channel = Channel(np.random.randint(0, 255, (10, 10), dtype=np.uint8))
        self.assertIsNone(channel.originalPixels)

    def testOriginalPixels(self):
        channel = Channel(np.random.randint(0, 255, (10, 10), dtype=np.uint8))
        originalPixels = channel.pixels
        channel.applyClosing(4)
        self.assertTrue(np.array_equal(originalPixels, channel.originalPixels))

    def testHasNoOriginalPixels(self):
        channel = Channel(np.random.randint(0, 255, (10, 10), dtype=np.uint8))
        self.assertFalse(channel.hasOriginal)

    def testHasOriginalPixels(self):
        channel = Channel(np.random.randint(0, 255, (10, 10), dtype=np.uint8))
        channel.applyConvolution([[1, 2, 3], [-3, -2, -1]])
        self.assertTrue(channel.hasOriginal)

    def testReplaceFromArrayOriginalSaved(self):
        channel = Channel(np.random.randint(0, 255, (10, 10), dtype=np.uint8))
        channel.replaceFromArray(np.random.randint(0, 255, (11, 11), dtype=np.uint8))
        self.assertTrue(channel.hasOriginal)

    def testReplaceFromArrayException(self):
        channel = Channel(np.random.randint(0, 255, (10, 10), dtype=np.uint8))
        with self.assertRaises(AssertionError):
            channel.replaceFromArray(np.array([1, 2, 3]))

    def testReplaceFromArrayNewValues(self):
        array = np.random.randint(0, 255, (10, 10), dtype=np.uint8)
        channel = Channel(np.random.randint(0, 255, (100, 100), dtype=np.uint8))
        channel.replaceFromArray(array)
        self.assertTrue(np.array_equal(channel.pixels, array))

    def testGetShannonEntropyArbitraryBase(self):
        def entropy(array, base):
            numberPixels = array.shape[0] * array.shape[1]
            _, counts = np.unique(array, return_counts=True)
            probArray = counts / np.sum(counts)
            logArray = np.log(probArray) / np.log(base)
            entropy = -np.sum(probArray * logArray)
            return entropy

        base = 0
        while base <= 0:
            baseCoeff = np.random.randint(1, 10, size=(1,))
            base = np.random.rand() * baseCoeff
        channel = Channel(np.random.randint(1, 255, (100, 100), dtype=np.uint8))
        skimageEntropy = channel.getShannonEntropy(base)
        testEntropy = entropy(channel.pixels, base)
        self.assertAlmostEqual(testEntropy, skimageEntropy)

    def testGetExtrema(self):
        array = np.arange(0, 25, dtype=np.uint8).reshape((5, 5))
        channel = Channel(array)
        self.assertTupleEqual(channel.getExtrema(), (0, 24))

    def testGetMedian(self):
        array = np.arange(0, 100, dtype=np.uint8)
        np.random.shuffle(array)
        channel = Channel(array.reshape((10, 10)))
        self.assertEqual(channel.getMedian(), 49.5)

    def testPixelsOfIntensityOnTuple(self):
        array = np.ones((100, 100)) * 0.236
        i, j = np.random.randint(0, 100, (2,))
        array[i, j] = 0.56
        channel = Channel(array)
        self.assertListEqual([(i, j)], channel.getPixelsOfIntensity(0.56))

    def testPixlesOfIntensityRandomNumberOfTuple(self):
        import operator
        nbOfTuples = np.random.randint(1, 100)
        listOfTuples = []
        array = np.ones((132, 200)) * 0.14
        for _ in range(nbOfTuples):
            i, j = np.random.randint(0, 132), np.random.randint(0, 200)
            array[i, j] = 0.001
            listOfTuples.append((i, j))
        channel = Channel(array)
        listOfTuples = list(set(listOfTuples))
        listOfTuples.sort(key=operator.itemgetter(0, 1))
        self.assertListEqual(listOfTuples, channel.getPixelsOfIntensity(0.001))

    def testGetMinimumIndicesOneValue(self):
        array = np.ones((100, 100))
        i, j = np.random.randint(0, 100, (2,))
        array[i, j] = 0
        channel = Channel(array)
        self.assertListEqual([(i, j)], channel.getMinimum())

    def testGetMinimumIndicesRandomNumberOfValues(self):
        import operator
        nbOfTuples = np.random.randint(1, 100)
        listOfTuples = []
        array = np.ones((132, 200))
        for _ in range(nbOfTuples):
            i, j = np.random.randint(0, 132), np.random.randint(0, 200)
            array[i, j] = 0.99999
            listOfTuples.append((i, j))
        channel = Channel(array)
        listOfTuples = list(set(listOfTuples))
        listOfTuples.sort(key=operator.itemgetter(0, 1))
        self.assertListEqual(listOfTuples, channel.getMinimum())

    def testGetMaximumIndicesOneValue(self):
        array = np.zeros((100, 100))
        i, j = np.random.randint(0, 100, (2,))
        array[i, j] = 1
        channel = Channel(array)
        self.assertListEqual([(i, j)], channel.getMaximum())

    def testGetMaximumIndicesRandomNumberOfValues(self):
        import operator
        nbOfTuples = np.random.randint(1, 100)
        listOfTuples = []
        array = np.ones((132, 200))
        for _ in range(nbOfTuples):
            i, j = np.random.randint(0, 132), np.random.randint(0, 200)
            array[i, j] = 1.0001
            listOfTuples.append((i, j))
        channel = Channel(array)
        listOfTuples = list(set(listOfTuples))
        listOfTuples.sort(key=operator.itemgetter(0, 1))
        self.assertListEqual(listOfTuples, channel.getMaximum())

    def testConvolution(self):
        # FIXME: test result
        array = np.random.randint(low=0, high=255, size=(100, 200))
        kernel = [[-1, 0, 1], [1, 0, 1], [0, 1, 1]]
        channel = Channel(pixels=array).convolveWith(kernel)
        self.assertIsNotNone(channel)
        self.assertTrue(channel.pixels.shape == array.shape)

    def testXDerivative(self):
        array = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
        expected = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        channel = Channel(pixels=array).getXAxisDerivative()
        self.assertIsNotNone(channel)
        self.assertTrue(channel.pixels.shape == array.shape)
        self.assertTrue(channel.pixels.all() == expected.all())

    def testYDerivative(self):
        array = np.array([[0, 1, 2], [0, 1, 2], [0, 1, 2]])
        expected = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        channel = Channel(pixels=array).getYAxisDerivative()
        self.assertIsNotNone(channel)
        self.assertTrue(channel.pixels.shape == array.shape)
        self.assertTrue(channel.pixels.all() == expected.all())

    def testAverage(self):
        array = np.array([[0, 1, 2], [0, 1, 2], [0, 1, 2]])
        expected = 1.0
        result = Channel(pixels=array).getAverageValueOfPixels()
        self.assertIsNotNone(channel)
        self.assertTrue(result == expected)

    def testStddev(self):
        array = np.array([[0, 1, 2], [0, 1, 2], [0, 1, 2]])
        channel = Channel(pixels=array).getStandardDeviation()
        self.assertIsNotNone(channel)

    @patch("matplotlib.pyplot.show", new=Mock())
    def testMultichannelDisplay(self):
        listOfChannel = []
        nbChannel = np.random.randint(1, 10)
        for i in range(nbChannel):
            listOfChannel.append(Channel(np.random.randint(0, 255, (1000, 10000), np.uint8)))
        returnList = Channel.multiChannelDisplay(listOfChannel)
        self.assertListEqual(returnList, listOfChannel)


class TestChannelsSegmentation(env.DCCLabTestCase):
    def testNoMaskOnInit(self):
        array = np.array([[0, 1, 2], [0, 1, 2], [0, 1, 2]])
        channel = Channel(array)
        self.assertFalse(channel.hasMask)

    def testMaskFromThreshold(self):
        array = np.array([[0, 1, 2], [0, 1, 2], [0, 1, 2]])
        channel = Channel(array)
        channel.setMaskFromThreshold(1)
        self.assertTrue(channel.hasMask)
        self.assertTrue(channel.mask.pixels.all() == np.array([[0, 1, 1], [0, 1, 1], [0, 1, 1]]).all())

    def testMaskFromThreshold(self):
        array = np.array([[1, 0, 0, 0], [0, 2, 2, 0], [0, 0, 0, 3]])
        expectedMask = np.array([[1, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 1]])
        channel = Channel(array)
        channel.setMaskFromThreshold(0.5)
        self.assertTrue(channel.hasMask)
        self.assertTrue(channel.mask.pixels.all() == expectedMask.all())

    def testLabelMask(self):
        array = np.array([[1, 0, 0, 0], [0, 2, 2, 0], [0, 0, 0, 3]])
        channel = Channel(array)
        channel.setMaskFromThreshold(1)
        channel.labelMaskComponents()

        expectedMask = np.array([[1, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 1]])
        expectedComponents = np.array([[0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 2]])
        self.assertTrue(channel.labelledComponents.all() == expectedComponents.all())
        self.assertTrue(channel.numberOfComponents == 2)

    def testLabelWithoutMaskFail(self):
        array = np.array([[1, 0, 0, 0], [0, 2, 2, 0], [0, 0, 0, 3]])
        channel = Channel(array)
        with self.assertRaises(Exception):
            channel.labelMaskComponents()

    def testAnalyzeComponents(self):
        array = np.array([[1, 0, 0, 0], [0, 2, 2, 0], [0, 0, 0, 3]])
        channel = Channel(array.T)
        channel.setMaskFromThreshold(1)
        channel.labelMaskComponents()
        properties = channel.analyzeComponents()
        self.assertTrue(channel.numberOfComponents == 2)
        self.assertIsNotNone(properties)

    def testAnalyzeComponentsException(self):
        channel = Channel(np.random.randint(1, 255, (100, 100), dtype=np.uint8))
        with self.assertRaises(ValueError):
            channel.analyzeComponents()

    def testFilterNoise(self):
        array = np.array([[1, 0, 0, 0], [0, 2, 2, 0], [0, 0, 0, 3]])
        channel = Channel(array)
        channel.filterNoise()

    def testThreshold(self):
        array = np.array([[1, 0, 0, 0], [0, 2, 2, 0], [0, 0, 0, 3]])
        channel = Channel(array)
        channel.threshold(value=1.5)

    # def testSaveComponents(self):
    #     array = np.array([[1, 0, 0, 0],[0, 2,2, 0],[0, 0,0, 3]])
    #     channel = Channel(array)
    #     channel.setMaskFromThreshold(1)
    #     channel.labelMaskComponents()
    #     channel.analyzeComponents()
    #     channel.saveComponentsStatistics("/tmp/test.json")


class TestChannelSpectralFiltering(env.DCCLabTestCase):

    def testFourierTransform(self):
        def fourierTransform(array):
            returnArray = np.zeros_like(array, dtype=complex)
            m, n = array.shape
            for k in range(m):
                for l in range(n):
                    sum_ = 0
                    for i in range(m):
                        for j in range(n):
                            sum_ += array[i, j] * np.exp(-1j * 2 * np.pi * ((k * i) / m + (l * j) / n))
                    returnArray[k, l] = sum_
            return returnArray

        array = np.arange(0, 28).reshape((7, 4))
        channel = Channel(array)
        fftChannel = channel.fourierTransform(False)
        fftArray = fourierTransform(array)
        self.assertTrue(np.allclose(fftChannel, fftArray))

    def testFourierTransformShift(self):
        shape = (4, 3)
        array = np.random.randint(0, 1000, shape, dtype=np.uint16)
        channel = Channel(array)
        centerY, centerX = shape[0] // 2, shape[1] // 2
        fftChannelShift = channel.fourierTransform()
        fftChannel = channel.fourierTransform(False)
        self.assertFalse(np.array_equal(fftChannelShift, fftChannel))
        self.assertEqual(fftChannelShift[centerY, centerX], fftChannel[0, 0])

    def testHighPassFilterRectMask(self):
        image = Image(path=Path(self.dataDir / "testCziFileTwoChannels.czi"))
        channel = image.channels[0]
        fftChannel = channel.applyHighPassFilterFromRetcangularMask(30)
        self.assertFalse(np.allclose(channel.pixels, fftChannel.pixels))

    def testLowPassFilterRectMask(self):
        image = Image(path=Path(self.dataDir / "testCziFileTwoChannels.czi"))
        channel = image.channels[0]
        fftChannel = channel.applyLowPassFilterFromRectangularMask(40)
        self.assertFalse(np.allclose(channel.pixels, fftChannel.pixels))

    def testCreatXYGridsAllOdd(self):
        nbRows = 3
        nbCols = 5
        array = np.ones((nbRows, nbCols))
        x, y = Channel.createXYGridsFromArray(array, False)
        row = [i for i in range(nbCols)]
        handComputedX = np.array([row] * nbRows)
        column = [i for i in range(nbRows)]
        handComputedY = np.array([column] * nbCols).T
        self.assertTrue(np.array_equal(x, handComputedX))
        self.assertTrue(np.array_equal(y, handComputedY))

    def testCreateXYGridsOneOdd(self):
        nbRows = 8
        nbCols = 5
        array = np.ones((nbRows, nbCols))
        x, y = Channel.createXYGridsFromArray(array, False)
        row = [i for i in range(nbCols)]
        handComputedX = np.array([row] * nbRows)
        column = [i for i in range(nbRows)]
        handComputedY = np.array([column] * nbCols).T
        self.assertTrue(np.array_equal(x, handComputedX))
        self.assertTrue(np.array_equal(y, handComputedY))

    def testCreateXYGridsAllEven(self):
        nbRows = 8
        nbCols = 10
        array = np.ones((nbRows, nbCols))
        x, y = Channel.createXYGridsFromArray(array, False)
        row = [i for i in range(nbCols)]
        handComputedX = np.array([row] * nbRows)
        column = [i for i in range(nbRows)]
        handComputedY = np.array([column] * nbCols).T
        self.assertTrue(np.array_equal(x, handComputedX))
        self.assertTrue(np.array_equal(y, handComputedY))

    def testCreateXYGridsAllOddOriginAtCenter(self):
        array = np.ones((5, 5))
        x, y = Channel.createXYGridsFromArray(array)
        handComputedX = np.array([[-2] * 5, [-1] * 5, [0] * 5, [1] * 5, [2] * 5]).T
        handComputedY = np.flipud(handComputedX.T)
        self.assertTrue(np.array_equal(x, handComputedX))
        self.assertTrue(np.array_equal(y, handComputedY))

    def testCreateXYGridsOneOddOriginAtCenter(self):
        array = np.ones((5, 6))
        x, y = Channel.createXYGridsFromArray(array)
        handComputedX = np.array([[-2] * 5, [-1] * 5, [0] * 5, [1] * 5, [2] * 5, [3] * 5]).T
        handComputedY = np.flipud(np.array([np.arange(-2, 3)] * 6).T)
        self.assertTrue(np.array_equal(x, handComputedX))
        self.assertTrue(np.array_equal(y, handComputedY))

    def testCreateXYGridsAllEvenOriginAtCenter(self):
        array = np.ones((6, 6))
        x, y = Channel.createXYGridsFromArray(array)
        handComputedX = np.array([[-2] * 6, [-1] * 6, [0] * 6, [1] * 6, [2] * 6, [3] * 6]).T
        handComputedY = np.flipud(np.array([np.arange(-2, 4)] * 6).T)
        self.assertTrue(np.array_equal(x, handComputedX))
        self.assertTrue(np.array_equal(y, handComputedY))

    def testCreateGaussianMask(self):
        array = np.ones((3, 3))
        xy = Channel.createXYGridsFromArray(array)
        mask = Channel.createGaussianMask(xy, 1 / np.sqrt(2))
        e = np.exp
        handComputedMask = np.array([[e(-2), e(-1), e(-2)], [e(-1), e(0), e(-1)], [e(-2), e(-1), e(-2)]])
        self.assertTrue(np.allclose(mask, handComputedMask))

    def testCreateSigmoidMask(self):
        array = np.ones((3, 3))
        xy = Channel.createXYGridsFromArray(array)
        radius = 1
        mask = Channel.createSigmoidMask(xy, radius)

        def sigmoid(expArg: float) -> float:
            return 1 / (1 + np.exp(-expArg))

        handComputedMask = np.array(
            [[sigmoid(1 - 2 ** (1 / 2)), 1 / 2, sigmoid(1 - 2 ** (1 / 2))], [1 / 2, sigmoid(1), 1 / 2],
             [sigmoid(1 - 2 ** (1 / 2)), 1 / 2, sigmoid(1 - 2 ** (1 / 2))]])
        self.assertTrue(np.allclose(mask, handComputedMask))

    def testPowerSpectrum(self):
        image = Image(path=Path(self.dataDir / "testCziFileTwoChannels.czi"))
        channel = image.channels[-1]
        fftChannel = np.fft.fft2(channel.pixels)
        fftShiftChannel = np.fft.fftshift(fftChannel)
        amplitude = np.abs(fftShiftChannel) ** 2
        self.assertTrue(np.array_equal(channel.powerSpectrum(), amplitude / np.sum(amplitude)))

    def testPowerSpectrumValues(self):
        array = np.array([[i * 2 * np.pi / 8 for i in range(30)]] * 30)
        values = (np.sin(array) + 1) * 255 / 2
        channel = Channel(values.astype(np.uint8) + values.astype(np.uint8).T)
        centerY, centerX = channel.shape[1] // 2, channel.shape[0] // 2
        ps = channel.powerSpectrum()
        sumToMultiply = np.sum(
            np.abs(np.fft.fftshift(np.fft.fft2(values.astype(np.uint8) + values.astype(np.uint8).T))) ** 2)
        # Check if center value is the DC component (after sqrt and normalization)
        self.assertAlmostEqual(np.sqrt(ps[centerY, centerX] * sumToMultiply),
                               np.sum(channel.pixels))

    def testAzimuthalAverage(self):
        array = np.array(
            [[5, 4, 4, 4, 4, 4, 5, 5], [4, 3, 3, 3, 3, 3, 4, 5], [3, 2, 2, 2, 2, 2, 3, 4], [3, 2, 1, 1, 1, 2, 3, 4],
             [3, 2, 1, 0, 1, 2, 3, 4], [3, 2, 1, 1, 1, 2, 3, 4], [3, 2, 2, 2, 2, 2, 3, 4], [4, 3, 3, 3, 3, 3, 4, 5]],
            dtype=np.uint8)
        azmAvg = Channel.azimuthalAverage(array).tolist()
        self.assertListEqual(azmAvg, [0, 1, 2, 3, 4, 5])

    # def testPowerSpectrumCircle(self):
    #     import skimage.morphology.selem as selem
    #     mask = selem.disk(100)
    #     array = np.zeros((500, 500), dtype=np.uint8)
    #     array[500 // 2 - 100:500 // 2 + 100 + 1, 500 // 2 - 100:500 // 2 + 100 + 1] = mask
    #     channel = Channel(array)
    #     channel.display()
    #     rectangle = channel.applyLowPassFilterFromRectangularMask(4)
    #     rectangle.display()
    #     sigmoid = channel.applyLowPassFilterFromSigmoidMask(4)
    #     sigmoid.display()
    #     channel.displayPowerSpectrum(True)
    #
    # def testWeirdFunction(self):
    #     array = np.ones((1000, 1000))
    #     x, y = Channel.createXYGridsFromArray(array)
    #     sin = np.sin
    #     cos = np.cos
    #     tan = np.tan
    #     array_ = sin(cos(tan(x / 150 * y / 150))) <= sin(cos(tan(x / 150))) + sin(cos(tan(y / 150)))
    #     plt.show()
    #     channel = Channel(array_.astype(np.uint8))
    #     channel.display()
    #     channel.displayPowerSpectrum()
    #
    # def testOtherWeirdFunction(self):
    #     array = np.ones((1000, 1000))
    #     x, y = Channel.createXYGridsFromArray(array)
    #     sin = np.sin
    #     cos = np.cos
    #     array_ = sin(sin(x / 50) + cos(y / 50)) >= cos(sin(x * y / (50 ** 2)) + cos(x / 50))
    #     channel = Channel(array_.astype(np.uint8))
    #     channel.display()
    #     channel.displayPowerSpectrum()
    #     channel.displayPhaseSpectrum()
    #
    # def testImage(self):
    #     path = Path(self.dataDir / "testCziFileTwoChannels.czi")
    #     image = Image(path=path)
    #     channel = image.channels[0]
    #     # channel2 = image.channels[1]
    #     # channel.displayPowerSpectrumDensityAzimuthalAverage(2)
    #     # channel.displayPowerSpectrum()
    #     noise = channel.applyGaussianNoise(0, 10)
    #     filtered = noise.applyLowPassFilterFromSigmoidMask(50, 1 / 8)
    #     filtered2 = noise.applyLowPassFilterFromSigmoidMask(50, 1 / 4)
    #     Channel.multiChannelDisplay([noise, filtered, filtered2])


if __name__ == '__main__':
    unittest.main()

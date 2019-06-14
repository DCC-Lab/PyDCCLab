from .channel import *
import cv2 as cv
import warnings


class ChannelInt(Channel):

    def __init__(self, pixels: np.ndarray):
        Channel.__init__(self, pixels)
        if "int" not in str(pixels.dtype):
            raise TypeError("Pixel type must be integer.")
        self._originalFactor = np.iinfo(self._originalDType).max

    def applyConvolution(self, matrix: typing.Union[np.ndarray, list]):
        self.saveOriginal()
        result = self.convolveWith(matrix).convertToUnsignedInt(self._originalDType)
        self._pixels = result.pixels

    def applyGaussianFilter(self, sigma: float):
        self.saveOriginal()
        result = self.getGaussianFilter().convertToUnsignedInt(self._originalDType)
        self._pixels = result.pixels

    def applyXDerivative(self):
        self.saveOriginal()
        result = self.getXAxisDerivative().convertToUnsignedInt(self._originalDType)
        self._pixels = result.pixels

    def applyYDerivative(self):
        self.saveOriginal()
        result = self.getYAxisDerivative().convertToUnsignedInt(self._originalDType)
        self._pixels = result.pixels

    def getHistogramValues(self, normed: bool = False) -> typing.Tuple[np.ndarray, np.ndarray]:
        array = self.pixels.ravel()
        nbBins = len(np.bincount(array))
        hist, bins = np.histogram(array, nbBins, [0, nbBins], density=normed)
        return hist, bins

    def convolveWith(self, matrix: typing.Union[np.ndarray, list]):
        warnings.warn("Converting to float32.")
        floatChannel = self.convertToNormalizedFloat()
        return floatChannel.convolveWith(matrix)

    def getGaussianFilter(self, sigma: float = 1):
        warnings.warn("Converting to float32.")
        floatChannel = self.convertToNormalizedFloat()
        return floatChannel.getGaussianFilter(sigma)

    def getEntropyFiltering(self, filterSize: int):
        if self._originalDType == np.uint16:
            warnings.warn("Converting to uint8.")
        entropyFiltered = entropy(self.convertTo8BitsInteger().pixels, morphology.selem.square(filterSize))
        return Channel(entropyFiltered)

    def getStandardDeviationFilterSlow(self, filterSize: int):
        warnings.warn("Converting to float32.")
        floatChannel = self.convertToNormalizedFloat()
        return floatChannel.getStandardDeviationFilterSlow(filterSize)

    def getStandardDeviationFilter(self, filterSize: int):
        warnings.warn("Converting to float32.")
        floatChannel = self.convertToNormalizedFloat()
        return floatChannel.getStandardDeviationFilter(filterSize)

    def getHorizontalSobelFilter(self):
        warnings.warn("Converting to float32.")
        floatChannel = self.convertToNormalizedFloat()
        return floatChannel.getHorizontalSobelFilter()

    def getVerticalSobelFilter(self):
        warnings.warn("Converting to float32.")
        floatChannel = self.convertToNormalizedFloat()
        return floatChannel.getVerticalSobelFilter()

    def getBothDirectionsSobelFilter(self):
        warnings.warn("Converting to float32.")
        floatChannel = self.convertToNormalizedFloat()
        return floatChannel.getBothDirectionsSobelFilter()

    def getIsodataThresholding(self):
        """
        Adapted from skimage's isodata thresholding method.
        Their version was not behaving properly with our image format (different than uint8).
        :return: The thresholded Channel instance according to isodata method.
        """
        # We ignore warnings related to division by 0 since they give nan and we treat nan later.
        warnings.catch_warnings()
        warnings.simplefilter("ignore", category=RuntimeWarning)
        hist, bins = self.getHistogramValues()

        hist = np.array(hist, dtype=np.float32)
        bins = np.array(bins)
        binsCenters = np.array([(i + i + 1) / 2 for i in range(len(bins) - 1)])
        pixelProbabilityThresholdOne = np.cumsum(hist)
        pixelProbabilityThresholdTwo = np.cumsum(hist[::-1])[::-1] - hist
        intensitySum = hist * binsCenters
        pixelProbabilityThresholdTwo[-1] = 1
        low = np.cumsum(intensitySum) / pixelProbabilityThresholdOne
        high = (np.cumsum(intensitySum[::-1])[::-1] - intensitySum) / pixelProbabilityThresholdTwo
        allMean = (low + high) / 2
        binWidth = binsCenters[1] - binsCenters[0]
        distances = allMean - binsCenters
        thresh = 0
        for i in range(len(distances)):
            if distances[i] is not None and 0 <= distances[i] < binWidth:
                thresh = binsCenters[i]
        threshArray = self.pixels >= thresh
        return Channel(threshArray.astype(np.uint8))

    def getOtsuThresholding(self):
        """
        Adapted from skimage's Otsu thresholding method.
        Their version was not behaving properly with our image format (different than uint8).
        :return: The thresholded DCCImage instance according to Otsu's method.
        """
        # We ignore warnings related to division by 0 since they give nan and we treat nan later.
        warnings.catch_warnings()
        warnings.simplefilter("ignore", category=RuntimeWarning)
        if self.getExtremaValuesOfPixels()[0] == self.getExtremaValuesOfPixels()[1]:
            raise ValueError(
                "This method only works for image with more than one \"color\" (i.e. more than one pixel value).")
        hist, bins = self.getHistogramValues()
        hist = np.array(hist, dtype=np.float32)
        bins = np.array(bins)
        binsCenters = np.array([(i + i + 1) / 2 for i in range(len(bins) - 1)])
        pixelProbabilityGroupOne = np.cumsum(hist)
        pixelProbabilityGroupTwo = np.cumsum(hist[::-1])[::-1]
        pixelIntensityGroupOneMean = np.cumsum(hist * binsCenters) / pixelProbabilityGroupOne
        pixelIntensityGroupTwoMean = (np.cumsum((hist * binsCenters)[::-1]) / pixelProbabilityGroupTwo[::-1])[::-1]
        varianceTwoGroups = pixelProbabilityGroupOne[:-1] * pixelProbabilityGroupTwo[1:] * (
                pixelIntensityGroupOneMean[:-1] - pixelIntensityGroupTwoMean[1:]) ** 2
        index = np.nanargmax(varianceTwoGroups)
        thresh = binsCenters[index]
        threshArray = self.pixels >= thresh
        return Channel(threshArray.astype(np.uint8))

    def getAdaptiveThresholdMean(self, oddRegionSize: int = 3):
        threshArray = cv.adaptiveThreshold(self.convertTo8BitsInteger().pixels, 256, cv.ADAPTIVE_THRESH_MEAN_C,
                                           cv.THRESH_BINARY,
                                           oddRegionSize, 0)
        return Channel(threshArray.astype(np.uint8))

    def getAdaptiveThresholdGaussian(self, oddRegionSize: int = 3):
        threshArray = cv.adaptiveThreshold(self.convertTo8BitsInteger().pixels, 256, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv.THRESH_BINARY, oddRegionSize, 0)
        return Channel(threshArray.astype(np.uint8))

    def convertTo8BitsInteger(self):
        return self.convertToUnsignedInt(np.uint8)

    def convertTo16BitsInteger(self):
        return self.convertToUnsignedInt(np.uint16)

    def convertToNormalizedFloat(self):
        return Channel(np.copy(self.pixels) / self._originalFactor)

    def convertToUnsignedInt(self, dtype):
        convertedArray = np.copy(self.pixels.astype(float)) / self._originalFactor * np.iinfo(dtype).max
        return Channel(convertedArray.astype(dtype))

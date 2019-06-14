from .channel import *
import cv2 as cv
import warnings


class ChannelInt(Channel):

    def __init__(self, pixels: np.ndarray):
        Channel.__init__(self, pixels)
        if "int" not in str(pixels.dtype):
            raise TypeError("Pixel type must be integer.")
        self._originalFactor = np.iinfo(self._originalDType).max

    def convertToNormalizedFloat(self):
        from .channelFloat import ChannelFloat
        # For a bound integer array, we take the maximum of the type
        # and we convert the array to float
        floatArray = np.copy(self.pixels).astype(np.float32)
        return ChannelFloat(floatArray / self._originalFactor)

    def getHistogramValues(self, normed: bool = False) -> typing.Tuple[np.ndarray, np.ndarray]:
        array = self.pixels.ravel()
        nbBins = len(np.bincount(array))
        hist, bins = np.histogram(array, nbBins, [0, nbBins], density=normed)
        return hist, bins

    def convolveWith(self, matrix: typing.Union[np.ndarray, list]):
        warnings.warn("Converting to float32 prior to the convolution.")
        convolvedArray = convolve2d(self.convertToNormalizedFloat().pixels, matrix, mode="same", boundary="symm")
        return Channel(convolvedArray)

    def getEntropyFiltering(self, filterSize: int):
        entropyFiltered = entropy(self.pixels.astype(float), morphology.selem.square(filterSize))
        return Channel(entropyFiltered.astype(np.uint16))

    def getStandardDeviationFilteringSlow(self, filterSize: int):
        stdFiltered = filters.generic_filter(self.pixels.astype(float), np.std, size=filterSize, mode="nearest")
        return Channel(stdFiltered.astype(np.uint16))

    def getStandardDeviationFilter(self, filterSize: int):
        pixels = self.pixels.astype(float)
        stdDevFilter1 = filters.uniform_filter(pixels, filterSize, mode="nearest")
        stdDevFilter2 = filters.uniform_filter(pixels * pixels, filterSize, mode="nearest")
        stdFiltered = np.sqrt(stdDevFilter2 - stdDevFilter1 * stdDevFilter1)
        if np.any(np.isnan(stdFiltered)):
            warnings.warn("Nan values encountered! Replacing them with 0.", category=RuntimeWarning)
            stdFiltered = np.nan_to_num(stdFiltered)
        return Channel(stdFiltered.astype(np.uint16))

    def getGaussianFilter(self, sigma: float = 1):
        gaussianFiltered = gaussian(self.pixels.astype(float), sigma, mode="nearest", multichannel=False,
                                    preserve_range=True)
        return Channel(gaussianFiltered.astype(np.uint16))

    def getHorizontalSobelFilter(self):
        sobelH = sobel_h(self.pixels.astype(float))
        return Channel(sobelH.astype(np.uint16))

    def getVerticalSobelFilter(self):
        sobelV = sobel_v(self.pixels.astype(float))
        return ChannelUint16(sobelV.astype(np.uint16))

    def getBothDirectionsSobelFilter(self):
        sobelHV = sobel(self.pixels.astype(float))
        return Channel(sobelHV.astype(np.uint16))

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
        return Channel(threshArray.astype(np.uint16))

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
        return Channel(threshArray.astype(np.uint16))

    def getAdaptiveThresholdMean(self, oddRegionSize: int = 3):
        threshArray = cv.adaptiveThreshold(self.convertTo8BitsInteger().pixels, 256, cv.ADAPTIVE_THRESH_MEAN_C,
                                           cv.THRESH_BINARY,
                                           oddRegionSize, 0)
        return Channel(threshArray.astype(np.uint16))

    def getAdaptiveThresholdGaussian(self, oddRegionSize: int = 3):
        threshArray = cv.adaptiveThreshold(self.convertTo8BitsInteger().pixels, 256, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv.THRESH_BINARY, oddRegionSize, 0)
        return Channel(threshArray.astype(np.uint16))

    def convertTo8BitsInteger(self):
        convertedArray = np.copy(self.pixels.astype(float)) / self._originalFactor * 255
        return Channel(convertedArray.astype(np.uint8))

    def convertTo16BitsInteger(self):
        convertedArray = np.copy(self.pixels.astype(float)) / self._originalFactor * (2 ** 16 - 1)
        return Channel(convertedArray.astype(np.uint16))

    def convertToNormalizedFloat(self):
        return Channel(self.pixels / self._originalFactor)

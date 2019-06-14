from .channel import *


class ChannelFloat(Channel):

    def __init__(self, pixels: np.ndarray):
        if "float" not in str(pixels.dtype):
            raise TypeError("Pixel type must be float.")
        maxValue = np.max(pixels)
        if maxValue <= 1.0:
            self.__originalFactor = 1.0
            normalizedPixels = np.copy(pixels)
        else:
            self.__originalFactor = maxValue
            normalizedPixels = np.copy(pixels) / maxValue
        Channel.__init__(self, normalizedPixels)

    def getHistogramValues(self, normed: bool = False) -> typing.Tuple[np.ndarray, np.ndarray]:
        pixels = self.convertTo8BitsInteger().pixels
        array = pixels.ravel()
        nbBins = len(np.bincount(array))
        hist, bins = np.histogram(array, nbBins, [0, nbBins], density=normed)
        return hist, bins

    def getEntropyFilter(self, filterSize: int):
        warnings.warn("Converting to uint8.")
        pixels = self.convertTo8BitsInteger().pixels
        entropyFiltered = entropy(pixels, morphology.selem.square(filterSize, dtype=np.float32))
        return Channel(entropyFiltered.astype(np.float32))

    def convolveWith(self, matrix: typing.Union[np.ndarray, list]):
        convolvedArray = convolve2d(self.pixels, matrix, mode="same", boundary="symm")
        return Channel(convolvedArray)

    def getGaussianFilter(self, sigma: float = 1):
        gaussianFiltered = gaussian(self.pixels, sigma, mode="nearest", multichannel=False,
                                    preserve_range=True)
        return Channel(gaussianFiltered)


    def getStandardDeviationFilter(self, filterSize: int):
        pixels = self.pixels
        stdDevFilter1 = filters.uniform_filter(pixels, filterSize, mode="nearest")
        stdDevFilter2 = filters.uniform_filter(pixels * pixels, filterSize, mode="nearest")
        stdFiltered = np.sqrt(stdDevFilter2 - stdDevFilter1 * stdDevFilter1)
        if np.any(np.isnan(stdFiltered)):
            warnings.warn("Nan values encountered! Replacing them with 0.", category=RuntimeWarning)
            stdFiltered = np.nan_to_num(stdFiltered)
        return Channel(stdFiltered)

    def getIsodataThresholding(self):
        integerChannel = self.convertTo8BitsInteger()
        return integerChannel.getIsodataThresholding()

    def getOtsuThresholding(self):
        integerChannel = self.convertTo8BitsInteger()
        return integerChannel.getOtsuThresholding()

    def getAdaptiveThresholdMean(self, oddRegionSize: int = 3):
        integerChannel = self.convertTo8BitsInteger()
        return integerChannel.getAdaptiveThresholdMean(oddRegionSize)

    def getAdaptiveThresholdGaussian(self, oddRegionSize: int = 3):
        integerChannel = self.convertTo8BitsInteger()
        return integerChannel.getAdaptiveThresholdGaussian(oddRegionSize)

    def getHorizontalSobelFilter(self):
        sobelH = sobel_h(self.pixels)
        return Channel(sobelH)

    def getVerticalSobelFilter(self):
        sobelV = sobel_v(self.pixels)
        return Channel(sobelV)

    def getBothDirectionsSobelFilter(self):
        sobelHV = sobel(self.pixels)
        return Channel(sobelHV)

    def convertTo8BitsInteger(self):
        return self.convertToUnsignedInt(np.uint8)

    def convertTo16BitsInteger(self):
        return self.convertToUnsignedInt(np.uint16)

    def convertToUnsignedInt(self, dtype):
        convertedArray = ((np.copy(self.pixels)) * np.iinfo(dtype).max)
        return Channel(convertedArray.astype(dtype))

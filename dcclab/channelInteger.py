from .channel import *
from .channelFloat import ChannelFloat


class ChannelInt(Channel):

    def __init__(self, pixels: np.ndarray):
        Channel.__init__(self, pixels)
        if "int" not in str(pixels.dtype):
            raise TypeError("Pixel type must be integer.")
        self.__originalFactor = np.iinfo(self.__originalDType).max

    def convertToNormalizedFloat(self):
        # For a bound integer array, we take the maximum of the type
        # and we convert the array to float
        floatArray = np.copy(self.pixels).astype(np.float32)
        return ChannelFloat(floatArray / self.__originalFactor)

    def getHistogramValues(self, normed: bool = False) -> typing.Tuple[np.ndarray, np.ndarray]:
        array = self.pixels.ravel()
        nbBins = len(np.bincount(array))
        hist, bins = np.histogram(array, nbBins, [0, nbBins], density=normed)
        return hist, bins


class ChannelUint8(ChannelInt):

    def __int__(self, pixels: np.ndarray):
        ChannelInt.__init__(self, pixels)
        if pixels.dtype != np.uint8:
            raise TypeError("Pixels type must be 8 bits unsigned integer.")

    def convolveWith(self, matrix: typing.Union[np.ndarray, list]):
        convolvedArray = convolve2d(self.pixels.astype(float), matrix, mode="same", boundary="symm")
        return ChannelUint8(convolvedArray.astype(np.uint8))

    def getEntropyFiltering(self, filterSize: int):
        entropyFiltered = entropy(self.pixels.astype(float), morphology.selem.square(filterSize))
        return ChannelUint8(entropyFiltered.astype(np.uint8))

    def getStandardDeviationFilteringSlow(self, filterSize: int):
        stdFiltered = filters.generic_filter(self.pixels.astype(float), np.std, size=filterSize, mode="nearest")
        return ChannelUint8(stdFiltered.astype(np.uint8))

    def getStandardDeviationFilter(self, filterSize: int):
        pixels = self.pixels.astype(float)
        stdDevFilter1 = filters.uniform_filter(pixels, filterSize, mode="nearest")
        stdDevFilter2 = filters.uniform_filter(pixels * pixels, filterSize, mode="nearest")
        stdFiltered = np.sqrt(stdDevFilter2 - stdDevFilter1 * stdDevFilter1)
        if np.any(np.isnan(stdFiltered)):
            warnings.warn("Nan values encountered! Replacing them with 0.", category=RuntimeWarning)
            stdFiltered = np.nan_to_num(stdFiltered)
        return ChannelUint8(stdFiltered.astype(np.uint8))

    def getGaussianFilter(self, sigma: float = 1):
        gaussianFiltered = gaussian(self.pixels.astype(float), sigma, mode="nearest", multichannel=False,
                                    preserve_range=True)
        return ChannelUint8(gaussianFiltered.astype(np.uint8))

    def getHorizontalSobelFilter(self):
        sobelH = sobel_h(self.pixels.astype(float))
        return ChannelUint8(sobelH.astype(np.uint8))

    def getVerticalSobelFilter(self):
        sobelV = sobel_v(self.pixels.astype(float))
        return ChannelUint8(sobelV.astype(np.uint8))

    def getBothDirectionsSobelFilter(self):
        sobelHV = sobel(self.pixels.astype(float))
        return ChannelUint8(sobelHV.astype(np.uint8))

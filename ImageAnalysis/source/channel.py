import numpy as np
import typing
from skimage import color, measure, morphology, feature, img_as_ubyte
from skimage.filters.rank import entropy
import PIL.Image
from scipy.signal import convolve2d
from scipy.ndimage import label, sum, measurements, distance_transform_edt, filters
from skimage.filters import *
from DCCExceptions import *
import matplotlib.pyplot as plt
import warnings


class Channel:

    def __init__(self, pixels: np.ndarray):
        if not pixels.dtype == np.float32:
            raise PixelTypeException
        if pixels.ndim > 2:
            raise DimensionException(pixels.ndim)
        self.__pixels = pixels
        self.__dimensions = pixels.ndim
        self.__shape = pixels.shape

    def __eq__(self, other) -> bool:
        if not isinstance(other, Channel):
            raise InvalidEqualityTestException(type(other))
        return np.array_equal(self.__pixels, other.getPixels())

    def getPixels(self) -> np.ndarray:
        return self.__pixels

    def getWidth(self) -> int:
        return int(self.__shape[0])

    def getLength(self) -> int:
        return int(self.__shape[1])

    def getNumberOfPixels(self) -> int:
        return self.getLength() * self.getWidth()

    def copy(self) -> np.ndarray:
        return np.copy(self.__pixels)

    def displayChannel(self, colorMap=None):
        plt.imshow(self.__pixels, cmap=colorMap)
        plt.show()
        return self

    @staticmethod
    def __convertPixelsTo16BitsUnsignedInt(pixels: np.ndarray) -> np.ndarray:
        return pixels.astype(np.uint16)

    @staticmethod
    def __ravelPixels(pixels: np.ndarray) -> np.ndarray:
        return pixels.ravel()

    def getHistogramValues(self, normed: bool = False) -> typing.Tuple[np.ndarray, np.ndarray]:
        array = self.__ravelPixels(self.__convertPixelsTo16BitsUnsignedInt(self.__pixels))
        nbBins = len(np.bincount(array))
        hist, bins = np.histogram(array, nbBins, [0, nbBins], density=normed)
        return hist, bins

    def displayHistogram(self, normed: bool = False) -> typing.Tuple[np.ndarray, np.ndarray]:
        histogram, bins = self.getHistogramValues(normed)
        plt.bar(bins[:-1], histogram, width=np.diff(bins), ec="k", align="edge", color="black", alpha=0.5)
        plt.show()
        return histogram, bins

    def convolveWith(self, matrix: typing.Union[np.ndarray, list]):
        # todo test unitaire
        convolvedArray = convolve2d(self.__pixels, matrix, mode="same", boundary="symm")
        return Channel(convolvedArray.astype(np.float32))

    def getXAxisDerivative(self):
        dxFilter = [[-1, 0, 1]]
        return self.convolveWith(dxFilter)

    def getYAxisDerivative(self):
        dyFilter = [[-1], [0], [1]]
        return self.convolveWith(dyFilter)

    def getAverageValueOfPixels(self) -> float:
        return np.average(self.__pixels)

    def getStadardDeviationOfPixels(self):
        return np.std(self.__pixels)

    def getShannonEntropyOfPixels(self, base=2) -> float:
        return measure.shannon_entropy(self.__pixels, base)

    def getExtremaValuesOfPixels(self) -> typing.Tuple[int, int]:
        return np.min(self.__pixels), np.max(self.__pixels)

    def getPixelsOfIntensity(self, intensity: float) -> typing.List[tuple]:
        coordsList = []
        array = self.__pixels
        coordsTemp = np.where(array[:, :] == intensity)
        coords = list(zip(coordsTemp[0], coordsTemp[1])) if len(coordsTemp[0]) != 0 else None
        coordsList.append(coords)
        coordsList = coordsList[0]
        return coordsList

    def getMinimumIntensityPixels(self) -> typing.List[typing.Tuple[int, int]]:
        minimum = self.getExtremaValuesOfPixels()[0]
        return self.getPixelsOfIntensity(minimum)

    def getMaximumIntensityPixels(self):
        maximum = self.getExtremaValuesOfPixels()[1]
        return self.getPixelsOfIntensity(maximum)

    def getEntropyFiltering(self, filterSize: int):
        # We have to cast image in 8 bits uint because the algorithm semms to properly works only in this type
        image = img_as_ubyte(self.__pixels)
        entropyFiltered = entropy(image, morphology.selem.square(filterSize, dtype=np.float32))
        return Channel(entropyFiltered.astype(np.float32))

    def getStandardDeviationFilteringSlow(self, filterSize: int):
        message = "This filtering method is very slow with big images. " \
                  "Use getStandardDeviationFiltering for faster results."
        warnings.warn(message)
        # VERY SLOW WITH BIG IMAGES
        stdFiltered = filters.generic_filter(self.__pixels, np.std, size=filterSize, mode="nearest")
        return Channel(stdFiltered.astype(np.float32))

    def getStandardDeviationFiltering(self, filterSize: int):
        stdDevFilter1 = filters.uniform_filter(self.__pixels, filterSize, mode="nearest")
        stdDevFilter2 = filters.uniform_filter(self.__pixels * self.__pixels, filterSize, mode="nearest")
        stdFiltered = np.sqrt(stdDevFilter2 - stdDevFilter1 * stdDevFilter1).astype(np.float32)
        if np.any(np.isnan(stdFiltered)):
            warnings.warn("Nan values encountered! Replacing them with 0.", category=RuntimeWarning)
            stdFiltered = np.nan_to_num(stdFiltered)
        return Channel(stdFiltered)

    def getGaussianFiltering(self, sigma: float = 1):
        gaussianFiltered = gaussian(self.__pixels, sigma, mode="nearest", multichannel=False, preserve_range=True)
        return Channel(gaussianFiltered.astype(np.float32))

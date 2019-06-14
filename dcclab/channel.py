import numpy as np
import typing

from skimage import measure, morphology
from skimage.filters.rank import entropy
from skimage.filters import *

from scipy.signal import convolve2d
from scipy.ndimage import label, sum, filters
from .DCCExceptions import *

import matplotlib.pyplot as plt

import warnings

try:
    from deprecated import deprecated
except:
    exit("need 'deprecated' module: pip install deprecated")


class Channel:

    def __new__(cls, pixels: np.ndarray):
        if cls is Channel:
            if "float" in str(pixels.dtype):
                return super(Channel, cls).__new__(ChannelFloat)
            elif "int" in str(pixels.dtype):
                return super(Channel, cls).__new__(ChannelInt)
            else:
                raise PixelTypeException("Can't read images of type {}".format(pixels.dtype))

    def __init__(self, pixels: np.ndarray):
        pixels.squeeze()
        if pixels.ndim != 2:
            raise DimensionException(pixels.ndim)
        self._pixels = np.copy(pixels)
        self._originalDType = pixels.dtype
        self.__original = None

    def __str__(self):
        return str(self.pixels)

    @property
    def pixels(self):
        return self._pixels

    @property
    def dimension(self):
        return self.pixels.ndim

    @property
    def shape(self):
        return self.pixels.shape

    @property
    def width(self) -> int:
        return int(self.shape[0])

    @property
    def height(self) -> int:
        return int(self.shape[1])

    @property
    def sizeInBytes(self) -> int:
        return self.pixels.nbytes

    @property
    def numberOfPixels(self) -> int:
        return self.width * self.height

    def __eq__(self, other) -> bool:
        if not isinstance(other, Channel):
            return False
        return np.array_equal(self.pixels, other.pixels)

    def copy(self) -> np.ndarray:
        return np.copy(self.pixels)

    @property
    def isBinary(self) -> bool:
        return np.array_equal(self.pixels, self.pixels.astype(bool))

    """ Display-related functions """

    def display(self, colorMap=None):
        plt.imshow(self.pixels, cmap=colorMap)
        plt.show()
        return self

    def getHistogramValues(self, normed: bool = False) -> typing.Tuple[np.ndarray, np.ndarray]:
        pass

    def displayHistogram(self, normed: bool = False) -> typing.Tuple[np.ndarray, np.ndarray]:
        histogram, bins = self.getHistogramValues(normed)
        plt.bar(bins[:-1], histogram, width=np.diff(bins), ec="k", align="edge", color="black", alpha=0.5)
        plt.show()
        return histogram, bins

    """ Manipulation-related functions """

    def convertToNormalizedFloat(self):
        pass

    def saveOriginal(self):
        if self.__original == None:
            self.__original = np.copy(self.pixels)

    def restoreOriginal(self):
        if self.__original is not None:
            self._pixels = self.__original

    def applyConvolution(self, matrix: typing.Union[np.ndarray, list]):
        self.saveOriginal()
        result = self.convolveWith(matrix)
        self._pixels = result.pixels

    def applyXDerivative(self):
        self.saveOriginal()
        result = self.getXAxisDerivative()
        self._pixels = result.pixels

    def applyYDerivative(self):
        self.saveOriginal()
        result = self.getYAxisDerivative()
        self._pixels = result.pixels

    def applyGaussianFilter(self, sigma: float):
        self.saveOriginal()
        result = self.getGaussianFilter(sigma)
        self._pixels = result.pixels

    def applyThresholding(self):
        self.applyIsodataThresholding()

    def applyIsodataThresholding(self):
        self.saveOriginal()
        result = self.getIsodataThresholding()
        self._pixels = result.pixels

    def applyOtsuThresholding(self):
        self.saveOriginal()
        result = self.getOtsuThresholding()
        self._pixels = result.pixels

    def applyOpening(self):
        self.saveOriginal()
        if self.isBinary:
            result = self.getBinaryOpening()
        else:
            result = self.getOpening()
        self._pixels = result.pixels

    def applyClosing(self):
        self.saveOriginal()
        if self.isBinary:
            result = self.getBinaryClosing()
        else:
            result = self.getClosing()
        self._pixels = result.pixels

    def convolveWith(self, matrix: typing.Union[np.ndarray, list]):
        pass

    def getXAxisDerivative(self):
        dxFilter = [[-1, 0, 1]]
        return self.convolveWith(dxFilter)

    def getYAxisDerivative(self):
        dyFilter = [[-1], [0], [1]]
        return self.convolveWith(dyFilter)

    def getAverageValueOfPixels(self) -> float:
        return np.average(self.pixels)

    def getStandardDeviationOfPixels(self):
        return np.std(self.pixels)

    def getShannonEntropyOfPixels(self, base=2) -> float:
        return measure.shannon_entropy(self.pixels, base)

    def getExtremaValuesOfPixels(self) -> typing.Tuple[int, int]:
        return np.min(self.pixels), np.max(self.pixels)

    def getPixelsOfIntensity(self, intensity: float) -> typing.List[tuple]:
        coordsList = []
        array = self.pixels
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

    def getEntropyFilter(self, filterSize: int):
        pass

    @deprecated(reason="Too slow. Use getStandardDeviationFilter")
    def getStandardDeviationFilterSlow(self, filterSize: int):
        pass

    def getStandardDeviationFilter(self, filterSize: int):
        pass

    def getGaussianFilter(self, sigma: float = 1):
        pass

    def getHorizontalSobelFilter(self):
        pass

    def getVerticalSobelFilter(self):
        pass

    def getBothDirectionsSobelFilter(self):
        pass

    def getIsodataThresholding(self):
        pass

    def getOtsuThresholding(self):
        pass

    def getAdaptiveThresholdMean(self, oddRegionSize: int = 3):
        pass

    def getAdaptiveThresholdGaussian(self, oddRegionSize: int = 3):
        pass

    def getOpening(self, windowSize: int = 3):
        opened = morphology.opening(self.pixels, np.ones((windowSize, windowSize)))
        return Channel(opened)

    def getBinaryOpening(self, windowSize: int = 3):
        if not self.isBinary:
            raise NotBinaryImageException
        binaryOpened = morphology.binary_opening(self.pixels, np.ones((windowSize, windowSize))).astype(np.float32)
        return Channel(binaryOpened)

    def getClosing(self, windowSize: int = 3):
        closed = morphology.closing(self.pixels, np.ones((windowSize, windowSize)))
        return Channel(closed)

    def getBinaryClosing(self, windowSize: int = 3):
        if not self.isBinary:
            raise NotBinaryImageException
        binarClosed = morphology.binary_closing(self.pixels, np.ones((windowSize, windowSize))).astype(np.float32)
        return Channel(binarClosed)

    def getConnectedComponents(self, connectionStructure: np.ndarray = None) -> tuple:
        if not self.isBinary:
            raise NotBinaryImageException
        labeled, nbObjects = label(self.pixels, structure=connectionStructure)
        sizes = sum(self.pixels, labeled, range(nbObjects + 1))
        return Channel(labeled), nbObjects, sizes

    def convertTo16BitsInteger(self):
        pass

    def convertTo8BitsInteger(self):
        pass

    def convertToUnsignedInt(self, dtype):
        pass


from .channelFloat import ChannelFloat
from .channelInteger import ChannelInt

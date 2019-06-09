import numpy as np
from typing import List
import typing

from skimage import measure, morphology, img_as_ubyte
from skimage.filters.rank import entropy
from scipy.signal import convolve2d
from scipy.ndimage import label, sum, filters
from skimage.filters import *
from DCCExceptions import *
import matplotlib.pyplot as plt
import warnings
try:
    from deprecated import deprecated
except:
    exit("need 'deprecated' module: pip install deprecated")

class ChannelDisplay:

    def displayChannel(self, colorMap=None):
        plt.imshow(self.pixels, cmap=colorMap)
        plt.show()
        return self

    def getHistogramValues(self, normed: bool = False) -> typing.Tuple[np.ndarray, np.ndarray]:
        array = self.pixels.astype(np.uint16).ravel()
        nbBins = len(np.bincount(array))
        hist, bins = np.histogram(array, nbBins, [0, nbBins], density=normed)
        return hist, bins

    def displayHistogram(self, normed: bool = False) -> typing.Tuple[np.ndarray, np.ndarray]:
        histogram, bins = self.getHistogramValues(normed)
        plt.bar(bins[:-1], histogram, width=np.diff(bins), ec="k", align="edge", color="black", alpha=0.5)
        plt.show()
        return histogram, bins


class ChannelMath:
    def convolveWith(self, matrix: typing.Union[np.ndarray, list]):
        # todo test unitaire
        convolvedArray = convolve2d(self.pixels, matrix, mode="same", boundary="symm")
        return Channel(convolvedArray.astype(np.float32))

    def getXAxisDerivative(self):
        dxFilter = [[-1, 0, 1]]
        return self.convolveWith(dxFilter)

    def getYAxisDerivative(self):
        dyFilter = [[-1], [0], [1]]
        return self.convolveWith(dyFilter)

    def getAverageValueOfPixels(self) -> float:
        return np.average(self.pixels)

    def getStadardDeviationOfPixels(self):
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

    def getEntropyFiltering(self, filterSize: int):
        # We have to cast image in 8 bits uint because the algorithm semms to properly works only in this type
        image = img_as_ubyte(self.pixels)
        entropyFiltered = entropy(image, morphology.selem.square(filterSize, dtype=np.float32))
        return Channel(entropyFiltered.astype(np.float32))

    def getStandardDeviationFilteringSlow(self, filterSize: int):
        message = "This filtering method is very slow with big images. " \
                  "Use getStandardDeviationFiltering for faster results."
        warnings.warn(message)
        # VERY SLOW WITH BIG IMAGES
        stdFiltered = filters.generic_filter(self.pixels, np.std, size=filterSize, mode="nearest")
        return Channel(stdFiltered.astype(np.float32))

    def getStandardDeviationFiltering(self, filterSize: int):
        stdDevFilter1 = filters.uniform_filter(self.pixels, filterSize, mode="nearest")
        stdDevFilter2 = filters.uniform_filter(self.pixels * self.pixels, filterSize, mode="nearest")
        stdFiltered = np.sqrt(stdDevFilter2 - stdDevFilter1 * stdDevFilter1).astype(np.float32)
        if np.any(np.isnan(stdFiltered)):
            warnings.warn("Nan values encountered! Replacing them with 0.", category=RuntimeWarning)
            stdFiltered = np.nan_to_num(stdFiltered)
        return Channel(stdFiltered)

    def getGaussianFiltering(self, sigma: float = 1):
        gaussianFiltered = gaussian(self.pixels, sigma, mode="nearest", multichannel=False, preserve_range=True)
        return Channel(gaussianFiltered.astype(np.float32))

    def getHorizontalSobelFiltering(self):
        sobelH = sobel_h(self.pixels)
        return Channel(sobelH.astype(np.float32))

    def getVerticalSobelFiltering(self):
        sobelV = sobel_v(self.pixels)
        return Channel(sobelV.astype(np.float32))

    def getBothDirectionsSobelFiltering(self):
        sobelHV = sobel(self.pixels)
        return Channel(sobelHV.astype(np.float32))

    def getIsodataThresholding(self):
        """
        Adapted from skimage's isodata thresholding method.
        Their version was not behaving properly with our image format (different than uint8).
        :return: The thresholded DCCImage instance according to isodata method.
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
        return Channel(threshArray.astype(np.float32))

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
        return Channel(threshArray.astype(np.float32))

    def getAdaptiveThreshold(self):
        # todo voir avec openCV
        pass

    def getOpening(self, windowSize: int = 3):
        opened = morphology.opening(self.pixels, np.ones((windowSize, windowSize)))
        return Channel(opened)

    def getBinaryOpening(self, windowSize: int = 3):
        if not self.arePixelsInBinary():
            raise NotBinaryImageException
        binaryOpened = morphology.binary_opening(self.pixels, np.ones((windowSize, windowSize))).astype(np.float32)
        return Channel(binaryOpened)

    def getClosing(self, windowSize: int = 3):
        closed = morphology.closing(self.pixels, np.ones((windowSize, windowSize)))
        return Channel(closed)

    def getBinaryClosing(self, windowSize: int = 3):
        if not self.arePixelsInBinary():
            raise NotBinaryImageException
        binarClosed = morphology.binary_closing(self.pixels, np.ones((windowSize, windowSize))).astype(np.float32)
        return Channel(binarClosed)

    def getConnectedComponents(self) -> tuple:
        if not self.arePixelsInBinary():
            raise NotBinaryImageException
        labeled, nbObjects = label(self.pixels)
        sizes = sum(self.pixels, labeled, range(nbObjects + 1))
        return Channel(labeled.astype(np.float32)), nbObjects, sizes


class Channel(ChannelMath, ChannelDisplay):

    def __init__(self, pixels: np.ndarray):
        if not pixels.dtype == np.float32:
            raise PixelTypeException
        if pixels.ndim > 2:
            raise DimensionException(pixels.ndim)
        self.__pixels = pixels

    @property
    def pixels(self):
        return self.__pixels

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
    def length(self) -> int:
        return self.height

    @property
    def numberOfPixels(self) -> int:
        return self.width() * self.height()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Channel):
            raise InvalidEqualityTestException(type(other))
        return np.array_equal(self.pixels, other.pixels())

    @deprecated(reason="Renamed as a @property pixels")    
    def getPixels(self) -> np.ndarray:
        return self.pixels

    @deprecated(reason="Renamed as a @property width")    
    def getWidth(self) -> int:
        return self.width

    @deprecated(reason="Renamed as a @property height")    
    def getLength(self) -> int:
        return self.height

    @deprecated(reason="Renamed as a @property numberOfPixels")    
    def getNumberOfPixels(self) -> int:
        return self.getLength() * self.getWidth()

    def copy(self) -> np.ndarray:
        return np.copy(self.pixels)

    @deprecated(reason="Renamed as a @property isBinary")    
    def arePixelsInBinary(self) -> bool:
        return self.isBinary

    @property
    def isBinary(self) -> bool:
        return np.alltrue(np.logical_or(self.pixels == 0, self.pixels) == 1)

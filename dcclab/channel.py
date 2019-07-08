import numpy as np
import typing

from skimage import measure, morphology
from skimage.filters.rank import entropy
from skimage.filters import *

from scipy.signal import convolve2d
from scipy.ndimage import label, sum, filters
import scipy.ndimage as ndimage
from .DCCExceptions import *

import matplotlib.pyplot as plt
import json
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
            elif "int" in str(pixels.dtype) or "bool" in str(pixels.dtype):
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

        # Segmentation @properties
        self.mask = None  # type: Channel
        self.labelledComponents = None
        self.numberOfComponents = 0
        self.componentsProperties = None

    def __str__(self) -> str:
        return str(self.pixels)

    @property
    def pixels(self) -> np.ndarray:
        return self._pixels

    @property
    def dimension(self) -> int:
        return self.pixels.ndim

    @property
    def shape(self) -> typing.Tuple[int, int]:
        return self.pixels.shape

    @property
    def width(self) -> int:
        return int(self.shape[1])

    @property
    def height(self) -> int:
        return int(self.shape[0])

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

    @property
    def hasMask(self) -> bool:
        if self.mask is not None:
            return self.mask.isBinary
        return False

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

    """ High-level Image segmentation functions """

    @property
    def hasLabelledComponents(self) -> bool:
        return self.labelledComponents is not None

    def labelMaskComponents(self):
        if self.hasMask:
            labels, nbObjects = ndimage.label(self.mask.pixels)
            self.labelledComponents = labels
            self.numberOfComponents = nbObjects
        else:
            # FIXME: Should use pixels if isBinary ?
            raise Exception("Channel has no mask")

    def analyzeComponents(self) -> dict:
        if self.isLabelled:
            maskSizes = ndimage.sum(self.mask.pixels, self.labelledComponents, range(1, self.numberOfComponents + 1))
            sumValues = ndimage.sum(self.pixels, self.labelledComponents, range(1, self.numberOfComponents + 1))
            centersOfMass = ndimage.center_of_mass(self.pixels, self.labelledComponents,
                                                   range(1, self.numberOfComponents + 1))
            # centerOfMass = np.average(self.params["objectsCM"], axis=0, weights=self.params["objectsMass"])
            properties = dict()
            properties["objectsSize"] = maskSizes
            # properties["totalSize"] = np.sum(self.params["objectsSize"])
            # properties["objectsMass"] = self.__getObjectsMass()
            # properties["totalMass"] = np.sum(self.params["objectsMass"])
            properties["objectsCM"] = centersOfMass
            # properties["totalCM"] = self.__getCenterOfMass()
            self.componentsProperties = properties
            return properties
        else:
            raise ValueError("Channel has not been labelled")

    def saveComponentsStatistics(self, filePath: str):
        properties = self.analyzeComponents()
        jsonParams = json.dumps(properties, indent=4)
        if filePath.split(".")[-1] != "json":
            filePath += ".json"

        with open(filePath, "w+") as file:
            file.write(jsonParams)

    """ Manipulation-related functions """

    def convertToNormalizedFloat(self):
        pass

    def convertToNormalizedFloatMinToZeroMaxToOne(self):
        pass

    def convertToNormalizedFloat(self):
        pass

    def filterNoise(self):
        self.applyNoiseFilter()

    def threshold(self, value=None):
        if value is not None:
            self.applyGlobalThresholding(value)
        else:
            self.applyThresholding()

    def setMask(self, mask):
        if mask.isBinary:
            self.mask = mask
        else:
            raise NotImplementedError("Mask must be binary")

    def setMaskFromThreshold(self, value=None):
        if value is not None:
            binaryMask = self.pixels > value
            self.mask = Channel(pixels=binaryMask)
        else:
            raise NotImplementedError("Mask requires a value for thresholding")

    def saveOriginal(self) -> None:
        if self.__original is None:
            self.__original = np.copy(self.pixels)

    def restoreOriginal(self) -> None:
        if self.__original is not None:
            self._pixels = self.__original

    @property
    def originalPixels(self) -> np.ndarray:
        if self.__original is not None:
            return self.__original

    @property
    def hasOriginal(self) -> bool:
        if self.__original is not None:
            return True
        return False

    def replaceFromArray(self, channelArray):
        assert channelArray.ndim == 2
        self.saveOriginal()
        self._pixels = channelArray

    def applyConvolution(self, matrix: typing.Union[np.ndarray, list]) -> None:
        self.saveOriginal()
        result = self.convolveWith(matrix)
        self._pixels = result.pixels

    def applyXDerivative(self) -> None:
        self.saveOriginal()
        result = self.getXAxisDerivative()
        self._pixels = result.pixels

    def applyYDerivative(self) -> None:
        self.saveOriginal()
        result = self.getYAxisDerivative()
        self._pixels = result.pixels

    def applyGaussianFilter(self, sigma: float) -> None:
        self.saveOriginal()
        result = self.getGaussianFilter(sigma)
        self._pixels = result.pixels

    def applyThresholding(self, value=None) -> None:
        if value is None:
            self.applyIsodataThresholding()
        else:
            self.applyGlobalThresholding(value)

    def applyGlobalThresholding(self, value) -> None:
        self.saveOriginal()
        result = self.getGlobalThresholding(value)
        self._pixels = result.pixels

    def applyIsodataThresholding(self) -> None:
        self.saveOriginal()
        result = self.getIsodataThresholding()
        self._pixels = result.pixels

    def applyOtsuThresholding(self) -> None:
        self.saveOriginal()
        result = self.getOtsuThresholding()
        self._pixels = result.pixels

    def applyOpening(self, size: int) -> None:
        self.saveOriginal()
        if self.isBinary:
            result = self.getBinaryOpening(size)
        else:
            result = self.getOpening(size)
        self._pixels = result.pixels

    def applyClosing(self, size: int) -> None:
        self.saveOriginal()
        if self.isBinary:
            result = self.getBinaryClosing(size)
        else:
            result = self.getClosing(size)
        self._pixels = result.pixels

    def applyNdImageBinaryOpening(self, size: int = None, iterations: int = 1):
        # fixme: mask.applyOpening already exist: but ndimage method differs from morphology
        self.saveOriginal()
        if not self.isBinary:
            raise TypeError("Channel has to be binary")
        struct = None
        if size is not None:
            struct = np.ones((size, size))
        self._pixels = ndimage.binary_opening(self.pixels, struct, iterations=iterations)

    def applyNdImageBinaryClosing(self, size: int = None, iterations: int = 1):
        self.saveOriginal()
        if not self.isBinary:
            raise TypeError("Channel has to be binary")
        struct = None
        if size is not None:
            struct = np.ones((size, size))
        self._pixels = ndimage.binary_closing(self.pixels, struct, iterations=iterations)

    def applyErosion(self, size: int = 2):
        self.saveOriginal()
        result = self.getErosion(size)
        self._pixels = result.pixels

    def applyDilation(self, size: int = 2):
        self.saveOriginal()
        result = self.getDilation(size)
        self._pixels = result.pixels

    def applyNoiseFilter(self, algorithm=None):
        self.saveOriginal()
        result = self.getNoiseFiltering(algorithm)
        self._pixels = result.pixels

    def applyNoiseFilterWithErosionDilation(self, erosion_size=2, dilation_size=2, closing_size=2):
        self.saveOriginal()
        result = self.getNoiseFilteringWithErosionDilation(erosion_size, dilation_size, closing_size)
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

    @deprecated("Renamed getStandardDeviation()")
    def getStandardDeviationOfPixels(self) -> float:
        return self.getStandardDeviation()

    def getStandardDeviation(self) -> float:
        return np.std(self.pixels)

    @deprecated("Renamed getShannonEntropy()")
    def getShannonEntropyOfPixels(self, base=2) -> float:
        return self.getShannonEntropy(base=base)

    def getShannonEntropy(self, base=2) -> float:
        return measure.shannon_entropy(self.pixels, base)

    @deprecated("Renamed getExtrema()")
    def getExtremaValuesOfPixels(self) -> typing.Tuple[int, int]:
        return self.getExtrema()

    def getExtrema(self) -> typing.Tuple[int, int]:
        return np.min(self.pixels), np.max(self.pixels)

    def getMedian(self):
        import time
        before = time.clock()
        median = np.median(self.pixels)
        after = time.clock()
        print("Median cpu time : {}".format(after - before))
        return median

    def getPixelsOfIntensity(self, intensity: float) -> typing.List[tuple]:
        coordsList = []
        array = self.pixels
        coordsTemp = np.where(array[:, :] == intensity)
        coords = list(zip(coordsTemp[0], coordsTemp[1])) if len(coordsTemp[0]) != 0 else None
        coordsList.append(coords)
        coordsList = coordsList[0]
        return coordsList

    @deprecated("Renamed getMinimum()")
    def getMinimumIntensityPixels(self) -> typing.List[typing.Tuple[int, int]]:
        return self.getMinimum()

    def getMinimum(self) -> typing.List[typing.Tuple[int, int]]:
        minimum = self.getExtremaValuesOfPixels()[0]
        return self.getPixelsOfIntensity(minimum)

    @deprecated("Renamed getMaximum()")
    def getMaximumIntensityPixels(self) -> typing.List[tuple]:
        return self.getMaximum()

    def getMaximum(self) -> typing.List[tuple]:
        maximum = self.getExtremaValuesOfPixels()[1]
        return self.getPixelsOfIntensity(maximum)

    def getEntropyFilter(self, filterSize: int):
        pass

    def getStandardDeviationFilter(self, filterSize: int):
        pass

    def getGaussianFilter(self, sigma: float = 1):
        pass

    def getHorizontalSobelFilter(self):
        pass

    def getVerticalSobelFilter(self):
        pass

    @deprecated("Renamed getSobelFilter()")
    def getBothDirectionsSobelFilter(self):
        return self.getSobelFilter()

    def getSobelFilter(self):
        pass

    def getGlobalThresholding(self, value):
        mask = self.pixels > value
        return Channel(self.pixels * mask)

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

    def getErosion(self, size: int = 2):
        return Channel(ndimage.grey_erosion(self.pixels, size=size))

    def getDilation(self, size: int = 2):
        return Channel(ndimage.grey_dilation(self.pixels, size=size))

    def getNoiseFiltering(self, algorithm=None):
        return self.getNoiseFilteringWithErosionDilation()

    def getNoiseFilteringWithErosionDilation(self, erosion_size=2, dilation_size=2, closing_size=2):
        workingChannel = self.getErosion(erosion_size)
        workingChannel.applyDilation(dilation_size)
        workingChannel.applyClosing(closing_size)
        return workingChannel

    def getConnectedComponents(self, connectionStructure: np.ndarray = None) -> tuple:
        if not self.isBinary:
            raise NotBinaryImageException
        labeled, nbObjects = label(self.pixels, structure=connectionStructure)
        sizes = sum(self.pixels, labeled, range(nbObjects + 1))
        return Channel(labeled), nbObjects, sizes

    def convertTo16BitsUnsignedInteger(self):
        pass

    def convertTo8BitsUnsignedInteger(self):
        pass

    def _convertToUnsignedInt(self, dtype):
        pass

    @staticmethod
    def multiChannelDisplay(channels: list):
        nrows = int(np.ceil(len(channels) / 4))
        ncols = len(channels) if len(channels) < 4 else 4
        for i in range(len(channels)):
            plt.subplot(nrows, ncols, i + 1)
            plt.imshow(channels[i].pixels)
        plt.show()

    def applyHighPassFilterFromMask(self, filterSize: int):
        fftShiftPixels = self.fourierTransform()
        rows, cols = self.pixels.shape
        halfRows, halfCols = rows // 2, cols // 2
        fftShiftPixels[halfRows - filterSize:halfRows + filterSize,
        halfCols - filterSize:halfCols + filterSize] = 0
        ifftShift = np.fft.ifftshift(fftShiftPixels)
        filteredPixels = np.abs(np.fft.ifft2(ifftShift))
        return Channel(filteredPixels)

    def applyLowPassFilterFromMask(self, filterSize: int):
        fftShiftPixels = self.fourierTransform()
        rows, cols = self.pixels.shape
        halfRows, halfCols = rows // 2, cols // 2
        mask = np.zeros((rows, cols), np.uint8)
        mask[halfRows - filterSize:halfRows + filterSize, halfCols - filterSize:halfCols + filterSize] = 1
        fftShiftPixelsWithMask = fftShiftPixels * mask
        ifftShift = np.fft.ifftshift(fftShiftPixelsWithMask)
        filteredPixels = np.abs(np.fft.ifft2(ifftShift))
        return Channel(filteredPixels)

    def powerSpectrum(self, naturalLogScale: bool = True) -> np.ndarray:
        fftShiftPixels = self.fourierTransform()
        powerSpectrum = np.abs(fftShiftPixels) ** 2
        if naturalLogScale:
            powerSpectrum = np.log(powerSpectrum)
        return powerSpectrum

    def fourierTransform(self, shift: bool = True) -> np.ndarray:
        pixels = self.pixels
        fftPixels = np.fft.fft2(pixels)
        if shift:
            fftPixels = np.fft.fftshift(fftPixels)
        return fftPixels


from .channelFloat import ChannelFloat
from .channelInteger import ChannelInt

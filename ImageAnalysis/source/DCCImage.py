import numpy as np
import typing
from skimage import color, measure, morphology, feature
from skimage.filters.rank import entropy
import PIL.Image
from scipy.signal import convolve2d
from scipy.ndimage import label, sum, measurements, distance_transform_edt, filters
from skimage.filters import *
from DCCImagesExceptions import *
import matplotlib.pyplot as plt
import warnings


class DCCImage:
    def __init__(self, imageAsArray: np.ndarray):
        if not imageAsArray.dtype == np.float32:
            raise PixelTypeException
        if not (1 < imageAsArray.ndim <= 3):
            raise ImageDimensionsException(imageAsArray.ndim)
        self.__pixelArray = imageAsArray
        self.__dimensions = imageAsArray.ndim
        self.__shape = imageAsArray.shape

    def __str__(self):
        return str(self.getArray())

    def __eq__(self, other) -> bool:
        if not isinstance(other, DCCImage):
            raise InvalidEqualityTestException(type(other))
        return np.array_equal(self.__pixelArray, other.getArray())

    def getArray(self) -> np.ndarray:
        return self.__pixelArray

    def getWidth(self) -> int:
        return int(self.__shape[0])

    def getLength(self) -> int:
        return int(self.__shape[1])

    def getNumberOfChannel(self) -> int:
        if self.isImageInGray():
            nbChannels = 1
        else:
            nbChannels = self.__shape[-1]
        return int(nbChannels)

    def getNumberOfPixels(self) -> int:
        return self.getLength() * self.getWidth()

    def toPILImage(self) -> PIL.Image.Image:
        return PIL.Image.fromarray(self.__pixelArray)

    def copyDCCImage(self):
        copyArray = np.copy(self.__pixelArray)
        return DCCImage(copyArray)

    def showImage(self, showInGray: bool = True):
        if self.isImageInGray() and showInGray:
            plt.gray()
        plt.imshow(self.__pixelArray)
        plt.show()
        return self

    def saveToTIFF(self, name: str):
        unacceptedChars = ["?", "/", "\\", "*", "<", ">", "|", "."]
        name = name.strip()
        if len(name) == 0 or name.isspace() or any(char in name for char in unacceptedChars):
            raise InvalidImageNameException
        image = self.toPILImage()
        image.save("{}.tif".format(name))

    def splitChannels(self) -> typing.List[np.ndarray]:
        if self.isImageInGray():
            raise ImageDimensionsException(self.__dimensions)
        pixelsPerChannel = []
        for channel in range(self.getNumberOfChannel()):
            pixelsPerChannel.append(self.getArray()[..., channel])
        return pixelsPerChannel

    # Now, interesting part:
    def getGrayscaleConversion(self):
        # todo test unitaire
        if self.isImageInGray():
            grayConversion = self.getArray()
        else:
            grayConversion = color.rgb2gray(self.getArray())
        return DCCImage(grayConversion.astype("float32"))

    @staticmethod
    def __convertToUInt16Array(array: np.ndarray) -> np.ndarray:
        if not np.alltrue(np.mod(array, 1) == 0):
            warnings.warn("Conversion to 16-bits unsigned integers may cause loss of precision.")
        return array.astype(np.uint16)

    @staticmethod
    def __ravelArray(array: np.ndarray) -> np.ndarray:
        return array.ravel()

    def getGrayscaleHistogramValues(self, normed: bool = False) -> typing.Tuple[np.ndarray, np.ndarray]:
        array = self.getGrayscaleConversion().getArray()
        arrayUint = self.__convertToUInt16Array(array)
        arrayRaveled = self.__ravelArray(arrayUint)
        nbBins = len(np.bincount(arrayRaveled))
        hist, bins = np.histogram(arrayRaveled, nbBins, [0, nbBins], density=normed)
        return hist, bins

    def getRGBHistogramValues(self, normed: bool = False) -> typing.Tuple[
        typing.List[np.ndarray], typing.List[np.ndarray]]:
        histPerChannel = []
        binsPerChannel = []
        if self.getNumberOfChannel() != 3:
            raise ImageDimensionsException(self.__dimensions)
        array = self.getArray()
        arrayUint = self.__convertToUInt16Array(array)
        for channel in range(self.getNumberOfChannel()):
            arrayRaveled = self.__ravelArray(arrayUint[..., channel])
            nbBins = len(np.bincount(arrayRaveled))
            hist, bins = np.histogram(arrayRaveled, nbBins, [0, nbBins], density=normed)
            histPerChannel.append(hist)
            binsPerChannel.append(bins)
        return histPerChannel, binsPerChannel

    def displayGrayscaleHistogram(self, normed: bool = False) -> typing.Tuple[np.ndarray, np.ndarray]:
        histogram, bins = self.getGrayscaleHistogramValues(normed)
        plt.bar(bins[:-1], histogram, width=np.diff(bins), ec="k", align="edge", color="black", alpha=0.5)
        plt.show()
        return histogram, bins

    def displayRGBHistogram(self, normed: bool = False) -> typing.Tuple[
        typing.List[np.ndarray], typing.List[np.ndarray]]:
        allHistograms, allBins = self.getRGBHistogramValues(normed)
        colors = ["red", "green", "blue"]
        for element in zip(allHistograms, allBins, colors):
            bins = list(element)[1]
            histogram = list(element)[0]
            color = list(element)[2]
            plt.bar(bins[:-1], histogram, width=np.diff(bins), ec="k", align="edge", color=color, alpha=0.5)
        plt.show()
        return allHistograms, allBins

    def getConvolvedImage(self, matrix: typing.Union[np.ndarray, list]):
        convolvedArray = np.zeros_like(self.getArray())
        if self.isImageInGray():
            convolvedArray = convolve2d(self.getArray(), matrix, mode="same", boundary="symm")
        else:
            for channel in range(self.getNumberOfChannel()):
                convolvedArray[..., channel] = convolve2d(self.getArray()[..., channel], matrix, mode="same",
                                                          boundary="symm")
        return DCCImage(convolvedArray.astype(np.float32))

    def getXAxisDerivative(self):
        dxFilter = [[-1, 0, 1]]
        return self.getConvolvedImage(dxFilter)

    def getYAxisDerivative(self):
        dyFilter = [[-1], [0], [1]]
        return self.getConvolvedImage(dyFilter)

    def getAverageValueOfImage(self) -> typing.List[float]:
        averageList = []
        if self.isImageInGray():
            averageList.append(measurements.mean(self.getArray()))
        else:
            for channel in range(self.getNumberOfChannel()):
                averageList.append(measurements.mean(self.getArray()[..., channel]))
        return averageList

    def getStadardDeviationValueOfImage(self) -> typing.List[float]:
        stanDevList = []
        if self.isImageInGray():
            stanDevList.append(measurements.standard_deviation(self.getArray()))
        else:
            for channel in range(self.getNumberOfChannel()):
                stanDevList.append(measurements.standard_deviation(self.getArray()[..., channel]))
        return stanDevList

    def getShannonEntropyOfImage(self, base=2) -> float:
        grayscaleImage = self.getGrayscaleConversion().getArray()
        return measure.shannon_entropy(grayscaleImage, base)

    def getExtremaValuesOfPixels(self) -> typing.List[tuple]:
        extrema = []
        if self.isImageInGray():
            extrema.append((np.min(self.__pixelArray), np.max(self.__pixelArray)))
        else:
            for channel in range(self.getNumberOfChannel()):
                extrema.append((np.min(self.__pixelArray[..., channel]), np.max(self.__pixelArray[..., channel])))
        return extrema

    def getPixelsOfIntensityGrayImage(self, intensity: float) -> typing.List[tuple]:
        coordsList = []
        array = self.getGrayscaleConversion().getArray()
        coordsTemp = np.where(array[:, :] == intensity)
        coords = list(zip(coordsTemp[0], coordsTemp[1])) if len(coordsTemp[0]) != 0 else None
        coordsList.append(coords)
        coordsList = coordsList[0]
        return coordsList

    def getPixelsOfIntensityColorImageAllChannels(self, intensity: float) -> typing.List[typing.List[tuple]]:
        channels = self.getNumberOfChannel()
        array = self.getArray()
        coordsListPerChannel = []
        for channel in range(channels):
            coordsTemp = np.where(array[..., channel] == intensity)
            coords = list(zip(coordsTemp[0], coordsTemp[1])) if len(coordsTemp[0]) != 0 else None
            coordsListPerChannel.append(coords)
        return coordsListPerChannel

    def getPixelsOfIntensityColorImageOneChannel(self, intensity: float, channel: int) -> typing.List[tuple]:
        coordsList = []
        array = self.getArray()
        if channel >= self.getNumberOfChannel():
            raise ValueError("The specified channel must be in the interval [0, {}[".format(self.getNumberOfChannel()))
        coordsTemp = np.where(array[..., channel] == intensity)
        coords = list(zip(coordsTemp[0], coordsTemp[1])) if len(coordsTemp[0]) != 0 else None
        coordsList.append(coords)
        return coordsList[0]

    def getMinimumIntensityPixels(self) -> typing.Union[
        typing.List[typing.Tuple[int, int]], typing.List[typing.List[typing.Tuple[int, int]]]]:
        minimumsCoordsList = []
        if self.isImageInGray():
            minimum = self.getExtremaValuesOfPixels()[0][0]
            minimumsCoordsList = self.getPixelsOfIntensityGrayImage(minimum)
        else:
            for channel in range(self.getNumberOfChannel()):
                minimum = self.getExtremaValuesOfPixels()[channel][0]
                minimumsCoordsList.append(self.getPixelsOfIntensityColorImageOneChannel(minimum, channel))
        return minimumsCoordsList

    def getMaximumIntensityPixels(self) -> typing.Union[
        typing.List[typing.Tuple[int, int]], typing.List[typing.List[typing.Tuple[int, int]]]]:
        maximumsCoordsList = []
        if self.isImageInGray():
            maximum = self.getExtremaValuesOfPixels()[0][1]
            maximumsCoordsList = self.getPixelsOfIntensityGrayImage(maximum)
        else:
            for channel in range(self.getNumberOfChannel()):
                maximum = self.getExtremaValuesOfPixels()[channel][1]
                maximumsCoordsList.append(self.getPixelsOfIntensityColorImageOneChannel(maximum, channel))
        return maximumsCoordsList

    def getEntropyFiltering(self, filterSize: int):
        image = self.getGrayscaleConversion().getArray()
        # I have to cast as 16-bits unsigned integer because the entropy filter only works in uint8 or uint16
        image = self.__convertToUInt16Array(image)
        entropyFiltered = entropy(image, morphology.selem.square(filterSize, dtype=np.float32))
        return DCCImage(entropyFiltered.astype(np.float32))

    def getStandardDeviationFilteringSlow(self, filterSize: int):
        message = "This filtering method is very slow with big images. " \
                  "Use getStandardDeviationFiltering for faster results."
        warnings.warn(message)
        # VERY SLOW WITH BIG IMAGES
        image = self.getGrayscaleConversion().getArray()
        stdFiltered = filters.generic_filter(image, np.std, size=filterSize, mode="nearest").astype(np.float32)
        return DCCImage(stdFiltered)

    def getStandardDeviationFiltering(self, filterSize: int):
        image = self.getGrayscaleConversion().getArray()
        stdFilterPart1 = filters.uniform_filter(image, filterSize, mode="nearest")
        stdFilterPart2 = filters.uniform_filter(image * image, filterSize, mode="nearest")
        stdFiltered = np.sqrt(stdFilterPart2 - stdFilterPart1 * stdFilterPart1).astype(np.float32)
        if np.any(np.isnan(stdFiltered)):
            warnings.warn("Nan values encountered! Replacing them with 0.", category=RuntimeWarning)
            stdFiltered = np.nan_to_num(stdFiltered)
        return DCCImage(stdFiltered)

    def getGrayGaussianFiltering(self, sigma: float):
        image = self.getGrayscaleConversion().getArray()
        gaussianFiltered = gaussian(image, sigma, mode="nearest", multichannel=False, preserve_range=True)
        return DCCImage(gaussianFiltered.astype(np.float32))

    def getColorGaussianFiltering(self, sigma: float):
        image = self.getArray()
        gaussianFiltered = gaussian(image, sigma, mode="nearest", multichannel=True, preserve_range=True)
        return DCCImage(gaussianFiltered.astype(np.float32))

    def getHorizontalSobelFiltering(self):
        array = self.getGrayscaleConversion().getArray()
        sobelH = sobel_h(array)
        return DCCImage(sobelH.astype(np.float32))

    def getVerticalSobelFiltering(self):
        array = self.getGrayscaleConversion().getArray()
        sobelV = sobel_v(array)
        return DCCImage(sobelV.astype(np.float32))

    def getBothDirectionsSobelFiltering(self):
        array = self.getGrayscaleConversion().getArray()
        sobelHV = sobel(array)
        return DCCImage(sobelHV.astype(np.float32))

    def getIsodataThresholding(self):
        """
        Adapted from skimage's isodata thresholding method.
        Their version was not behaving properly with our image format (different than uint8).
        :return: The thresholded DCCImage instance according to isodata method.
        """
        # We ignore warnings related to division by 0 since they give nan and we treat nan later.
        warnings.catch_warnings()
        warnings.simplefilter("ignore", category=RuntimeWarning)
        inputArray = self.getGrayscaleConversion().getArray()
        hist, bins = self.getGrayscaleHistogramValues()

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
        threshArray = inputArray >= thresh
        return DCCImage(threshArray.astype(np.float32))

    def getOtsuThresholding(self):
        """
        Adapted from skimage's Otsu thresholding method.
        Their version was not behaving properly with our image format (different than uint8).
        :return: The thresholded DCCImage instance according to Otsu's method.
        """
        # We ignore warnings related to division by 0 since they give nan and we treat nan later.
        warnings.catch_warnings()
        warnings.simplefilter("ignore", category=RuntimeWarning)
        inputArray = self.getGrayscaleConversion().getArray()
        if np.max(inputArray) == np.min(inputArray):
            raise ValueError(
                "This method only works for image with more than one \"color\" (i.e. more than one pixel value).")
        hist, bins = self.getGrayscaleHistogramValues()
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
        threshArray = inputArray >= thresh
        return DCCImage(threshArray.astype(np.float32))

    def getAdaptiveThresholdingGaussian(self, blockSize: int = 3, sigma: float = None):
        inputArray = self.getArray()
        threshArray = inputArray >= threshold_local(inputArray, blockSize, mode="nearest", param=sigma)
        return DCCImage(threshArray.astype(np.float32))

    def getAdaptiveThresholdingMean(self, blockSize: int = 3):
        inputArray = self.getArray()
        threshArray = inputArray >= threshold_local(inputArray, blockSize, mode="nearest", method="mean")
        return DCCImage(threshArray.astype(np.float32))

    def getAdaptiveThresholdingMedian(self, blockSize: int = 3):
        warnings.warn("This thresholding method can be very slow.")
        inputArray = self.getArray()
        threshArray = inputArray >= threshold_local(inputArray, blockSize, mode="nearest", method="median")
        return DCCImage(threshArray.astype(np.float32))

    def getWatershedSegmentation(self):
        inputArray = self.getArray()
        distance = distance_transform_edt(inputArray)
        localMaxs = feature.peak_local_max(distance, indices=False, footprint=np.ones((3, 3)), labels=inputArray)
        markers = label(localMaxs)[0]
        labels = morphology.watershed(-distance, markers, mask=inputArray).astype(np.float32)
        return DCCImage(labels)

    def getOpening(self, windowSize: int = 3):
        inputArrayGray = self.getGrayscaleConversion().getArray()
        opened = morphology.opening(inputArrayGray, np.ones((windowSize, windowSize)))
        return DCCImage(opened)

    def getBinaryOpening(self, windowSize: int = 3):
        inputArray = self.getArray()
        if not self.isImageInBinary():
            raise NotBinaryImageException
        binaryOpened = morphology.binary_opening(inputArray, np.ones((windowSize, windowSize))).astype(np.float32)
        return DCCImage(binaryOpened)

    def getClosing(self, windowSize: int = 3):
        inputArrayGray = self.getGrayscaleConversion().getArray()
        closed = morphology.closing(inputArrayGray, np.ones((windowSize, windowSize)))
        return DCCImage(closed)

    def getBinaryClosing(self, windowSize: int = 3):
        inputArray = self.getArray()
        if not self.isImageInBinary():
            raise NotBinaryImageException
        binaryClosed = morphology.binary_closing(inputArray, np.ones((windowSize, windowSize))).astype(np.float32)
        return DCCImage(binaryClosed)

    def getConnectedComponents(self):
        inputArray = self.getArray()
        if not self.isImageInBinary():
            raise NotBinaryImageException
        labeled, nbObjects = label(inputArray)
        sizes = sum(inputArray, labeled, range(nbObjects + 1))
        return DCCImage(labeled.astype(np.float32)), nbObjects, sizes

    def isImageInBinary(self) -> bool:
        return np.alltrue(np.logical_or(self.getArray() == 0, self.getArray() == 1)) and self.isImageInGray()

    def isImageInGray(self) -> bool:
        return self.__dimensions == 2


if __name__ == '__main__':
    array = np.zeros((5, 5), dtype=np.float32)
    import DCCImagesFromFiles
    import DCCImageCollection

    cziImage = DCCImagesFromFiles.DCCImagesFromCZIFile(
        r"C:\Users\goubi\PycharmProjects\BigData-ImageAnalysis\ImageAnalysis\unitTesting\testCziFile2Images.czi")
    jpeg = DCCImagesFromFiles.DCCImageFromNormalFile(
        r"C:\Users\goubi\PycharmProjects\BigData-ImageAnalysis\ImageAnalysis\unitTesting\testNotCziFile.jpg")
    cziImage.showImagesOneByOne()
    cziImage.showImages()
    image = cziImage[0]
    i1 = image.getOtsuThresholding()
    i2 = image.getIsodataThresholding()
    print(image.getLength())
    import time

    # print(time.clock())
    # i3 = image.getAdaptiveThresholdingMedian(9)
    i4 = image.getOpening(14).getAdaptiveThresholdingMean(167)
    liste = [i1, i2, i4]
    coll = DCCImageCollection.DCCImageCollection(liste)
    # coll.showImages()
    image_open = np.ones((20, 20), dtype=np.float32)
    image_open[1][1] = 0
    windowSize = 3
    image_open[10: 10 + windowSize, 1:1 + windowSize] = 0
    image_open[3:3 + windowSize - 1, 6:6 + windowSize - 1] = 0
    image_open[15:15 + windowSize, 17:17 + windowSize - 1] = 0
    image_open[2:2 + windowSize, 15:15 + windowSize + 1] = 0
    print(image_open)
    image_open = DCCImage(image_open)
    print(image_open.getBinaryClosing(3))

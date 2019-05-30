try:
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
except ImportError:
    print("Please install the required libraries.")


class DCCImage:
    def __init__(self, imageAsArray: np.ndarray, metadata: str = None):
        if not imageAsArray.dtype == np.float32:
            raise PixelTypeException
        if not (1 < imageAsArray.ndim <= 3):
            raise ImageDimensionsException(imageAsArray.ndim)
        self.__pixelArray = imageAsArray
        self.__dimensions = imageAsArray.ndim
        self.__shape = imageAsArray.shape
        self.__metadata = metadata

    def __repr__(self):
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
            nbChannels = self.getArray().shape[-1]
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
            plt.imshow(self.__pixelArray, cmap="gray")
        else:
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

    def getMetadata(self) -> str:
        return self.__metadata

    def setMetadata(self, newMetadata: str) -> str:
        self.__metadata = newMetadata
        return newMetadata

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
            raise ImageDimensionsException(self.getArray().ndim)
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

    @staticmethod
    def __convolution2D(inputImage: np.ndarray, matrix: typing.Union[np.ndarray, list]) -> np.ndarray:
        convolvedImage = np.zeros_like(inputImage)
        if inputImage.ndim > 2:
            for channel in range(inputImage.shape[-1]):
                convolvedImage[..., channel] = convolve2d(inputImage[..., channel], matrix, mode="same",
                                                          boundary="symm")
        else:
            convolvedImage = convolve2d(inputImage, matrix, mode="same", boundary="symm")
        return convolvedImage.astype("float32")

    def getXAxisDerivative(self):
        dxFilter = [[-1, 0, 1]]
        dxImage = self.__convolution2D(self.getGrayscaleConversion().getArray(), dxFilter)
        return DCCImage(dxImage)

    def getYAxisDerivative(self):
        dyFilter = [[-1], [0], [1]]
        dyImage = self.__convolution2D(self.getGrayscaleConversion().getArray(), dyFilter)
        return DCCImage(dyImage)

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
        inputArray = self.__convertToUInt16Array(self.getArray())
        threshArray = inputArray >= threshold_isodata(inputArray)
        return DCCImage(threshArray.astype(np.float32))

    def getOtsuThresholding(self):
        inputArray = self.__convertToUInt16Array(self.getArray())
        threshArray = inputArray >= threshold_otsu(inputArray)
        return DCCImage(threshArray.astype(np.float32))

    def getAdaptiveThresholdingGaussian(self, blockSize: int = 3):
        inputArray = self.getArray()
        threshArray = threshold_local(inputArray, blockSize, mode="nearest")
        return DCCImage(threshArray.astype(np.float32))

    def getAdaptiveThresholdingMean(self, blockSize: int = 3):
        inputArray = self.getArray()
        threshArray = threshold_local(inputArray, blockSize, mode="nearest", method="mean")
        return DCCImage(threshArray.astype(np.float32))

    def getAdaptiveThresholdingMedian(self, blockSize: int = 3):
        inputArray = self.getArray()
        threshArray = threshold_local(inputArray, blockSize, mode="nearest", method="median")
        return DCCImage(threshArray.astype(np.float32))

    def getWatershedSegmentation(self):
        inputArray = self.getArray()
        distance = distance_transform_edt(inputArray)
        localMaxs = feature.peak_local_max(distance, indices=False, footprint=np.ones((3, 3)), labels=inputArray)
        markers = label(localMaxs)[0]
        labels = morphology.watershed(-distance, markers, mask=inputArray).astype(np.float32)
        return DCCImage(labels)

    def getClosing(self):
        inputArrayGray = self.getGrayscaleConversion().getArray()
        closed = morphology.closing(inputArrayGray)
        return DCCImage(closed)

    def getBinaryClosing(self):
        inputArray = self.getArray()
        if not self.isImageInBinary():
            raise NotBinaryImageException
        binaryClosed = morphology.binary_closing(inputArray).astype(np.float32)
        return DCCImage(binaryClosed)

    def getOpening(self):
        inputArrayGray = self.getGrayscaleConversion().getArray()
        opened = morphology.opening(inputArrayGray)
        return DCCImage(opened)

    def getBinaryOpening(self):
        inputArray = self.getArray()
        if not self.isImageInBinary():
            raise NotBinaryImageException
        binaryOpened = morphology.binary_opening(inputArray).astype(np.float32)
        return DCCImage(binaryOpened)

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
        return self.getArray().ndim == 2


if __name__ == '__main__':
    array = np.zeros((5, 5), dtype=np.float32)
    import DCCImagesFromFiles

    cziImage = DCCImagesFromFiles.DCCImagesFromCZIFile(
        r"C:\Users\goubi\PycharmProjects\BigData-ImageAnalysis\ImageAnalysis\unitTesting\testCziFile2Images.czi")
    jpeg = DCCImagesFromFiles.DCCImageFromNormalFile(
        r"C:\Users\goubi\PycharmProjects\BigData-ImageAnalysis\ImageAnalysis\unitTesting\testNotCziFile.jpg")
    cziImage = cziImage.getImageAtIndex(0)
    # hist, bins = cziImage.getGrayscaleHistogram()
    # cziImage.getStandardDeviationFiltering(3).showImage()
    # cziImage.showImage()
    for i in range(1, 4):
        for j in range(1, 4):
            array[i][j] = 1
    image = DCCImage(array)
    # cziImage.getWatershedSegmentation().showImage()
    cziImage.showImage()
    cziImage.getOpening().showImage()
    cziImage.getOtsuThresholding().showImage()
    stuff = cziImage.getGrayGaussianFiltering(1.5).getOtsuThresholding().getBinaryOpening().getConnectedComponents()
    stuff[0].showImage(False)
    #   cziImage.getOtsuThresholding().getWatershedSegmentation().showImage()
    #   cziImage.get().showImage()
    blobs = cziImage.getGrayGaussianFiltering(2.5).getOtsuThresholding().getBlobs()
    cziImage.showBlobs(blobs)

try:
    import numpy as np
    import typing
    from skimage import color, filters, measure, morphology
    from skimage.filters.rank import entropy
    import PIL.Image
    from scipy.signal import convolve2d
    from scipy.ndimage import measurements, filters
    from skimage.filters import gaussian
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

    def __eq__(self, other) -> bool:
        if not isinstance(other, DCCImage):
            raise InvalidEqualityTest(type(other))
        return np.array_equal(self.__pixelArray, other.getArray())

    def getArray(self) -> np.ndarray:
        return self.__pixelArray

    def getWidth(self) -> int:
        return int(self.__shape[0])

    def getLength(self) -> int:
        return int(self.__shape[1])

    def getNumberOfChannel(self) -> int:
        if self.__dimensions == 3:
            nbChannels = self.__shape[2]
        else:
            nbChannels = 1
        return int(nbChannels)

    def getNumberOfPixels(self) -> int:
        return self.getLength() * self.getWidth()

    def toPILImage(self) -> PIL.Image.Image:
        return PIL.Image.fromarray(self.__pixelArray)

    def copyDCCImage(self):
        copyArray = np.copy(self.__pixelArray)
        return DCCImage(copyArray)

    def showImage(self):
        plt.imshow(self.__pixelArray)
        plt.show()
        return self

    def saveToTIFF(self, name: str):
        unacceptedChars = ["?", "/", "\\", "*", "<", ">", "|", "."]
        name = name.strip()
        if len(name) == 0 or name.isspace() or any(char in name for char in unacceptedChars):
            raise InvalidImageName
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
        if self.getNumberOfChannel() == 1:
            grayConversion = self.getArray()
        else:
            # raises ValueError if not 3 or 4
            grayConversion = color.rgb2gray(self.getArray())
        return DCCImage(grayConversion.astype("float32"))

    @staticmethod
    def __convertToUInt16Array(array) -> np.ndarray:
        if not np.alltrue(np.mod(array, 1) == 0):
            warnings.warn("Conversion to 16-bits unsigned integers may cause loss of precision.")
        return array.astype(np.uint16)

    @staticmethod
    def __ravelArray(array) -> np.ndarray:
        return array.ravel()

    def getGrayscaleHistogramValues(self, normed=False) -> typing.Tuple[np.ndarray, np.ndarray]:
        array = self.getGrayscaleConversion().getArray()
        arrayUint = self.__convertToUInt16Array(array)
        arrayRaveled = self.__ravelArray(arrayUint)
        nbBins = len(np.bincount(arrayRaveled))
        hist, bins = np.histogram(arrayRaveled, nbBins, [0, nbBins], density=normed)
        return hist, bins

    def getRGBHistogramValues(self, normed=False) -> typing.Tuple[typing.List[np.ndarray], typing.List[np.ndarray]]:
        histPerChannel = []
        binsPerChannel = []
        colors = ["red", "green", "blue"]
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

    def displayGrayscaleHistogram(self, normed=False) -> typing.Tuple[np.ndarray, np.ndarray]:
        histogram, bins = self.getGrayscaleHistogramValues(normed)
        plt.bar(bins[:-1], histogram, width=np.diff(bins), ec="k", align="edge", color="black", alpha=0.5)
        plt.show()
        return histogram, bins

    def displayRGBHistogram(self, normed=False) -> typing.Tuple[typing.List[np.ndarray], typing.List[np.ndarray]]:
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
    def __convolution2D(inputImage: np.ndarray, matrix: typing.Union[np.ndarray, list]):
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
        if self.getNumberOfChannel() == 1:
            averageList.append(measurements.mean(self.getArray()))
        else:
            for channel in range(self.getNumberOfChannel()):
                averageList.append(measurements.mean(self.getArray()[..., channel]))
        return averageList

    def getStadardDeviationValueOfImage(self):
        stanDevList = []
        if self.getNumberOfChannel() == 1:
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
        if self.getNumberOfChannel() == 1:
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
        """
        Function that returns a list of tuples representing the (x, y) position of the minimum intensity pixels
        of the DCCImage. If the image is in grayscale, the returning list only contains the tuples, but if the image is
        in color, the returning list contains a list of tuples for each color channel.
        :return: List of tuples or a list of lists of tuples
        """
        minimumsCoordsList = []
        if self.getNumberOfChannel() == 1:
            minimum = self.getExtremaValuesOfPixels()[0][0]
            minimumsCoordsList = self.getPixelsOfIntensityGrayImage(minimum)
        else:
            for channel in range(self.getNumberOfChannel()):
                minimum = self.getExtremaValuesOfPixels()[channel][0]
                minimumsCoordsList.append(self.getPixelsOfIntensityColorImageOneChannel(minimum, channel))
        return minimumsCoordsList

    def getMaximumIntensityPixels(self) -> typing.Union[
        typing.List[typing.Tuple[int, int]], typing.List[typing.List[typing.Tuple[int, int]]]]:
        """
        Function that returns a list of tuples representing the (x, y) position of the maximum intensity pixels
        of the DCCImage. If the image is in grayscale, the returning list only contains the tuples, but if the image is
        in color, the returning list contains a list of tuples for each color channel.
        :return: List of tuples or a list of lists of tuples
        """
        maximumsCoordsList = []
        if self.getNumberOfChannel() == 1:
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
        image = image.astype(np.uint16)
        entropyFiltered = entropy(image, morphology.selem.square(filterSize, dtype=np.float32))
        return DCCImage(entropyFiltered.astype(np.float32))

    def getStandardDeviationFilteringSlow(self, filterSize: int):
        message = "This filtering method is very slow with big images. " \
                  "Use getStandardDeviationFiltering for faster results."
        warnings.warn(message)
        # VERY SLOW WITH BIG IMAGES
        image = self.getGrayscaleConversion().getArray()
        stdFiltered = filters.generic_filter(image, np.std, size=filterSize, mode="nearest")
        return DCCImage(stdFiltered.astype(np.float32))

    def getStandardDeviationFiltering(self, filterSize: int):
        image = self.getGrayscaleConversion().getArray()
        # We must add a small random number because otherwise some numbers become too small
        # and NaN appear throughout the resulting image.
        image += np.random.rand(image.shape[0], image.shape[1]) * 1e-6
        stdFilterPart1 = filters.uniform_filter(image, filterSize, mode="nearest")
        stdFilterPart2 = filters.uniform_filter(image * image, filterSize, mode="nearest")
        stdFiltered = np.sqrt(stdFilterPart2 - stdFilterPart1 * stdFilterPart1)
        return DCCImage(stdFiltered.astype(np.float32))

    def getGrayGaussianFiltering(self, sigma: float):
        image = self.getGrayscaleConversion().getArray()
        gaussianFiltered = gaussian(image, sigma, mode="nearest", multichannel=False, preserve_range=True)
        return DCCImage(gaussianFiltered.astype(np.float32))

    def getColorGaussianFiltering(self, sigma: float):
        image = self.getArray()
        gaussianFiltered = gaussian(image, sigma, mode="nearest", multichannel=True, preserve_range=True)
        return DCCImage(gaussianFiltered.astype(np.float32))


if __name__ == '__main__':
    array = np.ones((5, 5, 3), dtype=np.float32)
    import DCCImagesFromFiles

    cziImage = DCCImagesFromFiles.DCCImagesFromCZIFile(
        r"C:\Users\goubi\PycharmProjects\BigData-ImageAnalysis\ImageAnalysis\unitTesting\testCziFile2Images.czi")
    jpeg = DCCImagesFromFiles.DCCImageFromNormalFile(
        r"C:\Users\goubi\PycharmProjects\BigData-ImageAnalysis\ImageAnalysis\unitTesting\testNotCziFile.jpg")
    cziImage = cziImage.getImageAtIndex(0)
    # hist, bins = cziImage.getGrayscaleHistogram()
    jpeg.displayRGBHistogram(True)

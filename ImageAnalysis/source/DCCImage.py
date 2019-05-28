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
        return np.array_equal(self.__pixelArray, other.getDCCImageAsArray())

    def getDCCImageAsArray(self) -> np.ndarray:
        return self.__pixelArray

    def getDCCImageWidth(self) -> int:
        return int(self.__shape[0])

    def getDCCImageLength(self) -> int:
        return int(self.__shape[1])

    def getDCCImageNumberOfChannels(self) -> int:
        if self.__dimensions == 3:
            nbChannels = self.__shape[2]
        else:
            nbChannels = 1
        return int(nbChannels)

    def getNumberOfPixels(self) -> int:
        return self.getDCCImageLength() * self.getDCCImageWidth()

    def toPILImage(self) -> PIL.Image.Image:
        return PIL.Image.fromarray(self.__pixelArray)

    def copyDCCImage(self):
        copyArray = np.copy(self.__pixelArray)
        return DCCImage(copyArray)

    def showImage(self) -> None:
        plt.imshow(self.__pixelArray)
        plt.show()

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
    def grayscaleConversion(self):
        # todo test unitaire
        if self.getDCCImageNumberOfChannels() == 1:
            grayConversion = self.getDCCImageAsArray()
        else:
            # raises ValueError if not 3 or 4
            grayConversion = color.rgb2gray(self.getDCCImageAsArray())
        return DCCImage(grayConversion.astype("float32"))

    def grayscaleHistogram(self, normed=False):
        # todo faire en sorte d'avoir un histogramme et être capable de le normaliser + trouver le bon nombre de bins
        pass

    def RGBHistogram(self, normed=False):
        # todo faire en sorte d'avoir un histogramme et être capable de le normaliser + trouver le bon nombre de bins
        pass

    # Garder private ou mettre public?
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

    def DCCImageXAxisDerivative(self):
        dxFilter = [[-1, 0, 1]]
        dxImage = self.__convolution2D(self.grayscaleConversion().getDCCImageAsArray(), dxFilter)
        return DCCImage(dxImage)

    def DCCImageYAxisDerivative(self):
        dyFilter = [[-1], [0], [1]]
        dyImage = self.__convolution2D(self.grayscaleConversion().getDCCImageAsArray(), dyFilter)
        return DCCImage(dyImage)

    def DCCImageAverage(self) -> typing.List[float]:
        averageList = []
        if self.getDCCImageNumberOfChannels() == 1:
            averageList.append(measurements.mean(self.getDCCImageAsArray()))
        else:
            for channel in range(self.getDCCImageNumberOfChannels()):
                averageList.append(measurements.mean(self.getDCCImageAsArray()[..., channel]))
        return averageList

    def DCCImageStandardDeviation(self):
        stanDevList = []
        if self.getDCCImageNumberOfChannels() == 1:
            stanDevList.append(measurements.standard_deviation(self.getDCCImageAsArray()))
        else:
            for channel in range(self.getDCCImageNumberOfChannels()):
                stanDevList.append(measurements.standard_deviation(self.getDCCImageAsArray()[..., channel]))
        return stanDevList

    def DCCImageShannonEntropy(self, base=2) -> float:
        grayscaleImage = self.grayscaleConversion().getDCCImageAsArray()
        return measure.shannon_entropy(grayscaleImage, base)

    def __getDCCImageExtremaOfIntensity(self) -> typing.List[typing.Tuple[float]]:
        pass

    def minimumIntensityPixelsPositionPerChannel(self) -> typing.Union[
        typing.List[typing.Tuple[int, int]], typing.List[typing.List[typing.Tuple[int, int]]]]:
        """
        Function that returns a list of tuples representing the (x, y) position of the minimum intensity pixels
        of the DCCImage. If the image is in grayscale, the returning list only contains the tuples, but if the image is
        in color, the returning list contains a list of tuples for each color channel.
        :return: List of tuples or a list of lists of tuples
        """
        minimumsCoordsList = []
        image = self.getDCCImageAsArray()
        if image.ndim == 2:
            minimum = np.min(image)
            minimumCoordTemp = np.where(image[:, :] == minimum)
            minimumCoord = list(zip(minimumCoordTemp[0], minimumCoordTemp[1]))
            minimumsCoordsList.append(minimumCoord)
            minimumsCoordsList = minimumsCoordsList[0]
        else:
            for channel in range(image.shape[-1]):
                minimum = np.min(image[..., channel])
                minimumCoordTemp = np.where(image[..., channel] == minimum)
                minimumCoord = list(zip(minimumCoordTemp[0], minimumCoordTemp[1]))
                minimumsCoordsList.append(minimumCoord)
        return minimumsCoordsList

    def maximumIntensityPixelsPositionPerChannel(self) -> typing.Union[
        typing.List[typing.Tuple[int, int]], typing.List[typing.List[typing.Tuple[int, int]]]]:
        """
        Function that returns a list of tuples representing the (x, y) position of the maximum intensity pixels
        of the DCCImage. If the image is in grayscale, the returning list only contains the tuples, but if the image is
        in color, the returning list contains a list of tuples for each color channel.
        :return: List of tuples or a list of lists of tuples
        """
        maximumsCoordsList = []
        image = self.getDCCImageAsArray()
        if image.ndim == 2:
            maximum = np.max(image)
            maximumCoordTemp = np.where(image[:, :] == maximum)
            maximumCoord = list(zip(maximumCoordTemp[0], maximumCoordTemp[1]))
            maximumsCoordsList.append(maximumCoord)
            maximumsCoordsList = maximumsCoordsList[0]
        else:
            for channel in range(image.shape[-1]):
                maximum = np.max(image[..., channel])
                maximumCoordTemp = np.where(image[..., channel] == maximum)
                maximumCoord = list(zip(maximumCoordTemp[0], maximumCoordTemp[1]))
                maximumsCoordsList.append(maximumCoord)
        return maximumsCoordsList

    def DCCImageWithEntropyFilter(self, filterSize: int):
        image = self.grayscaleConversion().getDCCImageAsArray()
        # I have to cast as 16-bits unsigned integer because the entropy filter only works in uint8 or uint16
        image = image.astype(np.uint16)
        entropyFiltered = entropy(image, morphology.selem.square(filterSize, dtype=np.float32))
        return DCCImage(entropyFiltered.astype(np.float32))

    def DCCImageWithStandardDeviationFilter_MK1(self, filterSize: int):
        # VERY SLOW WITH BIG IMAGES
        image = self.grayscaleConversion().getDCCImageAsArray()
        stdFiltered = filters.generic_filter(image, np.std, size=filterSize, mode="nearest")
        return DCCImage(stdFiltered.astype(np.float32))

    def DCCImageWithStandardDeviationFilter_MK2(self, filterSize: int):
        image = self.grayscaleConversion().getDCCImageAsArray()
        # We must add a small random number because otherwise some numbers become too small
        # and NaN appear throughout the resulting image.
        image += np.random.rand(image.shape[0], image.shape[1]) * 1e-6
        stdFilterPart1 = filters.uniform_filter(image, filterSize, mode="nearest")
        stdFilterPart2 = filters.uniform_filter(image * image, filterSize, mode="nearest")
        stdFiltered = np.sqrt(stdFilterPart2 - stdFilterPart1 * stdFilterPart1)
        return DCCImage(stdFiltered.astype(np.float32))

    def DCCImageWithGaussianFilterGray(self, sigma: float):
        image = self.grayscaleConversion().getDCCImageAsArray()
        gaussianFiltered = gaussian(image, sigma, mode="nearest", multichannel=False, preserve_range=True)
        return DCCImage(gaussianFiltered.astype(np.float32))

    def DCCImageWithGaussianFilterColors(self, sigma: float):
        image = self.getDCCImageAsArray()
        gaussianFiltered = gaussian(image, sigma, mode="nearest", multichannel=True, preserve_range=True)
        return DCCImage(gaussianFiltered.astype(np.float32))



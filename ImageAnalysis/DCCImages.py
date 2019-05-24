import numpy as np
import tifffile
import typing
from skimage import color, data, filters, img_as_float32, measure, morphology
import ImageAnalysis.cziUtil as cziUtil
import PIL.Image
from scipy.signal import convolve2d
from scipy.ndimage import filters, measurements
from ImageAnalysis.DCCImagesExceptions import *
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

    # Voir si pertinent de décomposer convolution2D en deux méthodes
    """
    @staticmethod
    def __convolution2DGray(inputGray: np.ndarray, matrix: np.ndarray):
        if not inputGray.ndim == 2:
            raise ImageDimensionsException(inputGray.ndim)
        return convolve2d(inputGray, matrix, mode="same", boundary="symm").astype(np.float32)

    @staticmethod
    def __convolution2DColors(inputColors: np.ndarray, matrix: np.ndarray):
        if inputColors.ndim == 2:
            raise ImageDimensionsException(inputColors.ndim)
        convolvedColoredImage = np.zeros_like(inputColors)
        for channel in range(inputColors.shape[-1]):
            convolvedColoredImage[..., channel] = convolve2d(inputColors[..., channel], matrix, mode="same",
                                                             boundary="symm")
        return convolvedColoredImage.astype(np.float32)
        """

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

    def maximumIntensityPixelsPositions(self) -> typing.Union[typing.List[tuple], typing.List[typing.List[tuple]]]:
        """
        Function that returns a list of tuples representing the (x, y) position of the maximum intensity pixels
        of the DCCImage. If the image is in grayscale, the returning list only contains the tuples, but if the image is
        in color, the returning list contains a list of tuples for each color channel.
        :return: List of tuples or a list of lists of tuples
        """
        maximumsCoordsList = []
        image = self.getDCCImageAsArray()
        if image.ndim == 2:
            maximum = np.min(image)
            maximumCoordTemp = np.where(image[:, :] == maximum)
            maximumCoord = list(zip(maximumCoordTemp[0], maximumCoordTemp[1]))
            maximumsCoordsList.append(maximumCoord)
            maximumsCoordsList = maximumsCoordsList[0]
        else:
            for channel in range(image.shape[-1]):
                maximum = np.min(image[..., channel])
                maximumCoordTemp = np.where(image[..., channel] == maximum)
                maximumCoord = list(zip(maximumCoordTemp[0], maximumCoordTemp[1]))
                maximumsCoordsList.append(maximumCoord)
        return maximumsCoordsList

    def DCCImageWithEntropyFilter(self, filterSize: int):
        image = self.grayscaleConversion().getDCCImageAsArray()
        entropyFiltered = filters.rank.entropy(image, morphology.selem.square(filterSize, dtype=np.float32))
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
        stdFilterPart2 = filters.uniform_filter(np.float_power(image, 2), filterSize, mode="nearest")
        stdFiltered = np.sqrt(stdFilterPart2, np.float_power(stdFilterPart1, 2))
        return DCCImage(stdFiltered.astype(np.float32))

    def DCCImageWithGaussianFilterGray(self, sigma: float):
        image = self.grayscaleConversion().getDCCImageAsArray()
        gaussianFiltered = filters.gaussian(image, sigma, mode="nearest", multichannel=False, preserve_range=True)
        return DCCImage(gaussianFiltered.astype(np.float32))

    def DCCImageWithGaussianFilterColors(self, sigma: float):
        image = self.getDCCImageAsArray()
        gaussianFiltered = filters.gaussian(image, sigma, mode="nearest", multichannel=True, preserve_range=True)
        return DCCImage(gaussianFiltered.astype(np.float32))


class DCCImageStack:
    def __init__(self, DCCImageArray: typing.List[DCCImage]):
        if not all(isinstance(image, DCCImage) for image in DCCImageArray):
            raise NotDCCImageException
        self.__imageStack = DCCImageArray
        self.__numberOfImages = len(DCCImageArray)

    def __knowIfImageInStackAndPosition(self, image: DCCImage) -> tuple:
        if not isinstance(image, DCCImage):
            raise NotDCCImageException
        isFound = False
        index = -1
        while index < self.__numberOfImages - 1 and not isFound:
            index += 1
            isFound = self.__imageStack[index] == image
        return isFound, index

    def isImageInStack(self, image: DCCImage) -> bool:
        return self.__knowIfImageInStackAndPosition(image)[0]

    def getIndexOfImage(self, image: DCCImage) -> int:
        isInStack = self.isImageInStack(image)
        index = self.__knowIfImageInStackAndPosition(image)[-1]
        if not isInStack:
            raise ImageNotInStackException
        return index

    def addDCCImage(self, image: DCCImage) -> int:
        if self.isImageInStack(image):
            raise ImageAlreadyInStackException
        self.__imageStack.append(image)
        self.__numberOfImages += 1
        return self.__numberOfImages - 1

    def removeAtIndex(self, index: int) -> DCCImage:
        removedImage = self.__imageStack.pop(index)
        self.__numberOfImages -= 1
        return removedImage

    def removeDCCImage(self, image: DCCImage) -> int:
        imageIndex = self.getIndexOfImage(image)
        del self.__imageStack[imageIndex]
        self.__numberOfImages -= 1
        return imageIndex

    def getNumberOfImages(self) -> int:
        return self.__numberOfImages

    def __len__(self) -> int:
        return self.getNumberOfImages()

    def asNumpyArray(self) -> np.ndarray:
        return np.array(self.__imageStack)

    def asList(self) -> list:
        return self.__imageStack

    def getImageAtIndex(self, index: int) -> DCCImage:
        return self.__imageStack[index]

    def clearAll(self) -> None:
        self.__imageStack.clear()
        self.__numberOfImages = 0
        print(self.__imageStack)

    def showImages(self) -> int:
        imagesShown = 0
        for image in self.__imageStack:
            image.showImage()
            imagesShown += 1
        return imagesShown


class DCCImagesFromCZIFile(DCCImageStack):

    def __init__(self, path: str):
        self.__path = path
        cziObject = cziUtil.readCziImage(path)
        arrayOfImages = cziUtil.getImagesFromCziFileObject(cziObject).astype(np.float32)
        listOfImages = []
        self.__metadata = cziUtil.extractMetadataFromCziFileObject(cziObject)
        cziUtil.closeCziFileObject(cziObject)
        for image in arrayOfImages:
            listOfImages.append(
                DCCImage(image, metadata=self.__metadata))  # Voir si pertinent que DCCImage ait un attribut metadata
        DCCImageStack.__init__(self, listOfImages)

    def getMetadata(self) -> str:
        return self.__metadata

    def setMetadata(self, newMetadata: str) -> None:
        if not isinstance(newMetadata, str):
            raise TypeError("Metadata must be a string object")
        self.__metadata = newMetadata
        for image in self.asList():
            image.setMetadata(self.__metadata)

    def saveMetadata(self, filename: str) -> None:
        unacceptedChars = ["?", "/", "\\", "*", "<", ">", "|", ".", ","]
        filename = filename.strip()
        if len(filename) == 0 or filename.isspace() or any(char in filename for char in unacceptedChars):
            raise InvalidMetadataFileName
        with open("{}.xml".format(filename), "w", encoding="utf-8") as file:
            file.write(self.__metadata)

    def getPath(self) -> str:
        return self.__path


class DCCImageFromNormalFile(DCCImage):
    def __init__(self, path: str):
        self.__path = path
        if path.lower().__contains__(".tiff") or path.lower().__contains__(".tif"):
            raise InvalidFileFormat("To read tiff files, please use DCCImagesFromTiffFile.")
        elif path.lower().__contains__(".czi"):
            raise InvalidFileFormat("To read czi files, please use DCCImagesFromCZIFile.")
        image = PIL.Image.open(path)
        imageToArray = np.array(image, dtype=np.float32)
        DCCImage.__init__(self, imageToArray)

    def getPath(self) -> str:
        return self.__path


class DCCImagesFromTiffFile(DCCImageStack):
    def __init__(self, path: str):
        self.__path = path
        if not (path.lower().__contains__(".tiff") or path.lower().__contains__(".tif")):
            raise InvalidFileFormat("Please use the right class to extract the image(s) form the file.")
        tiffFileObject = tifffile.TiffFile(path)
        imageAsArray = tiffFileObject.asarray().astype(dtype="float32")
        self.__metadata = tiffFileObject.ome_metadata
        imageList = []
        for i in range(imageAsArray.shape[0]):
            imageList.append(DCCImage(imageAsArray[i], metadata=self.__metadata))
        DCCImageStack.__init__(self, imageList)

    def getMetadata(self) -> str:
        return self.__metadata

    def setMetadata(self, newMetadata: str) -> None:
        if not isinstance(newMetadata, str):
            raise TypeError("Metadata must be a string object")
        self.__metadata = newMetadata

    def saveMetadata(self, filename: str) -> None:
        unacceptedChars = ["?", "/", "\\", "*", "<", ">", "|", ".", ","]
        filename = filename.strip()
        if len(filename) == 0 or filename.isspace() or any(char in filename for char in unacceptedChars):
            raise InvalidMetadataFileName
        with open("{}.xml".format(filename), "w") as file:
            file.write(self.__metadata)

    def getPath(self) -> str:
        return self.__path


if __name__ == '__main__':
    path = "C:\\Users\\goubi\\PycharmProjects\\BigData-ImageAnalysis\\ImageAnalysis\\unitTesting\\testCziFile2Images.czi"
    path2 = "C:\\Users\\goubi\\PycharmProjects\\BigData-ImageAnalysis\\ImageAnalysis\\unitTesting\\testNotCziFile.jpg"
    array = np.ones((10, 10), dtype=np.float32)
    array[0][7] = 12
    image = DCCImage(array)
    positionsMin = image.minimumIntensityPixelsPositionPerChannel()
    print(positionsMin)

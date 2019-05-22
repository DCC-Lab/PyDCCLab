import numpy as np
import typing
from skimage import color
import ImageAnalysis.cziUtil as cziUtil
import cv2
import PIL.Image
from ImageAnalysis.DCCImagesExceptions import ImageNotInStackException, ImageAlreadyInStackException, \
    ImageDimensionsException, PixelTypeException, InvalidEqualityTest, NotDCCImageException


class DCCImage:
    def __init__(self, imageAsArray: np.ndarray):
        if not (1 < imageAsArray.ndim <= 3):
            raise ImageDimensionsException(imageAsArray.ndim)
        if not imageAsArray.dtype == np.float32:
            raise PixelTypeException
        self.__pixelArray = imageAsArray
        self.__dimensions = imageAsArray.ndim
        self.__shape = imageAsArray.shape

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

    def copyDCCImage(self):  # -> DCCImage:
        copyArray = np.copy(self.__pixelArray)
        return DCCImage(copyArray)


class DCCImageStack:
    def __init__(self, DCCImageArray: typing.List[DCCImage]):
        if not all(isinstance(image, DCCImage) for image in DCCImageArray):
            raise NotDCCImageException
        self.__imageStack = DCCImageArray
        self.__numberOfImages = len(DCCImageArray)


    #Voir si ça ne serait pas mieux de juste avoir le lancement de l'exception dans isImageIn
    def isImageInStack(self, image: DCCImage):
        if not isinstance(image, DCCImage):
            raise NotDCCImageException
        isFound = False
        index = 0
        while index < self.__numberOfImages and not isFound:
            isFound = self.__imageStack[index] == image
            index += 1
        return index

    def addDCCImage(self, image: DCCImage):
        if not isinstance(image, DCCImage):
            raise NotDCCImageException
        if self.isImageInStack(image) >= self.__numberOfImages:
            raise ImageAlreadyInStackException
        self.__imageStack.append(image)
        self.__numberOfImages += 1

    def removeAtIndex(self, index: int):
        removedImage = self.__imageStack.pop(index)
        self.__numberOfImages -= 1
        return removedImage

    def removeDCCImage(self, image: DCCImage):
        imageIndex = self.isImageInStack(image)
        if imageIndex >= self.__numberOfImages:
            raise ImageNotInStackException
        del self.__imageStack[imageIndex]
        self.__numberOfImages -= 1
        return imageIndex

    def asNumpyArray(self):
        return np.array(self.__imageStack)

    def getNumberOfImages(self):
        return self.__numberOfImages

    def __del__(self):
        for image in self.__imageStack:
            del image


if __name__ == '__main__':
    imageList = []
    for i in range(5):
        array = np.ones((1250, 1251), dtype=np.float32)
        array[i][i] = i
        image = DCCImage(array)
        imageList.append(image)
    stack = DCCImageStack(imageList)
    image = DCCImage(np.zeros((10, 10), dtype=np.float32))
    stack.isImageInStack(image)

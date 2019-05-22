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
        if not imageAsArray.dtype == np.float32:
            raise PixelTypeException
        if not (1 < imageAsArray.ndim <= 3):
            raise ImageDimensionsException(imageAsArray.ndim)
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

    def __knowIfImageInStackAndPosition(self, image):
        if not isinstance(image, DCCImage):
            raise NotDCCImageException
        isFound = False
        index = -1
        while index < self.__numberOfImages - 1 and not isFound:
            index += 1
            isFound = self.__imageStack[index] == image
        return isFound, index

    def isImageInStack(self, image: DCCImage):
        return self.__knowIfImageInStackAndPosition(image)[0]

    def getIndexOfImage(self, image: DCCImage):
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

    def removeAtIndex(self, index: int):
        removedImage = self.__imageStack.pop(index)
        self.__numberOfImages -= 1
        return removedImage

    def removeDCCImage(self, image: DCCImage):
        imageIndex = self.getIndexOfImage(image)
        del self.__imageStack[imageIndex]
        self.__numberOfImages -= 1
        return imageIndex

    def getNumberOfImages(self):
        return self.__numberOfImages

    def __len__(self):
        return self.getNumberOfImages()

    def asNumpyArray(self):
        return np.array(self.__imageStack)

    def asList(self):
        return self.__imageStack

    def getImageAtIndex(self, index: int):
        return self.__imageStack[index]

    def clearAll(self):
        self.__imageStack.clear()
        self.__numberOfImages = 0
        print(self.__imageStack)



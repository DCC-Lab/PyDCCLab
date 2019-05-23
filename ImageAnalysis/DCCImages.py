import numpy as np
import typing
import typing
from skimage import color
import ImageAnalysis.cziUtil as cziUtil
import cv2
import PIL.Image
from ImageAnalysis.DCCImagesExceptions import ImageNotInStackException, ImageAlreadyInStackException, \
    ImageDimensionsException, PixelTypeException, InvalidEqualityTest, NotDCCImageException, InvalidImageName
import matplotlib.pyplot as plt


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

    def copyDCCImage(self):
        copyArray = np.copy(self.__pixelArray)
        return DCCImage(copyArray)

    def showImage(self):
        plt.imshow(self.__pixelArray)
        plt.show()

    def saveToTIFF(self, name: str):
        unacceptedChars = ["?", "/", "\\", "*", "<", ">", "|", "."]
        name = name.strip()
        if len(name) == 0 or name.isspace() or any(char in name for char in unacceptedChars):
            raise InvalidImageName
        image = self.toPILImage()
        image.save("{}.tif".format(name))


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

    def showImages(self):
        for image in self.__imageStack:
            image.showImage()


class DCCImagesFromCZIFile(DCCImageStack):

    def __init__(self, path):
        cziObject = cziUtil.readCziImage(path)
        arrayOfImages = cziUtil.getImagesFromCziFileObject(cziObject).astype(np.float32)
        listOfImages = []
        self.__metadata = cziUtil.extractMetadataFromCziFileObject(cziObject)
        cziUtil.closeCziFileObject(cziObject)
        for image in arrayOfImages:
            listOfImages.append(DCCImage(image))
        DCCImageStack.__init__(self, listOfImages)

    def getMetadata(self):
        return self.__metadata

    def setMetadata(self, newMetadata):
        self.__metadata = newMetadata


class DCCImageFromNormalFile(DCCImage):
    def __init__(self, path):
        image = PIL.Image.open(path)
        imageToArray = np.array(image, dtype=np.float32)
        DCCImage.__init__(self, imageToArray)


if __name__ == '__main__':
    path = "C:\\Users\\goubi\\PycharmProjects\\BigData-ImageAnalysis\\ImageAnalysis\\unitTesting\\testCziFile2Images.czi"
    path2 = "C:\\Users\\goubi\\PycharmProjects\\BigData-ImageAnalysis\\ImageAnalysis\\unitTesting\\testNotCziFile.jpg"
    cziImages = DCCImagesFromCZIFile(path)
    cziImages.showImages()

from DCCImage import DCCImage
from DCCExceptions import *
import numpy as np
import matplotlib.pyplot as plt
import typing


class DCCImageCollection:
    def __init__(self, DCCImageArray: typing.List[DCCImage] = None):
        if DCCImageArray is not None:
            if not all(isinstance(image, DCCImage) for image in DCCImageArray):
                raise NotDCCImageException
            self.__imageCollection = DCCImageArray
        else:
            self.__imageCollection = []
        self.__numberOfImages = len(DCCImageArray)

    def __getitem__(self, item):
        return self.getImageAtIndex(item)

    def __knowIfImageInListAndPosition(self, image: DCCImage) -> tuple:
        if not isinstance(image, DCCImage):
            raise NotDCCImageException
        isFound = False
        index = -1
        while index < self.__numberOfImages - 1 and not isFound:
            index += 1
            isFound = self.__imageCollection[index] == image
        return isFound, index

    def isImageInCollection(self, image: DCCImage) -> bool:
        return self.__knowIfImageInListAndPosition(image)[0]

    def getIndexOfImage(self, image: DCCImage) -> int:
        isInCollection = self.isImageInCollection(image)
        index = self.__knowIfImageInListAndPosition(image)[-1]
        if not isInCollection:
            raise ImageNotInCollectionException
        return index

    def addDCCImage(self, image: DCCImage) -> int:
        if self.isImageInCollection(image):
            raise ImageAlreadyInCollectionException
        self.__imageCollection.append(image)
        self.__numberOfImages += 1
        return self.__numberOfImages - 1

    def removeAtIndex(self, index: int) -> DCCImage:
        removedImage = self.__imageCollection.pop(index)
        self.__numberOfImages -= 1
        return removedImage

    def removeDCCImage(self, image: DCCImage) -> int:
        imageIndex = self.getIndexOfImage(image)
        del self.__imageCollection[imageIndex]
        self.__numberOfImages -= 1
        return imageIndex

    def getNumberOfImages(self) -> int:
        return self.__numberOfImages

    def __len__(self) -> int:
        return self.getNumberOfImages()

    def asNumpyArray(self) -> np.ndarray:
        return np.array(self.__imageCollection)

    def asList(self) -> list:
        return self.__imageCollection

    def getImageAtIndex(self, index: int) -> DCCImage:
        return self.__imageCollection[index]

    def clearAll(self) -> None:
        self.__imageCollection.clear()
        self.__numberOfImages = 0
        print(self.__imageCollection)

    def showImagesOneByOne(self, showInGray: object = True) -> object:
        imagesShown = 0
        for image in self.__imageCollection:
            image.showImage(showInGray)
            imagesShown += 1
        return imagesShown

    def showImages(self, showInGray: bool = True) -> int:
        colorMap = "gray" if showInGray else None
        nbOfImages = self.__numberOfImages
        if nbOfImages == 0:
            raise EmptyDCCImageCollectionException
        imagesShown = 0
        fig = plt.figure()
        for i in range(nbOfImages):
            plt.subplot((nbOfImages // 3) + 1, nbOfImages if nbOfImages // 3 == 0 else 3, i + 1)
            plt.imshow(self.__imageCollection[i].getArray(), cmap=colorMap)
            imagesShown += 1
        plt.show()
        return imagesShown

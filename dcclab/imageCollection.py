from .image import Image
import numpy as np
import matplotlib.pyplot as plt
import typing

class ImageCollection:
    def __init__(self, images: typing.List[Image] = None, pathList = None):
        if images is not None:
            if not all(isinstance(image, Image) for image in images):
                raise NotDCCImageException
            self.__images = images
        elif pathList is not None:
            raise NotImplemented("pathList not implemented yet")
        else:
            self.__images = []

    @property
    def images(self):
        return self.__images
    
    def __getitem__(self, index):
        return self.images[index]

    def __len__(self) -> int:
        return len(self.images)

    @property
    def numberOfImages(self):
        return len(self.images)

    def indexOf(self, image) -> int:
        if not isinstance(image, Image):
            raise NotDCCImageException

        for (i, imageInList) in enumerate(self.images):
            if image == imageInList:
                return i

        return None

    def contains(self, image) -> bool:
        return self.indexOf(image) is not None

    def append(self, image: Image):
        if self.contains(image):
            raise ImageAlreadyInCollectionException
        self.images.append(image)

    def removeAt(self, index: int):
        self.images.pop(index)

    def remove(self, image: Image):
        index = self.indexOf(image)
        del self.images[index]

    def asNumpyArray(self) -> np.ndarray:
        return np.array(self.images)

    def showAllSequentially(self, showInGray: object = True):
        for image in self.images:
            image.display()

    def showAllOnGrid(self, showInGray: bool = True) -> int:
        colorMap = "gray" if showInGray else None
        imagesShown = 0
        fig = plt.figure()
        nbOfImages = len(self.images)
        for i in range(nbOfImages):
            rows = (nbOfImages // 3) + 1
            cols = nbOfImages if nbOfImages // 3 == 0 else 3
            plt.subplot(rows, cols, i + 1)
            plt.imshow(self.images[i].asArray(), cmap=colorMap)
        plt.show()
        return imagesShown

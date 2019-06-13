from .image import *
import numpy as np
import matplotlib.pyplot as plt
import typing
from .lifReader import LifReader


class ImageCollection:
    def __init__(self, images: typing.List[Image] = None, pathPattern:str=None):
        self.__images = []
        if images is not None:
            if not all(isinstance(image, Image) for image in images):
                raise NotDCCImageException
            self.__images = images
        elif pathPattern is not None:
            self.appendMatchingFiles(pathPattern)

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

    def appendMatchingFiles(self, pathPattern):
        directory = os.path.dirname(pathPattern)
        basePattern = os.path.basename(pathPattern)
        paths = [os.path.join(directory,f) for f in os.listdir(directory) if re.match(basePattern, f)]
        paths.sort()
        for path in paths:
            try:
                image = Image(path)
                self.__images.append(image)
            except:
                pass

    def removeAt(self, index: int):
        self.images.pop(index)

    def remove(self, image: Image):
        index = self.indexOf(image)
        del self.images[index]

    def asArray(self) -> np.ndarray:
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


class ZStack(ImageCollection):
    def __init__(self, images: typing.List[Image] = None, pathPattern: str=None):
        ImageCollection.__init__(images, pathPattern)
        if not self.imagesAreSimilar:
            raise ValueError("Images in z-stack are not all the same shape")

    def imagesAreSimilar(self) -> bool:
        shape = None
        for image in self.images:
            if shape is None:
                shape = image.shape
            elif shape != image.shape:
                return False
        return True

    def show(self):
        # TODO: Do something nicer with z-stack
        self.showAllSequentially()


class LIFFile:
    def __init__(self, path: str):
        self.path = path
        lifObject = LifReader(self.path)
        self.__series = lifObject.getSeries()

    @property
    def series(self):
        return self.__series

    def __getitem__(self, indices: list or int):
        if indices is None:
            return self.__series
        elif type(indices) is not list:
            indices = [indices]
        if max(indices) < len(self.__series):
            raise IndexError

        items = [self.__series[i] for i in indices]

        return items[0] if len(items) == 1 else items

    def keepSeries(self, indices: list or int):
        self.__series = self[indices]

    def removeAt(self, index: int):
        self.__series.pop(index)

    def getZStacks(self, seriesIndices=None, channels=None):
        series = self[seriesIndices]

        stacks = []
        for serie in series:
            # TODO: create ZStackCollection Object with array
            stacks.append(serie.getStack(channels))  # numpy array

        return stacks

    def getMetadata(self, serieIndex: int=0):
        return self.__series[serieIndex].getMetadata()

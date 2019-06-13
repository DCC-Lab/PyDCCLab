from .image import *
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Union
from .__lifReader import LifReader


class ImageCollection:
    def __init__(self, images: Union[List[Image], np.ndarray]=None, pathPattern: str=None):
        self.__images = []
        if images is not None:
            if type(images) is np.ndarray:
                self.collectionFromArray(images)
            elif not all(isinstance(image, Image) for image in images):
                raise NotDCCImageException
            else:
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
                image = Image(path=path)
                self.__images.append(image)
            except:
                pass

    def collectionFromArray(self, array):
        if array.ndim < 3:
            raise EmptyDCCImageCollectionException  # fixme: better exception or redirect for error "image collection from single image"...

        elif array.ndim == 3:
            self.__images = [Image(array[:, :, i]) for i in range(array.shape[2])]

        elif array.ndim > 3:  # Todo
            raise NotImplementedError("ImageCollection from single channel 3D array only.")

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
    def __init__(self, images: Union[List[Image], np.ndarray]=None, pathPattern: str=None):
        super().__init__(images, pathPattern)
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

    @property
    def numberOfSeries(self):
        return len(self.__series)

    def __len__(self):
        return self.numberOfSeries

    def __getitem__(self, indices: Union[int, tuple, list, slice]=None):
        if indices is None:
            return self.__series
        if type(indices) is slice:
            return self.__series[indices]
        elif type(indices) is int:
            return self.__series[indices]
        elif type(indices) is tuple:
            indices = list(indices)

        if type(indices) is list:
            return [self.__series[i] for i in indices]

    def keepSeries(self, indices):
        self.__series = self[indices]

    def removeAt(self, index: int):
        self.__series.pop(index)

    def getMetadata(self, serieIndex: int=None):
        if serieIndex is None:
            metadata = []
            for serie in self.__series:
                metadata.append(serie.getMetadata())
        else:
            metadata = self.__series[serieIndex].getMetadata()

        return metadata

    def getZStacks(self, seriesIndices=None, channels=None):
        if type(seriesIndices) is int:
            seriesIndices = [seriesIndices]

        series = self[seriesIndices]

        stacks = []
        for serie in series:
            # TODO: create ZStackCollection Object with array
            stacks.append(serie.getStack(channels))  # numpy array

        return stacks

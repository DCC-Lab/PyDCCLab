from .image import *
import numpy as np
import json
import matplotlib.pyplot as plt
from typing import List, Union
from .__lifReader import LifReader
from scipy import ndimage


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

    @property
    def array(self) -> np.ndarray:
        return np.array(self.images)

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
    def __init__(self, images: Union[List[Image], np.ndarray]=None, pathPattern: str=None, keepOriginal: bool=True):
        super().__init__(images, pathPattern)
        if not self.imagesAreSimilar:
            raise ValueError("Images in z-stack are not all the same shape")

        self.__array = None
        if type(images) is np.ndarray:
            self.__array = images

        self.__keepOriginal = keepOriginal
        self.__masked = False
        self.__labeled = False
        self.originalZStack = None
        self.maskedZStack = None
        self.labeledZStack = None
        self.params = {}

    def imagesAreSimilar(self) -> bool:
        shape = None
        for image in self.images:
            if shape is None:
                shape = image.shape
            elif shape != image.shape:
                return False
        return True

    def __getitem__(self, index):
        if self.__array is not None:
            if self.__array.ndim == 3:
                return self.__array[:, :, index]

        return self.images[index]

    def __len__(self) -> int:
        if self.__array is not None:
            return self.__array.shape[-1]
        else:
            return len(self.images)

    @property
    def shape(self):
        if self.__array is not None:
            return self.__array.shape
        else:
            imageShape = self[0].shape
            depth = len(self)
            return imageShape[0], imageShape[1], depth

    def setArray(self):
        if self.__array is None:
            self.__array = np.dstack([im.asArray() for im in self.images])

    @property
    def array(self) -> np.ndarray:
        self.setArray()
        return self.__array

    def removeNoise(self, erosion_size=2, dilation_size=2, closing_size=2):
        self.__checkOriginal()
        if self.__array is None:
            self.setArray()
        self.__array = ndimage.grey_erosion(self, size=erosion_size)
        self.__array = ndimage.grey_dilation(self, size=dilation_size)
        self.__array = ndimage.grey_closing(self, size=closing_size)

    def setMask(self, maskClosing=3, __apply=False):  # todo: better mask options/algo
        self.__checkOriginal()
        mask = self.__array > self.__array.max()/80
        mask = ndimage.binary_opening(mask, iterations=maskClosing)
        mask = ndimage.binary_closing(mask, iterations=maskClosing)
        if __apply:
            self.__array = mask
        else:
            self.maskedZStack = mask
        self.__masked = True

    def applyMask(self, maskClosing=3):
        """
        Precision/ambiguity : There's a difference between turning a Zstack
        into a mask (what applyMask does right now) and applying a mask on
        zStack to remove some pixels (which no methods here do).
        """
        self.setMask(maskClosing, __apply=True)

    def setLabel(self, __apply=False):
        mask = self.__checkMask()
        labeledZStack, nbOfObjects = ndimage.label(mask)
        self.params["nbOfObjects"] = nbOfObjects
        if __apply:
            self.__array = labeledZStack
        else:
            self.labeledZStack = labeledZStack
        self.__labeled = True

    def applyLabel(self):
        self.setLabel(__apply=True)

    def __checkOriginal(self):
        if (self.originalZStack is None) and self.__keepOriginal:
            self.originalZStack = self.__array.copy()

    def __checkMask(self):
        if not self.__masked:
            raise Exception("Cannot label without a mask reference.")
        else:
            return self.maskedZStack or self.__array

    def parameterize(self):
        assert self._allStacksAreInMemory(), "Need all stacks in memory. Use setters method."
        self.params["objectsSize"] = self.__getObjectsSize()
        self.params["totalSize"] = sum(self.params["objectsSize"])
        self.params["objectsMass"] = self.__getObjectsMass()
        self.params["totalMass"] = sum(self.params["objectsMass"])
        self.params["objectsCM"] = self.__getObjectsCenterOfMass()
        self.params["totalCM"] = self.__getCenterOfMass()

        return self.params

    def _allStacksAreInMemory(self):
        stacks = [self.originalZStack, self.maskedZStack, self.labeledZStack]
        if any(stack is None for stack in stacks):
            return False
        else:
            return True

    def __getObjectsSize(self):
        maskSizes = ndimage.sum(self.maskedZStack, self.labeledZStack, range(1, self.params['nbOfObjects'] + 1))
        return list(maskSizes)

    def __getObjectsMass(self):
        sumValues = ndimage.sum(self.originalZStack, self.labeledZStack, range(1, self.params['nbOfObjects'] + 1))
        return list(sumValues)

    def __getObjectsCenterOfMass(self):
        centersOfMass = ndimage.center_of_mass(self.originalZStack, self.labeledZStack, range(1, self.params['nbOfObjects'] + 1))
        return list(centersOfMass)

    def __getCenterOfMass(self):
        centerOfMass = np.average(self.params["objectsCM"], axis=0, weights=self.params["objectsMass"])
        return list(centerOfMass)

    def saveParamsToFile(self, filepath):
        jsonParams = json.dumps(self.params, indent=4)

        with open(filepath+".json", "w+") as file:
            file.write(jsonParams)

    def show(self, axis=-1):
        plt.imshow(self.__array.mean(axis))
        plt.show()

    def showAllStacks(self, axis=-1):
        stacks = self._stacksInMemory()
        fig, axes = plt.subplots(1, len(stacks))
        for i, (key, stack) in enumerate(stacks.items()):
            if key in ["Original ", ""]:
                axes[i].imshow(stack.mean(axis))
            else:
                axes[i].imshow(stack.max(axis))
            axes[i].set_title(key + "Stack")
        plt.show()

    def _stacksInMemory(self):
        stacks = {"Original ": self.originalZStack, "": self.__array, "Mask ": self.maskedZStack, "Label ": self.labeledZStack}
        stacksInMemory = {k: v for k, v in stacks.items() if v is not None}
        return stacksInMemory


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

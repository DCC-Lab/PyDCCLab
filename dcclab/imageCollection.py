from .image import *
import numpy as np
import json
import matplotlib.pyplot as plt
from typing import List, Union
from .__lifReader import LifReader
from scipy import ndimage
from collections import OrderedDict


class ImageCollection:
    def __init__(self, images:List[Image]=None, imagesArray:np.ndarray=None, pathPattern: str=None):
        print("Here")
        self.__images = []
        if images is not None:
            if not all(isinstance(image, Image) for image in images):
                raise NotDCCImageException
            else:
                self.__images = images
        elif imagesArray is not None:
            if imagesArray.ndim == 4:
                self.appendFromImagesArray(imagesArray)
            else:
                raise ValueError("ImageCollection is initialized by a 4D numpy array: [width][height][channel][collection]")
        elif pathPattern is not None:
            self.appendMatchingFiles(pathPattern)

    @property
    def images(self):
        return self.__images

    @property
    def asArray(self) -> np.ndarray:
        # An ImageCollection may not always be put into
        # an array: if all images have different sizes, this will
        # fail
        return np.stack([ image.asArray() for image in self.images ], axis=3)

    def __getitem__(self, index):
        return self.images[index]

    def __len__(self) -> int:
        return len(self.images)

    @property
    def numberOfImages(self):
        return len(self.images)

    def indexOf(self, image) -> int:
        if not isinstance(image, Image):
            return None

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

    def appendFromImagesArray(self, imagesArray):
        if imagesArray.ndim == 4:
            images = [Image(imagesArray[:, :,:, i]) for i in range(array.shape[3])]
            self.append(images)
        else:
            raise NotImplementedError("ImageCollection from 4D arrays only.")

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

    # Image manipulation

    @property
    def isLabelled(self) -> bool:
        # Only if all images are labelled, we return True
        for image in self.images:
            if not image.isLabelled:
                return False
        return True

    def labelMaskComponents(self):
        for image in self.images:
            image.labelMaskComponents()

    def analyzeComponents(self):
        for image in self.images:
            image.analyzeComponents()

    def filterNoise(self):
        for image in self.images:
            image.filterNoise()

    def threshold(self, value = None):
        for image in self.images:
            image.threshold(value)

    def setMaskFromThreshold(self, value = None):
        for image in self.images:
            image.setMaskFromThreshold(value)


class ZStack(ImageCollection):
    def __init__(self, images:List[Image]=None, imagesArray:np.ndarray=None, pathPattern: str=None, keepOriginal: bool=True):
        super().__init__(images, imagesArray, pathPattern)
        if not self.imagesAreSimilar:
            raise ValueError("Images in z-stack are not all the same shape")

        self.__keepOriginal = keepOriginal
        self.params = OrderedDict()

    @property
    def imagesAreSimilar(self) -> bool:
        shape = None
        for image in self.images:
            if shape is None:
                shape = image.shape
            elif shape != image.shape:
                return False
        return True

    @property
    def asArray(self) -> np.ndarray:
        # An ZStack is always a 4D array
        # All images are the same size
        return np.stack([ image.asArray() for image in self.images ], axis=3)

    # def removeNoise(self, erosion_size=2, dilation_size=2, closing_size=2):
    #     self.__checkOriginal()
    #     if self.__array is None:
    #         self.setArray()
    #     self.__array = ndimage.grey_erosion(self, size=erosion_size)
    #     self.__array = ndimage.grey_dilation(self, size=dilation_size)
    #     self.__array = ndimage.grey_closing(self, size=closing_size)

    # def setMask(self, maskClosing=3, _apply=False):  # todo: better mask options/algo
    #     mask = self.__array > self.__array.max()/80
    #     mask = ndimage.binary_opening(mask, iterations=maskClosing)
    #     mask = ndimage.binary_closing(mask, iterations=maskClosing)
    #     if _apply:
    #         self.__checkOriginal()
    #         self.__array = mask
    #     else:
    #         self.maskedZStack = mask
    #     self.__masked = True

    # def applyMask(self, maskClosing=3):
    #     """
    #     Precision/ambiguity : There's a difference between turning a Zstack
    #     into a mask (what applyMask does right now) and applying a mask on
    #     zStack to remove some pixels (which no methods here do).
    #     """
    #     self.setMask(maskClosing, _apply=True)

    # def setLabel(self, _apply=False):
    #     mask = self.__checkMask()
    #     labeledZStack, nbOfObjects = ndimage.label(mask)
    #     self.params["nbOfObjects"] = nbOfObjects
    #     if _apply:
    #         self.__checkOriginal()
    #         self.__array = labeledZStack
    #     else:
    #         self.labeledZStack = labeledZStack
    #     self.__labeled = True

    # def applyLabel(self):
    #     self.setLabel(_apply=True)

    # def __checkOriginal(self):
    #     if (self.originalZStack is None) and self.__keepOriginal:
    #         self.originalZStack = self.__array.copy()

    # def __checkMask(self):
    #     if not self.__masked:
    #         raise Exception("Cannot label without a mask reference.")
    #     else:
    #         if self.maskedZStack is not None:
    #             return self.maskedZStack
    #         else:
    #             return self.__array

    # def parameterize(self):
    #     assert self._readyForParameterization(), "Need all stacks in memory. Use setters method."
    #     self.params["objectsSize"] = self.__getObjectsSize()
    #     self.params["totalSize"] = np.sum(self.params["objectsSize"])
    #     self.params["objectsMass"] = self.__getObjectsMass()
    #     self.params["totalMass"] = np.sum(self.params["objectsMass"])
    #     self.params["objectsCM"] = self.__getObjectsCenterOfMass()
    #     self.params["totalCM"] = self.__getCenterOfMass()

    #     return self.params

    # def _readyForParameterization(self):
    #     stacks = [self.maskedZStack, self.labeledZStack]
    #     if any(stack is None for stack in stacks):
    #         return False
    #     else:
    #         return True

    # def __getObjectsSize(self):
    #     maskSizes = ndimage.sum(self.maskedZStack, self.labeledZStack, range(1, self.params['nbOfObjects'] + 1))
    #     return list(maskSizes)

    # def __getObjectsMass(self):
    #     if self.originalZStack is None:
    #         originalZStack = self.__array
    #     else:
    #         originalZStack = self.originalZStack

    #     sumValues = ndimage.sum(originalZStack, self.labeledZStack, range(1, self.params['nbOfObjects'] + 1))
    #     return list(sumValues)

    # def __getObjectsCenterOfMass(self):
    #     if self.originalZStack is None:
    #         originalZStack = self.__array
    #     else:
    #         originalZStack = self.originalZStack

    #     centersOfMass = ndimage.center_of_mass(originalZStack, self.labeledZStack, range(1, self.params['nbOfObjects'] + 1))
    #     return list(centersOfMass)

    # def __getCenterOfMass(self):
    #     centerOfMass = np.average(self.params["objectsCM"], axis=0, weights=self.params["objectsMass"])
    #     return list(centerOfMass)

    # def saveParamsToFile(self, filepath):
    #     jsonParams = json.dumps(self.params, indent=4)
    #     if filepath.split(".")[-1] != "json":
    #         filepath += ".json"

    #     with open(filepath, "w+") as file:
    #         file.write(jsonParams)

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
        stacks = OrderedDict([("Original ", self.originalZStack), ("", self.__array), ("Mask ", self.maskedZStack), ("Label ", self.labeledZStack)])
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

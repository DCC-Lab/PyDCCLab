from .image import *
from .image import Image
from dcclab.utils.pathPattern import *
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Union
import sys
from enum import Enum

class Axis(Enum):
    x = 'x'
    y = 'y'
    z = 'z'
    t = 't'
    any = '.'

class ImageCollection:
    Axes = [Axis.x, Axis.y, Axis.z, Axis.t]

    def __init__(self, images: List['Image'] = None, imagesArray: np.ndarray = None, pathPattern: str = None):
        self.__images = []
        self.__axes = None
        self.__iteration = 0

        shape = None
        if images is not None:
            if not all(isinstance(image, Image) for image in images):
                raise NotDCCImageException
            else:
                self.__images = images
        elif imagesArray is not None:
            self.fromArray(imagesArray)
        elif pathPattern is not None:
            shape = self.appendMatchingFiles(pathPattern)

        if shape is None:
            self.__shape = (len(self.__images),)
            self.__axes = ['.']
        else:
            self.__shape = shape
            self.__axes = ImageCollection.Axes[0:self.dimension]

    @property
    def shape(self):
        return self.__shape

    @property
    def dimension(self):
        return len(self.shape)

    @property
    def axes(self):
        return self.__axes

    @axes.setter
    def axes(self, value):
        if len(value) != self.dimension:
            raise ValueError("Axes must be an array {0} of dimension {1}".format(value, self.dimension))
        else:
            self.__axes = value

    @property
    def shape(self):
        return self.__shape

    def reshape(self, tuple, axes=None):
        product = 1
        for v in tuple:
            product *= v

        if product != len(self.__images):
            raise ValueError("Shape {0} must be compatible with {1} elements".format(tuple, len(self.__images)))

        self.__shape = tuple

        if axes is None:
            self.axes = [ Axis.any ] * len(tuple)
        else:
            self.axes = axes

    def __getitem__(self, index):
        if isinstance(index, tuple):
            flatIndex = self.ravel(index)
        else:
            flatIndex = index
        return self.images[flatIndex]

    def __iter__(self):
        self.__iteration = 0
        return self

    def __next__(self):
        try:
            return self.unravel(self.__iteration)
        except ValueError as err:
            raise StopIteration
        finally:
            self.__iteration = self.__iteration + 1

    def ravel(self, indexes):
        return np.ravel_multi_index(indexes, self.shape)

    def unravel(self, index):
        return np.unravel_index(index, self.shape)

    def save(self, pathOrPattern: str):
        pattern = PathPattern(pathOrPattern)
        if pattern.isWritePattern:
            for (i, image) in enumerate(self.images):
                path = pattern.filePathWithIndex(i)
                image.save(path)
        else:
            raise ValueError("To save files in ImageCollection, use a Python format-string such as Image-{0:03d}.tiff")

    @property
    def images(self):
        return self.__images

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
    def sizeInBytes(self):
        sizeInBytes = 0
        for image in self.images:
            sizeInBytes += image.sizeInBytes
        return sizeInBytes

    @property
    def hasLabelledComponents(self) -> bool:
        for image in self.images:
            if not image.hasLabelledComponents:
                return False
        return True

    @property
    def hasMask(self) -> bool:
        for image in self.images:
            if not image.hasMask:
                return False
        return True

    @property
    def hasOriginal(self) -> bool:
        for image in self.images:
            if not image.hasOriginal:
                return False
        return True

    def clear(self):
        self.__images = []

    def asArray(self) -> np.ndarray:
        # An ImageCollection may not always be put into
        # an array: if all image have different sizes, this will
        # fail
        return np.stack([image.asArray() for image in self.images], axis=3)

    def __len__(self) -> int:
        return len(self.images)

    @property
    def numberOfImages(self):
        return len(self)

    def indexOf(self, image) -> int:
        if not isinstance(image, Image):
            return None

        for (i, imageInList) in enumerate(self.images):
            if image == imageInList:
                return i

        return None

    def contains(self, image) -> bool:
        return self.indexOf(image) is not None

    def append(self, image: 'Image'):
        if self.contains(image):
            raise ImageAlreadyInCollectionException
        if not isinstance(image, Image):
            raise NotImageException

        self.images.append(image)

    def extend(self, images: List['Image']):
        for image in images:
            if self.contains(image):
                raise ImageAlreadyInCollectionException
            self.images.append(image)

    def appendMatchingFiles(self, pattern):
        paths = PathPattern(pattern)
        if paths.hasCaptureGroups:
            thePaths = paths.matchingFilesWithCaptureGroups()
            allIndexes = sorted(thePaths.keys())
        else:
            thePaths = paths.matchingFiles()
            allIndexes = [ (v,) for v in range(len(thePaths)) ]
            thePaths = dict(zip(allIndexes, thePaths))

        for indexes in allIndexes:
            path = thePaths[indexes]
            try:
                image = Image(path=path)
                self.append(image)
            except:
                pass

        if len(allIndexes) >= 2:
            firstIndex = allIndexes[0]
            lastIndex = allIndexes[-1]
            newShape = np.array(lastIndex)-np.array(firstIndex)+1
        else:
            newShape = (1,)

        return tuple([v for v in newShape])

    def appendFromImagesArray(self, imagesArray):
        if imagesArray.ndim == 4:
            images = [Image(imagesArray[:, :, :, i]) for i in range(imagesArray.shape[3])]
            for image in images:
                self.append(image)
        else:
            raise NotImplementedError("ImageCollection from 4D arrays only: [width][height][channel][collection]")

    def fromArray(self, imagesArray):
        """ Instantiate self.__images from an Array."""
        # FIXME (?) : ImageCollection already has appendFromImagesArray. but the method doesn't overwrite self.__images

        self.__images = []
        if imagesArray.ndim == 4:
            nbOfImages = imagesArray.shape[3]
            for i in range(nbOfImages):
                self.progressBar(i, nbOfImages - 1)
                image = Image(imagesArray[:, :, :, i])
                self.__images.append(image)
            print("\n")  # end progress bar
        else:
            raise NotImplementedError("ImageCollection from 4D arrays only.")

    def replaceFromArray(self, imagesArray):
        assert self.numberOfImages == imagesArray.shape[3], "Array has to contain the same number of image."

        for i, image in enumerate(self.images):
            image.replaceFromArray(imagesArray[:, :, :, i])

    def removeAt(self, index: int):
        self.images.pop(index)

    def remove(self, image: 'Image'):
        if not isinstance(image, Image):
            raise NotImageException

        index = self.indexOf(image)
        if index is None:
            raise ImageNotInCollectionException
        del self.images[index]

    def removeChannels(self, channels: list):
        """ These functions 'can' crash if image don't have the same numberOfChannels"""
        for image in self.images:
            image.removeChannels(channels)

    def keepChannel(self, channel: int):
        for image in self.images:
            image.keepChannel(channel)

    def restoreOriginal(self):
        for image in self.images:
            image.restoreOriginal()

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

    def labelMaskComponents(self):
        for image in self.images:
            image.labelMaskComponents()

    def setLabelledComponents(self, labels: ['Channel']):
        if len(labels) == len(self.images):
            for image, label in zip(self.images, labels):
                image.setLabelledComponents(label)
        else:
            # todo: Must provide one mask per channel for each image
            raise NotImplementedError

    @property
    def labelInfo(self) -> dict:
        uniqueValues = dict()
        for image in self.images:
            for channel in image.channels:
                # todo: check if its semantic ?
                values, counts = np.unique(channel.labelledComponents, return_counts=True)
                for value, count in zip(values, counts):
                    if value not in uniqueValues:
                        uniqueValues[value] = int(count)
                    else:
                        uniqueValues[value] += count
        return uniqueValues

    def analyzeComponents(self):
        for image in self.images:
            image.analyzeComponents()

    def filterNoise(self):
        for image in self.images:
            image.filterNoise()

    def threshold(self, value=None):
        for image in self.images:
            image.threshold(value)

    def setMask(self, mask: 'Channel'):
        if mask.isBinary:
            for image in self.images:
                image.setMask(mask)
        else:
            raise ValueError("Mask must be binary")

    def setMasks(self, masks: ['Channel']):
        if len(masks) == len(self.images):
            for image, mask in zip(self.images, masks):
                image.setMask(mask)
        else:
            # todo: Must provide one mask per channel for each image
            raise NotImplementedError

    def setMaskFromThreshold(self, value=None):
        for image in self.images:
            image.setMaskFromThreshold(value)

    def applyConvolution(self, matrix: Union[np.ndarray, list]) -> None:
        for image in self.images:
            image.applyConvolution(matrix)

    def applyXDerivative(self) -> None:
        for image in self.images:
            image.applyXDerivative()

    def applyYDerivative(self) -> None:
        for image in self.images:
            image.applyYDerivative()

    def applyGaussianFilter(self, sigma: float) -> None:
        for image in self.images:
            image.applyGaussianFilter(sigma)

    def applyThresholding(self, value=None) -> None:
        if value is None:
            self.applyIsodataThresholding()
        else:
            self.applyGlobalThresholding(value)

    def applyGlobalThresholding(self, value) -> None:
        for image in self.images:
            image.applyGlobalThresholding(value)

    def applyIsodataThresholding(self) -> None:
        for image in self.images:
            image.applyIsodataThresholding()

    def applyOtsuThresholding(self) -> None:
        for image in self.images:
            image.applyOtsuThresholding()

    def applyOpening(self, size: int = 2) -> None:
        for image in self.images:
            image.applyOpening(size)

    def applyClosing(self, size: int = 2) -> None:
        for image in self.images:
            image.applyClosing(size)

    def applyErosion(self, size: int = 2):
        for image in self.images:
            image.applyErosion(size)

    def applyDilation(self, size: int = 2):
        for image in self.images:
            image.applyDilation(size)

    def applyNoiseFilter(self, algorithm=None):
        self.applyNoiseFilterWithErosionDilation()

    def applyNoiseFilterWithErosionDilation(self, erosion_size=2, dilation_size=2, closing_size=2):
        for image in self.images:
            image.applyNoiseFilterWithErosionDilation(erosion_size, dilation_size, closing_size)

    def applyOpeningToMask(self, size: int = None, iterations: int = 1):
        assert self.hasMask, "Mask is not present."
        for image in self.images:
            image.applyOpeningToMask(size, iterations)

    def applyClosingToMask(self, size: int = None, iterations: int = 1):
        assert self.hasMask, "Mask is not present."
        for image in self.images:
            image.applyClosingToMask(size, iterations)

    @staticmethod
    def progressBar(value, endvalue, bar_length=20):
        percent = float(value) / endvalue
        arrow = '-' * int(round(percent * bar_length) - 1) + '>'
        spaces = ' ' * (bar_length - len(arrow))

        sys.stdout.write("\r   [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
        sys.stdout.flush()

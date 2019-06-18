from .image import *
import numpy as np
import json
import inspect
import matplotlib.pyplot as plt
from typing import List, Union
from .__lifReader import LifReader
from scipy import ndimage
from collections import OrderedDict


class ImageCollection:
    def __init__(self, images:List[Image]=None, imagesArray:np.ndarray=None, pathPattern: str=None):
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
    def sizeInBytes(self):
        sizeInBytes = 0
        for image in self.images:
            sizeInBytes += image.sizeInBytes
        return sizeInBytes

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
            images = [Image(imagesArray[:, :, :, i]) for i in range(imagesArray.shape[3])]
            for image in images:
                self.append(image)
        else:
            raise NotImplementedError("ImageCollection from 4D arrays only.")

    def fromSingleChannelArray(self, channelArray, channel):
        """ fixme: if its a single channel 4D array, then fromArray works...
            and if we use 'from' we mean to define all the collection as a single channel,
            so no need to specify which channel it is...
            unless to function is called something like replaceChannelFromArray(array, channnel)"""
        raise NotImplementedError()

    def fromArray(self, imagesArray):
        """ FIXME: fromSingleChannelArray and fromArray should only be defined inside ImageCollection.
            but ImageCollection already has appendFromImagesArray. but the method doesn't overwrite
            self.images ... """

        self.__images = []  # fromArray redefines ?
        if imagesArray.ndim == 4:
            images = [Image(imagesArray[:, :, :, i]) for i in range(imagesArray.shape[3])]
            for image in images:
                self.__images.append(image)
        else:
            raise NotImplementedError("ImageCollection from 4D arrays only.")

    def removeAt(self, index: int):
        self.images.pop(index)

    def remove(self, image: Image):
        index = self.indexOf(image)
        del self.images[index]

    def removeChannels(self, channels: list):
        """ These functions 'can' crash if images don't have the same numberOfChannels"""
        for image in self.images:
            image.removeChannels(channels)

    def keepChannel(self, channel: int):
        for image in self.images:
            image.keepChannel(channel)

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

    def setMask(self, mask:Channel):
        if mask.isBinary:
            for image in self.images:
                image.setMask(mask)
        else:
            raise ValueError("Mask must be binary")

    def setMasks(self, masks:[Channel]):
        if len(masks) == len(self.images):
            # We have one mask per image
            for mask in masks:
                for image in self.images:
                    image.setMask(mask)
        else:
            raise NotImplementedError("Must provide one mask per channel for each image, may be different")

    def setMaskFromThreshold(self, value = None):
        for image in self.images:
            image.setMaskFromThreshold(value)

    def applyConvolution(self, matrix: typing.Union[np.ndarray, list]) -> None:
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

    def applyOpening(self, size: int) -> None:
        for image in self.images:
            image.applyOpening(size)

    def applyClosing(self, size: int) -> None:
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


class ZStack(ImageCollection):
    def __init__(self, images: List[Image]=None, imagesArray: np.ndarray=None, pathPattern: str=None, keepOriginal: bool=True):
        super().__init__(images, imagesArray, pathPattern)
        if not self.imagesAreSimilar:
            raise ValueError("Images in z-stack are not all the same shape")

        self.__keepOriginal = keepOriginal  # todo : init Channel Objects with keepOriginal flag. + Define ZStack.original ?
        self.params = OrderedDict()
        self.processIn3D = True

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
    def numberOfChannels(self):
        """ Can be moved to ImageCollection [addressing the issue in removeChannels()] """
        """ Not clean, but it works since imagesAreSimilar... """
        """ Coulf be stored as a property variable in init instead """
        return self.images[0].shape[2]

    def asArray(self) -> np.ndarray:
        # A ZStack is always a 4D array of shape (X, Y, C, Z)
        # All images are the same size
        return np.stack([image.asArray() for image in self.images], axis=3)

    def asSingleChannelArray(self, channel) -> np.ndarray:
        imagesArray = self.asArray()
        singleChannel = imagesArray[:, :, channel, :]
        np.squeeze(singleChannel)
        return singleChannel

    def apply3DFilter(self, filterFunc, *filterArgs):  # todo: maybe multiple functions
        """ These Functions should be processed over one Channel at a time"""
        if self.processIn3D is None:
            raise ZStackProcessDimensionIsNotDefined
        elif self.processIn3D:
            filteredArrays = []
            for channel in list(range(self.numberOfChannels)):
                array = self.asSingleChannelArray(channel)
                filteredArrays.append(filterFunc(array, *filterArgs))
            newStack = np.stack(filteredArrays, axis=2)
            self.fromArray(newStack)
        else:
            callerFunction = inspect.stack()[1].function
            getattr(super(), callerFunction)(*filterArgs)

    def applyOpening(self, size: int=2) -> None:
        self.apply3DFilter(ndimage.grey_opening, size)

    def applyClosing(self, size: int=2) -> None:
        self.apply3DFilter(ndimage.grey_closing, size)

    def applyErosion(self, size: int=2):
        self.apply3DFilter(ndimage.grey_erosion, size)

    def applyDilation(self, size: int=2):
        self.apply3DFilter(ndimage.grey_dilation, size)

    def applyNoiseFilter(self, algorithm=None):
        if self.processIn3D:
            raise NotImplementedError()
        else:
            super().applyNoiseFilter(size)

    def applyNoiseFilterWithErosionDilation(self, erosion_size=2, dilation_size=2, closing_size=2):
        if self.processIn3D:
            raise NotImplementedError()
        else:
            super().applyNoiseFilterWithErosionDilation(size)

    def show(self, axis=-1):
        stack4DArray = self.asArray()
        plt.imshow(stack4DArray.mean(axis))
        plt.show()

    def showAllStacks(self, axis=-1):
        stacks = self.stacksInMemory()
        fig, axes = plt.subplots(1, len(stacks))
        for i, (key, stack) in enumerate(stacks.items()):
            if key in ["Original ", ""]:
                axes[i].imshow(stack.mean(axis))
            else:
                axes[i].imshow(stack.max(axis))
            axes[i].set_title(key + "Stack")
        plt.show()

    def stacksInMemory(self):
        stacks = OrderedDict([("Original ", self.originalZStack), ("", self.__array), ("Mask ", self.maskedZStack), ("Label ", self.labeledZStack)])
        stacksInMemory = {k: v for k, v in stacks.items() if v is not None}
        return stacksInMemory

from .image import *
from .pathPattern import *
import numpy as np
import json
import inspect
from .image import Image

import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from typing import List, Union
from scipy import ndimage
from collections import OrderedDict
from PIL import Image as PILImage
import sys


class ImageCollection:
    def __init__(self, images:List[Image]=None, imagesArray:np.ndarray=None, pathPattern: str=None):
        self.__images = []
        if images is not None:
            if not all(isinstance(image, Image) for image in images):
                raise NotDCCImageException
            else:
                self.__images = images
        elif imagesArray is not None:
            self.fromArray(imagesArray)
        elif pathPattern is not None:
            self.appendMatchingFiles(pathPattern)

    def save(self, pathOrPattern:str):
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
    def isLabelled(self) -> bool:
        for image in self.images:
            if not image.isLabelled:
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
        # an array: if all images have different sizes, this will
        # fail
        return np.stack([image.asArray() for image in self.images], axis=3)

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
        if not isinstance(image, Image):
            raise NotImageException

        self.images.append(image)

    def extend(self, images: List[Image]):
        for image in images:
            if self.contains(image):
                raise ImageAlreadyInCollectionException
            self.images.append(image)

    def appendMatchingFiles(self, pattern):
        paths = PathPattern(pattern)
        for path in paths.matchingFiles():
            try:
                image = Image(path=path)
                self.append(image)
            except:
                pass

    def appendFromImagesArray(self, imagesArray):
        if imagesArray.ndim == 4:
            images = [Image(imagesArray[:, :, :, i]) for i in range(imagesArray.shape[3])]
            for image in images:
                self.append(image)
        else:
            raise NotImplementedError("ImageCollection from 4D arrays only: [width][height][channel][collection]")

    def fromArray(self, imagesArray):
        """ Intentiate self.__images from an Array."""
        # FIXME (?) : ImageCollection already has appendFromImagesArray. but the method doesn't overwrite self.__images

        self.__images = []
        if imagesArray.ndim == 4:
            nbOfImages = imagesArray.shape[3]
            for i in range(nbOfImages):
                progressBar(i, nbOfImages-1)
                image = Image(imagesArray[:, :, :, i])
                self.__images.append(image)
            print("\n")  # end progress bar
        else:
            raise NotImplementedError("ImageCollection from 4D arrays only.")

    def replaceFromArray(self, imagesArray):
        assert self.numberOfImages == imagesArray.shape[3], "Array has to contain the same number of images."

        for i, image in enumerate(self.images):
            image.replaceFromArray(imagesArray[:, :, :, i])

    def removeAt(self, index: int):
        self.images.pop(index)

    def remove(self, image: Image):
        if not isinstance(image, Image):
            raise NotImageException

        index = self.indexOf(image)
        if index is None:
            raise ImageNotInCollectionException
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

    def labelMaskComponents(self):
        for image in self.images:
            image.labelMaskComponents()

    def analyzeComponents(self):
        for image in self.images:
            image.analyzeComponents()

    def filterNoise(self):
        for image in self.images:
            image.filterNoise()

    def threshold(self, value=None):
        for image in self.images:
            image.threshold(value)

    def setMask(self, mask: Channel):
        if mask.isBinary:
            for image in self.images:
                image.setMask(mask)
        else:
            raise ValueError("Mask must be binary")

    def setMasks(self, masks: [Channel]):
        if len(masks) == len(self.images):
            for mask in masks:
                for image in self.images:
                    image.setMask(mask)
        else:
            raise NotImplementedError("Must provide one mask per channel for each image, may be different")

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

    def applyOpeningToMask(self, size: int=None, iterations: int = 1):
        for image in self.images:
            image.applyOpeningToMask(size, iterations)

    def applyClosingToMask(self, size: int=None, iterations: int = 1):
        for image in self.images:
            image.applyClosingToMask(size, iterations)


class ZStack(ImageCollection):
    def __init__(self, images: List[Image]=None, imagesArray: np.ndarray=None, pathPattern: str=None, cropAtInit=False):
        self.cropX, self.cropY = [], []
        self.cropFig = None
        self.cropRect = None

        if cropAtInit:
            imagesArray = self.crop4DArray(imagesArray)
        super().__init__(images, imagesArray, pathPattern)
        if not self.imagesAreSimilar:
            raise ValueError("Images in z-stack are not all the same shape")

        self.componentsProperties = OrderedDict()
        self.processIn3D = True  # default None ?

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
        # Can be moved to ImageCollection [addressing the issue in removeChannels()]
        # Not clean, but it works since imagesAreSimilar...
        # Could be stored as a property variable in init instead
        return self.images[0].shape[2]

    @property
    def shape(self):
        x, y, c = self.images[0].shape
        z = len(self)
        return x, y, c, z

    def asArray(self) -> np.ndarray:
        return np.stack([image.asArray() for image in self.images], axis=3)

    def asChannelArray(self, channel: int) -> np.ndarray:
        imagesArray = self.asArray()
        return imagesArray[:, :, channel, :]

    def asOriginalArray(self) -> np.ndarray:
        return np.stack([image.asOriginalArray() for image in self.images], axis=3)

    def asOriginalChannelArray(self, channel: int) -> np.ndarray:
        originalArray = self.asOriginalArray()
        return originalArray[:, :, channel, :]

    def apply3DFilter(self, filterFunc, *filterArgs):
        """ These Functions should be processed over one Channel at a time """
        if self.processIn3D is None:
            raise ZStackProcessDimensionIsNotDefined
        elif self.processIn3D:
            filteredArrays = []
            for channel in list(range(self.numberOfChannels)):
                array = self.asChannelArray(channel)
                filteredArrays.append(filterFunc(array, *filterArgs))
            newStack = np.stack(filteredArrays, axis=2)
            self.replaceFromArray(newStack)
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

    def applyNoiseFilter(self, algorithm: str='ErosionDilation', *filterArgs):
        # fixme: filterArgs hidden from user
        if algorithm == 'ErosionDilation':
            self.applyNoiseFilterWithErosionDilation(*filterArgs)
        else:
            raise NotImplementedError()

    def applyNoiseFilterWithErosionDilation(self, erosion_size=2, dilation_size=2, closing_size=2):
        # todo: maybe try to implement multiple function with args call inside self.apply3DFilter(s)
        # this function actually doesnt really make any sense,
        # its only through specific data noise filtering that such a combo happenned to be effective,
        # I guess this could be removed from the API, but I will look for a way to easily execute multiple filters in one call
        if self.processIn3D is None:
            raise ZStackProcessDimensionIsNotDefined
        elif self.processIn3D:
            filteredArrays = []
            for channel in list(range(self.numberOfChannels)):
                array = self.asChannelArray(channel)
                array = ndimage.grey_erosion(array, erosion_size)
                array = ndimage.grey_dilation(array, dilation_size)
                array = ndimage.grey_closing(array, closing_size)
                filteredArrays.append(array)
            newStack = np.stack(filteredArrays, axis=2)
            self.replaceFromArray(newStack)
        else:
            super().applyNoiseFilterWithErosionDilation(erosion_size, dilation_size, closing_size)

    def getChannelMaskArray(self, channel: int):
        maskStackArray = np.stack([image.channels[channel].mask.pixels for image in self.images], axis=2)
        return maskStackArray

    def getChannelLabelArray(self, channel: int):
        labelStackArray = np.stack([image.channels[channel].labelledComponents for image in self.images], axis=2)
        return labelStackArray

    def labelMaskComponents(self):
        """ Labelling always need to be processed in 3D """
        for channel in list(range(self.numberOfChannels)):
            maskStackArray = self.getChannelMaskArray(channel)
            labelStackArray, nbObjects = label(maskStackArray)
            self.componentsProperties["Channel {}".format(channel)] = OrderedDict()
            self.componentsProperties["Channel {}".format(channel)]["nbOfObjects"] = nbObjects

            self.channelLabelsFromArray(channel, labelStackArray)

    def channelLabelsFromArray(self, channel, labelStackArray):
        for i in range(labelStackArray.shape[2]):
            labelArray = labelStackArray[:, :, i]
            self.images[i].channels[channel].labelledComponents = labelArray

    def analyzeComponents(self):
        for channel in list(range(self.numberOfChannels)):
            properties = self.componentsProperties['Channel {}'.format(channel)]
            if self.hasOriginal:
                originalArray = self.asOriginalChannelArray(channel)
            else:
                originalArray = self.asChannelArray(channel)
            maskArray = self.getChannelMaskArray(channel)
            labelArray = self.getChannelLabelArray(channel)
            nbOfObjects = properties['nbOfObjects']

            properties["objectsSize"] = self.getObjectsSize(maskArray, labelArray, nbOfObjects)
            properties["totalSize"] = np.sum(properties["objectsSize"]).tolist()
            properties["objectsMass"] = self.getObjectsMass(originalArray, labelArray, nbOfObjects)
            properties["totalMass"] = np.sum(properties["objectsMass"]).tolist()
            properties["objectsCM"] = self.getObjectsCenterOfMass(originalArray, labelArray, nbOfObjects)
            properties["totalCM"] = np.average(properties["objectsCM"], axis=0, weights=properties["objectsMass"]).tolist()

    def getObjectsSize(self, mask, label, nbOfObjects):
        maskSizes = ndimage.sum(mask, label, range(1, nbOfObjects + 1))
        return list(maskSizes)

    def getObjectsMass(self, originalStack, label, nbOfObjects):
        sumValues = ndimage.sum(originalStack, label, range(1, nbOfObjects + 1))
        return list(sumValues)

    def getObjectsCenterOfMass(self, originalStack, label, nbOfObjects):
        centersOfMass = ndimage.center_of_mass(originalStack, label, range(1, nbOfObjects + 1))
        return list(centersOfMass)

    def saveComponentsProperties(self, filePath: str):
        jsonParams = json.dumps(self.componentsProperties, indent=4)
        if filePath.split(".")[-1] != "json":
            filePath += ".json"

        with open(filePath, "w+") as file:
            file.write(jsonParams)

    def crop(self):
        # Cropping will not keep original content since cropping Z axis will change self.numberOfImages
        # => using fromArray(), not replaceFromArray()
        cropArray = self.crop4DArray(self.asArray())
        self.fromArray(cropArray)

    # todo: clean method
    def crop4DArray(self, array, axis=-1, bothAxis=True, viewChannelIndex: int=None):
        """ Static method to crop any 4D Arrays
            Careful: this method can be time and memory intensive if array has multiple channels with size around 1 GigaPixel
            :param viewChannelIndex to quickly load crop window of specified channelIndex, while still cropping all channels.
            :param bothAxis to crop both 3D planes
        """
        # todo: maybe add warning if viewChannelIndex=None and array has more than one channel and each channel is around or over 1 Gigapixel
        print("... Loading crop figure")

        if array.shape[2] == 1:
            # Skip useless and slow numpy conversion (a = a + 0.0) of np.mean if theres nothing to average
            projection = array[:, :, 0, :]
        elif viewChannelIndex is not None:
            projection = array[:, :, viewChannelIndex, :]
        else:
            # Careful : numpy.mean gets exponentially slower with array shape and can easily lead to MemoryError
            projection = array.mean(2)
        projection = projection.mean(axis)

        self.ask2DCropIndices(projection, axis)

        if axis == -1:
            array = array[self.cropY[0]: self.cropY[1], self.cropX[0]: self.cropX[1]]
            if bothAxis:
                return self.crop4DArray(array, axis=0)
            else:
                return array
        else:
            array = array[:, self.cropY[0]: self.cropY[1], :, self.cropX[0]: self.cropX[1]]
            return array

    def ask2DCropIndices(self, channelArray, axis=-1):
        # todo: move 2D / 3D crop logic to Channel / Image
        self.cropX = [0, channelArray.shape[axis+1]]
        self.cropY = [0, channelArray.shape[-axis]]

        figure, self.cropFig = plt.subplots()
        self.cropFig.imshow(channelArray, aspect="auto")
        rs = RectangleSelector(self.cropFig, self.__drawRectangleCallback,
                               drawtype='box', useblit=False, button=[1],
                               minspanx=5, minspany=5, spancoords='pixels',
                               interactive=True)
        plt.title("Select ROI", fontsize=18)
        plt.show()

    def __drawRectangleCallback(self, clickEvent, releaseEvent):
        x1, y1 = clickEvent.xdata, clickEvent.ydata
        x2, y2 = releaseEvent.xdata, releaseEvent.ydata

        if self.cropRect is not None:
            self.cropRect.remove()
        self.cropRect = plt.Rectangle((min(x1, x2), min(y1, y2)), np.abs(x1-x2), np.abs(y1-y2), fill=False)
        self.cropFig.add_patch(self.cropRect)
        self.cropX = [int(x1), int(x2)]
        self.cropY = [int(y1), int(y2)]

    def show(self, axis=-1):
        stack4DArray = self.asArray()
        plt.imshow(stack4DArray.mean(axis))
        plt.show()

    def showAllStacks(self, channel: int=None, axis=-1):
        if channel is None:
            raise NotImplementedError("Can only plot single channel stacks.")  # TODO
        stacksDict = self.channelStacksInMemory(channel)
        fig, axes = plt.subplots(1, len(stacksDict))
        for i, (key, stack) in enumerate(stacksDict.items()):
            if key in ["Original ", ""]:
                axes[i].imshow(stack.mean(axis))
            else:
                axes[i].imshow(stack.max(axis))
            axes[i].set_title(key + "Stack")
        plt.show()

    def channelStacksInMemory(self, channel) -> dict:
        stacks = OrderedDict()
        if self.hasOriginal:
            stacks["Original "] = self.asOriginalChannelArray(channel)
        stacks[""] = self.asChannelArray(channel)
        if self.hasMask:
            stacks["Mask "] = self.getChannelMaskArray(channel)
        if self.isLabelled:
            stacks["Label "] = self.getChannelLabelArray(channel)
        return stacks


def progressBar(value, endvalue, bar_length=20):

        percent = float(value) / endvalue
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))

        sys.stdout.write("\r   [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
        sys.stdout.flush()


# FIXME: temporary, merge with pathPattern logic inside ZStack init
# notice that the folder contains one 2Dimage per channel per layer
def getZStackFromFolder(inputDir, channelsToSegment=[0], crop=True):
    files = list(os.walk(inputDir))[0][2]

    channelStacks = []
    for i, channel in enumerate(channelsToSegment):
        print("... Loading channel {}/{}".format(i+1, len(channelsToSegment)))
        channelFilePaths = [os.path.join(inputDir, f) for f in files if str(channel+1) in f.split("_")[-1]]

        channelImages = []
        for filePath in channelFilePaths:
            channelImages.append(np.array(PILImage.open(filePath)))
        stack = np.stack(channelImages, axis=-1)
        channelStacks.append(stack)

    stackArray = np.stack(channelStacks, axis=2)

    return ZStack(imagesArray=stackArray, cropAtInit=crop)

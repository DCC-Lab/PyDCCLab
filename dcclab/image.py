from .channel import *
from .DCCExceptions import *
from .cziUtil import *
import tifffile
import PIL
from .imageFile import *
import os
import re
from typing import List, Union

class Image:

    supportedClasses = [CZIFile, TIFFFile, PILFile, MATLABFile]
    supportedFormats = []


    def __init__(self, imageData:np.ndarray = None, path: str = None):
        self._getSupportedFormats() #FIXME

        if path is not None:
            if not os.path.exists(path):
                raise ValueError("Cannot load '{0}': file does not exist".format(path))

            self.path = path
            self.channels:List[Channel] = []
            self.__fileObject = None
            for supportedClass in Image.supportedClasses:
                try:
                    fileObject = supportedClass(path)
                    imageData = fileObject.imageDataFromPath()
                    if imageData.nbytes != 0:
                        self.channels = self.channelsFromImageData(imageData)
                        self.__fileObject = fileObject
                    break
                except:
                    continue
            if self.__fileObject is None:
                message = "Cannot read '{0}': not a recognized image format ({1})".format(self.path, Image.supportedFormats)
                raise InvalidFileFormatException(message)
        else:
            self.path = None
            self.__fileObject = None
            self.channels = self.channelsFromImageData(imageData)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Image):
            return False
        return np.array_equal(self.asArray(), other.asArray())

    def __getitem__(self, index):
        return self.channels[index]

    @property
    def shape(self):
        if len(self.channels) != 0:
            return self.channels[0].shape

    @property
    def sizeInBytes(self) -> int:
        totalSize = 0
        for channel in self.channels:
            totalSize += channel.sizeInBytes
        return totalSize

    def removeChannels(self, channels:list):
        for index in channels:
            del self.channels[index]

    def asChannelsArray(self):
        channelsPixels = list(map(lambda c: c.pixels, self.channels))
        return channelsPixels

    def asArray(self):
        channelArrays = self.asChannelsArray()
        # An image is always 3D: width x height x channels,
        # even when there is only one channel
        imageData = np.dstack(channelArrays) 
        return imageData

    def save(self, filePath):
        imageAsArray = self.asArray()

        if len(self.channels) == 1:
            mode = 'L'
        elif len(self.channels) == 3:
            mode = 'RGB'
        pilImage = PIL.Image.fromarray(imageAsArray,mode=mode)
        pilImage.save(filePath)

    def display(self, colorMap=None):
        plt.imshow(self.asArray(), cmap=colorMap)
        plt.show()

    def channelsFromImageData(self, imageData):
        if imageData.ndim == 2:
            return [Channel(imageData)]
        elif imageData.ndim == 3:
            channelsData = np.squeeze(np.dsplit(imageData, imageData.shape[2]))
            channels = list(map(lambda pix: Channel(pix), channelsData))
            return channels
        else:
            raise DimensionException(imageData.ndim)

    def _getSupportedFormats(self):
        fmts = list(map( lambda cls: cls.supportedFormats, Image.supportedClasses))
        Image.supportedFormats = [item for sublist in fmts for item in sublist]

    @property
    def isLabelled(self) -> bool:
        # Only if all channels are labelled, we return True
        for channel in self.channels:
            if not channel.isLabelled:
                return False
        return True

    def labelMaskComponents(self):
        for channel in self.channels:
            channel.labelMaskComponents()

    def analyzeComponents(self):
        for channel in self.channels:
            channel.analyzeComponents()

    def filterNoise(self):
        for channel in self.channels:
            channel.filterNoise()

    def threshold(self, value = None):
        for channel in self.channels:
            channel.threshold(value)

    def setMask(self, mask:Channel):
        if mask.isBinary:
            for channel in self.channels:
                channel.setMask(mask)
        else:
            raise ValueError("Mask must be binary")

    def setMasks(self, masks:List[Channel]):
        if len(masks) == len(self.channels):
            for mask in masks:
                if mask.isBinary:
                    for channel in self.channels:
                        channel.setMask(mask)
                else:
                    raise ValueError("Mask must be binary")
        else:
            raise ValueError("Must provide one mask per channel")

    def setMaskFromThreshold(self, value = None):
        for channel in self.channels:
            channel.setMaskFromThreshold(value)


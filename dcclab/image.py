from .channel import *
from .DCCExceptions import *
from .cziUtil import *
import tifffile
import PIL
from .imageFile import *

import re


class Image:

    def __init__(self, path: str):
        self.path = path
        supportedClasses = [CZIFile, TIFFFile, PILFile]
        self.__channels = []
        self.__fileObject = None
        for supportedClass in supportedClasses:
            try:
                self.__fileObject = supportedClass(path)
                imageData = self.__fileObject.imageDataFromPath()
                self.__channels = self.channelsFromImageData(imageData)
                break
            except:
                continue
        if self.__fileObject is None:
            raise InvalidFileFormatException(
                "Cannot read {}. Please verify that the name is correct.".format(self.path))

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

    @property
    def channels(self):
        return self.__channels

    def removeChannels(self, channels):
        for index in channels:
            del self.channels[index]

    def asChannelsArray(self):
        channelsPixels = list(map(lambda c: c.pixels, self.channels))
        return channelsPixels

    def asArray(self):
        channelArrays = self.asChannelsArray()
        imageData = np.dstack(channelArrays)
        return imageData

    def display(self, colorMap=None):
        plt.imshow(self.asArray(), cmap=colorMap)
        plt.show()

    def channelsFromImageData(self, imageData):
        if imageData.ndim == 2:
            return (Channel(imageData))
        elif imageData.ndim == 3:
            channelsData = np.squeeze(np.dsplit(imageData, imageData.shape[2]))
            channels = list(map(lambda pix: Channel(pix), channelsData))
            return channels

        return ()

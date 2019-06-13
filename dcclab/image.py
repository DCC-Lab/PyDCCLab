from .channel import *
from .DCCExceptions import *
from .cziUtil import *
import tifffile
import PIL
from .imageFile import *

import re


class Image:
    supportedClasses = [CZIFile, TIFFFile, PILFile]
    supportedFormats = []

    def __init__(self, imageData:np.ndarray = None, path: str = None):
        self._getSupportedFormats() #FIXME

        if path is not None:
            if not os.path.exists(path):
                raise ValueError("Cannot load '{0}': file does not exist".format(path))

            self.path = path
            self.__channels = []
            self.__fileObject = None
            for supportedClass in Image.supportedClasses:
                try:
                    fileObject = supportedClass(path)
                    imageData = fileObject.imageDataFromPath()
                    if imageData.nbytes != 0:
                        self.__channels = self.channelsFromImageData(imageData)
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
            self.__channels = self.channelsFromImageData(imageData)


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
    def _getSupportedFormats(self):
        fmts = list(map( lambda cls: cls.supportedFormats, Image.supportedClasses))
        Image.supportedFormats = [item for sublist in fmts for item in sublist]

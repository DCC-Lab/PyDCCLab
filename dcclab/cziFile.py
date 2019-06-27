from .image import *
from .cziUtil import *
from .channel import *

"""
The main goal of this file is to read czi files and extract images data (if it is a zstack, it will be read, if it is 
a time serie, it will be read...). It will use ImageCollection instances (derived classes, like the zstack specific
class). It is not the plan to use inheritance because it is unsure of what the structure will be (is it a zstack? or a
simple single image?). For now, it doesn't use any of ImageCollection derived classes, but a future implementation
can be done easily because of the current structure.
"""


class CZIFile(object):
    supportedFormats = ['czi']
    allAxes = "XYCZTRSIBMHV"

    def __init__(self, path):
        self.__cziObj = None
        try:
            self.__cziObj = readCziImage(path)
        except ValueError:
            raise InvalidFileFormatException("Not a compatible format for this reader.")
        self.__tilesDirectory = self.__cziObj.filtered_subblock_directory
        self.__shape = self.__cziObj.shape
        self.__axes = self.__cziObj.axes
        self.__originalDType = self.__cziObj.dtype
        self.__axesDimAndIndex = self.__findAxesDimAndIndex()
        self.__totalWidth = self.__axesDimAndIndex["X"][0]
        self.__totalHeight = self.__axesDimAndIndex["Y"][0]
        self.__isZStack = self.__axesDimAndIndex["Z"][0] is not None
        self.__isTimeSerie = self.__axesDimAndIndex["T"][0] is not None
        self.__isScene = self.__axesDimAndIndex["S"][0] is not None
        self.__numberOfChannels = self.__axesDimAndIndex["C"][0]
        self.__channelMaps = self.__buildChannelMaps() if self.__numberOfChannels > 0 else None
        self.__imagesMappedWithChannels = self.__mapImageToChannels() if self.__channelMaps is not None else None
        # self.__imageList = self.__createImages()
        # self.__zStack = self.__buildZStack()

    @property
    def shape(self):
        return self.__shape

    @property
    def totalWidth(self):
        return self.__totalWidth

    @property
    def totalHeight(self):
        return self.__totalHeight

    @property
    def isZstack(self):
        return self.__isZStack

    @property
    def isTimeSerie(self):
        return self.__isTimeSerie

    @property
    def isScene(self):
        return self.__isScene

    @property
    def channelMaps(self):
        return self.__channelMaps

    @property
    def numberOfChannels(self):
        return self.__numberOfChannels

    @property
    def axes(self):
        return self.__axes

    @property
    def imagesMap(self):
        return self.__imagesMappedWithChannels

    def __createImages(self):
        imageList = None
        if self.__channelMaps is None:
            imageList = self.__YX0Image()
        elif len(self.__channelMaps) > 1:
            imageList = self.__recreateMosaics()
        else:
            imageList = self.__recreateSingleMosaic(self.__channelMaps[0])
        return imageList

    def __recreateMosaics(self):
        mosaics = []
        return mosaics

    def __recreateSingleMosaic(self, channelDict: dict):
        mosaic = np.array((self.__totalWidth, self.__totalHeight), dtype=self.__originalDType)
        for key in channelDict.keys():
            xStart = key[0][0]
            yStart = key[1][0]
            xStop = key[0][-1] + 1
            yStop = key[1][-1] + 1
            mosaic[xStart:xStop, yStart:yStop] = channelDict[key]
        return mosaic

    def __YX0Image(self):
        images = []
        for tile in self.__tilesDirectory:
            images.append(tile.data_segment().data())
        return images

    def __mapImageToChannels(self):
        imagesDict = {}
        channelMaps = self.__channelMaps
        if len(channelMaps) > 1:
            for key in channelMaps[0].keys():
                imagesDict[key] = Image(np.dstack([d[key] for d in channelMaps]))
        else:
            for key in channelMaps[0].keys():
                imagesDict[key] = Image(channelMaps[0][key])
        return imagesDict

    def __buildChannelMaps(self):
        channelMaps = [{} for _ in range(self.__numberOfChannels)]
        for directoryEntry in self.__tilesDirectory:
            tile = directoryEntry.data_segment().data()
            index = tuple(slice(i - j, i - j + k) for i, j, k in
                          zip(directoryEntry.start, self.__cziObj.start, tile.shape))
            tileChannel = index[self.__axesDimAndIndex["C"][1]].start
            xSlice = index[self.__axesDimAndIndex["X"][1]]
            ySlice = index[self.__axesDimAndIndex["Y"][1]]
            zIndex = index[self.__axesDimAndIndex["Z"][1]].start if self.__isZStack else None
            tIndex = index[self.__axesDimAndIndex["T"][1]].start if self.__isTimeSerie else None
            sIndex = index[self.__axesDimAndIndex["S"][1]].start if self.__isScene else None
            mapKey = (range(xSlice.start, xSlice.stop), range(ySlice.start, ySlice.stop), zIndex, sIndex, tIndex)
            channelMaps[tileChannel][mapKey] = np.squeeze(tile)
        if not all(len(x) == len(channelMaps[0]) for x in channelMaps):
            closeCziFileObject(self.__cziObj)
            raise TypeError("The number of tiles in each channel is not the same.")
        return channelMaps

    def __findAxesDimAndIndex(self):
        def findValue(key):
            valueReturn = None
            index = None
            try:
                index = self.__axes.index(key)
            except ValueError:
                if key == "C":
                    if self.__axes == "YX0":
                        valueReturn = 0
                    else:
                        closeCziFileObject(self.__cziObj)
                        raise ValueError("This image has no channel and is not of shape \"YX0\"")
            if index is not None:
                valueReturn = self.__shape[index]
            return valueReturn, index

        return {key: findValue(key) for key in CZIFile.allAxes}

    def __buildTimeSeries(self):
        return None

    def __buildZStack(self):
        zStack = None
        # if self.__isZStack:
        #   zStack = []
        #  channelMaps = self.__channelMaps
        # for key in channelMaps[0].keys():

        return zStack

    def __del__(self):
        if self.__cziObj is not None:
            closeCziFileObject(self.__cziObj)

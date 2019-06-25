from .image import *
from .cziUtil import *
from .channel import *


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
        self.__axesDimAndIndex = self.__findAxesDimAndIndex()
        self.__isZStack = False if self.__axesDimAndIndex["Z"][0] is None else True
        self.__isTimeSeries = False if self.__axesDimAndIndex["T"][0] is None else True
        self.__isScene = False if self.__axesDimAndIndex["S"][0] is None else True
        self.__numberOfChannels = self.__axesDimAndIndex["C"][0]
        self.__channelMaps = self.__buildChannelMaps()
        self.__imageMappedWithChannel = self.__mapImageToChannels()
        self.__zStack = self.__buildZStack()

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
        return self.__imageMappedWithChannel


    def __mapImageToChannels(self):
        imagesDict = {}
        channelMaps = self.__channelMaps
        for key in channelMaps[0].keys():
            imagesDict[key] = Image(np.dstack([d[key] for d in channelMaps]))
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
            tIndex = index[self.__axesDimAndIndex["T"][1]].start if self.__isTimeSeries else None
            mapKey = (range(xSlice.start, xSlice.stop), range(ySlice.start, ySlice.stop), zIndex, tIndex)
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
                pass
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



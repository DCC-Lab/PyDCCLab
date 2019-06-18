from .imageFile import *


class CZIFile(ImageFile):
    supportedFormats = ['czi']
    allAxes = "XYCZTRSIBMHV"

    def __init__(self, path):
        ImageFile.__init__(self, path)
        self.__cziObj = readCziImage(path)
        self.__tilesDirectory = self.__cziObj.filtered_subblock_directory
        self.__shape = self.__cziObj.shape
        self.__axes = self.__cziObj.axes
        self.__axesDimAndIndex = self.__findAxesDimAndIndex()
        self.__numberOfChannel = self.__axesDimAndIndex["C"][0]
        self.__mosaics = self.__mosaicMaps()
        self.tilesAt(1, 1, 1)

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

    def __mosaicMaps(self):
        channelsDict = [{}] * self.__numberOfChannel
        for directoryEntry in self.__tilesDirectory:
            tile = directoryEntry.data_segment().data()
            index = tuple(slice(i - j, i - j + k) for i, j, k in
                          zip(directoryEntry.start, self.__cziObj.start, tile.shape))
            tileChannel = index[self.__axesDimAndIndex["C"][1]].start
            xSlice = index[self.__axesDimAndIndex["X"][1]]
            ySlice = index[self.__axesDimAndIndex["Y"][1]]
            mapKey = (range(xSlice.start, xSlice.stop), range(ySlice.start, ySlice.stop))
            channelsDict[tileChannel][mapKey] = Channel(np.squeeze(tile))
        return channelsDict

    def __del__(self):
        if self.__cziObj is not None:
            closeCziFileObject(self.__cziObj)

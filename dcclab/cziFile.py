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
        self.__isZStack = False if self.__axesDimAndIndex["Z"][0] is None else True
        self.__isTimeSeries = False if self.__axesDimAndIndex["T"][0] is None else True
        self.__numberOfChannel = self.__axesDimAndIndex["C"][0]
        if len(self.__tilesDirectory) % self.__numberOfChannel != 0:
            raise Exception("The number of tiles for each channel is not the same.")
        self.__mosaics = self.__mosaicMaps()
        self.__images = self.__getImages()

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
            if self.__isZStack:
                zIndex = index[self.__axesDimAndIndex["Z"][1]].start
            else:
                zIndex = None
            if self.__isTimeSeries:
                tIndex = index[self.__axesDimAndIndex["T"][1]].start
            else:
                tIndex = None
            mapKey = (range(xSlice.start, xSlice.stop), range(ySlice.start, ySlice.stop), zIndex, tIndex)
            channelsDict[tileChannel][mapKey] = Channel(np.squeeze(tile))
        print(channelsDict)
        return channelsDict

    def __getImages(self) -> typing.List[typing.List[np.ndarray]]:
        listOfChannels = [np.squeeze(channel.data_segment().data()) for channel in self.__tilesDirectory]
        listOfImages = [listOfChannels[x:x + self.__numberOfChannel] for x in
                        range(0, len(listOfChannels), self.__numberOfChannel)]
        plt.imshow(listOfImages[1][0])
        plt.show()
        return listOfImages

    def __del__(self):
        if self.__cziObj is not None:
            closeCziFileObject(self.__cziObj)

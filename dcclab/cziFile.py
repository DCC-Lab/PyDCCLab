from .imageFile import *
from .cziUtil import *
from .imageCollection import *
from .timeSeries import TimeSeries

"""
The main goal of this file is to read czi files and extract images data (if it is a zstack, it will be read, if it is 
a time serie, it will be read...). It will use ImageCollection instances (derived classes, like the zstack specific
class). It is not the plan to use inheritance because it is unsure of what the structure will be (is it a zstack? or a
simple single image?). For now, it doesn't use any of ImageCollection derived classes, but a future implementation
can be done easily because of the current structure.
"""


class CZIFile(ImageFile):
    supportedFormats = ['czi']
    # See czi documentation for more info about the axes
    allAxes = "XYCZTRSIBMHV"

    def __init__(self, path):
        ImageFile.__init__(self, path)
        self.__cziObj = None
        try:
            self.__cziObj = readCziImage(path)
        except ValueError:
            raise InvalidFileFormatException("Not a compatible format for this reader.")
        self.__mosaic, self.__indexAndTiles = decodeImages(self.__cziObj)
        self.__shape = self.__cziObj.shape
        self.__axes = self.__cziObj.axes
        self.__originalDType = self.__cziObj.dtype
        self.__axesDimAndIndex = self.__findAxesDimAndIndex()
        self.__totalWidth = self.__axesDimAndIndex["X"][0]
        self.__totalHeight = self.__axesDimAndIndex["Y"][0]
        self.__isZStack = self.__axesDimAndIndex["Z"][0] > 1
        self.__isTimeSeries = self.__axesDimAndIndex["T"][0] > 1
        self.__isScenes = self.__axesDimAndIndex["S"][0] > 1
        if self.__isTimeSeries and self.__isScenes:
            raise NotImplementedError("Time series and scenes combination is not implemented")
        if self.__isTimeSeries and self.__isZStack:
            raise NotImplementedError("Time series and z-stack combination is not implemented")
        if self.__isZStack and self.__isScenes:
            raise NotImplementedError("Z-stack and scenes combination is not implemented")
        self.__numberOfChannels = self.__axesDimAndIndex["C"][0]
        self.__tileMap = self.__buildTileMap() if self.__axes != "YX0" else None

    def allData(self):
        pass

    def imageData(self):
        image = None
        if not (self.__isScenes or self.__isTimeSeries or self.__isZStack):
            image = Image(self.__mosaic.squeeze().transpose(1, 2, 0)) if self.__axes != "YX0" else self.__YX0Image()
        else:
            raise ValueError("This file contains more than just one image.")
        return image

    def mapData(self):
        pass

    def scenesData(self):
        scenes = None
        if self.__isScenes:
            scenes = []
            nbScenes = self.__axesDimAndIndex["S"][0]
            channelIndex = self.__axesDimAndIndex["C"][1]
            mosaic = self.__squeezeAccordingToSlice(self.__mosaic, slice(0, channelIndex))
            for i in range(nbScenes):
                scenes.append(Image(mosaic[i, :, :, :].transpose(1, 2, 0)))
        return ImageCollection(scenes)

    def timeSeriesData(self):
        tSeries = None
        if self.__isTimeSeries:
            tSeries = []
            nbTime = self.__axesDimAndIndex["T"][0]
            mosaic = self.__mosaic.squeeze()
            for i in range(nbTime):
                tSeries.append(Image(mosaic[i, :, :, :].transpose(1, 2, 0)))
        return TimeSeries(tSeries)

    def zStackData(self):
        zStack = None
        if self.__isZStack:
            zStack = []
            nbStack = self.__axesDimAndIndex["Z"][0]
            mosaic = self.__mosaic.squeeze()
            for i in range(nbStack):
                zStack.append(Image(mosaic[:, i, :, :].transpose(1, 2, 0)))
        return ZStack(zStack)

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
        return self.__isTimeSeries

    @property
    def isScenes(self):
        return self.__isScenes

    @property
    def tileMap(self):
        return self.__tileMap

    @property
    def numberOfChannels(self):
        return self.__numberOfChannels

    @property
    def axes(self):
        return self.__axes

    @property
    def originalDType(self):
        return self.__originalDType

    def __YX0Image(self):
        singleImage = None
        if self.__axes == "YX0":
            singleImage = self.__mosaic
        return Image(singleImage)

    def __buildTileMap(self):
        tileMap = {}
        for element in self.__indexAndTiles:
            tile = element[1]
            index = element[0]
            tileChannel = index[self.__axesDimAndIndex["C"][1]].start
            xSlice = index[self.__axesDimAndIndex["X"][1]]
            ySlice = index[self.__axesDimAndIndex["Y"][1]]
            zIndex = index[self.__axesDimAndIndex["Z"][1]].start if self.__isZStack else None
            tIndex = index[self.__axesDimAndIndex["T"][1]].start if self.__isTimeSeries else None
            sIndex = index[self.__axesDimAndIndex["S"][1]].start if self.__isScenes else None
            mapKey = (range(xSlice.start, xSlice.stop), range(ySlice.start, ySlice.stop),
                      zIndex, sIndex, tIndex, tileChannel)
            tileMap[mapKey] = np.squeeze(tile)
        return tileMap

    def __findAxesDimAndIndex(self):
        def findValue(key):
            valueReturn = 0
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

    def __del__(self):
        try:
            if self.__cziObj is not None:
                closeCziFileObject(self.__cziObj)
        except AttributeError:
            print("Object already deleted")

    @staticmethod
    def __squeezeAccordingToSlice(array: np.ndarray, s: slice, removeLastDim: bool = True) -> np.ndarray:
        """
        Useful when you want to squeeze an array only in a specific range. For example, an array with shape
        (1, 1, 1, 1000, 1000, 1) with axes BSCYX0, you don't want to remove the Channel dimension with np.squeeze.
        You can use this method to remove axes [0, 1[ by specifying a slice(0, 1) and these axes will be removed.
        :param array: input array to squeeze
        :param s: slice object containing info on which axes to remove.
        :param removeLastDim: boolean specifying if the last axe should be removed.
        :return: The squeezed array
        """
        sliceToTuple = tuple(range(s.start, s.stop))
        if removeLastDim:
            sliceToTuple += (-1,)
        return array.squeeze(axes=sliceToTuple)

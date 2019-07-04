from .__lifReader import LifReader
from .imageCollection import ZStack  # FIXME: creates a circular import that crashes
from typing import Union, List
from .cziUtil import *
from .channel import *
import scipy.io as sio
import PIL


class ImageFile(object):
    supportedFormats = []

    def __init__(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError("{} does not exists.".format(path))
        self.path = path

    def zStackData(self):
        """
        :return: images data as z-stack if possible
        """
        return None

    def zStacksData(self):
        """
        :return: images data as z-stack if possible
        """
        return None

    def timeSeriesData(self):
        """
        :return: images data as a time series if possible
        """
        return None

    def scenesData(self):
        """
        :return: images data as scenes if possible
        """
        return None

    def imageData(self):
        """
        :return: image data (if coherent to return the data of a single image)
        """
        return None

    def allData(self):
        """
        :return: all image data as a list (whether it is a time series, a zstack, a time series of zstack...)
        """
        return None

    def mapData(self):
        """
        :return: images data as a map (key:x/y indexes, value: image data)
        """
        return None

    # FIXME is it really necessary?
    def metadata(self):
        return


# This class is only temporary
class CZIFile_(ImageFile):
    supportedFormats = ['czi']

    def __init__(self, path: str):
        ImageFile.__init__(self, path)

    def imageDataFromPath(self) -> np.ndarray:
        cziObj = readCziImage(self.path)
        axes = cziObj.axes
        print(axes)
        print(cziObj.shape)
        if axes == "BSCYX0":
            if cziObj.shape[1] != 1:
                closeCziFileObject(cziObj)
                raise NotImplementedError("Multiple scenes")
        if axes not in ["BCYX0", "BSCYX0", "YX0"]:
            closeCziFileObject(cziObj)
            raise NotImplementedError(axes)
        mosaic, self.__indexAndTiles = decodeImages(cziObj)
        try:
            cIndex = axes.index("C")
        except ValueError:
            cIndex = -1
        self.__numberOFChannels = mosaic.shape[cIndex]
        mosaic = mosaic.squeeze()
        closeCziFileObject(cziObj)
        if axes == "YX0":
            wholeImage = mosaic
        elif mosaic.ndim == 3:
            wholeImage = mosaic.transpose((1, 2, 0))
        else:
            wholeImage = mosaic
        return wholeImage


class TIFFFile(ImageFile):
    # todo implement parent's methods
    supportedFormats = ['tif', 'tiff']

    def __init__(self, path):
        ImageFile.__init__(self, path)

    def imageDataFromPath(self) -> np.ndarray:
        # todo better method that return every images if multipage
        tiffFileObject = tifffile.TiffFile(self.path)
        imageAsArray = tiffFileObject.asarray().astype(dtype="float32")
        self.__metadata = tiffFileObject.ome_metadata
        imageList = []
        for i in range(imageAsArray.shape[0]):
            imageList.append(imageAsArray[i])
        return imageAsArray


class PILFile(ImageFile):
    # todo implement parent's methods
    supportedFormats = ['(formats supported by PIL module))']

    def __init__(self, path):
        ImageFile.__init__(self, path)

    def imageDataFromPath(self) -> np.ndarray:
        image = PIL.Image.open(self.path)
        imageAsArray = np.array(image)
        return imageAsArray


class MATLABFile(ImageFile):
    # todo implement parent's methods
    supportedFormats = ['mat']

    def __init__(self, path, variable=None):
        ImageFile.__init__(self, path)
        self.variable = variable

    def imageDataFromPath(self) -> np.ndarray:
        dataset = sio.loadmat(self.path)
        if self.variable is not None:
            array = dataset[self.variable]
            if array.ndim == 3:
                return array
            elif array.ndim == 2:
                return np.expand_dims(array, 2)  # always return 3D
            else:
                raise ValueError("Not an image variable")
        else:
            # Try 3D matrices first
            for name in dataset.keys():
                variable = dataset[name]
                if isinstance(variable, np.ndarray):
                    if variable.ndim == 3:
                        return variable
            # We haven't found any 3D variable. Let's try 2D
            for name in dataset.keys():
                variable = dataset[name]
                if isinstance(variable, np.ndarray):
                    if variable.ndim == 2:
                        return np.expand_dims(variable, 2)  # always return 3D

        return None


class LIFFile(ImageFile):
    supportedFormats = ['lif']

    def __init__(self, path):
        ImageFile.__init__(self, path)
        self.__lifObject = LifReader(self.path)
        self.series = self.__lifObject.getSeries()

    @property
    def numberOfSeries(self):
        return len(self.series)

    def __len__(self):
        return self.numberOfSeries

    def __getitem__(self, indices: Union[int, tuple, list, slice]=None):
        if indices is None:
            return self.series
        if type(indices) is slice:
            return self.series[indices]
        elif type(indices) is int:
            return self.series[indices]
        elif type(indices) is tuple:
            indices = list(indices)

        if type(indices) is list:
            return [self.series[i] for i in indices]

    def keepSeries(self, indices):
        self.series = self[indices]
        if type(self.series) is not list:
            self.series = [self.series]

    def removeAt(self, index: int):
        self.series.pop(index)

    def zStackData(self, seriesIndex: int=None, channelIndices=None, crop=False) -> ZStack:
        if seriesIndex is None:
            assert self.numberOfSeries == 1
            seriesIndex = 0

        print("... Loading serie")
        stackArray = self.series[seriesIndex].getStack(channelIndices)
        print("... Loading ZStack Collection")
        zStack = ZStack(imagesArray=stackArray, cropAtInit=crop)
        return zStack

    def zStacksData(self, seriesIndices=None, channelIndices=None, crop=False) -> List[ZStack]:
        if type(seriesIndices) is int:
            seriesIndices = [seriesIndices]

        series = self[seriesIndices]

        zStacks = []
        for i, serie in enumerate(series):
            print("... Loading serie {}/{}".format(i+1, len(series)))
            stackArray = serie.getStack(channelIndices)
            print("... Loading ZStack Collection")
            zStack = ZStack(imagesArray=stackArray, cropAtInit=crop)
            zStacks.append(zStack)

        return zStacks

    def imageDataFromPath(self):
        # todo ?  not sure we need to implement this method. It's not a parent method but I see that all other child classes have this method defined...
        return None

    def metadata(self, serieIndex: int=None, asJson: bool=False):
        if serieIndex is None:
            metadata = []
            for i, serie in enumerate(self.series):
                metadata.append({'serie %i' % i: serie.getMetadata()})
        else:
            metadata = self.series[serieIndex].getMetadata()

        if asJson:
            return json.dumps(metadata, indent=4)
        return metadata

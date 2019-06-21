from .cziUtil import *
from .channel import *
import PIL.Image
import scipy.io as sio


class ImageFile(object):
    supportedFormats = []

    def __init__(self, path):
        self.path = path

    def imageDataFromPath(self) -> np.ndarray:
        return

    def metadata(self):
        return


class CZIFile(ImageFile):
    supportedFormats = ['czi']

    def __init__(self, path: str):
        ImageFile.__init__(self, path)

    def imageDataFromPath(self) -> np.ndarray:
        cziObj = readCziImage(self.path)
        axes = cziObj.axes
        if axes == "BSCYX0":
            if cziObj.shape[1] != 1:
                closeCziFileObject(cziObj)
                raise NotImplementedError("Multiple scenes")
        if axes not in ["BCYX0", "BSCYX0", "YX0"]:
            closeCziFileObject(cziObj)
            raise NotImplementedError(axes)
        mosaic, self.__tilesWithChannelNumber = decodeImages(cziObj)
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
    supportedFormats = ['(formats supported by PIL module))']

    def __init__(self, path):
        ImageFile.__init__(self, path)

    def imageDataFromPath(self) -> np.ndarray:
        image = PIL.Image.open(self.path)
        imageAsArray = np.array(image)
        return imageAsArray


class MATLABFile(ImageFile):
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

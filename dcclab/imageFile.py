from .cziUtil import *
from .channel import *
import PIL.Image
import scipy.io as sio

class ImageFile(object):
    supportedFormats:[]

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
        mosaic, self.__tilesWithChannelNumber = decodeImages(cziObj)
        mosaic = np.squeeze(mosaic)
        self.__numberOFChannels = mosaic.shape[-3]
        closeCziFileObject(cziObj)
        wholeImage = mosaic.transpose((1, 2, 0)) if mosaic.ndim == 3 else mosaic
        return wholeImage


class TIFFFile(ImageFile):
    supportedFormats = ['tif','tiff']

    def __init__(self, path):
        ImageFile.__init__(self, path)

    def imageDataFromPath(self) -> np.ndarray:
        #todo better method that return every images if multipage
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

    def __init__(self, path, variable = None):
        ImageFile.__init__(self, path)
        self.variable = variable

    def imageDataFromPath(self) -> np.ndarray:
        dataset = sio.loadmat(self.path)
        if self.variable is not None:
            array = dataset[self.variable]
            if array.ndim == 2 or array.ndim == 3:
                return array
            elif array.ndim != 3:
                raise ValueError("Not an image variable")
        else:
            for name in dataset.keys():
                variable = dataset[name]
                if isinstance(variable, np.ndarray):
                    if variable.ndim == 2 or variable.ndim == 3:
                        return variable
        return None

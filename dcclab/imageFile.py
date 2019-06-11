from .cziUtil import *
from .channel import *
import PIL.Image


class ImageFile(object):
    def __init__(self, path):
        self.path = path

    def imageDataFromPath(self):
        return

    def metadata(self):
        return


class CZIFile(ImageFile):

    def __init__(self, path: str):
        ImageFile.__init__(self, path)

    def imageDataFromPath(self):
        cziObj = readCziImage(self.path)
        mosaic, self.__tilesWithChannelNumber = decodeImages(cziObj)
        mosaic = np.squeeze(mosaic)
        self.__numberOFChannels = mosaic.shape[-3]
        closeCziFileObject(cziObj)
        wholeImage = mosaic.transpose((1, 2, 0)) if mosaic.ndim == 3 else mosaic
        return wholeImage


class TIFFFile(ImageFile):

    def __init__(self, path):
        ImageFile.__init__(self, path)

    def imageDataFromPath(self):
        #todo better method that return every images if multipage
        tiffFileObject = tifffile.TiffFile(self.path)
        imageAsArray = tiffFileObject.asarray().astype(dtype="float32")
        self.__metadata = tiffFileObject.ome_metadata
        imageList = []
        for i in range(imageAsArray.shape[0]):
            imageList.append(imageAsArray[i])
        return imageAsArray


class PILFile(ImageFile):

    def __init__(self, path):
        ImageFile.__init__(self, path)

    def imageDataFromPath(self):
        image = PIL.Image.open(self.path)
        imageAsArray = np.array(image)
        return imageAsArray

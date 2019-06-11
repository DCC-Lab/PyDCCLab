from .cziUtil import *
from .channel import *


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
        out, self.__tilesWithChannelNumber = decodeImages(cziObj)
        out = np.squeeze(out)
        self.__numberOFChannels = out.shape[-3]
        closeCziFileObject(cziObj)
        wholeImage = out.transpose((1, 2, 0)) if out.ndim == 3 else out
        dtype = wholeImage.dtype
        normalizeValue = np.finfo(dtype).max if "float" in str(dtype) else np.iinfo(dtype).max
        return (wholeImage / normalizeValue).astype(np.float32)


class TIFFFile(ImageFile):

    def __init__(self, path):
        ImageFile.__init__(self, path)

    def imageDataFromPath(self):
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

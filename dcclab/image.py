from .channel import *
from .DCCExceptions import *
from .cziUtil import *
import tifffile
import PIL

import re


class Image:

    def __init__(self, path: str):
        self.__path = path

        self.fileObject = CZIFile(path)
        # for type in suppertedTypes:
        #   self.fileObject = objectFIle

        imageData = self.fileObject.imageDataFromPath()
        # self.__channels = self.channelsFromImageData(imageData)
        metaData = self.fileObject.metadata()

    @property
    def channels(self):
        return self.__channels

    def asChannelsArray(self):
        channelsPixels = list(map(lambda c: c.pixels, self.channels))
        return channelsPixels

    def asArray(self):
        channelArrays = self.asChannelsArray()
        imageData = np.dstack(channelArrays)
        return imageData

    def display(self, colorMap=None):
        plt.imshow(self.asArray(), cmap=colorMap)
        plt.show()

    def channelsFromImageData(self, imageData):
        if imageData.ndim == 2:
            return (Channel(imageData))
        elif imageData.ndim == 3:
            channelsData = np.squeeze(np.dsplit(imageData, imageData.shape[2]))
            channels = list(map(lambda pix: Channel(pix), channelsData))
            return channels

        return ()

    # def imageDataFromPath(self, path: str):
    #     cziPattern = r'\.czi\Z'
    #     tiffPattern = r"\.ti[f]{1,2}\Z"
    #     if re.search(cziPattern, path, re.IGNORECASE) is not None:
    #         imageData = self.imageDataFromCZI(path)
    #     elif re.search(tiffPattern, path, re.IGNORECASE) is not None:
    #         imageData = self.imageDataFromTIFF(path)
    #     else:
    #         imageData = self.imageDataFromAnyFile(path)
    #     return imageData.astype(np.float32)

    # def imageDataFromCZI(self, path):
    #     cziObj = readCziImage(path)
    #     imagesDirectory = cziObj.filtered_subblock_directory
    #     subblocks = cziObj.subblocks()
    #     imageData = cziObj.asarray()
    #     closeCziFileObject(cziObj)
    #     return imageData.astype(np.float32)

    # def imageDataFromTIFF(self, path):
    #     tiffFileObject = tifffile.TiffFile(path)
    #     imageData = tiffFileObject.asarray().astype(dtype="float32")
    #     # self.__metadata = tiffFileObject.ome_metadata
    #     return imageData.astype(np.float32)

    # def imageDataFromAnyFile(self, path: str):
    #     pilImage = PIL.Image.open(path)
    #     return np.array(pilImage, dtype=np.float32)


class ImageFile(object):
    def __init__(self, path):
        self.path = path
        # self.imageDataFromPath()

    def imageDataFromPath(self):
        return

    def metadata(self):
        return


class CZIFile(ImageFile):

    def __init__(self, path: str):
        ImageFile.__init__(self, path)

    def imageDataFromPath(self):
        cziObj = readCziImage(self.path)
        out, tilesWithChannelNumber = decodeImages(cziObj)
        self.__tiles = [Channel(tile[0], tile[1]) for tile in tilesWithChannelNumber]
        cziObj.close()


class TIFFFile(ImageFile):

    def imageDataFromPath(self):
        return

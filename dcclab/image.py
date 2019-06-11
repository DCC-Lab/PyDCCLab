from .channel import *
from .DCCExceptions import *
from .cziUtil import *
import tifffile
import PIL

import re


class Image:

    def __init__(self, path: str):
        self.path = path
        self.__channels = []
        try:
            imageData = self.imageDataFromPath(path)
            self.__channels = self.channelsFromImageData(imageData)
        except:
            raise ValueError("Not known format recognized for {0}".format(path))

    @property
    def shape(self):
        if len(self.channels) != 0:
            return self.channels[0].shape
    
    @property
    def channels(self):
        return self.__channels

    def removeChannels(self, channels):
        for index in channels:
            del self.channels[index]

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

    def imageDataFromPath(self, path: str):
        cziPattern = r'\.czi\Z'
        tiffPattern = r"\.ti[f]{1,2}\Z"
        if re.search(cziPattern, path, re.IGNORECASE) is not None:
            imageData = self.imageDataFromCZI(path)
        elif re.search(tiffPattern, path, re.IGNORECASE) is not None:
            imageData = self.imageDataFromTIFF(path)
        else:
            imageData = self.imageDataFromAnyFile(path)
        return imageData.astype(np.float32)

    def imageDataFromCZI(self, path):
        cziObj = readCziImage(path)
        imagesDirectory = cziObj.filtered_subblock_directory
        subblocks = cziObj.subblocks()
        imageData = cziObj.asarray()
        closeCziFileObject(cziObj)
        return imageData.astype(np.float32)

    def imageDataFromTIFF(self, path):
        tiffFileObject = tifffile.TiffFile(path)
        imageData = tiffFileObject.asarray().astype(dtype="float32")
        # self.__metadata = tiffFileObject.ome_metadata
        return imageData.astype(np.float32)

    def imageDataFromAnyFile(self, path: str):
        pilImage = PIL.Image.open(path)
        return np.array(pilImage, dtype=np.float32)

class ImageCZI(Image):
    def __init__(self, path):
        Image.__init__(self, path)

    def imageDataFromPath(self, path: str):
        try:
            cziObj = readCziImage(path)
            imagesDirectory = cziObj.filtered_subblock_directory
            subblocks = cziObj.subblocks()
            imageData = cziObj.asarray()
            closeCziFileObject(cziObj)
            return imageData.astype(np.float32)
        except:
            pass



if __name__ == '__main__':
    path = r"A:\injection AAV\résultats bruts\AAV\AAV493AAV498\AAV493AAV498_S51\AAV493AAV498_S51\S51-06.czi"
    path2 = r"A:\injection AAV\résultats bruts\AAV\AAV498AAV455\AAV498AAV455_S95\AAV498-455_S95_C-06.czi"
    path3 = r"A:\injection AAV\résultats bruts\AAV\AAV343\Jun109_AAV344a.tif"
    path4 = r"AAV498-455_S95_C-06.czi"
    path5 = r"S51-06.czi"
    im = Image(path)
    # im = Image(r"/tmp/test.tiff")
    # im2 = Image(r"/tmp/test2.png")
    # im2.display()

from .imageFile import *


class Image:

    def __init__(self, path: str):
        self.path = path
        self.__channels = []
        try:
            imageData = self.imageDataFromPath(path)
            self.__channels = self.channelsFromImageData(imageData)
        except:
            raise ValueError("Not known format recognized for {0}".format(path))

    def imageDataFromPath(self, path):
        imageData = None
        supportedClasses = [CZIFile, TIFFFile, PILFile]
        for supportedClass in supportedClasses:
            try:
                imageData = supportedClass(path).imageDataFromPath()
                break
            except:
                continue
        if imageData is None:
            raise ValueError
        return imageData

    @property
    def shape(self):
        if len(self.channels) != 0:
            return self.channels[0].shape

    @property
    def sizeInBytes(self) -> int:
        totalSize = 0
        for channel in self.channels:
            totalSize += channel.sizeInBytes
        return totalSize

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
            return Channel(imageData)
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

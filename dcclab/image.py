from .imageFile import *


class Image:
    supportedClasses = {CZIFile, TIFFFile, PILFile}

    def __init__(self, path: str):
        self.__path = path

        self.__fileObject = None
        imageData = None
        for fileClass in self.supportedClasses:
            try:
                self.__fileObject = fileClass(path)
                imageData = self.__fileObject.imageDataFromPath()
                break
            except:
                continue
        if self.__fileObject is None:
            raise InvalidFileFormatException("The file cannot be read. Please check if the format is supported.")

        self.__channels = self.channelsFromImageData(imageData)

    @property
    def path(self):
        return self.__path

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

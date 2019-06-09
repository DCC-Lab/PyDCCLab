from channel import *
import cziUtil
import re


class Image:

    def __init__(self, path: str):
        self.__path = path
        self.image = self.__findRightReader(path)
        if self.image.ndim == 2:
            self.__channels = (Channel(self.image))
        elif self.image.ndim == 3:
            self.__channels = (Channel(pix) for pix in self.image.dsplit())

    @property
    def channels(self):
        self.__channels

    @staticmethod
    def __findRightReader(path: str):
        cziPattern = r'\.czi\Z'
        tiffPattern = r"\.ti[f]{1,2}\Z"
        if re.search(cziPattern, path, re.IGNORECASE) is not None:
            image = _ImageFromCZIFile(path)
        elif re.search(tiffPattern, path, re.IGNORECASE) is not None:
            image = _ImageFromTIFFFile(path)
        else:
            image = _ImageFromOtherFile(path)
        return image


class _ImageFromCZIFile:

    def __init__(self, path: str):
        self.__cziObj = cziUtil.readCziImage(path)
        self.__imagesDirectory = self.__cziObj.filtered_subblock_directory
        self.__subblocks = self.__cziObj.subblocks()
        # if len(self.__imagesSubBlocks) > 50
        index = 0
        #for image in self.__subblocks:
         #   image.data()
          #  index += 1
           # print(index)
        print(self.__cziObj.shape)
        plt.imshow(self.__cziObj.asarray()[0, 0, 0, :, :, 0])
        plt.show()

    def __del__(self):
        cziUtil.closeCziFileObject(self.__cziObj)


class _ImageFromTIFFFile:
    import tifffile

    def __init__(self, path: str):
        tiffFileObject = self.tifffile.TiffFile(path)
        imagesAsArray = tiffFileObject.asarray().astype(dtype="float32")
        self.__metadata = tiffFileObject.ome_metadata


class _ImageFromOtherFile:
    from PIL import Image

    def __init__(self, path: str):
        image = self.Image.open(path)
        imageToArray = np.array(image, dtype=np.float32)


if __name__ == '__main__':
    path = r"A:\injection AAV\résultats bruts\AAV\AAV498AAV455\AAV498AAV455_S95\AAV498-455_S95_C-07.czi"
    im = Image(path)

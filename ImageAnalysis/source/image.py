from channel import *
import cziUtil
import re
import tifffile
import PIL

class Image:

    def __init__(self, path: str):
        self.__path = path
        pixels = self.imageArrayFromPath(path)
        if pixels.ndim == 2:
            self.__channels = (Channel(pixels))
        elif pixels.ndim == 3:
            self.__channels = (Channel(pix) for pix in np.dsplit(pixels, pixels.shape[2]) )

    @property
    def channels(self):
        self.__channels

    def imageArrayFromPath(self, path: str):
        cziPattern = r'\.czi\Z'
        tiffPattern = r"\.ti[f]{1,2}\Z"
        if re.search(cziPattern, path, re.IGNORECASE) is not None:
            pixels = self.imageArrayFromCZI(path)
        elif re.search(tiffPattern, path, re.IGNORECASE) is not None:
            pixels = self.imageArrayFromTIFF(path)
        else:
            pixels = self.imageArrayFromAnyFile(path)
        return pixels

    def imageArrayFromCZI(self, path):
        cziObj = cziUtil.readCziImage(path)
        imagesDirectory = cziObj.filtered_subblock_directory
        subblocks = cziObj.subblocks()
        pixels = cziObj.asarray()
        cziUtil.closeCziFileObject(cziObj)
        return pixels

    def imageArrayFromTIFF(self, path):
        tiffFileObject = tifffile.TiffFile(path)
        pixels = tiffFileObject.asarray().astype(dtype="float32")
        #self.__metadata = tiffFileObject.ome_metadata
        return pixels

    def imageArrayFromAnyFile(self, path: str):
        pilImage = PIL.Image.open(path)
        return np.array(pilImage, dtype=np.float32)


if __name__ == '__main__':
    path = r"A:\injection AAV\résultats bruts\AAV\AAV498AAV455\AAV498AAV455_S95\AAV498-455_S95_C-07.czi"
    im = Image(path)
    # im = Image(r"/tmp/test.tiff")
    # im2 = Image(r"/tmp/test.png")


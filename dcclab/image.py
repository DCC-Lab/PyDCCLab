from .channel import *
import cziUtil
import re
import tifffile
import PIL

class Image:

    def __init__(self, path: str):
        self.__path = path
        imageData = self.imageArrayFromPath(path)
        self.__channels = self.channelsFromImageData(imageData)

    @property
    def channels(self):
        return self.__channels

    def display(self, colorMap=None):
        channelsPixels = list(map( lambda c: c.pixels, self.channels))
        imageData = np.dstack(channelsPixels)
        plt.imshow(imageData, cmap=colorMap)
        plt.show()

    def channelsFromImageData(self, imageData):
        if imageData.ndim == 2:
            return (Channel(imageData))
        elif imageData.ndim == 3:
            channelsData = np.squeeze(np.dsplit(imageData, imageData.shape[2]))
            channels = list(map( lambda pix: Channel(pix), channelsData))
            return channels

        return ()

    def imageArrayFromPath(self, path: str):
        cziPattern = r'\.czi\Z'
        tiffPattern = r"\.ti[f]{1,2}\Z"
        if re.search(cziPattern, path, re.IGNORECASE) is not None:
            imageData = self.imageArrayFromCZI(path)
        elif re.search(tiffPattern, path, re.IGNORECASE) is not None:
            imageData = self.imageArrayFromTIFF(path)
        else:
            imageData = self.imageArrayFromAnyFile(path)
        return imageData.astype(np.float32)

    def imageArrayFromCZI(self, path):
        cziObj = cziUtil.readCziImage(path)
        imagesDirectory = cziObj.filtered_subblock_directory
        subblocks = cziObj.subblocks()
        imageData = cziObj.asarray()
        cziUtil.closeCziFileObject(cziObj)
        return imageData.astype(np.float32)

    def imageArrayFromTIFF(self, path):
        tiffFileObject = tifffile.TiffFile(path)
        imageData = tiffFileObject.asarray().astype(dtype="float32")
        #self.__metadata = tiffFileObject.ome_metadata
        return imageData.astype(np.float32)

    def imageArrayFromAnyFile(self, path: str):
        pilImage = PIL.Image.open(path)
        return np.array(pilImage, dtype=np.float32)


if __name__ == '__main__':
    path = r"A:\injection AAV\résultats bruts\AAV\AAV498AAV455\AAV498AAV455_S95\AAV498-455_S95_C-07.czi"
    im = Image(path)
    # im = Image(r"/tmp/test.tiff")
    # im2 = Image(r"/tmp/test2.png")
    # im2.display()


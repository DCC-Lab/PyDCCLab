from channel import *
import cziUtil
import re
import os
import time


class Image:

    def __init__(self, path: str):
        self.__path = path
        self.__image = self.__findRightReader(path)

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

    def getChannel(self, index: int):
        return self.__image.getChannel(index)


class _ImageFromCZIFile:

    def __init__(self, path: str):
        self.__fileOpened = True
        if os.path.getsize(path) > 1024 * 1024 * 2000:
            self.__fileOpened = False
            raise Exception("File too big to load.")
        self.__cziObj = cziUtil.readCziImage(path)
        out, self.__channels = cziUtil.decodeImages(self.__cziObj, max_workers=4)
        self.__fullImageMosaic = np.squeeze(out).astype(np.float32)
        self.__imageMosaics = self.__fullImageMosaic
        if self.__fullImageMosaic.ndim == 3:
            self.__imageMosaics = [Channel(self.__fullImageMosaic[x, :, :]) for x in range(3)]

    def getChannel(self, index: int) -> Channel:
        return self.__channels[index]

    def getImageMosaicAtChannel(self, channel: int):
        return self.__imageMosaics[channel]

    def __len__(self) -> int:
        return len(self.__channels)

    def __getitem__(self, item) -> Channel:
        return self.getChannel(item)

    def __del__(self):
        if self.__fileOpened:
            print("Closing")
            cziUtil.closeCziFileObject(self.__cziObj)


class _ImageFromTIFFFile:
    import tifffile

    def __init__(self, path: str):
        tiffFileObject = self.tifffile.TiffFile(path)
        series = tiffFileObject.series
        self.__channel = []
        for iterator in series:
            self.__channel.append(Channel(iterator.asarray().astype(np.float32)))
        self.__metadata = tiffFileObject.ome_metadata

    def getChannel(self, index: int) -> Channel:
        return self.__channel[index]


class _ImageFromOtherFile:
    from PIL import Image

    def __init__(self, path: str):
        image = self.Image.open(path)
        imageToArray = np.array(image, dtype=np.float32)



if __name__ == '__main__':
    path = r"A:\injection AAV\résultats bruts\AAV\AAV493AAV498\AAV493AAV498_S51\AAV493AAV498_S51\S51-06.czi"
    path2 = r"A:\injection AAV\résultats bruts\AAV\AAV498AAV455\AAV498AAV455_S95\AAV498-455_S95_C-06.czi"
    path3 = r"A:\injection AAV\résultats bruts\AAV\AAV343\Jun109_AAV344a.tif"
    path4 = r"AAV498-455_S95_C-06.czi"
    path5 = r"S51-06.czi"
    im = Image(path)

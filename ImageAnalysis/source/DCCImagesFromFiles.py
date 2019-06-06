from DCCImageCollection import DCCImageCollection as parent
import cziUtil as cziUtil
import tifffile
from DCCImage import DCCImage
import numpy as np
from DCCExceptions import *
import PIL.Image
import Database.CziMetadataManagement.metadata as meta


class DCCImagesFromCZIFile(parent):

    def __init__(self, path: str, numberOfImagesToRead: int = None):
        self.__path = path
        cziObject = cziUtil.readCziImage(path)
        arrayOfImages = cziUtil.getImagesFromCziFileObject(cziObject)
        # arrayOfImages = arrayOfImages.astype(np.float32)
        cziUtil.closeCziFileObject(cziObject)
        listOfImages = []
        if numberOfImagesToRead is None:
            for image in arrayOfImages:
                listOfImages.append(DCCImage(image.astype(np.float32)))
        else:
            for index in range(numberOfImagesToRead):
                print(index)
                listOfImages.append(DCCImage(arrayOfImages[index].astype(np.float32)))
        parent.__init__(self, listOfImages)

    def getMetadata(self) -> meta.Metadata:
        return meta.Metadata(self.__path)

    def getPath(self) -> str:
        return self.__path


class DCCImageFromNormalFile(DCCImage):
    def __init__(self, path: str):
        self.__path = path
        if path.lower().__contains__(".tiff") or path.lower().__contains__(".tif"):
            raise InvalidFileFormatException("To read tiff files, please use DCCImagesFromTiffFile.")
        elif path.lower().__contains__(".czi"):
            raise InvalidFileFormatException("To read czi files, please use DCCImagesFromCZIFile.")
        image = PIL.Image.open(path)
        imageToArray = np.array(image, dtype=np.float32)
        DCCImage.__init__(self, imageToArray)

    def getPath(self) -> str:
        return self.__path


class DCCImagesFromTiffFile(parent):
    def __init__(self, path: str):
        self.__path = path
        if not (path.lower().__contains__(".tiff") or path.lower().__contains__(".tif")):
            raise InvalidFileFormatException("Please use the right class to extract the image(s) form the file.")
        tiffFileObject = tifffile.TiffFile(path)
        imageAsArray = tiffFileObject.asarray().astype(dtype="float32")
        self.__metadata = tiffFileObject.ome_metadata
        imageList = []
        for i in range(imageAsArray.shape[0]):
            imageList.append(DCCImage(imageAsArray[i]))
        parent.__init__(self, imageList)

    def getMetadata(self) -> str:
        return self.__metadata

    def getPath(self) -> str:
        return self.__path

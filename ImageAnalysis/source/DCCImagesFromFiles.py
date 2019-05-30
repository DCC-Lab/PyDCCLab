from DCCImageCollection import *
import cziUtil as cziUtil
import tifffile
from DCCImage import *


class DCCImagesFromCZIFile(DCCImageCollection):

    def __init__(self, path: str):
        self.__path = path
        cziObject = cziUtil.readCziImage(path)
        arrayOfImages = cziUtil.getImagesFromCziFileObject(cziObject).astype(np.float32)
        listOfImages = []
        self.__metadata = cziUtil.extractMetadataFromCziFileObject(cziObject)
        cziUtil.closeCziFileObject(cziObject)
        for image in arrayOfImages:
            listOfImages.append(
                DCCImage(image, metadata=self.__metadata))  # Voir si pertinent que DCCImage ait un attribut metadata
        DCCImageCollection.__init__(self, listOfImages)

    def getMetadata(self) -> str:
        return self.__metadata

    def setMetadata(self, newMetadata: str) -> None:
        if not isinstance(newMetadata, str):
            raise TypeError("Metadata must be a string object")
        self.__metadata = newMetadata
        for image in self.asList():
            image.setMetadata(self.__metadata)

    def saveMetadata(self, filename: str) -> None:
        unacceptedChars = ["?", "/", "\\", "*", "<", ">", "|", ".", ","]
        filename = filename.strip()
        if len(filename) == 0 or filename.isspace() or any(char in filename for char in unacceptedChars):
            raise InvalidMetadataFileNameException
        with open("{}.xml".format(filename), "w", encoding="utf-8") as file:
            file.write(self.__metadata)

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


class DCCImagesFromTiffFile(DCCImageCollection):
    def __init__(self, path: str):
        self.__path = path
        if not (path.lower().__contains__(".tiff") or path.lower().__contains__(".tif")):
            raise InvalidFileFormatException("Please use the right class to extract the image(s) form the file.")
        tiffFileObject = tifffile.TiffFile(path)
        imageAsArray = tiffFileObject.asarray().astype(dtype="float32")
        self.__metadata = tiffFileObject.ome_metadata
        imageList = []
        for i in range(imageAsArray.shape[0]):
            imageList.append(DCCImage(imageAsArray[i], metadata=self.__metadata))
        DCCImageCollection.__init__(self, imageList)

    def getMetadata(self) -> str:
        return self.__metadata

    def setMetadata(self, newMetadata: str) -> None:
        if not isinstance(newMetadata, str):
            raise TypeError("Metadata must be a string object")
        self.__metadata = newMetadata

    def saveMetadata(self, filename: str) -> None:
        unacceptedChars = ["?", "/", "\\", "*", "<", ">", "|", ".", ","]
        filename = filename.strip()
        if len(filename) == 0 or filename.isspace() or any(char in filename for char in unacceptedChars):
            raise InvalidMetadataFileNameException
        with open("{}.xml".format(filename), "w") as file:
            file.write(self.__metadata)

    def getPath(self) -> str:
        return self.__path

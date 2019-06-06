from channel import *
import cziUtil
import re
from PyQt5.QtCore import *
import traceback


class Image:

    def __init__(self, path: str):
        self.__path = path
        self.image = self.__findRightReader(path)
        # Channel.__init__(self, self.__image)

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

    def __init__(self, path: str, nbOfWorkers: int = 1):
        self.__cziObj = cziUtil.readCziImage(path)
        self.__images = self.__cziObj.filtered_subblock_directory
        subListsOfImages = self.__split(self.__images, nbOfWorkers)
        self.__subblocks = self.__cziObj.subblocks()
        self.__workers = []
        for i in range(nbOfWorkers):
            self.__workers.append(_Worker(self.__decode, subListsOfImages[i]))

    def __decode(self, subList: list, statusSignal=None):
        pass


    def __del__(self):
        cziUtil.closeCziFileObject(self.__cziObj)

    @staticmethod
    def __split(originalList, numberOfSubLists):
        k, m = divmod(len(originalList), numberOfSubLists)
        return list(originalList[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(numberOfSubLists))


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


class _WorkerSignals(QObject):
    status = pyqtSignal(str)
    finished = pyqtSignal()


class _Worker(QRunnable):
    def __init__(self, workerFunction, *args, **kwargs):
        super(_Worker, self).__init__()

        self.function = workerFunction
        self.args = args
        self.kwargs = kwargs
        self.signals = _WorkerSignals()

        self.kwargs["statusSignal"] = self.signals.status

    @pyqtSlot()
    def run(self):
        try:
            self.function(*self.args, **self.kwargs)
        except Exception as e:
            print("ERROR: ", e)
            traceback.print_exc()
        finally:
            self.signals.finished.emit()


if __name__ == '__main__':
    path = r"A:\injection AAV\résultats bruts\AAV\AAV493AAV498\AAV493AAV498_S51\AAV493AAV498_S51\S51-06.czi"
    im = Image(path)

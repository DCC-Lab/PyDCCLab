from .cziMetadata import CZIMetadata
from .csvMetadata import CSVMetadata
import os
try:
    import deprecated
except:
    exit("pip install deprecated")


class ImageMetadata:
    supportedClasses = [CZIMetadata, CSVMetadata]
    supportedFormats = ['CZI', 'CSV']

    def __init__(self, path: str):
        if path is not None:
            if not os.path.exists(path):
                raise ValueError("Cannot load '{0}': file does not exist".format(path))

            self.path = path
            self.__fileObject = None
            for supportedClass in ImageMetadata.supportedClasses:
                try:
                    self.__fileObject = supportedClass(path)
                    break
                except:
                    continue
            if self.__fileObject is None:
                message = "Cannot read '{0}': not a recognized image format ({1})".format(self.path, ImageMetadata.supportedFormats)
                raise TypeError(message)
        else:
            self.path = None
            self.__fileObject = None

    @property
    def metadata(self) -> dict:
        if isinstance(self.__fileObject, CZIMetadata):
            return self.__fileObject.asDict().get('metadata')
        elif isinstance(self.__fileObject, CSVMetadata):
            return self.__fileObject.asDict
        else:
            return {}

    @property
    def channels(self) -> dict:
        if isinstance(self.__fileObject, CZIMetadata):
            return self.__fileObject.asDict().get('channels')
        else:
            return {}

    @property
    def keys(self) -> dict:
        if isinstance(self.__fileObject, CZIMetadata):
            return self.__fileObject.keys
        elif isinstance(self.__fileObject, CSVMetadata):
            return self.__fileObject.keys
        else:
            return {}

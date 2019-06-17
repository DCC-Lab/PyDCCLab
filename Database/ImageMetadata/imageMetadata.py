from Database.ImageMetadata import CZIMetadata
import os
try:
    import deprecated
except:
    exit("pip install deprecated")

class ImageMetadata:
    supportedClasses = [CZIMetadata]
    supportedFormats = ['CZI']

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
        else:
            return {}

    @property
    def channels(self) -> dict:
        if isinstance(self.__fileObject, CZIMetadata):
            return self.__fileObject.asDict().get('channels')
        else:
            return {}

    @deprecated("Renamed metadata: a property is never named getXXX")
    @property
    def getMetadata(self) -> dict:
        return metadata

    @deprecated("Renamed channels: a property is never named getXXX")
    @property
    def getChannels(self) -> dict:
        return self.channels



if __name__ == '__main__':
    # Some scratch tests :  # TODO To delete when the class is completed. This is only for quick tests.
    path = 'P:\\injection AAV\\résultats bruts\\AAV\\AAV498AAV455\\AAV498AAV455_S94\\AAV498-455_S94_C.czi'
    mdata = ImageMetadata(path)
    for key, value in mdata.getMetadata.items():
        print(key, value)

    for key, value in mdata.getChannels.items():
        print(key, value)
        for subkey, subvalue in value.items():
            print(subkey, subvalue)

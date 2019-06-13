from .cziMetadata.cziMetadata import CZIMetadata
import os


class ImageMetadata:
    supportedClasses = [CZIMetadata]
    supportedFormats = ['CZI']

    def __init__(self, path: str):
        if not os.path.exists(path):
            raise ValueError("Cannot load '{0}': file does not exist".format(path))

        self.path = path
        self.__fileObject = None
        self.__fileType = None
        for supportedClass in ImageMetadata.supportedClasses:
            try:
                self.__fileObject = supportedClass(path)
                self.__fileType = type(self.__fileObject)
                break
            except:
                continue
        if self.__fileObject is None:
            message = "Cannot read '{0}': not a recognized image format ({1})".format(self.path, ImageMetadata.supportedFormats)
            raise TypeError(message)


if __name__ == '__main__':
    # Some scratch tests :  # TODO To delete when the class is completed. This is only for quick tests.
    print('Hello World')

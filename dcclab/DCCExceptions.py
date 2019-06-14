class ImageNotInCollectionException(Exception):
    def __init__(self):
        Exception.__init__(self, "The image is not present in the collection.")


class ImageAlreadyInCollectionException(Exception):
    def __init__(self):
        Exception.__init__(self, "The image is already in the collection.")


class DimensionException(Exception):
    def __init__(self, dimensions):
        Exception.__init__(self, "Cannot accept {} dimensions arrays.".format(dimensions))


class PixelTypeException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class InvalidEqualityTestException(Exception):
    def __init__(self, otherType):
        Exception.__init__(self, "Can't compare equality of a DCCImage instance and {}.".format(otherType))


class NotDCCImageException(Exception):
    def __init__(self):
        Exception.__init__(self, "Attribute must be a DCCImage instance.")


class InvalidImageNameException(Exception):
    def __init__(self):
        Exception.__init__(self, "The given name/filename is invalid.")


class InvalidMetadataFileNameException(Exception):
    def __init__(self):
        Exception.__init__(self, "The given filename is invalid.")


class InvalidFileFormatException(Exception):
    def __init__(self, message: str):
        Exception.__init__(self, message)


class NotBinaryImageException(Exception):
    def __init__(self):
        Exception.__init__(self, "The image must be in binary format (only black and white pixels).")

class EmptyDCCImageCollectionException(Exception):
    def __init__(self):
        Exception.__init__(self, "There are no images in the collection.")

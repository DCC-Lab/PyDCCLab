class ImageNotInStackException(Exception):
    def __init__(self):
        Exception.__init__(self, "The image is not present in the stack.")


class ImageAlreadyInStackException(Exception):
    def __init__(self):
        Exception.__init__(self, "The image is already in the stack.")


class ImageDimensionsException(Exception):
    def __init__(self, dimensions):
        Exception.__init__(self, "Cannot accept {} dimensions arrays.".format(dimensions))


class PixelTypeException(Exception):
    def __init__(self):
        Exception.__init__(self, "Pixels type must be 32 bits float.")


class InvalidEqualityTest(Exception):
    def __init__(self, otherType):
        Exception.__init__(self, "Can't compare equality of a DCCImage instance and {}.".format(otherType))

class NotDCCImageException(Exception):
    def __init__(self):
        Exception.__init__(self, "Attribute must be a DCCImage instance.")

class InvalidImageName(Exception):
    def __init__(self):
        Exception.__init__(self, "The given name/filename is invalid.")

from .channel import *
from .channelFloat import ChannelFloat


class ChannelInt(Channel):

    def __init__(self, pixels: np.ndarray):
        Channel.__init__(self, pixels)
        if "int" not in str(pixels.dtype):
            raise TypeError("Pixel type must be integer.")
        self.__originalFactor = np.iinfo(self.__originalDType).max

    def convertToNormalizedFloat(self):
        # For a bound integer array, we take the maximum of the type
        # and we convert the array to float
        floatArray = np.copy(self.pixels).astype(np.float32)
        return ChannelFloat(floatArray / self.__originalFactor)

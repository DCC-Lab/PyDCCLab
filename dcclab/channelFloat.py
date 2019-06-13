from .channel import *
from .channelInteger import ChannelInt


class ChannelFloat(Channel):

    def __init__(self, pixels: np.ndarray):
        if "float" not in str(pixels.dtype):
            raise TypeError("Pixel type must be integer.")
        maxValue = np.max(pixels)
        if maxValue <= 1.0:
            self.__originalFactor = 1.0
            normalizedPixels = np.copy(pixels)
        else:
            self.__originalFactor = maxValue
            normalizedPixels = np.copy(pixels) / maxValue
        Channel.__init__(self, normalizedPixels)

    def convertTo8BitsInteger(self):
        if self.__originalFactor <= 255:
            newPixels = (np.copy(self.pixels) * 255).astype(np.uint8)
        else:
            newPixels = np.copy(self.pixels)
            newPixels[newPixels >= 256] = 255
        return ChannelInt(newPixels.astype(np.uint8))

    def convertTo16BitsInteger(self):
        maxValue = 2 ** 16
        if self.__originalFactor <= (maxValue - 1):
            newPixels = (np.copy(self.pixels) * (maxValue - 1))
        else:
            newPixels = np.copy(self.pixels)
            newPixels[newPixels >= maxValue] = maxValue - 1
        return ChannelInt(newPixels.astype(np.uint8))

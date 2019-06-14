from .channel import *


class ChannelFloat(Channel):

    def __init__(self, pixels: np.ndarray):
        if "float" not in str(pixels.dtype):
            raise TypeError("Pixel type must be float.")
        maxValue = np.max(pixels)
        if maxValue <= 1.0:
            self.__originalFactor = 1.0
            normalizedPixels = np.copy(pixels)
        else:
            self.__originalFactor = maxValue
            normalizedPixels = np.copy(pixels) / maxValue
        Channel.__init__(self, normalizedPixels)

    def convertTo8BitsInteger(self):
        from .channelInteger import ChannelUint8
        if self.__originalFactor <= 255:
            newPixels = (np.copy(self.pixels) * 255).astype(np.uint8)
        else:
            newPixels = np.copy(self.pixels) / np.max(self.pixels) * 255
        return ChannelUint8(newPixels.astype(np.uint8))

    def convertTo16BitsInteger(self):
        from .channelInteger import ChannelUint16
        maxValue = 2 ** 16
        if self.__originalFactor <= (maxValue - 1):
            newPixels = (np.copy(self.pixels) * (maxValue - 1))
        else:
            newPixels = np.copy(self.pixels) / np.max(self.pixels) * maxValue - 1
        return ChannelUint16(newPixels.astype(np.uint16))

    def getEntropyFiltering(self, filterSize: int):
        # We have to cast image in 8 bits uint because the algorithm seems to properly work only in this type
        pixels = self.convertTo8BitsInteger().pixels
        entropyFiltered = entropy(pixels, morphology.selem.square(filterSize, dtype=np.float32))
        return Channel(entropyFiltered.astype(np.float32))

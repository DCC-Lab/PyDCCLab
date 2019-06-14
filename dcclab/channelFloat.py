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
        newPixels = (np.copy(self.pixels) * 255).astype(np.uint8)
        return Channel(newPixels.astype(np.uint8))

    def convertTo16BitsInteger(self):
        newPixels = ((np.copy(self.pixels)) * (2 ** 16 - 1)).astype(np.uint16)
        return Channel(newPixels.astype(np.uint16))

    def getEntropyFiltering(self, filterSize: int):
        # We have to cast image in 8 bits uint because the algorithm seems to properly work only in this type
        pixels = self.convertTo8BitsInteger().pixels
        entropyFiltered = entropy(pixels, morphology.selem.square(filterSize, dtype=np.float32))
        return Channel(entropyFiltered.astype(np.float32))

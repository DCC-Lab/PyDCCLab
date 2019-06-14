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

    def getHistogramValues(self, normed: bool = False) -> typing.Tuple[np.ndarray, np.ndarray]:
        pixels = self.convertTo8BitsInteger().pixels
        array = pixels.ravel()
        nbBins = len(np.bincount(array))
        hist, bins = np.histogram(array, nbBins, [0, nbBins], density=normed)
        return hist, bins

    def convertTo8BitsInteger(self):
        return self.convertToUnsignedInt(np.uint8)

    def convertTo16BitsInteger(self):
        return self.convertToUnsignedInt(np.uint16)

    def getEntropyFiltering(self, filterSize: int):
        # We have to cast image in 8 bits uint because the algorithm seems to properly work only in this type
        pixels = self.convertTo8BitsInteger().pixels
        entropyFiltered = entropy(pixels, morphology.selem.square(filterSize, dtype=np.float32))
        return Channel(entropyFiltered.astype(np.float32))

    def convertToUnsignedInt(self, dtype):
        convertedArray = ((np.copy(self.pixels)) * np.iinfo(dtype).max)
        return Channel(convertedArray.astype(dtype))

import numpy as np
import math


class HalfWidthAtHalfMaximumOneDimension:

    def __init__(self, data: np.ndarray, maximum: float = None, positiveSlopeSideOfPeak: bool = None):
        # If no maximum is provided, taking the maximal value of data. Else, taking the provided one.
        # if positiveSlopeSideOfPeak is not None: assumes there is only half of the central peak, either the increasing
        # side (arg is True) or the decreasing one (arg is False).
        # Else, the algorithm takes the left left side of the peak.
        if maximum is None:
            maximum = np.max(data)
        self.maximum = maximum
        if positiveSlopeSideOfPeak is None:
            data = data[:np.argmax(data)]
            positiveSlopeSideOfPeak = True
        if not isinstance(data, np.ndarray):
            raise TypeError("The data must be within a numpy array.")
        if data.ndim != 1:
            raise ValueError("The data must be in one dimension.")
        self.__data = data
        self.__sideOfPeak = "left" if positiveSlopeSideOfPeak else "right"
        self.report = None

    def findHWHMWithinError(self, error=0.05):
        halfMax = self.maximum / 2
        inferiorBound = halfMax - halfMax * error
        superiorBound = halfMax + halfMax * error
        pointsForHWHM = np.where((self.__data >= inferiorBound) & (self.__data <= superiorBound))[0]
        nbPoints = len(pointsForHWHM)
        if nbPoints == 0:
            raise ValueError("The error is too small. Not enough values were found to compute the HWHM.")
        mean = np.mean(pointsForHWHM)
        left = 0
        right = mean
        if self.__sideOfPeak == "left":
            left = mean
            right = len(self.__data)
        HWHM = right - left
        self.report = self._errorStatsReport(pointsForHWHM)
        return HWHM

    def findHWHMWithLinearFit(self, maxNbPoints: int = 3, moreInUpperPart: bool = True):
        if maxNbPoints < 2:
            raise ValueError("There should be at least 2 points for the linear fit.")
        halfMax = self.maximum / 2
        halfK = maxNbPoints / 2
        upperKs = math.ceil(halfK)
        lowerKs = math.floor(halfK)
        if not moreInUpperPart:
            temp = upperKs
            upperKs = lowerKs
            lowerKs = temp
        lows, highs, lIndices, hIndices = splitInTwoWithMiddleValue(halfMax, self.__data, True)
        lows = lows[:lowerKs]
        highs = highs[-upperKs:]
        lIndices = lIndices[:lowerKs]
        hIndices = hIndices[-upperKs:]
        if self.__sideOfPeak == "left":
            lows = lows[-lowerKs:]
            highs = highs[:upperKs]
            lIndices = lIndices[-lowerKs:]
            hIndices = hIndices[:upperKs]
        xData = np.append(lIndices, hIndices)
        yData = np.append(lows, highs)
        (slope, zero), covMat = np.polyfit(xData, yData, 1, full=False,
                                           cov=True)
        left = findXWithY(halfMax, slope, zero)
        right = len(self.__data)
        if self.__sideOfPeak == "right":
            right = findXWithY(halfMax, slope, zero)
            left = 0
        HWHM = right - left
        self.report = self._linearFitStatsReport(xData, slope, zero, covMat)
        return HWHM

    def _errorStatsReport(self, dataUsed: np.ndarray):
        nbPoints = len(dataUsed)
        mean = np.mean(dataUsed)
        stdDev = np.std(dataUsed)
        report = f"HWHM error method: {mean} average, {stdDev} standard deviation, {nbPoints} points used."
        return report

    def _linearFitStatsReport(self, dataUsed: np.ndarray, slope: float, zero: float, covMat: np.ndarray):
        nbPoints = len(dataUsed)
        slopeError, zeroError = np.diag(covMat) ** 0.5
        report = f"HWHM linear fit method: {nbPoints} points used, "
        report += f"({slope} ± {slopeError}) slope, ({zero} ± {zeroError}) error\n"
        report += "*uncertainty is taken as the square root of the fit's covariance matrix diagonal*"
        return report


class FullWidthAtHalfMaximumOneDimension(HalfWidthAtHalfMaximumOneDimension):

    def __init__(self, data: np.ndarray, maximum: float = None):
        super(FullWidthAtHalfMaximumOneDimension, self).__init__(data, maximum)

    def findFWHMWithinError(self, error: float = 0.05):
        HWHM = self.findHWHMWithinError(error)
        return 2 * HWHM

    def findFWHMWithLinearFit(self, maxNbPoints: int = 3, moreInUpperPart: bool = True):
        HWHM = self.findHWHMWithLinearFit(maxNbPoints, moreInUpperPart)
        return 2 * HWHM


def splitInTwoWithMiddleValue(middleValue: float, array: np.ndarray, returnIndices: bool = False):
    # Assumes the values are only increasing or decreasing, not both.
    # Excludes the middle value
    upper = np.ravel(np.where(array > middleValue))  # Doesn't change anything since 1D data
    lower = np.ravel(np.where(array < middleValue))  # Doesn't change anything since 1D data
    lowerValues = array[lower]
    upperValues = array[upper]
    if not returnIndices:
        return lowerValues, upperValues
    return lowerValues, upperValues, lower, upper


def linearEquation(y1, y2, x1, x2):
    deltaY = y2 - y1
    deltaX = x2 - x1
    slope = deltaY / deltaX
    zero = y1 - slope * x1
    return slope, zero


def findXWithY(y, slope, zero):
    x = (y - zero) / slope
    return x

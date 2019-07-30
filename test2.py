import dcclab as dcc
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import typing


def createXYGridsFromArray(array: np.ndarray, gridOriginAtCenter: bool = True) -> typing.Tuple[
    np.ndarray, np.ndarray]:
    shape = array.shape
    y, x = np.indices(shape)
    if gridOriginAtCenter:
        y, x = np.flipud(y - np.max(y) // 2), x - np.max(x) // 2
    return x, y


def generateCircles(arrayShape: typing.Tuple[int, int], nbCircles: int, radiusAvg: float, radiusStdDev: float):
    array = np.zeros(arrayShape)
    radii = []
    positions = set()
    while len(positions) < nbCircles:
        tempRadius = np.random.normal(radiusAvg, radiusStdDev)
        tempRadius = abs(int(np.ceil(tempRadius)))
        tempX = np.random.choice(range(arrayShape[0] + 1))
        tempY = np.random.choice(range(arrayShape[1] + 1))
        positions.add((tempX, tempY))
        radii.append(tempRadius)

    for i in range(nbCircles):
        cv.circle(array, positions.pop(), radii[-(i + 1)], 1, -2)
    return array


def checkpoint(h, k, x, y, a, b, angle):
    cos = np.cos(angle)
    sin = np.sin(angle)
    return (((x - h) * cos - (y - k) * sin) ** 2) / a ** 2 + (
            ((x - h) * sin + (y - k) * cos) ** 2) / b ** 2


def addCirclesInEllipse(arrayShape: typing.Tuple[int, int], radiusAvg: float, radiusStdDev: float, nbCircles: int,
                        angle: float, center: typing.Tuple[int, int],
                        ellipseShape: typing.Tuple[int, int]):
    array = np.zeros(arrayShape)
    x, y = createXYGridsFromArray(array, False)
    cos = np.cos(angle)
    sin = np.sin(angle)
    a, b = ellipseShape
    centerX, centerY = center
    mask = (((x - centerX) * cos - (y - centerY) * sin) ** 2) / a ** 2 + (
            ((x - centerX) * sin + (y - centerY) * cos) ** 2) / b ** 2 <= 1
    array = mask.astype(np.uint8)
    radii = []
    positions = set()
    x, y = np.where(array > 0)
    x = np.squeeze(x)
    y = np.squeeze(y)

    while len(positions) < nbCircles:
        tempRadius = np.random.normal(radiusAvg, radiusStdDev)
        tempRadius = abs(int(np.ceil(tempRadius)))
        tempX = np.random.choice(x)
        tempY = np.random.choice(y)
        if checkpoint(centerX, centerY, tempX + tempRadius, tempY + tempRadius, a, b, angle) < 1 and checkpoint(
                centerX, centerY, tempX - tempRadius, tempY - tempRadius, a, b, angle) < 1:
            positions.add((tempX, tempY))
            radii.append(tempRadius)

    for i in range(nbCircles):
        cv.circle(array, positions.pop(), radii[-(i + 1)], 2, -2)
    return array


def generateFiberLikeStructures(arrayShape: typing.Tuple[int, int], avgLength: float, avgThickness: float,
                                avgAngle: float,
                                stdDevLength: float, stdDevThicksness: float, stdDevAngle: float,
                                nbLines: int):
    array = np.zeros(arrayShape)
    possibleX = range(arrayShape[0] // 2 - arrayShape[0] // 4, arrayShape[0] // 2 + arrayShape[0] // 4)
    possibleY = range(arrayShape[1] // 2 - arrayShape[1] // 4, arrayShape[1] // 2 + arrayShape[1] // 4)
    points1 = set()
    points = []
    thicknesses = []
    while len(points1) < nbLines:
        randomAdditionX = np.random.choice(range(-arrayShape[0] // 4, arrayShape[0] // 4))
        randomAdditionY = np.random.choice(range(-arrayShape[1] // 4, arrayShape[1] // 4))
        p1X = np.random.choice(possibleX) + randomAdditionX
        p1Y = np.random.choice(possibleY) + randomAdditionY
        p1 = (p1X, p1Y)
        points1.add(p1)

    for point in points1:
        length = np.random.normal(avgLength, stdDevLength)
        length = int(np.ceil(abs(length)))
        angle = np.random.normal(avgAngle, stdDevAngle)
        angle = int(np.ceil(abs(angle)))
        thickness = np.random.normal(avgThickness, stdDevThicksness)
        thickness = int(np.ceil(abs(thickness)))
        xLength = int(np.round(length * np.cos(angle)))
        yLength = int(np.round(length * np.sin(angle)))
        point2 = (point[0] + xLength, point[1] + yLength)
        points.append((point, point2))
        thicknesses.append(thickness)

    for i in range(nbLines):
        ptX, ptY = points[i]
        cv.line(array, ptX, ptY, 1, thicknesses[i])
    return array


def generateMoreRealistFiberStructures(arrayShape: typing.Tuple[int, int], avgRootLength: float,
                                       stdDevRootLength: float,
                                       avgBifurcation: float, stdDevBifurcation: float, avgThickness: float,
                                       stdDevThickness: float,
                                       avgBifurcationLength: float, stdDevBifurcationLength: float, avgRootAngle: float,
                                       stdDevRootAngle: float, avgBifurcationAngle: float,
                                       stdDevBifurcationAngle: float, nbRoots: int):
    array = np.zeros(arrayShape)
    possibleX = range(arrayShape[0] // 2 - arrayShape[0] // 4, arrayShape[0] // 2 + arrayShape[0] // 4)
    possibleY = range(arrayShape[1] // 2 - arrayShape[1] // 4, arrayShape[1] // 2 + arrayShape[1] // 4)
    rootsBegin = set()

    while len(rootsBegin) < nbRoots:
        randomAdditionX = np.random.choice(range(-arrayShape[0] // 4, arrayShape[0] // 4))
        randomAdditionY = np.random.choice(range(-arrayShape[1] // 4, arrayShape[1] // 4))
        p1X = np.random.choice(possibleX) + randomAdditionX
        p1Y = np.random.choice(possibleY) + randomAdditionY
        p1 = (p1X, p1Y)
        rootsBegin.add(p1)

    for root in rootsBegin:
        rootLength = int(np.ceil(np.random.normal(avgRootLength, stdDevRootLength)))
        nbBifurcations = int(np.ceil(np.random.normal(avgBifurcation, stdDevBifurcation)))
        rootAngle = np.random.normal(avgRootAngle, stdDevRootAngle)
        rootEndX = int(np.round(np.cos(rootAngle) * rootLength)) + root[0]
        rootEndY = int(np.round(np.sin(rootAngle) * rootLength)) + root[1]
        rootThickness = int(np.ceil(abs(np.random.normal(avgThickness, stdDevThickness))))
        rootEnd = (rootEndX, rootEndY)
        cv.line(array, root, rootEnd, 1, rootThickness)
        for _ in range(nbBifurcations):
            bifurcationLength = int(np.ceil(np.random.normal(avgBifurcationLength, stdDevBifurcationLength)))
            bifurcationAngle = np.random.normal(avgBifurcationAngle, stdDevBifurcationAngle)
            bifurcationEndX = int(np.round(np.cos(bifurcationAngle) * bifurcationLength)) + rootEnd[0]
            bifurcationEndY = int(np.round(np.sin(bifurcationAngle) * bifurcationLength)) + rootEnd[1]
            bifurcationThickness = int(np.ceil(abs(np.random.normal(avgThickness, stdDevThickness))))
            bifurcationEnd = (bifurcationEndX, bifurcationEndY)
            cv.line(array, rootEnd, bifurcationEnd, 1, bifurcationThickness)

    return array


def otherFiberMethod(arrayShape: typing.Tuple[int, int], avgLength: float, stdDevLength: float, avgThickness: float,
                     stdDevThickness: float, avgSpacing: float, stdDevSpacing: float, avgAngle: float,
                     stdDevAngle: float, nbLines: int):
    spacings = np.abs(np.random.normal(avgSpacing, stdDevSpacing, nbLines)).astype(np.uint16)
    startingX = np.round(np.cumsum(np.zeros((nbLines,)) + spacings)).astype(np.uint16)
    startingY = np.abs(np.random.normal(arrayShape[1] // 8, arrayShape[1] // 16, nbLines)).astype(np.uint16)
    startingPoints = zip(startingX, startingY)
    lengths = np.abs(np.random.normal(avgLength, stdDevLength, nbLines)).astype(np.uint16)
    thicknesses = np.ceil(np.abs(np.random.normal(avgThickness, stdDevThickness, nbLines))).astype(np.uint8)
    angles = np.random.choice(np.arange(92 / 180 * np.pi, 98 / 180 * np.pi, 0.005),
                              nbLines)
    finishingPosX = (np.cos(angles) * lengths).astype(int) + startingX
    finishingPosY = (np.sin(angles) * lengths).astype(int) + startingY
    finishingPoints = zip(finishingPosX, finishingPosY)
    array = np.zeros(arrayShape)
    for initialPoints, finalPoints, thickness in zip(startingPoints, finishingPoints, thicknesses):
        cv.line(array, initialPoints, finalPoints, 1, thickness)

    return array


if __name__ == '__main__':
    # path = r"A:\injection AAV\résultats bruts\AAV\AAV400-401\2019-04-12\AAV400+CRE_neurones_antimcherry_antiRabit488-02.czi"
    # path = r"C:\Users\goubi\PycharmProjects\BigData-ImageAnalysis\dcclab\tests\testData\testCziFile.czi"
    # czi = dcc.CZIFile(path)
    # image = czi.imageData()
    # channelEGFP = image[0]  # image[1]
    # bin = channelEGFP.getOtsuThresholding()
    # closed = bin.getBinaryClosing(3)
    # watershed = channelEGFP.watershedSegmentation()
    # # dcc.Channel.multiChannelDisplay([channelEGFP, bin, closed])
    # # exit()
    # channelEGFP.displayPowerSpectrum()
    # channelEGFP.displayPowerSpectrumAzimuthalAverage(2)

    # czi = dcc.CZIFile(r"A:\injection AAV\résultats bruts\AAV\AAV543AAV478\AAV543AAV478_S61\S61-2.czi")
    # czi2 = dcc.CZIFile(r"A:\injection AAV\résultats bruts\AAV\AAV543AAV478\AAV543AAV478_S61\S61-4.czi")
    # czi3 = dcc.CZIFile(r"A:\injection AAV\résultats bruts\AAV\AAV534\AAV534_patte\AAV534.czi")
    # image = czi.imageData()
    # channelEGFP = image[1]
    # channelMCherry = image[-1]
    # dcc.Channel.multiChannelDisplay([channelEGFP, channelMCherry])
    # channelEGFP.displayPowerSpectrum()
    # channelMCherry.displayPowerSpectrum()
    # ps1DM_ = channelMCherry.powerSpectrumAzimuthalAverage()
    # ps1DE_ = channelEGFP.powerSpectrumAzimuthalAverage()
    # x_ = range(len(ps1DE_))
    # plt.plot(x_, ps1DE_, label="EGFP", color="green")
    # plt.plot(x_, ps1DM_, label="mCherry", color="red")
    # plt.legend()
    # plt.yscale("log", basey=2)
    # plt.show()
    # exit()
    # image = czi2.imageData()
    # channelEGFP = image[1]
    # channelMCherry = image[-1]
    # dcc.Channel.multiChannelDisplay([channelEGFP, channelMCherry])
    # channelEGFP.displayPowerSpectrum()
    # channelMCherry.displayPowerSpectrum()
    # ps1DM_1 = channelMCherry.powerSpectrumAzimuthalAverage()
    # ps1DE_1 = channelEGFP.powerSpectrumAzimuthalAverage()
    # x_1 = range(len(ps1DE_1))
    # plt.plot(x_1, ps1DE_1, label="EGFP", color="green")
    # plt.plot(x_1, ps1DM_1, label="mCherry", color="red")
    # plt.legend()
    # plt.yscale("log", basey=2)
    # plt.show()
    # image = czi3.imageData()
    # channelEGFP = image[0]
    # channelMCherry = image[-1]
    # dcc.Channel.multiChannelDisplay([channelEGFP, channelMCherry])
    # channelEGFP.displayPowerSpectrum()
    # channelMCherry.displayPowerSpectrum()
    # ps1DM = channelMCherry.powerSpectrumAzimuthalAverage()
    # ps1DE = channelEGFP.powerSpectrumAzimuthalAverage()
    # x = range(len(ps1DE))
    # plt.plot(x, ps1DE, label="EGFP", color="green")
    # plt.plot(x, ps1DM, label="mCherry", color="red")
    # plt.plot(x_, ps1DE_, label="EGFP Nice image", color="yellow")
    # plt.plot(x_, ps1DM_, label="mCherry Nice image", color="pink")
    # plt.plot(x_1, ps1DE_1, label="EGFP Nice image 2", color="blue")
    # plt.plot(x_1, ps1DM_1, label="mCherry Nice image 2", color="black")
    # plt.legend()
    # plt.yscale("log", basey=2)
    # plt.show()
    # print("Pizza time!")
    otherArray = np.random.randint(0, 10, (1000, 1000))
    im = dcc.Image(imageData=otherArray)
    channel = im[0]
    channel.powerSpectrumAngularAverage()
    exit()
    array = generateCircles((1000, 1000), 100, 8, 2)
    array[-1, -1] = 10
    # array = addCirclesInEllipse((1400, 1500), 8, 2, 100, 0, (713, 697), (700, 500))
    channel = dcc.Image(array)[0]
    channel.display()
    channel.displayPowerSpectrum()
    channel.displayPowerSpectrumAzimuthalAverage(2)
    channel = channel.getGaussianFilter(5)
    noisyChannel = channel.applyGaussianNoise(0.8, 0)
    noisyChannel.display()
    noisyChannel.displayPowerSpectrum()
    ncps1d = noisyChannel.powerSpectrumAzimuthalAverage()
    ps1d = channel.powerSpectrumAzimuthalAverage()
    x = range(len(ps1d))
    plt.plot(x, ps1d, label="No noise")
    plt.plot(x, ncps1d, label="Noise")
    plt.legend()
    plt.yscale("log", basey=2)
    plt.show()

    exit()
    w = noisyChannel.watershedSegmentation()
    print(w[1])
    dcc.Channel.multiChannelDisplay([channel, noisyChannel, w[0]], ["gray", "gray", "gist_ncar"])
    array = otherFiberMethod((1000, 1000), 700, 70, 3, 2, 10, 2, np.pi / 2, np.pi / 4, 100)
    channel = dcc.Channel(array)
    channel.display()
    channel.displayPowerSpectrum()
    channel.displayPowerSpectrumAzimuthalAverage(50)
    array10 = generateMoreRealistFiberStructures((1000, 1000), 300, 100, 3, 2, 2, 2, 125, 25, 0, 2 * np.pi, 0, np.pi,
                                                 10)
    array5 = generateMoreRealistFiberStructures((1000, 1000), 300, 100, 3, 2, 2, 2, 125, 25, 0, 2 * np.pi, 0, np.pi,
                                                5)
    array10_2 = generateFiberLikeStructures((1000, 1000), 300, 2, 0, 100, 2, 2 * np.pi, 10)
    array5_2 = generateFiberLikeStructures((1000, 1000), 300, 2, 0, 100, 2, 2 * np.pi, 5)
    channel10 = dcc.Channel(array10)
    channel5 = dcc.Channel(array5)
    channel10_2 = dcc.Channel(array10_2)
    channel5_2 = dcc.Channel(array5_2)
    channel5.display()
    dcc.Channel.multiChannelDisplay([channel5, channel10, channel5_2, channel10_2])
    channel5.displayPowerSpectrum()
    channel10.displayPowerSpectrum()
    channel5_2.displayPowerSpectrum()
    channel10_2.displayPowerSpectrum()
    ps1D5 = channel5.powerSpectrumAzimuthalAverage()
    ps1D10 = channel10.powerSpectrumAzimuthalAverage()
    ps1D5_2 = channel5_2.powerSpectrumAzimuthalAverage()
    ps1D10_2 = channel10_2.powerSpectrumAzimuthalAverage()
    x = range(len(ps1D5))
    plt.plot(x, ps1D5, label="5 roots")
    plt.plot(x, ps1D10, label="10 roots")
    plt.plot(x, ps1D5_2, label="5 not roots")
    plt.plot(x, ps1D10_2, label="10 not roots")
    plt.legend()
    plt.yscale("log", basey=10)
    plt.show()

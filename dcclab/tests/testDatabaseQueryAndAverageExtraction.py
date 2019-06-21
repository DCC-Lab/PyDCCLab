import env
from dcclab import Image, cziUtil
import os

# For this test, the query was done by Mathieu on his computer. Selected channel is mCherry
if __name__ == '__main__':
    listOfAverages = []
    listOfStdDev = []

    readQuery = open(r"querry_mcher.csv", "r",
                     encoding="utf-8")

    writeResults = open(r"querry_mcher_results.csv",
                        "a", encoding="utf-8")

    lines = readQuery.readlines()
    numberOfFiles = len(lines)

    startIndex = 0
    if startIndex == 0:
        writeResults.write(
            "WARNING: The czi file reader is only capable of properly reading single image (mutli or mono channel). "
            "If it is a z-stack or any other multi image file, it will be ignored.")
    for i in range(startIndex, len(lines)):
        path, channelNumber = lines[i].split(",")
        pathChanged = path.replace("P", "A", 1)  # Change the P drive to A for my computer
        ok = True
        size = os.stat(pathChanged).st_size
        if size > 550 * 1024 * 1024:
            ok = False
        if ok:
            try:
                image = Image(path=pathChanged)
                average = image.channels[int(channelNumber)].getAverageValueOfPixels()
                stdDev = image.channels[int(channelNumber)].getStandardDeviation()
                listOfAverages.append(average)
                listOfStdDev.append(stdDev)
                print(average)
                print(stdDev)
            except NotImplementedError as e:
                print(e)
                average = "NotYetImplemented"
                stdDev = average
                print("NotYetImplemented")
            except IndexError:
                print("Index error : ", pathChanged, channelNumber, image.shape)
                average = "IndexError"
                stdDev = average
        else:
            average = "FileTooBig"
            stdDev = average
            print("FileTooBig")
        writeResults.writelines(
            "\n{path},{number},{average},{stdDev}".format(path=path, number=channelNumber.strip(), average=average,
                                                          stdDev=stdDev))
        print("{} / {} files read".format(i + 1, numberOfFiles))

    readQuery.close()
    writeResults.close()

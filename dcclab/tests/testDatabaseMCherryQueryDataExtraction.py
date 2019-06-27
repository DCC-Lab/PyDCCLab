import env
from dcclab import Image, cziUtil
import os

# For this test, the query was done by Mathieu on his computer. Selected channel is mCherry
if __name__ == '__main__':
    listOfAverages = []
    listOfStdDev = []

    readQuery = open(r"query_mcher.csv", "r",
                     encoding="utf-8")

    writeResults = open(r"query_mcher_results.csv",
                        "w", encoding="utf-8")

    lines = readQuery.readlines()
    numberOfFiles = len(lines)

    startIndex = 0
    for i in range(startIndex, len(lines)):
        path, channelNumber = lines[i].split(";")
        channelNumber = channelNumber.split(":")[1]
        # The paths in
        pathChanged = os.path.join("../", path)
        print(pathChanged)
        ok = True
        size = os.stat(pathChanged).st_size
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

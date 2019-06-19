import env
from dcclab import Image
import os

# For this test, the query was done by Mathieu on his computer. Selected channel is mCherry
if __name__ == '__main__':
    listOfAverages = []

    readQuery = open(r"C:\Users\goubi\PycharmProjects\BigData-ImageAnalysis\dcclab\tests\querry_mcher.csv", "r",
                     encoding="utf-8")
    writeResults = open(r"C:\Users\goubi\PycharmProjects\BigData-ImageAnalysis\dcclab\tests\querry_mcher_results.czv",
                        "w", encoding="utf-8")
    writeResults.write(
        "WARNING: The czi file reader is only capable of properly reading single image (mutli or mono channel). "
        "If it is a z-stack or a time serie, only one image will be taken.")

    lines = readQuery.readlines()
    numberOfFiles = len(lines)
    currentNumber = 0
    for line in lines:

        path, channelNumber = line.split(",")
        pathChanged = path.replace("P", "A", 1)  # Change the P drive to A for my computer
        ok = ""
        size = os.stat(pathChanged).st_size
        if size > 200 * 1024 * 1024:
            while ok not in ["Y", "N"]:
                ok = input("Heavy file ({}). Continue? (Y/N)".format(size)).upper()
        if ok in ["Y", ""]:
            try:
                image = Image(path=pathChanged)
                average = image.channels[int(channelNumber)].getAverageValueOfPixels()
                listOfAverages.append(average)
                print(average)
            except NotImplementedError as e:
                print(e)
                average = "-"
        else:
            average = "-"
        writeResults.write("{0},{1},{2}".format(path, channelNumber, average))
        currentNumber += 1
        print("{} / {} files read".format(currentNumber, numberOfFiles))

    readQuery.close()
    writeResults.close()

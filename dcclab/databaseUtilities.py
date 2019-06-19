import os
import fnmatch
import zipfile


def findFiles(directory, extension) -> list:
    filesFound = []
    for root, directories, files in os.walk(os.path.normpath(directory)):
        for file in files:
            if fnmatch.fnmatch(file, extension):
                filesFound.append(os.path.join(root, file))
    return filesFound


def appendToZip(path, file):
    try:
        with zipfile.ZipFile(path, 'a') as zip:
            zip.write(file)
    except:
        pass


if __name__ == '__main__':

    pass
from zipfile import ZipFile
import os
import fnmatch


def findFiles(directory, extension) -> list:
    filesFound = []
    for root, directories, files in os.walk(os.path.normpath(directory)):
        for file in files:
            if fnmatch.fnmatch(file, extension):
                filesFound.append(os.path.join(root, file))
    return filesFound


def appendToZip(path, file):
    try:
        with ZipFile(path, 'a') as zeep:
            zeep.write(file)
    except:
        pass


if __name__ == '__main__':
    pass
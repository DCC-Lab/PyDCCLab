from zipfile import ZipFile
from pathlib import Path
from fnmatch import fnmatch
import os


def findFiles(directory, extension) -> list:
    filesFound = []
    for root, directories, files in os.walk(os.path.normpath(directory)):
        for file in files:
            if fnmatch(file, extension):
                filesFound.append(os.path.join(root, file))
    return filesFound

def appendToZip(path, file):
    try:
        with ZipFile(path, 'a') as zeep:
            zeep.write(file)
    except:
        pass


def findFolderInPath(folder, path):
    try:
        newPath = os.path.dirname(path)
        if os.path.basename(newPath) == folder:
            return os.path.dirname(newPath)
        else:
            return findFolderInPath(folder, newPath)
    except:
        pass


if __name__ == '__main__':
    pass
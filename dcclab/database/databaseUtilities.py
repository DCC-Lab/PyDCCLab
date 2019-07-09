from zipfile import ZipFile
from pathlib import Path
from fnmatch import fnmatch
import os


def findFilesOS(directory, extension) -> list:
    filesFound = []
    for root, directories, files in os.walk(os.path.normpath(directory)):
        for file in files:
            if fnmatch(file, extension):
                filesFound.append(os.path.join(root, file))
    return filesFound

def findFiles(directory, extension) -> list:
    files = []
    subfiles = []
    for entry in os.scandir(directory):
        if entry.is_file() and fnmatch(entry, extension):
            files.append(entry)
        elif entry.is_dir():
            subfiles = findFiles(entry, extension)
    return files + subfiles


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
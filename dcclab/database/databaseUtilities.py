from zipfile import ZipFile
import os
import re


def findFiles(directory, extension) -> list:
    # Although os.walk is slow, I haven't found a faster way to find files in a directory and sub directories.
    # In python 3.x, os.walk was modified to use os.scandir, which greatly improved its performances. I doubt
    # there is a faster way to do this.
    filesFound = []
    for root, directories, files in os.walk(os.path.normpath(directory)):
        for file in files:
            if re.search(r'^.*\.{}$'.format(extension), file, re.IGNORECASE):
                filesFound.append(os.path.join(root, file))
    return filesFound


if __name__ == '__main__':
    pass
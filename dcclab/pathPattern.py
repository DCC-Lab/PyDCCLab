import re
import os

class PathPattern:
    def __init__(self, pattern:str):
        self.pattern = pattern
        re.compile(pattern) # will raise exception if needed

    @property
    def directory(self):
        dirName = os.path.dirname(self.pattern)
        if dirName == '':
            dirName = './'
        return dirName

    @property
    def basePattern(self):
        return os.path.basename(self.pattern)

    @property
    def hasCaptureGroups(self) -> bool:
        if re.search(r"\(.+\)", self.pattern):
            return True
        else:
            return False

    @property
    def numberOfCaptureGroups(self) -> int:
        captureGroups = re.findall(r"(\(.+?\))", self.pattern)
        return len(captureGroups)

    @property
    def isPythonFormatString(self) -> bool:
        if re.search(r"\{\d+.*?\}", self.pattern):
            return True
        else:
            return False

    @property
    def numberOfFormatGroups(self) -> int:
        formatGroups = re.findall(r"\{\d+.*?\}", self.pattern)
        return len(formatGroups)

    @property
    def isWritePattern(self) -> bool:
        if self.isPythonFormatString:
            return True
        else:
            return False

    @property
    def isReadPattern(self) -> bool:
        if self.hasCaptureGroups:
            return True
        else:
            return False

    def matchingFiles(self) -> list:
        if self.isWritePattern:
            raise ValueError("Patterns with format strings are for writing files, not reading")

        paths = []
        for filename in os.listdir(self.directory):
            if re.match(self.basePattern, filename):
                filePath = os.path.join(self.directory,filename)
                paths.append(filePath)
        paths.sort()
        return paths

    def filePathWithIndex(self, i:int, j:int = None, k:int = None):
        if self.isReadPattern:
            raise ValueError("Patterns with capture groups are for reading files, not writing")

        if self.numberOfFormatGroups == 1:
            filePath = self.pattern.format(i)
        elif self.numberOfFormatGroups == 2:
            filePath = self.pattern.format(i, j)
        elif self.numberOfFormatGroups == 3:
            filePath = self.pattern.format(i, j, k)
        else:
            raise ValueError("More than 3 indices not supported")
            
        return filePath



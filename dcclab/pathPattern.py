import re
import os

class PathPattern:
    def __init__(self, pattern:str):
        self.pattern = pattern


    @property
    def directory(self):
        return os.path.dirname(self.pattern)

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

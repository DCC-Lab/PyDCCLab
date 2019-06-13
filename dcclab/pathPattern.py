import re

class PathPattern:
    def __init__(self, pattern:str):
        self.pattern = pattern

    @property
    def hasCaptureGroups(self) -> bool:
        if re.search(r"\(.+\)", self.pattern):
            return True
        else:
            return False

    @property
    def numberOfCaptureGroups(self) -> int:
        match = re.search(r"(\(.*\))", self.pattern)
        if match is not None:
            return len(match.groups())
        else:
            return 0

    @property
    def isPythonFormatString(self) -> bool:
        if re.search(r"\{\d+.*\}"):
            return True
        else:
            return False

    @property
    def numberOfFormatElements(self) -> int:
        return 0

    def isWritePattern(self) -> bool:
        if self.isPythonFormatString:
            return True
        else:
            return False

    def isReadPattern(self) -> bool:
        try:
            re.compile(self.pattern)
            # is Valid regexp

        except:
            pass

        if re.search(""):
            return True
        else:
            return False


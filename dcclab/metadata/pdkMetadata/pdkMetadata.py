class pdkMetadata:
    # Dev notes : The file is a RAW movie type file.
    # The metadata is in a .ini file within the same folder as the .raw file.
    def __init__(self, filePath):
        self.filePath = filePath
        self.acquisitionFrequency = None
        self.acquisitionType = None
        self.xSize = None
        self.ySize = None
        self.objective = None
        self.numberOfFrames = None
        self.simulation = None
        self.notes = None


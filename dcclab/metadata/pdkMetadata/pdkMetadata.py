class pdkMetadata:
    # Dev notes : The file is a RAW movie type file.
    # The metadata is in a .ini file within the same folder as the .raw file.
    def __init__(self, filePath):
        self.filePath = filePath
        acquisitionFrequency = None
        acquisitionType = None
        imageDimension = None
        objective = None
        numberOfFrames = None
        simulation = None
        notes = None


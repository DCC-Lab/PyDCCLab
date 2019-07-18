class PDKMetadata:
    # Dev notes : The file is a RAW movie type file.
    # The metadata is in a .ini file within the same folder as the .raw file.
    def __init__(self, xlsxLine: list):
        self.acquisitionFrequency = xlsxLine[0]
        self.acquisitionType = xlsxLine[1]
        self.imageDimensions = xlsxLine[2]
        self.objective = xlsxLine[3]
        self.numberOfFrames = xlsxLine[4]
        self.simulation = xlsxLine[5]
        self.notes = xlsxLine[6]
        self.filePath = xlsxLine[7]

    def __repr__(self):
        return {'pdkMetadata': {'acquisition_frequency': self.acquisitionFrequency,
                                'acquisition_type': self.acquisitionType, 'image_dimensions': self.imageDimensions,
                                'objective': self.objective, 'number_of_frames': self.numberOfFrames,
                                'simulation': self.simulation, 'note': self.notes, 'file_path': self.filePath}}

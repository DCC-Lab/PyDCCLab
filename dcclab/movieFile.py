from .imageFile import *
from .pathPattern import *
import os
import cv2

class MovieFile(ImageFile):
    def __init__(self, path:str, frameShape=None, sampleType=None, frameRate=None):
        super(MovieFile, self).__init__(path)
        self.path = path
        self.frameRate = frameRate
        self.frameShape = frameShape
        self.sampleType = sampleType
        self.videoCapture = None
        self.videoWriter = None
        self.cachedData = None
        try:
            self.cachedData = self.timeSeriesData()
        except:
            pass

    @property
    def isUsingOpenCV(self):
        return isinstance(self.videoCapture, cv2.VideoCapture)

    @property
    def bytesPerSample(self):
        return self.sampleType.itemsize

    @property
    def samplesPerPixel(self):
        return self.frameShape[2]

    @property
    def frameSize(self):
        return self.frameShape[0]*self.frameShape[1]*self.frameShape[2]*self.bytesPerSample
    
    def save(self, path, timeData = None):
        if timeData is None:
            timeData = self.cachedData

        self.beginWriting(path, timeData)
        for i in range(timeData.shape[3]):
            self.writeNextFrame(timeData[:,:,:,i])
        self.endWriting()

    def timeSeriesData(self):
        if self.cachedData is None:
            self.beginReading()
            try:
                while (1):
                    if self.appendNextFrame() is None:
                        break
            finally:
                self.endReading()

        return self.cachedData

    def beginReading(self):
        self.cachedData = None
        if PathPattern(self.path).extension == 'raw':
            self.videoCapture = open(self.path, "rb")
        else:
            self.videoCapture = cv2.VideoCapture(self.path)
            self.frameRate = self.videoCapture.get(cv2.CAP_PROP_FPS)

    def readNextFrame(self) -> np.ndarray:
        if self.isUsingOpenCV:
            success, frame = self.videoCapture.read()
            return frame
        else:
            if self.frameShape is None or self.sampleType is None:
                raise ValueError("No frame size determined. You must set frameShape and sampleType")
            
            binaryData = self.videoCapture.read(self.frameSize)
            if len(binaryData) != self.frameSize:
                return None
            else:
                frameData = np.frombuffer(binaryData,dtype=self.sampleType)
                frameData = np.reshape(frameData, self.frameShape)
                return frameData

        return None

    def appendNextFrame(self) -> np.array:
        frameData = self.readNextFrame()
        if frameData is not None:
            frameData = np.expand_dims(frameData, 3)
            if self.cachedData is None:
                self.cachedData = frameData
            else:
                self.cachedData = np.concatenate((self.cachedData,frameData),3)
        
        return frameData

    def endReading(self):
        if self.isUsingOpenCV:
            self.videoCapture.release()
            self.videoCapture = None
        else:
            self.videoCapture.close()

    def beginWriting(self, path, frameData):
        height, width, channels, timeSteps = frameData.shape
        if self.frameRate is None:
            raise ValueError("No frame rate determined. You must set frameRate")

        fourcc = 0 # no compression
        pathPattern = PathPattern(path)
        if pathPattern.extension == 'mov' or pathPattern.extension == 'mp4':
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        self.videoWriter = cv2.VideoWriter(path, fourcc, self.frameRate, (width, height))

    def writeNextFrame(self, frame):
        self.videoWriter.write(frame)

    def endWriting(self):
        self.videoWriter.release()

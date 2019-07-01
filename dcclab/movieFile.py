from .imageFile import *
from .pathPattern import *
import os
import cv2

class MovieFile(ImageFile):
    def __init__(self, path:str):
        super(MovieFile, self).__init__(path)
        self.path = path
        self.frameRate = None
        self.frameShape = None
        self.samplesPerPixel = None
        self.sampleType = np.int8
        self.readModeCV = True
        self.videoCapture = None
        self.videoWriter = None
        self.cachedData = self.timeSeriesData()

    @property
    def isUsingOpenCV(self):
        return isinstance(self.videoCapture, cv2.VideoCapture)

    @property
    def bytesPerSample(self):
        return self.sampleType.itemsize

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
        self.beginReading()
        timeSeriesData = None
        try:
            frame = self.readNextFrame()
            timeSeriesData = frame
            while(frame is not None):
               timeSeriesData = np.concatenate((timeSeriesData,frame),3)
               frame = self.readNextFrame()
        except:
            self.endReading()

        return timeSeriesData

    def beginReading(self):
        if PathPattern(self.path).extension == 'raw':
            self.videoCapture = open(self.path, "rb")
        else:
            self.videoCapture = cv2.VideoCapture(self.path)
            self.frameRate = self.videoCapture.get(cv2.CAP_PROP_FPS)

    def readNextFrame(self) -> np.ndarray:
        if self.isUsingOpenCV:
            success, frame = self.videoCapture.read()
            if success is False:
                return None

            if frame is not None:
                return np.expand_dims(frame, 3)
        else:
            if self.frameShape is None or self.samplesPerPixel is None or self.bytesPerSample is None:
                raise ValueError("No frame size determined. You must set frameShape, samplesPerPixel and bytesPerSample")
            binaryData = self.videoCapture.read(self.frameSize)
            frameData = np.frombuffer(binaryData,dtype=self.sampleType)
            frameData.reshape(self.frameShape)
            return frameData

        return None

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

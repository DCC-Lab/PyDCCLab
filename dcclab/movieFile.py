from .imageFile import *
from .pathPattern import *
import cv2

class MovieFile(ImageFile):
    def __init__(self, path:str):
        super(MovieFile, self).__init__(path)
        self.path = path
        self.videoCapture = None
        self.videoWriter = None
        self.cachedData = self.timeSeriesData()

    def save(self, path, timeSeriesData):
        self.beginWriting(path, timeSeriesData)
        for i in range(timeSeriesData.shape[3]):
            self.writeNextFrame(timeSeriesData[:,:,:,i])
        self.endWriting()

    def timeSeriesData(self):
        self.beginReading()
        frame = self.readNextFrame()
        timeSeriesData = frame
        while(frame is not None):
           timeSeriesData = np.concatenate((timeSeriesData,frame),3)
           frame = self.readNextFrame()

        self.endReading()
        return timeSeriesData

    def beginReading(self):
        self.videoCapture = cv2.VideoCapture(self.path)

    def readNextFrame(self) -> np.ndarray:
        _, frame = self.videoCapture.read()
        if frame is not None:
            return np.expand_dims(frame, 3)

        return None

    def endReading(self):
        self.videoCapture.release()
        self.videoCapture = None

    def beginWriting(self, path, frameData): 
        height, width, channels, timeSteps = frameData.shape
        self.videoWriter = cv2.VideoWriter(path, 0, 20.0, (width, height))

    def writeNextFrame(self, frame):
        self.videoWriter.write(frame) # Write out frame to video

    def endWriting(self):
        self.videoWriter.release()

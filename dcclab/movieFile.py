from .imageFile import *
from .pathPattern import *
import cv2

class MovieFile(ImageFile):
    def __init__(self, path:str):
        super(MovieFile, self).__init__(path)
        self.path = path
        self.frameRate = None
        self.videoCapture = None
        self.videoWriter = None
        self.cachedData = self.timeSeriesData()

    def save(self, path, timeData = None):
        if timeData is None:
            timeData = self.cachedData

        self.beginWriting(path, timeData)
        for i in range(timeData.shape[3]):
            self.writeNextFrame(timeData[:,:,:,i])
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
        self.frameRate = self.videoCapture.get(cv2.CAP_PROP_FPS)

    def readNextFrame(self) -> np.ndarray:
        success, frame = self.videoCapture.read()
        if success is False:
            return None

        if frame is not None:
            return np.expand_dims(frame, 3)

        return None

    def endReading(self):
        self.videoCapture.release()
        self.videoCapture = None

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

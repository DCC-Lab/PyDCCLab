from .imageCollection import *
import cv2

class TimeSeries(ImageCollection):
    def __init__(self, images:List[Image]=None, imagesArray:np.ndarray=None, pathPattern: str=None, keepOriginal: bool=True):
        super().__init__(images, imagesArray, pathPattern)
        if not self.imagesAreSimilar:
            raise ValueError("Images in TimeSeries are not all the same shape")

    def asArray(self) -> np.ndarray:
        return np.stack([ image.asArray() for image in self.images ], axis=3)

    def show(self, axis=-1):
        stack4DArray = self.asArray()
        plt.imshow(stack4DArray.mean(axis))
        plt.show()

    def save(self, path):
        pattern = PathPattern(path)
        if path.extension == 'avi':
            self.saveAsAVI(path)
            
        if pattern.isWritePattern:
            if pattern.numberOfFormatGroups == 0:
                self.saveAsAVI(path)

                
    def saveAsAVI(self, path):
        height, width, channels = self.images[0].shape

        # Define the codec and create VideoWriter object
        # fourcc = cv2.VideoWriter_fourcc(*'DIB ') 
        # use fourcc = 0 for uncompressed.
        out = cv2.VideoWriter(path, 0, 20.0, (width, height))
        for image in self.images:
            out.write(image.asArray())
        out.release()





import env
from dcclab import *
import unittest
import os

class TestMovieFile(env.dcclabTestCase):
    def testInit(self):
        self.assertIsNotNone(MovieFile(self.dataFile("testMovie.mov")))

    def testReadImageData(self):
        movie = MovieFile(self.dataFile("testMovie.mov"))
        timeData = movie.timeSeriesData()
        self.assertIsNotNone(timeData)
        self.assertTrue(len(timeData.shape) == 4)

    def testWriteImageDataAsAVI(self):
        movie = MovieFile(self.dataFile("testMovie.mov"))
        timeData = movie.timeSeriesData()
        tmpFile = self.tmpFile("output.avi")
        movie.save(tmpFile, timeData)
        self.assertTrue(Path(tmpFile).exists())
        self.assertTrue(os.path.getsize(tmpFile) > 0)

    def testWriteImageDataAsAVINoExplicitRead(self):
        movie = MovieFile(self.dataFile("testMovie.mov"))
        tmpFile = self.tmpFile("output.avi")
        movie.save(tmpFile)
        self.assertTrue(os.path.exists(tmpFile))
        self.assertTrue(os.path.getsize(tmpFile) > 0)

    def testWriteImageDataAsMOVNoExplicitRead(self):
        movie = MovieFile(self.dataFile("testMovie.mov"))
        tmpFile = self.tmpFile("output2.mov")
        movie.save(tmpFile)
        self.assertTrue(os.path.exists(tmpFile))
        self.assertTrue(os.path.getsize(tmpFile) > 0)
        movieSaved = MovieFile(tmpFile)

    def testOsOpenAPI(self):
        file = open(self.dataFile("testMovie.raw"),"rb")
        self.assertIsNotNone(file)
        file.close()


    def testOsReadChunk(self):
        file = open(self.dataFile("testMovie.raw"),"rb")
        data = file.read(1000)
        self.assertIsNotNone(data)
        self.assertTrue(len(data) == 1000)
        file.close()

    def testOsReadLargeChunk(self):
        file = open(self.dataFile("testMovie.raw"),"rb")
        data = file.read(1024*512*3)
        self.assertIsNotNone(data)
        self.assertTrue(len(data) == 1024*512*3)
        file.close()

    def testOsReadLargeChunk(self):
        try:
            file = open(self.dataFile("testMovie.raw"),"rb")

            width = 1024
            height = 512
            spp = 3
            dt = np.dtype('int16').newbyteorder('>')
            bpp = dt.itemsize
            size = height*width*spp*bpp
            data = file.read(size)

            self.assertTrue(bpp == 2)
            self.assertIsNotNone(data)
            self.assertTrue(len(data) == size)

            numpyArray = np.frombuffer(data,dtype=dt)
            numpyArray.reshape(width, height, spp)
        except:
            self.fail("Exception")
        finally:
            file.close()

    def testReadRaw(self):
        sampleType = np.dtype('int16').newbyteorder('>')
        frameShape = (1024,512,3)
        movie = MovieFile(self.dataFile("testMovie.raw"),
                          frameShape=frameShape,
                          sampleType=sampleType)

        self.assertIsNotNone(movie.cachedData)

    def testReadRawLater(self):
        movie = MovieFile(self.dataFile("testMovie.raw"))
        movie.sampleType = np.dtype('int16').newbyteorder('>')
        movie.frameShape = (1024,512,3)
        movie.beginReading()
        try:
            while (1):
                if movie.appendNextFrame() is None:
                    break
            
        except:
            self.fail()
        finally:
            movie.endReading()
        self.assertIsNotNone(movie.cachedData)

if __name__ == '__main__':
    unittest.main()

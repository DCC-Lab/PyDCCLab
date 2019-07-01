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

if __name__ == '__main__':
    unittest.main()

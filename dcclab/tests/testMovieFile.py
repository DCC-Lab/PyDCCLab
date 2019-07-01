import env
from dcclab import *
import unittest
import os
from pathlib import Path

class TestMovieFile(env.dcclabTestCase):
    def testInit(self):
        self.assertIsNotNone(MovieFile(self.dataFile("testMovie.mov")))

    def testImageData(self):
        movie = MovieFile(self.dataFile("testMovie.mov"))
        timeData = movie.timeSeriesData()
        self.assertIsNotNone(timeData)
        self.assertTrue(len(timeData.shape) == 4)

    def testWriteImageData(self):
        movie = MovieFile(self.dataFile("testMovie.mov"))
        timeData = movie.timeSeriesData()

        movie.save(self.tmpFile("output.avi"), timeData)

if __name__ == '__main__':
    unittest.main()

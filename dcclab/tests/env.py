import unittest
import sys
import os
from pathlib import Path
import tempfile

# append module root directory to sys.path
sys.path.insert(0,
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(
                            os.path.abspath(__file__)
                        )
                    )
                )
            )

class dcclabTestCase(unittest.TestCase):
    dataDir = Path('./testData')
    tmpDir = Path("{0}/{1}".format(tempfile.gettempdir(), "testfiles"))
  
    def __init__(self,tests=()):
        super(dcclabTestCase, self).__init__(tests)

    @classmethod
    def setUpClass(self):
        self.createTempDirectories()

    @classmethod
    def tearDownClass(self):
        self.deleteTempDirectoriesAndFiles()

    @classmethod
    def createTempDirectories(self):    
        self.tmpDir.mkdir( parents=True, exist_ok=True )

    @classmethod
    def deleteTempDirectoriesAndFiles(self):
        for filename in self.tmpDir.iterdir():
            Path(self.tmpDir / filename).unlink()
        self.tmpDir.rmdir()


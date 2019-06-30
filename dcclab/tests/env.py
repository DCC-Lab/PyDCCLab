import sys
import os
import unittest
import tempfile
from pathlib import Path

class dcclabTestCase(unittest.TestCase):
    moduleDir = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))) 
    tmpDir = Path(os.path.join(tempfile.gettempdir(), "testfiles"))
    testsDir = Path(os.path.dirname(os.path.abspath(__file__) ))
    dataDir = Path(os.path.join(testsDir, 'testData'))

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
        # It's ok if it has been deleted at this point
        if self.tmpDir.exists():
            for filename in self.tmpDir.iterdir():
                Path(self.tmpDir / filename).unlink()
            self.tmpDir.rmdir()

# Very important:  append module root directory to sys.path
sys.path.insert(0, dcclabTestCase.moduleDir)

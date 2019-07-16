import sys
import os
import unittest
import tempfile
from pathlib import Path


class DCCLabTestCase(unittest.TestCase):
    moduleDir = Path(os.path.abspath(os.path.join(os.path.dirname(__file__)))) 
    tmpDir = Path(tempfile.gettempdir(), "testfiles")
    testsDir = Path(moduleDir, "dcclab", "tests")
    dataDir = Path(testsDir, 'testData')

    def __init__(self, tests=()):
        super(DCCLabTestCase, self).__init__(tests)

    @classmethod
    def setUpClass(cls):
        cls.createTempDirectories()

    @classmethod
    def tearDownClass(cls):
        cls.deleteTempDirectoriesAndFiles()

    @classmethod
    def createTempDirectories(cls):
        cls.tmpDir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def deleteTempDirectoriesAndFiles(cls):
        # It's ok if it has been deleted at this point
        if cls.tmpDir.exists():
            for filename in cls.tmpDir.iterdir():
                Path(cls.tmpDir / filename).unlink()
            cls.tmpDir.rmdir()

    @classmethod
    def dataFile(cls, filename):
        return os.path.join(cls.dataDir, filename)

    @classmethod
    def tmpFile(cls, filename):
        return os.path.join(cls.tmpDir, filename)

# No need to add the directory to sys path because this is for PyCharm only, which includes it already
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
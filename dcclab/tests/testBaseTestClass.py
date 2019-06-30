import env
import os
from pathlib import Path

class TestPatterns(env.dcclabTestCase):
    def testInit(self):
        self.assertIsNotNone(self.tmpDir)
        self.assertIsNotNone(self.dataDir)

    def testTestDir(self):
        self.assertIsNotNone(self.testDir)
        self.assertTrue(os.path.exists(Path(self.testDir / 'env.py')))
        
    def testTmpDirExists(self):
        self.assertTrue(os.path.exists(self.tmpDir), "Temporary directory not created")

    def testTmpDirIsEmpty(self):
        files = []
        for filename in self.tmpDir.iterdir():
            files.append(filename)
        self.assertTrue(len(files) == 0, "Temporary directory empty")

    def testDataDirExists(self):
        self.assertTrue(os.path.exists(self.dataDir), "Data directory not present")

    def testDataDirNotEmpty(self):
        files = []
        for filename in self.dataDir.iterdir():
            files.append(filename)
        self.assertTrue(len(files) != 0)

if __name__ == '__main__':
    unittest.main()

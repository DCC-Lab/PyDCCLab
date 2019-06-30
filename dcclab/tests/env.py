import sys
import os
from pathlib import Path, PureWindowsPath
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

dataDir = Path('./testData')
tmpDir = Path("{0}/{1}".format(tempfile.gettempdir(), "testfiles"))
tmpDir.mkdir( parents=True, exist_ok=True )

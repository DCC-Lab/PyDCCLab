import dcclab as dcc
import os
from dcclab.tests import env

env.dcclabTestCase.createTempDirectories()
print(env.dcclabTestCase.tmpDir)

a = dcc.Image(path=env.dcclabTestCase.dataFile('test.png'))
a.save(env.dcclabTestCase.tmpFile('test.tif'))
a.save(env.dcclabTestCase.tmpFile('test.bmp'))
a.save(env.dcclabTestCase.tmpFile('test.gif'))
a.save(env.dcclabTestCase.tmpFile('test2.png'))
# b = dcc.Image('/tmp/matlab.mat')


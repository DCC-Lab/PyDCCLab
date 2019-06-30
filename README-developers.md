[TOC]

# CERVO-dcclab Python module

This simple module is meant to simplify the loading and treatment of images at CERVO. The ultimate goal of this module is to allow users to rapidly extract useful and pertinent information about microscopy images taken in their lab, possibly at the CERVO research center.

## Image-oriented API

The first API, for users, is said to be "image-oriented".  This is likely going to be the most used API: I have an image, show me the filtered image, the z-stack or segment this collection of images.  *It must be expressed in a natural language for people who deal with images.* An `Image()` keeps an internal reference (hidden) to a `ImageFile`.  

## File-oriented API

Sometimes however, a user has a specific file and needs to comb through all the data it contains.  For instance, a Carl-Zeiss File (`.czi`) contains several images and Leica file (`.lif`) can contain several stacks and time series.  Hence, in this particular case, it become very much application-specific.  An file-oriented API uses the file as the source and can return Images, zStacks, TimeSeries, etc… contained in the file. An `ImageFile` can be created independently, and methods exist to obtain `ImageData`, `ImageStackData`, etc...

## Class hierarchy

![image-20190629121821276](assets/image-20190629120540243.png) 

## Testing

Everything needs to be unit tested.  

### Writing tests

Import `env` first.  A testcase file should look like this:

```python
import env # important: definition of dcclabTestCase, sys.path modified for dcclab testing
from dcclab import *
import unittest
import numpy as np

class TestChannelFloat(env.dcclabTestCase):
    def setUp(self) -> None:
        array = np.ones((10, 10), dtype=np.float32) * 2.35
        self.channelNotNormalized = Channel(array)
        arrayNormed = np.ones_like(array) * 0.87
        self.channelNormalized = Channel(arrayNormed)

    def testIsNormalizedAfterInit(self):
        self.assertTrue(np.max(self.channelNotNormalized.pixels) == 1)

    ...

```

You should use the `dcclabTestCase` base class for your test cases, since that will give you access to 4 special directories:

| Class variable | Description                                                  |
| -------------- | ------------------------------------------------------------ |
| tmpDir         | A temporary directory that gets deleted with its content when tests are done |
| dataDir        | The directory (testData) where all data for testing (i.e. test files) should be stored |
| moduleDir      | The directory where the module is                            |
| testsDir       | The tests directory                                          |

If generally useful functions are needed in the module, they should go there. You also get `dataFile(filename)` and `tmpFile(filename)` to quickly obtain a path into those directories. If generally useful functions are needed, they should go there. 

### Running all tests

You can run all tests with:

```shell
cd dcclab/tests/
python -m unittest
```

### Test coverage

You can check the coverage of your code with

```shell
coverage run testFile.py
coverage html
```

then open `htmlcov/index.html`. We should always aim for nearly 100% coverage.



## Coding style

The coding style for the group is available [online](https://github.com/DCC-Lab/Documentation/blob/master/HOWTO-CodingStyle.md). However, we highlight important aspects here:

1. Plan for usage, not for coders.

2. The code should read as a text.
   Variable names and function names are important. A boolean variable can be called `isDone`. A table representing an image can be called `image`. A function can have an action verb in its name. 

3. We do not need to use "array" in the name to describe an array, because it could be an array, a list, a set. We use th eplural form instead. For instance, in `Image`, the channels are kept in `Image().channels`, which happens to be a list. In `ImageCollection`, the images are in `images`.

4. We take a "camel-case" style, that is, the first letter is lowercase, and then each word is capitalized, as in `createRayPlot()`. We never use underscores (_) which are reserved for internal, hidden, private, low-level variables.

5. Properties must be declared with `@property`.

6. Functions shoudl have an action word (`applyFilter`).  If we "get" something, we use the name without `get` (i.e. `imageData`).  When we set something that is not a property, we use `set` (i.e. `setPermissionToReadOnly`)

7. Always expose as little as possible.

   
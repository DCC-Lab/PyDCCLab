# CERVO-dcclab Python module

This simple module is meant to simplify the loading and treatment of images at CERVO (or in any lab) and to provide access to databases for data. The ultimate goal of this module is to rapidly be able to extract useful and pertinent information about microscopy images and spectra. It consists of several "sub modules" 

## Installation

`pip install dcclab --user` should work, but if by any chance you get an error for a missing module when using it, then `pip install modulename` should fix it.
Required modules should be installed automatically. If anything is missing, [let us know](mailto:dccote@cervo.ulaval.ca).

You should then be able to simply import the module in your own scripts:

```
from dcclab import *

# ... you script
img = Image('yourFile.tiff')
img.display()

```

## You are a lab member and you want to do image Analysis

### Documentation

**The documentation so far is pretty minimal. I recommend using (help(classname)). This needs to be worked on.**

There are many image libraries, and this is one more to work with.  Every module has a purpose, and the present module aims to be **easy to use**.  This means clarity of the module for users is key, and to a certain extent, clarity for developers is also important: the module was developed by trainees in the laboratory of [Daniel Côté](http://www.dccmlab.ca) at the [CERVO Brain Research Center](http://www.cervo.ulaval.ca) in Québec city, and new trainees every year contribute to the module. Therefore, it is the primary design consideration for the module to be readable, not to be high-performance.  That said, the library offers a very impressive performance nevertheless. Below you will find definitions and conventions for the code, classes and files.

The module makes heavy use of the `numpy` module, because every package manipulating images goes back to this high-performance module for storing arrays. We are no different, and we use it like everyone else.

This module is a task-oriented module for image analysis: it provides simple tools (classes) to easily read image files, inspect them and manipulate them. For instance, the following classes:

1. `Image`: can read most image formats, including Zeiss microscope files (`.czi`).
2. `Channel`: each image has one or several channels.  The channels, which correspond to specific fluorophores, can be manipulated with filters, threshold, segmentation and other operations. More complex methods like  watershed are also available to use.
3. `ImageCollection`: can read a collection of image files (e.g., a directory, a z-stack, a map, etc...)

### Definitions

1. `Channel`: a channel is what most people would consider a grayscale image.  It represents a collection of pixels in 2D for a single contrast mechanism (for instance, GFP, DAPI, Raman, wide field, etc…). When need as an array, it is a `numpy.ndarray` that has 2 dimensions: width ⨉ height. *It is never a 3D array because it never has more than one contrast agent.* The Channel contains also any information that was recovered from reading a file (if it came from a file: objective, magnification, scale, etc…) if that information was available.

2. `Image`: an image is what anyone would consider "an image": it represents a collection channels. For instance, an image from a microscope may return three colours in red, green and blue (commonly stored as an RGB image such as TIFF for instance). When needed, it is a `numpy.ndarray` that has 3 dimensions: width ⨉ height ⨉ channels. Note that the is always a channel dimension, even with only one channel.

3. `ImageCollection`: as the name implies, it is a collection of `Images`. We often deal with collection of images, and we often want to operate on a group of images (e.g., segment many images, strip a channel from images, obtain the average of a given colour, etc…).  The images may or may not be stored as separate files.  They may be stored as separate frames in a movie.  The may be stored in some proprietary format.  Regardless, to the scientist, it is a collection of images that may or may not have more than one `Channel`. The images may or may not have the same format, therefore  it is not always possible to obtain a `numpy.ndarray` representing the entire collection. When all images are the same format (width, height and number of channels), then one can obtain a 4D `numpy.ndarray` with width ⨉ height ⨉ channels ⨉ collection. Note that the `ImageCollection`  always has a channel dimension, even with only one channel, and there is always a collection dimension, even with only one image in the collection.

4. `ZStack`: of all `ImageCollections`, the z-satck is the most common.  It represents a one-dimensional series of images that were all taken at different z depths.  It is of course a special type of `ImageCollection` because all images are the same contrast, essentially at the same position (x,y) but different z, and all have the same "properties" (size, laser, etc…), therefore it is always possible to obtain a 4D `numpy.ndarray`representing the z-stack with width ⨉ height ⨉ channels ⨉ collection. Note that the stack always has a channel dimension, even with only one channel, and there is always a collection dimension, even with only one image in the collection.

### Operations

With images, we want to filter noise, segment images, find cells, threshold them, mask them, blur them, etc… All these operations are defined in the module with a language that is "task-oriented": the function for removing noise is called `filterNoise`, the function to threshold is called `threshold`, etc… That way, code will read like a sentence: `image.filterNoise()` or `image.threshold()`, or even `image.filterNoise().maskWithThreshold().labelMaskComponents()`.

Operations to manipulate "images" as we say, really are operations that operate on `Channels`, not `Images`. Indeed, when a scientist wants to segment an "image", he or she really wants to segment either a single channel, or all channels separately.  Hence most (but not all) operations are defined at the level of `Channel` where all the work takes place. Before going any further, we can already hear people taking offense: *"But I want to segment my images! I don't care about this abstract separation of channels and images defined in your module. And examples above use images, not channels!"*.  And you are right.  This is why `Image`  and `ImageCollection` also define most operations, but `Image` will loop through its `Channels` to operate, and `ImageCollection` will loop through its `Images`, which will loop through their `Channels` to actually get the work done. 99% of the time, this is what people expect. If one had the following script:

```python
from dcclab import *

coll = ImageCollection(filePath='somefiles-\d+.tiff') #details on loading patterns later
coll.filterNoise()
coll.applyGaussianFilter()
```

one would expect that the noise be removed from all images in the collection, in each channel. If one knows that the collection has several unnecessary channels (say we know GFP is in the Green channel (2) and Red (1) and Blue (3) are not used), then we can remove them from the images before filtering out the noise:

```python
from dcclab import *

coll = ImageCollection(filePath='somefiles-\d+.tiff') #details on loading patterns later
coll.removeChannels(1,3)
coll.filterNoise()
coll.applyGaussianFilter()
coll.align()
```

## You are a lab member and you want to use the databases
We have a growing database of spectra, for different projects and for different modalities.  The data is organized like this:
* We have `datasets`: a dataset is typically a series of measurements in the lab, typically done in a single day.  For instance, we have `DRS-001`, `DRS-002` `WINE-001`, etc. You can obtain a description of the datasets with `db.describeDatasets()`
* Each dataset contains many spectra, each identified with a **unique** `spectrumId`.  It looks like  `datasetId-id1-id2-id3-id4`.  What id1, id2,id3 and id4 are depends on the dataset. It is very important to understand that each spectrumId is unique. The `idx` represents a parameter of the dataset.  It can be a region (for SHAVASANA-001, they can be STN, RPG, etc...) but also just an acquisition (1,2,3,) representing multiple measurements.
* The class `db = SpectraDB()` can return a Panda Dataframe with all the spectra you need, which happens to be very convenient
* A large number of spectra or a small one depending on its parameters when it is called. `db.getSpctralDataframe(datasetId="WINE-001")` will return all the spectra in that dataset.
* The data is retrieved from the sewrver at CERVO.  You will need to have the appropriate passwords, instructions will appear the first time you try to connect.  They will be securely stored in a keychain on your computer, you will not have to reenter them later. You need one to access the server, and one to access the database. Most people will use `dcclab` for the username, who can read the data but not delete it.
* Because the spectra can be quite large, a cache is created on your disk and subsequent calls will not go back to the server, they will get the data from the disk, which will be much faster. You still need to do it once though.
* If you know MySQL, then you can `execute` SQL statements on the database and use `fetchAll` or `fetchOne` to retrieve the results.  This is very general and will allow you to perform any task even if it was not programmed in `SpectraDB` or `LabdataDB`.

Example:
```python
from dcclab.database import *

db = SpectraDB() # to access the database of spectra
print(db.describeDatasets()) # Shows the dataset
print(db.getSpectralDataFrame(datasetId="WINE-001"))

db.execute("select * from wines") # wines is a separate table with information about the wines project. It is specific to this project.
for row in db.fectchAll():
  print(row)
```



## You are a programmer and want to programm the database

A `Database` class allows one to manage files that may be spread over different fileservers. A local example at CERVO — the  **Plateforme d'Outils Moléculaires** — is supported, but the DCCLab, PDK, and Martin Levesque groups will be supported in the near future. 

For each specific database, a new class inheriting from the `Database` object can be queried through a general SQL API but also specific-task-oriented API. MySQL is supported (SQLite support has been dropped for now, too complicated to manage both).  MySQL over ssh is also supported.  For example, the database allow requests such as:

1. all images using the viral vector AAV-173,
2. all images of microglia,
3. all images of neurons from the subthalamic nucleus.

The database is ready to use (i.e. `connected`) upon creation.  To begin using the `Database`, making queries or inserting into it, use the exposed API (e.g., `select(table, columns, condition) -> Row:`) or execute an explicit SQL command (e.g., `    execute(statement)`). To create a new database, a `Database` object has to be created with `writePermission=True` (sqlite3) or created on the MySQL server directly. If it does not exist yet, the database will be created at the `Database.path` location (in **URI**).


## Disclaimer

Copyrights DCC/M Lab Members (2019-).

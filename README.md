# CERVO-dcclab Python module
This simple module is meant to simplify the loading and treatment of images at CERVO.

## Image Analysis

This module is a task-oriented module for image analysis: it provides simple tools (classes) to easily read image files, inspect them and manipulate them. For instance, the following classes:

1. `Image`: can read most image formats, including Zeiss microscope files (`.czi`).
2. `Channel`: each image has one or several channels.  The channels, which correspond to specific fluorophores, can be manipulated with filters, threshold, segmentation and other operations.
3. `ImageCollection`: can read a collection of image files (e.g., a directory, a z-stack, a map, etc...)

## Database

Currently under development, a `Database` class allows one to obtain files from various CERVO databases. As of now, only the **Molecular Tools Platform** is supported, but the DCCLab, PDK group and Martin Levesque group will be supported in the near future.

For example, the database will allow requests such as:

1. All images using the viral vector AAV-173
2. All images of microglia.
3. All images of neurons from the subthalamic nucleus.

## Installation

To install development versions, use:

```
python setup.py install -f
```

Required modules should be installed automatically. If anything is missing, [let us know](mailto:dccote@cervo.ulaval.ca).

You should then be able to simply import the module in your own scripts:

```
import dcclab

# ... you script
img = Image('yourFile.tiff')
img.display()

```




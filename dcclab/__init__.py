""" We import almost everything by default, in the general
namespace because it is simpler for everyone 

Circular dependecies on modules, use forward references:
Forward references: https://www.python.org/dev/peps/pep-0484/#forward-references

"""
from .analysis import *
from .database import *
from .image import *
from .metadata import *
from .ml  import *
from .utils import *
from .DCCExceptions import *

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
__author__ = "Daniel Cote <dccote@cervo.ulaval.ca>"

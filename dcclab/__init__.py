""" We import almost everything by default, in the general
namespace because it is simpler for everyone 

Circular dependecies on modules, use forward references:
Forward references: https://www.python.org/dev/peps/pep-0484/#forward-references

"""
from .analysis import *
from .database import *
from .images import *
from .metadata import *
from .ml  import *
from .utils import *

__version__ = "1.1.0"
__author__ = "Daniel Cote <dccote@cervo.ulaval.ca>"

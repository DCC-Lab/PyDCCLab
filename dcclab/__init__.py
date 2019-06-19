import math

""" We import almost everything by default, in the general
namespace because it is simpler for everyone """

from .image import *
from .channel import *
from .imageCollection import *
from .DCCExceptions import *
from .channelInteger import *
from .channelFloat import *
from .pathPattern import *
from .lifFile import *

from .database import *
from .databaseUtilities import *
from .imageMetadata import *
from .cziMetadata import *
from .cziFilter import *
from .cziChannel import *

__version__ = "0.9.0"
__author__ = "Daniel Cote <dccote@cervo.ulaval.ca>"

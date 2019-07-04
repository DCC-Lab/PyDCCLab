""" We import almost everything by default, in the general
namespace because it is simpler for everyone """

from .image import *
from .channel import *
from .imageCollection import *
from .timeSeries import *
from .DCCExceptions import *
from .channelInteger import *
from .channelFloat import *
from .pathPattern import *
from .cziFile import *
from .movieFile import *

from .database import *
from .metadata import *

__version__ = "0.9.5"
__author__ = "Daniel Cote <dccote@cervo.ulaval.ca>"

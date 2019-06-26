""" We import almost everything by default, in the general
namespace because it is simpler for everyone """

from .cziMetadata import CZIMetadata
from .cziChannel import CZIChannel
from .cziFilter import CZIFilter

__version__ = "0.9.0"
__author__ = "Daniel Cote <dccote@cervo.ulaval.ca>"
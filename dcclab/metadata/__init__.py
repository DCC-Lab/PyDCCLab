""" We import almost everything by default, in the general
namespace because it is simpler for everyone """

from .csvMetadata import CSVMetadata
from .cziMetadata import CZIMetadata
from .metadata import Metadata

__version__ = "0.9.0"
__author__ = "Daniel Cote <dccote@cervo.ulaval.ca>"
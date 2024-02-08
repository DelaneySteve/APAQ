""" Airport runway parameters
"""

from pydantic import BaseModel
from enum import Enum

# Enumeration for the train status of a model
class RunwaySurface(Enum):
    """ Enumeration of all possible states that a runway surface can have.
    """
    ASPHALT = 'asphalt'
    UNKNOWN = 'unknown'
    CONCRETE = 'concrete'
    TURF = 'turf'
    BITUMINOUS = 'bituminous'
    MACADAM = 'macadam'
    GRAVEL = 'gravel'
    DIRT = 'dirt'
    PAVED = 'paved'
    GRASS = 'grass'
    LATERITE = 'laterite'
    TARMAC = 'tarmac'
    CORAL = 'coral'
    SEALED = 'sealed'
    SAND = 'sand'
    UNPAVED = 'unpaved'
    WATER = 'water'
    CLAY = 'clay'
    SOIL = 'soil'
    SILT = 'silt'
    TREATED = 'treated'
    ICE = 'ice'

class Runway(BaseModel):
    length_in_ft: int
    # surface: RunwaySurface # Surface parameter hidden until required by the model



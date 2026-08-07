from __future__ import annotations
from enum import Enum, auto

class HandlePosition(Enum):
    """Enum for handle positions."""

    TOP_LEFT = auto()
    TOP_CENTER = auto()
    TOP_RIGHT = auto()
    
    LEFT = auto()
    RIGHT = auto()
    
    BOTTOM_LEFT = auto()
    BOTTOM_CENTER = auto()
    BOTTOM_RIGHT = auto()
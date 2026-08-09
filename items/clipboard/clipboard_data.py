from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from qtpy.QtCore import QPointF, QRectF

@dataclass
class CanvasItemData:
    """A class that represents the data stored in the clipboard."""
    
    item_type: str
    layer_name: str
    
    rect: QRectF
    pos: QPointF
    rotation: float
    scale: float
    
    data: dict[str, Any]
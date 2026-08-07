from __future__ import annotations
from dataclasses import dataclass

from qtpy.QtCore import QPointF, QRectF

from items.enums.handle_position import HandlePosition

@dataclass(slots=True)
class ResizeState:
    """
    Store the initial state of a resize operation.
    """
    handle: HandlePosition
    
    start_rect: QRectF
    
    start_scene_pos: QPointF
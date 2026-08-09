from __future__ import annotations

from dataclasses import dataclass

from qtpy.QtCore import QPointF

@dataclass(slots=True)
class RotationState:
    """
    Represents the state of a rotation operation.
    """
    start_scene_pos: QPointF
    start_rotation: float
    center_scene_pos: QPointF
    snap_rotation: bool = False
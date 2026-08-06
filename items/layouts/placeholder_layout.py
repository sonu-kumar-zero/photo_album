from __future__ import annotations

from dataclasses import dataclass

from qtpy.QtCore import QRectF

@dataclass(slots=True)
class PlaceholderLayout:
    """
    Stores the geometry of all visual elements,
    inside a placeholder Item
    """
    
    icon_rect: QRectF
    title_rect: QRectF
    subtitle_rect: QRectF
    
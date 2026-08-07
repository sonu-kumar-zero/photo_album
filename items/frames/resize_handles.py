from __future__ import annotations

from PySide6.QtCore import QRectF
from qtpy.QtGui import QBrush, QColor, QPainter, QPen
from qtpy.QtWidgets import QGraphicsItem, QGraphicsObject, QStyleOptionGraphicsItem, QWidget

from items.enums.handle_position import HandlePosition

class ResizeHandle(QGraphicsObject):
    """
    Interactive resize handle displayed by SelectionFrame. It is used to resize the selected item.
    """
    
    SIZE = 10  # Size of the resize handle in pixels
    
    def __init__(
        self,
        position: HandlePosition,
        parent: QGraphicsItem | None = None
    ) -> None:
        super().__init__(parent)
        
        self._position = position
        self._hovered = False  # Indicates whether the handle is currently hovered by the mouse
        
        self.setAcceptHoverEvents(True)  # Enable hover events for the handle
        
    def boundingRect(self) -> QRectF:
        return QRectF(
            -self.SIZE / 2, -self.SIZE / 2, self.SIZE, self.SIZE
        )
    
    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionGraphicsItem,
        widget: QWidget | None = None
    ) -> None:
        
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if self._hovered:
            brush = QBrush(QColor(255, 255, 255))
        else:
            brush = QBrush(QColor(230, 230, 230))
            
        pen = QPen(
            QColor(0, 120, 215),
            1.5
        )
        
        painter.setBrush(brush)
        painter.setPen(pen)
        
        painter.drawRect(
            self.boundingRect()
        )
        
    def hoverEnterEvent(self, event) -> None:
        self._hovered = True
        self.update()  # Trigger a repaint to reflect the hover state
        super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event) -> None:
        self._hovered = False
        self.update()  # Trigger a repaint to reflect the hover state
        super().hoverLeaveEvent(event)
        
    @property
    def position(self) -> HandlePosition:
        return self._position
    
        
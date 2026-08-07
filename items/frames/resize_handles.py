from __future__ import annotations

from PySide6.QtCore import QRectF, Qt
from qtpy.QtGui import QBrush, QColor, QPainter, QPen
from qtpy.QtWidgets import QGraphicsItem, QGraphicsObject, QStyleOptionGraphicsItem, QWidget

from items.enums.handle_position import HandlePosition

class ResizeHandle(QGraphicsObject):
    """
    Interactive resize handle displayed by SelectionFrame. It is used to resize the selected item.
    """
    
    SIZE = 10  # Size of the resize handle in pixels
    
    _CURSOR_MAP: dict[HandlePosition, Qt.CursorShape] = {
        HandlePosition.TOP_LEFT: Qt.CursorShape.SizeFDiagCursor,
        HandlePosition.BOTTOM_RIGHT: Qt.CursorShape.SizeFDiagCursor,

        HandlePosition.TOP_RIGHT: Qt.CursorShape.SizeBDiagCursor,
        HandlePosition.BOTTOM_LEFT: Qt.CursorShape.SizeBDiagCursor,

        HandlePosition.LEFT: Qt.CursorShape.SizeHorCursor,
        HandlePosition.RIGHT: Qt.CursorShape.SizeHorCursor,

        HandlePosition.TOP_CENTER: Qt.CursorShape.SizeVerCursor,
        HandlePosition.BOTTOM_CENTER: Qt.CursorShape.SizeVerCursor,
    }
    
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
        
        pen = QPen(QColor(0, 120, 215), 1.5)
        brush = QBrush(QColor("white"))

        if self._hovered:
            brush = QBrush(QColor(245, 250, 255))

        painter.setPen(pen)
        painter.setBrush(brush)
        
        painter.drawRect(
            self.boundingRect()
        )
        
    def hoverEnterEvent(self, event) -> None:
        self._hovered = True
        self.setCursor(self._CURSOR_MAP[self._position])  # Change cursor based on handle position
        self.update()  # Trigger a repaint to reflect the hover state
        super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event) -> None:
        self._hovered = False
        self.unsetCursor()  # Reset cursor to default
        self.update()  # Trigger a repaint to reflect the hover state
        super().hoverLeaveEvent(event)
        
    @property
    def position(self) -> HandlePosition:
        return self._position
    
        
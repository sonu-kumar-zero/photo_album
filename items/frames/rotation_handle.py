from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from qtpy.QtGui import QBrush, QColor, QPainter, QPen
from qtpy.QtWidgets import QGraphicsObject, QGraphicsItem, QWidget, QStyleOptionGraphicsItem


class RotationHandle(QGraphicsObject):
    """
    Handle used to rotate the selected item.
    """
    
    SIZE = 12.0
    
    rotationStarted = Signal(QPointF)
    rotationMoved = Signal(QPointF)
    rotationFinished = Signal()
    
    def __init__(self, parent: QGraphicsItem | None = None) -> None:
        super().__init__(parent)
        
        self.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)
        
        self.setAcceptHoverEvents(True)
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        
    def boundingRect(self):
        half = self.SIZE / 2
        
        return QRectF(-half, -half, self.SIZE, self.SIZE)
    
    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionGraphicsItem,
        widget: QWidget | None = None
    ) -> None:
        half = self.SIZE / 2
        
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.setPen(QPen(QColor(0, 120, 215), 2))
        
        painter.drawEllipse(
            int(-half), int(-half), int(self.SIZE), int(self.SIZE)
        )
        
    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        
        self.rotationStarted.emit(event.scenePos())
        event.accept()
        
    def mouseMoveEvent(self, event):
        self.rotationMoved.emit(event.scenePos())
        event.accept()
        
    def mouseReleaseEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        
        self.rotationFinished.emit()
        event.accept()

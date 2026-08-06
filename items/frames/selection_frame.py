from __future__ import annotations

from PySide6.QtCore import QRectF, Qt
from qtpy.QtGui import QColor, QPainter, QPen
from qtpy.QtWidgets import QGraphicsObject, QWidget, QStyleOptionGraphicsItem

class SelectionFrame(QGraphicsObject):
    """
    Draws the selection border around a canvasItem.
    Resize handles will be added later.
    """
    
    def __init__(self,
        *,
        owner: QGraphicsObject | None = None
    ):
        super().__init__(owner)
        self.setVisible(False)
        self._pen = QPen(
            QColor(0, 0, 0, 255), 
            2
        )
        
    def boundingRect(self) -> QRectF:
        parent = self.parentItem()
        
        if parent is None:
            return QRectF()
        
        return parent.boundingRect()
    
    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionGraphicsItem,
        widget: QWidget | None = None
    ) -> None:
        parent = self.parentItem()
        if parent is None:
            return
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(self._pen)
        
        painter.drawRect(
            parent.boundingRect()
        )
from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt
from qtpy.QtGui import QColor, QPainter, QPen
from qtpy.QtWidgets import QGraphicsObject, QWidget, QStyleOptionGraphicsItem

from items.frames.resize_handles import ResizeHandle
from items.enums.handle_position import HandlePosition

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
        
        self._handles: dict[HandlePosition, ResizeHandle] = {}
        
        for position in HandlePosition:
            handle = ResizeHandle(position=position, parent=self)
            self._handles[position] = handle
        
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
        self._updateHandlePositions()        
        parent = self.parentItem()
        if parent is None:
            return
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(self._pen)
        
        painter.drawRect(
            parent.boundingRect()
        )
        
    def _updateHandlePositions(self) -> None:
        parent = self.parentItem()
        
        if parent is None:
            return
        
        rect = parent.boundingRect()
        
        left = rect.left()
        right = rect.right()
        
        top = rect.top()
        bottom = rect.bottom()
        
        center_x = rect.center().x()
        center_y = rect.center().y()
        
        positions = {
            HandlePosition.TOP_LEFT: QPointF(left, top),
            HandlePosition.TOP_CENTER: QPointF(center_x, top),
            HandlePosition.TOP_RIGHT: QPointF(right, top),
            
            HandlePosition.LEFT: QPointF(left, center_y),
            HandlePosition.RIGHT: QPointF(right, center_y),
            
            HandlePosition.BOTTOM_LEFT: QPointF(left, bottom),
            HandlePosition.BOTTOM_CENTER: QPointF(center_x, bottom),
            HandlePosition.BOTTOM_RIGHT: QPointF(right, bottom),
        }
        
        for position, point in positions.items():
            self._handles[position].setPos(point)
        
    def updateGeometry(self) -> None:
        self._updateHandlePositions()
        self.update()
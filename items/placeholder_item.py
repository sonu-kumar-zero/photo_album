from __future__ import annotations

from qtpy.QtCore import QRectF, Qt
from qtpy.QtGui import QColor, QFont, QPainter, QPainterPath, QPen
from qtpy.QtWidgets import QGraphicsItem, QGraphicsSceneHoverEvent, QStyleOptionGraphicsItem, QWidget

from items.canvas_item import CanvasItem

class PlaceholderItem(CanvasItem):
    """
    Placeholder item for future implementation.
    """
    
    BORDER_RADIUS = 10.0
    
    def __init__(
        self,
        rect: QRectF,
        parent: QGraphicsItem | None = None,
    ) -> None:
        super().__init__(rect, parent)
        self._hovered = False
        self._text = "Drop Image"
        
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None) -> None:
        rect = self.rect()
        
        path = QPainterPath()
        path.addRoundedRect(
            rect,
            self.BORDER_RADIUS,
            self.BORDER_RADIUS
        )

        # Background
        painter.setBrush(QColor(240, 240, 240))
        
        # Border
        if self.isSelected():
            pen = QPen(self._selected_pen)
        elif self._hovered:
            pen = QPen(
                QColor(255, 170, 0),
                2
            )
        else:
            pen = QPen(self._normal_pen)
        
        pen.setStyle(Qt.PenStyle.DashLine)
        painter.setPen(pen)
        painter.drawPath(path)
        
        # Text
        
        font = QFont()
        font.setPointSize(12)
        painter.setFont(font)
        painter.setPen(
            QColor(120, 120, 120)
        )
        painter.drawText(
            rect,
            Qt.AlignmentFlag.AlignCenter,
            self._text
        )
    
    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self._hovered = True
        self.update()
        return super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self._hovered = False
        self.update()
        return super().hoverLeaveEvent(event)
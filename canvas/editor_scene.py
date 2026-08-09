
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtGui import QColor, QPen
from qtpy.QtCore import QPointF, QRect, QRectF, Qt
from qtpy.QtGui import QKeyEvent, QPainter

from canvas.page_item import PageItem
from items.canvas_item import CanvasItem
from utils.constants import MARGIN

class EditorScene(QGraphicsScene):
    """Graphics scene used by the editor."""

    def __init__(self) -> None:
        super().__init__()

        self._page = PageItem()
        self.addItem(self._page)

        margin = MARGIN

        self.setSceneRect(
            -PageItem.WIDTH / 2 - margin,
            -PageItem.HEIGHT / 2 - margin,
            PageItem.WIDTH + margin * 2,
            PageItem.HEIGHT + margin * 2,
        )
        
    @property
    def page(self) -> PageItem:
        return self._page
    
    def drawBackground(
        self, 
        painter: QPainter, 
        rect: QRectF | QRect
    ) -> None:
        painter.fillRect(
            rect,
            QColor(46, 46, 46)
        )
        
        spacing = 20
        major_spacing = spacing * 5
                
        left = int(rect.left()) - (int(rect.left()) % spacing)
        top = int(rect.top()) - (int(rect.top()) % spacing)
        
        right = int(rect.right())
        bottom = int(rect.bottom())
        
        x = left
        while x <= right:
            y = top
            while y <= bottom:
                
                if x % major_spacing == 0 and y % major_spacing == 0:
                    painter.setPen(QColor(200, 200, 200))
                else:
                    painter.setPen(QColor(100, 100, 100))
                painter.drawPoint(x, y)
                y += spacing
            x += spacing
        
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        size = 20
        
        painter.drawLine(-size, 0, size, 0)
        painter.drawLine(0, -size, 0, size)
        
        radius = 5
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(Qt.PenStyle.NoPen)
        
        painter.drawEllipse(
            QPointF(0, 0),
            radius,
            radius
        )
        
    def deleteSelectedItems(self) -> None:
        selected_items = self.selectedItems()

        for item in selected_items:
            if isinstance(item, CanvasItem):
                self.removeItem(item)
                item.deleteLater()
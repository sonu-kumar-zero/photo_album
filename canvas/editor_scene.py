
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtGui import QColor
from qtpy.QtCore import QRect, QRectF
from qtpy.QtGui import QPainter

from canvas.page_item import PageItem
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
        dot_color = QColor(64, 64, 64)
        painter.setPen(dot_color)
        
        left = int(rect.left()) - (int(rect.left()) % spacing)
        top = int(rect.top()) - (int(rect.top()) % spacing)
        
        right = int(rect.right())
        bottom = int(rect.bottom())
        
        x = left
        while x <= right:
            y = top
            while y <= bottom:
                painter.drawPoint(x, y)
                y += spacing
            x += spacing
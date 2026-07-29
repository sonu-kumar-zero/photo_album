
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtGui import QColor

from canvas.page_item import PageItem

class EditorScene(QGraphicsScene):
    """Graphics scene used by the editor."""

    def __init__(self) -> None:
        super().__init__()

        self.setBackgroundBrush(QColor(45,45,45))

        self._page = PageItem()
        self.addItem(self._page)

        self.setSceneRect(self.itemsBoundingRect().adjusted(
            -500,-500,500,500
        ))

    @property
    def page(self) -> PageItem:
        return self._page
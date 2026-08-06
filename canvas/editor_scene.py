
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtGui import QColor

from canvas.page_item import PageItem
from utils.constants import MARGIN

class EditorScene(QGraphicsScene):
    """Graphics scene used by the editor."""

    def __init__(self) -> None:
        super().__init__()

        self.setBackgroundBrush(QColor(45,45,45))

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
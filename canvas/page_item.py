from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtCore import QRectF
from PySide6.QtGui import QBrush, QColor, QPen

from utils.constants import PAGE_HEIGHT, PAGE_WIDTH

class PageItem(QGraphicsRectItem):
    """Represents a single editable page."""

    WIDTH = PAGE_WIDTH
    HEIGHT = PAGE_HEIGHT

    def __init__(self) -> None:
        super().__init__(QRectF(0, 0, self.WIDTH, self.HEIGHT))

        self.setBrush(QBrush(QColor("white")))
        self.setPen(QPen(QColor(220,220,220), 2))
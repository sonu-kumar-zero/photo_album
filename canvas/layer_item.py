from PySide6.QtCore import QRectF
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QGraphicsObject, QGraphicsItem


class LayerItem(QGraphicsObject):
    """
    Base class for all page layers.

    A layer does not render anything itself. It simply acts as a
    parent/container for other graphics items.
    """
    
    def __init__(
        self,
        *,
        name: str,
        parent: QGraphicsItem | None = None
    ) -> None:
        super().__init__(parent)
        self._name = name

    def boundingRect(self) -> QRectF:
        return QRectF()

    def paint(self, painter: QPainter, option, widget=None) -> None:
        pass
from __future__ import annotations
from typing import Any

from PySide6.QtCore import QRectF, QUuid
from PySide6.QtGui import QColor, QPen, QPainter
from PySide6.QtWidgets import QGraphicsItem, QGraphicsObject

from items.frames.selection_frame import SelectionFrame

class CanvasItem(QGraphicsObject):
    """
    Base class for every editable object on a page.
    """
    """
    Future responsibilities

    - Selection
    - Hover
    - Resize Handles
    - Rotation Handle
    - UUID
    - Serialization
    - Context Menu
    - Locking
    - Visibility
    """

    def __init__(
        self,
        rect: QRectF,
        parent: QGraphicsItem | None = None,
    ) -> None:
        super().__init__(parent)

        self._id = QUuid.createUuid()
        self._rect = QRectF(rect)

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
            True,
        )

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable,
            True,
        )

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges,
            True,
        )

        self.setAcceptHoverEvents(True)

        self._normal_pen = QPen(QColor(180, 180, 180), 1)
        self._selected_pen = QPen(QColor(0, 120, 215), 2)
        
        self._selection_frame = SelectionFrame(owner=self)
        self._selection_frame.resizeRequested.connect(self.setRect)

    @property
    def id(self) -> QUuid:
        return self._id

    def rect(self) -> QRectF:
        return QRectF(self._rect)

    def setRect(self, rect: QRectF) -> None:
        self.prepareGeometryChange()
        self._rect = QRectF(rect)
        self.update()

    def boundingRect(self) -> QRectF:
        return self._rect

    def paint(
        self,
        painter: QPainter,
        option,
        widget=None,
    ) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        raise NotImplementedError
    
    @property
    def width(self) -> float:
        return self._rect.width()
    
    @property
    def height(self) -> float:
        return self._rect.height()

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: Any) -> Any:
        if (
            change == QGraphicsItem.GraphicsItemChange.ItemSelectedHasChanged
        ):
            self._selection_frame.setVisible(bool(value))
        return super().itemChange(change, value)

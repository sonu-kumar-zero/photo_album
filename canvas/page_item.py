from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QBrush, QPainter, QPen
from PySide6.QtWidgets import QGraphicsObject
from typing import cast

from items.canvas_item import CanvasItem
from items.clipboard.clipboard_data import CanvasItemData
from items.placeholder_item import PlaceholderItem
from utils.constants import PAGE_HEIGHT, PAGE_WIDTH
from canvas.layer_item import LayerItem

from items.item_factory import ItemFactory

class PageItem(QGraphicsObject):
    """Represents a single editable page."""

    WIDTH = PAGE_WIDTH
    HEIGHT = PAGE_HEIGHT

    def __init__(self) -> None:
        super().__init__()

        self._rect = QRectF(
            -cast(float, self.WIDTH) / 2,
            -cast(float, self.HEIGHT) / 2,
            cast(float, self.WIDTH),
            cast(float, self.HEIGHT),
        )
        
        self._placeholder_layer = LayerItem(name="Placeholder", parent=self)
        self._text_layer = LayerItem(name="Text", parent=self)
        self._guide_layer = LayerItem(name="Guide", parent=self)
        self._overlay_layer = LayerItem(name="Overlay", parent=self)
        
        self._placeholder = PlaceholderItem(
            QRectF(
                -150,
                -100,
                300,
                200,
            ),
            self._placeholder_layer,
        )
        
        self._placeholder2 = PlaceholderItem(
            QRectF(
                -100,
                50,
                200,
                150,
            ),
            self._placeholder_layer,
        )

    def boundingRect(self) -> QRectF:
        """
        Return the item's bounding rectangle.

        We enlarge it slightly so the shadow is not clipped.
        """

        shadow_margin = 24

        return self._rect.adjusted(
            -shadow_margin,
            -shadow_margin,
            shadow_margin,
            shadow_margin,
        )

    def pageRect(self) -> QRectF:
        """
        Returns the actual page rectangle.
        """

        return self._rect

    def paint(
        self,
        painter: QPainter,
        option,
        widget=None,
    ) -> None:

        rect = self._rect

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        #
        # Shadow
        #

        painter.setPen(Qt.PenStyle.NoPen)

        for i in range(10):

            alpha = max(0, 22 - i * 2)

            painter.setBrush(
                QColor(0, 0, 0, alpha)
            )

            painter.drawRect(
                rect.adjusted(
                    -i,
                    -i,
                    i,
                    i,
                ).translated(6, 6)
            )

        #
        # Page
        #

        painter.setBrush(QBrush(Qt.GlobalColor.white))

        painter.setPen(
            QPen(
                QColor(220, 220, 220),
                2,
            )
        )

        painter.drawRect(rect)
        
    @property
    def placeholderLayer(self) -> LayerItem:
        return self._placeholder_layer
    
    @property
    def textLayer(self) -> LayerItem:
        return self._text_layer
    
    @property
    def guideLayer(self) -> LayerItem:
        return self._guide_layer
    
    @property
    def overlayLayer(self) -> LayerItem:
        return self._overlay_layer

    def layerByName(self, name: str) -> LayerItem | None:
        """
        Returns the layer with the given name, or None if not found.
        """

        for layer in self.childItems():
            if isinstance(layer, LayerItem) and layer.name == name:
                return layer

        return None
    
    def createItemFromData(
        self,
        data: CanvasItemData,
    ) -> CanvasItem:
        
        layer = self.layerByName(data.layer_name)
        if layer is None:
            raise ValueError(f"Layer '{data.layer_name}' not found")
        
        return ItemFactory.create(data, parent=layer)
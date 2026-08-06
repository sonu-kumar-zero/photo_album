from __future__ import annotations

from qtpy.QtCore import QRectF, Qt
from qtpy.QtGui import QColor, QFont, QPainter, QPainterPath, QPen
from qtpy.QtWidgets import (
    QGraphicsItem,
    QGraphicsSceneHoverEvent,
    QStyleOptionGraphicsItem,
    QWidget,
)

from items.canvas_item import CanvasItem
from utils.icon_cache import IconCache
from items.layouts.placeholder_layout import PlaceholderLayout

class PlaceholderItem(CanvasItem):
    """
    Placeholder item where users can drop images.
    """

    BORDER_RADIUS = 10.0
    ICON_SIZE = 48

    def __init__(
        self,
        rect: QRectF,
        parent: QGraphicsItem | None = None,
    ) -> None:
        super().__init__(rect, parent)

        self._hovered = False

        self._text = "Drop Image"
        self._subtitle = "Drag & Drop or Double-click"

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionGraphicsItem,
        widget: QWidget | None = None,
    ) -> None:
        rect = self.rect()

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        #
        # Rounded path
        #

        path = QPainterPath()
        path.addRoundedRect(
            rect,
            self.BORDER_RADIUS,
            self.BORDER_RADIUS,
        )

        #
        # Background
        #

        if self._hovered:
            background = QColor(248, 248, 248)
        else:
            background = QColor(240, 240, 240)

        painter.fillPath(path, background)

        #
        # Border
        #

        if self.isSelected():
            pen = QPen(self._selected_pen)

        elif self._hovered:
            pen = QPen(QColor(255, 170, 0), 2)

        else:
            pen = QPen(self._normal_pen)

        pen.setDashPattern([6, 4])

        painter.setPen(pen)
        painter.drawPath(path)

        #
        # Icon
        #
        
        layout = self._calculate_layout()

        icon = IconCache.pixmap(
            "image_placeholder",
            self.ICON_SIZE,
        )

        icon_rect = layout.icon_rect

        painter.drawPixmap(
            icon_rect.toRect(),
            icon,
        )

        #
        # Title
        #

        title_rect = layout.title_rect

        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)

        painter.setFont(title_font)
        painter.setPen(QColor(70, 70, 70))

        painter.drawText(
            title_rect,
            Qt.AlignmentFlag.AlignCenter,
            self._text,
        )

        #
        # Subtitle
        #

        subtitle_rect = layout.subtitle_rect

        subtitle_font = QFont()
        subtitle_font.setPointSize(9)

        painter.setFont(subtitle_font)
        painter.setPen(QColor(130, 130, 130))

        painter.drawText(
            subtitle_rect,
            Qt.AlignmentFlag.AlignCenter,
            self._subtitle,
        )

    def hoverEnterEvent(
        self,
        event: QGraphicsSceneHoverEvent,
    ) -> None:
        self._hovered = True
        self.update()

        super().hoverEnterEvent(event)

    def hoverLeaveEvent(
        self,
        event: QGraphicsSceneHoverEvent,
    ) -> None:
        self._hovered = False
        self.update()

        super().hoverLeaveEvent(event)
        
    def _calculate_layout(self) -> PlaceholderLayout:
        """
        Calculate the layout of the placeholder item.
        """

        rect = self.rect()

        icon_rect = QRectF(
            rect.center().x() - self.ICON_SIZE / 2,
            rect.center().y() - 60,
            self.ICON_SIZE,
            self.ICON_SIZE,
        )

        title_rect = QRectF(
            rect.left() + 10,
            icon_rect.bottom() + 10,
            rect.width() - 20,
            24,
        )

        subtitle_rect = QRectF(
            rect.left() + 10,
            title_rect.bottom() + 2,
            rect.width() - 20,
            20,
        )

        return PlaceholderLayout(
            icon_rect=icon_rect,
            title_rect=title_rect,
            subtitle_rect=subtitle_rect,
        )

from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtGui import QColor, QPen
from qtpy.QtCore import QPointF, QRect, QRectF, Qt
from qtpy.QtGui import QKeyEvent, QPainter

from canvas.page_item import PageItem
from items.canvas_item import CanvasItem
from items.clipboard.clipboard_data import CanvasItemData
from items.item_factory import ItemFactory
from items.placeholder_item import PlaceholderItem
from utils.constants import MARGIN

from items.clipboard.editor_clipboard import EditorClipboard


class EditorScene(QGraphicsScene):
    """Graphics scene used by the editor."""

    def __init__(self) -> None:
        super().__init__()

        self._page = PageItem()
        self.addItem(self._page)
        
        self._current_page = self._page

        margin = MARGIN

        self.setSceneRect(
            -PageItem.WIDTH / 2 - margin,
            -PageItem.HEIGHT / 2 - margin,
            PageItem.WIDTH + margin * 2,
            PageItem.HEIGHT + margin * 2,
        )
        
        self._clipboard_item: CanvasItem | None = None
        
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
    
    def duplicateSelectedItems(self) -> None:
        selected_items = self.selectedItems()
        
        if not selected_items:
            return
        
        new_items: list[CanvasItem] = []
        
        for item in selected_items:
            if not isinstance(item, CanvasItem):
                continue
            
            duplicate = item.duplicate()
            
            duplicate.setPos(
                item.pos() + QPointF(20, 20)
            )
            
            self.addItem(duplicate)
            
            new_items.append(duplicate)
            
        self.clearSelection()
        
        for item in new_items:
            item.setSelected(True)
    
    def copySelectedItemsToClipboard(self) -> None:
        selected_items = self.selectedItems()
        
        if len(selected_items) != 1:
            return
        
        item = selected_items[0]
        
        if not isinstance(item, CanvasItem):
            EditorClipboard.clear()
            return
        
        EditorClipboard.setData(item.copyData())

    def pasteFromClipboard(self) -> None:      
        if not EditorClipboard.hasData():
            return
        
        data = EditorClipboard.data()
        
        if not isinstance(data, CanvasItemData):
            return
        
        page = self._current_page
        
        if page is None:
            return
        
        new_item = page.createItemFromData(data)
        
        new_item.setPos(
            data.pos + QPointF(20, 20)
        )        
        
        self.clearSelection()
        new_item.setSelected(True)
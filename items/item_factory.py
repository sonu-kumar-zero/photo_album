from __future__ import annotations
from collections.abc import Callable

from qtpy.QtWidgets import QGraphicsItem

from items.canvas_item import CanvasItem
from items.clipboard.clipboard_data import CanvasItemData
from items.placeholder_item import PlaceholderItem

class ItemFactory:

    _registry: dict[
        str,
        Callable[
            [CanvasItemData, QGraphicsItem | None],
            CanvasItem,
        ]
    ] = {
        "PlaceholderItem": PlaceholderItem.fromData,
    }
    
    @classmethod
    def create(
        cls,
        data: CanvasItemData,
        parent: QGraphicsItem | None = None,
    ) -> CanvasItem:
        creator = cls._registry.get(data.item_type)
        
        if creator is None:
            raise ValueError(f"Unknown item type: {data.item_type}")
        
        return creator(data, parent)
from __future__ import annotations

from pathlib import Path
from qtpy.QtCore import QSize
from qtpy.QtGui import QIcon, QPixmap

class IconCache:
    """
    Centralized cache for icons to avoid reloading them multiple times.
    """
    
    _cache: dict[tuple[str,int], QPixmap] = {}
    
    _icon_dir = (
        Path(__file__).resolve().parent.parent / "resources" / "icons"
    )
    
    @classmethod
    def pixmap(
        cls,
        name: str,
        size: int = 16
    ) -> QPixmap:
        """
        Get a QPixmap for the given icon name and size.
        
        If the icon is not already cached, it will be loaded from disk.
        """
        key = (name, size)
        if key not in cls._cache:
            icon = QIcon(
                str(cls._icon_dir / f"{name}.svg")
            )
            cls._cache[key] = icon.pixmap(
                QSize(size, size)
            )
        return cls._cache[key]
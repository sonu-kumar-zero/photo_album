from __future__ import annotations

from typing import Any


class EditorClipboard:
    """
    Internal clipboard used by ImageBook.
    """

    _data: Any = None

    @classmethod
    def setData(cls, data: Any) -> None:
        cls._data = data

    @classmethod
    def data(cls) -> Any:
        return cls._data

    @classmethod
    def hasData(cls) -> bool:
        return cls._data is not None

    @classmethod
    def clear(cls) -> None:
        cls._data = None
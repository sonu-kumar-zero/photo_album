from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from qtpy.QtGui import QColor, QPainter, QPen
from qtpy.QtWidgets import QApplication, QGraphicsObject, QWidget, QStyleOptionGraphicsItem

from items.frames.resize_handles import ResizeHandle
from items.enums.handle_position import HandlePosition
from items.interactions.resize_state import ResizeState

from items.geometry.resize_algorithm import ResizeAlgorithm

class SelectionFrame(QGraphicsObject):
    """
    Draws the selection border around a canvasItem.
    Resize handles will be added later.
    """
    
    MIN_WIDTH = 50.0
    MIN_HEIGHT = 50.0
    
    resizeRequested = Signal(QRectF)  # Signal emitted when the selection frame's rectangle changes
    
    def __init__(self,
        *,
        owner: QGraphicsObject | None = None
    ):
        super().__init__(owner)
        self.setVisible(False)
        self._pen = QPen(
            QColor(0, 0, 0, 255), 
            2
        )
        
        self._handles: dict[HandlePosition, ResizeHandle] = {}
        
        for position in HandlePosition:
            handle = ResizeHandle(position=position, parent=self)
            self._handles[position] = handle
        
        for handle in self._handles.values():
            handle.resizeStarted.connect(self._onResizeStarted)
            handle.resizeMoved.connect(self._onResizeMoved)
            handle.resizeFinished.connect(self._onResizeFinished)
            
        self._resize_state: ResizeState | None = None
        self._owner = owner
        
    def boundingRect(self) -> QRectF:
        if self._owner is None:
            return QRectF()
        
        return self._owner.boundingRect()
    
    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionGraphicsItem,
        widget: QWidget | None = None
    ) -> None:
        self._updateHandlePositions()        
        if self._owner is None:
            return
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(self._pen)
        
        painter.drawRect(
            self._owner.boundingRect()
        )
        
    def _updateHandlePositions(self) -> None:
        if self._owner is None:
            return
        
        rect = self._owner.boundingRect()
        
        left = rect.left()
        right = rect.right()
        
        top = rect.top()
        bottom = rect.bottom()
        
        center_x = rect.center().x()
        center_y = rect.center().y()
        
        positions = {
            HandlePosition.TOP_LEFT: QPointF(left, top),
            HandlePosition.TOP_CENTER: QPointF(center_x, top),
            HandlePosition.TOP_RIGHT: QPointF(right, top),
            
            HandlePosition.LEFT: QPointF(left, center_y),
            HandlePosition.RIGHT: QPointF(right, center_y),
            
            HandlePosition.BOTTOM_LEFT: QPointF(left, bottom),
            HandlePosition.BOTTOM_CENTER: QPointF(center_x, bottom),
            HandlePosition.BOTTOM_RIGHT: QPointF(right, bottom),
        }
        
        for position, point in positions.items():
            self._handles[position].setPos(point)
        
    def updateGeometry(self) -> None:
        self._updateHandlePositions()
        self.update()
        
    def _onResizeStarted(
        self,
        handle: HandlePosition,
        scene_pos: QPointF
    )->None:    
        if self._owner is None:
            return
        
        keep_aspect_ratio = bool(
            QApplication.keyboardModifiers() 
            & Qt.KeyboardModifier.ShiftModifier
        )
        
        self._resize_state = ResizeState(
            handle=handle,
            start_rect=self._owner.boundingRect(),
            start_scene_pos=scene_pos,
            keep_aspect_ratio=keep_aspect_ratio
        )
    
    def _onResizeMoved(
        self,
        handle: HandlePosition,
        scene_pos: QPointF
    ) -> None:
        if self._resize_state is None:
            return
        
        delta = (
            scene_pos - self._resize_state.start_scene_pos
        )
        
        rect = ResizeAlgorithm.resize(
            rect=self._resize_state.start_rect,
            handle=handle,
            delta=delta,
            min_width=self.MIN_WIDTH,
            min_height=self.MIN_HEIGHT,
            keep_aspect_ratio=self._resize_state.keep_aspect_ratio
        )
        
        self.resizeRequested.emit(rect)
    
    def _onResizeFinished(self) -> None:
        self._resize_state = None
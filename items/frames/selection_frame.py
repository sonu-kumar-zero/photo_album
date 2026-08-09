from __future__ import annotations
from math import atan2, degrees

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from qtpy.QtGui import QColor, QPainter, QPen
from qtpy.QtWidgets import QApplication, QGraphicsObject, QWidget, QStyleOptionGraphicsItem

from items.frames.resize_handles import ResizeHandle
from items.enums.handle_position import HandlePosition
from items.frames.rotation_handle import RotationHandle
from items.interactions.resize_state import ResizeState

from items.geometry.resize_algorithm import ResizeAlgorithm
from items.interactions.rotation_state import RotationState

class SelectionFrame(QGraphicsObject):
    """
    Draws the selection border around a canvasItem.
    Resize handles will be added later.
    """
    
    MIN_WIDTH = 50.0
    MIN_HEIGHT = 50.0
    
    resizeRequested = Signal(QRectF)  # Signal emitted when the selection frame's rectangle changes
    rotationRequested = Signal(float)  # Signal emitted when the selection frame's rotation changes
    
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
        self._rotation_handle = RotationHandle(parent=self)
        
        for position in HandlePosition:
            handle = ResizeHandle(position=position, parent=self)
            self._handles[position] = handle
        
        for handle in self._handles.values():
            handle.resizeStarted.connect(self._onResizeStarted)
            handle.resizeMoved.connect(self._onResizeMoved)
            handle.resizeFinished.connect(self._onResizeFinished)
            
        self._rotation_handle.rotationStarted.connect(
            self._onRotationStarted
        )
        
        self._rotation_handle.rotationMoved.connect(
            self._onRotationMoved
        )
        self._rotation_handle.rotationFinished.connect(
            self._onRotationFinished
        )
            
        self._resize_state: ResizeState | None = None
        self._owner = owner
        
        self._rotation_state: RotationState | None = None
        
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
        
        self._rotation_handle.setPos(
            rect.center().x(),
            rect.top() - 30
        )
        
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
        
    def _onRotationStarted(self, scene_pos: QPointF) -> None:
        # Handle rotation start logic here
        parent = self.parentItem()
        
        if parent is None:
            return
        
        center_scene = parent.mapToScene(parent.transformOriginPoint())
        
        
        self._rotation_state = RotationState(
            start_scene_pos=scene_pos,
            start_rotation=parent.rotation(),
            center_scene_pos=center_scene
        )
    
    def _onRotationMoved(self, scene_pos: QPointF) -> None:
        # Handle rotation move logic here
        if self._rotation_state is None or self._owner is None:
            return
        
        state = self._rotation_state
        start_vector = (
            state.start_scene_pos
            - state.center_scene_pos
        )
        
        current_vector = (
            scene_pos
            - state.center_scene_pos
        )
        
        start_angle = degrees(
            atan2(
                start_vector.y(),
                start_vector.x()
            )
        )
        
        current_angle = degrees(
            atan2(
                current_vector.y(),
                current_vector.x()
            )
        )
        
        delta_angle = current_angle - start_angle
        
        rotation = (
            state.start_rotation + delta_angle
        )
        
        self.rotationRequested.emit(rotation)
        
    def _onRotationFinished(self) -> None:
        # Handle rotation finish logic here
        self._rotation_state = None
    
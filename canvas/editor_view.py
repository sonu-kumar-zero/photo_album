from PySide6.QtWidgets import QGraphicsScene, QGraphicsView
from PySide6.QtCore import Qt, QPoint
from qtpy.QtGui import QMouseEvent, QPainter, QWheelEvent

from canvas.editor_scene import EditorScene
from utils.constants import MIN_ZOOM, MAX_ZOOM, ZOOM_FACTOR

class EditorView(QGraphicsView):
    """Graphics view used by the editor"""

    def __init__(self, scene: QGraphicsScene) -> None:
        super().__init__(scene)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setRenderHints(
            QPainter.RenderHint.Antialiasing
            | QPainter.RenderHint.TextAntialiasing
            | QPainter.RenderHint.SmoothPixmapTransform
        )

        self.setFrameShape(QGraphicsView.Shape.NoFrame)

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)

        self._zoom = 1.0
        self._min_zoom = MIN_ZOOM
        self._max_zoom = MAX_ZOOM
        self._zoom_factor = ZOOM_FACTOR

        self._is_panning = False
        self._last_pan_point = QPoint()

    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.angleDelta().y() > 0:
            factor = self._zoom_factor
        else:
            factor = 1 / self._zoom_factor

        new_zoom = self._zoom * factor

        if not (self._min_zoom <= new_zoom <= self._max_zoom):
            return super().wheelEvent(event)

        self._zoom = new_zoom
        self.scale(factor, factor)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.MiddleButton:
            self._is_panning = True
            self._last_pan_point = event.pos()

            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
            return
        
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._is_panning:
            delta = event.pos() - self._last_pan_point
            self._last_pan_point = event.pos()

            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta.x()
            )

            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta.y()
            )
            
            event.accept()
            return

        return super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.MiddleButton:
            self._is_panning = False
            self.unsetCursor()
            
            event.accept()
            return
        return super().mouseReleaseEvent(event)
    
    def keyPressEvent(self, event) -> None:
        
        if (
            event.key() == Qt.Key.Key_C
            and event.modifiers() 
            & Qt.KeyboardModifier.ControlModifier
        ): 
            scene = self.scene()
            if isinstance(scene, EditorScene):
                scene.copySelectedItemsToClipboard()
            
            event.accept()
            return
        
        if (
            event.key() == Qt.Key.Key_V
            and event.modifiers() 
            & Qt.KeyboardModifier.ControlModifier
        ): 
            scene = self.scene()
            if isinstance(scene, EditorScene):
                scene.pasteFromClipboard()
            
            event.accept()
            return
        
        
        if (
            event.key() == Qt.Key.Key_D
            and event.modifiers() 
            & Qt.KeyboardModifier.ControlModifier
        ): 
            scene = self.scene()
            if isinstance(scene, EditorScene):
                scene.duplicateSelectedItems()
            
            event.accept()
            return
        
        if event.key() in {
            Qt.Key.Key_Delete,
            Qt.Key.Key_Backspace
        }:
            scene = self.scene()
            
            if isinstance(scene, EditorScene):
                scene.deleteSelectedItems()
            event.accept()
            return
        
        super().keyPressEvent(event)
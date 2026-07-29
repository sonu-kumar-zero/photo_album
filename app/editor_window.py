from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

from canvas.editor_scene import EditorScene
from canvas.editor_view import EditorView

class EditorWindow(QMainWindow):
    """main application window"""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Image Editor")
        self.resize(1600,900)

        self.scene = EditorScene()
        self.view = EditorView(self.scene)

        self.setCentralWidget(self.view)
import sys

from PySide6.QtWidgets import QApplication

from app.editor_window import EditorWindow

def main() -> None:
    app = QApplication(sys.argv)

    window = EditorWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
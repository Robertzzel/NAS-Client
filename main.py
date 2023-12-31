import sys
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget
from app import MainUI
from ui_functions import UIFunctions


class AVGui(QMainWindow):
    getPathSignal = Signal(bool)
    listFilesSignal = Signal()
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowFlags(Qt.FramelessWindowHint))
        self.ui = MainUI(self)
        self.ui_functions = UIFunctions(self, self.ui)

    # Move Window with mouse
    def mousePressEvent(self, event):
        self.dragPos = self.pos()
        self.mouse_original_pos = self.mapToGlobal(event.pos())

    def mouseMoveEvent(self, event):
        if self.isMaximized():
            self.showNormal()
        else:
            if event.buttons() == Qt.LeftButton:
                last_pos = self.dragPos + self.mapToGlobal(event.pos()) - self.mouse_original_pos
                self.move(last_pos)
                event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        win = AVGui()
    except Exception as ex:
        print(ex)
        sys.exit(1)
    win.show()
    sys.exit(app.exec_())


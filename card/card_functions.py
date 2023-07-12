import pathlib
import types

from PySide6.QtGui import QPixmap
from card.card import Card

def get_card(parent, isDire: bool, name: str, cb1, cb2, doubleClickCB=None):
    dir_pixmap = QPixmap(str(pathlib.Path(__file__).parent.parent / "images" / "directory.png"))
    file_pixmap = QPixmap(str(pathlib.Path(__file__).parent.parent / "images" / "file.png"))

    card = Card(parent)
    card.resize(100, 100)
    card.name_label.setText(name)
    if isDire:
        image = dir_pixmap
    else:
        image = file_pixmap

    #card.image_label.setFixedSize(100, 100)
    card.image_label.setPixmap(image)
    if doubleClickCB is not None:
        card.mouseDoubleClickEvent = types.MethodType(doubleClickCB, Card)

    card.button_1.setText("DOWNLOAD")
    card.button_2.setText("DELETE")
    card.button_1.clicked.connect(cb1)
    card.button_2.clicked.connect(cb2)
    return card

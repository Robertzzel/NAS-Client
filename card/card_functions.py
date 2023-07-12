import pathlib
import types

from PySide6.QtGui import QPixmap
from card.card import Card


def get_card(parent, isDire: bool, name: str, cb1, cb2, doubleClickCB=None):
    card = Card(parent)
    card.name_label.setText(name)

    if isDire:
        image = QPixmap(str(pathlib.Path(__file__).parent.parent / "images" / "directory.png"))
    else:
        image = QPixmap(str(pathlib.Path(__file__).parent.parent / "images" / "file.png"))

    card.image_label.setPixmap(image)
    if doubleClickCB is not None:
        card.mouseDoubleClickEvent = types.MethodType(doubleClickCB, Card)

    card.button_1.setText("DOWNLOAD")
    card.button_2.setText("DELETE")
    card.button_1.clicked.connect(cb1)
    card.button_2.clicked.connect(cb2)
    return card

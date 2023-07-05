import socket
import ssl

from PySide6 import QtWidgets
from app import MainUI


class UIFunctions:
    def __init__(self, mainWindow, ui):
        self.mainWindow = mainWindow
        self.ui: MainUI = ui
        self.setup()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)
        self.tlsSocket = ssl.wrap_socket(self.sock, ssl_version=ssl.PROTOCOL_TLSv1_2)
        #try:
            #self.tlsSocket.connect(("licenta-robert-1.go.ro", 4040))
        #except Exception as e:
        self.tlsSocket.connect(("192.168.1.5", 4040))

    def setup(self):
        # top buttons
        self.ui.exit_button.clicked.connect(self.mainWindow.close)
        self.ui.minimze_button.clicked.connect(self.mainWindow.showMinimized)

        # side bar buttons
        self.ui.login_page_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.browse_page_button.clicked.connect(self.setBrowserPage)

    def receiveMessage(self):
        message = bytearray()
        messageLengthSize = self.tlsSocket.recv(10)
        messageSize = int(messageLengthSize.decode())

        while len(message) < messageSize:
            message.extend(self.tlsSocket.recv(2048))

        return message[1:], message[0]

    def sendMessage(self, message: bytes):
        msgSize = str(len(message)).rjust(10, '0').encode()
        self.tlsSocket.send(msgSize)
        self.tlsSocket.send(message)

    def setBrowserPage(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.listCurrentDirectory()

    def addRowToBowser(self, type: str, name: str):
        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout.setObjectName("horizontalLayout")

        durationLabel = QtWidgets.QLabel(parent=self.ui.browse_page)
        durationLabel.setObjectName("label")
        durationLabel.setStyleSheet("color: rgb(161, 168, 166);")
        durationLabel.setText(type)
        horizontalLayout.addWidget(durationLabel)

        sizeLabel = QtWidgets.QLabel(parent=self.ui.browse_page)
        sizeLabel.setObjectName("label_2")
        sizeLabel.setStyleSheet("color: rgb(161, 168, 166);")
        horizontalLayout.addWidget(sizeLabel)
        sizeLabel.setText(name)

        if type == "File":
            pushButton = QtWidgets.QPushButton(parent=self.ui.browse_page)
            pushButton.setObjectName("pushButton")
            pushButton.setStyleSheet("color: rgb(161, 168, 166);")
            pushButton.setText("DOWNLOAD")
            #pushButton.clicked.connect(callback)
            horizontalLayout.addWidget(pushButton)
        else:
            deleteVideoButton = QtWidgets.QPushButton(parent=self.ui.browse_page)
            deleteVideoButton.setObjectName("deleteVideoButton")
            deleteVideoButton.setText("GO IN")
            deleteVideoButton.setStyleSheet("color: rgb(161, 168, 166);")
            #deleteVideoButton.clicked.connect(deleteVideo)
            horizontalLayout.addWidget(deleteVideoButton)

        self.ui.browse_page_layout.addLayout(horizontalLayout)

    def resetBrowser(self):
        self.clearLayout(self.ui.browse_page_layout)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            if child.layout():
                self.clearLayout(child.layout())

    def listCurrentDirectory(self):
        self.sendMessage(b"0")
        msg, status = self.receiveMessage()
        if status != 0:
            pass

        self.resetBrowser()

        msgContents = (i.split(":") for i in msg.decode().split(";"))
        for elem in msgContents:
            if elem[0] == "":
                continue
            self.addRowToBowser(elem[0], elem[1])


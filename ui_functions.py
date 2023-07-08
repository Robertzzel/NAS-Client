import os
import shutil
import socket
import ssl
import tempfile
from typing import IO

from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog, QMessageBox

from app import MainUI
from operations import Operations


class UIFunctions:
    def __init__(self, mainWindow, ui):
        self.mainWindow = mainWindow
        self.ui: MainUI = ui
        self.setup()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(100)
        self.tlsSocket = ssl.wrap_socket(self.sock, ssl_version=ssl.PROTOCOL_TLSv1_2)

        res = self.connectSocket()
        if not res:
            message_box = QMessageBox()
            message_box.setText("The programming tried to connect to the server but it did not work.")
            message_box.setWindowTitle("Cannot connect to server")
            message_box.setIcon(QMessageBox.Icon.Information)
            message_box.exec()
            raise Exception("Cannot connect")

    def connectSocket(self):
        try:
            self.tlsSocket.connect(("192.168.1.5", 4040))
            return True
        except Exception as e:
            return False

    def setup(self):
        # top buttons
        self.ui.exit_button.clicked.connect(self.mainWindow.close)
        self.ui.minimze_button.clicked.connect(self.mainWindow.showMinimized)

        # side bar buttons
        self.ui.login_page_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.browse_page_button.clicked.connect(self.setBrowserPage)
        self.ui.browse_page_button.setEnabled(False)

        #login page
        self.ui.login_button.clicked.connect(self.login)

        self.ui.exit_directory_button.clicked.connect(self.goOutDirectory)
        self.ui.add_file_button.clicked.connect((lambda checked=True, id=False: self.uploadFileOrDirectory(id)))
        self.ui.add_directory_button.clicked.connect((lambda checked=True, id=True: self.uploadFileOrDirectory(id)))

    def login(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        self.sendMessage(f"{username},{password}".encode())
        msg, status = self.receiveMessage()
        if status != 0:
            print(msg)
            return

        self.ui.browse_page_button.setEnabled(True)

    def receiveMessage(self):
        message = bytearray()
        messageLengthSize = self.tlsSocket.recv(10)
        messageSize = int(messageLengthSize.decode())

        while len(message) < messageSize:
            message.extend(self.tlsSocket.recv(2048))

        return message[1:], message[0]

    def receiveFileMessage(self, file: IO):
        messageLengthSize = self.tlsSocket.recv(10)
        messageSize = int(messageLengthSize.decode())
        receivedBytes = 0
        status = 1

        while receivedBytes < 1:
            message = self.tlsSocket.recv(1)
            receivedBytes += len(message)
            status = int(message[0])

        if status != 0:
            return

        while receivedBytes < messageSize:
            message = self.tlsSocket.recv(2048)
            file.write(message)
            receivedBytes += len(message)

    def sendMessage(self, message: bytes):
        msgSize = str(len(message)).rjust(10, '0').encode()
        self.tlsSocket.send(msgSize)
        self.tlsSocket.send(message)

    def uploadFile(self, fileName: str):
        stats = os.stat(fileName)

        self.sendMessage(str(Operations.UploadFile.value).encode())
        self.sendMessage(fileName.split("/")[-1].encode())

        msgSize = str(stats.st_size).rjust(10, '0').encode()
        self.tlsSocket.send(msgSize)

        with open(fileName, "rb") as f:
            while True:
                chunk = f.read(2048)
                if not chunk:
                    break
                self.tlsSocket.send(chunk)

    def uploadDirectory(self, directoryName: str):
        tmp_archive = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
        tmp_archive.close()
        fileName = shutil.make_archive(tmp_archive.name, 'zip', directoryName)

        self.sendMessage(str(Operations.UploadDirectory.value).encode())
        self.sendMessage(directoryName.split("/")[-1].encode())

        stats = os.stat(fileName)
        msgSize = str(stats.st_size).rjust(10, '0').encode()
        self.tlsSocket.send(msgSize)

        with open(fileName, "rb") as f:
            while True:
                chunk = f.read(2048)
                if not chunk:
                    break
                self.tlsSocket.send(chunk)

        msg, status = self.receiveMessage()
        if status != 0:
            print("Nu a mers")

        self.listCurrentDirectory()
        os.remove(fileName)

    def setBrowserPage(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.listCurrentDirectory()

    def getRowFromTypeAndName(self, type: str, name: str):
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

        downloadButton = QtWidgets.QPushButton(parent=self.ui.browse_page)
        downloadButton.setObjectName("pushButton")
        downloadButton.setStyleSheet("color: rgb(161, 168, 166);")
        downloadButton.setText("DOWNLOAD")
        downloadButton.clicked.connect(lambda checked=True, id=name: self.downloadFile(id))
        horizontalLayout.addWidget(downloadButton)

        if type != "File":
            goInDirectoryButton = QtWidgets.QPushButton(parent=self.ui.browse_page)
            goInDirectoryButton.setObjectName("deleteVideoButton")
            goInDirectoryButton.setText("GO IN")
            goInDirectoryButton.setStyleSheet("color: rgb(161, 168, 166);")
            goInDirectoryButton.clicked.connect((lambda checked=True, id=name: self.goInDirectory(id)))
            horizontalLayout.addWidget(goInDirectoryButton)

        deleteButton = QtWidgets.QPushButton(parent=self.ui.browse_page)
        deleteButton.setObjectName("deleteButton")
        deleteButton.setText("DELETE")
        deleteButton.setStyleSheet("color: rgb(161, 168, 166);")
        deleteButton.clicked.connect((lambda checked=True, id=name: self.deleteFileOrDirectory(id)))
        horizontalLayout.addWidget(deleteButton)

        return horizontalLayout

    def downloadFile(self, file: str):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        if dialog.exec() != QFileDialog.DialogCode.Accepted:
            return

        directory = dialog.selectedFiles()[0] + "/"
        self.sendMessage(str(Operations.GetFile.value).encode())
        self.sendMessage(file.encode())

        with open(f"{directory}{file}", "wb") as f:
            self.receiveFileMessage(f)

    def goInDirectory(self, dir: str):
        self.sendMessage(str(Operations.GoInDirectory.value).encode())
        self.sendMessage(dir.encode())
        msg, status = self.receiveMessage()
        if status != 0:
            print("Nu a mers")
            return

        self.listCurrentDirectory()

    def goOutDirectory(self):
        self.sendMessage(str(Operations.GoOutDirectory.value).encode())
        msg, status = self.receiveMessage()
        if status != 0:
            print("Nu a mers")
            return

        self.listCurrentDirectory()

    def deleteFileOrDirectory(self, name: str):
        self.sendMessage(str(Operations.Delete.value).encode())
        self.sendMessage(name.encode())
        msg, status = self.receiveMessage()
        if status != 0:
            print("Nu a mers")
            return
        self.listCurrentDirectory()

    def resetBrowser(self):
        self.clearLayout(self.ui.browse_page_layout)

    def clearLayout(self, layout, exceptions=("horizontalLayout_2","scrollArea")):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() and child.widget().objectName() not in exceptions:
                child.widget().deleteLater()
            if child.layout() and child.layout().objectName() not in exceptions:
                self.clearLayout(child.layout())

    def listCurrentDirectory(self):
        self.sendMessage(str(Operations.GetFiles.value).encode())
        msg, status = self.receiveMessage()
        if status != 0:
            return

        self.resetBrowser()

        msgContents = [i.split(":") for i in msg.decode().split(";")]

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")

        currentDir = msgContents[0][1]
        self.ui.cueent_diretory_label.setText(currentDir)
        for elem in msgContents[1:]:
            if elem[0] == "":
                continue
            try:
                self.verticalLayout.addLayout(self.getRowFromTypeAndName(elem[0], elem[1]))
            except:
                print(elem)

        self.ui.scrollArea.setWidget(self.scrollAreaWidgetContents)

    def uploadFileOrDirectory(self, isDir: bool):
        dialog = QFileDialog()
        if isDir:
            dialog.setFileMode(QFileDialog.Directory)
            dirname = dialog.getExistingDirectory(None, "Select Directory")
            if dirname == '':
                return
            self.uploadDirectory(dirname)
        else:
            dialog.setFileMode(QFileDialog.AnyFile)
            if not dialog.exec():
                return
            filename = dialog.selectedFiles()[0]
            self.uploadFile(filename)



import os
import queue
import shutil
import socket
import ssl
import tempfile
from typing import IO
from concurrent.futures import ThreadPoolExecutor
from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFileDialog, QMessageBox

from app import MainUI
from card.card_functions import get_card
from operations import Operations


class UIFunctions:

    def __init__(self, mainWindow, ui):
        self.mainWindow = mainWindow
        self.ui: MainUI = ui
        self.setup()
        self.threadPool = ThreadPoolExecutor(1)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(100)
        self.tlsSocket = ssl.wrap_socket(self.sock, ssl_version=ssl.PROTOCOL_TLSv1_2)
        self.uiQueue = queue.Queue()
        self.currentFiles = []

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
            self.tlsSocket.connect(("localhost", 4040))
            return True
        except Exception as e:
            return False

    def setup(self):
        # top buttons
        self.ui.exit_button.clicked.connect(self.mainWindow.close)
        self.ui.minimze_button.clicked.connect(self.mainWindow.showMinimized)

        # sidebar buttons
        self.ui.login_page_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.browse_page_button.clicked.connect(self.setBrowserPage)
        self.ui.browse_page_button.setEnabled(True)

        #login page
        self.ui.login_button.clicked.connect(lambda: self.threadPool.submit(self.login))

        self.ui.exit_directory_button.clicked.connect(self.goOutDirectory)
        self.ui.add_file_button.clicked.connect((lambda checked=True, id=False: self.threadPool.submit(self.uploadFileOrDirectory, (id))))
        self.ui.add_directory_button.clicked.connect((lambda checked=True, id=True: self.threadPool.submit(self.uploadFileOrDirectory, (id))))

        self.mainWindow.getPathSignal.connect(self.getPathCallback)
        self.mainWindow.listFilesSignal.connect(self.listCurrentDirectory)

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

        self.mainWindow.listFilesSignal.emit()
        os.remove(fileName)

    def setBrowserPage(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.mainWindow.listFilesSignal.emit()

    def downloadFile(self, file: str):
        self.mainWindow.getPathSignal.emit(True)

        directory = self.uiQueue.get() + "/"
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

        self.mainWindow.listFilesSignal.emit()

    def goOutDirectory(self):
        self.sendMessage(str(Operations.GoOutDirectory.value).encode())
        msg, status = self.receiveMessage()
        if status != 0:
            print("Nu a mers")
            return

        self.mainWindow.listFilesSignal.emit()

    def deleteFileOrDirectory(self, name: str):
        self.sendMessage(str(Operations.Delete.value).encode())
        self.sendMessage(name.encode())
        msg, status = self.receiveMessage()
        if status != 0:
            print("Nu a mers")
            return
        self.mainWindow.listFilesSignal.emit()

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

        self.currentFiles = [i.split(":") for i in msg.decode().split(";")]

        self.resetBrowser()
        scrollAreaWidgetContents = QtWidgets.QWidget()
        verticalLayout = QtWidgets.QVBoxLayout(scrollAreaWidgetContents)

        currentDir = self.currentFiles[0][1]
        self.ui.cueent_diretory_label.setText(currentDir)
        elementsOnLine = 3

        auxLayout = QtWidgets.QHBoxLayout()
        for i, elem in enumerate(self.currentFiles[1:]):
            if elem[0] == "":
                continue

            isDir = elem[0] != "File"
            if isDir:
                auxLayout.addWidget(get_card(
                        self.mainWindow,
                        isDir,
                        elem[1],
                        lambda checked=True, id=elem[1]: self.threadPool.submit(self.downloadFile, (id)),
                        lambda checked=True, id=elem[1]: self.deleteFileOrDirectory(id),
                        lambda checked=True, event=None, id=elem[1]: self.goInDirectory(id)))
            else:
                auxLayout.addWidget(get_card(
                        self.mainWindow,
                        isDir,
                        elem[1],
                        lambda checked=True, id=elem[1]: self.threadPool.submit(self.downloadFile, (id)),
                        lambda checked=True, id=elem[1]: self.deleteFileOrDirectory(id)))

            if (i+1) % elementsOnLine == 0 or i == (len(self.currentFiles[1:]) - 1):
                verticalLayout.addLayout(auxLayout)
                auxLayout = QtWidgets.QHBoxLayout()

        self.ui.scrollArea.setWidget(scrollAreaWidgetContents)

    def uploadFileOrDirectory(self, isDir: bool):
        self.mainWindow.getPathSignal.emit(isDir)
        path = self.uiQueue.get()
        if isDir:
            self.uploadDirectory(path)
        else:
            self.uploadFile(path)

    def getPathCallback(self, isDir: bool):
        dialog = QFileDialog()
        path = None
        if isDir:
            dialog.setFileMode(QFileDialog.Directory)
            path = dialog.getExistingDirectory(None, "Select Directory")
            path = None if path == '' else path
        else:
            dialog.setFileMode(QFileDialog.AnyFile)
            path = None if not dialog.exec() else dialog.selectedFiles()[0]
        self.uiQueue.put(path)



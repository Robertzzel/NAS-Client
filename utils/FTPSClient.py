import json
import os
import socket
import ssl

from utils.Codes import StatusCodes
from utils.Commands import Commands
from utils.FileDetails import FileDetails


def receiveMessage(s):
    message = bytearray()
    messageLengthSize = s.recv(10)
    messageSize = int(messageLengthSize.decode())

    while len(message) < messageSize:
        message.extend(s.recv(2048))

    return message


def receiveFile(s, fileName: str):
    messageLengthSize = s.recv(10)
    messageSize = int(messageLengthSize.decode())
    receivedBytes = 0

    with open(fileName, "wb") as f:
        while receivedBytes < messageSize:
            message = s.recv(2048)
            f.write(message)
            receivedBytes += len(message)


def sendMessage(s, message: bytes):
    msgSize = str(len(message)).rjust(10, '0').encode()
    s.send(msgSize + message)


def sendFile(s, fileName: str):
    stats = os.stat(fileName)
    msgSize = str(stats.st_size).rjust(10, '0').encode()
    s.send(msgSize)

    with open(fileName, "rb") as f:
        while True:
            chunk = f.read(2048)
            if not chunk:
                break
            s.send(chunk)


class FTPSClient:
    def __init__(self):
        self.__controlConnectionSocket = None
        self.controlConnection = None

    def initControlConnection(self, serverHost: str, serverPort: int):
        self.__controlConnectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.controlConnection = ssl.wrap_socket(self.__controlConnectionSocket, ssl_version=ssl.PROTOCOL_TLSv1_2)
        self.controlConnection.connect((serverHost, serverPort))
        response = receiveMessage(self.controlConnection)
        status = int(response.decode())
        self.raiseExceptionIfNotSuccessful(status, StatusCodes.ServiceReadyForNewUser)

    def newDataTransferConnection(self, serverHost: str, port: int):
        dataTransferConnectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataTransferConnection = ssl.wrap_socket(dataTransferConnectionSocket, ssl_version=ssl.PROTOCOL_TLSv1_2)
        dataTransferConnection.connect((serverHost, port))
        return dataTransferConnection

    def login(self, username: str, password: str):
        sendMessage(self.controlConnection, f"{Commands.USER.value} {username}".encode())
        response = receiveMessage(self.controlConnection)
        status = int(response.decode())
        self.raiseExceptionIfNotSuccessful(status, StatusCodes.UserNameOkayNeedPassword)

        sendMessage(self.controlConnection, f"{Commands.PASS.value} {password}".encode())
        response = receiveMessage(self.controlConnection)
        status = int(response.decode())
        self.raiseExceptionIfNotSuccessful(status, StatusCodes.UserLoggedInProceed)

    def printWorkingDirectory(self):
        sendMessage(self.controlConnection, f"{Commands.PWD.value}".encode())
        response = receiveMessage(self.controlConnection)
        status, path = response.decode().split("\n")
        status = int(status)
        self.raiseExceptionIfNotSuccessful(status, StatusCodes.PathnameCreated)
        return path

    def changeWorkingDirectory(self, path: str):
        sendMessage(self.controlConnection, f"{Commands.CWD.value} {path}".encode())
        response = receiveMessage(self.controlConnection)
        status = response.decode()
        status = int(status)
        self.raiseExceptionIfNotSuccessful(status, StatusCodes.RequestedFileActionOkayCompleted)

    def changeWorkingDirectoryUp(self):
        sendMessage(self.controlConnection, f"{Commands.CDUP.value}".encode())
        response = receiveMessage(self.controlConnection)
        status = response.decode()
        status = int(status)
        self.raiseExceptionIfNotSuccessful(status, StatusCodes.RequestedFileActionOkayCompleted)

    def removeDirectory(self, path: str):
        sendMessage(self.controlConnection, f"{Commands.RMD.value} {path}".encode())
        response = receiveMessage(self.controlConnection)
        status = int(response.decode())
        self.raiseExceptionIfNotSuccessful(status, StatusCodes.PathnameCreated)

    def makeDirectory(self, path: str):
        sendMessage(self.controlConnection, f"{Commands.MKD.value} {path}".encode())
        response = receiveMessage(self.controlConnection)
        status = int(response.decode())
        self.raiseExceptionIfNotSuccessful(status, StatusCodes.PathnameCreated)

    def list(self, path: str = None):
        dataTransferConnection = self.__pasv()
        command = f"{Commands.LIST.value}{'' if path is None else f' {path}'}".encode()
        sendMessage(self.controlConnection, command)
        response = receiveMessage(self.controlConnection)
        status = int(response.decode())
        self.raiseExceptionIfNotSuccessful(status, StatusCodes.DataConnectionAlreadyOpen)
        response = receiveMessage(self.controlConnection)
        status = int(response.decode())
        self.raiseExceptionIfNotSuccessful(status, StatusCodes.ClosingDataConnection)
        files = receiveMessage(dataTransferConnection)

        filesDetails = []
        for entry in json.loads(files.decode()):
            filesDetails.append(FileDetails(entry['Name'], entry['Size'], entry['IsDir']))

        return filesDetails

    def __pasv(self):
        sendMessage(self.controlConnection, f"{Commands.PASV.value}".encode())
        response = receiveMessage(self.controlConnection)
        status, _, _, _, ip = response.decode().split(" ")
        self.raiseExceptionIfNotSuccessful(int(status), StatusCodes.EnteringPassiveMode)
        host0, host1, host2, host3, port0, port1 = ip.split(",")
        host = "localhost"#f"{host0}.{host1}.{host2}.{host3}"
        port = int(port0) * 256 + int(port1)
        return self.newDataTransferConnection(host, port)

    def raiseExceptionIfNotSuccessful(self, statusCode: int, successfulStatus: StatusCodes):
        statusCode = StatusCodes(statusCode)
        if statusCode == successfulStatus:
            return None
        if statusCode == StatusCodes.NeedAccountForLogin:
            raise Exception("Not logged in, " + statusCode.name)
        if statusCode == StatusCodes.ServiceNotAvailable:
            raise Exception("FTP server not avalabile, " + statusCode.name)
        if statusCode == StatusCodes.RequestedFileActionNotTaken:
            raise Exception("File action not taken, " + statusCode.name)
        if statusCode == StatusCodes.RequestedActionNotTaken:
            raise Exception("Action not taken, " + statusCode.name)
        if statusCode == StatusCodes.CantOpenDataConnection:
            raise Exception("Cannot open data connection, " + statusCode.name)

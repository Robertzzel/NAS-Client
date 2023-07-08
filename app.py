# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'first.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PySide6 import QtCore, QtGui, QtWidgets


class MainUI(QtWidgets.QWidget):
    def __init__(self, MainWindow):
        super().__init__()
        MainWindow.setMinimumSize(QtCore.QSize(1000, 600))
        MainWindow.setMaximumSize(QtCore.QSize(1000, 600))
        MainWindow.setStyleSheet("background-color: rgb(17, 17, 17);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.top_bar_frame = QtWidgets.QFrame(self.centralwidget)
        self.top_bar_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.top_bar_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.top_bar_frame.setObjectName("top_bar_frame")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.top_bar_frame)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.top_bar_layout = QtWidgets.QHBoxLayout()
        self.top_bar_layout.setSpacing(0)
        self.top_bar_layout.setObjectName("top_bar_layout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.top_bar_layout.addItem(spacerItem)
        self.minimze_button = QtWidgets.QPushButton(self.top_bar_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.minimze_button.sizePolicy().hasHeightForWidth())
        self.minimze_button.setSizePolicy(sizePolicy)
        self.minimze_button.setStyleSheet("color: rgb(161, 168, 166);")
        self.minimze_button.setObjectName("minimze_button")
        self.top_bar_layout.addWidget(self.minimze_button)
        self.toggle_size_button = QtWidgets.QPushButton(self.top_bar_frame)
        self.toggle_size_button.setStyleSheet("color: rgb(161, 168, 166);")
        self.toggle_size_button.setObjectName("toggle_size_button")
        self.top_bar_layout.addWidget(self.toggle_size_button)
        self.exit_button = QtWidgets.QPushButton(self.top_bar_frame)
        self.exit_button.setStyleSheet("color: rgb(161, 168, 166);")
        self.exit_button.setObjectName("exit_button")
        self.top_bar_layout.addWidget(self.exit_button)
        self.top_bar_layout.setStretch(0, 100)
        self.top_bar_layout.setStretch(1, 1)
        self.top_bar_layout.setStretch(2, 1)
        self.top_bar_layout.setStretch(3, 1)
        self.horizontalLayout_6.addLayout(self.top_bar_layout)
        self.verticalLayout.addWidget(self.top_bar_frame)
        self.bar_and_contents_frame = QtWidgets.QFrame(self.centralwidget)
        self.bar_and_contents_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bar_and_contents_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bar_and_contents_frame.setObjectName("bar_and_contents_frame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.bar_and_contents_frame)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.bar_and_contents_layout = QtWidgets.QHBoxLayout()
        self.bar_and_contents_layout.setSpacing(0)
        self.bar_and_contents_layout.setObjectName("bar_and_contents_layout")
        self.side_bar_frame = QtWidgets.QFrame(self.bar_and_contents_frame)
        self.side_bar_frame.setStyleSheet("background-color: rgb(24, 24, 24);")
        self.side_bar_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.side_bar_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.side_bar_frame.setObjectName("side_bar_frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.side_bar_frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.side_bar_layout = QtWidgets.QVBoxLayout()
        self.side_bar_layout.setObjectName("side_bar_layout")
        self.landing_page_button = QtWidgets.QPushButton(self.side_bar_frame)
        self.landing_page_button.setStyleSheet("color: rgb(161, 168, 166);")
        self.landing_page_button.setObjectName("landing_page_button")
        self.side_bar_layout.addWidget(self.landing_page_button)
        self.login_page_button = QtWidgets.QPushButton(self.side_bar_frame)
        self.login_page_button.setStyleSheet("color: rgb(161, 168, 166);")
        self.login_page_button.setObjectName("login_page_button")
        self.side_bar_layout.addWidget(self.login_page_button)
        self.browse_page_button = QtWidgets.QPushButton(self.side_bar_frame)
        self.browse_page_button.setStyleSheet("color: rgb(161, 168, 166);")
        self.browse_page_button.setObjectName("browse_page_button")
        self.side_bar_layout.addWidget(self.browse_page_button)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.side_bar_layout.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.side_bar_layout)
        self.bar_and_contents_layout.addWidget(self.side_bar_frame)
        self.contents_frame = QtWidgets.QFrame(self.bar_and_contents_frame)
        self.contents_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.contents_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.contents_frame.setObjectName("contents_frame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.contents_frame)
        self.verticalLayout_5.setContentsMargins(-1, -1, 9, -1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.contents_layout = QtWidgets.QVBoxLayout()
        self.contents_layout.setObjectName("contents_layout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.contents_frame)
        self.stackedWidget.setStyleSheet("background-color: rgb(24, 24, 24);")
        self.stackedWidget.setObjectName("stackedWidget")
        self.landing_page = QtWidgets.QWidget()
        self.landing_page.setStyleSheet("background-color: rgb(24, 24, 24);")
        self.landing_page.setObjectName("landing_page")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.landing_page)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.landing_page_layout = QtWidgets.QVBoxLayout()
        self.landing_page_layout.setObjectName("landing_page_layout")
        self.verticalLayout_8.addLayout(self.landing_page_layout)
        self.stackedWidget.addWidget(self.landing_page)
        self.login_page = QtWidgets.QWidget()
        self.login_page.setStyleSheet("background-color: rgb(24, 24, 24);")
        self.login_page.setObjectName("login_page")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.login_page)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.login_page_layout = QtWidgets.QVBoxLayout()
        self.login_page_layout.setObjectName("login_page_layout")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.login_page_layout.addItem(spacerItem2)
        self.login_page_email_layout = QtWidgets.QHBoxLayout()
        self.login_page_email_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.login_page_email_layout.setObjectName("login_page_email_layout")
        self.email_label = QtWidgets.QLabel(self.login_page)
        self.email_label.setStyleSheet("color: rgb(161, 168, 166);")
        self.email_label.setAlignment(QtCore.Qt.AlignCenter)
        self.email_label.setObjectName("email_label")
        self.login_page_email_layout.addWidget(self.email_label)
        self.lineEdit = QtWidgets.QLineEdit(self.login_page)
        self.lineEdit.setStyleSheet("color: rgb(161, 168, 166);")
        self.lineEdit.setObjectName("lineEdit")
        self.login_page_email_layout.addWidget(self.lineEdit)
        self.login_page_email_layout.setStretch(0, 3)
        self.login_page_email_layout.setStretch(1, 10)
        self.login_page_layout.addLayout(self.login_page_email_layout)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.login_page_layout.addItem(spacerItem3)
        self.login_page_password_layout = QtWidgets.QHBoxLayout()
        self.login_page_password_layout.setObjectName("login_page_password_layout")
        self.password_label = QtWidgets.QLabel(self.login_page)
        self.password_label.setStyleSheet("color: rgb(161, 168, 166);")
        self.password_label.setAlignment(QtCore.Qt.AlignCenter)
        self.password_label.setObjectName("password_label")
        self.login_page_password_layout.addWidget(self.password_label)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.login_page)
        self.lineEdit_2.setStyleSheet("color: rgb(161, 168, 166);")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.login_page_password_layout.addWidget(self.lineEdit_2)
        self.login_page_password_layout.setStretch(0, 3)
        self.login_page_password_layout.setStretch(1, 10)
        self.login_page_layout.addLayout(self.login_page_password_layout)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.login_page_layout.addItem(spacerItem4)
        self.login_page_button_layout = QtWidgets.QHBoxLayout()
        self.login_page_button_layout.setObjectName("login_page_button_layout")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.login_page_button_layout.addItem(spacerItem5)
        self.login_button = QtWidgets.QPushButton(self.login_page)
        self.login_button.setStyleSheet("color: rgb(161, 168, 166);")
        self.login_button.setObjectName("login_button")
        self.login_page_button_layout.addWidget(self.login_button)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.login_page_button_layout.addItem(spacerItem6)
        self.login_page_button_layout.setStretch(0, 10)
        self.login_page_button_layout.setStretch(1, 4)
        self.login_page_button_layout.setStretch(2, 10)
        self.login_page_layout.addLayout(self.login_page_button_layout)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.login_page_layout.addItem(spacerItem7)
        self.login_page_layout.setStretch(0, 10)
        self.login_page_layout.setStretch(1, 3)
        self.login_page_layout.setStretch(2, 2)
        self.login_page_layout.setStretch(3, 3)
        self.login_page_layout.setStretch(4, 4)
        self.login_page_layout.setStretch(5, 2)
        self.login_page_layout.setStretch(6, 10)
        self.verticalLayout_4.addLayout(self.login_page_layout)
        self.stackedWidget.addWidget(self.login_page)
        self.browse_page = QtWidgets.QWidget()
        self.browse_page.setStyleSheet("background-color: rgb(24, 24, 24);")
        self.browse_page.setObjectName("browse_page")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.browse_page)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.browse_page_layout = QtWidgets.QVBoxLayout()
        self.browse_page_layout.setObjectName("browse_page_layout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.exit_directory_button = QtWidgets.QPushButton(self.browse_page)
        self.exit_directory_button.setStyleSheet("color: rgb(161, 168, 166);")
        self.exit_directory_button.setObjectName("exit_directory_button")
        self.horizontalLayout_2.addWidget(self.exit_directory_button)
        self.add_file_button = QtWidgets.QPushButton(self.browse_page)
        self.add_file_button.setStyleSheet("color: rgb(161, 168, 166);")
        self.add_file_button.setObjectName("add_file_button")
        self.horizontalLayout_2.addWidget(self.add_file_button)
        self.add_directory_button = QtWidgets.QPushButton(self.browse_page)
        self.add_directory_button.setStyleSheet("color: rgb(161, 168, 166);")
        self.add_directory_button.setObjectName("add_directory_button")
        self.horizontalLayout_2.addWidget(self.add_directory_button)
        self.cueent_diretory_label = QtWidgets.QLabel(self.browse_page)
        self.cueent_diretory_label.setStyleSheet("color: rgb(161, 168, 166);")
        self.cueent_diretory_label.setObjectName("cueent_diretory_label")
        self.horizontalLayout_2.addWidget(self.cueent_diretory_label)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem8)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(3, 10)
        self.horizontalLayout_2.setStretch(4, 5)
        self.browse_page_layout.addLayout(self.horizontalLayout_2)
        self.scroll_view_layout = QtWidgets.QVBoxLayout()
        self.scroll_view_layout.setObjectName("scroll_view_layout")
        self.scrollArea = QtWidgets.QScrollArea(self.browse_page)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 717, 502))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.scroll_view_layout.addWidget(self.scrollArea)
        self.browse_page_layout.addLayout(self.scroll_view_layout)
        self.browse_page_layout.setStretch(0, 1)
        self.browse_page_layout.setStretch(1, 20)
        self.verticalLayout_6.addLayout(self.browse_page_layout)
        self.stackedWidget.addWidget(self.browse_page)
        self.contents_layout.addWidget(self.stackedWidget)
        self.verticalLayout_5.addLayout(self.contents_layout)
        self.bar_and_contents_layout.addWidget(self.contents_frame)
        self.bar_and_contents_layout.setStretch(0, 4)
        self.bar_and_contents_layout.setStretch(1, 12)
        self.horizontalLayout_4.addLayout(self.bar_and_contents_layout)
        self.verticalLayout.addWidget(self.bar_and_contents_frame)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 23)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.minimze_button.setText(_translate("MainWindow", "-"))
        self.toggle_size_button.setText(_translate("MainWindow", "O"))
        self.exit_button.setText(_translate("MainWindow", "X"))
        self.landing_page_button.setText(_translate("MainWindow", "LANDING"))
        self.login_page_button.setText(_translate("MainWindow", "LOGIN"))
        self.browse_page_button.setText(_translate("MainWindow", "BROWSE"))
        self.email_label.setText(_translate("MainWindow", "EMAIL"))
        self.password_label.setText(_translate("MainWindow", "PASSWORD"))
        self.login_button.setText(_translate("MainWindow", "LOGIN"))
        self.exit_directory_button.setText(_translate("MainWindow", "<- BACK"))
        self.add_file_button.setText(_translate("MainWindow", "ADD FILE"))
        self.add_directory_button.setText(_translate("MainWindow", "ADD DIR"))
        self.cueent_diretory_label.setText(_translate("MainWindow", "TextLabel"))
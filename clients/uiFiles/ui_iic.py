# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../qtCreatorFiles/ui_iic.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_IIC(object):
    def setupUi(self, IIC):
        IIC.setObjectName("IIC")
        IIC.resize(934, 652)
        self.gridLayout = QtWidgets.QGridLayout(IIC)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(IIC)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setObjectName("tabWidget")
        self.loginTab = QtWidgets.QWidget()
        self.loginTab.setObjectName("loginTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.loginTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.userGBox = QtWidgets.QGroupBox(self.loginTab)
        self.userGBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.userGBox.sizePolicy().hasHeightForWidth())
        self.userGBox.setSizePolicy(sizePolicy)
        self.userGBox.setObjectName("userGBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.userGBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.userGBox)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.userLE = QtWidgets.QLineEdit(self.userGBox)
        self.userLE.setObjectName("userLE")
        self.gridLayout_3.addWidget(self.userLE, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.userGBox)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.passwordLE = QtWidgets.QLineEdit(self.userGBox)
        self.passwordLE.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLE.setObjectName("passwordLE")
        self.gridLayout_3.addWidget(self.passwordLE, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.userGBox)
        self.serverGBox = QtWidgets.QGroupBox(self.loginTab)
        self.serverGBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.serverGBox.sizePolicy().hasHeightForWidth())
        self.serverGBox.setSizePolicy(sizePolicy)
        self.serverGBox.setObjectName("serverGBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.serverGBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.serverLabel = QtWidgets.QLabel(self.serverGBox)
        self.serverLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.serverLabel.setObjectName("serverLabel")
        self.gridLayout_2.addWidget(self.serverLabel, 0, 0, 1, 1)
        self.serverLE = QtWidgets.QLineEdit(self.serverGBox)
        self.serverLE.setObjectName("serverLE")
        self.gridLayout_2.addWidget(self.serverLE, 0, 1, 1, 2)
        self.mportSB = QtWidgets.QSpinBox(self.serverGBox)
        self.mportSB.setMaximum(65535)
        self.mportSB.setProperty("value", 41984)
        self.mportSB.setObjectName("mportSB")
        self.gridLayout_2.addWidget(self.mportSB, 1, 1, 1, 1)
        self.mportLabel = QtWidgets.QLabel(self.serverGBox)
        self.mportLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.mportLabel.setObjectName("mportLabel")
        self.gridLayout_2.addWidget(self.mportLabel, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.serverGBox)
        self.fontBox = QtWidgets.QGroupBox(self.loginTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fontBox.sizePolicy().hasHeightForWidth())
        self.fontBox.setSizePolicy(sizePolicy)
        self.fontBox.setObjectName("fontBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.fontBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.fontSB = QtWidgets.QSpinBox(self.fontBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fontSB.sizePolicy().hasHeightForWidth())
        self.fontSB.setSizePolicy(sizePolicy)
        self.fontSB.setMinimum(2)
        self.fontSB.setMaximum(24)
        self.fontSB.setProperty("value", 10)
        self.fontSB.setObjectName("fontSB")
        self.gridLayout_4.addWidget(self.fontSB, 0, 1, 1, 1)
        self.fontLabel = QtWidgets.QLabel(self.fontBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fontLabel.sizePolicy().hasHeightForWidth())
        self.fontLabel.setSizePolicy(sizePolicy)
        self.fontLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fontLabel.setObjectName("fontLabel")
        self.gridLayout_4.addWidget(self.fontLabel, 0, 0, 1, 1)
        self.fontButton = QtWidgets.QPushButton(self.fontBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fontButton.sizePolicy().hasHeightForWidth())
        self.fontButton.setSizePolicy(sizePolicy)
        self.fontButton.setObjectName("fontButton")
        self.gridLayout_4.addWidget(self.fontButton, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.fontBox)
        self.frame = QtWidgets.QFrame(self.loginTab)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loginButton = QtWidgets.QPushButton(self.frame)
        self.loginButton.setObjectName("loginButton")
        self.horizontalLayout.addWidget(self.loginButton)
        spacerItem = QtWidgets.QSpacerItem(703, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.closeButton = QtWidgets.QPushButton(self.frame)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addWidget(self.frame)
        self.tabWidget.addTab(self.loginTab, "")
        self.scanTab = QtWidgets.QWidget()
        self.scanTab.setEnabled(False)
        self.scanTab.setObjectName("scanTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scanTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.scanTab)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scanTW = QtWidgets.QTreeWidget(self.groupBox)
        self.scanTW.setColumnCount(2)
        self.scanTW.setObjectName("scanTW")
        self.scanTW.headerItem().setText(0, "1")
        self.scanTW.headerItem().setText(1, "2")
        self.verticalLayout_3.addWidget(self.scanTW)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.refreshSButton = QtWidgets.QPushButton(self.groupBox)
        self.refreshSButton.setObjectName("refreshSButton")
        self.horizontalLayout_2.addWidget(self.refreshSButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.removePageB = QtWidgets.QPushButton(self.groupBox)
        self.removePageB.setObjectName("removePageB")
        self.horizontalLayout_2.addWidget(self.removePageB)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.scanTab)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.incompTW = QtWidgets.QTreeWidget(self.groupBox_3)
        self.incompTW.setColumnCount(2)
        self.incompTW.setObjectName("incompTW")
        self.incompTW.headerItem().setText(0, "1")
        self.incompTW.headerItem().setText(1, "2")
        self.verticalLayout_4.addWidget(self.incompTW)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.refreshIButton = QtWidgets.QPushButton(self.groupBox_3)
        self.refreshIButton.setObjectName("refreshIButton")
        self.horizontalLayout_3.addWidget(self.refreshIButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.subsPageB = QtWidgets.QPushButton(self.groupBox_3)
        self.subsPageB.setObjectName("subsPageB")
        self.horizontalLayout_3.addWidget(self.subsPageB)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.tabWidget.addTab(self.scanTab, "")
        self.progressTab = QtWidgets.QWidget()
        self.progressTab.setEnabled(False)
        self.progressTab.setObjectName("progressTab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.progressTab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox_2 = QtWidgets.QGroupBox(self.progressTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox_2)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.markBucket = QtWidgets.QWidget()
        self.markBucket.setGeometry(QtCore.QRect(0, 0, 48, 16))
        self.markBucket.setObjectName("markBucket")
        self.scrollArea.setWidget(self.markBucket)
        self.verticalLayout_6.addWidget(self.scrollArea)
        self.verticalLayout_5.addWidget(self.groupBox_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.refreshPButton = QtWidgets.QPushButton(self.progressTab)
        self.refreshPButton.setObjectName("refreshPButton")
        self.horizontalLayout_4.addWidget(self.refreshPButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.tabWidget.addTab(self.progressTab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(IIC)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(IIC)

    def retranslateUi(self, IIC):
        _translate = QtCore.QCoreApplication.translate
        IIC.setWindowTitle(_translate("IIC", "Overview and Management"))
        self.userGBox.setTitle(_translate("IIC", "User Information"))
        self.label.setText(_translate("IIC", "Username"))
        self.label_2.setText(_translate("IIC", "Password"))
        self.serverGBox.setTitle(_translate("IIC", "Server Information"))
        self.serverLabel.setText(_translate("IIC", "Server name:"))
        self.serverLE.setText(_translate("IIC", "127.0.0.1"))
        self.mportLabel.setText(_translate("IIC", "Port:"))
        self.fontBox.setTitle(_translate("IIC", "Font size"))
        self.fontLabel.setText(_translate("IIC", "Font size"))
        self.fontButton.setText(_translate("IIC", "Set font"))
        self.loginButton.setText(_translate("IIC", "L&ogin"))
        self.closeButton.setText(_translate("IIC", "&Close"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.loginTab), _translate("IIC", "&Login"))
        self.groupBox.setTitle(_translate("IIC", "Scanned papers"))
        self.refreshSButton.setText(_translate("IIC", "Refresh"))
        self.removePageB.setText(_translate("IIC", "Remove page from server"))
        self.groupBox_3.setTitle(_translate("IIC", "Incomplete papers"))
        self.refreshIButton.setText(_translate("IIC", "Refresh"))
        self.subsPageB.setText(_translate("IIC", "Substitute missing page with blank"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.scanTab), _translate("IIC", "&Scans"))
        self.groupBox_2.setTitle(_translate("IIC", "Marking progress"))
        self.refreshPButton.setText(_translate("IIC", "Refresh"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.progressTab), _translate("IIC", "&Marking"))

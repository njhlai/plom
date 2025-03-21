# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './qtCreatorFiles/ui_chooser.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Chooser(object):
    def setupUi(self, Chooser):
        Chooser.setObjectName("Chooser")
        Chooser.resize(540, 572)
        self.verticalLayout = QtWidgets.QVBoxLayout(Chooser)
        self.verticalLayout.setObjectName("verticalLayout")
        self.serverGBox = QtWidgets.QGroupBox(Chooser)
        self.serverGBox.setEnabled(True)
        self.serverGBox.setObjectName("serverGBox")
        self.gridLayout = QtWidgets.QGridLayout(self.serverGBox)
        self.gridLayout.setObjectName("gridLayout")
        self.infoLabel = QtWidgets.QLabel(self.serverGBox)
        self.infoLabel.setText("")
        self.infoLabel.setObjectName("infoLabel")
        self.gridLayout.addWidget(self.infoLabel, 3, 1, 1, 3)
        self.infoLabelStatic = QtWidgets.QLabel(self.serverGBox)
        self.infoLabelStatic.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.infoLabelStatic.setObjectName("infoLabelStatic")
        self.gridLayout.addWidget(self.infoLabelStatic, 3, 0, 1, 1)
        self.serverLabel = QtWidgets.QLabel(self.serverGBox)
        self.serverLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.serverLabel.setObjectName("serverLabel")
        self.gridLayout.addWidget(self.serverLabel, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.getServerInfoButton = QtWidgets.QPushButton(self.serverGBox)
        self.getServerInfoButton.setObjectName("getServerInfoButton")
        self.horizontalLayout_5.addWidget(self.getServerInfoButton)
        self.gridLayout.addLayout(self.horizontalLayout_5, 2, 2, 1, 2)
        self.mportLabel = QtWidgets.QLabel(self.serverGBox)
        self.mportLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.mportLabel.setObjectName("mportLabel")
        self.gridLayout.addWidget(self.mportLabel, 2, 0, 1, 1)
        self.serverLE = QtWidgets.QLineEdit(self.serverGBox)
        self.serverLE.setObjectName("serverLE")
        self.gridLayout.addWidget(self.serverLE, 1, 1, 1, 3)
        self.mportSB = QtWidgets.QSpinBox(self.serverGBox)
        self.mportSB.setMaximum(65535)
        self.mportSB.setProperty("value", 41984)
        self.mportSB.setObjectName("mportSB")
        self.gridLayout.addWidget(self.mportSB, 2, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)
        self.verticalLayout.addWidget(self.serverGBox)
        self.markGBox = QtWidgets.QGroupBox(Chooser)
        self.markGBox.setEnabled(True)
        self.markGBox.setObjectName("markGBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.markGBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.vlabel = QtWidgets.QLabel(self.markGBox)
        self.vlabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.vlabel.setObjectName("vlabel")
        self.gridLayout_2.addWidget(self.vlabel, 0, 2, 1, 1)
        self.pgLayout = QtWidgets.QHBoxLayout()
        self.pgLayout.setObjectName("pgLayout")
        self.pgSB = QtWidgets.QSpinBox(self.markGBox)
        self.pgSB.setProperty("value", 1)
        self.pgSB.setObjectName("pgSB")
        self.pgLayout.addWidget(self.pgSB)
        self.pgDrop = QtWidgets.QComboBox(self.markGBox)
        self.pgDrop.setObjectName("pgDrop")
        self.pgLayout.addWidget(self.pgDrop)
        self.gridLayout_2.addLayout(self.pgLayout, 0, 1, 1, 1)
        self.pgLabel = QtWidgets.QLabel(self.markGBox)
        self.pgLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pgLabel.setObjectName("pgLabel")
        self.gridLayout_2.addWidget(self.pgLabel, 0, 0, 1, 1)
        self.vLayout = QtWidgets.QHBoxLayout()
        self.vLayout.setObjectName("vLayout")
        self.vSB = QtWidgets.QSpinBox(self.markGBox)
        self.vSB.setProperty("value", 1)
        self.vSB.setObjectName("vSB")
        self.vLayout.addWidget(self.vSB)
        self.vDrop = QtWidgets.QComboBox(self.markGBox)
        self.vDrop.setObjectName("vDrop")
        self.vLayout.addWidget(self.vDrop)
        self.gridLayout_2.addLayout(self.vLayout, 0, 3, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setColumnStretch(2, 1)
        self.gridLayout_2.setColumnStretch(3, 1)
        self.verticalLayout.addWidget(self.markGBox)
        self.userGBox = QtWidgets.QGroupBox(Chooser)
        self.userGBox.setEnabled(True)
        self.userGBox.setObjectName("userGBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.userGBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.userGBox)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.userLE = QtWidgets.QLineEdit(self.userGBox)
        self.userLE.setObjectName("userLE")
        self.gridLayout_3.addWidget(self.userLE, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.userGBox)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.passwordLE = QtWidgets.QLineEdit(self.userGBox)
        self.passwordLE.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLE.setObjectName("passwordLE")
        self.gridLayout_3.addWidget(self.passwordLE, 1, 1, 1, 1)
        self.gridLayout_3.setColumnStretch(0, 1)
        self.gridLayout_3.setColumnStretch(1, 3)
        self.verticalLayout.addWidget(self.userGBox)
        self.settingsBox = QtWidgets.QGroupBox(Chooser)
        self.settingsBox.setObjectName("settingsBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.settingsBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.fontLabel = QtWidgets.QLabel(self.settingsBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fontLabel.sizePolicy().hasHeightForWidth())
        self.fontLabel.setSizePolicy(sizePolicy)
        self.fontLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fontLabel.setObjectName("fontLabel")
        self.horizontalLayout_2.addWidget(self.fontLabel)
        self.fontSB = QtWidgets.QSpinBox(self.settingsBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fontSB.sizePolicy().hasHeightForWidth())
        self.fontSB.setSizePolicy(sizePolicy)
        self.fontSB.setMinimum(4)
        self.fontSB.setMaximum(24)
        self.fontSB.setProperty("value", 10)
        self.fontSB.setObjectName("fontSB")
        self.horizontalLayout_2.addWidget(self.fontSB)
        spacerItem1 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.optionsButton = QtWidgets.QPushButton(self.settingsBox)
        self.optionsButton.setObjectName("optionsButton")
        self.horizontalLayout_2.addWidget(self.optionsButton)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 1)
        self.verticalLayout.addWidget(self.settingsBox)
        self.taskGBox = QtWidgets.QGroupBox(Chooser)
        self.taskGBox.setObjectName("taskGBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.taskGBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.markButton = QtWidgets.QPushButton(self.taskGBox)
        self.markButton.setObjectName("markButton")
        self.horizontalLayout.addWidget(self.markButton)
        self.identifyButton = QtWidgets.QPushButton(self.taskGBox)
        self.identifyButton.setObjectName("identifyButton")
        self.horizontalLayout.addWidget(self.identifyButton)
        self.manageButton = QtWidgets.QPushButton(self.taskGBox)
        self.manageButton.setObjectName("manageButton")
        self.horizontalLayout.addWidget(self.manageButton)
        spacerItem2 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.closeButton = QtWidgets.QPushButton(self.taskGBox)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 3)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 2)
        self.verticalLayout.addWidget(self.taskGBox)

        self.retranslateUi(Chooser)
        QtCore.QMetaObject.connectSlotsByName(Chooser)
        Chooser.setTabOrder(self.serverLE, self.mportSB)
        Chooser.setTabOrder(self.mportSB, self.getServerInfoButton)
        Chooser.setTabOrder(self.getServerInfoButton, self.pgSB)
        Chooser.setTabOrder(self.pgSB, self.pgDrop)
        Chooser.setTabOrder(self.pgDrop, self.vSB)
        Chooser.setTabOrder(self.vSB, self.vDrop)
        Chooser.setTabOrder(self.vDrop, self.userLE)
        Chooser.setTabOrder(self.userLE, self.passwordLE)
        Chooser.setTabOrder(self.passwordLE, self.fontSB)
        Chooser.setTabOrder(self.fontSB, self.markButton)
        Chooser.setTabOrder(self.markButton, self.identifyButton)
        Chooser.setTabOrder(self.identifyButton, self.closeButton)

    def retranslateUi(self, Chooser):
        _translate = QtCore.QCoreApplication.translate
        Chooser.setWindowTitle(_translate("Chooser", "Plom Client"))
        self.serverGBox.setTitle(_translate("Chooser", "Server Information"))
        self.infoLabelStatic.setText(_translate("Chooser", "Info:"))
        self.serverLabel.setText(_translate("Chooser", "Server name:"))
        self.getServerInfoButton.setText(_translate("Chooser", "&Validate server"))
        self.mportLabel.setText(_translate("Chooser", "Port:"))
        self.serverLE.setText(_translate("Chooser", "127.0.0.1"))
        self.markGBox.setTitle(_translate("Chooser", "Marking information"))
        self.vlabel.setText(_translate("Chooser", "Version:"))
        self.pgLabel.setText(_translate("Chooser", "Question:"))
        self.userGBox.setTitle(_translate("Chooser", "User Information"))
        self.label.setText(_translate("Chooser", "Username:"))
        self.label_2.setText(_translate("Chooser", "Password:"))
        self.settingsBox.setTitle(_translate("Chooser", "Settings"))
        self.fontLabel.setText(_translate("Chooser", "Font size:"))
        self.optionsButton.setText(_translate("Chooser", "&Options..."))
        self.taskGBox.setTitle(_translate("Chooser", "Choose task"))
        self.markButton.setText(_translate("Chooser", "&Mark"))
        self.identifyButton.setText(_translate("Chooser", "&Identify"))
        self.manageButton.setText(_translate("Chooser", "Manage &server"))
        self.closeButton.setText(_translate("Chooser", "&Close"))

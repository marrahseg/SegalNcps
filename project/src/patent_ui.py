# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'patent.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(355, 541)
        Dialog.setMinimumSize(QtCore.QSize(0, 0))
        Dialog.setMaximumSize(QtCore.QSize(355, 543))
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.PatienttabWidget = QtWidgets.QTabWidget(Dialog)
        self.PatienttabWidget.setObjectName("PatienttabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.tab)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.RightLeftHand = QtWidgets.QLineEdit(self.frame)
        self.RightLeftHand.setObjectName("RightLeftHand")
        self.gridLayout_4.addWidget(self.RightLeftHand, 3, 2, 1, 1)
        self.label_46 = QtWidgets.QLabel(self.frame)
        self.label_46.setObjectName("label_46")
        self.gridLayout_4.addWidget(self.label_46, 3, 0, 1, 1)
        self.label_52 = QtWidgets.QLabel(self.frame)
        self.label_52.setObjectName("label_52")
        self.gridLayout_4.addWidget(self.label_52, 0, 0, 1, 1)
        self.Fullname = QtWidgets.QLineEdit(self.frame)
        self.Fullname.setObjectName("Fullname")
        self.gridLayout_4.addWidget(self.Fullname, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 4, 0, 1, 1)
        self.DateOfBrith = QtWidgets.QLineEdit(self.frame)
        self.DateOfBrith.setObjectName("DateOfBrith")
        self.gridLayout_4.addWidget(self.DateOfBrith, 4, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 2, 0, 1, 1)
        self.SubjectID = QtWidgets.QLineEdit(self.frame)
        self.SubjectID.setObjectName("SubjectID")
        self.gridLayout_4.addWidget(self.SubjectID, 2, 2, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        self.frame_3 = QtWidgets.QFrame(self.tab)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(self.frame_3)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.BTPatientSpin = QtWidgets.QSpinBox(self.frame_3)
        self.BTPatientSpin.setMaximum(999)
        self.BTPatientSpin.setObjectName("BTPatientSpin")
        self.horizontalLayout.addWidget(self.BTPatientSpin)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_7 = QtWidgets.QLabel(self.frame_3)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout.addWidget(self.label_7)
        self.EvPatientSpin = QtWidgets.QSpinBox(self.frame_3)
        self.EvPatientSpin.setMaximum(999)
        self.EvPatientSpin.setObjectName("EvPatientSpin")
        self.horizontalLayout.addWidget(self.EvPatientSpin)
        self.label_8 = QtWidgets.QLabel(self.frame_3)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout.addWidget(self.label_8)
        self.ApPatientSpin = QtWidgets.QSpinBox(self.frame_3)
        self.ApPatientSpin.setMaximum(999)
        self.ApPatientSpin.setObjectName("ApPatientSpin")
        self.horizontalLayout.addWidget(self.ApPatientSpin)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.frame_3)
        self.frame_2 = QtWidgets.QFrame(self.tab)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")
        self.Power_label = QtWidgets.QLabel(self.frame_2)
        self.Power_label.setObjectName("Power_label")
        self.gridLayout.addWidget(self.Power_label, 0, 0, 1, 1)
        self.Freq_spin = QtWidgets.QSpinBox(self.frame_2)
        self.Freq_spin.setObjectName("Freq_spin")
        self.gridLayout.addWidget(self.Freq_spin, 5, 1, 1, 1)
        self.Connect_Button = QtWidgets.QPushButton(self.frame_2)
        self.Connect_Button.setObjectName("Connect_Button")
        self.gridLayout.addWidget(self.Connect_Button, 9, 1, 1, 1)
        self.Freq_label = QtWidgets.QLabel(self.frame_2)
        self.Freq_label.setObjectName("Freq_label")
        self.gridLayout.addWidget(self.Freq_label, 5, 0, 1, 1)
        self.Power_spin = QtWidgets.QSpinBox(self.frame_2)
        self.Power_spin.setObjectName("Power_spin")
        self.gridLayout.addWidget(self.Power_spin, 0, 1, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.frame_2)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 6, 1, 1, 1)
        self.Protlabel = QtWidgets.QLabel(self.frame_2)
        self.Protlabel.setObjectName("Protlabel")
        self.gridLayout.addWidget(self.Protlabel, 6, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_4 = QtWidgets.QFrame(self.tab)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.textEditPatient = QtWidgets.QTextEdit(self.frame_4)
        self.textEditPatient.setMinimumSize(QtCore.QSize(0, 0))
        self.textEditPatient.setObjectName("textEditPatient")
        self.gridLayout_3.addWidget(self.textEditPatient, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.frame_4)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame_4, 0, QtCore.Qt.AlignBottom)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.SearchButton = QtWidgets.QPushButton(self.tab)
        self.SearchButton.setObjectName("SearchButton")
        self.horizontalLayout_2.addWidget(self.SearchButton)
        self.ExcuteButton = QtWidgets.QPushButton(self.tab)
        self.ExcuteButton.setObjectName("ExcuteButton")
        self.horizontalLayout_2.addWidget(self.ExcuteButton)
        self.SaveButton = QtWidgets.QPushButton(self.tab)
        self.SaveButton.setMinimumSize(QtCore.QSize(29, 0))
        self.SaveButton.setObjectName("SaveButton")
        self.horizontalLayout_2.addWidget(self.SaveButton)
        self.CancelButton = QtWidgets.QPushButton(self.tab)
        self.CancelButton.setMinimumSize(QtCore.QSize(29, 0))
        self.CancelButton.setObjectName("CancelButton")
        self.horizontalLayout_2.addWidget(self.CancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.PatienttabWidget.addTab(self.tab, "")
        self.horizontalLayout_3.addWidget(self.PatienttabWidget)

        self.retranslateUi(Dialog)
        self.PatienttabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.RightLeftHand.setPlaceholderText(_translate("Dialog", "example:left"))
        self.label_46.setText(_translate("Dialog", "R/L-handed:"))
        self.label_52.setText(_translate("Dialog", "Fullname:"))
        self.Fullname.setPlaceholderText(_translate("Dialog", "example:ahmad karami"))
        self.label_2.setText(_translate("Dialog", "Date of Brith"))
        self.DateOfBrith.setPlaceholderText(_translate("Dialog", "example:25"))
        self.label_5.setText(_translate("Dialog", "Subject ID"))
        self.SubjectID.setPlaceholderText(_translate("Dialog", "example:13"))
        self.label_6.setText(_translate("Dialog", "BT:"))
        self.label_7.setText(_translate("Dialog", "EV:"))
        self.label_8.setText(_translate("Dialog", "AP:"))
        self.Power_label.setText(_translate("Dialog", "power:"))
        self.Connect_Button.setText(_translate("Dialog", "Connect to magestim"))
        self.Freq_label.setText(_translate("Dialog", "frequency:"))
        self.comboBox.setItemText(0, _translate("Dialog", "lDLPFC"))
        self.comboBox.setItemText(1, _translate("Dialog", "RDLPFC"))
        self.comboBox.setItemText(2, _translate("Dialog", "lMlP"))
        self.comboBox.setItemText(3, _translate("Dialog", "RMlP"))
        self.Protlabel.setText(_translate("Dialog", "protocol:"))
        self.textEditPatient.setPlaceholderText(_translate("Dialog", "Please enter the patient\'s medical condition here "))
        self.label.setText(_translate("Dialog", "Comments:"))
        self.SearchButton.setText(_translate("Dialog", "Search"))
        self.ExcuteButton.setText(_translate("Dialog", "excute"))
        self.SaveButton.setText(_translate("Dialog", "Save"))
        self.CancelButton.setText(_translate("Dialog", "Cancel"))
        self.PatienttabWidget.setTabText(self.PatienttabWidget.indexOf(self.tab), _translate("Dialog", "Pation Information"))

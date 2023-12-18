from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from PyQt5.uic.properties import QtGui
from qt_material import apply_stylesheet

from src.RefHead_ui import Ui_Dialog


class MyDialogHead_Dialog(QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Refrence head indices ")
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap("../icons/logo/glog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.setWindowIcon(icon)
        self.setupUi(self)

        icon5 = QIcon("../UI/button/replay.svg")
        self.DefaultButton.setIcon(icon5)

        icon6 = QIcon("../UI/button/development.svg")
        self.SetButton.setIcon(icon6)


        self.SetButton.clicked.connect(self.onSet_button_clicked)
        self.DefaultButton.clicked.connect(self.onDefault_button_clicked)


    def show_dialog(self):
        # apply_stylesheet(self, theme='../UI/dark_purp_segal.xml')
        apply_stylesheet(self, theme='../UI/reza_color.xml')
        self.exec_()

    def onDefault_button_clicked(self):
        self.default_mode = True
        self.BTSpin.setValue(174)
        self.EVSpin.setValue(142)
        self.APSpin.setValue(212)
        self.close()


    def onSet_button_clicked(self):
        self.default_mode = False
        BTIndices = self.RBTspinBox.value()
        EVIndices = self.REVspinBox.value()
        APIndices = self.RAPspinBox.value()
        print("hsffjgsgfs", BTIndices, EVIndices, APIndices)

        self.BTSpin.setValue(BTIndices)
        self.EVSpin.setValue(EVIndices)
        self.APSpin.setValue(APIndices)
        self.close()
        return BTIndices, EVIndices, APIndices

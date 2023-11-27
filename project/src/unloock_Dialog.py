from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLineEdit
from PyQt5.uic.properties import QtGui
from qt_material import apply_stylesheet

from unlock_ui import Ui_Form


class MyUnlock_Dialog(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Segal Step")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icons/logo/glog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setupUi(self)


        self.UnLockButton.clicked.connect(self.onunlock_Successful)
        icon4 = QIcon("../UI/button/unlocked.svg")
        self.my_Unlock.UnLockButton.setIcon(icon4)
        self.UnLocklineEdit.setEchoMode(QLineEdit.Password)
        self.my_Unlock.setWindowTitle("Open Lock")

    def show_dialog(self):
        # apply_stylesheet(self, theme='../UI/dark_purp_segal.xml')
        apply_stylesheet(self, theme='../UI/reza_color.xml')
        self.exec_()

    ########################<<<<<<<<<<<<<<If the user clicks on the "Reference Head Indices",
    # this method displays the lock entry window.>>>>>########
    def onLock_Breaker(self):
        self.my_Unlock.show()

    ####################وقتی دکمه ی NLOCK را زد این متد فعال شده و دیالوگ جدیدی باز میشود
    def onunlock_Successful_Area(self):
        if self.UnLocklineEdit.text() == "s1996":
            self.UnLocklineEdit.setText("")
            self.my_StandardArea.close()
            self.show_dialog()

        else:
            self.my_UnlockArea.close()


            self.my_Unlock.close()

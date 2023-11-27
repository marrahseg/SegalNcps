from PyQt5.QtWidgets import QDialog, QLineEdit
from qt_material import apply_stylesheet

from src.unlockArea_ui import Ui_Form


class MyUnlockArea_Dialog(QDialog, Ui_Form):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Custom Title")
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap("../icons/logo/glog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.setWindowIcon(icon)
        self.setupUi(self)
        self.UnLocklineEdit.setEchoMode(QLineEdit.Password)
        self.UnLockButton.clicked.connect(self.onunlock_Successful_Area)
        self.UnLockButton.clicked.connect(self.onunlock_Successful_Area)

    def show_dialog(self):
        # apply_stylesheet(self, theme='../UI/dark_purp_segal.xml')
        apply_stylesheet(self, theme='../UI/reza_color.xml')
        self.exec_()



    #############################باز کردن قفل یرای standard area
    def onLock_Breaker_Area(self):
        self.show()

    ####################وقتی دکمه ی NLOCK را زد این متد فعال شده و دیالوگ جدیدی باز میشود
    def onunlock_Successful_Area(self):
        if self.UnLocklineEdit.text() == "s1996":
            self.UnLocklineEdit.setText("")
            # self.my_StandardArea.close()
            self.show_dialog()

        else:
            self.close()


            self.close()





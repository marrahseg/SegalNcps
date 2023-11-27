from PyQt5.QtWidgets import QDialog
from qt_material import apply_stylesheet

from src.standardarea_ui import Ui_Form


class MyStandardArea_Dialog(QDialog, Ui_Form):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("StandardArea")
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap("../icons/logo/glog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.setWindowIcon(icon)
        self.setupUi(self)

    def show_dialog(self):
        # apply_stylesheet(self, theme='../UI/dark_purp_segal.xml')
        apply_stylesheet(self, theme='../UI/reza_color.xml')
        self.exec_()
import sys
from PyQt5.QtWidgets import QApplication
from myDev import Window_withDev
from ui_loder import Window_ui
from qt_material import apply_stylesheet



if __name__ == "__main__":
     app = QApplication(sys.argv)
     win = Window_withDev()
     # win = Window_ui()

     # apply_stylesheet(app, theme='color.xml')
     apply_stylesheet(app, theme='dark_purp_segal.xml')

     win.show()
     # win.showFullScreen()

     # win.frame.hide()
     win.onResetBotton()
     app.exec()

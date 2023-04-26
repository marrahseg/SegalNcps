import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen
from myDev import Window_withDev
from qt_material import apply_stylesheet





if __name__ == "__main__":

     app = QApplication(sys.argv)
     win = Window_withDev()

     pixmap = QPixmap("bj - Copy.jpg")
     splash = QSplashScreen(pixmap)
     splash.show()
     app.processEvents()

     apply_stylesheet(app, theme='../UI/dark_purp_segal.xml')
     splash.finish(win)

     win.show()

     win.showFullScreen()

     app.exec()

import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen
from myANrobot import Window_withDevAN
from qt_material import apply_stylesheet






if __name__ == "__main__":

     app = QApplication(sys.argv)
     win = Window_withDevAN()


     pixmap = QPixmap("../UI/bj - Copy.jpg")
     splash = QSplashScreen(pixmap)
     splash.show()
     app.processEvents()
     splash.finish(win)

     win.frame_40.setStyleSheet("border-color:#7B1FA2")
     win.frame_20.setStyleSheet("border-color:#7B1FA2")
     win.groupBox_6.setStyleSheet("border-color:#FFFFFF")
     win.groupBox.setStyleSheet("border-color:#FFFFFF")

     win.frame_17.setStyleSheet("border-color:#FFFFFF")
     win.frame_18.setStyleSheet("border-color:#FFFFFF")
     win.frame_19.setStyleSheet("border-color:#FFFFFF")
     win.frame_23.setStyleSheet("border-color:#FFFFFF")
     win.frame_22.setStyleSheet("border-color:#FFFFFF")
     win.frame_21.setStyleSheet("border-color:#FFFFFF")
     # win.groupBox_6.setStyleSheet("border-color:#7B1FA2")


     # win.frame_26.setStyleSheet("border-color:#7B1FA2")
     win.line.setStyleSheet("background-color:#9E9E9E;")
     win.line_3.setStyleSheet("background-color:#9E9E9E;")
     win.line_2.setStyleSheet("background-color:#9E9E9E;")
     win.line_4.setStyleSheet("background-color:#9E9E9E;")
     win.line_5.setStyleSheet("background-color:#9E9E9E;")
     win.line_6.setStyleSheet("background-color:#9E9E9E;")
     win.line_7.setStyleSheet("background-color:#9E9E9E;")
     win.line_8.setStyleSheet("background-color:#9E9E9E;")
     win.line_9.setStyleSheet("background-color:#9E9E9E;")
     win.line_10.setStyleSheet("background-color:#9E9E9E;")
     win.line_11.setStyleSheet("background-color:#9E9E9E;")

     win.pushButton.setStyleSheet("border-radius: 20px")


     # win.frame_36.setStyleSheet("border-color:#7B1FA2")

     # win.frame_37.setStyleSheet("border-color:#7B1FA2")
     # win.frame_38.setStyleSheet("border-color:#7B1FA2")
     # win.frame_39.setStyleSheet("border-color:#7B1FA2")
     # win.frame_31.setStyleSheet("border-color:#7B1FA2")
     # win.frame_34.setStyleSheet("border-color:#7B1FA2")
     # win.frame_32.setStyleSheet("border-color:#7B1FA2")
     # win.frame_33.setStyleSheet("border-color:#7B1FA2")
     # win.frame_30.setStyleSheet("border-color:#7B1FA2")
     # win.frame_35.setStyleSheet("border-color:#7B1FA2")
     win.frame_27.setStyleSheet("border-color:#FFFFFF")
     win.frame_26.setStyleSheet("border-color:#FFFFFF")
     win.frame_47.setStyleSheet("border-color:#FFFFFF")


     win.ResetButton.setStyleSheet("background-color: #E0E0E0;color: #000000;border-radius: 20px")
     win.StartButton.setStyleSheet("background-color: #E0E0E0;color: #000000;border-radius: 20px")
     win.StartWoMovementButton.setStyleSheet("background-color: #E0E0E0;color: #000000;border-radius: 20px")
     # win.GoMotionButton.setStyleSheet("background-color: #FF0000;color: #FFFFFF;border-radius: 20px")




     # win.frame_10.setStyleSheet("border-color:#7B1FA2")
     # win.frame_11.setStyleSheet("border-color:#7B1FA2")
     # win.frame_12.setStyleSheet("border-color:#7B1FA2")
     # win.frame_13.setStyleSheet("border-color:#7B1FA2")
     # win.frame_14.setStyleSheet("border-color:#9E9E9E")
     # win.frame_9.setStyleSheet("border-color:#7B1FA2")
     # win.YSlider.setStyleSheet("QSlider::tick:vertical { background-color: blue; } QSlider::sub-page:vertical { background-color: yellow; }")
     # win.YSlider.setStyleSheet("QSlider::handle:vertical { background-color: blue; }")




     # apply_stylesheet(app, theme='../UI/dark_purp_segal.xml')
     apply_stylesheet(app, theme='../UI/reza_color.xml')





     win.show()

     # win.showFullScreen()

     app.exec()

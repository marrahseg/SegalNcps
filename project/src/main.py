import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen
from myANrobot import WindowWithDevAN
from qt_material import apply_stylesheet

if __name__ == "__main__":
    app = QApplication(sys.argv)

    pixmap = QPixmap("../UI/splash/bj - Copy.jpg")
    splash = QSplashScreen(pixmap)
    splash.show()

    win = WindowWithDevAN()
    app.processEvents()
    splash.finish(win)

    win.PNamelabel.setStyleSheet("font-weight: bold;font-size: 16px;")
    win.Bt_label.setStyleSheet("font-weight: bold;font-size: 16px;")
    win.label_62.setStyleSheet("font-weight: bold;font-size: 16px;")
    win.label_63.setStyleSheet("font-weight: bold;font-size: 16px;")
    win.label_64.setStyleSheet("font-weight: bold;font-size: 16px;")
    win.label_65.setStyleSheet("font-weight: bold;font-size: 16px;")
    win.Ev_label.setStyleSheet("font-weight: bold;font-size: 16px;")
    win.Ap_label.setStyleSheet("font-weight: bold;font-size: 16px;")

    win.frame_40.setStyleSheet("border-color:#FFFFFF")
    win.frame_41.setStyleSheet("border-color:#FFFFFF")
    win.frame_42.setStyleSheet("border-color:#FFFFFF")
    win.frame_43.setStyleSheet("border-color:#FFFFFF")
    win.frame_47.setStyleSheet("border-color:#FFFFFF")
    win.frame_38.setStyleSheet("border-color:#FFFFFF")
    win.frame_39.setStyleSheet("border-color:#FFFFFF")

    win.groupBox_HeadPosition.setStyleSheet("border-color:#FFFFFF")
    win.groupBox.setStyleSheet("border-color:#FFFFFF")
    win.frame_37.setStyleSheet("border-color:#CFD8DC")
    win.groupBox_3.setStyleSheet("color:#FFFFFF")

    win.line.setStyleSheet("background-color:#9E9E9E;")
    win.line_3.setStyleSheet("background-color:#9E9E9E;")
    win.line_2.setStyleSheet("background-color:#9E9E9E;")
    win.line_4.setStyleSheet("background-color:#9E9E9E;")

    win.frame_30.setStyleSheet("border-color:#CFD8DC")
    win.frame_31.setStyleSheet("border-color:#FFFFFF")
    win.frame_32.setStyleSheet("border-color:#FFFFFF")
    win.frame_33.setStyleSheet("border-color:#FFFFFF")
    win.frame_27.setStyleSheet("border-color:#FFFFFF")
    win.frame_26.setStyleSheet("border-color:#FFFFFF")
    win.frame_47.setStyleSheet("border-color:#FFFFFF")

    win.bt_setRotation.setStyleSheet("background-color: #E0E0E0;color: #000000;border-radius: 20px")
    win.StartButton.setStyleSheet("background-color: #E0E0E0;color: #000000;border-radius: 20px")
    win.bt_clac_spot.setStyleSheet("background-color: #E0E0E0;color: #000000;border-radius: 20px")
    win.Button_Motion.setStyleSheet("background-color: #E0E0E0;color: #000000;border-radius: 20px")
    win.bt_cp_poz.setStyleSheet("background-color: #E0E0E0;color: #000000;border-radius: 20px")
    win.bt_reset_pos.setStyleSheet("background-color: #E0E0E0;color: #000000;border-radius: 20px")
    win.pushButton_reset_robot_position.setStyleSheet(
        "background-color: #E0E0E0;color: #000000;border-radius: 20px;text-align: left;")
    win.pushButton_drag_robot.setStyleSheet(
        "background-color: #E0E0E0;color: #000000;border-radius: 20px;text-align: left;")
    win.pushButton_gather_headxy.setStyleSheet(
        "background-color: #E0E0E0;color: #000000;border-radius: 20px;text-align: left;")
    win.pushButton_gather_headz.setStyleSheet(
        "background-color: #E0E0E0;color: #000000;border-radius: 20px;text-align: left;")
    win.pushButton_live_robot_position.setStyleSheet(
        "background-color: #E0E0E0;color: #000000;border-radius: 20px;text-align: left;")
    win.pushButton_ready_robot_position.setStyleSheet(
        "background-color: #E0E0E0;color: #000000;border-radius: 20px;text-align: left;")
    win.pushButton_start_robot_movement.setStyleSheet(
        "background-color: #E0E0E0;color: #000000;border-radius: 20px;text-align: left;")
    win.bt_setCz.setStyleSheet("background-color: #E0E0E0;color: #000000;border-radius: 30px")
    win.bt_left.setStyleSheet("background-color: #E0E0E0;color: #000000;border-radius: 30px")
    win.bt_right.setStyleSheet("background-color: #E0E0E0;color: #000000;border-radius: 30px")

    apply_stylesheet(app, theme='../UI/theme/reza_color.xml')

    win.show()
    app.exec()

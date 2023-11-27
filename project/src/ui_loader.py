import configparser
import os
import pickle

import cv2
import np as np
import numpy as np
import pyvista as pv
from PIL import Image
from PyQt5.uic.properties import QtCore, QtWidgets, QtGui
from trimesh import transformations
import Constants
from pyvistaqt import QtInteractor
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage, QFont, QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QWidget, QDialog, QLabel, QLineEdit
from qt_material import apply_stylesheet
from src.NCPSUI_ui import Ui_MainWindow
from PyQt5 import QtGui

#######Dialogs
import Infopation_Dialog
import unloock_Dialog
import resizeHead_Dialog
import unlockArea_Dialog
import standardArea_Dialog
import defultvariable


motor_real = False

##############################read txt file
with open("../UI/defultvariable.txt", "r") as f:
    contents = f.read()
    # print(contents)
exec(contents)
# اصلی
# my_Xside_pics_add = '../UI/MRI_PROJECT/MRI_FINAL_reza2/X_174/'
# my_Yside_pics_add = '../UI/MRI_PROJECT/MRI_FINAL_reza2/Y_212/'
# my_Zside_pics_add = '../UI/MRI_PROJECT/MRI_FINAL_reza2/Z_142/'


my_Xside_pics_add = '../UI/MRI_PROJECT/MRI_CROPED_REZA/X_crop/'
my_Yside_pics_add = '../UI/MRI_PROJECT/MRI_CROPED_REZA/Y_crop/'
my_Zside_pics_add = '../UI/MRI_PROJECT/MRI_CROPED_REZA/Z_crop/'







############################################
class Window_ui(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        os.getcwd()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icons/logo/glog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setupUi(self)

        #######instance  Dialog #########
        self.my_Pation = Infopation_Dialog.PationInfo_Dialog()
        self.my_Unlock = unloock_Dialog.MyUnlock_Dialog
        self.my_dialog_head = resizeHead_Dialog.MyDialogHead_Dialog()
        self.my_UnlockArea = unlockArea_Dialog.MyUnlockArea_Dialog()
        self.my_StandardArea = standardArea_Dialog.MyStandardArea_Dialog()

        #######initial object  class Dialog #########

        self.timer = QTimer()
        self.initAllpicture()
        self.signalsSlat()
        self.show_3Brain()
        self.set_Icon()
        self.set_setting_ui()
        self.set_logo()

        self.centerBX = 0
        self.centerBY = 0
        self.centerBZ = 0

        self.x_now = 0
        self.y_now = 0
        self.z_now = 0
        self.oa_now = 0
        self.ca_now = 0

        self.x_go = 0
        self.y_go = 0
        self.z_go = 0
        self.oa_go = 0
        self.ca_go = 0

        self.counter = 0

        self.onResetBotton()
        self.update_pics_lines_and_now_position(self.x_go, self.y_go, self.z_go)
        self.change_slider_Pos(self.x_go, self.y_go, self.z_go)


    def signalsSlat(self):
        self.StartButton.clicked.connect(self.onStartBottonClicked)
        self.StartWoMovementButton.clicked.connect(self.onStartWoMovementButton)
        self.XSlider.valueChanged.connect(self.onSliderchangeClicked)
        self.YSlider.valueChanged.connect(self.onSliderchangeClicked)
        self.ZSlider.valueChanged.connect(self.onSliderchangeClicked)
        self.ResetButton.clicked.connect(self.onResetBotton)

        self.actionHide_Button.triggered.connect(self.onMyHideShow)
        self.timer.timeout.connect(self.onTimer_interrupt)

        # self.SetOffsetButton.clicked.connect(self.onChangeOffset)
        # self.ResetOffsetButton.clicked.connect(self.onResetOffset)
        # self.actionShow_Offseting.triggered.connect(self.onMyHideOffseting)
        # self.actionChange_Offset.triggered.connect(self.onMyHideOffseting)

        ###############################>>>>>>>>>>>>>>>>>>>MENU BAR>>>>>>>>>>>>>>>>>>>>>############################
        self.actionDark.triggered.connect(self.on_dark_theme)
        self.actionLight.triggered.connect(self.on_light_theme)
        self.actionSave_as.triggered.connect(self.onSaveFigData)
        self.actionShow.triggered.connect(self.onShow_slider_onBrain)
        self.actionHide_Button.triggered.connect(self.onHide_slider_onBrain)
        self.actionShow_Coil.triggered.connect(self.onShow_Coil)


        ###########################>>>>>>>RefHead>>>>>>>#######################
        self.CreateExamaction.triggered.connect(self.my_Pation.onCreate_dialog)
        self.OpenExamaction.triggered.connect(self.my_Pation.onLoad_Exam)
        self.Refrenceheadaction.triggered.connect(self.my_Unlock.onLock_Breaker)
        self.actionRegister_areas.triggered.connect(self.my_UnlockArea.onLock_Breaker_Area)
        self.actionStandard_area_2.triggered.connect(self.my_UnlockArea.onLock_Breaker_Area)
        ###########################>>>>>>>RefHead>>>>>>>#######################


        ####################show defult pic in x

        pixmap1 = QPixmap(my_Xside_pics_add + self.picListX[0])
        pixmap1 = pixmap1.scaled(self.Xpiclabel.size())
        self.Xpiclabel.setPixmap(pixmap1)

        ######################### show defult pic in y
        pixmap2 = QPixmap(my_Yside_pics_add + self.picListY[0])
        pixmap2 = pixmap2.scaled(self.Ypiclabel.size())
        self.Ypiclabel.setPixmap(pixmap2)

        ######################## show defult pic in z

        pixmap3 = QPixmap(my_Zside_pics_add + self.picListZ[0])
        pixmap3 = pixmap3.scaled(self.Zpiclabel.size())
        self.Zpiclabel.setPixmap(pixmap3)

    def set_Icon(self):
        icon1 = QIcon("../UI/button/start-up.svg")
        self.StartButton.setIcon(icon1)

        icon2 = QIcon("../UI/button/reset (1).svg")
        self.ResetButton.setIcon(icon2)

        icon3 = QIcon("../UI/button/clock.svg")
        self.StartWoMovementButton.setIcon(icon3)

    def set_setting_ui(self):
        self.default_mode = False
        self.searchbox = False
        self.setWindowTitle("Segal Step")
        # self.InformationtabWidget.setTabEnabled(2, False)
        # self.InformationtabWidget.setTabText(2, "")

    def set_logo(self):
        pixiconimage = QPixmap("../icons/logo/logo.png")
        pixiconimage = pixiconimage.scaled(260, 150, Qt.AspectRatioMode.KeepAspectRatio)
        # self.label.setPixmap(pixiconimage)

    def onChangeOffset(self):
        a = int(self.Xplain_Vline.text())
        b = int(self.Xplain_Hline.text())
        c = int(self.Yplain_Vline.text())
        d = int(self.Yplain_Hline.text())
        e = int(self.Zplain_Vline.text())
        f = int(self.Zplain_Hline.text())

        try:
            if (a != 0):
                # LINEY_OFFSET_XPLAN += a
                Constants.LINEY_OFFSET_XPLAN += a
            else:
                print("a is not change")

                if (b != 0):
                    Constants.LINEZ_OFFSET_XPLAN += b

                else:
                    print("b is not change")

                    if (c != 0):
                        Constants.LINEX_OFFSET_YPLAN += c
                    else:
                        print("b is not change")

                        if (d != 0):
                            Constants.LINEZ_OFFSET_YPLAN += d
                        else:
                            print("d is not change")

                            if (e != 0):
                                Constants.LINEX_OFFSET_ZPLAN += e
                            else:
                                print("e is not change")
                                if (f != 0):
                                    Constants.LINEY_OFFSET_ZPLAN += f
                                else:
                                    print("f is not change")
        except:
            print("fffffffffffffffffffffffff")

    def DisableHeading(self):
        self.APSpin.setEnabled(False)
        self.EVSpin.setEnabled(False)
        self.BTSpin.setEnabled(False)

    def UnDisableHeading(self):
        self.APSpin.setEnabled(True)
        self.EVSpin.setEnabled(True)
        self.BTSpin.setEnabled(True)

    def onResetOffset(self):
        self.Xplain_Vline.setText("0")
        self.Xplain_Hline.setText("0")
        self.Yplain_Vline.setText("0")
        self.Yplain_Hline.setText("0")
        self.Zplain_Vline.setText("0")
        self.Zplain_Hline.setText("0")

        Constants.LINEY_OFFSET_XPLAN = +166
        Constants.LINEZ_OFFSET_XPLAN = +45
        ########################### plain Y
        Constants.LINEX_OFFSET_YPLAN = +166
        Constants.LINEZ_OFFSET_YPLAN = +45
        ##########################plain Z
        Constants.LINEX_OFFSET_ZPLAN = +167
        Constants.LINEY_OFFSET_ZPLAN = +60

    def moveSphere(self, _Bx, _By, _Bz):
        _xx, _yy, _zz = self.change_Coordinate_origin()
        self.brain_point.SetCenter(_xx, _yy, _zz)
        print("cccccccccccccccc", _xx, _yy, _zz)

    def change_Coordinate_origin(self):

        _Bx, _By, _Bz = int(self.Xshowlabel.text()), int(self.Yshowlabel.text()), int(self.Zshowlabel.text())

        ###############################set centrt Bx
        _Xpoint = (_By + Y_PIC_OFFSET) * (47 + 38) / (NUMBER_Y_LIST - 1)
        _centerBX = _Xpoint - 38 + X_BRAIN_OFFSET

        ###############################SET CENTER BY
        _Ypoint = (_Bx + X_PIC_OFFSET) * (50 + 21) / (NUMBER_X_LIST - 1)
        _centerBY = _Ypoint - 21 + Y_BRAIN_OFFSET

        #########################set center BZ
        _Zpoint = (_Bz + Z_PIC_OFFSET) * (53 + 12) / (NUMBER_Z_LIST - 1)
        _centerBZ = _Zpoint - 12 + Z_BRAIN_offset

        ############################set center oa
        # _oapoint = (_Boa + Z_PIC_OFFSET) * (51 + 91) / (NUMBER_Z_LIST - 1)
        # _centerBoa = _oapoint - 91

        print('center point:', _centerBX, _centerBY, _centerBZ)
        return _centerBX, _centerBY, _centerBZ

    def print_point(*args, **kwargs):
        print(args[1])

    def show_3Brain(self):

        self.Brain_interactor = QtInteractor(self.frame_14)

        self.verticalLayout_23.addWidget(self.Brain_interactor.interactor)

        mesh = pv.read('../UI/Brain for Half_Skull.stl')


        self.Brain_interactor.add_mesh(mesh, color=(158, 158, 158), specular=0.7,
                                       specular_power=15, ambient=0.3, smooth_shading=True, opacity=1)
        self.Brain_interactor.add_bounding_box( line_width=150, color='red')

       #برش# مغز
        # clipped_mesh = mesh.clip(invert=True)
        # self.Brain_interactor.add_mesh(clipped_mesh, color='blue', opacity=1)

        self.Brain_interactor.background_color = (255, 255, 255)
        self.Brain_interactor.add_text("Segal STEP   |   Segal Step AN-624",
                                       position='upper_edge', font='arial', font_size=9, color=(0, 0, 0),shadow=True)
        self.Brain_interactor.setStyleSheet("font-family: Arial; font-size: 5px; color: black;")

        self.brain_point = self.Brain_interactor.add_sphere_widget(self.print_point, color=(183, 28, 28),
                                                                   center=(0, 0, 0), radius=3, test_callback=False)


        print("center of point:", self.brain_point.SetCenter)

    def onShow_Coil(self):
        self.mesh_coil = pv.read('../UI/Coil TMS v0.stl')
        self.Brain_interactor.add_mesh(self.mesh_coil, opacity=1, color=(13, 71, 161))
        new_position = [-20, 90, 0]  # مختصات جدید موقعیت کویل را وارد کنید
        transform = np.eye(4)
        transform[:3, 3] = new_position
        self.mesh_coil.transform(transform)

        rotation_angle_degrees = 30
        rotation_axis = [0, 1, 0]  # محور y
        rotation_angle_radians = np.radians(rotation_angle_degrees)
        rotation_matrix = transformations.rotation_matrix(rotation_angle_radians, rotation_axis)
        self.mesh_coil.transform(rotation_matrix)

        rotation_angle_degrees = 70
        rotation_axis = [1, 0, 0]  # محور X
        rotation_angle_radians = np.radians(rotation_angle_degrees)
        rotation_matrix = transformations.rotation_matrix(rotation_angle_radians, rotation_axis)
        self.mesh_coil.transform(rotation_matrix)

        rotation_angle_degrees = 360
        rotation_axis = [0, 0, 1]  # محور Z
        rotation_angle_radians = np.radians(rotation_angle_degrees)
        rotation_matrix = transformations.rotation_matrix(rotation_angle_radians, rotation_axis)
        self.mesh_coil.transform(rotation_matrix)

    def onSaveFigData(self):

        config = configparser.ConfigParser()
        config['Head Adjusted Coordinates (Coil Position):'] = {}
        config['forge.example'] = {}
        config['forge.example']['X'] = self.Xshowlabel.text()
        config['forge.example']['Y'] = self.Yshowlabel.text()

        config['forge.example']['Z'] = self.Zshowlabel.text()
        config['forge.example']['OA'] = self.OAshowlabel.text()
        config['forge.example']['CA'] = self.CAshowlabel.text()

        fileName = QFileDialog.getSaveFileName(self, ("Save data"), '', ("*.txt"))

        with open(fileName[0], 'w') as configfile:
            config.write(configfile)

    def on_dark_theme(self):
        apply_stylesheet(self, theme='../UI/dark_purp_segal.xml')

    def on_light_theme(self):
        apply_stylesheet(self, theme='../UI/color.xml')

    def onShow_slider_onBrain(self):
        self.slider_onBrain_x = self.Brain_interactor.add_slider_widget \
            (None, rng=[-87, 86], value=0, title="RightLeft_x", pointa=(0.025, 0.1), pointb=(0.31, 0.1), style='modern')

        self.slider_onBrain_y = self.Brain_interactor.add_slider_widget \
            (None, rng=[-122, 90], value=-14, title="FrontBack_y", pointa=(0.35, 0.1), pointb=(0.64, 0.1),
             style='modern')
        self.slider_onBrain_z = self.Brain_interactor.add_slider_widget \
            (None, rng=[-43, 99], value=98, title="UpDown_z", pointa=(0.67, 0.1), pointb=(0.98, 0.1), style='modern')

    def onHide_slider_onBrain(self):
        print("Brain")


    def initAllpicture(self):

        ########################################### sort of listX
        picListX = os.listdir(my_Xside_pics_add)
        listXminus = []
        listXplus = []
        for item in picListX:
            if item[0] == '-':
                listXminus.append(item)
            elif item[0] == '+':
                listXplus.append(item)
        listXplus.sort()
        listXminus.sort(reverse=True)
        self.picListX = []
        self.picListX.extend(listXminus)
        self.picListX.append('0x.jpg')
        self.picListX.extend(listXplus)


        ########################################### sort of listY
        picListY = os.listdir(my_Yside_pics_add)
        listYplus = []
        listYminus = []

        for item in picListY:
            if item[0] == '-':
                listYminus.append(item)
            elif item[0] == '+':
                listYplus.append(item)

        listYplus.sort()
        listYminus.sort(reverse=True)

        self.picListY = []
        self.picListY.extend(listYminus)
        self.picListY.append('0y.jpg')
        self.picListY.extend(listYplus)

        ######################################### SORT OF LIST Z
        picListZ = os.listdir(my_Zside_pics_add)
        listZminus = []
        listZplus = []
        for item in picListZ:
            if item[0] == '-':
                listZminus.append(item)
            elif item[0] == '+':
                listZplus.append(item)
        listZplus.sort()
        listZminus.sort(reverse=True)
        self.picListZ = []
        self.picListZ.extend(listZminus)
        self.picListZ.append('0z.jpg')
        self.picListZ.extend(listZplus)

    def onSliderchangeClicked(self, val):
        _mx, _my, _mz = self.xyz_calculator(self.XSlider.value(), self.YSlider.value(), self.ZSlider.value(), 0)

        self.update_pics_lines(_mx, _my, _mz)
        self.change_spin_vals(_mx, _my, _mz)

    def onStartBottonClicked(self):
        print("mmmmmm")
        _mx, _my, _mz = self.xyz_calculator(self.XSpin.value(), self.YSpin.value(), self.ZSpin.value(), 1)
        _moa = self.OASpin.value()
        _mca = self.CASpin.value()
        print("salam", _mx, _my, _mz)

        self.x_go = _mx
        self.y_go = _my
        self.z_go = _mz
        self.oa_go = _moa
        self.ca_go = _mca
        print("starting timer ....")

        self.timer.start(100)

    def onResetBotton(self):
        self.XSpin.setValue(16)
        self.YSpin.setValue(-14)
        self.ZSpin.setValue(10)
        self.CASpin.setValue(0)
        self.OASpin.setValue(0)
        # self.moveSphere(0, -14, 98)
        self.brain_point.SetCenter(12, -6, 97)

        _mx, _my, _mz = self.xyz_calculator(self.XSpin.value(), self.YSpin.value(), self.ZSpin.value(), 1)

        self.x_go = _mx
        self.y_go = _my
        self.z_go = _mz
        # self.oa_go = _moa
        # self.ca_go = _mca

        self.update_pics_lines(_mx, _my, _mz)
        self.change_slider_Pos(_mx, _my, _mz)

    def onStartWoMovementButton(self):
        _mx, _my, _mz = self.xyz_calculator(self.XSpin.value(), self.YSpin.value(), self.ZSpin.value(), 1)
        _moa = self.OASpin.value()
        _mca = self.CASpin.value()

        # self.x_go = _mx
        # self.y_go = _my
        # self.z_go = _mz
        # self.oa_go = _moa
        # self.ca_go = _mca

        # self.NoteBrowser.setText("Go to Cpoint")

        self.update_pics_lines_and_now_position(_mx, _my, _mz)
        self.change_slider_Pos(_mx, _my, _mz)
        self.CAshowlabel.setText(str(_mca))
        self.OAshowlabel.setText(str(_moa))

    def onTimer_interrupt(self):
        _mx = 0
        _my = 0
        _mz = 0

        self.moveSphere(self.x_now, self.y_now, self.z_now)

        ################################# x check
        if self.x_now != self.x_go:
            if self.x_now < self.x_go:
                _mx = self.x_now + 1
            else:
                _mx = self.x_now - 1

            _my = self.y_now
            _mz = self.z_now
            self.update_pics_lines_and_now_position(_mx, _my, _mz)
            self.change_slider_Pos(_mx, _my, _mz)

        else:
            _mx = self.x_now
            ################################# y check
            if self.y_now != self.y_go:
                if self.y_now < self.y_go:
                    _my = self.y_now + 1
                else:
                    _my = self.y_now - 1

                _mz = self.z_now
                self.update_pics_lines_and_now_position(_mx, _my, _mz)
                self.change_slider_Pos(_mx, _my, _mz)

            else:
                _my = self.y_now
                ################################# OA check
                if self.oa_now != self.oa_go:
                    if self.oa_now < self.oa_go:
                        self.oa_now = self.oa_now + 1
                    else:
                        self.oa_now = self.oa_now - 1
                    self.OAshowlabel.setText(str(self.oa_now))

                    _mz = self.z_now
                    self.update_pics_lines_and_now_position(_mx, _my, _mz)
                    self.change_slider_Pos(_mx, _my, _mz)

                else:
                    ################################ z check
                    if self.z_now != self.z_go:
                        if self.z_now < self.z_go:
                            _mz = self.z_now + 1
                        else:
                            _mz = self.z_now - 1

                        self.update_pics_lines_and_now_position(_mx, _my, _mz)
                        self.change_slider_Pos(_mx, _my, _mz)
                    else:
                        _mz = self.z_now
                        ################################# OA check
                        if self.oa_now != self.oa_go:
                            if self.oa_now < self.oa_go:
                                self.oa_now = self.oa_now + 1
                            else:
                                self.oa_now = self.oa_now - 1
                            self.OAshowlabel.setText(str(self.oa_now))
                        else:
                            if self.ca_now != self.ca_go:
                                if self.ca_now < self.ca_go:
                                    self.ca_now = self.ca_now + 1
                                else:
                                    self.ca_now = self.ca_now - 1
                                self.CAshowlabel.setText(str(self.ca_now))

                            else:
                                self.update_pics_lines_and_now_position(_mx, _my, _mz)
                                self.change_slider_Pos(_mx, _my, _mz)
                                self.CAshowlabel.setText(str(self.ca_now))
                                self.OAshowlabel.setText(str(self.oa_now))
                                self.timer.stop()

    def xyz_calculator(self, mx, my, mz, scale_flag):
        if scale_flag:
            valueBt = self.BTSpin.value()
            valueEv = self.EVSpin.value()
            valueAp = self.APSpin.value()

            if self.default_mode == True:
                BTIndices, EVIndices, APIndices = self.onSet_button_clicked()

            else:
                BTIndices = NUMBER_X_LIST
                EVIndices = NUMBER_Y_LIST
                APIndices = NUMBER_Z_LIST

            _scaleX = valueBt / BTIndices
            _scaleY = valueAp / EVIndices
            _scaleZ = valueEv / APIndices

            _cx = int((int(mx) + X_PIC_OFFSET) * _scaleX)
            _cy = int((int(my) + Y_PIC_OFFSET) * _scaleY)
            _cz = int((int(mz) + Z_PIC_OFFSET) * _scaleZ)


        else:
            _cx = int(mx)
            _cy = int(my)
            _cz = int(mz)

        return _cx, _cy, _cz

    def change_slider_Pos(self, valX, valY, valZ):
        self.XSlider.setValue(valX)
        self.YSlider.setValue(valY)
        self.ZSlider.setValue(valZ)

    def X_label_modifier(self, valX, valY, valZ):
        _ximg = QPixmap(my_Xside_pics_add + self.picListX[valX])
        self.pixmap_XX3 = QPixmap(self.Xpiclabel.size())

        # تنظیم مقیاس عکس و رسم آن درون pixmap_XX3
        scaled_ximg = _ximg.scaled(self.Xpiclabel.size(), aspectRatioMode=Qt.KeepAspectRatio)


        qpx = QPainter(self.pixmap_XX3)
        qpx.drawPixmap(self.Xpiclabel.rect(), scaled_ximg)

        #########add text to pic
        font = QFont()
        font.setPointSize(10)
        qpx.setFont(font)
        qpx.setPen(QColor(158, 158, 158))
        qpx.drawText(10, 18, " X Axis")

        # horiz line  z
        dummy = abs(NUMBER_Z_LIST - 1 - valZ)
        dummy += Constants.LINEZ_OFFSET_XPLAN
        pen = QPen(Qt.blue, 3)
        qpx.setPen(pen)
        qpx.drawLine(-700, dummy, 700, dummy)

        # vertical line,y
        myy_loc = abs(NUMBER_Y_LIST - 1 - valY)
        myy_loc += Constants.LINEY_OFFSET_XPLAN
        pen = QPen(Qt.green, 3)
        qpx.setPen(pen)
        qpx.drawLine(myy_loc, 500, myy_loc, -500)
        qpx.end()

        self.Xpiclabel.setPixmap(self.pixmap_XX3)

    def Y_label_modifier(self, valX, valY, valZ):
        _yimg = QPixmap(my_Yside_pics_add + self.picListY[valY])
        self.pixmap_YY = QPixmap(self.Ypiclabel.size())

        qpy = QPainter(self.pixmap_YY)
        qpy.drawPixmap(self.Ypiclabel.rect(), _yimg)

        #########add text to pic
        font = QFont()
        font.setPointSize(10)
        qpy.setFont(font)
        qpy.setPen(QColor(158, 158, 158))
        qpy.drawText(10, 18, " Y Axis")

        ############# horiz Line ,z
        pen = QPen(Qt.blue, 3)
        qpy.setPen(pen)
        dummy = abs(NUMBER_Z_LIST - 1 - valZ)
        dummy += Constants.LINEZ_OFFSET_YPLAN
        qpy.drawLine(-800, dummy, 800, dummy)

        ###########vert Line,x
        pen = QPen(Qt.red, 3)
        qpy.setPen(pen)
        dummy = valX
        dummy += Constants.LINEX_OFFSET_YPLAN
        qpy.drawLine(dummy, 500, dummy, -500)
        qpy.end()

        self.Ypiclabel.setPixmap(self.pixmap_YY)

    def Z_label_modifier(self, valX, valY, valZ):
        _zimg = QPixmap(my_Zside_pics_add + self.picListZ[valZ])
        self.pixmap_ZZ2 = QPixmap(self.Zpiclabel.size())

        self.qpz = QPainter(self.pixmap_ZZ2)
        self.qpz.drawPixmap(self.Zpiclabel.rect(), _zimg)

        #########add text to pic
        font = QFont()
        font.setPointSize(10)
        self.qpz.setFont(font)
        self.qpz.setPen(QColor(158, 158, 158))
        self.qpz.drawText(10, 18, " Z Axis")

        ########### horiz,y
        pen = QPen(Qt.green, 3)
        dummy = abs(NUMBER_Y_LIST - 1 - valY)
        dummy += Constants.LINEY_OFFSET_ZPLAN
        self.qpz.setPen(pen)
        self.qpz.drawLine(-800, dummy, 800, dummy)

        ########## vertic,x
        pen = QPen(Qt.red, 3)
        self.qpz.setPen(pen)
        dummy = valX
        dummy += Constants.LINEX_OFFSET_ZPLAN
        self.qpz.drawLine(dummy, 500, dummy, -500)
        self.qpz.end()
        self.Zpiclabel.setPixmap(self.pixmap_ZZ2)

    def update_pics_lines(self, valX, valY, valZ):
        self.X_label_modifier(valX, valY, valZ)
        self.Y_label_modifier(valX, valY, valZ)
        self.Z_label_modifier(valX, valY, valZ)

    def update_pics_lines_and_now_position(self, valX, valY, valZ):
        self.X_label_modifier(valX, valY, valZ)
        self.Y_label_modifier(valX, valY, valZ)
        self.Z_label_modifier(valX, valY, valZ)

        self.x_now = valX
        self.y_now = valY
        self.z_now = valZ

        self.Xshowlabel.setText(str(self.x_now - X_PIC_OFFSET))
        self.Yshowlabel.setText(str(self.y_now - Y_PIC_OFFSET))
        self.Zshowlabel.setText(str(self.z_now - Z_PIC_OFFSET))
        self.OAshowlabel.setText(str(self.oa_now))
        self.CAshowlabel.setText(str(self.ca_now))

    def change_spin_vals(self, valX, valY, valZ):

        self.XSpin.setValue(valX - X_PIC_OFFSET)
        self.YSpin.setValue(valY - Y_PIC_OFFSET)
        self.ZSpin.setValue(valZ - Z_PIC_OFFSET)

    def onMyHideShow(self):
        if self.frame_2.isHidden() == False:
            self.frame_2.hide()
            self.actionHideMenu.setText("Show Menu")
            print("closed")
        else:
            self.frame_2.show()
            self.actionHideMenu.setText("Hide Menu")

    def onMyHideOffseting(self):
        if self.OffsetinggroupBox.isHidden() == False:
            self.OffsetinggroupBox.hide()
            # self.HideMenuButton.setText("Show Menu")
            print("closed")
        else:
            self.OffsetinggroupBox.show()


import configparser
import os
import easygui as easygui
import numpy as np
import pyvista as pv

from pyvistaqt import QtInteractor
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage, QFont, QColor
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from qt_material import apply_stylesheet
from src.NCPSUI_ui import Ui_MainWindow




motor_real = False


##############################read txt file
with open("../UI/defultvariable.txt", "+r") as f:
    contents = f.read()

exec(contents)
#################################################



class Window_ui(QMainWindow, Ui_MainWindow):
    def __init__(self,  parent=None):
        super().__init__(parent)
        os.getcwd()
        self.setupUi(self)
        self.closeBotton.hide()
        self.minimizBotton.hide()
        self.setWindowTitle("SEGAL NCPS")
        self.OffsetinggroupBox.hide()


        self.timer = QTimer()
        self.initAllpicture()
        self.signalsSlat()
        self.show_3Brain()


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

        self.onResetBotton()
        self.update_pics_lines_and_now_position(self.x_go, self.y_go, self.z_go)
        self.change_slider_Pos(self.x_go, self.y_go, self.z_go)



    def signalsSlat(self):

        self.StartButton.clicked.connect(self.onStartBottonClicked)
        self.XSlider.valueChanged.connect(self.onSliderchangeClicked)
        self.YSlider.valueChanged.connect(self.onSliderchangeClicked)
        self.ZSlider.valueChanged.connect(self.onSliderchangeClicked)
        self.ResetButton.clicked.connect(self.onResetBotton)
        self.SetOffsetButton.clicked.connect(self.onChangeOffset)
        self.ResetOffsetButton.clicked.connect(self.onResetOffset)
        self.actionShow_Offseting.triggered.connect(self.onMyHideOffseting)

        self.HideMenuButton.clicked.connect(self.onMyHideShow)
        self.timer.timeout.connect(self.onTimer_interrupt)
        self.actionChange_Offset.triggered.connect(self.onMyHideOffseting)
        ###############################MENU BAR
        self.actionDark.triggered.connect(self.on_dark_theme)
        self.actionLight.triggered.connect(self.on_light_theme)
        self.actiondialog.triggered.connect(self.on_show_dialog)
        self.actionSave_as.triggered.connect(self.onSaveFigData)
        self.actionShow.triggered.connect(self.onShow_slider_onBrain)
        self.actionHide.triggered.connect(self.onHide_slider_onBrain)
        self.actionOpen.triggered.connect(self.getfile)


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



    def onChangeOffset(self):
        a = int(self.Xplain_Vline.text())
        b = int(self.Xplain_Hline.text())
        c = int(self.Yplain_Vline.text())
        d = int(self.Yplain_Hline.text())
        e = int(self.Zplain_Vline.text())
        f = int(self.Zplain_Hline.text())

        self.aa = LINEY_OFFSET_XPLAN + a
        self.bb = LINEZ_OFFSET_XPLAN + b
        print("hhhhhhhhhhhhh",self.aa)

        ########################### plain Y
        self.cc = LINEX_OFFSET_YPLAN + c
        self.dd = LINEZ_OFFSET_YPLAN + d

        ##########################plain Z
        self.ee = LINEX_OFFSET_ZPLAN + e
        self.ff = LINEY_OFFSET_ZPLAN + f


        if ( a != 0):
            self.aa += a
        else:
            print("a is not change")
            if ( b != 0):
                self.bb += b
            else:
                print("b is not change")
                if ( c != 0):
                    self.cc += c
                else:
                    print("b is not change")
                    if( d != 0):
                        self.dd += d
                    else:
                        print("d is not change")
                        if( e != 0):
                            self.ee += e
                        else:
                            print("e is not change")
                            if ( f != 0):
                                self.ff += f
                            else:
                                print(" f is not change")


    def onResetOffset(self):
        self.Xplain_Vline.setText("0")
        self.Xplain_Hline.setText("0")
        self.Yplain_Vline.setText("0")
        self.Yplain_Hline.setText("0")
        self.Zplain_Vline.setText("0")
        self.Zplain_Hline.setText("0")



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
        mesh = pv.read(brain_stlfile_path).triangulate().decimate(0.7)
        # mesh = examples.download_cow().triangulate().decimate(0.7)



        self.Brain_interactor.add_mesh(mesh ,color=(158, 158, 158), opacity=0.6)

        self.Brain_interactor.background_color = (0, 0, 0)

        self.Brain_interactor.add_text("Segal NCPS   |   Navigated Coil Placement System", position='upper_edge', font='arial', font_size=5, color=None)
        self.brain_point = self.Brain_interactor.add_sphere_widget(self.print_point, color=(183, 28, 28), center=(0, 0, 0),  radius=3, test_callback=False)

        print("center of point:", self.brain_point.SetCenter)


###############################################
        # self.brain_point.SetCenter(14, -6, 96)


        # self.Brain_interactor.add_mesh(edges, color="green", line_width=5)
        # self.Brain_interactor.add_mesh(dataset, style='wireframe', color='blue', label='Input')
        # self.Brain_interactor.add_mesh(edges, color="red", line_width=2)



    def onSaveFigData(self):

        config = configparser.ConfigParser()
        config['Head Adjusted Coordinates (Coil Position):'] = {}
        config['forge.example'] = {}
        config['forge.example']['X'] = self.Xshowlabel.text()
        config['forge.example']['Y'] = self.Yshowlabel.text()
        config['forge.example']['Z'] = self.Zshowlabel.text()
        config['forge.example']['OA'] = self.OAshowlabel.text()
        config['forge.example']['CA'] = self.CAshowlabel.text()


        fileName = QFileDialog.getSaveFileName(self, ("Save data"), '',("*.txt"))

        with open(fileName[0], 'w') as configfile:
            config.write(configfile)

    def on_show_dialog(self, s):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(" Information ")
        dlg.setText("Save Information")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Information)

        returnValue = dlg.exec()
        if returnValue == QMessageBox.Yes:
            print('OK clicked')
        dlg.exec()

    def on_dark_theme(self):
        apply_stylesheet(self, theme='../UI/dark_purp_segal.xml')

    def on_light_theme(self):
        apply_stylesheet(self, theme='../UI/color.xml')

    def onShow_slider_onBrain(self):
        self.slider_onBrain_x=self.Brain_interactor.add_slider_widget\
            (None,  rng=[-87, 86], value=0, title="RightLeft_x", pointa=(0.025, 0.1), pointb=(0.31, 0.1), style='modern')

        self.slider_onBrain_y=self.Brain_interactor.add_slider_widget\
            (None,   rng=[-122, 90], value=-14, title="FrontBack_y", pointa=(0.35, 0.1), pointb=(0.64, 0.1), style='modern')
        self.slider_onBrain_z= self.Brain_interactor.add_slider_widget\
            (None,  rng=[-43, 99], value=98, title="UpDown_z", pointa=(0.67, 0.1), pointb=(0.98, 0.1), style='modern')

    def onHide_slider_onBrain(self):
        print("Brain")


    def getfile(self):

        file_path = easygui.fileopenbox()

        with open(file_path, "r") as f:

            lines = f.readlines()
            line1 = lines[0].strip()
            line2 = lines[1].strip()
            line3 = lines[2].strip()


            line1parts = line1.split()
            line2parts = line2.split()
            line3parts = line3.split()

            x = int(line1parts[2])
            y = int(line2parts[2])
            z = int(line3parts[2])


            message = "value of x = {}\n\nvalue of y = {}\n\nvalue of z = {}\n\n ".format(x , y , z)
            msg_box = QMessageBox()
            msg_box.setText(message)
            msg_box.setWindowTitle("Confirm Information")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.resize(1200, 600)
            msg_box.exec_()


            self.XSpin.setValue(x)
            self.YSpin.setValue(y)
            self.ZSpin.setValue(z)

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

        _mx, _my, _mz = self.xyz_calculator(self.XSpin.value(), self.YSpin.value(), self.ZSpin.value(), 1)
        _moa = self.OASpin.value()
        _mca = self.CASpin.value()

        self.x_go = _mx
        self.y_go = _my
        self.z_go = _mz
        self.oa_go = _moa
        self.ca_go = _mca
        print("starting timer ....")
        self.NoteBrowser.setText("Go to Cpoint")

        self.timer.start(100)

    def onResetBotton(self):
        self.XSpin.setValue(0)
        self.YSpin.setValue(-14.41)
        self.ZSpin.setValue(98)
        self.CASpin.setValue(0)
        self.OASpin.setValue(0)
        # self.moveSphere(0, -14, 98)
        self.brain_point.SetCenter(12, -6, 97)

        _mx, _my, _mz = self.xyz_calculator(self.XSpin.value(), self.YSpin.value(), self.ZSpin.value(), 1)
        self.NoteBrowser.setText("Please enter the numbers")

        self.x_go = _mx
        self.y_go = _my
        self.z_go = _mz
        # self.oa_go = _moa
        # self.ca_go = _mca


        self.update_pics_lines(_mx, _my, _mz)
        self.change_slider_Pos(_mx, _my, _mz)

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
            ######################################### calculate x value
            valueBt = self.BTSpin.value()
            _scaleX = valueBt / NUMBER_X_LIST
            _cx = int(mx) + X_PIC_OFFSET
            ######################################### calculate y value
            valueAp = self.APSpin.value()
            _scaleY = valueAp / NUMBER_Y_LIST
            _cy = int(my) + Y_PIC_OFFSET
            ######################################### calculate z value
            valueEv = self.EVSpin.value()
            _scaleZ = valueEv / NUMBER_Z_LIST
            _cz = int(mz) + Z_PIC_OFFSET

        else:
            _cx = int(mx)
            _cy = int(my)
            _cz = int(mz)

        return _cx, _cy, _cz

    def change_slider_Pos(self,valX, valY, valZ):
        self.XSlider.setValue(valX)
        self.YSlider.setValue(valY)
        self.ZSlider.setValue(valZ)

    def X_label_modifier(self, valX, valY, valZ):
        _ximg = QPixmap(my_Xside_pics_add + self.picListX[valX])
        self.pixmap_XX3 = QPixmap(self.Xpiclabel.size())

        qpx = QPainter(self.pixmap_XX3)
        qpx.drawPixmap(self.Xpiclabel.rect(), _ximg)


        #########add text to pic
        font = QFont()
        font.setPointSize(10)
        qpx.setFont(font)
        qpx.setPen(QColor(158, 158, 158))
        qpx.drawText(10, 18, " X Axis")


        #horiz line  z
        dummy = abs(NUMBER_Z_LIST - 1 - valZ)
        dummy += LINEZ_OFFSET_XPLAN
        pen = QPen(Qt.red, 3)
        qpx.setPen(pen)
        qpx.drawLine(-700, dummy, 700, dummy)

        # vertical line,y
        myy_loc = abs(NUMBER_Y_LIST - 1 - valY)
        myy_loc += LINEY_OFFSET_XPLAN
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
        pen = QPen(Qt.red, 3)
        qpy.setPen(pen)
        dummy = abs(NUMBER_Z_LIST - 1 - valZ)
        dummy += LINEZ_OFFSET_YPLAN
        qpy.drawLine(-800, dummy, 800, dummy)

        ###########vert Line,x
        pen = QPen(Qt.green, 3)
        qpy.setPen(pen)
        dummy = valX
        dummy += LINEX_OFFSET_YPLAN
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
        pen = QPen(Qt.red, 3)
        dummy = abs(NUMBER_Y_LIST - 1 - valY)
        dummy += LINEY_OFFSET_ZPLAN
        self.qpz.setPen(pen)
        self.qpz.drawLine(-800, dummy, 800, dummy)

        ########## vertic,x
        pen = QPen(Qt.green, 3)
        self.qpz.setPen(pen)
        dummy = valX
        dummy += LINEX_OFFSET_ZPLAN
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
        if self.frame_3.isHidden() == False:
            self.frame_3.hide()
            self.HideMenuButton.setText("Show Menu")
            print("closed")
        else:
            self.frame_3.show()
            self.HideMenuButton.setText("Hide Menu")

    def onMyHideOffseting(self):
        if self.OffsetinggroupBox.isHidden() == False:
            self.OffsetinggroupBox.hide()
            # self.HideMenuButton.setText("Show Menu")
            print("closed")
        else:
            self.OffsetinggroupBox.show()



import configparser
import os



import pyvista as pv

from pyvistaqt import QtInteractor
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from qt_material import apply_stylesheet
from src.Ui12_ui import Ui_MainWindow


motor_real = False
brain_stlfile_path ='./UI/Brain for Half_Skull.stl'
########################addres of All pic
my_Xside_pics_add = './UI/MRI_PROJECT/MRI_FINAL_reza2/X_174/'
my_Yside_pics_add = './UI/MRI_PROJECT/MRI_FINAL_reza2/Y_212/'
my_Zside_pics_add = './UI/MRI_PROJECT/MRI_FINAL_reza2/Z_142/'


########################## plain X
LINEY_OFFSET_XPLAN = +145
LINEZ_OFFSET_XPLAN = +45


########################### plain Y
LINEX_OFFSET_YPLAN = +157
LINEZ_OFFSET_YPLAN = +45


##########################plain Z
LINEX_OFFSET_ZPLAN = +156
LINEY_OFFSET_ZPLAN = +52


#################for set number of pic
X_PIC_OFFSET = 87
Y_PIC_OFFSET = 122
Z_PIC_OFFSET = 43

##################number of list x,y,z
NUMBER_X_LIST = 174
NUMBER_Y_LIST = 212
NUMBER_Z_LIST = 142



class Window_ui(QMainWindow, Ui_MainWindow):
    def __init__(self,  parent=None):
        super().__init__(parent)

        self.setupUi(self)

        self.CloseButton.hide()
        self.minimizedButton.hide()
        self.setWindowTitle("SEGAL NCPS")
        self.frame_23.setMaximumWidth(560)


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

        self.StartBotton.clicked.connect(self.onStartBottonClicked)
        self.Xslider.sliderMoved.connect(self.onSliderchangeClicked)
        self.Yslider.sliderMoved.connect(self.onSliderchangeClicked)
        self.Zslider.sliderMoved.connect(self.onSliderchangeClicked)
        self.ResetButton.clicked.connect(self.onResetBotton)


        self.HideShowButton.clicked.connect(self.onMyHideShow)
        self.timer.timeout.connect(self.onTimer_interrupt)

        ###############################MENU BAR
        self.actionDark.triggered.connect(self.on_dark_theme)
        self.actionLight.triggered.connect(self.on_light_theme)
        self.actiondialog.triggered.connect(self.on_show_dialog)
        self.actionSave_as.triggered.connect(self.onSaveFigData)
        self.actionShow_Botten.triggered.connect(self.onShow_slider_onBrain)
        self.actionHide_Botton.triggered.connect(self.onHide_slider_onBrain)

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

        #################### Signal and slot for brain sphere update
        # self.Xslider.sliderMoved.connect(self.on_change_sphere_by_sliderX)
        # self.Yslider.sliderMoved.connect(self.on_change_sphere_by_sliderY)
        # self.Zslider.sliderMoved.connect(self.on_change_sphere_by_sliderZ)


    # def on_change_sphere_by_sliderX(self, val):
    #     self.centerBY = val
    #     self.show_sphere()
    #
    # def on_change_sphere_by_sliderY(self, val):
    #     self.centerBX = val
    #     self.show_sphere()
    #
    # def on_change_sphere_by_sliderZ(self, val):
    #     self.centerBZ = val
    #     self.show_sphere()

    def moveSphere(self, _x, _y, _z, _oa):
        self.brain_point.SetCenter(self.fit_sphere_by_SpinValues(_x, _y, _z, _oa))



    def fit_sphere_by_SpinValues(self, _Bx, _By, _Bz, _oa):
        _xx, _yy, _zz = self.change_Coordinate_origin(_Bx, _By, _Bz)

        #do calcultations based on _xx , _yy, _zz, _oa
        # _finalx, _finaly, _finalz = 0, 0, 0

        #return _finalx, _finaly, _finalz
        return _xx, _yy, _zz


    def change_Coordinate_origin(self, _Bx, _By, _Bz):

        ###############################set centrt Bx
        _Xpoint = (_By + Y_PIC_OFFSET) * (33 + 42) / (NUMBER_Y_LIST - 1)
        _centerBX = _Xpoint - 42


        ###############################SET CENTER BY
        _Ypoint = (_Bx + X_PIC_OFFSET) * (50 + 13) / (NUMBER_X_LIST - 1)
        _centerBY = _Ypoint - 13


        #########################set center BZ
        _Zpoint = (_Bz + Z_PIC_OFFSET) * (51 + 91) / (NUMBER_Z_LIST - 1)
        _centerBZ = _Zpoint - 91
        ##################################

        print('center point:', _centerBX, _centerBY, _centerBZ)
        return _centerBX, _centerBY, _centerBZ

    def print_point(*args, **kwargs):
        print(args[1])

    def show_3Brain(self):

        self.Brain_interactor = QtInteractor(self.frame_8)
        self.verticalLayout_38.addWidget(self.Brain_interactor.interactor)
        mesh = pv.read(brain_stlfile_path)
        self.Brain_interactor.add_mesh(mesh, color=(158, 158, 158), opacity=0.6)

        self.Brain_interactor.camera.position = (100, 300, 100)
        # self.Brain_interactor.camera.elevation = 90
        self.Brain_interactor.background_color = (0, 0, 0)
        self.Brain_interactor.add_text("Segal NCPS   |   Navigated Coil Placement System", position= 'upper_edge', font= 'arial', font_size=5, color=None)
        self.brain_point = self.Brain_interactor.add_sphere_widget(self.print_point, color=(183, 28, 28), center=(0, 0, 0),  radius=3, test_callback=False)
        print("center of point:", self.brain_point.SetCenter)


    def onSaveFigData(self):

        config = configparser.ConfigParser()
        config['Head Adjusted Coordinates (Coil Position):'] = {}
        config['forge.example'] = {}
        config['forge.example']['X'] = self.XlabelShow.text()
        config['forge.example']['Y'] = self.YlabelShow.text()
        config['forge.example']['Z'] = self.ZlabelShow.text()
        config['forge.example']['OA'] = self.OAlabelShow.text()
        config['forge.example']['CA'] = self.CAlabelShow.text()

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
        print('dark theme')
        apply_stylesheet(self, theme='dark_purp_segal.xml')

    def on_light_theme(self):
        print('light them')
        apply_stylesheet(self, theme='color.xml')

    def onShow_slider_onBrain(self):
        self.slider_onBrain_x=self.Brain_interactor.add_slider_widget(None,  rng=[-87, 86], value=0, title="RightLeft_x", pointa=(0.025, 0.1), pointb=(0.31, 0.1), style='modern')
        self.slider_onBrain_y=self.Brain_interactor.add_slider_widget(None,   rng=[-122, 90], value=-14, title="FrontBack_y", pointa=(0.35, 0.1), pointb=(0.64, 0.1), style='modern')
        self.slider_onBrain_z= self.Brain_interactor.add_slider_widget(None,  rng=[-43, 99], value=98, title="UpDown_z", pointa=(0.67, 0.1), pointb=(0.98, 0.1), style='modern')

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

    def onSliderchangeClicked(self):
        _mx, _my, _mz = self.xyz_calculator(self.Xslider.value(), self.Yslider.value(), self.Zslider.value(), 0)

        self.update_pics_lines(_mx, _my, _mz)
        self.change_spin_vals(_mx, _my, _mz)

    def onStartBottonClicked(self):
        _mx, _my, _mz = self.xyz_calculator(self.Xspin.value(), self.Yspin.value(), self.Zspin.value(), 1)
        _moa = self.OAspin.value()
        _mca = self.CAspin.value()

        self.x_go = _mx
        self.y_go = _my
        self.z_go = _mz
        self.oa_go = _moa
        self.ca_go = _mca
        print("starting timer ....")
        self.timer.start(100)

    def onResetBotton(self):
        self.Xspin.setValue(0)
        self.Yspin.setValue(-14.41)
        self.Zspin.setValue(98)
        self.CAspin.setValue(0)
        self.OAspin.setValue(0)

        _mx, _my, _mz = self.xyz_calculator(self.Xspin.value(), self.Yspin.value(), self.Zspin.value(), 1)


        self.x_go = _mx
        self.y_go = _my
        self.z_go = _mz
        # self.oa_go = _moa
        # self.ca_go = _mca


        self.update_pics_lines(_mx, _my, _mz)
        self.change_slider_Pos(_mx, _my, _mz)

        self.brain_point.SetCenter(-46, -13, 100)

    def onTimer_interrupt(self):
        _mx = 0
        _my = 0
        _mz = 0


        
        self.moveSphere(self.x_now, self.y_now, self.z_now, self.oa_now)

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
                    self.OAlabelShow.setText(str(self.oa_now))

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
                            self.OAlabelShow.setText(str(self.oa_now))
                        else:
                            if self.ca_now != self.ca_go:
                                if self.ca_now < self.ca_go:
                                    self.ca_now = self.ca_now + 1
                                else:
                                    self.ca_now = self.ca_now - 1
                                self.CAlabelShow.setText(str(self.ca_now))

                            else:
                                self.update_pics_lines_and_now_position(_mx, _my, _mz)
                                self.change_slider_Pos(_mx, _my, _mz)
                                self.CAlabelShow.setText(str(self.ca_now))
                                self.OAlabelShow.setText(str(self.oa_now))
                                self.timer.stop()

    def xyz_calculator(self, mx, my, mz, scale_flag):
        if scale_flag:
            ######################################### calculate x value
            valueBt = self.BTspinbox.value()
            _scaleX = valueBt / NUMBER_X_LIST
            _cx = int(mx) + X_PIC_OFFSET
            ######################################### calculate y value
            valueAp = self.APspinbox.value()
            _scaleY = valueAp / NUMBER_Y_LIST
            _cy = int(my) + Y_PIC_OFFSET
            ######################################### calculate z value
            valueEv = self.EVspinbox.value()
            _scaleZ = valueEv / NUMBER_Z_LIST
            _cz = int(mz) + Z_PIC_OFFSET

        else:
            _cx = int(mx)
            _cy = int(my)
            _cz = int(mz)

        return _cx, _cy, _cz

    def change_slider_Pos(self,valX, valY, valZ):
        self.Xslider.setValue(valX)
        self.Yslider.setValue(valY)
        self.Zslider.setValue(valZ)


    def X_label_modifier(self, valX, valY, valZ):
        _ximg = QPixmap(my_Xside_pics_add + self.picListX[valX])
        self.pixmap_XX3 = QPixmap(self.Xpiclabel.size())


        #horiz line  z
        dummy = abs(NUMBER_Z_LIST - 1 - valZ)
        dummy += LINEZ_OFFSET_XPLAN
        qpx = QPainter(self.pixmap_XX3)
        qpx.drawPixmap(self.Xpiclabel.rect(), _ximg)
        pen = QPen(Qt.red, 3)
        qpx.setPen(pen)
        qpx.drawLine(-600, dummy, 600, dummy)

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

        ############# horiz Line ,z
        qpy = QPainter(self.pixmap_YY)
        qpy.drawPixmap(self.Ypiclabel.rect(), _yimg)

        pen = QPen(Qt.red, 3)
        qpy.setPen(pen)
        dummy = abs(NUMBER_Z_LIST - 1 - valZ)
        dummy += LINEZ_OFFSET_YPLAN
        qpy.drawLine(-600, dummy, 600, dummy)

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

        ########### horiz,y
        pen = QPen(Qt.red, 3)
        dummy = abs(NUMBER_Y_LIST - 1 - valY)
        dummy += LINEY_OFFSET_ZPLAN
        self.qpz.setPen(pen)
        self.qpz.drawLine(-600, dummy, 600, dummy)

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


        self.XlabelShow.setText(str(self.x_now - X_PIC_OFFSET))
        self.YlabelShow.setText(str(self.y_now - Y_PIC_OFFSET))
        self.ZlabelShow.setText(str(self.z_now - Z_PIC_OFFSET))
        self.OAlabelShow.setText(str(self.oa_now))
        self.CAlabelShow.setText(str(self.ca_now))

    def change_spin_vals(self, valX, valY, valZ):
        self.Xspin.setValue(valX - X_PIC_OFFSET)
        self.Yspin.setValue(valY - Y_PIC_OFFSET)
        self.Zspin.setValue(valZ - Z_PIC_OFFSET)

    def onMyHideShow(self):
        if self.frame_36.isHidden() == False:
            self.frame_36.hide()
            self.HideShowButton.setText("Show Menu")
            print("closed")
        else:
            self.frame_36.show()
            self.HideShowButton.setText("Hide Menu")
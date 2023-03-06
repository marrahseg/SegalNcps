
import os
import pickle
import pyvista as pv
from pyvistaqt import QtInteractor
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from qt_material import apply_stylesheet
from Ui12_ui import Ui_MainWindow


motor_real = False

########################addres of All pic
my_Xside_pics_add = './MRI_PROJECT/MRI_FINAL_reza2/X_174/'
my_Yside_pics_add = './MRI_PROJECT/MRI_FINAL_reza2/Y_212/'
my_Zside_pics_add = './MRI_PROJECT/MRI_FINAL_reza2/Z_142/'


##########################linx _y,z plain
LINEX_XOFFSET_YPLAN = +157
LINEX_ZOFFSET_YPLAN = +45

LINEX_XOFFSET_ZPLAN = +156
LINEX_YOFFSET_ZPLAN = +45

########################liny _x,z plain
LINEY_YOFFSET_XPLAN = +145
LINEY_ZOFFSET_XPLAN = +45

LINEY_XOFFSET_ZPLAN = +156
LINEY_YOFFSET_ZPLAN = +52

##################3####linz _y,x plain
LINEZ_YOFFSET_XPLAN = +145
LINEZ_ZOFFSET_XPLAN = +45

LINEZ_XOFFSET_YPLAN = +156
LINEZ_ZOFFSET_YPLAN = +45

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
        self.timer = QTimer()
        # self.timer.start(500)
        # self.timer.stop(self)

        # self.mesh = pv.read('Brain for Half_Skull.stl')
        self.frame_23.setMaximumWidth(560)


        self.initAllpicture()
        self.signalsSlat()
        #self.dmodel()
        pv.set_plot_theme("dark")
        self.show_3Brain()


        self.x_now = 0
        self.y_now = 0
        self.z_now = 0

        self.x_go = 0
        self.y_go = 0
        self.z_go = 0

        self.onResetBotton()
        self.update_pics_lines_and_now_position(self.x_go, self.y_go, self.z_go)
        self.change_slider_Pos(self.x_go, self.y_go, self.z_go)
        # self.x_go = self.x_now - 1
        # self.y_go = self.y_now - 1
        # self.z_go = self.z_now - 1

    def signalsSlat(self):

        self.StartBotton.clicked.connect(self.onStartBottonClicked)
        self.Xslider.valueChanged.connect(self.onSliderchangeClicked)
        self.Yslider.valueChanged.connect(self.onSliderchangeClicked)
        self.Zslider.valueChanged.connect(self.onSliderchangeClicked)
        self.ResetButton.clicked.connect(self.onResetBotton)

        self.HideShowButton.clicked.connect(self.myHideShow)
        self.timer.timeout.connect(self.onTimer_interrupt)

        ###############################MENU BAR
        self.actionDark.triggered.connect(self.on_dark_theme)
        self.actionLight.triggered.connect(self.on_light_theme)
        self.actiondialog.triggered.connect(self.on_show_dialog)
        self.actionSave_as.triggered.connect(self.saveFigData)
        self.actionShow_Botten.triggered.connect(self.show_slider_onBrain)
        self.actionHide_Botton.triggered.connect(self.hide_slider_onBrain)

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


    ########## slots

    def show_3Brain(self):

        self.Brain_interactor = QtInteractor(self.frame_8)
        self.verticalLayout_38.addWidget(self.Brain_interactor.interactor)
        mesh = pv.read('Brain for Half_Skull.stl')
        self.Brain_interactor.add_mesh(mesh, color=(158, 158, 158))
        self.brain_point = self.Brain_interactor.add_sphere_widget(self.print_point, color=(183, 28, 28), center=(2, 36, 67),  radius=3, test_callback=False)

    def print_point(*args, **kwargs):
        print(args[1])

    def saveFigData(self):
        fileName = QFileDialog.getSaveFileName(self, 'Save Figure Data', '', 'pickle (*.seg)')
        if (fileName[0] == ''):
            return
        fileName = str(fileName[0])
        file_pi = open(fileName, 'wb')
        pickle.dump(self.figure, file_pi, -1)
        file_pi.close()
        return

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

    def show_slider_onBrain(self):
        self.slider_onBrain_z= self.Brain_interactor.add_slider_widget(None,  rng=[-43, 99], value=0, title="UpDown_z", pointa= (0.67, 0.1), pointb= (0.98, 0.1), style= 'modern')
        self.slider_onBrain_x=self.Brain_interactor.add_slider_widget(None,  rng=[-87, 86], value=0, title="RightLeft_x", pointa=(0.025, 0.1),pointb=(0.31, 0.1), style= 'modern')
        self.slider_onBrain_y=self.Brain_interactor.add_slider_widget(None,   rng=[-122, 90], value=0, title="FrontBack_y", pointa=(0.35, 0.1), pointb= (0.64, 0.1), style='modern')

    def hide_slider_onBrain(self):
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
        # print(self.picListY)

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
        # print(self.picListZ)

    def onSliderchangeClicked(self):
        _mx, _my, _mz = self.xyz_calculator(self.Xslider.value(), self.Yslider.value(), self.Zslider.value(), 0)
        self.update_pics_lines(_mx, _my, _mz)
        self.change_spin_vals(_mx, _my, _mz)

    def onStartBottonClicked(self):
        _mx, _my, _mz = self.xyz_calculator(self.Xspin.value(), self.Yspin.value(), self.Zspin.value(), 1)
        self.x_go = _mx
        self.y_go = _my
        self.z_go = _mz
        print("starting timer ....")
        self.timer.start(100)


        self.brain_point.SetCenter(20, 0, 100)

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



        # self.timer.start(100)
        self.update_pics_lines(_mx, _my, _mz)
        self.change_slider_Pos(_mx, _my, _mz)

        self.brain_point.SetCenter(-46, -13, 100)
        self.brain_point.SetCenter(-46, -13, 100)

    def onTimer_interrupt(self):
        _mx = 0
        _my = 0
        _mz = 0
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
                ################################# z check
                if self.z_now != self.z_go:
                    if self.z_now < self.z_go:
                        _mz = self.z_now + 1
                    else:
                        _mz = self.z_now - 1

                    self.update_pics_lines_and_now_position(_mx, _my, _mz)
                    self.change_slider_Pos(_mx, _my, _mz)
                else:
                    _mz = self.z_now
                    self.update_pics_lines_and_now_position(_mx, _my, _mz)
                    self.change_slider_Pos(_mx, _my, _mz)
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

    def change_slider_Pos(self, valX, valY, valZ):
        self.Xslider.setValue(valX)
        self.Yslider.setValue(valY)
        self.Zslider.setValue(valZ)

    def X_label_modifier(self, valX, valY, valZ):
        _ximg = QPixmap(my_Xside_pics_add + self.picListX[valX])
        self.pixmap_XX3 = QPixmap(self.Xpiclabel.size())

        dummy = abs(NUMBER_Z_LIST - 1 - valZ)
        dummy += LINEZ_ZOFFSET_XPLAN
        qpx = QPainter(self.pixmap_XX3)
        qpx.drawPixmap(self.Xpiclabel.rect(), _ximg)
        pen = QPen(Qt.red, 3)
        qpx.setPen(pen)
        qpx.drawLine(-600, dummy, 600, dummy)

        # vertical line,y
        myy_loc = abs(NUMBER_Y_LIST - 1 - valY)
        myy_loc += LINEY_YOFFSET_XPLAN
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
        dummy += LINEZ_ZOFFSET_YPLAN
        qpy.drawLine(-600, dummy, 600, dummy)

        ###########vert Line,x
        pen = QPen(Qt.green, 3)
        qpy.setPen(pen)
        dummy =  valX
        dummy += LINEX_XOFFSET_YPLAN
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
        dummy += LINEY_YOFFSET_ZPLAN
        self.qpz.setPen(pen)
        self.qpz.drawLine(-600, dummy, 600, dummy)

        ########## vertic,x
        pen = QPen(Qt.green, 3)
        self.qpz.setPen(pen)
        dummy = valX
        dummy += LINEX_XOFFSET_ZPLAN
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

    def change_spin_vals(self, valX, valY, valZ):
        self.Xspin.setValue(valX - X_PIC_OFFSET)
        self.Yspin.setValue(valY - Y_PIC_OFFSET)
        self.Zspin.setValue(valZ - Z_PIC_OFFSET)

    def myHideShow(self):
        if self.frame_36.isHidden() == False:
            self.frame_36.hide()
            self.HideShowButton.setText("Show Menu")
            print("closed")
        else:
            self.frame_36.show()
            self.HideShowButton.setText("Hide Menu")




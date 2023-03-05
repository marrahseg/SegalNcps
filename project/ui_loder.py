
import os
import pickle
import time

import numpy as np
import pyvista
import pyvista as pv
from PyQt5.uic.properties import QtWidgets
from pyvistaqt import QtInteractor

import stl
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtWidgets import QMainWindow, QLabel, QDialog, QMessageBox, QFileDialog
from pyqtgraph import Vector
from PyQt5 import QtCore, QtGui

from pyqtgraph.opengl import GLViewWidget, MeshData, GLMeshItem, GLLinePlotItem
from pyvista.examples import examples
from qt_material import apply_stylesheet

from Ui12_ui import Ui_MainWindow

motor_real = False

my_Xside_pics_add = './MRI_PROJECT/MRI_FINAL_reza2/X_174/'
my_Yside_pics_add = './MRI_PROJECT/MRI_FINAL_reza2/Y_212/'
my_Zside_pics_add = './MRI_PROJECT/MRI_FINAL_reza2/Z_142/'


#linx _y,z plain
LINEX_XOFFSET_YPLAN = +157
LINEX_ZOFFSET_YPLAN = +45

LINEX_XOFFSET_ZPLAN = +156
LINEX_YOFFSET_ZPLAN = +45

#liny _x,z plain
LINEY_YOFFSET_XPLAN = +145
LINEY_ZOFFSET_XPLAN = +45

LINEY_XOFFSET_ZPLAN = +156
LINEY_YOFFSET_ZPLAN = +52

#linz _y,x plain
LINEZ_YOFFSET_XPLAN = +145
LINEZ_ZOFFSET_XPLAN = +45

LINEZ_XOFFSET_YPLAN = +156
LINEZ_ZOFFSET_YPLAN = +45

#for set number of pic
X_PIC_OFFSET = 87
Y_PIC_OFFSET = 122
Z_PIC_OFFSET = 43

#number of list x,y ,z
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
        #self.timer = QtCore.QTimer()
        #self.timer.start(100)

        # self.mesh = pv.read('Brain for Half_Skull.stl')
        self.frame_23.setMaximumWidth(560)


        self.initAllpicture()
        self.signalsSlat()
        #self.dmodel()
        pv.set_plot_theme("dark")
        self.show_3Brain()


        self.XXX = 0
        self.YYY = 0
        self.ZZZ = 0

    def signalsSlat(self):

        self.StartBotton.clicked.connect(self.onStartBottonClicked)
        self.Xslider.valueChanged.connect(self.on_change_Xslider)
        self.Yslider.valueChanged.connect(self.on_change_Yslider)
        self.Zslider.valueChanged.connect(self.on_change_Zslider)
        self.ResetButton.clicked.connect(self.onResetBotton)

        self.HideShowButton.clicked.connect(self.myHideShow)
        #self.timer.timeout.connect(self.myOrbitBrain)




        # self.StartBotton.clicked.connect(self.onStartBottonClicked)
        # self.ResetButton.clicked.connect(self.onResetBotton)
        self.actionDark.triggered.connect(self.on_dark_theme)
        self.actionLight.triggered.connect(self.on_light_theme)
        self.actiondialog.triggered.connect(self.on_show_dialog)
        self.actionSave_as.triggered.connect(self.saveFigData)
        self.actionShow_Botten.triggered.connect(self.show_slider_onBrain)
        self.actionHide_Botton.triggered.connect(self.hide_slider_onBrain)

        # show defult pic in x
        pixmap1 = QPixmap(my_Xside_pics_add + self.picListX[0])
        w1 = self.Xpiclabel.width()
        h1 = self.Xpiclabel.height()
        pixmap1 = pixmap1.scaled(w1, h1, Qt.KeepAspectRatio)
        self.Xpiclabel.setPixmap(pixmap1)

        # show defult pic in y
        pixmap2 = QPixmap(my_Yside_pics_add + self.picListY[0])
        w2 = self.Ypiclabel.width()
        h2 = self.Ypiclabel.height()
        # print("w: ", w2, " h: ", h2)
        pixmap2 = pixmap2.scaled(w2, h2, Qt.KeepAspectRatio)
        self.Ypiclabel.setPixmap(pixmap2)

        # show defult pic in z
        pixmap3 = QPixmap(my_Zside_pics_add + self.picListZ[0])
        w3 = self.Zpiclabel.width()
        h3 = self.Zpiclabel.height()
        pixmap3 = pixmap3.scaled(w3, h3, Qt.KeepAspectRatio)
        self.Zpiclabel.setPixmap(pixmap3)
    ########## slots:



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
        #dlg.setDetailedText("salam")

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


    def on_xslider_change(self, val):
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa, on_xslider_change", val)
        self.X_label_modifier(val)
        self.move_lineX_plainZ(val)
        self.move_lineX_plainY(val)

    def on_yslider_change(self, val):
        print("maryammmmmmmmmmmmmmmm on_yslider_change: ", val)
        self.Y_label_modifier(val)
        self.move_lineY_plainX(val)
        self.move_lineY_plainZ(val)

    def on_zslider_change(self, val):
        self.Z_label_modifier(val)
        self.move_lineZ_plainX(val)
        self.move_lineZ_plainY(val)

    def initAllpicture(self):

        # sort of listX
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
        # print(self.picListX)


        # sort of listY
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

        # SORT OF LIST Z
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

    def myOrbitBrain(self):
        self.mview.orbit(5, 0)

    # def dmodel(self):
    #     self.mview = GLViewWidget(rotationMethod='quaternion')
    #     stl_mesh = stl.mesh.Mesh.from_file('Brain2.stl')
    #
    #     points = stl_mesh.points.reshape(-1, 3)
    #     faces = np.arange(points.shape[0]).reshape(-1, 3)
    #
    #     mesh_data = MeshData(vertexes=points, faces=faces)
    #     mesh = GLMeshItem(meshdata=mesh_data, smooth=True, drawFaces=True, drawEdges=True, edgeColor=(0, 0, 0, 76))
    #
    #     self.mview.opts['distance'] = 55.0
    #     self.mview.opts['center'] = Vector(15, 15, 0)
    #     self.mview.opts['fov'] = 60
    #     self.mview.opts['elevation'] = 15
    #     self.mview.opts['azimuth'] = 199
    #
    #     print("camera=", self.mview.cameraPosition())
    #
    #     self.mview.addItem(mesh)
    #     self.mview.setBackgroundColor(0, 0, 0)
    #     self.gridLayout_3.addWidget(self.mview, 0, 0, 1, 1)

    def onStartBottonClicked(self):
        _mx, _my, _mz = self.xyz_calculator(self.Xspin.value(), self.Yspin.value(), self.Zspin.value(), 1)
        # self.calculator_picNum_X_Y_Z()
        self.update_pics(_mx, _my, _mz)
        self.brain_point.SetCenter(20, 0, 100)
        # self.motor_drive()

    def onResetBotton(self):
        self.Xspin.setValue(0)
        self.Yspin.setValue(-14.41)
        self.Zspin.setValue(98)
        self.CAspin.setValue(0)
        self.OAspin.setValue(0)

        self.calculator_picNum_X_Y_Z()


        # self.Xslider.setValue(87)
        # self.X_label_modifier(87)
        #
        # self.Yslider.setValue(122 - 14.41)
        # self.Y_label_modifier(122 - 14.41)
        #
        #
        # self.Zslider.setValue(99 + 43)
        # self.Z_label_modifier(99 + 42)
        #
        # self.NoteBrowser.setText("Please insert your indexing")
        #
        #
        # self.brain_point.SetCenter(-46, -13, 100)

    #use not


    #for z slidr,x
    def move_lineZ_plainX(self, xloc_Zplain):
        dummy = abs(NUMBER_Z_LIST - 1 - xloc_Zplain)
        self.pixmapX_moveZ = QPixmap(my_Xside_pics_add + self.picListX[self.XXX])
        # self.pixmap_myx_img = self.pixmap_myx_img.scaled(w1, h1, Qt.KeepAspectRatio)
        self.pixmap_XX3 = QPixmap(self.Xpiclabel.size())
        # self.pixmap.fill(Qt.transparent)

        qpZ_onX = QPainter(self.pixmap_XX3)
        qpZ_onX.drawPixmap(self.Xpiclabel.rect(), self.pixmapX_moveZ)
        pen = QPen(Qt.red, 3)
        qpZ_onX.setPen(pen)
        qpZ_onX.drawLine(-600, dummy + LINEZ_ZOFFSET_XPLAN, 600, dummy + LINEZ_ZOFFSET_XPLAN)

        pen = QPen(Qt.green, 3)
        qpZ_onX.setPen(pen)
        dummy = abs(NUMBER_Y_LIST  - 1 - self.YYY)
        dummy += LINEZ_YOFFSET_XPLAN
        print("dummydummydummydummy: ", dummy)
        qpZ_onX.drawLine(dummy, -600, dummy, 600)
        qpZ_onX.end()

        self.Xpiclabel.setPixmap(self.pixmap_XX3)

    #for z slide,y
    def move_lineZ_plainY(self, yloc_Zplain):

        dummy = abs(NUMBER_Z_LIST - 1 - yloc_Zplain)
        self.pixmapY_moveZ = QPixmap(my_Yside_pics_add + self.picListY[self.YYY])
        self.pixmap_YY3 = QPixmap(self.Ypiclabel.size())

        # horiz line
        qpX_onY = QPainter(self.pixmap_YY3)
        qpX_onY.drawPixmap(self.Ypiclabel.rect(), self.pixmapY_moveZ)
        pen = QPen(Qt.red, 3)
        qpX_onY.setPen(pen)
        qpX_onY.drawLine(-600, dummy + LINEZ_ZOFFSET_YPLAN, 600, dummy + LINEZ_ZOFFSET_YPLAN)

        # vertic  line
        pen = QPen(Qt.green, 3)
        qpX_onY.setPen(pen)
        dummy = abs(NUMBER_X_LIST  - 1- self.XXX)
        dummy += LINEZ_XOFFSET_YPLAN
        qpX_onY.drawLine(dummy, -600, dummy, 600)
        qpX_onY.end()

        self.Ypiclabel.setPixmap(self.pixmap_YY3)

    #for X slide,y
    def move_lineX_plainY(self, yloc_Xplain):
        # yloc_Xplain = abs(173 - yloc_Xplain)
        self.pixmapY_moveX = QPixmap(my_Yside_pics_add + self.picListY[self.YYY])
        # self.pixmap_myx_img = self.pixmap_myx_img.scaled(w1, h1, Qt.KeepAspectRatio)
        self.pixmap_YY1 = QPixmap(self.Ypiclabel.size())

        # verig
        qpX_onY = QPainter(self.pixmap_YY1)
        qpX_onY.drawPixmap(self.Ypiclabel.rect(), self.pixmapY_moveX)
        linevert = QPen(Qt.green, 3)
        qpX_onY.setPen(linevert)
        qpX_onY.drawLine(yloc_Xplain + LINEX_XOFFSET_YPLAN, 500, yloc_Xplain + LINEX_XOFFSET_YPLAN, -500)

        # horiz
        dummy = abs(NUMBER_Z_LIST - 1 - self.ZZZ)
        dummy += LINEX_ZOFFSET_YPLAN
        linehoriz = QPen(Qt.red, 3)
        qpX_onY.setPen(linehoriz)
        qpX_onY.drawLine(-600, dummy, 600, dummy)
        qpX_onY.end()

        self.Ypiclabel.setPixmap(self.pixmap_YY1)

    # for X slide,z
    def move_lineX_plainZ(self, zloc_Xplain):

        self.pixmapZ_moveX = QPixmap(my_Zside_pics_add + self.picListZ[self.ZZZ])
        # self.pixmap_myx_img = self.pixmap_myx_img.scaled(w1, h1, Qt.KeepAspectRatio)
        self.pixmap_ZZ1 = QPixmap(self.Zpiclabel.size())
        # self.pixmap.fill(Qt.transparent)

        qpX_onZ = QPainter(self.pixmap_ZZ1)
        qpX_onZ.drawPixmap(self.Ypiclabel.rect(), self.pixmapZ_moveX)
        pen = QPen(Qt.green, 3)
        qpX_onZ.setPen(pen)
        qpX_onZ.drawLine(zloc_Xplain + LINEX_XOFFSET_ZPLAN, 500, zloc_Xplain + LINEX_XOFFSET_ZPLAN, -500)

        pen = QPen(Qt.red, 3)
        qpX_onZ.setPen(pen)
        dummy = abs(NUMBER_Y_LIST - 1 - self.YYY)
        dummy += LINEX_YOFFSET_ZPLAN
        qpX_onZ.drawLine(5, dummy, 600, dummy)

        qpX_onZ.end()

        self.Zpiclabel.setPixmap(self.pixmap_ZZ1)

    #for Y slide,x
    def move_lineY_plainX(self, xloc_Yplain):
        print("cccccccccccccccccc", xloc_Yplain)
        dummy = abs(NUMBER_Y_LIST - 1- xloc_Yplain)
        pixmapX_moveY = QPixmap(my_Xside_pics_add + self.picListX[self.XXX])
        pixmap_XX2 = QPixmap(self.Xpiclabel.size())
        # vertig
        qpY_onX = QPainter(pixmap_XX2)
        qpY_onX.drawPixmap(self.Xpiclabel.rect(), pixmapX_moveY)
        pen = QPen(Qt.green, 3)
        qpY_onX.setPen(pen)
        qpY_onX.drawLine(dummy + LINEY_YOFFSET_XPLAN, -600, dummy + LINEY_YOFFSET_XPLAN, 600)

        # horiz
        pen = QPen(Qt.red, 3)
        qpY_onX.setPen(pen)
        dummy = abs(NUMBER_Z_LIST - 1 - self.ZZZ)
        dummy += LINEY_ZOFFSET_XPLAN
        qpY_onX.drawLine(-600, dummy, 600, dummy)
        qpY_onX.end()

        self.Xpiclabel.setPixmap(pixmap_XX2)

    #for Y slide,z
    def move_lineY_plainZ(self, zloc_Yplain):
        dummy = abs(NUMBER_Y_LIST - 1 - zloc_Yplain)
        self.pixmapZ_moveY = QPixmap(my_Zside_pics_add + self.picListZ[self.ZZZ])
        # self.pixmap_myx_img = self.pixmap_myx_img.scaled(w1, h1, Qt.KeepAspectRatio)
        self.pixmap_ZZ2 = QPixmap(self.Zpiclabel.size())
        # self.pixmap.fill(Qt.transparent)



        qp = QPainter(self.pixmap_ZZ2)
        qp.drawPixmap(self.Zpiclabel.rect(), self.pixmapZ_moveY)
        pen = QPen(Qt.red, 3)
        qp.setPen(pen)
        qp.drawLine(-600, dummy + LINEY_YOFFSET_ZPLAN, 600, dummy + LINEY_YOFFSET_ZPLAN)

        pen = QPen(Qt.green, 3)
        qp.setPen(pen)
        dummy = abs(NUMBER_X_LIST - 1 - self.XXX)
        dummy += LINEY_XOFFSET_ZPLAN
        qp.drawLine(dummy, -600, dummy, 600)
        qp.end()

        self.Zpiclabel.setPixmap(self.pixmap_ZZ2)

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

    def calculator_picNum_X_Y_Z (self):

        # getvalueX
        valueBt = self.BTspinbox.value()
        print("valueBt", valueBt)
        _scaleX = valueBt / 174
        print("_scaleX:", _scaleX)
        valueX = self.Xspin.value()
        print("valueX:", valueX)
        # picNumX = int ((valueX * valueBt) / 174) + 87
        picNumX = int(valueX) + 87
        print("picNumX:", picNumX)

        # getvalueY
        valueAp = self.APspinbox.value()
        print("valueAp:", valueAp)
        _scaleY = valueAp / 212
        print("_scaleY:", _scaleY)
        valueY = self.Yspin.value()
        print("valueY:", valueY)
        # picNumY = int((valueY * valueAp) / 212) + 122
        picNumY = int(valueY) + 122
        # self.Yslidertest(picNumY)

        # getvaluez
        valueEv = self.EVspinbox.value()
        print("valueEv", valueEv)
        _scaleZ = valueEv / 142
        print("_scaleZ:", _scaleZ)
        valueZ = self.Zspin.value()
        print("valueZ:", valueZ)
        # picNumZ = int((valueZ * valueEv) / 142) + 43
        picNumZ = int(valueZ) + 43

        # executing on pictures
        # self.XXX = picNumX
        # self.YYY = picNumY
        # self.ZZZ = picNumZ


        _X = picNumX
        _Y = picNumY
        _Z = picNumZ



        print("salam", self.XXX, self.YYY, self.ZZZ)

        # change value of slider
        # self.Xslider.setValue(picNumX)
        # self.Yslider.setValue(picNumY)
        # self.Zslider.setValue(picNumZ)


        ############################################REZAA
        # self.move_lineX_plainZ(picNumX)
        # self.move_lineX_plainY(picNumX)

        mm_x = int(valueX * _scaleX)
        mm_y = int(valueY * _scaleY)
        mm_z = int(valueZ * _scaleZ)
        mm_a = int(self.OAspin.value())
        mm_b = int(self.CAspin.value())

        self.xlabelShow.setText(str("%.2f" % (valueX * _scaleX)))
        self.YlabelShow.setText(str("%.2f" % (valueY * _scaleY)))
        self.ZlabelShow.setText(str("%.2f" % (valueZ * _scaleZ)))
        self.OAlabelShow.setText(str(("%.2f" % self.OAspin.value())))
        self.CAlabelShow.setText(str(("%.2f" % self.CAspin.value())))

        self.brain_point.SetCenter(20, 0, 100)

        self.NoteBrowser.setText("Go to c point")

        return _X, _Y, _Z


        if motor_real:
            self.motor_set(0, -15, 98, 0, 0)
            time.sleep(0.5)
            self.motor_set(mm_x, mm_y, mm_z, mm_a, mm_b)



        # self.X_label_modifier(self.XXX, self.YYY, self.ZZZ)
        # self.Y_label_modifier(self.XXX, self.YYY, self.ZZZ)
        # self.Z_label_modifier(self.XXX, self.YYY, self.ZZZ)
        #
        # self.move_lineX_plainZ()
        # self.move_lineX_plainY()
        #
        # self.move_lineY_plainX()
        # self.move_lineY_plainZ()
        #
        # self.move_lineZ_plainX()
        # self.move_lineZ_plainY()



        # self.Xstring = str(picNumX)
        # self.Ystring = str(picNumY)
        # self.Zstring = str(picNumZ)
        # print('X,Y,Z string:', self.Xstring, self.Ystring, self.Zstring)

        # #get value of slider x,y,z
        # self.Xslidervlue  = self.Xslider.sliderMoved()
        # self.Yslideralue = self.Yslider.sliderMoved()
        # self.Zslidervalue = self.Zslider.sliderMoved()

    def on_change_Xslider(self, val):
        _mx, _my, _mz = self.xyz_calculator(val, self.Yslider.value(), self.Zslider.value(), 0)
        self.update_pics(_mx, _my, _mz)
        # self.calculator_picNum_X_Y_Z(val)
        # self.Xspin.setValue(self.XXX)

    def on_change_Yslider(self, val):
        _mx, _my, _mz = self.xyz_calculator(self.Xslider.value(), val, self.Zslider.value(), 0)
        self.update_pics(_mx, _my, _mz)


    def on_change_Zslider(self, val):
        _mx, _my, _mz = self.xyz_calculator(self.Xslider.value(), self.Yslider.value(), val, 0)
        self.update_pics(_mx, _my, _mz)






    def X_label_modifier(self, valX, valY, valZ):
        print("ssssssssssssssssssssssssssssssssss self.xxx = ", valX)
        self.Xspin.setValue(valX - X_PIC_OFFSET)

        w1 = self.Xpiclabel.width()
        h1 = self.Xpiclabel.height()

        self.pixmapX_moveZ = QPixmap(my_Xside_pics_add + self.picListX[valX])
        self.pixmapX_moveZ = self.pixmapX_moveZ.scaled(w1, h1, Qt.KeepAspectRatio)

        self.pixmap_XX3 = QPixmap(self.Xpiclabel.size())
        # self.pixmap.fill(Qt.transparent)

        # horiz line,z
        dummy = abs(NUMBER_Z_LIST - 1 - valZ)
        # dummy += 45
        #lineZ_zoffset_Xplane=45
        dummy += LINEZ_ZOFFSET_XPLAN
        qpx = QPainter(self.pixmap_XX3)
        qpx.drawPixmap(self.Xpiclabel.rect(), self.pixmapX_moveZ)
        pen = QPen(Qt.red, 3)
        qpx.setPen(pen)
        qpx.drawLine(-600, dummy, 600, dummy)

        # vertical line,y
        myy_loc = abs(NUMBER_Y_LIST - 1 - valY)
        # myy_loc += 145
        # lineY_yoffset_Xplane = +145
        myy_loc += LINEY_YOFFSET_XPLAN
        pen = QPen(Qt.green, 3)
        qpx.setPen(pen)
        print("myy_locmyy_locmyy_locmyy_loc: ", myy_loc)
        qpx.drawLine(myy_loc, 500, myy_loc, -500)
        qpx.end()

        self.Xpiclabel.setPixmap(self.pixmap_XX3)

        # self.move_lineX_plainZ(valX)
        # self.move_lineX_plainY(valX)

    def Y_label_modifier(self, valX, valY, valZ):

        self.Yspin.setValue(valY - Y_PIC_OFFSET)


        w1 = self.Ypiclabel.width()
        h1 = self.Ypiclabel.height()

        self.pixmapY_moveX = QPixmap(my_Yside_pics_add + self.picListY[valY])
        self.pixmapY_moveX = self.pixmapY_moveX.scaled(w1, h1, Qt.KeepAspectRatio)

        self.pixmap_YY1 = QPixmap(self.Ypiclabel.size())
        # self.pixmap.fill(Qt.transparent)

        #  horiz Line ,z
        qpy = QPainter(self.pixmap_YY1)
        qpy.drawPixmap(self.Ypiclabel.rect(), self.pixmapY_moveX)

        pen = QPen(Qt.red, 3)
        qpy.setPen(pen)
        dummy = abs(NUMBER_Z_LIST - 1 - valZ)
        # dummy += 45
        dummy += LINEZ_ZOFFSET_YPLAN
        qpy.drawLine(-600, dummy, 600, dummy)

        #  vert Line,x
        pen = QPen(Qt.green, 3)
        qpy.setPen(pen)
        dummy = abs(NUMBER_X_LIST - 1 - valX)
        # dummy += 156
        # lineX_xoffset_Yplane = +157
        dummy += LINEX_XOFFSET_YPLAN
        qpy.drawLine(dummy, 500, dummy, -500)
        qpy.end()

        self.Ypiclabel.setPixmap(self.pixmap_YY1)

        # self.move_lineY_plainX(valY)
        # self.move_lineY_plainZ(valY)

    def Z_label_modifier(self, valX, valY, valZ):

        self.Zspin.setValue(valZ - Z_PIC_OFFSET)

        w1 = self.Zpiclabel.width()
        h1 = self.Zpiclabel.height()
        self.pixmapZ_moveY = QPixmap(my_Zside_pics_add + self.picListZ[valZ])
        self.pixmapZ_moveX = self.pixmapZ_moveY.scaled(w1, h1, Qt.KeepAspectRatio)
        self.pixmap_ZZ2 = QPixmap(self.Zpiclabel.size())

        self.qpz = QPainter(self.pixmap_ZZ2)
        self.qpz.drawPixmap(self.Zpiclabel.rect(), self.pixmapZ_moveY)

        # horiz,y
        pen = QPen(Qt.red, 3)
        dummy = abs(NUMBER_Y_LIST - 1 - valY)
        # dummy += 45
        # lineY_yoffset_Zplane = +52
        dummy += LINEY_YOFFSET_ZPLAN
        self.qpz.setPen(pen)
        self.qpz.drawLine(-600, dummy, 600, dummy)

        # vertic,x
        pen = QPen(Qt.green, 3)
        self.qpz.setPen(pen)
        dummy = abs(NUMBER_X_LIST - 1 - valX)
        # dummy += 156
        dummy += LINEX_XOFFSET_ZPLAN
        self.qpz.drawLine(dummy, 500, dummy, -500)
        self.qpz.end()

        self.Zpiclabel.setPixmap(self.pixmap_ZZ2)

        # self.move_lineZ_plainX(valZ)
        # self.move_lineZ_plainY(valZ)

    def update_pics(self, valX, valY, valZ):
        self.X_label_modifier(valX, valY, valZ)
        self.Y_label_modifier(valX, valY, valZ)
        self.Z_label_modifier(valX, valY, valZ)

    def myHideShow(self):
        if self.frame_36.isHidden() == False:
            self.frame_36.hide()
            self.HideShowButton.setText("Show Menu")
            print("closed")
        else:
            self.frame_36.show()
            self.HideShowButton.setText("Hide Menu")




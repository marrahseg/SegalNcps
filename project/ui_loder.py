
import os
import time

import numpy as np
import stl
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtWidgets import QMainWindow, QLabel
from pyqtgraph import Vector
from PyQt5 import QtCore, QtGui

from pyqtgraph.opengl import GLViewWidget, MeshData, GLMeshItem, GLLinePlotItem

from Ui12_ui import Ui_MainWindow

my_Xside_pics_add = './MRI_PROJECT/MRI_FINAL_reza2/X_174/'
my_Yside_pics_add = './MRI_PROJECT/MRI_FINAL_reza2/Y_212/'
my_Zside_pics_add = './MRI_PROJECT/MRI_FINAL_reza2/Z_142/'



class Window_ui(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        self.CloseButton.hide()
        self.minimizedButton.hide()
        self.setWindowTitle("SEGAL NCPS")
        self.timer = QtCore.QTimer()

        self.timer.start(100)
        self.frame_23.setMaximumWidth(560)

        self.initAllpicture()
        self.signalsSlat()
        self.dmodel()


        self.XXX = 0
        self.YYY = 0
        self.ZZZ = 0

    def signalsSlat(self):

        self.Xslider.sliderMoved.connect(self.on_xslider_change)
        self.Yslider.sliderMoved.connect(self.on_yslider_change)
        self.Zslider.sliderMoved.connect(self.on_zslider_change)
        self.HideShowButton.clicked.connect(self.myHideShow)
        self.timer.timeout.connect(self.myOrbitBrain)
        self.StartBotton.clicked.connect(self.onStartBottonClicked)
        self.ResetButton.clicked.connect(self.onResetBotton)

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
    def on_xslider_change(self, val):
        self.Xslidertest(val)
        self.move_lineX_plainZ(val)
        self.move_lineX_plainY(val)


    def on_yslider_change(self, val):
        self.Yslidertest(val)
        self.move_lineY_plainX(val)
        self.move_lineY_plainZ(val)

    def on_zslider_change(self, val):
        self.Zslidertest(val)
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

    def dmodel(self):
        self.mview = GLViewWidget(rotationMethod='quaternion')
        stl_mesh = stl.mesh.Mesh.from_file('Brain2.stl')

        points = stl_mesh.points.reshape(-1, 3)
        faces = np.arange(points.shape[0]).reshape(-1, 3)

        mesh_data = MeshData(vertexes=points, faces=faces)
        mesh = GLMeshItem(meshdata=mesh_data, smooth=True, drawFaces=True, drawEdges=True, edgeColor=(0, 0, 0, 76))

        self.mview.opts['distance'] = 55.0
        self.mview.opts['center'] = Vector(15, 15, 0)
        self.mview.opts['fov'] = 60
        self.mview.opts['elevation'] = 15
        self.mview.opts['azimuth'] = 199

        print("camera=", self.mview.cameraPosition())

        self.mview.addItem(mesh)
        self.mview.setBackgroundColor(0, 0, 0)
        self.gridLayout_3.addWidget(self.mview, 0, 0, 1, 1)

    def onStartBottonClicked(self):

        #getvalueX
        valueBt = self.BTspinbox.value()
        print("valueBt", valueBt)
        _scaleX = valueBt / 174
        print("_scaleX:", _scaleX)
        valueX = self.Xspin.value()
        print("X valu:", valueX)
        # picNumX = int ((valueX * valueBt) / 174) + 87
        picNumX = int(valueX) + 87
        print("picNumX:", picNumX)

        self.Xslider.setValue(picNumX)
        self.on_xslider_change(picNumX)

        #getvalueY
        valueAp = self.APspinbox.value()
        print("valueAp:", valueAp)
        _scaleY = valueAp / 212
        print("_scaleY:", _scaleY)
        valueY = self.Yspin.value()
        print("valueY:", valueY)
        # picNumY = int((valueY * valueAp) / 212) + 122
        picNumY = int(valueY) + 122
        # self.Yslidertest(picNumY)
        self.Yslider.setValue(picNumY)
        self.on_yslider_change(picNumY)

        # getvaluez
        valueEv = self.EVspinbox.value()
        print("valueEv", valueEv)
        _scaleZ = valueEv / 142
        print("_scaleZ:", _scaleZ)
        valueZ = self.Zspin.value()
        print("valueZ:", valueZ)
        # picNumZ = int((valueZ * valueEv) / 142) + 43
        picNumZ = int(valueZ) + 43
        self.Zslider.setValue(picNumZ)
        self.on_zslider_change(picNumZ)


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


        self.NoteBrowser.setText("Go to c point")

        self.motor_set(0, -15, 98, 0, 0)
        time.sleep(0.5)
        self.motor_set(mm_x, mm_y, mm_z, mm_a, mm_b)

    def onResetBotton(self):
        self.CAspin.setValue(0)
        self.Xspin.setValue(0)
        self.Yspin.setValue(0)
        self.Zspin.setValue(0)
        self.OAspin.setValue(0)

        self.Xslider.setValue(87)
        self.Xslidertest(87)
        self.Yslider.setValue(122 - 14.41)
        self.Yslidertest(122 - 14.41)
        self.Zslider.setValue(99 + 43)
        self.Zslidertest(99 + 42)


        self.NoteBrowser.setText("Please insert your indexing")

    #for z slidr,x
    def move_lineZ_plainX(self, xloc_Zplain):
        xloc_Zplain = abs(141 - xloc_Zplain)
        self.pixmapX_moveZ = QPixmap(my_Xside_pics_add + self.picListX[self.XXX])
        # self.pixmap_myx_img = self.pixmap_myx_img.scaled(w1, h1, Qt.KeepAspectRatio)
        self.pixmap_XX3 = QPixmap(self.Xpiclabel.size())
        # self.pixmap.fill(Qt.transparent)

        qp = QPainter(self.pixmap_XX3)
        qp.drawPixmap(self.Xpiclabel.rect(), self.pixmapX_moveZ)
        pen = QPen(Qt.red, 3)
        qp.setPen(pen)
        qp.drawLine(10, xloc_Zplain+50, 600, xloc_Zplain+50)

        pen = QPen(Qt.green, 3)
        qp.setPen(pen)
        dummy = abs(211 - self.YYY)
        dummy += 45
        qp.drawLine(dummy, -600, dummy, 600)
        qp.end()

        self.Xpiclabel.setPixmap(self.pixmap_XX3)

    #for z slide,y
    def move_lineZ_plainY(self, yloc_Zplain):

        yloc_Zplain = abs(141 - yloc_Zplain)
        self.pixmapY_moveZ = QPixmap(my_Yside_pics_add + self.picListY[self.YYY])

        self.pixmap_YY3 = QPixmap(self.Ypiclabel.size())
        # self.pixmap.fill(Qt.transparent)
        # horiz line
        qp = QPainter(self.pixmap_YY3)
        qp.drawPixmap(self.Ypiclabel.rect(), self.pixmapY_moveZ)
        pen = QPen(Qt.red, 3)
        qp.setPen(pen)
        qp.drawLine(10, yloc_Zplain+45, 600, yloc_Zplain+45)
        # vertic  line
        pen = QPen(Qt.green, 3)
        qp.setPen(pen)
        dummy = abs(173 - self.XXX)
        dummy += 156
        qp.drawLine(dummy, -600, dummy, 600)


        qp.end()

        self.Ypiclabel.setPixmap(self.pixmap_YY3)

    #for X slide,y
    def move_lineX_plainY(self, yloc_Xplain):
        # yloc_Xplain = abs(173 - yloc_Xplain)
        self.pixmapY_moveX = QPixmap(my_Yside_pics_add + self.picListY[self.YYY])
        # self.pixmap_myx_img = self.pixmap_myx_img.scaled(w1, h1, Qt.KeepAspectRatio)
        self.pixmap_YY1 = QPixmap(self.Ypiclabel.size())

        # verig
        qp = QPainter(self.pixmap_YY1)
        qp.drawPixmap(self.Ypiclabel.rect(), self.pixmapY_moveX)
        linevert = QPen(Qt.green, 3)
        qp.setPen(linevert)
        qp.drawLine(yloc_Xplain+157, 500, yloc_Xplain+157, -500)

        # horiz
        dummy = abs(141 - self.ZZZ)
        dummy += 45
        linehoriz = QPen(Qt.red, 3)
        qp.setPen(linehoriz)
        qp.drawLine(-600, dummy, 600, dummy)
        qp.end()

        self.Ypiclabel.setPixmap(self.pixmap_YY1)

    # for X slide,z
    def move_lineX_plainZ(self, zloc_Xplain):
        # zloc_Xplain = abs(173 - zloc_Xplain)
        self.pixmapZ_moveX = QPixmap(my_Zside_pics_add + self.picListZ[self.ZZZ])
        # self.pixmap_myx_img = self.pixmap_myx_img.scaled(w1, h1, Qt.KeepAspectRatio)
        self.pixmap_ZZ1 = QPixmap(self.Zpiclabel.size())
        # self.pixmap.fill(Qt.transparent)

        qp = QPainter(self.pixmap_ZZ1)
        qp.drawPixmap(self.Ypiclabel.rect(), self.pixmapZ_moveX)
        pen = QPen(Qt.green, 3)
        qp.setPen(pen)
        qp.drawLine(zloc_Xplain+156, 500, zloc_Xplain+156, -500)

        pen = QPen(Qt.red, 3)
        qp.setPen(pen)
        dummy = abs(211 - self.YYY)
        dummy += 45
        qp.drawLine(5, dummy, 600, dummy)

        qp.end()

        self.Zpiclabel.setPixmap(self.pixmap_ZZ1)

    #for Y slide,x
    def move_lineY_plainX(self, xloc_Yplain):
        xloc_Yplain = abs(211 - xloc_Yplain)
        pixmapX_moveY = QPixmap(my_Xside_pics_add + self.picListX[self.XXX])
        pixmap_XX2 = QPixmap(self.Xpiclabel.size())
        # vertig
        qp = QPainter(pixmap_XX2)
        qp.drawPixmap(self.Xpiclabel.rect(), pixmapX_moveY)
        pen = QPen(Qt.green, 3)
        qp.setPen(pen)
        qp.drawLine(xloc_Yplain+145, 10, xloc_Yplain+145, 600)

        # horiz
        pen = QPen(Qt.red, 3)
        qp.setPen(pen)
        dummy = abs(141 - self.ZZZ)
        dummy += 45
        qp.drawLine(-600, dummy, 600, dummy)
        qp.end()

        self.Xpiclabel.setPixmap(pixmap_XX2)

    #for Y slide,z
    def move_lineY_plainZ(self, zloc_Yplain):
        zloc_Yplain = abs(211 - zloc_Yplain)
        self.pixmapZ_moveY = QPixmap(my_Zside_pics_add + self.picListZ[self.ZZZ])
        # self.pixmap_myx_img = self.pixmap_myx_img.scaled(w1, h1, Qt.KeepAspectRatio)
        self.pixmap_ZZ2 = QPixmap(self.Zpiclabel.size())
        # self.pixmap.fill(Qt.transparent)



        qp = QPainter(self.pixmap_ZZ2)
        qp.drawPixmap(self.Zpiclabel.rect(), self.pixmapZ_moveY)
        pen = QPen(Qt.red, 3)
        qp.setPen(pen)
        qp.drawLine(10, zloc_Yplain+52, 600, zloc_Yplain+52)

        pen = QPen(Qt.green, 3)
        qp.setPen(pen)
        dummy = abs(173 - self.XXX)
        dummy += 156
        qp.drawLine(dummy, -600, dummy, 600)
        qp.end()

        self.Zpiclabel.setPixmap(self.pixmap_ZZ2)

    def Xslidertest(self, val):
        self.XXX = int(val)
        self.Xspin.setValue(val - 87)

        w1 = self.Xpiclabel.width()
        h1 = self.Xpiclabel.height()

        self.pixmapX_moveZ = QPixmap(my_Xside_pics_add + self.picListX[val])
        self.pixmapX_moveZ = self.pixmapX_moveZ.scaled(w1, h1, Qt.KeepAspectRatio)

        self.pixmap_XX3 = QPixmap(self.Xpiclabel.size())
        # self.pixmap.fill(Qt.transparent)

        # horiz line
        dummy = abs(141 - self.ZZZ)
        dummy += 45
        self.qpx = QPainter(self.pixmap_XX3)
        self.qpx.drawPixmap(self.Xpiclabel.rect(), self.pixmapX_moveZ)
        pen = QPen(Qt.red, 3)
        self.qpx.setPen(pen)
        self.qpx.drawLine(-600, dummy, 600, dummy)

        # vertical line

        myy_loc = abs(211 - self.YYY) + 145
        pen = QPen(Qt.green, 3)
        self.qpx.setPen(pen)
        self.qpx.drawLine(myy_loc, 500, myy_loc, -500)

        self.qpx.end()

        self.Xpiclabel.setPixmap(self.pixmap_XX3)

        #for move line in y slider,Z img
        # self.move_lineX_plainY(val)
        # self.move_lineX_plainZ(val)

    def Yslidertest(self, val):
        val = int(val)
        self.YYY = val
        self.Yspin.setValue(val-122)

        w1 = self.Ypiclabel.width()
        h1 = self.Ypiclabel.height()

        self.pixmapY_moveX = QPixmap(my_Yside_pics_add + self.picListY[val])
        self.pixmapY_moveX = self.pixmapY_moveX.scaled(w1, h1, Qt.KeepAspectRatio)

        self.pixmap_YY1 = QPixmap(self.Ypiclabel.size())
        # self.pixmap.fill(Qt.transparent)

        #  horiz Line
        self.qpy = QPainter(self.pixmap_YY1)
        self.qpy.drawPixmap(self.Ypiclabel.rect(), self.pixmapY_moveX)

        pen = QPen(Qt.red, 3)
        self.qpy.setPen(pen)
        dummy = abs(141 - self.ZZZ)
        dummy += 45
        self.qpy.drawLine(-600, dummy, 600, dummy)

        #  vert Line
        pen = QPen(Qt.green, 3)
        self.qpy.setPen(pen)
        dummy = abs(173 - self.XXX)
        dummy += 156
        self.qpy.drawLine(dummy, 500, dummy, -500)
        self.qpy.end()

        self.Ypiclabel.setPixmap(self.pixmap_YY1)

        #for move line in x,z img
        # self.move_lineY_plainX(val)
        # self.move_lineY_plainZ(val)

    def Zslidertest(self, val):
        self.ZZZ = int(val)
        self.Zspin.setValue(val - 43)


        w1 = self.Zpiclabel.width()
        h1 = self.Zpiclabel.height()
        self.pixmapZ_moveY = QPixmap(my_Zside_pics_add + self.picListZ[val])
        self.pixmapZ_moveX = self.pixmapZ_moveY.scaled(w1, h1, Qt.KeepAspectRatio)
        self.pixmap_ZZ2 = QPixmap(self.Zpiclabel.size())


        self.qpz = QPainter(self.pixmap_ZZ2)
        self.qpz.drawPixmap(self.Zpiclabel.rect(), self.pixmapZ_moveY)
        # horiz
        pen = QPen(Qt.red, 3)
        dummy = abs(211 - self.YYY)
        dummy += 45
        self.qpz.setPen(pen)
        self.qpz.drawLine(10, dummy, 600, dummy)

        # vertic
        pen = QPen(Qt.green, 3)
        self.qpz.setPen(pen)
        dummy = abs(173 - self.XXX)
        dummy += 156
        self.qpz.drawLine(dummy, 500, dummy, -500)
        self.qpz.end()


        self.Zpiclabel.setPixmap(self.pixmap_ZZ2)

        # self.move_lineZ_plainX(val)
        # self.move_lineZ_plainY(val)

    def myRestore(self):
        self.restoreGeometry()

    def myHideShow(self):
        if self.frame_36.isHidden() == False:
            self.frame_36.hide()
            self.HideShowButton.setText("Show Menu")
            print("closed")
        else:
            self.frame_36.show()
            self.HideShowButton.setText("Hide Menu")

    #def myclick(self):
       # print("clicked")

        #pixmap1 = QPixmap('br1.jpg')
        #pixmap2 = QPixmap('br2.jpg')
        #pixmap3 = QPixmap('br3.jpg')

        #self.label_8.setPixmap(pixmap1)
        #self.label_9.setPixmap(pixmap2)
        #self.label_12.setPixmap(pixmap3)

    #def iniitUI(self):

        #self.setWindowTitle(self.title)
        #self.setGeometry(self.left,self.top,self.width,self.height)

        #label =QLabel(self)
        #pixmap1 =QPixmap("br1.jpg")
        #label.setPixmap(pixmap1)

        #label = QLabel(self)
        #pixmap2 = QPixmap("br2.jpg2")
        #label.setPixmap(pixmap2)

        #label = QLabel(self)
        #pixmap3 = QPixmap("br3.jpg")
        #label.setPixmap(pixmap3)
        #self.show()

    # def update_pics(self, posX, posY, posZ):
    #     if posX:
    #         self.Xslidertest(posX)
    #         self.move_lineX_plainZ(posX)
    #         self.move_lineX_plainY(posX)
    #     if posY:
    #         self.Yslidertest(posY)
    #         self.move_lineY_plainX(posY)
    #         self.move_lineY_plainZ(posY)
    #     if posZ:
    #         self.Zslidertest(posZ)
    #         self.move_lineZ_plainX(posZ)
    #         self.move_lineZ_plainY(posZ)

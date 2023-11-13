import configparser

import os
import pickle
import pyvista as pv
from PyQt5.uic.properties import QtCore, QtWidgets, QtGui

import Constants






from pyvistaqt import QtInteractor
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage, QFont, QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QWidget, QDialog, QLabel, QLineEdit
from qt_material import apply_stylesheet
from src.NCPSUI_ui import Ui_MainWindow
from patent_ui import Ui_Dialog
from RefHead_ui import Ui_Dialog as Ui_Dialog1
from unlock_ui import Ui_Form as Ui_Unlock
from unlockArea_ui import Ui_Form as Ui_UnlockArea
from standardarea_ui import Ui_Form as Ui_StandardArea
from PyQt5 import QtGui




motor_real = False


##############################read txt file
with open("../UI/defultvariable.txt", "r") as f:
    contents = f.read()
    # print(contents)
exec(contents)
############################################


class Window_ui(QMainWindow, Ui_MainWindow):


    def __init__(self,  parent=None):
        super().__init__(parent)
        os.getcwd()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("glog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setupUi(self)

        #######initial object  class Dialog #########
        self.my_dialog = MyDialog()
        self.my_dialog_head = MyDialogHead()
        self.my_Unlock = MyUnlock()
        self.my_UnlockArea = MyUnlockArea()
        self.my_StandardArea = MyStandardArea()
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

        # self.SetOffsetButton.clicked.connect(self.onChangeOffset)
        # self.ResetOffsetButton.clicked.connect(self.onResetOffset)
        self.actionShow_Offseting.triggered.connect(self.onMyHideOffseting)

        self.actionHidemenu.triggered.connect(self.onMyHideShow)
        self.timer.timeout.connect(self.onTimer_interrupt)
        self.actionChange_Offset.triggered.connect(self.onMyHideOffseting)


        ###############################>>>>>>>>>>>>>>>>>>>MENU BAR>>>>>>>>>>>>>>>>>>>>>############################
        self.actionDark.triggered.connect(self.on_dark_theme)
        self.actionLight.triggered.connect(self.on_light_theme)
        self.actiondialog.triggered.connect(self.on_show_dialog)
        self.actionSave_as.triggered.connect(self.onSaveFigData)
        self.actionShow.triggered.connect(self.onShow_slider_onBrain)
        self.actionHide.triggered.connect(self.onHide_slider_onBrain)


        # self.execuitButton.clicked.connect(self.onexecuit_head_size)
        ###########################################################################

        #############<<<<<>>>>>>>>>>>>>>Pation Information>>>>>>>>>>>#########
        self.CreateExamaction.triggered.connect(self.onCreate_dialog)
        self.OpenExamaction.triggered.connect(self.onLoad_Exam)
        self.my_dialog.SaveButton.clicked.connect(self.onSave_Pation_Info)
        self.my_dialog.CancelButton.clicked.connect(self.onCancel_Dialog)
        self.my_dialog.ExcuteButton.clicked.connect(self.onexecuit_head_size)
        self.my_dialog.SearchButton.clicked.connect(self.onfind_Pateint_by_id)
        #########pationmaneger


        ###########################>>>>>>>RefHead>>>>>>>#######################
        self.Refrenceheadaction.triggered.connect(self.onLock_Breaker)
        self.my_Unlock.UnLockButton.clicked.connect(self.onunlock_Successful)
        self.my_dialog_head.SetButton.clicked.connect(self.onSet_button_clicked)
        self.my_dialog_head.DefaultButton.clicked.connect(self.onDefault_button_clicked)
        ###########################>>>>>>>RefHead>>>>>>>#######################



        # self.Standardareaaction.triggered.connect(self.onLock_Breaker_Area)



        self.actionRegister_areas.triggered.connect(self.onLock_Breaker_Area)
        self.my_UnlockArea.UnLockButton.clicked.connect(self.onunlock_Successful_Area)

        self.actionStandard_area.triggered.connect(self.onLock_Breaker_Area)
        self.my_UnlockArea.UnLockButton.clicked.connect(self.onunlock_Successful_Area)




        self.pushButton.clicked.connect(self.onGoMotionRobot)






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

        icon4 = QIcon("../UI/button/unlocked.svg")
        self.my_Unlock.UnLockButton.setIcon(icon4)

        icon5 = QIcon("../UI/button/replay.svg")
        self.my_dialog_head.DefaultButton.setIcon(icon5)

        icon6 = QIcon("../UI/button/development.svg")
        self.my_dialog_head.SetButton.setIcon(icon6)

    def set_setting_ui(self):
        self.default_mode = False
        self.searchbox = False

        self.setWindowTitle("Segal Step")
        self.InformationtabWidget.setTabEnabled(2, False)
        self.InformationtabWidget.setTabText(2, "")

        self.my_Unlock.UnLocklineEdit.setEchoMode(QLineEdit.Password)
        self.my_UnlockArea.UnLocklineEdit.setEchoMode(QLineEdit.Password)
        self.my_dialog.setWindowTitle("My Custom Title")
        self.my_Unlock.setWindowTitle("Open Lock")
        self.my_dialog_head.setWindowTitle("Refrence head indices ")
        self.my_StandardArea.setWindowTitle("StandardArea")



        self.my_dialog.frame.setStyleSheet("border-color:#9E9E9E")
        self.my_dialog.frame_3.setStyleSheet("border-color:#9E9E9E")
        self.my_dialog.frame_4.setStyleSheet("border-color:#9E9E9E")





    def set_logo(self):
        pixiconimage = QPixmap("logo.png")
        pixiconimage = pixiconimage.scaled(260, 150, Qt.AspectRatioMode.KeepAspectRatio)
        # self.label.setPixmap(pixiconimage)

#وقتی روی دکمه کلیک کرد متنش عوض شه و اون عملیات 6 مرحله ای ربات راانجام دهد
    def onGoMotionRobot(self):
        self.counter += 1

        if self.counter == 1:
            self.pushButton.setText("Go to Reset")

        elif self.counter == 2:
            self.pushButton.setText("Enable Drag")

        elif self.counter == 3:
            self.pushButton.setText("Get X , Y")

        elif self.counter == 4:
            self.pushButton.setText("Get Z")

        elif self.counter == 5:
            self.pushButton.setText("Start")

        if self.counter == 5:
            self.counter = 0

    ################To Eneable the line edits for patient information
    def set_Enable_PatientDialog(self):
        self.my_dialog.Fullname.setEnabled(True)
        self.my_dialog.RightLeftHand.setEnabled(True)
        self.my_dialog.DateOfBrith.setEnabled(True)
        self.my_dialog.ApPatientSpin.setEnabled(True)
        self.my_dialog.BTPatientSpin.setEnabled(True)
        self.my_dialog.EvPatientSpin.setEnabled(True)
        self.my_dialog.textEditPatient.setEnabled(True)

######To disable the line edits for patient information
    def set_Disabled_PatientDialog(self):
        self.my_dialog.Fullname.setDisabled(True)
        self.my_dialog.RightLeftHand.setDisabled(True)
        self.my_dialog.DateOfBrith.setDisabled(True)
        self.my_dialog.ApPatientSpin.setDisabled(True)
        self.my_dialog.BTPatientSpin.setDisabled(True)
        self.my_dialog.EvPatientSpin.setDisabled(True)
        self.my_dialog.textEditPatient.setDisabled(True)

#########"When you click on this button, the measurements of the patient's head size will be uploaded here."##########
    def onexecuit_head_size(self):
            if self.searchbox == True:

                aa = self.my_dialog.BTPatientSpin.value()
                bb = self.my_dialog.EvPatientSpin.value()
                cc = self.my_dialog.ApPatientSpin.value()
                dd = self.my_dialog.Fullname.text()

                self.label_6.setText(dd)
                self.BTSpin.setValue(aa)
                self.EVSpin.setValue(bb)
                self.APSpin.setValue(cc)
            else:
                pass
#############################باز کردن قفل یرای standard area
    def onLock_Breaker_Area(self):
        self.my_UnlockArea.show()
####################وقتی دکمه ی NLOCK را زد این متد فعال شده و دیالوگ جدیدی باز میشود
    def onunlock_Successful_Area(self):
        if self.my_UnlockArea.UnLocklineEdit.text() == "s1996":
            self.my_UnlockArea.UnLocklineEdit.setText("")
            self.my_StandardArea.close()
            self.my_dialog_head.show_dialog()

        else:
            self.my_UnlockArea.close()

    def onCreate_dialog(self):
        self.my_dialog.SearchButton.hide()
        self.my_dialog.SaveButton.show()

        self.set_Enable_PatientDialog()
        self.my_dialog.show_dialog()

    def onCancel_Dialog(self):
        self.clearData_inPatientUi()
        self.my_dialog.close()


    #
    # def onExcute_patient_info(self):
    #     # a = int(self.my_dialog.BTPatientSpin.value())
    #     # b = int(self.my_dialog.EvPatientSpin.value())
    #     # c = int(self.my_dialog.ApPatientSpin.value())
    #     d = self.my_dialog.Fullname.text()
    #     self.label_6.setText(d)
    #
    #     self.my_dialog.close()
    #     #
    #     # self.BTSpin.setValue(a)
    #     # self.EVSpin.setValue(b)
    #     # self.APSpin.setValue(c)

    def onSave_Pation_Info(self):
        print("ssssssssssssssssssssssss")
        print(self.my_dialog.Fullname.text())
        Fullname = self.my_dialog.Fullname.text()
        SubjectID = self.my_dialog.SubjectID.text()
        Rlhande = self.my_dialog.RightLeftHand.text()
        DBO = self.my_dialog.DateOfBrith.text()
        ApPatient = self.my_dialog.ApPatientSpin.text()
        EvPatient = self.my_dialog.EvPatientSpin.text()
        BTPatient = self.my_dialog.BTPatientSpin.text()

        file_name = f"{SubjectID}{Fullname}.pickle"

        try:
            with open(file_name, "rb") as file:
                users = pickle.load(file)
        except FileNotFoundError:
            users = {}

        users[SubjectID] = {
            "fullname": Fullname,
            "subject_id": SubjectID,
            "right_left_hand": Rlhande,
            "DBO": DBO,
            "ap_patient": ApPatient,
            "ev_patient": EvPatient,
            "bt_patient": BTPatient
        }

        with open(file_name, "wb") as file:
            pickle.dump(users, file)

        self.clearData_inPatientUi()

        self.my_dialog.accept()


    def clearData_inPatientUi(self):
        self.my_dialog.Fullname.clear()
        self.my_dialog.SubjectID.clear()
        self.my_dialog.RightLeftHand.clear()
        self.my_dialog.DateOfBrith.clear()
        self.my_dialog.ApPatientSpin.setValue(0)
        self.my_dialog.EvPatientSpin.setValue(0)
        self.my_dialog.BTPatientSpin.setValue(0)
        self.my_dialog.textEditPatient.clear()


    def onLoad_Exam(self):
        self.my_dialog.SearchButton.show()
        self.my_dialog.SaveButton.hide()
        self.set_Disabled_PatientDialog()
        self.my_dialog.Fullname.setEnabled(True)
        self.my_dialog.show_dialog()

    def onfind_Pateint_by_id(self):

        PateintID = self.my_dialog.SubjectID.text()
        print(PateintID)

        Fullname = self.my_dialog.Fullname.text()


        filename = f"{PateintID}{Fullname}.pickle"


        try:
            with open(filename, "rb") as file:
                users = pickle.load(file)
                if PateintID in users:
                    self.set_Enable_PatientDialog()
                    self.my_dialog.Fullname.setProperty("text", users[PateintID]["fullname"])
                    self.my_dialog.RightLeftHand.setProperty("text", users[PateintID]["right_left_hand"])
                    self.my_dialog.DateOfBrith.setProperty("text", users[PateintID]["DBO"])
                    self.my_dialog.ApPatientSpin.setValue(int(users[PateintID]["ap_patient"]))
                    self.my_dialog.EvPatientSpin.setValue(int(users[PateintID]["ev_patient"]))
                    self.my_dialog.BTPatientSpin.setValue(int(users[PateintID]["bt_patient"]))
                    self.searchbox = True


                else:
                    return None

        except FileNotFoundError:
            print("فایل data.pickle پیدا نشد!")
            return





    ########################<<<<<<<<<<<<<<If the user clicks on the "Reference Head Indices",
    # this method displays the lock entry window.>>>>>########
    def onLock_Breaker(self):
        self.my_Unlock.show()

    ########>>>>>>>>>>>>>>>>>>>>>>>If the "Unlock" button is pressed and the correct
    # password is entered, the activation will be triggered>>>>>>>>>>>>>>>>####################
    def onunlock_Successful(self):
        if self.my_Unlock.UnLocklineEdit.text() == "s1996":
            self.my_Unlock.UnLocklineEdit.setText("")
            self.my_Unlock.close()
            self.my_dialog_head.show_dialog()

        else:
            self.my_Unlock.close()

    def onSet_button_clicked(self):
        self.default_mode = False
        BTIndices = self.my_dialog_head.RBTspinBox.value()
        EVIndices = self.my_dialog_head.REVspinBox.value()
        APIndices = self.my_dialog_head.RAPspinBox.value()
        print("hsffjgsgfs", BTIndices, EVIndices, APIndices)

        self.BTSpin.setValue(BTIndices)
        self.EVSpin.setValue(EVIndices)
        self.APSpin.setValue(APIndices)
        self.my_dialog_head.close()
        return BTIndices, EVIndices, APIndices


    def onDefault_button_clicked(self):
        self.default_mode = True
        self.BTSpin.setValue(174)
        self.EVSpin.setValue(142)
        self.APSpin.setValue(212)
        self.my_dialog_head.close()



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

        self.Brain_interactor.add_mesh(mesh , color = (158, 158, 158),specular= 0.7,
                                       specular_power=15, ambient=0.3, smooth_shading=True, opacity=1)

        # mesh = pv.read('../UI/brain for half - Brain for Half_Skull 1-1.STL')
        #
        # mesh2 = pv.read('../UI/brain for half - Brain for Half_Skull 2-1.STL')
        #
        # self.Brain_interactor.add_mesh(mesh2, color =(171, 71, 188), specular= 0.7,
        #                                specular_power=15, ambient=0.3, smooth_shading=True)


        self.Brain_interactor.background_color = (255, 255, 255)
        self.Brain_interactor.add_text("Segal NCPS   |   Navigated Coil Placement System",
                                       position='upper_edge', font='arial', font_size=5, color=(0, 0, 0))

        self.brain_point = self.Brain_interactor.add_sphere_widget(self.print_point, color=(183, 28, 28), center=(0, 0, 0),  radius=3, test_callback=False )

        print("center of point:", self.brain_point.SetCenter)


        #اضافه کردن کویل و محور ها
        self.Add_axes()
        self.Add_coil()



    def Add_axes(self):
        axes_actor = self.Brain_interactor.add_axes_at_origin(xlabel='Y', ylabel='X', zlabel='Z', line_width=3)
        axes_actor.GetXAxisCaptionActor2D().GetCaptionTextProperty().SetColor(0, 0, 0)
        axes_actor.GetYAxisCaptionActor2D().GetCaptionTextProperty().SetColor(0, 0, 0)
        axes_actor.GetZAxisCaptionActor2D().GetCaptionTextProperty().SetColor(0, 0, 0)

        # قرار دادن مرکز محور مختصات روی مرکز کره
        center = self.brain_point.GetCenter()
        axes_actor.SetOrigin(center[0], center[1], center[2])

        axes_actor.SetTotalLength(100, 100, 100)


    def Add_coil(self):
        center1 = [0, 45, 94]
        radius1 = 20
        height1 = 5

        # مشخصات استوانه دوم
        radius2 = radius1
        height2 = height1

        # محاسبه موقعیت مرکز استوانه دوم
        center2 = [center1[0] + radius1 + radius2, center1[1], center1[2]]

        # اضافه کردن استوانه اول
        cylinder1 = pv.Cylinder(center=center1, direction=[0, 0, 1], height=height1, radius=radius1, resolution=100)
        self.Brain_interactor.add_mesh(cylinder1, color=(0, 0, 0), opacity=0.5)

        # اضافه کردن استوانه دوم
        cylinder2 = pv.Cylinder(center=center2, direction=[0, 0, 1], height=height2, radius=radius2, resolution=100)
        self.Brain_interactor.add_mesh(cylinder2, color=(0, 0, 0), opacity=0.5)

        # تنظیم سطح جانبی استوانه‌ها به هم مماس
        side_surface1 = pv.Cylinder(center=center1, direction=[0, 0, 1], height=height1, radius=radius1, resolution=100)
        side_surface2 = pv.Cylinder(center=center2, direction=[0, 0, 1], height=height2, radius=radius2, resolution=100)

        # تنظیم پوشش سطح جانبی
        self.Brain_interactor.add_mesh(side_surface1, color=(0, 0, 0), opacity=0.5)
        self.Brain_interactor.add_mesh(side_surface2, color=(0, 0, 0), opacity=0.5)





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
        print("salam",_mx, _my, _mz)

        self.x_go = _mx
        self.y_go = _my
        self.z_go = _mz
        self.oa_go = _moa
        self.ca_go = _mca
        print("starting timer ....")
        self.NoteBrowser.setText("Go to Cpoint")


        # self.motor_set(self.x_go - self.x_go, self.y_go - self.y_go, self.z_go - self.z_go, self.oa_go - self.oa_now, self.ca_go - self.ca_now)
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


        self.x_go = _mx
        self.y_go = _my
        self.z_go = _mz
        # self.oa_go = _moa
        # self.ca_go = _mca


        self.update_pics_lines(_mx, _my, _mz)
        self.change_slider_Pos(_mx, _my, _mz)

    def  onStartWoMovementButton(self):
        _mx, _my, _mz = self.xyz_calculator(self.XSpin.value(), self.YSpin.value(), self.ZSpin.value(), 1)
        _moa = self.OASpin.value()
        _mca = self.CASpin.value()

        # self.x_go = _mx
        # self.y_go = _my
        # self.z_go = _mz
        # self.oa_go = _moa
        # self.ca_go = _mca

        self.NoteBrowser.setText("Go to Cpoint")

        self.update_pics_lines_and_now_position(_mx, _my, _mz)
        self.change_slider_Pos(_mx, _my, _mz)
        self.CAshowlabel.setText(str(_mca))
        self.OAshowlabel.setText(str(_moa))

    def onTimer_interrupt(self):
        _mx = 0
        _my = 0
        _mz = 0

        self.moveSphere(self.x_now, self.y_now, self.z_now)

        self.rectangle_actor.SetPosition(self.x_now, self.y_now, self.z_now)



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
                BTIndices ,EVIndices ,APIndices = self.onSet_button_clicked()

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

    # def xyz_calculator(self, mx, my, mz, scale_flag):
    #     if scale_flag:
    #         ######################################### calculate x value
    #         valueBt = self.BTSpin.value()
    #         _scaleX = valueBt / NUMBER_X_LIST
    #         _cx = int(mx) + X_PIC_OFFSET
    #         ######################################### calculate y value
    #         valueAp = self.APSpin.value()
    #         _scaleY = valueAp / NUMBER_Y_LIST
    #         _cy = int(my) + Y_PIC_OFFSET
    #         ######################################### calculate z value
    #         valueEv = self.EVSpin.value()
    #         _scaleZ = valueEv / NUMBER_Z_LIST
    #         _cz = int(mz) + Z_PIC_OFFSET
    #
    #     else:
    #         _cx = int(mx)
    #         _cy = int(my)
    #         _cz = int(mz)
    #
    #     return _cx, _cy, _cz
    #
    #
















    #
    # def xyz_calculator(self, mx, my, mz, scale_flag):
    #     if scale_flag:
    #         valueBt = self.BTSpin.value()
    #         valueAp = self.APSpin.value()
    #         valueEv = self.EVSpin.value()
    #
    #         if self.default_mode == True:
    #             BTIndices ,EVIndices ,APIndices = self.onSet_button_clicked()
    #
    #         else:
    #             BTIndices = NUMBER_X_LIST
    #             EVIndices = NUMBER_Y_LIST
    #             APIndices = NUMBER_Z_LIST
    #
    #         _scaleX = valueBt / BTIndices
    #         _scaleY = valueAp / EVIndices
    #         _scaleZ = valueEv / APIndices
    #
    #
    #
    #         _cx = int(mx) + X_PIC_OFFSET
    #         _cy = int(my) + Y_PIC_OFFSET
    #         _cz = int(mz) + Z_PIC_OFFSET
    #     else:
    #         _cx = int(mx)
    #         _cy = int(my)
    #         _cz = int(mz)
    #
    #     return _cx, _cy, _cz

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
        dummy += Constants.LINEZ_OFFSET_XPLAN
        pen = QPen(Qt.red, 3)
        qpx.setPen(pen)
        qpx.drawLine(-700, dummy, 700, dummy)

        # vertical line,y
        myy_loc = abs(NUMBER_Y_LIST - 1 - valY)
        myy_loc +=  Constants.LINEY_OFFSET_XPLAN
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
        dummy += Constants.LINEZ_OFFSET_YPLAN
        qpy.drawLine(-800, dummy, 800, dummy)

        ###########vert Line,x
        pen = QPen(Qt.green, 3)
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
        pen = QPen(Qt.red, 3)
        dummy = abs(NUMBER_Y_LIST - 1 - valY)
        dummy +=  Constants.LINEY_OFFSET_ZPLAN
        self.qpz.setPen(pen)
        self.qpz.drawLine(-800, dummy, 800, dummy)

        ########## vertic,x
        pen = QPen(Qt.green, 3)
        self.qpz.setPen(pen)
        dummy = valX
        dummy +=  Constants.LINEX_OFFSET_ZPLAN
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
            self.actionHideMenu.setText("Show Menu")

            print("closed")
        else:
            self.frame_3.show()
            self.actionHideMenu.setText("Hide Menu")

    def onMyHideOffseting(self):
        if self.OffsetinggroupBox.isHidden() == False:
            self.OffsetinggroupBox.hide()
            # self.HideMenuButton.setText("Show Menu")
            print("closed")
        else:
            self.OffsetinggroupBox.show()

##########################################Pation Information  dialog#############
class MyDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Segal Step")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("glog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.setupUi(self)

    def show_dialog(self):
        # apply_stylesheet(self, theme='../UI/dark_purp_segal.xml')
        apply_stylesheet(self, theme='../UI/reza_color.xml')
        self.exec_()

#################Locking the resizing of head  dialog#############
class MyUnlock(QWidget,Ui_Unlock):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Segal Step")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("glog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)


        self.setupUi(self)

    def show_dialog(self):
        # apply_stylesheet(self, theme='../UI/dark_purp_segal.xml')
        apply_stylesheet(self, theme='../UI/reza_color.xml')
        self.exec_()

##########################resizing of head  dialog#############
class MyDialogHead(QDialog, Ui_Dialog1):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Custom Title")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("glog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.setupUi(self)

    def show_dialog(self):
        # apply_stylesheet(self, theme='../UI/dark_purp_segal.xml')
        apply_stylesheet(self, theme='../UI/reza_color.xml')
        self.exec_()


class MyUnlockArea(QDialog, Ui_UnlockArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Custom Title")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("glog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.setupUi(self)

    def show_dialog(self):
        # apply_stylesheet(self, theme='../UI/dark_purp_segal.xml')
        apply_stylesheet(self, theme='../UI/reza_color.xml')
        self.exec_()



class MyUnlockArea(QDialog, Ui_UnlockArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Custom Title")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("glog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.setupUi(self)

    def show_dialog(self):
        # apply_stylesheet(self, theme='../UI/dark_purp_segal.xml')
        apply_stylesheet(self, theme='../UI/reza_color.xml')
        self.exec_()



class MyStandardArea(QDialog, Ui_StandardArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Custom Title")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("glog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.setupUi(self)

    def show_dialog(self):
        # apply_stylesheet(self, theme='../UI/dark_purp_segal.xml')
        apply_stylesheet(self, theme='../UI/reza_color.xml')
        self.exec_()





















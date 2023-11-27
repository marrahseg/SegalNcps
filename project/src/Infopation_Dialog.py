import pickle

from PyQt5.QtWidgets import QDialog
from PyQt5.uic.properties import QtGui
from qt_material import apply_stylesheet

from src.patent_ui  import Ui_Dialog



class PationInfo_Dialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Segal Step")
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap("../icons/logo/glog.png"))
        # self.setWindowIcon(icon)

        self.setupUi(self)

        self.SaveButton.clicked.connect(self.onSave_Pation_Info)
        self.CancelButton.clicked.connect(self.onCancel_Dialog)
        self.ExcuteButton.clicked.connect(self.onexecuit_head_size)
        self.SearchButton.clicked.connect(self.onfind_Pateint_by_id)

        self.frame.setStyleSheet("border-color:#9E9E9E")
        self.frame_3.setStyleSheet("border-color:#9E9E9E")
        self.frame_4.setStyleSheet("border-color:#9E9E9E")

    def show_dialog(self):
        # apply_stylesheet(self, theme='../UI/dark_purp_segal.xml')
        apply_stylesheet(self, theme='../UI/reza_color.xml')
        self.exec_()

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

    def onCancel_Dialog(self):
        self.clearData_inPatientUi()
        self.my_dialog.close()

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

    def set_Enable_PatientDialog(self):
        self.Fullname.setEnabled(True)
        self.RightLeftHand.setEnabled(True)
        self.DateOfBrith.setEnabled(True)
        self.ApPatientSpin.setEnabled(True)
        self.BTPatientSpin.setEnabled(True)
        self.EvPatientSpin.setEnabled(True)
        self.textEditPatient.setEnabled(True)

    def set_Disabled_PatientDialog(self):
        self.Fullname.setDisabled(True)
        self.RightLeftHand.setDisabled(True)
        self.DateOfBrith.setDisabled(True)
        self.ApPatientSpin.setDisabled(True)
        self.BTPatientSpin.setDisabled(True)
        self.EvPatientSpin.setDisabled(True)
        self.textEditPatient.setDisabled(True)

    def onCreate_dialog(self):
        self.SearchButton.hide()
        self.SaveButton.show()
        self.set_Enable_PatientDialog()
        self.show_dialog()

    def onLoad_Exam(self):
        self.SearchButton.show()
        self.SaveButton.hide()
        self.set_Disabled_PatientDialog()
        self.Fullname.setEnabled(True)
        self.show_dialog()

    def onCancel_Dialog(self):
        self.clearData_inPatientUi()
        self.close()

    def clearData_inPatientUi(self):
        self.Fullname.clear()
        self.SubjectID.clear()
        self.RightLeftHand.clear()
        self.DateOfBrith.clear()
        self.ApPatientSpin.setValue(0)
        self.EvPatientSpin.setValue(0)
        self.BTPatientSpin.setValue(0)
        self.textEditPatient.clear()



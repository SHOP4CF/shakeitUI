# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InfoDialogUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1026, 496)
        Dialog.setStyleSheet("QDialog{\n"
"    background-color: rgb(72, 110, 176);\n"
"}\n"
"\n"
"QLabel{\n"
"    font: 20pt \"Open Sans\";\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton{\n"
"    background-color: rgb(36, 55, 88);\n"
"    color: white;\n"
"    font: 20pt \"Open Sans\";\n"
"    min-height: 80px;\n"
"    min-width: 200px;\n"
"\n"
"    border-radius: 15px;\n"
"    border-top: 1px solid rgb(18, 28, 44);\n"
"    border-left: 1.5px solid  rgb(18, 28, 44);\n"
"    border-right: 1.5px solid  rgb(18, 28, 44);\n"
"    border-bottom: 2px solid rgb(18, 28, 44);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(18, 28, 44);\n"
"    border-top: 1px solid rgb(0, 0, 0);\n"
"    border-left: 1.5px solid  rgb(0,0,0);\n"
"    border-right: 1.5px solid  rgb(0,0,0);\n"
"    border-bottom: 2px solid rgb(0,0,0);\n"
" }")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 10, 919, 371))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setStyleSheet("font: bold 28pt \"Open Sans\";")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(21)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("font: italic 21pt \"Open Sans\";")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(125, 380, 781, 101))
        self.buttonBox.setStyleSheet("margin-left: 60px;\n"
"margin-right: 60px;")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Try to pick up more elements than the AI!"))
        self.label_2.setText(_translate("Dialog", "The elements will be automatically picked up by the robot when they are laying flat with no other elements near it.\n"
"Use the different shakes to get the elements into the correct position.\n"
"You have 60 seconds to pickup as many elements as you can. \n"
"Try beating the AI, the AI has a score of {} pickups."))
        self.label_3.setText(_translate("Dialog", "Are you ready?"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TimesUpDialogUI.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TimesUpDialog(object):
    def setupUi(self, TimesUpDialog):
        TimesUpDialog.setObjectName("TimesUpDialog")
        TimesUpDialog.resize(1020, 493)
        TimesUpDialog.setStyleSheet("QDialog{\n"
"    background-color: rgb(72, 110, 176);\n"
"}")
        self.verticalLayoutWidget = QtWidgets.QWidget(TimesUpDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(240, 20, 541, 441))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.frame_2 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.frame_2.setMinimumSize(QtCore.QSize(310, 100))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 100))
        self.frame_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(18, 28, 44);\n"
"border-radius: 15px;\n"
"\n"
"")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label1 = QtWidgets.QLabel(self.frame_2)
        self.label1.setGeometry(QtCore.QRect(20, 0, 251, 101))
        self.label1.setStyleSheet("font: bold 30pt \"Open Sans\";")
        self.label1.setObjectName("label1")
        self.yourScore = QtWidgets.QLabel(self.frame_2)
        self.yourScore.setGeometry(QtCore.QRect(290, 0, 231, 101))
        self.yourScore.setStyleSheet("font: 30pt \"Open Sans\";")
        self.yourScore.setObjectName("yourScore")
        self.verticalLayout.addWidget(self.frame_2)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(26)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.frame_3 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.frame_3.setMinimumSize(QtCore.QSize(310, 100))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 100))
        self.frame_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(36, 55, 88);\n"
"border-radius: 15px;\n"
"\n"
"")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label2 = QtWidgets.QLabel(self.frame_3)
        self.label2.setGeometry(QtCore.QRect(20, 0, 201, 101))
        self.label2.setStyleSheet("font: bold 30pt \"Open Sans\";")
        self.label2.setObjectName("label2")
        self.aiScore = QtWidgets.QLabel(self.frame_3)
        self.aiScore.setGeometry(QtCore.QRect(230, 0, 281, 101))
        self.aiScore.setStyleSheet("font: 30pt \"Open Sans\";")
        self.aiScore.setObjectName("aiScore")
        self.verticalLayout.addWidget(self.frame_3)

        self.retranslateUi(TimesUpDialog)
        QtCore.QMetaObject.connectSlotsByName(TimesUpDialog)

    def retranslateUi(self, TimesUpDialog):
        _translate = QtCore.QCoreApplication.translate
        TimesUpDialog.setWindowTitle(_translate("TimesUpDialog", "Dialog"))
        self.label_2.setText(_translate("TimesUpDialog", "Times up!"))
        self.label1.setText(_translate("TimesUpDialog", "Your score:"))
        self.yourScore.setText(_translate("TimesUpDialog", "# pickups"))
        self.label.setText(_translate("TimesUpDialog", "versus"))
        self.label2.setText(_translate("TimesUpDialog", "AI score:"))
        self.aiScore.setText(_translate("TimesUpDialog", "# pickups"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TimesUpDialog = QtWidgets.QDialog()
    ui = Ui_TimesUpDialog()
    ui.setupUi(TimesUpDialog)
    TimesUpDialog.show()
    sys.exit(app.exec_())

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QTimer
from TimesUpDialogUI import Ui_TimesUpDialog


class TimesUpDialog(QDialog):

    def __init__(self, player, ai, parent=None):
        super(TimesUpDialog, self).__init__(parent)
        self.ui = Ui_TimesUpDialog()
        self.ui.setupUi(self)

        self.ui.yourScore.setText("{} pickups".format(player))
        self.ui.aiScore.setText("{} pickups".format(ai))

        self.timer = QTimer(self)
        self.timer.setInterval(20000)  # closes after 20 seconds
        self.timer.timeout.connect(self.timeout)
        self.timer.start()

    def closeEvent(self, event):
        self.timer.stop()
        self.close()

    def timeout(self):
        self.close()

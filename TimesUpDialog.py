from PyQt5.QtWidgets import QDialog
from TimesUpDialogUI import Ui_TimesUpDialog
import time


class TimesUpDialogWindow:

    @staticmethod
    def launch(mainWindow, player, ai):
        dialog = QDialog(mainWindow)
        ui = Ui_TimesUpDialog()
        ui.setupUi(dialog)

        ui.yourScore.setText("{} pickups".format(player))
        ui.aiScore.setText("{} pickups".format(ai))

        dialog.open()

        return dialog.result()

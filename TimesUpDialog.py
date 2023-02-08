from PyQt5.QtWidgets import QDialog
from TimesUpDialogUI import Ui_TimesUpDialog


class TimesUpDialogWindow:

    @staticmethod
    def launch(mainWindow, player, ai):
        dialog = QDialog(mainWindow)
        ui = Ui_TimesUpDialog()
        ui.setupUi(dialog)

        ui.yourScore.setText(player + " pickups")
        ui.aiScore.setText(ai + " pickups")

        return dialog.exec_()

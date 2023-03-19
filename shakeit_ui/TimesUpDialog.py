from PyQt5.QtWidgets import QDialog
from shakeit_ui.TimesUpDialogUI import Ui_TimesUpDialog


class TimesUpDialogWindow:

    @staticmethod
    def launch(mainWindow, player, ai):
        dialog = QDialog(mainWindow)
        ui = Ui_TimesUpDialog()
        ui.setupUi(dialog)

        ui.yourScore.setText("{} pickups".format(player))
        ui.aiScore.setText("{} pickups".format(ai))

        return dialog.exec_()

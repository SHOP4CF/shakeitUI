from PyQt5.QtWidgets import QDialog
from shakeit_ui.ExitDialogUI import Ui_Exit


class ExitDialogWindow:

    @staticmethod
    def launch(mainWindow):
        # setting up UI #
        dialog = QDialog(mainWindow)
        ui = Ui_Exit()
        ui.setupUi(dialog)

        ui.buttonBox.accepted.connect(dialog.accept)
        ui.buttonBox.rejected.connect(dialog.reject)

        # return result
        return dialog.exec_()

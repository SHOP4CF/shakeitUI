from PyQt5.QtWidgets import QDialog
from ExitDialogUI import Ui_Exit


class ExitDialogWindow:

    @staticmethod
    def launch(main_window):
        # setting up UI #
        dialog = QDialog(main_window)
        ui = Ui_Exit()
        ui.setupUi(dialog)

        ui.buttonBox.accepted.connect(dialog.accept)
        ui.buttonBox.rejected.connect(dialog.reject)

        # return result
        return dialog.exec_()

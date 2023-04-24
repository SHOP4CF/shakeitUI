from PyQt5.QtWidgets import QDialog
from InfoDialogUI import Ui_Dialog


class InfoDialogWindow:

    @staticmethod
    def launch(main_window, ai):
        # setting up UI #
        dialog = QDialog(main_window)
        ui = Ui_Dialog()
        ui.setupUi(dialog)

        string = ui.label_2.text().format(ai)
        ui.label_2.setText(string)

        ui.buttonBox.accepted.connect(dialog.accept)
        ui.buttonBox.rejected.connect(dialog.reject)

        # return result
        return dialog.exec_()

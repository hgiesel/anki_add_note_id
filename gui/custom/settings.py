from aqt import QDialog, QLayout

from ..settings_ui import Ui_Settings

class Settings(QDialog):
    def __init__(self, mw, callback):
        super().__init__(parent=mw)

        self.mw = mw

        self.ui = Ui_Settings()
        self.ui.setupUi(self)

        self.cb = callback

        self.layout().setSizeConstraint(QLayout.SetFixedSize)

    def setupUi(self, reduceNoteId, copyNoteId):
        self.ui.reduceNoteId.setChecked(reduceNoteId)
        self.ui.copyNoteId.setChecked(copyNoteId)

    def accept(self):
        reduce = self.ui.reduceNoteId.isChecked()
        copy = self.ui.copyNoteId.isChecked()

        self.cb(reduce, copy)
        super().accept()

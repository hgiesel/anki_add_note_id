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

    def setupUi(self, keepNoteId, copyNoteId):
        self.ui.keepNoteId.setChecked(keepNoteId)
        self.ui.copyNoteId.setChecked(copyNoteId)

    def accept(self):
        keep = self.ui.keepNoteId.isChecked()
        copy = self.ui.copyNoteId.isChecked()

        self.cb(keep, copy)
        super().accept()

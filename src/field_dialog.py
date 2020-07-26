from PyQt5 import QtWidgets

from aqt import AnkiQt
from aqt.fields import FieldDialog

from anki.models import NoteType
from anki.hooks import wrap


def init_noteid_option(self):
    noteid_cb = QtWidgets.QCheckBox('Insert note id (overwrites current content!)')

    self.form.noteid = noteid_cb
    self.form._2.addWidget(self.form.noteid, 4, 1)

def save_noteid_option(self):
    # boilerplate
    if self.currentIdx is None:
        return
    idx = self.currentIdx
    fld = self.model['flds'][idx]
    f = self.form

    noteid = f.noteid.isChecked()
    if 'noteid' not in fld or fld['noteid'] != noteid:
        fld['noteid'] = noteid
        self.change_tracker.mark_basic()

def load_noteid_option(self, idx):
    self.currentIdx = idx
    fld = self.model['flds'][idx]
    f = self.form
    f.noteid.setChecked(fld['noteid'] if 'noteid' in fld else False)

def add_noteid_to_notes(self):
    # mid = self.model['id']
    from aqt.utils import showText
    mid = self.model['id']
    nids = self.col.db.list(f'select id from notes where mid == {mid}')

    for nid in nids:
        note = self.col.getNote(nid)
        flds = self.model['flds']

        for id, fld in enumerate(flds):
            if 'noteid' in fld and fld['noteid']:
                note.fields[id] = str(note.id)

        note.flush()

def init_field_dialog():
    # setupSignals is called before executing QDialog
    FieldDialog.setupSignals = wrap(FieldDialog.setupSignals, init_noteid_option, 'after')

    FieldDialog.saveField = wrap(FieldDialog.saveField, save_noteid_option, 'after')
    FieldDialog.loadField = wrap(FieldDialog.loadField, load_noteid_option, 'after')

    FieldDialog.accept = wrap(FieldDialog.accept, add_noteid_to_notes, 'after')

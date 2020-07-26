from PyQt5 import QtWidgets
from typing import Optional

from aqt import AnkiQt
from aqt.fields import FieldDialog
from aqt.gui_hooks import state_did_reset

from anki.models import NoteType
from anki.hooks import wrap

def init_noteid_option(self):
    noteid_cb = QtWidgets.QCheckBox('Insert note id (overwrites current content!)')

    self.form.noteid = noteid_cb
    self.form._2.addWidget(self.form.noteid, 4, 1)

def bools_to_meta_state(noteid: bool) -> Optional[str]:
    if noteid:
        return 'noteid'

    return None

def save_noteid_option(self):
    # boilerplate
    if self.currentIdx is None:
        return
    idx = self.currentIdx
    fld = self.model['flds'][idx]
    f = self.form

    meta = bools_to_meta_state(f.noteid.isChecked())
    if 'meta' not in fld or fld['meta'] != meta:
        fld['meta'] = meta
        self.change_tracker.mark_basic()

def load_noteid_option(self, idx):
    self.currentIdx = idx
    fld = self.model['flds'][idx]
    f = self.form
    f.noteid.setChecked(fld['meta'] == 'noteid' if 'meta' in fld else False)

def add_upon_reset(self):
    def add_noteids():
        mid = self.model['id']
        nids = self.col.db.list(f'select id from notes where mid == {mid}')
        flds = self.model['flds']

        for id, fld in enumerate(flds):
            if 'meta' in fld and fld['meta'] == 'noteid':
                for nid in nids:
                    note = self.col.getNote(nid)
                    note.fields[id] = str(note.id)

                    note.flush()

        state_did_reset.remove(add_noteids)

    state_did_reset.append(add_noteids)

def init_field_dialog():
    # setupSignals is called before executing QDialog
    FieldDialog.setupSignals = wrap(FieldDialog.setupSignals, init_noteid_option, 'after')

    FieldDialog.saveField = wrap(FieldDialog.saveField, save_noteid_option, 'after')
    FieldDialog.loadField = wrap(FieldDialog.loadField, load_noteid_option, 'after')

    FieldDialog.accept = wrap(FieldDialog.accept, add_upon_reset, 'before')

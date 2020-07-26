from random import choice
from string import hexdigits

from aqt import mw, dialogs
from aqt.gui_hooks import (
    add_cards_will_add_note,
    add_cards_did_add_note,
    editor_did_load_note,
)

def make_unique_for_dupe_check(problem, note):
    flds = note.model()['flds']

    random_string = ''.join(choice(hexdigits) for i in range(30))

    for id, fld in enumerate(flds):
        if 'noteid' in fld and fld['noteid']:
            note.fields[id] = random_string

    ret = note.dupeOrEmpty()
    if ret != 1:
        problem = None

    return problem

def fill_with_noteid(note):
    flds = note.model()['flds']

    for id, fld in enumerate(flds):
        if 'noteid' in fld and fld['noteid']:
            note.fields[id] = str(note.id)

    note.flush()

def get_hider_js(id: int):
    return f"""
        document.body.querySelector("#f{id}").style.display = "none"
        document.body.querySelector("#name{id}").style.display = "none"
    """

def hide_noteid_fields(editor):
    if editor.addMode:
        flds = editor.note.model()['flds']

        for id, fld in enumerate(flds):
            if 'noteid' in fld and fld['noteid']:
                editor.web.eval(get_hider_js(id))

def init_addcards():
    add_cards_will_add_note.append(make_unique_for_dupe_check)
    add_cards_did_add_note.append(fill_with_noteid)
    editor_did_load_note.append(hide_noteid_fields)
